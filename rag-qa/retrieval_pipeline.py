"""
DebugMate AI — RAG Retrieval Pipeline
Member 4 (RAG + QA)

Stack: sentence-transformers (all-MiniLM-L6-v2) for embeddings, Chroma for vector storage.
Both are free/open-source, matching the project's cost-control strategy.

SETUP (run once, needs network):
    pip install sentence-transformers chromadb

USAGE:
    python retrieval_pipeline.py                # builds the DB, runs a demo query
    from retrieval_pipeline import retrieve      # import into the backend

This module is fully self-contained and does NOT depend on the FastAPI backend
or the LLM integration being built yet — it can be developed, tested, and handed
off independently, then imported once Member 2/3's side is ready.
"""

import json
import os
from typing import List, Dict

from sentence_transformers import SentenceTransformer
import chromadb

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base_starter.json")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_store")
COLLECTION_NAME = "debugmate_kb"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3


def load_knowledge_base(path: str = KB_PATH) -> List[Dict]:
    """Load the curated error knowledge base from JSON."""
    with open(path, "r") as f:
        return json.load(f)


def chunk_entry(entry: Dict) -> List[Dict]:
    """
    Split one knowledge-base entry into 3 focused chunks, per the schema doc:
      1. explanation + causes
      2. debugging steps + fix pattern
      3. learning concept + practice seed

    Each chunk keeps metadata pointing back to the source entry so retrieved
    chunks can be traced and logged for evaluation later.
    """
    base_meta = {
        "source_id": entry["id"],
        "error_type": entry["error_type"],
        "language": entry["language"],
    }

    chunk_1_text = (
        f"Error type: {entry['error_type']}. "
        f"Common ways this error appears: {'; '.join(entry['common_triggers'])}. "
        f"{entry['explanation']} "
        f"Common causes: {'; '.join(entry['likely_causes'])}."
    )

    chunk_2_text = (
        f"Debugging steps for {entry['error_type']}: "
        f"{'; '.join(entry['debugging_steps'])}. "
        f"Fix pattern: {entry['fix_pattern']}."
    )

    chunk_3_text = (
        f"Concept to learn for {entry['error_type']}: {entry['learning_concept']}. "
        f"Practice idea: {entry['practice_seed']}."
    )

    return [
        {"id": f"{entry['id']}-c1", "text": chunk_1_text, "chunk_type": "explanation_causes", **base_meta},
        {"id": f"{entry['id']}-c2", "text": chunk_2_text, "chunk_type": "debugging_fix", **base_meta},
        {"id": f"{entry['id']}-c3", "text": chunk_3_text, "chunk_type": "learning_practice", **base_meta},
    ]


def build_index(force_rebuild: bool = False) -> chromadb.Collection:
    """
    Embed every chunk and load it into a persistent Chroma collection.
    Safe to call repeatedly — skips rebuilding if the collection already has data,
    unless force_rebuild=True.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    if force_rebuild:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() > 0 and not force_rebuild:
        print(f"Collection already has {collection.count()} chunks — skipping rebuild.")
        return collection

    entries = load_knowledge_base()
    model = SentenceTransformer(EMBEDDING_MODEL)

    all_chunks = []
    for entry in entries:
        all_chunks.extend(chunk_entry(entry))

    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=[c["id"] for c in all_chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {"source_id": c["source_id"], "error_type": c["error_type"],
             "language": c["language"], "chunk_type": c["chunk_type"]}
            for c in all_chunks
        ],
    )
    print(f"Indexed {len(all_chunks)} chunks from {len(entries)} knowledge base entries.")
    return collection


def retrieve(query_error_message: str, code_snippet: str = "", top_k: int = TOP_K) -> List[Dict]:
    """
    Main entry point for the backend to call.

    Args:
        query_error_message: the raw error/traceback text the user submitted.
        code_snippet: optional code context, appended to improve match quality.
        top_k: number of chunks to retrieve.

    Returns:
        List of dicts: [{source_id, error_type, chunk_type, text, similarity}, ...]
        ordered by relevance (most relevant first).
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() == 0:
        build_index()
        collection = client.get_or_create_collection(COLLECTION_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL)
    query_text = query_error_message if not code_snippet else f"{query_error_message}\nCode: {code_snippet}"
    query_embedding = model.encode([query_text]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "source_id": results["metadatas"][0][i]["source_id"],
            "error_type": results["metadatas"][0][i]["error_type"],
            "chunk_type": results["metadatas"][0][i]["chunk_type"],
            "text": results["documents"][0][i],
            # Chroma returns distance (lower = more similar); convert to a similarity score
            "similarity": round(1 - results["distances"][0][i], 4),
        })
    return retrieved


def format_context_for_prompt(retrieved_chunks: List[Dict]) -> str:
    """
    Formats retrieved chunks into the tagged context block for the LLM prompt,
    per the schema doc's recommendation — clearly marked as trusted reference
    material so the model doesn't treat it as user input.
    """
    if not retrieved_chunks:
        return ""
    lines = ["<<KNOWLEDGE BASE CONTEXT>>"]
    for chunk in retrieved_chunks:
        lines.append(f"- ({chunk['error_type']} / {chunk['chunk_type']}): {chunk['text']}")
    lines.append("<</KNOWLEDGE BASE CONTEXT>>")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Building index (first run only)...")
    build_index()

    print("\n--- Demo query ---")
    demo_error = "NameError: name 'username' is not defined"
    demo_code = "print(username)"
    results = retrieve(demo_error, demo_code)

    for r in results:
        print(f"\n[{r['similarity']}] {r['source_id']} ({r['chunk_type']})")
        print(f"  {r['text']}")

    print("\n--- Formatted for LLM prompt ---")
    print(format_context_for_prompt(results))
