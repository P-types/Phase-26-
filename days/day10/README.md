# Day 10 — Grounded answers and guardrails

The baseline selects a line from retrieved synthetic manuals, includes its source/page, refuses unsupported questions, masks simple email/phone patterns, and flags common injection strings. It does not execute document instructions or call a live model. Five cases are in `data/day10_injection_cases.jsonl`; results are in `reports/day10_guardrail_results.csv`.

Run `uv run rag-evaluate --all`. This is a learning fixture, not a security audit or DPDP compliance claim. Expand the attack set and add human review before connecting a real service.
