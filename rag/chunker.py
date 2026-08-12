from .config import CHUNK_MAX_CHARS, CHUNK_OVERLAP_CHARS


def _split_paragraphs(text: str) -> list[str]:
    parts = text.replace("\r\n", "\n").split("\n\n")
    return [p.strip() for p in parts if p.strip()]


def chunk_text(
    text: str,
    max_chars: int = CHUNK_MAX_CHARS,
    overlap: int = CHUNK_OVERLAP_CHARS,
) -> list[str]:
    paragraphs = _split_paragraphs(text)
    if not paragraphs:
        return []

    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if not current:
            current = para
        elif len(current) + 2 + len(para) <= max_chars:
            current = f"{current}\n\n{para}"
        else:
            chunks.append(current)
            tail = current[-overlap:] if overlap > 0 else ""
            current = f"{tail}\n\n{para}".strip() if tail else para

    if current:
        chunks.append(current)

    return chunks