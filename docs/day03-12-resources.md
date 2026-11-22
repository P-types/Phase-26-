# Day 3–12 learning sources

Use official or primary material first. Read the matching `days/dayXX/README.md` before running an artifact.

## Day 3 — pandas and PostgreSQL

- [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) — loading, selecting, grouping and summarizing tabular data.
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) — tables, queries, joins, aggregates, indexes and `EXPLAIN`.

## Day 4–5 — APIs, structured outputs and validation

- [OpenAI Chat Completions API reference](https://platform.openai.com/docs/api-reference/chat/create) — messages, streaming and response options; follow the selected provider's own documentation when using another compatible endpoint.
- [JSON Schema getting started](https://json-schema.org/learn/getting-started-step-by-step) — schema constraints and validation.
- [Pydantic documentation](https://docs.pydantic.dev/latest/) — models, field constraints and JSON validation.
- [pytest documentation](https://docs.pytest.org/en/stable/) — fixtures, parametrization and readable test reports.

## Day 7–10 — retrieval and grounded answers

- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings) — vector representations and similarity search; use only if the provider and key are approved.
- [Qdrant search concepts](https://qdrant.tech/documentation/concepts/search/) — vector search, filtering and hybrid retrieval.
- [Elasticsearch BM25 similarity](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html) — lexical ranking background.
- [OWASP Top 10 for LLM applications](https://genai.owasp.org/llm-top-10/) — prompt injection and other application risks.

## Day 11 — evaluation and tracing

- [RAGAS documentation](https://docs.ragas.io/en/stable/) — RAG metrics and evaluation workflows.
- [Langfuse documentation](https://langfuse.com/docs) — tracing, datasets and observability.

## Use with care

Provider free tiers and pricing can change. Check the current official provider pricing and your mentor's spend cap before adding a key. Never commit a real key, real hospital/payment record, or raw prompt trace.
