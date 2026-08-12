from __future__ import annotations

from .config import APP_NAME, CHAT_MODEL, EMBEDDING_MODEL


def _print_progress(label: str):
    def cb(percent: float):
        print(f"\r{label}: {percent:.1f}%", end="", flush=True)
    return cb


class FoundryClient:
    def __init__(self, app_name: str = APP_NAME,
                 embedding_model: str = EMBEDDING_MODEL,
                 chat_model: str = CHAT_MODEL):
        self.app_name = app_name
        self.embedding_model_alias = embedding_model
        self.chat_model_alias = chat_model

        self._manager = None
        self._embedding_model = None
        self._embedding_client = None
        self._chat_model = None
        self._chat_client = None

    def _manager_instance(self):
        if self._manager is None:
            from foundry_local_sdk import Configuration, FoundryLocalManager

            config = Configuration(app_name=self.app_name)
            FoundryLocalManager.initialize(config)
            self._manager = FoundryLocalManager.instance
        return self._manager

    def _ensure_embedding_client(self):
        if self._embedding_client is None:
            manager = self._manager_instance()
            model = manager.catalog.get_model(self.embedding_model_alias)
            model.download(_print_progress("Embedding modeli indiriliyor"))
            print()
            model.load()
            self._embedding_model = model
            self._embedding_client = model.get_embedding_client()
        return self._embedding_client

    def embed_texts(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        client = self._ensure_embedding_client()
        vectors: list[list[float]] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            response = client.generate_embeddings(batch)
            vectors.extend(item.embedding for item in response.data)
        return vectors

    def embed_query(self, text: str) -> list[float]:
        client = self._ensure_embedding_client()
        response = client.generate_embedding(text)
        return response.data[0].embedding

    def _ensure_chat_client(self):
        if self._chat_client is None:
            manager = self._manager_instance()
            model = manager.catalog.get_model(self.chat_model_alias)
            model.download(_print_progress("Sohbet modeli indiriliyor"))
            print()
            model.load()
            self._chat_model = model
            self._chat_client = model.get_chat_client()
        return self._chat_client

    def chat(self, messages: list[dict]) -> str:
        client = self._ensure_chat_client()
        response = client.complete_chat(messages)
        return response.choices[0].message.content

    def chat_stream(self, messages: list[dict]):
        client = self._ensure_chat_client()
        for chunk in client.complete_streaming_chat(messages):
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def close(self) -> None:
        if self._embedding_model is not None:
            self._embedding_model.unload()
        if self._chat_model is not None:
            self._chat_model.unload()