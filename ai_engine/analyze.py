"""
DebugMate AI Engine.

This module owns ONLY the AI-side responsibility: prompt construction,
calling the LLM (via nexus-ai-gateway), parsing/validating structured
output, RAG grounding, and guardrails.

It knows nothing about HTTP, routes, or CORS -- that's the Backend's job.
Backend imports `analyze()` and calls it from whatever endpoint it defines.
"""

import json
import re

from gateway_client import GatewayClient, GatewayError
from guardrails import is_likely_out_of_scope, validate_input
from prompts import SYSTEM_PROMPT, build_user_prompt
from rag.retrieval import format_for_prompt, retrieve

REQUIRED_KEYS = {
    "error_type",
    "what_happened",
    "likely_causes",
    "debugging_steps",
    "possible_fix",
    "fix_explanation",
    "learning_topic",
    "practice_challenge",
}

# These two must be arrays -- everything else in REQUIRED_KEYS is a string.
LIST_KEYS = {"likely_causes", "debugging_steps"}


class AnalysisError(Exception):
    """Raised when the AI Engine can't produce a valid structured result.
    Backend decides how to turn this into an HTTP response."""


def _extract_json(raw_text: str) -> dict:
    """
    Models sometimes wrap JSON in markdown fences or add stray text around
    it despite instructions. Strip fences, then find the first {...} block.
    """
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise AnalysisError("Could not parse a JSON object out of the model's response")


async def analyze(
    language: str,
    code: str,
    error: str,
    intended_behavior: str | None = None,
) -> dict:
    """
    The single entry point Backend should call.

    Returns a dict with exactly the 7 required keys, all strings.
    Raises AnalysisError, GuardrailViolation, or GatewayError on failure --
    Backend catches these and maps them to whatever HTTP status codes it wants.
    """
    # Guardrail: reject unusable/oversized input before spending a call.
    validate_input(language, code, error)

    user_prompt = build_user_prompt(language, code, error, intended_behavior)

    # RAG: ground the answer in curated knowledge base content when a
    # relevant match exists. No match = no reference block, model relies
    # on its own knowledge as before -- this never blocks a response.
    retrieved = retrieve(error)
    reference_block = format_for_prompt(retrieved)
    if reference_block:
        user_prompt = f"{user_prompt}\n\n{reference_block}"

    if is_likely_out_of_scope(retrieved, error):
        user_prompt += (
            "\n\nNote: this request doesn't clearly look like a Python "
            "error. If it isn't, say so directly rather than inventing "
            "an analysis."
        )

    client = GatewayClient()
    raw_text = await client.chat(SYSTEM_PROMPT, user_prompt, mode="auto")

    parsed = _extract_json(raw_text)

    missing = REQUIRED_KEYS - parsed.keys()
    if missing:
        raise AnalysisError(f"AI response was missing expected fields: {sorted(missing)}")

    result = {}
    for key in REQUIRED_KEYS:
        value = parsed[key]
        if key in LIST_KEYS:
            # Models sometimes return a single string instead of a
            # one-item list despite instructions -- normalize rather
            # than reject, since the frontend just needs an array.
            if isinstance(value, str):
                value = [value]
            result[key] = [str(item) for item in value]
        else:
            result[key] = str(value)

    return result
