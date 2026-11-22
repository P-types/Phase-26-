"""Offline FAQ embeddings and simple hybrid retrieval for bootcamp exercises."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FAQ_PATH = ROOT / "data" / "day07_faqs.jsonl"
VECTOR_PATH = ROOT / "data" / "day07_faq_vectors.json"
TAMIL_ALIASES = {
    "வெண்டிலேட்டர்": "ventilator",
    "பம்ப்": "pump",
    "இன்ஃப்யூஷன்": "infusion",
    "ஆட்டோகிளேவ்": "autoclave",
    "வெப்பநிலை": "temperature",
    "அலாரம்": "alarm",
    "எச்சரிக்கை": "warning",
    "மின்சாரம்": "power",
    "மின்கலம்": "battery",
    "குறியீடு": "code",
    "பராமரிப்பு": "maintenance",
    "மருத்துவமனை": "hospital",
    "சாதனம்": "device",
    "கதவு": "door",
    "ஓட்டம்": "flow",
    "காட்சி": "display",
    "சேவை": "service",
    "பிழை": "error",
    "எப்படி": "how",
    "என்ன": "what",
}


def normalize_text(text: str) -> str:
    for tamil, english in TAMIL_ALIASES.items():
        text = text.replace(tamil, f" {english} ")
    return text.casefold()


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize_text(text))


def embed_text(text: str, dimensions: int = 96) -> list[float]:
    """Deterministic feature-hashing vector; a transparent offline baseline."""
    terms = tokens(text)
    features = terms + [f"{a}_{b}" for a, b in zip(terms, terms[1:])]
    vector = [0.0] * dimensions
    for feature in features:
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        vector[value % dimensions] += 1.0 if value & 1 else -1.0
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have equal dimensions")
    return sum(a * b for a, b in zip(left, right))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_faq_vectors() -> int:
    faqs = load_jsonl(FAQ_PATH)
    vectors = [
        {"id": item["id"], "vector": embed_text(item["question"] + " " + item["answer"])}
        for item in faqs
    ]
    VECTOR_PATH.write_text(json.dumps(vectors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(vectors)


def bm25_scores(query: str, docs: list[dict[str, Any]], field: str = "text") -> list[float]:
    query_terms = tokens(query)
    doc_terms = [tokens(str(doc.get(field, ""))) for doc in docs]
    n = len(docs)
    average = sum(map(len, doc_terms)) / max(n, 1)
    document_frequency = Counter(term for terms_ in doc_terms for term in set(terms_))
    scores = []
    for terms_ in doc_terms:
        counts = Counter(terms_)
        score = 0.0
        for term in query_terms:
            frequency = counts[term]
            if not frequency:
                continue
            idf = math.log(1 + (n - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            denominator = frequency + 1.2 * (0.25 + 0.75 * len(terms_) / max(average, 1))
            score += idf * frequency * 2.2 / denominator
        scores.append(score)
    return scores


def rank_documents(query: str, docs: list[dict[str, Any]], *, field: str = "text", top_k: int = 3) -> dict[str, list[dict[str, Any]]]:
    if not docs:
        return {"bm25": [], "hybrid": []}
    lexical = bm25_scores(query, docs, field)
    vectors = [embed_text(str(doc.get(field, ""))) for doc in docs]
    query_vector = embed_text(query)
    dense = [max(0.0, cosine(query_vector, vector)) for vector in vectors]
    max_lexical = max(lexical) or 1.0
    max_dense = max(dense) or 1.0
    q_terms = set(tokens(query))
    scored = []
    for index, doc in enumerate(docs):
        doc_terms = set(tokens(str(doc.get(field, ""))))
        exact_match = len(q_terms & doc_terms) / max(len(q_terms), 1)
        hybrid_score = 0.65 * lexical[index] / max_lexical + 0.35 * dense[index] / max_dense
        reranked_score = hybrid_score + 0.15 * exact_match
        scored.append((lexical[index], reranked_score, index, doc))
    bm25_order = sorted(scored, key=lambda item: (-item[0], item[2]))[:top_k]
    hybrid_order = sorted(scored, key=lambda item: (-item[1], item[2]))[:top_k]
    return {
        "bm25": [{**item[3], "score": item[0]} for item in bm25_order],
        "hybrid": [{**item[3], "score": item[1]} for item in hybrid_order],
    }


def faq_search(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    faqs = load_jsonl(FAQ_PATH)
    if VECTOR_PATH.exists():
        stored = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
        vector_by_id = {item["id"]: item["vector"] for item in stored}
    else:
        vector_by_id = {faq["id"]: embed_text(faq["question"] + " " + faq["answer"]) for faq in faqs}
    query_vector = embed_text(query)
    ranked = []
    for faq in faqs:
        score = cosine(query_vector, vector_by_id[faq["id"]])
        ranked.append({**faq, "score": score})
    return sorted(ranked, key=lambda item: (-item["score"], item["id"]))[:top_k]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the synthetic FAQ vector index")
    parser.add_argument("query", nargs="?", help="question in English or supported Tamil keywords")
    parser.add_argument("--build", action="store_true", help="write the 50-entry offline vector index")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args(argv)
    if args.build:
        print(f"Stored {save_faq_vectors()} offline vectors in {VECTOR_PATH.relative_to(ROOT)}")
        return 0
    if not args.query:
        parser.error("provide a query or use --build")
    for result in faq_search(args.query, args.top_k):
        print(f"{result['id']} score={result['score']:.3f}: {result['answer']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
