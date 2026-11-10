# Day 2 test report: synthetic service-ticket validation

## Result

- Command: `uv run pytest -q`
- Outcome: **6 passed**
- Runtime: 0.06 seconds

## Coverage

- Valid ticket parsing and whitespace normalization
- Rejection of an unsupported urgency and malformed timestamp
- Separation of valid and invalid CSV rows with row numbers after the header
- Duplicate ticket ID detection
- Required-column validation
- Safe warning/info logging without row contents

## Sample CSV run

Command: `uv run ticket-import data/day02_synthetic_service_tickets.csv`

- Rows read: 6
- Valid tickets: 6
- Invalid rows: 0

All sample records are fictional. Validation diagnostics include row numbers and field errors, not the input row contents.
