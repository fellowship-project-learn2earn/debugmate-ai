"""
Guardrails -- Week 10 deliverable.

Two jobs:
1. Protect the AI Engine's own cost/token budget with sane input limits,
   regardless of what validation Backend also does on its side.
2. Flag likely out-of-scope requests (not debugging-related) before
   spending a gateway call on them.

Kept deliberately simple/rule-based for the MVP -- the doc explicitly
warns against over-building. A full classifier is not justified here.
"""

MAX_CODE_LENGTH = 8000
MAX_ERROR_LENGTH = 4000

# Signals that a "code" submission is trying to get something executed
# rather than analyzed -- the system prompt already forbids execution,
# this is a second layer of defense that also gets logged for review.
_EXECUTION_REQUEST_PHRASES = [
    "run this code",
    "execute this",
    "please run",
    "run it for me",
]


class GuardrailViolation(Exception):
    """Raised when input fails validation before ever reaching the LLM."""


def validate_input(language: str, code: str, error: str) -> None:
    """Raises GuardrailViolation if input is unusable or oversized."""
    if not code.strip():
        raise GuardrailViolation("Code cannot be empty.")
    if not error.strip():
        raise GuardrailViolation("Error message cannot be empty.")
    if len(code) > MAX_CODE_LENGTH:
        raise GuardrailViolation(
            f"Code is too long ({len(code)} chars, max {MAX_CODE_LENGTH}). "
            "Trim to the relevant section."
        )
    if len(error) > MAX_ERROR_LENGTH:
        raise GuardrailViolation(
            f"Error message is too long ({len(error)} chars, max {MAX_ERROR_LENGTH})."
        )


def looks_like_execution_request(code: str, intended_behavior: str | None) -> bool:
    """
    Heuristic check: does the submission look like it's asking us to run
    the code, rather than analyze the error? Used for logging/flagging,
    not a hard block -- the system prompt is the primary defense.
    """
    combined = f"{code} {intended_behavior or ''}".lower()
    return any(phrase in combined for phrase in _EXECUTION_REQUEST_PHRASES)


def is_likely_out_of_scope(retrieved_docs: list[dict], error: str) -> bool:
    """
    If RAG retrieval found nothing relevant AND the error text doesn't
    look like a Python traceback at all, this is likely not a real
    debugging request. Used to add a note, not to hard-block --
    false positives are worse than a slightly generic answer.
    """
    if retrieved_docs:
        return False
    traceback_markers = ["error", "exception", "traceback", "line "]
    return not any(marker in error.lower() for marker in traceback_markers)
