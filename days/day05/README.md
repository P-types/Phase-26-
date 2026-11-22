# Day 5 — Structured outputs and prompt engineering

Run the local schema baseline:

```sh
uv run ticket-triage "Ventilator alarm keeps repeating" --mock
uv run python scripts/evaluate_day05_triage.py
```

The live path asks an OpenAI-compatible endpoint for JSON Schema output and validates it with Pydantic. `data/day05_triage_samples.jsonl` contains 20 fictional complaints. The report separates schema validity from label agreement and identifies the rule-based mock as a baseline, not model accuracy. After a key is configured locally, rerun with the same samples and record the model and prompt version in the accuracy sheet.
