"""Create a compact, reproducible insight note from the synthetic CSV."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "data/day03_vendor_payments.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    totals: dict[str, Decimal] = defaultdict(Decimal)
    names: dict[str, str] = {}
    monthly: dict[str, Decimal] = defaultdict(Decimal)
    invoices: dict[tuple[str, str], int] = defaultdict(int)
    late = 0
    unpaid = 0
    for row in rows:
        totals[row["vendor_id"]] += Decimal(row["amount_inr"])
        names[row["vendor_id"]] = row["vendor_name"]
        monthly[row["invoice_date"][:7]] += Decimal(row["amount_inr"])
        invoices[(row["vendor_id"], row["invoice_no"])] += 1
        if row["paid_date"]:
            late += date.fromisoformat(row["paid_date"]) > date.fromisoformat(row["due_date"])
        else:
            unpaid += 1
    duplicate_rows = [(vendor, invoice, count) for (vendor, invoice), count in invoices.items() if count > 1]
    lines = [
        "# Day 3 synthetic payments insights",
        "",
        f"- Dataset size: {len(rows)} invoices, {len(totals)} vendors.",
        f"- Late paid rows: {late}; unpaid rows: {unpaid}.",
        "- Duplicate invoice groups: " + (", ".join(f"{vendor}/{invoice} ({count} rows)" for vendor, invoice, count in duplicate_rows) or "none"),
        "",
        "## Top vendors by invoice total",
        "",
    ]
    for vendor, amount in sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:5]:
        lines.append(f"- {names[vendor]} ({vendor}): INR {amount:,.2f}")
    lines.extend(["", "## Monthly invoice totals", ""])
    for month, amount in sorted(monthly.items()):
        lines.append(f"- {month}: INR {amount:,.2f}")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The synthetic fixture contains one deliberately repeated vendor/invoice pair. A duplicate check should group by both vendor and invoice number; grouping by invoice number alone can create false positives across vendors. The index comparison is intentionally tiny, so PostgreSQL may prefer a sequential scan.",
        "",
        "These figures were computed directly from the CSV with Python because the local PostgreSQL server has no `pratham` login role. They are dataset checks, not evidence that `queries.sql` ran in PostgreSQL. Use a mentor-provided database URL to validate the SQL output.",
    ])
    (ROOT / "reports/day03_insights.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Summarized {len(rows)} synthetic payment rows")


if __name__ == "__main__":
    main()
