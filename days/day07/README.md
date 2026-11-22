# Day 7 — FAQ vector search

Run `uv run python scripts/generate_day07_faqs.py`, then `uv run faq-search --build`. This creates 50 short fictional FAQs and stores 96-dimensional deterministic feature-hashing vectors. Search in English or with the included Tamil keyword aliases:

```sh
uv run faq-search "வெண்டிலேட்டர் அலாரம் குறியீடு"
```

The 10 labelled questions and hit@3 results are in `data/day07_faq_queries.jsonl` and `reports/day07_faq_hit_rate.csv`. Feature hashing is a transparent offline baseline, not a pretrained semantic embedding model. Compare it with an approved provider embedding model as a follow-up.
