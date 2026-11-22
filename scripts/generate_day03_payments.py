"""Write a deterministic, fully synthetic vendor-payments CSV for Day 3."""

import csv
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "day03_vendor_payments.csv"
VENDORS = [
    ("V001", "BrightMed Supplies"),
    ("V002", "Coastal Lab Systems"),
    ("V003", "Delta Care Equipment"),
    ("V004", "Evergreen Clinical Tools"),
    ("V005", "Frontier Diagnostics"),
    ("V006", "Granite Health Tech"),
    ("V007", "Harbor Medical Parts"),
    ("V008", "Indigo Service Works"),
]


def main() -> None:
    rows = []
    for index in range(32):
        vendor_id, vendor_name = VENDORS[index % len(VENDORS)]
        month = 7 + index // len(VENDORS)
        invoice_date = date(2026, month, 3 + (index % 20))
        due_date = invoice_date + timedelta(days=30)
        delay = [-5, 0, 4, 18, -2, 42, 7, 0][index % 8]
        paid_date = "" if index in {13, 29} else (due_date + timedelta(days=delay)).isoformat()
        amount = 12000 + ((index * 7919) % 88000)
        invoice_no = f"INV-{vendor_id}-{month:02d}-{index % 4 + 1:02d}"
        if index == 27:
            invoice_no = "INV-V003-10-03"  # repeats the invoice in payment PAY-027
            vendor_id, vendor_name = VENDORS[2]
        rows.append({
            "payment_id": f"PAY-{index + 1:03d}",
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "invoice_no": invoice_no,
            "invoice_date": invoice_date.isoformat(),
            "due_date": due_date.isoformat(),
            "paid_date": paid_date,
            "amount_inr": f"{amount:.2f}",
            "bank_account_last4": f"{(4200 + (index % 8) * 317):04d}",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} fictional rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
