import math
from typing import NamedTuple

from .db import Chunk


class RetrievedChunk(NamedTuple):
    score: float
    source: str
    chunk_index: int
    content: str


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def search(
    query_embedding: list[float],
    chunks: list[Chunk],
    top_k: int = 3,
    threshold: float = 0.0,
) -> list[RetrievedChunk]:
    scored = [
        RetrievedChunk(
            score=cosine_similarity(query_embedding, c.embedding),
            source=c.source,
            chunk_index=c.chunk_index,
            content=c.content,
        )
        for c in chunks
        if c.embedding
    ]
    relevant = [r for r in scored if r.score >= threshold]
    relevant.sort(key=lambda r: r.score, reverse=True)
    return relevant[:top_k]