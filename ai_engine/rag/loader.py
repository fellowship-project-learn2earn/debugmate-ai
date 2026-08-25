"""
Knowledge base loader -- Week 8 deliverable.

Loads and chunks curated debugging material from rag/docs/. Supports
both .md (the current curated content) and .pdf (for future additions --
e.g. a team member drops in a PDF style guide or reference doc and it
gets ingested the same way).

Chunking uses langchain's RecursiveCharacterTextSplitter, matching the
pattern already validated in the team's "Talk to my documents" RAG app --
same chunk_size/overlap approach, same TF-IDF retrieval philosophy
downstream (see retrieval.py).
"""

import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path(__file__).parent / "docs"

_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def _parse_markdown(path: Path) -> dict:
    """
    Our .md files have a simple convention:
        # Title
        tags: tag1, tag2, tag3

        content...
    """
    text = path.read_text(encoding="utf-8")

    title_match = re.match(r"#\s*(.+)", text)
    title = title_match.group(1).strip() if title_match else path.stem

    tags_match = re.search(r"tags:\s*(.+)", text)
    tags = [t.strip() for t in tags_match.group(1).split(",")] if tags_match else []

    # content is everything after the tags line
    content = re.sub(r"^#.*\n.*tags:.*\n+", "", text, flags=re.MULTILINE).strip()

    return {"id": path.stem, "title": title, "tags": tags, "content": content}


def load_markdown_docs() -> list[dict]:
    """
    Load each .md file as a single chunk (they're short enough that
    splitting would only hurt retrieval precision, per the pattern of
    keeping one coherent explanation together).
    """
    docs = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        docs.append(_parse_markdown(path))
    return docs


def load_pdf_doc(path: Path, title: str | None = None, tags: list[str] | None = None) -> list[dict]:
    """
    Load and chunk a PDF the same way the reference app does. Longer
    source material genuinely needs chunking (unlike our short curated
    .md files), so this returns MULTIPLE chunks per PDF, each usable as
    its own retrievable knowledge base entry.
    """
    loader = PyPDFLoader(str(path))
    pages = loader.load()
    chunks = _splitter.split_documents(pages)

    return [
        {
            "id": f"{path.stem}-chunk-{i}",
            "title": title or path.stem,
            "tags": tags or [],
            "content": chunk.page_content,
        }
        for i, chunk in enumerate(chunks)
    ]


def load_all_docs() -> list[dict]:
    """Everything the knowledge base currently has: all markdown docs.
    Add load_pdf_doc(...) calls here as PDF sources are added later."""
    return load_markdown_docs()
