"""
Curated debugging knowledge base -- Week 8 deliverable.

Content lives in rag/docs/*.md so Knowledge+QA can edit or add entries
without touching Python code. This module just loads and exposes them.
"""

from rag.loader import load_all_docs

KNOWLEDGE_BASE = load_all_docs()
