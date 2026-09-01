# DebugMate AI

An AI-powered debugging tutor for beginner Python developers. Doesn't
just fix errors -- helps learners understand, diagnose, fix, learn, and
practice. Built for the Learn2Earn AI Engineering Fellowship, 12-week
MVP.

## Project structure

```
debugmate-ai/
├── ai_engine/    AI/ML component -- prompts, RAG, guardrails, gateway
│                 client, evaluation harness. Plain Python package,
│                 no web framework. See ai_engine/README.md.
├── backend/      FastAPI backend -- HTTP routes, request validation,
│                 CORS. Imports ai_engine directly. See backend/README.md.
├── frontend/     React + Vite frontend. See frontend/README.md.
└── rag-qa/       Separate RAG/knowledge-base work from Knowledge+QA --
                  NOT YET INTEGRATED with ai_engine/rag/. Two RAG
                  approaches currently exist in this repo (ai_engine's
                  TF-IDF + markdown docs, and this one's embeddings +
                  Chroma) -- which becomes canonical, or how they
                  combine, is a team decision, not made here.
```

## Running locally

Three processes, in three terminals:

```bash
# 1. Backend (also needs ai_engine/.env set -- see ai_engine/README.md)
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. Frontend
cd frontend
npm install
cp .env.example .env   # defaults to http://127.0.0.1:8000, fine for local dev
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

## Deployment

Both frontend and backend deploy to the same VPS already running the
project's `nexus-ai-gateway` (n8n) -- no AWS, reusing the existing
Cloudflare + Caddy setup rather than standing up new infrastructure:

1. `cd frontend && npm run build` -- produces static files in `dist/`.
2. Copy `dist/` to the VPS, add a Caddy site block serving it as static
   files (same pattern as any static site behind Caddy).
3. Add the FastAPI backend as another Docker service alongside the
   existing n8n container in the same `docker-compose.yml`.
4. Add a Caddy site block reverse-proxying an `api.` subdomain to the
   backend container -- same pattern as `llm-gateway.townscribe.org`
   proxying to n8n.
5. Add Cloudflare DNS records for both subdomains, pointing at the VPS.
   Caddy auto-issues TLS for each.
6. Set `FRONTEND_ORIGIN` on the backend to the real deployed frontend
   URL (see `backend/.env.example`) -- CORS only allows the Vite dev
   server by default.

## Status

- **ai_engine**: built, tested (syntax, RAG accuracy, guardrails, full
  request cycle with mocked LLM response), and live-tested against the
  real gateway -- 8/8 evaluation cases passed, 100% error-type match,
  100% keyword coverage.
- **backend**: built and tested (mocked end-to-end request cycle,
  guardrail error path, `ai_engine` import wiring) -- not yet tested
  against a live gateway call through the actual HTTP server.
- **frontend**: pre-existing, more complete version kept (a duplicate,
  less-complete copy with a conflicting API contract was removed during
  this restructure).
- **rag-qa**: separate, unintegrated -- see note above.
