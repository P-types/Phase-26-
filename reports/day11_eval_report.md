# Day 7–11 offline retrieval and RAG evaluation

All inputs are fictional training assets. These are deterministic, local proxies, not learned-model or RAGAS results.

- Day 7 FAQ vector search: hit@3 10/10 using 96-dimensional feature-hashing vectors.
- Day 8 chunking comparison (10 queries): {'paragraph_max_420': 10, 'fixed_300_overlap_60': 10} hit@3. See `day08_chunking_comparison.csv`.
- Day 9 retrieval: BM25 top1 10/10, hybrid plus heuristic reranking top1 10/10; hybrid hit@3 10/10.
- Day 10 guardrail cases: 5/5 passed all local checks.
- Day 11 golden set: 30 questions; context precision proxy 0.906, context recall@3 1.000, answer relevancy proxy 0.580, faithfulness proxy 1.000.

## Interpretation and next step

The lowest aggregate proxy is **answer relevancy proxy** (0.580). The first improvement is to replace character-hashed features and line selection with a configured multilingual embedding model plus a grounded answer model, then rerun the same labelled questions. The current heuristic reranker is transparent but is not a cross-encoder.

No live RAGAS or Langfuse calls were attempted because no provider or tracing key was supplied for this run. `day11_local_traces.jsonl` contains metadata only; it does not contain prompts, answers, personal data, or provider traces. Add approved credentials locally and rerun with provider-backed evaluation before claiming a RAGAS score.

## Metric caveats

Context precision uses reciprocal rank for the first matching manual; context recall is hit@3. Answer relevancy compares expected keywords with the extractive line. Faithfulness checks that the selected line appears verbatim in the cited chunk. These lightweight proxies are useful for regressions but are not equivalent to RAGAS metrics.
