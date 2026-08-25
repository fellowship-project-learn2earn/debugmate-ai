"""RAG subpackage -- knowledge base loading and retrieval."""

from rag.knowledge_base import KNOWLEDGE_BASE
from rag.retrieval import format_for_prompt, retrieve

__all__ = ["KNOWLEDGE_BASE", "retrieve", "format_for_prompt"]
