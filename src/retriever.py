"""Hybrid (dense + lexical) document retrieval."""
from dataclasses import dataclass


@dataclass
class Document:
    doc_id: str
    text: str
    score: float = 0.0


def hybrid_search(query: str, docs: list[Document], top_k: int = 5) -> list[Document]:
    # Replace with embeddings + BM25; keyword overlap used here as a stub.
    terms = set(query.lower().split())
    for doc in docs:
        overlap = len(terms & set(doc.text.lower().split()))
        doc.score = overlap / (len(terms) or 1)
    return sorted(docs, key=lambda d: d.score, reverse=True)[:top_k]
