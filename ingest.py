import sys

from rag.foundry import FoundryClient
from rag.ingest import ingest


def main() -> int:
    client = FoundryClient()
    try:
        ingest(client=client)
        print("\nIngestion tamamlandı. Artık şunu çalıştırabilirsin:  python app.py")
        return 0
    except Exception as exc:
        print(f"\nIngestion başarısız: {exc}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())