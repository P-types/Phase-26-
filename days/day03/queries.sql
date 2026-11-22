-- Day 3: PostgreSQL practice. Run from the repository root with:
--   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f days/day03/queries.sql
-- This creates a TEMP table only. The CSV contains synthetic training records.

\set ON_ERROR_STOP on

CREATE TEMP TABLE vendor_payments (
    payment_id text PRIMARY KEY,
    vendor_id text NOT NULL,
    vendor_name text NOT NULL,
    invoice_no text NOT NULL,
    invoice_date date NOT NULL,
    due_date date NOT NULL,
    paid_date date,
    amount_inr numeric(12, 2) NOT NULL CHECK (amount_inr >= 0),
    bank_account_last4 text NOT NULL
);

\copy vendor_payments FROM 'data/day03_vendor_payments.csv' WITH (FORMAT csv, HEADER true)

-- 1. Highest-spend vendors.
SELECT vendor_id, vendor_name, count(*) AS payment_count,
       sum(amount_inr) AS total_inr
FROM vendor_payments
GROUP BY vendor_id, vendor_name
ORDER BY total_inr DESC
LIMIT 5;

-- 2. Repeated invoices within a vendor.
SELECT vendor_id, invoice_no, count(*) AS copies,
       sum(amount_inr) AS recorded_inr
FROM vendor_payments
GROUP BY vendor_id, invoice_no
HAVING count(*) > 1
ORDER BY copies DESC, vendor_id;

-- 3. Monthly invoice totals, grouped by invoice date.
SELECT date_trunc('month', invoice_date)::date AS month,
       count(*) AS invoice_count, sum(amount_inr) AS total_inr
FROM vendor_payments
GROUP BY 1
ORDER BY 1;

-- 4. Paid late, by calendar day.
SELECT payment_id, vendor_name, invoice_no, due_date, paid_date,
       paid_date - due_date AS days_late, amount_inr
FROM vendor_payments
WHERE paid_date > due_date
ORDER BY days_late DESC, payment_id;

-- 5. Late-payment rate and average days late per vendor.
SELECT vendor_id, vendor_name,
       count(*) FILTER (WHERE paid_date > due_date) AS late_count,
       round(avg(paid_date - due_date) FILTER (WHERE paid_date > due_date), 1) AS avg_days_late
FROM vendor_payments
GROUP BY vendor_id, vendor_name
ORDER BY late_count DESC, vendor_id;

-- 6. Unpaid invoices already past their due date (as of a fixed training date).
SELECT payment_id, vendor_name, invoice_no, due_date, amount_inr
FROM vendor_payments
WHERE paid_date IS NULL AND due_date < DATE '2026-11-01'
ORDER BY due_date;

-- 7. Largest individual invoices.
SELECT payment_id, vendor_name, invoice_no, amount_inr
FROM vendor_payments
ORDER BY amount_inr DESC
LIMIT 10;

-- 8. Monthly totals by vendor (a simple GROUP BY with two dimensions).
SELECT date_trunc('month', invoice_date)::date AS month,
       vendor_id, sum(amount_inr) AS total_inr
FROM vendor_payments
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- 9. Invoice numbers reused across different vendors.
SELECT invoice_no, count(DISTINCT vendor_id) AS vendor_count,
       array_agg(DISTINCT vendor_id ORDER BY vendor_id) AS vendors
FROM vendor_payments
GROUP BY invoice_no
HAVING count(DISTINCT vendor_id) > 1;

-- 10. Indexing exercise: compare plans before and after this index.
EXPLAIN ANALYZE
SELECT * FROM vendor_payments
WHERE vendor_id = 'V003' AND invoice_date >= DATE '2026-09-01';

CREATE INDEX vendor_payments_vendor_date_idx
    ON vendor_payments (vendor_id, invoice_date);

EXPLAIN ANALYZE
SELECT * FROM vendor_payments
WHERE vendor_id = 'V003' AND invoice_date >= DATE '2026-09-01';
