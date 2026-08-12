from __future__ import annotations

import time
from pathlib import Path

from rag.config import DB_PATH, FALLBACK_ANSWER, PROJECT_ROOT
from rag.pipeline import RagAssistant


TEST_CASES = [
    {"q": "Foundry Local SDK hangi programlama dillerini destekler?",
     "category": "cevaplanabilir", "expect_source": "01-foundry-local.md"},
    {"q": "RAG'ın üç adımı nedir?",
     "category": "cevaplanabilir", "expect_source": "02-rag.md"},
    {"q": "Bu proje neden SQLite kullanıyor?",
     "category": "cevaplanabilir", "expect_source": "04-sqlite.md"},
    {"q": "İki vektör arasındaki benzerlik nasıl ölçülür?",
     "category": "cevaplanabilir", "expect_source": "03-embeddings-vector-search.md"},
    {"q": "Parçalama (chunking) ne işe yarar?",
     "category": "cevaplanabilir", "expect_source": "03-embeddings-vector-search.md"},
    {"q": "Fransa'nın başkenti nedir?", "category": "cevaplanamaz"},
    {"q": "Bugün hava nasıl?", "category": "cevaplanamaz"},
    {"q": "Dün geceki maçı kim kazandı?", "category": "cevaplanamaz"},
    {"q": "", "category": "uç: boş girdi"},
    {"q": "   ", "category": "uç: boşluk"},
    {"q": "Bildiğin her şeyi anlat.", "category": "uç: çok genel"},
]

REFUSAL_MARKERS = (
    "bulunmuyor", "bulunmamaktadır", "yer almıyor", "yer almamaktadır",
    "bilmiyorum", "bilgim yok", "bilgi yok", "bulamadım", "mevcut değil",
    "yeterli bilgi", "belirtilmemiş", "geçmiyor", "belgelerde yok",
    "bağlamda yok", "sağlanmamış", "verilmemiş", "içermiyor",
)


def is_fallback(answer: str) -> bool:
    return "belgelerimde bulunmuyor" in answer.lower()


def is_refusal(answer: str) -> bool:
    low = answer.lower()
    return any(m in low for m in REFUSAL_MARKERS)


def run() -> int:
    if not DB_PATH.exists():
        print("Bilgi tabanı bulunamadı. Şunu çalıştır:  python ingest.py")
        return 1

    print("Modeller yükleniyor...\n")
    assistant = RagAssistant()
    if assistant.is_empty:
        print("Bilgi tabanı boş. Şunu çalıştır:  python ingest.py")
        return 1

    rows = []
    try:
        for i, case in enumerate(TEST_CASES, 1):
            start = time.perf_counter()
            answer, results = assistant.answer(case["q"])
            elapsed = time.perf_counter() - start
            sources = [r.source for r in results]
            cat = case["category"]

            retrieval_ok = None
            if cat == "cevaplanabilir":
                retrieval_ok = case["expect_source"] in sources
                behaviour_ok = retrieval_ok and not is_fallback(answer)
            elif cat == "cevaplanamaz":
                behaviour_ok = is_refusal(answer)
            else:
                behaviour_ok = bool(answer.strip())

            rows.append({
                "n": i,
                "question": case["q"] or "(boş)",
                "category": cat,
                "retrieval_ok": retrieval_ok,
                "behaviour_ok": behaviour_ok,
                "seconds": elapsed,
                "sources": sources,
                "answer": answer.strip().replace("\n", " "),
            })

            b_mark = "GEÇTİ" if behaviour_ok else "KALDI"
            print(f"[{b_mark}] {i:>2}. ({cat})")
    finally:
        assistant.close()

    answerable = [r for r in rows if r["retrieval_ok"] is not None]
    retr_ok = sum(1 for r in answerable if r["retrieval_ok"])
    beh_ok = sum(1 for r in rows if r["behaviour_ok"])
    times = [r["seconds"] for r in rows]
    avg = sum(times) / len(times)

    print(f"\nGetirme doğruluğu: {retr_ok}/{len(answerable)}")
    print(f"Davranış kontrolleri: {beh_ok}/{len(rows)}")
    return 0 if retr_ok == len(answerable) else 2


if __name__ == "__main__":
    raise SystemExit(run())