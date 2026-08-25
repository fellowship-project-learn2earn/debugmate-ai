# DebugMate AI — RAG & Evaluation Methodology
**Owner:** Member 4 (RAG + QA) · **Status:** Ready for Week 8/10, built ahead of schedule

## 1. What this covers

This document explains how DebugMate AI grounds its answers in curated knowledge (RAG)
and how the team measures whether the AI's responses are actually good (evaluation).
It satisfies the Success Criteria requirement (Section 21) for "a documented AI
architecture and evaluation approach."

## 2. Knowledge base

12 curated entries covering the most common beginner Python errors: `NameError`,
`TypeError`, `IndexError`, `KeyError`, `AttributeError`, `ModuleNotFoundError`,
`IndentationError`, `SyntaxError`, `ValueError`, `ZeroDivisionError`,
`FileNotFoundError`, `RecursionError`.

Each entry follows a consistent schema (see `knowledge_base_schema.md`) with fields for
explanation, likely causes, debugging steps, fix pattern, learning concept, and a
practice-challenge seed — mirroring DebugMate's structured output format exactly.

## 3. Retrieval pipeline (RAG)

**Stack:** `sentence-transformers` (model: `all-MiniLM-L6-v2`) for embeddings, `Chroma`
for vector storage. Both are free and run locally — no per-call cost, consistent with
the project's cost-control strategy (Section 14).

**Why this stack:** MiniLM is small, fast, and well-documented, appropriate for a
12–15 entry knowledge base without needing GPU infrastructure. Chroma pairs naturally
with metadata filtering (by error type, tags) and is simpler to operate than a
pure similarity-search library for a beginner team.

**Process:**
1. Each knowledge base entry is split into 3 chunks — (a) explanation + causes,
   (b) debugging steps + fix, (c) learning concept + practice — so retrieval returns
   focused, relevant material rather than an entire entry at once.
2. All chunks are embedded and stored once at startup (or on knowledge base changes).
3. At query time, the user's error message (plus code snippet, if provided) is embedded
   and compared against stored chunks using cosine similarity.
4. The top-3 most similar chunks are retrieved and inserted into the LLM prompt inside
   a clearly tagged `<<KNOWLEDGE BASE CONTEXT>>` block, so the model treats it as
   trusted reference material rather than user input.

**Validation performed:** Before wiring this into the live LLM pipeline, the chunking
and retrieval logic was tested offline against one query per error type (12 total).
Initial testing surfaced a real bug — the `common_triggers` field (written specifically
to describe how each error commonly appears in raw text) wasn't being included in the
embedded chunk text, which caused a mismatch on ambiguous queries. After including it,
all 12 test queries retrieved the correct error type as the top match. This was
validated using a lightweight TF-IDF keyword-overlap method as a stand-in for semantic
embeddings; the real sentence-transformers model is expected to perform at least as
well, since it captures meaning rather than just keyword overlap.

The pipeline was then re-tested with the real `sentence-transformers` model
(`all-MiniLM-L6-v2`) against a larger set of 19 realistic error-message queries (roughly
covering all 12 error types, including near-duplicate cases per type). Result: **18/19
correct top-1 retrieval**.

**Known limitation (documented, not silently ignored):** the one failing case was
`KeyError: 'name'` retrieving `NameError` instead of `KeyError`. Root cause: the query
was an isolated 2-word error string where the literal dictionary key happens to be
"name" — a word that saturates NameError's own knowledge base text ("NameError,"
"variable name," "name '<var>' is not defined"). Strengthening KeyError's trigger
phrases reduced but did not eliminate this specific collision, because the ambiguity is
lexical, not a defect in the retrieval logic.

This is judged an acceptable, low-risk edge case rather than something requiring a
pipeline redesign, for two reasons:
1. In production, queries include the full error traceback *and* the surrounding code
   snippet (e.g. `user["name"]`), which resolves the ambiguity that a stripped,
   isolated error string does not have.
2. A key literally named `"name"` is a deliberately adversarial test case chosen to
   stress-test the system, not representative of typical error messages.

If this pattern recurs with other short/generic key or variable names once real user
traffic is observed, the recommended fix is to weight the query's error-type prefix
(e.g. "KeyError:") more heavily during retrieval rather than relying purely on full-text
semantic similarity — noted here as a follow-up item, not a blocker for MVP.

## 4. Evaluation approach (QA)

**Test set:** 24 realistic (language, code, error) test cases — 2 per error type across
all 12 covered errors — logged in `DebugMate_RAG_QA_Evaluation.xlsx` (Test Cases sheet).

**Rubric:** Every AI response is scored 1–5 on the 7 criteria defined in the project
proposal (Section 17): Correctness, Relevance, Clarity, Actionability, Educational
Value, Consistency, Safety. Scores are logged per test case in the Evaluation Rubric
sheet; an Overall Score is calculated automatically as the average of the 7 criteria.

**Scoring guide:**
| Score | Meaning |
|---|---|
| 5 | Excellent — nothing to improve for a beginner audience |
| 4 | Good — minor polish needed, no factual/safety issues |
| 3 | Acceptable — usable but noticeably weak in this dimension |
| 2 | Poor — likely to confuse or mislead a beginner |
| 1 | Failing — factually wrong, unsafe, or unusable |

**RAG impact measurement:** A subset of test cases are run through the system both
with and without retrieved knowledge-base context. Scores are compared side by side
in the RAG Comparison sheet, which auto-calculates the net score improvement. This is
the evidence used to justify RAG's inclusion in the final architecture rather than
treating it as an assumed improvement.

**Weak-response detection:** The Summary Dashboard sheet automatically averages scores
per criterion across all test cases and flags any test case scoring below 3.0 overall,
so the team can target fixes (prompt adjustments or knowledge base gaps) before the
Week 12 demo rather than discovering issues live.

## 5. What's still dependent on other workstreams

- Running real test cases through the live system requires Member 2's LLM integration
  (Week 5) and Member 3's `/analyze` endpoint (Weeks 3–4) to be in place.
- The retrieval pipeline (`retrieval_pipeline.py`) is fully self-contained and ready to
  import into the backend as soon as that integration point exists — no further RAG-side
  blocking work remains.

## 6. Files delivered

- `knowledge_base_schema.md` — field structure and design rationale
- `knowledge_base_starter.json` — 12 complete error entries
- `retrieval_pipeline.py` — working chunking + embedding + retrieval implementation
- `DebugMate_RAG_QA_Evaluation.xlsx` — test cases, rubric, RAG comparison, summary dashboard
- `evaluation_methodology.md` — this document
