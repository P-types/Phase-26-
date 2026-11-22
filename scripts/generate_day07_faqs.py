"""Generate 50 fictional FAQs and ten labelled retrieval questions."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVICES = ["ventilator", "patient monitor", "defibrillator", "infusion pump", "autoclave"]
TOPICS = [
    ("power indicator", "Record whether the external demo indicator is on or off."),
    ("alarm code", "Copy the fictional alert code and timestamp into the training ticket."),
    ("battery notice", "Record the displayed notice and route it to an authorized technician."),
    ("maintenance reminder", "Add the reminder date to the synthetic service log."),
    ("service record", "Include the demo asset ID, timestamp, alert code and observed symptom."),
    ("unavailable channel", "Note which demo channel is unavailable and preserve the display text."),
    ("self-check message", "Save the fictional self-check message for training review."),
    ("display warning", "Record the exact display wording in the synthetic ticket."),
    ("safe escalation", "Route unresolved demo alerts to the training facilitator."),
    ("training boundary", "This fictional FAQ is not operational or clinical guidance."),
]


def main() -> None:
    faqs = []
    for device in DEVICES:
        for topic, answer in TOPICS:
            number = len(faqs) + 1
            faqs.append({
                "id": f"FAQ{number:03d}",
                "device": device,
                "topic": topic,
                "question": f"For the {device} demo asset, what should a trainee do about the {topic}?",
                "answer": f"For the fictional {device} training asset: {answer}",
                "source": "synthetic-training-faq-v1",
            })
    path = ROOT / "data" / "day07_faqs.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in faqs), encoding="utf-8")
    queries = [
        ("How do I record the ventilator alarm code?", "FAQ002"),
        ("What should I log for a patient monitor power indicator?", "FAQ011"),
        ("Defibrillator battery notice handling", "FAQ023"),
        ("Infusion pump maintenance reminder date", "FAQ034"),
        ("Autoclave safe escalation for an unresolved alert", "FAQ049"),
        ("வெண்டிலேட்டர் அலாரம் குறியீடு", "FAQ002"),
        ("ஆட்டோகிளேவ் வெப்பநிலை எச்சரிக்கை", "FAQ048"),
        ("How to save a self-check message for the infusion pump?", "FAQ037"),
        ("Patient monitor unavailable channel", "FAQ016"),
        ("What is the training boundary for a defibrillator?", "FAQ030"),
    ]
    query_path = ROOT / "data" / "day07_faq_queries.jsonl"
    query_path.write_text(
        "".join(json.dumps({"query": query, "expected_id": expected}, ensure_ascii=False) + "\n" for query, expected in queries),
        encoding="utf-8",
    )
    print(f"Wrote {len(faqs)} synthetic FAQs and {len(queries)} labelled queries")


if __name__ == "__main__":
    main()
