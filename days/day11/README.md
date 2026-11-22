# Day 11 — Golden set and evaluation

`data/day11_golden_set.jsonl` contains 30 synthetic manual questions with expected source and keywords. `uv run rag-evaluate --all` creates `reports/day11_golden_eval.csv`, `reports/day11_eval_report.md`, and metadata-only local traces.

The report labels the measurements as local proxies. No RAGAS or Langfuse service was called because no provider or tracing key was supplied for this run. A live run should use approved keys, preserve the same golden set, and record provider/model/prompt version without logging sensitive content.
