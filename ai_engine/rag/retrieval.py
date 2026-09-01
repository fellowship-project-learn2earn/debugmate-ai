"""
Retrieval over the knowledge base -- Week 8 deliverable.

Uses TF-IDF + cosine similarity instead of a paid embeddings API. This is
a deliberate cost-control choice matching the project's "start free,
avoid unnecessary paid services" principle -- at ~10 short documents,
TF-IDF is more than accurate enough, and it costs nothing to run.
"""

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rag.knowledge_base import KNOWLEDGE_BASE

_corpus = [f"{doc['title']} {' '.join(doc['tags'])} {doc['content']}" for doc in KNOWLEDGE_BASE]

# "python", "code", and "error" appear in nearly every document here, so
# they're not discriminative -- left in, they inflate similarity scores
# for any query that merely mentions Python, even off-topic ones.
_DOMAIN_STOPWORDS = {"python", "code", "error"}
_vectorizer = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS | _DOMAIN_STOPWORDS))
_doc_vectors = _vectorizer.fit_transform(_corpus)


def retrieve(query: str, top_k: int = 2, min_score: float = 0.05) -> list[dict]:
    """
    Return up to `top_k` knowledge base entries relevant to `query`,
    each with a similarity score. Entries below `min_score` are dropped --
    better to send no reference material than an irrelevant one.
    """
    query_vector = _vectorizer.transform([query])
    scores = cosine_similarity(query_vector, _doc_vectors)[0]

    ranked = sorted(
        zip(KNOWLEDGE_BASE, scores),
        key=lambda pair: pair[1],
        reverse=True,
    )

    return [
        {**doc, "score": float(score)}
        for doc, score in ranked[:top_k]
        if score >= min_score
    ]


def format_for_prompt(retrieved: list[dict]) -> str:
    """Turn retrieved docs into a short block to inject into the prompt."""
    if not retrieved:
        return ""

    sections = [
        f"- {doc['title']}: {doc['content']}"
        for doc in retrieved
    ]
    return "Reference material (use if relevant, ignore if not applicable):\n" + "\n".join(sections)
