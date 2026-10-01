import json
from pathlib import Path
from math import sqrt


def _load_documents() -> list[dict]:
    docs_dir = Path(__file__).parent.parent / "experiment" / "documents"
    documents = []
    for f in sorted(docs_dir.glob("*.txt")):
        documents.append({"id": f.stem, "text": f.read_text().strip()})
    return documents


def _term_frequencies(text: str) -> dict[str, float]:
    words = text.lower().split()
    counts: dict[str, int] = {}
    for w in words:
        w = w.strip(".,;:!?\"'()[]")
        if w:
            counts[w] = counts.get(w, 0) + 1
    total = sum(counts.values())
    return {w: c / total for w, c in counts.items()} if total else {}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    mag_a = sqrt(sum(v * v for v in a.values()))
    mag_b = sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def retrieve(question: str, top_k: int = 3) -> tuple[list[str], float]:
    """Retrieve relevant documents using TF cosine similarity.

    Returns (documents, best_score). The score is the highest
    similarity between the question and any retrieved document.
    """
    documents = _load_documents()
    if not documents:
        return [], 0.0

    q_tf = _term_frequencies(question)
    scored = []
    for doc in documents:
        doc_tf = _term_frequencies(doc["text"])
        score = _cosine(q_tf, doc_tf)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    docs = [item[1]["text"] for item in top]
    best_score = top[0][0] if top else 0.0

    return docs, best_score
