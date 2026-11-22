# Bootcamp progress through Day 12

## Schedule assumption

The curriculum defines a 26-day Monday–Saturday schedule. Day 2 was being completed on Tuesday, Nov 10, 2026, so this tracker assumes Day 1 was Monday, Nov 9. Under that assumption, Day 12 fell on Saturday, Nov 21; Day 13 begins Monday, Nov 23. If the internship's official start date differs, adjust the due-day count before using this as an attendance record.

## Deliverables

| Day | Status in this repository | Artifact / remaining action |
| --- | --- | --- |
| 1 | Prepared and published | Starter project and pull-request checklist. |
| 2 | Prepared and published | Pydantic CSV validator, synthetic tickets, six passing tests and report. |
| 3 | Prepared; DB run pending | Synthetic vendor-payment CSV, 10 Postgres queries, computed insights. The local server has no `pratham` role; run with a mentor-provided database URL. |
| 4 | Prepared; live call pending | Streaming OpenAI-compatible CLI and mock cost log. A live request needs an approved provider key and current price rates. |
| 5 | Prepared; model evaluation pending | Pydantic triager and 20 synthetic examples. Offline mock schema check is 20/20; the simple rule baseline matches 15/20 expected urgency labels. This is not an LLM accuracy score. |
| 6 | Materials prepared; personal work pending | Quiz and answer key, blank scorecard, blog draft scaffold and retrospective prompts. Complete the quiz and personalize the draft. |
| 7 | Offline artifact complete | 50 synthetic FAQs, stored 96-dimensional feature-hashing vectors and 10 labelled queries; hit@3 is 10/10. These vectors are not learned semantic embeddings. |
| 8 | Offline artifact complete | Three fictional PDF manuals, extraction module, two chunk strategies and a 10-query comparison. Local Poppler extraction works. |
| 9 | Offline artifact complete | BM25, dense-hash hybrid and heuristic reranking benchmark over 10 English/Tamil queries; top-1 is 10/10 for both baselines. |
| 10 | Offline artifact complete | Citation-first extractive answers, weak-evidence refusal, a small PII masker and five injection/safety cases; local checks pass 5/5. This is not a compliance review. |
| 11 | Offline report complete; provider run pending | 30-question golden set, CSV evaluation, metadata-only local traces and proxy metrics. RAGAS and Langfuse were not run because no provider or tracing key was supplied for this run. |
| 12 | Materials prepared; personal work pending | Quiz and answer key, blank scorecard, blog draft scaffold and retrospective prompts. Complete the quiz and personalize the draft. |

## Daily log prompts

The deliverables above were prepared in the repository. Fill in the personal fields after completing the corresponding study session; this file does not claim that the intern attended the session, achieved quiz scores, or performed a live provider evaluation.

| Day | Did (your own activity) | Learned (your reflection) | Blocked |
| --- | --- | --- | --- |
| 3 |  |  | Local Postgres role missing; external DB URL needed. |
| 4 |  |  | Live provider key and current pricing needed. |
| 5 |  |  | Live provider key needed for model accuracy sheet. |
| 6 |  |  | Quiz score and personal blog reflection need your input. |
| 7 |  |  | Replace hashing baseline with an approved semantic embedder for a live comparison. |
| 8 |  |  | None for the synthetic PDF exercise. |
| 9 |  |  | For production-grade reranking, configure an approved multilingual model. |
| 10 |  |  | None for the offline safety fixture; broaden review before real use. |
| 11 |  |  | RAGAS model and Langfuse credentials needed for provider-backed results. |
| 12 |  |  | Quiz score and personal blog reflection need your input. |
