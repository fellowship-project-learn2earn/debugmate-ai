# DebugMate AI — Knowledge Base Schema (RAG)

This defines the structure every error entry in the knowledge base should follow.
Each entry becomes one or more retrievable chunks for the RAG pipeline.

## Why this structure

- **One error type per entry** keeps retrieval precise — the system pulls back exactly
  the concept relevant to the user's error, not a wall of unrelated material.
- **Consistent fields** let the backend map retrieved content directly onto DebugMate's
  structured output (What happened → Why → How to investigate → Fix → Learn → Practice).
- **Chunking note**: at embedding time, split each entry into 2–3 chunks — (1) explanation +
  causes, (2) debugging steps + fix, (3) learning concept + practice seed. This keeps each
  chunk focused and improves retrieval accuracy versus embedding the whole entry as one block.

## Fields

| Field | Type | Purpose |
|---|---|---|
| `id` | string | Unique key, e.g. `py-nameerror-001` |
| `error_type` | string | Exact exception name, e.g. `NameError` |
| `language` | string | `python` (only value for MVP) |
| `common_triggers` | array of strings | Short phrases describing what typically causes it — used to improve retrieval matching against raw error text |
| `explanation` | string | Beginner-friendly description of what the error means |
| `likely_causes` | array of strings | 2–5 common root causes, ordered most → least common |
| `debugging_steps` | array of strings | Ordered, concrete investigation steps (not just the fix) |
| `fix_pattern` | string | General shape of a correct fix — a pattern, not a copy-paste patch for one snippet |
| `learning_concept` | string | The underlying concept the user should study |
| `practice_seed` | string | A short template the practice-challenge generator can build a question from |
| `references` | array of strings | Trusted sources (official docs preferred) used to ground the entry |
| `tags` | array of strings | For filtering/search, e.g. `["scope", "variables", "beginner"]` |

## Example entries

```json
[
  {
    "id": "py-nameerror-001",
    "error_type": "NameError",
    "language": "python",
    "common_triggers": [
      "name '<var>' is not defined",
      "used a variable before assigning it",
      "typo in variable name"
    ],
    "explanation": "Python raised this because it tried to look up a variable name that doesn't exist yet in any accessible scope.",
    "likely_causes": [
      "The variable was never defined before this line ran",
      "The variable name is misspelled somewhere",
      "The variable was defined inside a function or block and isn't visible outside it",
      "The variable was defined after the line that uses it"
    ],
    "debugging_steps": [
      "Read the exact variable name in the error message",
      "Search the file for where that name is first assigned",
      "Check for spelling or case differences (Python is case-sensitive)",
      "Check whether the assignment happens inside a function, loop, or conditional that may not have run",
      "Confirm the assignment happens before the line that uses the variable"
    ],
    "fix_pattern": "Define the variable before it is used, correct the spelling, or move the assignment to a scope visible at the point of use.",
    "learning_concept": "Python variable scope and the order of execution",
    "practice_seed": "Give the user a snippet where a variable is defined inside an if-block that doesn't execute, and ask them to fix it so the variable is always defined.",
    "references": [
      "https://docs.python.org/3/tutorial/errors.html"
    ],
    "tags": ["scope", "variables", "beginner"]
  },
  {
    "id": "py-typeerror-001",
    "error_type": "TypeError",
    "language": "python",
    "common_triggers": [
      "unsupported operand type(s)",
      "object is not callable",
      "argument must be str, not int"
    ],
    "explanation": "Python raised this because an operation or function was used with a value of a type it doesn't support.",
    "likely_causes": [
      "Mixing incompatible types in an operation, e.g. string + integer",
      "Calling a variable that isn't actually a function",
      "Passing the wrong type of argument to a built-in or library function",
      "Forgetting to convert user input (which is always a string) before using it numerically"
    ],
    "debugging_steps": [
      "Read which operation or function call triggered the error",
      "Print or check the type() of each value involved",
      "Check whether input from a file, API, or user needs explicit conversion",
      "Check the documentation for the expected argument types"
    ],
    "fix_pattern": "Convert the value to the expected type before the operation, or adjust the function call to match expected argument types.",
    "learning_concept": "Python data types and type conversion",
    "practice_seed": "Give the user a snippet that adds a string and an integer, and ask them to fix the type mismatch.",
    "references": [
      "https://docs.python.org/3/library/exceptions.html#TypeError"
    ],
    "tags": ["types", "conversion", "beginner"]
  },
  {
    "id": "py-indexerror-001",
    "error_type": "IndexError",
    "language": "python",
    "common_triggers": [
      "list index out of range",
      "loop off-by-one",
      "accessing last element incorrectly"
    ],
    "explanation": "Python raised this because the code tried to access a position in a list (or other sequence) that doesn't exist.",
    "likely_causes": [
      "Using an index equal to or greater than the length of the list",
      "Off-by-one error in a loop range",
      "Assuming a list has more elements than it actually does",
      "Using len(list) as an index instead of len(list) - 1"
    ],
    "debugging_steps": [
      "Print len(list) right before the failing line",
      "Print the index value being used",
      "Check loop bounds — range(len(list)) is valid, range(len(list)+1) is not",
      "Confirm the list actually contains the expected number of items at this point in the program"
    ],
    "fix_pattern": "Adjust the index or loop range so it never exceeds len(list) - 1, or add a bounds check before accessing the element.",
    "learning_concept": "List indexing and zero-based indexing in Python",
    "practice_seed": "Give the user a loop that goes one index too far, and ask them to fix the off-by-one error.",
    "references": [
      "https://docs.python.org/3/tutorial/introduction.html#lists"
    ],
    "tags": ["lists", "indexing", "beginner"]
  }
]
```

## Suggested initial coverage (Week 8 target)

Aim for 10–15 entries covering the errors beginners hit most often:

`NameError`, `TypeError`, `IndexError`, `KeyError`, `AttributeError`, `ImportError` /
`ModuleNotFoundError`, `IndentationError`, `SyntaxError`, `ValueError`, `ZeroDivisionError`,
`FileNotFoundError`, `RecursionError`.

## Minimal retrieval pipeline (conceptual)

1. Embed each chunk at ingestion time → store `(chunk_id, vector, source_entry_id, chunk_text)`.
2. At query time, embed the incoming error message (+ optionally the code snippet).
3. Retrieve top-k (start with k=3) chunks by cosine similarity.
4. Pass retrieved chunk text into the LLM prompt as grounding context, tagged clearly
   (e.g. `<<KNOWLEDGE BASE CONTEXT>> ... <</KNOWLEDGE BASE CONTEXT>>`) so the model treats
   it as trusted reference material rather than user input.
5. Log which chunks were retrieved per request — needed later to evaluate whether RAG is
   actually improving answer quality (ties directly into the QA rubric).

Tools to use, all free/open-source per the cost-control strategy in the proposal:
`sentence-transformers` for embeddings, `FAISS` or `Chroma` for the vector store.
