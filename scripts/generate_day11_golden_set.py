"""Create a deterministic 30-question golden set over synthetic manual pages."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = [
    ("What should a trainee save for ventilator code V-01?", "ventilator", ["sensor", "warning", "code"]),
    ("What does fictional ventilator code V-02 refer to?", "ventilator", ["battery", "notice"]),
    ("How should a ventilator maintenance reminder be logged?", "ventilator", ["reminder", "date", "demo log"]),
    ("What is recorded for the ventilator power indicator?", "ventilator", ["external indicator", "on", "off"]),
    ("Which details belong in a ventilator service record?", "ventilator", ["asset id", "timestamp", "code"]),
    ("Where should an unresolved ventilator demo alert go?", "ventilator", ["training facilitator"]),
    ("Is the ventilator training PDF operating guidance?", "ventilator", ["not operating guidance"]),
    ("What does code V-03 represent?", "ventilator", ["maintenance reminder"]),
    ("Which timestamp and symptom data should be saved for a ventilator ticket?", "ventilator", ["timestamp", "observed symptom"]),
    ("What is the safe boundary for real ventilator procedures?", "ventilator", ["authorized personnel", "procedures"]),
    ("What should be recorded for infusion pump code P-11?", "infusion-pump", ["flow notice", "authorized review"]),
    ("What does infusion pump code P-12 mean in the demo?", "infusion-pump", ["door sensor", "timestamp", "asset id"]),
    ("What should a technician review for pump code P-13?", "infusion-pump", ["self-check", "message"]),
    ("How should the infusion pump status panel be copied?", "infusion-pump", ["displayed text", "demo ticket"]),
    ("What details should be in the infusion pump service record?", "infusion-pump", ["asset id", "timestamp", "observed symptom"]),
    ("Should settings be changed based on this pump sample?", "infusion-pump", ["do not change settings"]),
    ("Who reviews unresolved pump demo alerts?", "infusion-pump", ["training facilitator"]),
    ("What should be preserved for an infusion-pump self-check notice?", "infusion-pump", ["message", "technician"]),
    ("Where should the pump alert code and timestamp be copied?", "infusion-pump", ["synthetic ticket"]),
    ("Is the infusion-pump manual real clinical guidance?", "infusion-pump", ["not operating guidance"]),
    ("How should the autoclave temperature notice A-21 be handled?", "autoclave", ["temperature notice", "record the value"]),
    ("What should be saved for autoclave code A-22?", "autoclave", ["cycle notice", "displayed message"]),
    ("How is the autoclave maintenance reminder recorded?", "autoclave", ["reminder date", "demo log"]),
    ("What should be recorded from the autoclave display?", "autoclave", ["visible value", "timestamp", "asset id"]),
    ("What information belongs in an autoclave service record?", "autoclave", ["asset id", "timestamp", "code"]),
    ("Who should follow real autoclave procedures?", "autoclave", ["authorized personnel"]),
    ("Who handles an unresolved autoclave demo alert?", "autoclave", ["training facilitator"]),
    ("What does fictional autoclave code A-23 mean?", "autoclave", ["maintenance reminder"]),
    ("What should be preserved for an autoclave cycle notice?", "autoclave", ["displayed message", "technician"]),
    ("Are these autoclave instructions for real-device operation?", "autoclave", ["not operating guidance"]),
]


def main() -> None:
    path = ROOT / "data" / "day11_golden_set.jsonl"
    path.write_text(
        "".join(
            json.dumps(
                {"id": f"G{index:02d}", "question": question, "expected_manual": manual, "expected_keywords": keywords},
                ensure_ascii=False,
            ) + "\n"
            for index, (question, manual, keywords) in enumerate(QUESTIONS, start=1)
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(QUESTIONS)} golden questions to {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
