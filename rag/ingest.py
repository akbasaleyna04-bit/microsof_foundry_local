from __future__ import annotations

from pathlib import Path

from .config import (
    DB_PATH,
    DOC_EXTENSIONS,
    DOCS_DIR,
    EMBEDDING_MODEL,
)
from .chunker import chunk_text
from .db import connect, init_db, clear, insert_chunks, set_meta, count_chunks
from .foundry import FoundryClient


def read_documents(docs_dir: Path) -> list[tuple[str, str]]:
    docs_dir = Path(docs_dir)
    if not docs_dir.exists():
        raise FileNotFoundError(f"Belge klasörü bulunamadı: {docs_dir}")

    documents = []
    for path in sorted(docs_dir.iterdir()):
        if path.suffix.lower() in DOC_EXTENSIONS and path.is_file():
            text = path.read_text(encoding="utf-8")
            if text.strip():
                documents.append((path.name, text))
    return documents


def build_chunks(documents: list[tuple[str, str]]) -> list[tuple[str, int, str]]:
    rows = []
    for source, text in documents:
        for idx, chunk in enumerate(chunk_text(text)):
            rows.append((source, idx, chunk))
    return rows


def ingest(
    docs_dir: Path = DOCS_DIR,
    db_path: Path = DB_PATH,
    client: FoundryClient | None = None,
) -> int:
    documents = read_documents(docs_dir)
    if not documents:
        raise ValueError(f"{docs_dir} içinde belge bulunamadı")
    print(f"{len(documents)} belge okundu: "
          f"{', '.join(name for name, _ in documents)}")

    chunk_rows = build_chunks(documents)
    print(f"{len(chunk_rows)} parçaya bölündü.")

    client = client or FoundryClient()
    texts = [content for (_, _, content) in chunk_rows]
    print("Embedding'ler üretiliyor (ilk çalıştırmada model indirilir)...")
    embeddings = client.embed_texts(texts)

    conn = connect(db_path)
    init_db(conn)
    clear(conn)
    insert_chunks(
        conn,
        (
            (source, idx, content, embedding)
            for (source, idx, content), embedding in zip(chunk_rows, embeddings)
        ),
    )
    set_meta(conn, "embedding_model", EMBEDDING_MODEL)
    set_meta(conn, "embedding_dim", str(len(embeddings[0]) if embeddings else 0))
    total = count_chunks(conn)
    conn.close()

    print(f"{total} parça, embedding'leriyle {db_path} içine kaydedildi")
    return total