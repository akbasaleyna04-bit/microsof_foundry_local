from __future__ import annotations

from foundry_local_sdk.exception import FoundryLocalException
from .config import (
    DB_PATH,
    FALLBACK_ANSWER,
    SIMILARITY_THRESHOLD,
    SYSTEM_PROMPT,
    TOP_K,
)
from .db import connect, fetch_all_chunks
from .foundry import FoundryClient
from .retrieve import RetrievedChunk, search


def build_context(results: list[RetrievedChunk]) -> str:
    if not results:
        return "(İlgili hiçbir belge bulunamadı.)"
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(f"--- BİLGİ PARÇASI {i} (Kaynak: {r.source}) ---\n{r.content}")
    return "\n\n".join(blocks)


def build_messages(query: str, results: list[RetrievedChunk]) -> list[dict]:
    context = build_context(results)
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": query},
    ]


class RagAssistant:
    def __init__(self, db_path=DB_PATH, top_k: int = TOP_K,
                 threshold: float = SIMILARITY_THRESHOLD,
                 client: FoundryClient | None = None):
        self.db_path = db_path
        self.top_k = top_k
        self.threshold = threshold
        self.client = client or FoundryClient()
        conn = connect(db_path)
        self.chunks = fetch_all_chunks(conn)
        conn.close()

    @property
    def is_empty(self) -> bool:
        return len(self.chunks) == 0

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        query_embedding = self.client.embed_query(query)
        return search(query_embedding, self.chunks, top_k=self.top_k,
                      threshold=self.threshold)

    def answer(self, query: str) -> tuple[str, list[RetrievedChunk]]:
        if not query or not query.strip():
            return FALLBACK_ANSWER, []
        results = self.retrieve(query)
        messages = build_messages(query, results)
        try:
            answer = self.client.chat(messages)
        except (FoundryLocalException, Exception):
            answer = FALLBACK_ANSWER
        return answer, results

    def answer_stream(self, query: str):
        if not query or not query.strip():
            return [], iter([FALLBACK_ANSWER])
        results = self.retrieve(query)
        messages = build_messages(query, results)
        try:
            stream_gen = self.client.chat_stream(messages)
        except (FoundryLocalException, Exception):
            stream_gen = iter([FALLBACK_ANSWER])
        return results, stream_gen

    def close(self) -> None:
        self.client.close()