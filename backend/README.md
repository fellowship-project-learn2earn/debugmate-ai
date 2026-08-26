# DebugMate AI -- Backend

FastAPI backend. Thin HTTP layer only -- all AI logic (prompting, RAG,
guardrails, the LLM call) lives in `../ai_engine/`, imported directly.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The gateway credentials live in `../ai_engine/.env` (see
`ai_engine/.env.example`), not here -- ai_engine owns its own config
since it's a standalone, independently-testable module. This backend
only needs its own `.env` for `FRONTEND_ORIGIN` (see `.env.example`
in this folder), and only once you've deployed the frontend somewhere
real -- Vite's local dev server is already allowed by default.

## Run locally

```bash
uvicorn main:app --reload --port 8000
```

## Endpoints

- `GET /health` -- basic liveness check
- `POST /analyze` -- matches the frontend's DebuggingWorkspace.jsx exactly:
  ```json
  {"language": "Python", "code": "...", "error_message": "...", "intended_behavior": "optional"}
  ```
  Returns:
  ```json
  {
    "error_type": "...", "what_happened": "...",
    "likely_causes": ["...", "..."], "debugging_steps": ["...", "..."],
    "possible_fix": "...", "fix_explanation": "...",
    "learning_topic": "...", "practice_challenge": "..."
  }
  ```
- `POST /practice-feedback` -- for practice mode, not yet wired into the
  frontend UI: `{"challenge": "...", "user_answer": "..."}` ->
  `{"correct": bool, "feedback": "..."}`

## Error shape

Errors return `{"detail": {"message": "..."}}` (not FastAPI's default
array shape) to match what the frontend's `debugService.js` reads via
`body?.detail?.message`. 400 = bad input (empty code/error, rejected by
ai_engine's own guardrails before any LLM call). 502 = the LLM/gateway
call itself failed.

## Tested

- Full `/analyze` request cycle verified with a mocked LLM response --
  correct 200 response shape, correct field types (arrays stay arrays).
- Guardrail rejection verified -- empty code returns 400 with the
  correct `detail.message` shape the frontend expects.
- `ai_engine` import via sys.path confirmed working regardless of the
  process's working directory.
