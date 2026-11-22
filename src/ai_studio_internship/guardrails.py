"""Citation-first extractive answers and local guardrail checks."""

from __future__ import annotations

import re
from typing import Any

from ai_studio_internship.search import rank_documents, tokens

INJECTION_RE = re.compile(
    r"ignore (all )?(previous|prior|above) instructions|reveal (your )?(hidden )?(prompt|system)|"
    r"print (the )?(api key|secret)|follow my new instructions",
    re.IGNORECASE,
)
UNSAFE_RE = re.compile(r"\b(bypass|disable|override)\b.{0,45}\b(safety|interlock|alarm|guard)\b", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)\+?\d[\d .()/-]{7,}\d(?!\w)")


def detect_injection(text: str) -> bool:
    return bool(INJECTION_RE.search(text))


def mask_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    return PHONE_RE.sub("[REDACTED_PHONE]", text)


def grounded_answer(query: str, docs: list[dict[str, Any]], *, min_score: float = 0.18) -> dict[str, Any]:
    """Return a sentence copied from retrieved evidence, or a safe refusal."""

    masked_query = mask_pii(query)
    injection_detected = detect_injection(query)
    if UNSAFE_RE.search(masked_query):
        return {
            "answer": "I can't provide instructions for bypassing or disabling safety controls. Follow the authorized site's procedures.",
            "source": None,
            "page": None,
            "chunk_id": None,
            "score": 0.0,
            "refused": True,
            "injection_detected": injection_detected,
        }

    ranked = rank_documents(masked_query, docs, field="text", top_k=3)["hybrid"]
    if not ranked or float(ranked[0]["score"]) < min_score:
        return {
            "answer": "I don't know based on the available synthetic manuals.",
            "source": None,
            "page": None,
            "chunk_id": None,
            "score": float(ranked[0]["score"]) if ranked else 0.0,
            "refused": True,
            "injection_detected": injection_detected,
        }

    best = ranked[0]
    query_terms = set(tokens(masked_query))
    lines = [line.strip() for line in str(best.get("text", "")).splitlines() if line.strip()]
    sentence = max(lines or [str(best.get("text", ""))], key=lambda line: len(query_terms & set(tokens(line))))
    answer = mask_pii(sentence)
    return {
        "answer": answer,
        "source": best.get("manual_id"),
        "page": best.get("page"),
        "chunk_id": best.get("id"),
        "score": float(best["score"]),
        "refused": False,
        "injection_detected": injection_detected,
    }
