"""
Evaluation harness -- Week 10 deliverable.

Runs every case in eval_dataset.py through analyze() and scores the
result against the doc's criteria: technical correctness, relevance,
clarity, actionability, educational value, consistency, safety.

Automated checks here cover correctness (error_type match) and relevance
(expected keywords present) -- clarity/educational value/safety need a
human reviewer reading the transcript, which this script prints for you.

Run standalone:
    python3 evaluation.py
(with BAALEBOS_API_KEY set via .env or environment variable)
"""

import asyncio

from analyze import AnalysisError, analyze
from eval_dataset import EVAL_CASES
from gateway_client import GatewayError


def _score_case(case: dict, result: dict) -> dict:
    error_type_match = case["expected_error_type"].lower() in result["error_type"].lower()

    # Flatten list-valued fields (likely_causes, debugging_steps) into text
    # before searching for expected keywords.
    flattened = []
    for value in result.values():
        if isinstance(value, list):
            flattened.extend(value)
        else:
            flattened.append(value)
    full_text = " ".join(flattened).lower()

    keywords_found = [
        kw for kw in case["expected_keywords"] if kw.lower() in full_text
    ]
    keyword_coverage = len(keywords_found) / len(case["expected_keywords"])

    return {
        "case_id": case["id"],
        "error_type_match": error_type_match,
        "keyword_coverage": round(keyword_coverage, 2),
        "keywords_found": keywords_found,
        "keywords_missing": [k for k in case["expected_keywords"] if k not in keywords_found],
    }


async def run_evaluation():
    results = []
    for case in EVAL_CASES:
        print(f"\n{'=' * 60}\n{case['id']}\n{'=' * 60}")
        try:
            result = await analyze(
                language=case["language"],
                code=case["code"],
                error=case["error"],
            )
        except (AnalysisError, GatewayError) as exc:
            print(f"  FAILED: {exc}")
            results.append({"case_id": case["id"], "failed": True, "reason": str(exc)})
            continue

        score = _score_case(case, result)
        results.append(score)

        print(f"  error_type: {result['error_type']} (expected: {case['expected_error_type']})")
        print(f"  match: {'YES' if score['error_type_match'] else 'NO'}")
        print(f"  keyword coverage: {score['keyword_coverage']*100:.0f}% ({score['keywords_found']})")
        if score["keywords_missing"]:
            print(f"  missing: {score['keywords_missing']}")
        print(f"\n  what_happened: {result['what_happened']}")
        print(f"  practice_challenge: {result['practice_challenge']}")

    # summary
    completed = [r for r in results if not r.get("failed")]
    failed = [r for r in results if r.get("failed")]
    match_rate = sum(r["error_type_match"] for r in completed) / len(completed) if completed else 0
    avg_keyword_coverage = (
        sum(r["keyword_coverage"] for r in completed) / len(completed) if completed else 0
    )

    print(f"\n{'=' * 60}\nSUMMARY\n{'=' * 60}")
    print(f"Cases run: {len(EVAL_CASES)}  |  Failed calls: {len(failed)}")
    print(f"Error-type match rate: {match_rate*100:.0f}%")
    print(f"Average keyword coverage: {avg_keyword_coverage*100:.0f}%")
    print(
        "\nRemember: this only checks correctness + relevance automatically. "
        "Read the printed transcripts above for clarity, educational value, "
        "and safety -- those need a human judgment call."
    )


if __name__ == "__main__":
    asyncio.run(run_evaluation())
