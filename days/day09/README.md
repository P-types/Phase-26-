# Day 9 — Hybrid and multilingual retrieval

The local benchmark compares BM25 with a hybrid of BM25, hashed dense vectors and a transparent overlap reranker. A small Tamil keyword map supports the specific query terms in the fixture. It is a reproducible baseline, not a multilingual language model or learned cross-encoder.

Run `uv run rag-evaluate --all`; see `data/day09_retrieval_queries.jsonl` and `reports/day09_retrieval_benchmark.csv` for 10 English/Tamil-labelled queries and the before/after ranking.
