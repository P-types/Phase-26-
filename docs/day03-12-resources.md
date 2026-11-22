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

## Free model/API options for practice

Checked on 2026-11-22. Quotas, model IDs, and privacy terms change, so recheck the linked provider pages before each project. The app in this repository uses an OpenAI-compatible `/chat/completions` endpoint.

| Option | Get access | `LLM_BASE_URL` | How to choose a model |
| --- | --- | --- | --- |
| Gemini API via Google AI Studio | [Create a Gemini API key](https://aistudio.google.com/apikey). The free tier has limited eligible models and quotas. | `https://generativelanguage.googleapis.com/v1beta/openai` | Pick a model currently marked free on the [Gemini pricing page](https://ai.google.dev/gemini-api/docs/pricing) and confirm the model supports the feature you need. The free-tier pricing page says submitted content may be used to improve Google products. |
| GroqCloud | [Create a Groq API key](https://console.groq.com/keys). The console shows free-plan limits for eligible models. | `https://api.groq.com/openai/v1` | Choose a current model from [Groq's model list](https://console.groq.com/docs/models), then check the [rate limits](https://console.groq.com/docs/rate-limits). |
| OpenRouter free variants | [Create an OpenRouter API key](https://openrouter.ai/settings/keys). Choose an explicitly free variant from the [free models list](https://openrouter.ai/collections/free-models), or use the `openrouter/free` router. | `https://openrouter.ai/api/v1` | Free variants are rate limited; the current page lists 20 requests/minute and 50/day for `:free` models. Confirm that the selected model ID is still free; other models can cost money. |
| Ollama on your computer | [Install Ollama](https://ollama.com/download); no API key or cloud account is needed for local inference. | `http://localhost:11434/v1` | Choose a model that fits your computer from the [Ollama library](https://ollama.com/library), install it, and set `LLM_MODEL` to its local tag. Local runs use your computer's memory and processing power. |

Hugging Face is useful for exploring model cards and demos, but its [current Inference Providers pricing page](https://huggingface.co/docs/inference-providers/en/pricing) says free accounts have no included inference credits. Treat hosted inference there as paid unless the account page shows a current grant or the selected model/provider explicitly offers free usage.

### Connect a provider to this project

1. Copy `.env.example` to `.env` and fill the key, model ID, and base URL for one provider above. Keep `.env` on your computer; it is ignored by Git. For local Ollama, use `LLM_API_KEY=ollama` (the local server ignores this placeholder).
2. This project reads environment variables; it does not automatically load `.env`. In Bash, load it in the terminal before running a live command:

   ```bash
   set -a
   source .env
   set +a
   uv run studio-chat "Explain a Python type hint"
   ```

3. Start with a short prompt and a tiny synthetic input. Check the provider dashboard and terms. Never send real internship, hospital, payment, client, or personal data to a provider without explicit mentor approval. Free plans can use prompts for service improvement and have different retention terms.
4. Never paste the key into a notebook, source file, screenshot, commit, or chat. If a key is exposed, revoke it in the provider console and create a new one.

For a provider that asks for billing details or does not show a free quota, use local Ollama or offline `--mock` mode instead of enabling paid usage unintentionally.
