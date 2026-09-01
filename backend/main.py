"""
DebugMate AI -- Backend

Thin FastAPI layer: HTTP routes, request validation, CORS, error mapping.
All AI logic (prompting, RAG, guardrails, the LLM call) lives in
ai_engine/ -- this file only imports and calls into it.

ai_engine's internal modules use plain imports (e.g. `from gateway_client
import ...`) written to be run from inside ai_engine/ itself, so we add
that directory to sys.path before importing -- this avoids touching
ai_engine's already-tested internals.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- wire up ai_engine as an importable sibling package -------------------
AI_ENGINE_DIR = Path(__file__).resolve().parent.parent / "ai_engine"
if str(AI_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(AI_ENGINE_DIR))

from analyze import AnalysisError, analyze as ai_analyze  # noqa: E402
from feedback import FeedbackError, evaluate_practice_answer  # noqa: E402
from gateway_client import GatewayError  # noqa: E402
from guardrails import GuardrailViolation  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debugmate.backend")

app = FastAPI(title="DebugMate AI", version="0.1.0")

# --- Fixed: Cleaned up terminal snippet garbage (;31R) and fixed variable assignment ---
_allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://debugmate.baalebo.xyz"]
if os.getenv("FRONTEND_ORIGIN"):
    _allowed_origins.append(os.getenv("FRONTEND_ORIGIN"))

# Fixed typo here: Changed allow_origins from 'origins' to '_allowed_origins'
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- global exception handler to guarantee CORS headers on error responses ---
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Guarantees that error responses still receive appropriate CORS headers
    and follow the schema requested by debugService.js
    """
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail} if isinstance(exc.detail, dict) else {"detail": {"message": str(exc.detail)}}
    )
    
    # Manually append CORS headers to error outputs to prevent preflight blocks
    origin = request.headers.get("origin")
    if origin in _allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
    return response


# --- request/response models, matching the frontend's actual contract -----

class AnalyzeRequest(BaseModel):
    language: str = Field(default="Python")
    code: str = Field(default="")
    error_message: str = Field(default="", alias="error_message")
    intended_behavior: Optional[str] = None

    class Config:
        populate_by_name = True


class AnalyzeResponse(BaseModel):
    error_type: str
    what_happened: str
    likely_causes: list[str]
    debugging_steps: list[str]
    possible_fix: str
    fix_explanation: str
    learning_topic: str
    practice_challenge: str


class PracticeFeedbackRequest(BaseModel):
    challenge: str = Field(..., min_length=1)
    user_answer: str = Field(..., min_length=1)


class PracticeFeedbackResponse(BaseModel):
    correct: bool
    feedback: str


def _error_body(message: str) -> dict:
    """
    Frontend reads errors as body.detail.message (see debugService.js),
    so every HTTPException here uses this shape instead of a plain string.
    """
    return {"message": message}


@app.get("/health")
async def health():
    return {"status": "welcome to debugmate"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    try:
        result = await ai_analyze(
            language=req.language,
            code=req.code,
            error=req.error_message,
            intended_behavior=req.intended_behavior,
        )
    except GuardrailViolation as exc:
        raise HTTPException(status_code=400, detail=_error_body(str(exc))) from exc
    except (AnalysisError, GatewayError) as exc:
        logger.error("Analysis failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=_error_body("We couldn't analyze your error right now. Please try again."),
        ) from exc

    return AnalyzeResponse(**result)


@app.post("/practice-feedback", response_model=PracticeFeedbackResponse)
async def practice_feedback(req: PracticeFeedbackRequest):
    try:
        result = await evaluate_practice_answer(req.challenge, req.user_answer)
    except (FeedbackError, GatewayError) as exc:
        logger.error("Practice feedback failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=_error_body("We couldn't check your answer right now. Please try again."),
        ) from exc

    return PracticeFeedbackResponse(**result)

