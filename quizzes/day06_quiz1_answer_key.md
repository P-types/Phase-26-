# Day 6 — Quiz 1 answer key

Use this after attempting `day06_quiz1.md`; answers may use equivalent wording.

1. Rebase replays local commits on top of the fetched upstream tip, producing a linear history; merge-style pull creates a merge commit when histories diverge.
2. Put secrets in local `.env`; `.env` should be ignored by Git. Commit `.env.example` with names/placeholders only.
3. A type hint documents expected types and helps static tools; Python does not enforce it at runtime by itself.
4. It validates shape/types/constraints at an untrusted boundary and gives structured errors.
5. A unit test isolates a small unit; an integration test checks cooperating components or external boundaries.
6. A left join preserves every vendor row, so missing payment matches can be found with `WHERE payment_id IS NULL`.
7. `HAVING` filters aggregated groups; `WHERE` filters input rows before grouping.
8. Indexes use storage and add write/update maintenance cost; on small tables a sequential scan can be faster.
9. The system message sets task-level behavior/instructions; the user message supplies the current request or data.
10. Examples: transient network errors, 429 rate limits, 5xx service errors, timeouts. Use bounded retries with backoff and respect `Retry-After`.
