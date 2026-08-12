import json
import sqlite3
from pathlib import Path
from typing import Iterable, NamedTuple


class Chunk(NamedTuple):
    id: int
    source: str
    chunk_index: int
    content: str
    embedding: list


def connect(db_path: Path) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT    NOT NULL,
            chunk_index INTEGER NOT NULL,
            content     TEXT    NOT NULL,
            embedding   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )
    conn.commit()


def clear(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM chunks")
    conn.commit()


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )
    conn.commit()


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def insert_chunks(conn: sqlite3.Connection, rows: Iterable[tuple]) -> None:
    conn.executemany(
        "INSERT INTO chunks(source, chunk_index, content, embedding) "
        "VALUES (?, ?, ?, ?)",
        [
            (source, idx, content, json.dumps(embedding))
            for (source, idx, content, embedding) in rows
        ],
    )
    conn.commit()


def count_chunks(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM chunks").fetchone()["n"]


def fetch_all_chunks(conn: sqlite3.Connection, with_embeddings: bool = True) -> list[Chunk]:
    rows = conn.execute(
        "SELECT id, source, chunk_index, content, embedding FROM chunks "
        "ORDER BY source, chunk_index"
    ).fetchall()
    chunks = []
    for r in rows:
        embedding = json.loads(r["embedding"]) if with_embeddings else []
        chunks.append(
            Chunk(
                id=r["id"],
                source=r["source"],
                chunk_index=r["chunk_index"],
                content=r["content"],
                embedding=embedding,
            )
        )
    return chunks