# Day 3 — Data wrangling and SQL

Study `queries.sql` and `insights.md`. The fixture has 32 fictional invoices with one duplicate vendor/invoice pair, late paid rows, and unpaid rows. The SQL script loads a temporary table and demonstrates grouping, joins-by-keys, date functions, duplicate detection, and index-plan comparison.

From the repository root, provide a Postgres connection string and run:

```sh
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f days/day03/queries.sql
```

The local Postgres socket currently has no `pratham` role, so this environment could not execute the script. The Python summary in `reports/day03_insights.md` is a separate check of the CSV and must not be described as a Postgres run.
