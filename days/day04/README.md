# Day 4 — LLM API streaming and token economics

Run an offline streaming demo:

```sh
uv run studio-chat "Explain a Python type hint" --mock --log-path reports/day04_mock_usage.jsonl
```

For a live request, set `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL` in your shell (or a local `.env` loader you trust), then run the same command without `--mock`. The URL should be an OpenAI-compatible API base URL ending before `/chat/completions`.

The usage log records token counts and an optional estimated cost. If the provider returns no usage in its final stream event, token counts use a rough four-characters-per-token estimate. Cost remains `null` unless you supply current input/output rates in `LLM_INPUT_USD_PER_1K` and `LLM_OUTPUT_USD_PER_1K`. Prompts and responses are never written to the log. The checked-in log is a local mock example, not provider billing data.
