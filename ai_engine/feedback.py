"""
Practice mode feedback -- Week 9 deliverable.

Takes the practice_challenge from analyze()'s output plus the user's
attempted answer, and returns feedback via the LLM. Kept separate from
analyze() since it's a distinct interaction, not part of the initial
error analysis.
"""

import json
import re

from gateway_client import GatewayClient, GatewayError

FEEDBACK_SYSTEM_PROMPT = """You are DebugMate's practice-mode tutor.

You were given a small coding challenge and a beginner's attempted answer.
Evaluate it kindly and usefully -- beginners need encouragement, not just
correctness scoring.

Respond with ONLY a single JSON object, no markdown fences, no commentary:

{
  "correct": true or false,
  "feedback": "specific, encouraging feedback on their answer -- what they got right, what to adjust if anything"
}
"""


class FeedbackError(Exception):
    """Raised when feedback can't be produced or parsed."""


def _extract_json(raw_text: str) -> dict:
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
    raise FeedbackError("Could not parse feedback JSON from the model's response")


async def evaluate_practice_answer(challenge: str, user_answer: str) -> dict:
    """
    Returns {"correct": bool, "feedback": str}.
    Raises FeedbackError or GatewayError on failure.
    """
    if not user_answer.strip():
        raise FeedbackError("User answer cannot be empty.")

    user_prompt = f"Challenge given:\n{challenge}\n\nUser's answer:\n{user_answer}"

    client = GatewayClient()
    raw_text = await client.chat(FEEDBACK_SYSTEM_PROMPT, user_prompt, mode="auto")

    parsed = _extract_json(raw_text)
    if "correct" not in parsed or "feedback" not in parsed:
        raise FeedbackError(f"Feedback response missing expected fields: {parsed}")

    return {"correct": bool(parsed["correct"]), "feedback": str(parsed["feedback"])}
