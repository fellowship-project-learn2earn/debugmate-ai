# DebugMate AI Engine

The complete AI/ML component of DebugMate AI. Owns everything between
"user submits an error" and "structured, grounded, evaluated tutor
response" -- prompt construction, RAG retrieval, guardrails, the LLM
call (via [nexus-ai-gateway](https://github.com/baalebos-cloud/nexus-ai-gateway)),
practice-mode feedback, and an offline evaluation harness.

**This module has no web server, no routes, no CORS -- that's Backend's
responsibility (already built by Member 2).** This is a plain importable
Python package with two entry points Backend calls into.

## Architecture

```
error text --> guardrails --> RAG retrieval --> prompt --> gateway --> parse --> structured dict
                  |                |
              reject bad        ground answer in
              input early       curated knowledge
```

## Files

| File | Role |
|---|---|
| `analyze.py` | Main entry point: `analyze(language, code, error, intended_behavior=None)` |
| `feedback.py` | Practice-mode entry point: `evaluate_practice_answer(challenge, user_answer)` |
| `prompts.py` | System prompt (tutor behavior) + user prompt builder |
| `gateway_client.py` | Async client for nexus-ai-gateway, reads `.env` automatically |
| `guardrails.py` | Input validation, out-of-scope detection, execution-request flagging |
| `rag/loader.py` | Loads/chunks docs from `rag/docs/*.md`, plus PDF support for future additions |
| `rag/docs/*.md` | The actual curated content -- edit these directly, no Python required |
| `rag/knowledge_base.py` | Thin wrapper exposing loaded docs as `KNOWLEDGE_BASE` |
| `rag/retrieval.py` | TF-IDF retrieval (free, local, no embeddings API cost) |
| `eval_dataset.py` | 8 labeled real-world error cases |
| `evaluation.py` | Offline harness: runs the dataset through `analyze()` and scores it |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in this folder (see `.env.example`):

```
BAALEBOS_API_URL=https://olowoporoku.app.n8n.cloud/webhook/baalebos-ai
BAALEBOS_API_KEY=your_actual_key_here
```

## How Backend integrates this

```python
from ai_engine.analyze import analyze, AnalysisError
from ai_engine.feedback import evaluate_practice_answer, FeedbackError
from ai_engine.guardrails import GuardrailViolation
from ai_engine.gateway_client import GatewayError

# Initial error analysis:
try:
    result = await analyze(language=req.language, code=req.code, error=req.error)
    # -> {error_type, what_happened, why_it_happened, how_to_investigate,
    #     possible_fix, what_to_learn, practice_challenge}
except GuardrailViolation as exc:
    ...  # map to HTTP 400 -- bad input, rejected before any LLM call
except (AnalysisError, GatewayError) as exc:
    ...  # map to HTTP 502 -- LLM/gateway call failed

# Practice mode, after the user attempts the challenge:
try:
    fb = await evaluate_practice_answer(challenge, user_answer)
    # -> {"correct": bool, "feedback": str}
except (FeedbackError, GatewayError) as exc:
    ...  # map to HTTP 502
```

Backend owns HTTP status codes, request validation shape, CORS, and
routing. This module only decides what a *good analysis* looks like.

## Running the evaluation harness

```bash
python3 evaluation.py
```

Prints every case's result plus automated scoring (error-type match,
expected-keyword coverage) and a summary. Clarity, educational value,
and safety still need a human reading the printed transcripts -- the
doc is explicit that AI evaluation isn't fully automatable.

**Confirmed live result:** 8/8 cases succeeded, 100% error-type match
rate, 100% average keyword coverage against the real nexus-ai-gateway.

## Design choices worth knowing

- **RAG uses TF-IDF, not an embeddings API.** At ~10 short documents,
  TF-IDF is accurate enough and costs nothing to run -- matches the
  project's cost-control principle. This was independently validated by
  a teammate's own RAG prototype using the same approach. If the
  knowledge base grows into the hundreds of docs, revisit this.
- **Knowledge lives in markdown files, not Python.** `rag/docs/*.md`
  uses a simple `# Title` / `tags: a, b, c` / body convention -- add a
  new file to add a new topic, no code changes needed. `rag/loader.py`
  also supports PDF ingestion (chunked via `RecursiveCharacterTextSplitter`,
  same pattern as the reference document-QA app) for longer source
  material later.
- **Guardrails are rule-based, not a classifier.** The doc explicitly
  warns against over-building for a 3-month MVP; a full safety
  classifier isn't justified at this scale. The system prompt is the
  primary defense against unsafe/off-topic behavior; guardrails.py is
  a second, cheap layer.
- **No code is ever executed**, per the project's security decision --
  everything here only ever sends code as text to the LLM.

## Possible next additions (still AI/ML-scoped)

- Adversarial eval cases (no real error, mismatched error/code) to
  test the safety criterion directly -- current 8 cases are all
  "well-formed" errors.
- Simple in-memory response caching for identical (language, code,
  error) requests, supporting the cost-control principle further.
- A `confidence`/`is_uncertain` field in the output schema, making the
  system prompt's existing honesty instruction measurable.
- Logging which provider (of the gateway's 9) actually answered each
  request, to track consistency across the fallback chain.
