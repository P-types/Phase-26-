"""Run the offline schema smoke check and labelled 20-row triage baseline."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from ai_studio_internship.triager import offline_triage

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    samples = [json.loads(line) for line in (ROOT / "data/day05_triage_samples.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = []
    valid_count = 0
    for sample in samples:
        output = offline_triage(sample["complaint"])
        valid_count += 1
        equipment_ok = output.equipment == sample["expected_equipment"]
        urgency_ok = output.urgency == sample["expected_urgency"]
        rows.append({
            "id": sample["id"],
            "complaint": sample["complaint"],
            "expected_equipment": sample["expected_equipment"],
            "actual_equipment": output.equipment,
            "equipment_match": equipment_ok,
            "expected_urgency": sample["expected_urgency"],
            "actual_urgency": output.urgency,
            "urgency_match": urgency_ok,
            "schema_valid": True,
        })
    out_csv = ROOT / "reports/day05_triage_accuracy.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    equipment_matches = sum(row["equipment_match"] for row in rows)
    urgency_matches = sum(row["urgency_match"] for row in rows)
    (ROOT / "reports/day05_triage_accuracy.md").write_text(
        "# Day 5 triage sample run\n\n"
        f"- Synthetic complaints: {len(rows)}\n"
        f"- Outputs parsed and Pydantic-validated in offline mock mode: {valid_count}/{len(rows)}\n"
        f"- Equipment labels matching the hand-written expected labels: {equipment_matches}/{len(rows)}\n"
        f"- Urgency labels matching the hand-written expected labels: {urgency_matches}/{len(rows)}\n\n"
        "This measures only the deterministic offline rule baseline against its synthetic labels. It is not an LLM accuracy score. "
        "The CSV is the accuracy sheet template to complete again with a live model after an approved API key is configured. "
        "No real device or clinical data was used.\n",
        encoding="utf-8",
    )
    print(f"Validated {valid_count}/{len(rows)} synthetic triage outputs; wrote {out_csv.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
