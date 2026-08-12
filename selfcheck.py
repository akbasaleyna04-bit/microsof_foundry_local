import tempfile
from pathlib import Path

from rag.chunker import chunk_text
from rag import db
from rag.retrieve import cosine_similarity, search


def check_chunker() -> None:
    text = "\n\n".join(f"{i} numaralı paragraf." for i in range(20))
    chunks = chunk_text(text, max_chars=120, overlap=20)
    assert len(chunks) > 1
    print(f"[ok] parçalayıcı çalışıyor: {len(chunks)} parça")


def check_cosine() -> None:
    assert abs(cosine_similarity([1, 0], [1, 0]) - 1.0) < 1e-9
    assert abs(cosine_similarity([1, 0], [0, 1]) - 0.0) < 1e-9
    print("[ok] kosinüs benzerliği çalışıyor")


def check_db_and_search() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "test.db")
        db.init_db(conn)
        db.clear(conn)
        db.insert_chunks(conn, [
            ("a.md", 0, "kediler", [1.0, 0.0, 0.0]),
            ("b.md", 0, "köpekler", [0.0, 1.0, 0.0]),
        ])
        chunks = db.fetch_all_chunks(conn)
        results = search([0.1, 0.9, 0.0], chunks, top_k=1)
        assert results[0].source == "b.md"
        conn.close()
    print("[ok] sqlite + getirme çalışıyor")


def main() -> int:
    print("Çevrimdışı doğrulama çalışıyor...\n")
    check_chunker()
    check_cosine()
    check_db_and_search()
    print("\nTüm çevrimdışı kontroller geçti.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())