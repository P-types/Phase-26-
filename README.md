# AI Studio Internship

A personal Python workspace for the AI Studio internship exercises. Keep each day's work small, reproducible, and easy to review.

## Requirements

- Python 3.12 (managed by `uv` for this project)
- `uv`
- Git

## Start here

```sh
uv sync
uv run ai-studio-internship
```

`uv sync` creates an isolated `.venv` and installs the project from `uv.lock`. The starter command should print a short ready message.

## Project layout

- `src/ai_studio_internship/`: reusable Python code
- `days/dayXX/`: daily exercise notes and run instructions
- `data/`: local synthetic practice data only; do not commit restricted or client data
- `docs/`: design notes and learning notes

## Day 2: synthetic ticket validation

The package includes a Pydantic model and CSV loader for synthetic AMC tickets. Run the sample importer with:

```sh
uv run ticket-import data/day02_synthetic_service_tickets.csv
```

Run the Day 2 test suite with `uv run pytest`. The sample data is fictional; use only synthetic or anonymized records in future exercises.

## Days 3–12: foundations and RAG

The due-day index, repeatable commands, local evaluation reports, and pending personal steps are tracked in [`docs/progress-through-day12.md`](docs/progress-through-day12.md). The `days/` directory explains each artifact; [`docs/day03-12-resources.md`](docs/day03-12-resources.md) links to primary learning material.

Quick offline commands:

```sh
uv run python scripts/generate_day03_payments.py
uv run python scripts/generate_day07_faqs.py
uv run python scripts/build_synthetic_manuals.py
uv run python scripts/generate_day11_golden_set.py
uv run studio-chat "Explain a Python type hint" --mock
uv run ticket-triage "Ventilator alarm keeps repeating" --mock
uv run faq-search --build
uv run manual-ingest
uv run rag-evaluate --all
```

Provider-backed chat and triage require an approved OpenAI-compatible endpoint and locally configured environment variables. The committed fixtures and reports contain synthetic data only. Offline feature-hashing and retrieval metrics are learning baselines; they are not learned embeddings or RAGAS scores.

## Local configuration

Copy `.env.example` to `.env` and fill only the keys for the provider approved by your mentor. `.env` is ignored by Git. Never put API keys in source files, notebooks, screenshots, or commits. Do not send real hospital, payment, or client data to a model provider.

## Git workflow

1. Start from an up-to-date `main` branch.
2. Make one focused branch, such as `feat/day-02-ticket-validation`.
3. Commit a small change with a descriptive message.
4. Open a pull request and complete the checklist in `.github/pull_request_template.md`.
5. Explain the change and its failure cases during review; merge only after review.

Daily log format: `Did / Learned / Blocked`.
