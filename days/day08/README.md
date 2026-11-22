# Day 8 — PDF ingestion and chunking

`data/day08_manuals/` contains three one-page fictional training PDFs. They are synthetic retrieval fixtures, not real service or clinical instructions. `manual-ingest` uses Poppler's `pdftotext -layout` to extract text and emits fixed-size and paragraph-aware chunks. The comparison report uses the same 10 labelled questions for both chunkers.

```sh
uv run python scripts/build_synthetic_manuals.py
uv run manual-ingest
```

The current comparison is in `reports/day08_chunking_comparison.csv`. To study the effect of chunking, change `--size` and `--overlap` on `manual-ingest`, rerun the evaluation, and compare errors as well as hit rate.
