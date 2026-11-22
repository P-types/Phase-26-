# Day 3 — synthetic payments and SQL

## Dataset

`data/day03_vendor_payments.csv` contains 32 deterministic fictional invoices across eight demo vendors. It includes two unpaid rows, late payments, and one deliberately repeated invoice for duplicate detection. Account values are fake last-four-digit labels, not bank data.

## Insights to verify in PostgreSQL

- Compare the top five vendors by total invoice amount.
- Find the repeated `V003` invoice and confirm it is not counted as a second unique invoice.
- Compare monthly totals for July through October 2026.
- Inspect the unpaid rows separately from late paid rows.
- Compare `EXPLAIN ANALYZE` before and after the composite index. At 32 rows, a sequential scan may still be cheaper; that is expected and is a useful reminder that indexes are not automatically faster on tiny tables.

## Execution status

The SQL file is ready, but this environment's PostgreSQL socket has no `pratham` role (`FATAL: role "pratham" does not exist`). No database was created or changed. After a mentor supplies a database URL, run the command at the top of `queries.sql` and paste the observed results into this note.

## Pandas warm-up

In a notebook, load the CSV with `pandas.read_csv`, convert the date columns with `pd.to_datetime`, then use `groupby("vendor_name")["amount_inr"].sum().sort_values(ascending=False)` and compare it with query 1. For duplicates, use `df.duplicated(["vendor_id", "invoice_no"], keep=False)`.
