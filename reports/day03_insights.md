# Day 3 synthetic payments insights

- Dataset size: 32 invoices, 8 vendors.
- Late paid rows: 14; unpaid rows: 2.
- Duplicate invoice groups: V003/INV-V003-10-03 (2 rows)

## Top vendors by invoice total

- Delta Care Equipment (V003): INR 277,277.00
- Harbor Medical Parts (V007): INR 266,168.00
- Granite Health Tech (V006): INR 234,492.00
- Indigo Service Works (V008): INR 209,844.00
- Evergreen Clinical Tools (V004): INR 209,327.00

## Monthly invoice totals

- 2026-07: INR 317,732.00
- 2026-08: INR 472,548.00
- 2026-09: INR 539,364.00
- 2026-10: INR 430,180.00

## Interpretation

The synthetic fixture contains one deliberately repeated vendor/invoice pair. A duplicate check should group by both vendor and invoice number; grouping by invoice number alone can create false positives across vendors. The index comparison is intentionally tiny, so PostgreSQL may prefer a sequential scan.

These figures were computed directly from the CSV with Python because the local PostgreSQL server has no `pratham` login role. They are dataset checks, not evidence that `queries.sql` ran in PostgreSQL. Use a mentor-provided database URL to validate the SQL output.
