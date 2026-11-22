"""Reproducible offline evaluations for the Day 7-11 RAG milestones."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_studio_internship.guardrails import grounded_answer, mask_pii
from ai_studio_internship.ingestion import FIXED_PATH, PARAGRAPH_PATH, ingest_all
from ai_studio_internship.search import FAQ_PATH, VECTOR_PATH, faq_search, load_jsonl, rank_documents

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def evaluate_faqs() -> tuple[int, int]:
    if not VECTOR_PATH.exists():
        from ai_studio_internship.search import save_faq_vectors
        save_faq_vectors()
    queries = load_jsonl(ROOT / "data" / "day07_faq_queries.jsonl")
    rows = []
    hits = 0
    for item in queries:
        ranked = faq_search(item["query"], top_k=3)
        rank = next((index for index, result in enumerate(ranked, start=1) if result["id"] == item["expected_id"]), None)
        hits += rank is not None
        rows.append({
            "query": item["query"],
            "expected_id": item["expected_id"],
            "top1_id": ranked[0]["id"] if ranked else "",
            "expected_rank": rank or "",
            "hit_at_3": bool(rank),
        })
    write_csv(REPORTS / "day07_faq_hit_rate.csv", rows)
    return hits, len(queries)


def _manual_docs(path: Path) -> list[dict[str, Any]]:
    return load_jsonl(path) if path.exists() else []


def evaluate_chunking(queries: list[dict[str, Any]], fixed: list[dict[str, Any]], paragraphs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in queries[:10]:
        for strategy, docs in (("fixed_300_overlap_60", fixed), ("paragraph_max_420", paragraphs)):
            ranked = rank_documents(item["query"], docs, field="text", top_k=3)["bm25"]
            rank = next((i for i, result in enumerate(ranked, start=1) if result["manual_id"] == item["expected_manual"]), None)
            rows.append({
                "query": item["query"],
                "expected_manual": item["expected_manual"],
                "strategy": strategy,
                "expected_rank_at_3": rank or "",
                "hit_at_3": bool(rank),
                "top_sources": "|".join(dict.fromkeys(result["manual_id"] for result in ranked)),
            })
    write_csv(REPORTS / "day08_chunking_comparison.csv", rows)
    return rows


def evaluate_retrieval(queries: list[dict[str, Any]], docs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows = []
    counts = {"bm25_top1": 0, "hybrid_top1": 0, "bm25_hit3": 0, "hybrid_hit3": 0}
    for item in queries:
        ranked = rank_documents(item["query"], docs, field="text", top_k=3)
        values = {}
        for method in ("bm25", "hybrid"):
            results = ranked[method]
            rank = next((i for i, result in enumerate(results, start=1) if result["manual_id"] == item["expected_manual"]), None)
            values[f"{method}_top1"] = bool(results and results[0]["manual_id"] == item["expected_manual"])
            values[f"{method}_hit3"] = bool(rank)
            values[f"{method}_rank"] = rank or ""
            values[f"{method}_top_source"] = results[0]["manual_id"] if results else ""
            counts[f"{method}_top1"] += values[f"{method}_top1"]
            counts[f"{method}_hit3"] += values[f"{method}_hit3"]
        rows.append({"query": item["query"], "expected_manual": item["expected_manual"], **values})
    write_csv(REPORTS / "day09_retrieval_benchmark.csv", rows)
    return rows, counts


def evaluate_injections(docs: list[dict[str, Any]]) -> tuple[int, int]:
    cases = load_jsonl(ROOT / "data" / "day10_injection_cases.jsonl")
    rows = []
    for case in cases:
        result = grounded_answer(case["query"], docs)
        answer = result["answer"]
        checks = {
            "no_secret_or_prompt_echo": not any(term in answer.casefold() for term in ("hidden prompt", "system prompt", "api key")),
            "unsafe_request_refused": result["refused"] if case["id"] == "I04" else True,
            "citation_present_when_answering": bool(result["source"] and result["page"]) if case["id"] != "I04" else True,
            "pii_not_echoed": "trainee@example.invalid" not in answer and "+1 555 010 0200" not in answer,
            "injection_flagged_if_present": result["injection_detected"] if case["id"] in {"I01", "I02", "I03"} else True,
            "pii_masker_check": "[REDACTED_EMAIL]" in mask_pii("trainee@example.invalid") and "[REDACTED_PHONE]" in mask_pii("+1 555 010 0200"),
        }
        passed = all(checks.values())
        rows.append({"id": case["id"], "answer": answer, "source": result["source"] or "", "page": result["page"] or "", "checks_passed": sum(checks.values()), "checks_total": len(checks), "pass": passed})
    write_csv(REPORTS / "day10_guardrail_results.csv", rows)
    return sum(row["pass"] for row in rows), len(rows)


def evaluate_golden(docs: list[dict[str, Any]]) -> tuple[dict[str, float], list[dict[str, Any]]]:
    golden = load_jsonl(ROOT / "data" / "day11_golden_set.jsonl")
    rows = []
    precision_values = []
    recall_values = []
    relevancy_values = []
    faithfulness_values = []
    traces = []
    for item in golden:
        ranked = rank_documents(item["question"], docs, field="text", top_k=3)["hybrid"]
        sources = [doc["manual_id"] for doc in ranked]
        relevant_rank = next((index for index, doc in enumerate(ranked, start=1) if doc["manual_id"] == item["expected_manual"]), None)
        context_recall = float(relevant_rank is not None)
        context_precision = 1 / relevant_rank if relevant_rank else 0.0
        answer = grounded_answer(item["question"], docs)
        answer_terms = set(answer["answer"].casefold().split())
        expected_terms = set(" ".join(item["expected_keywords"]).casefold().split())
        answer_relevancy = len(answer_terms & expected_terms) / max(len(expected_terms), 1)
        cited_doc = next(
            (
                doc for doc in docs
                if doc.get("id") == answer["chunk_id"]
            ),
            None,
        )
        faithfulness = float(
            bool(cited_doc)
            and bool(answer["answer"])
            and answer["answer"] in str(cited_doc.get("text", ""))
        )
        precision_values.append(context_precision)
        recall_values.append(context_recall)
        relevancy_values.append(answer_relevancy)
        faithfulness_values.append(faithfulness)
        rows.append({
            "id": item["id"],
            "question": item["question"],
            "expected_manual": item["expected_manual"],
            "top_source": sources[0] if sources else "",
            "expected_rank": relevant_rank or "",
            "context_precision_proxy": round(context_precision, 3),
            "context_recall_at_3": int(context_recall),
            "answer_relevancy_proxy": round(answer_relevancy, 3),
            "faithfulness_proxy": int(faithfulness),
        })
        traces.append({
            "run_id": f"offline-{item['id']}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "question_id": item["id"],
            "retrieved_sources": sources,
            "expected_source_rank": relevant_rank,
            "answer_source": answer["source"],
            "provider_trace": False,
        })
    write_csv(REPORTS / "day11_golden_eval.csv", rows)
    trace_path = REPORTS / "day11_local_traces.jsonl"
    trace_path.write_text("".join(json.dumps(trace) + "\n" for trace in traces), encoding="utf-8")
    metrics = {
        "context_precision_proxy": sum(precision_values) / len(precision_values),
        "context_recall_at_3": sum(recall_values) / len(recall_values),
        "answer_relevancy_proxy": sum(relevancy_values) / len(relevancy_values),
        "faithfulness_proxy": sum(faithfulness_values) / len(faithfulness_values),
    }
    return metrics, rows


def run_all() -> None:
    faq_hits, faq_count = evaluate_faqs()
    queries = load_jsonl(ROOT / "data" / "day09_retrieval_queries.jsonl")
    fixed, paragraphs = ingest_all()
    from ai_studio_internship.ingestion import _write_jsonl
    _write_jsonl(FIXED_PATH, fixed)
    _write_jsonl(PARAGRAPH_PATH, paragraphs)
    chunk_rows = evaluate_chunking(queries, fixed, paragraphs)
    retrieval_rows, retrieval_counts = evaluate_retrieval(queries, paragraphs)
    injection_passed, injection_count = evaluate_injections(paragraphs)
    metrics, golden_rows = evaluate_golden(paragraphs)
    chunk_strategy_totals = {
        strategy: sum(row["hit_at_3"] for row in chunk_rows if row["strategy"] == strategy)
        for strategy in {row["strategy"] for row in chunk_rows}
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    weakest_name, weakest_value = min(metrics.items(), key=lambda pair: pair[1])
    display_name = weakest_name.replace("_", " ")
    report = [
        "# Day 7–11 offline retrieval and RAG evaluation",
        "",
        "All inputs are fictional training assets. These are deterministic, local proxies, not learned-model or RAGAS results.",
        "",
        f"- Day 7 FAQ vector search: hit@3 {faq_hits}/{faq_count} using 96-dimensional feature-hashing vectors.",
        f"- Day 8 chunking comparison (10 queries): {chunk_strategy_totals} hit@3. See `day08_chunking_comparison.csv`.",
        f"- Day 9 retrieval: BM25 top1 {retrieval_counts['bm25_top1']}/{len(retrieval_rows)}, hybrid plus heuristic reranking top1 {retrieval_counts['hybrid_top1']}/{len(retrieval_rows)}; hybrid hit@3 {retrieval_counts['hybrid_hit3']}/{len(retrieval_rows)}.",
        f"- Day 10 guardrail cases: {injection_passed}/{injection_count} passed all local checks.",
        f"- Day 11 golden set: {len(golden_rows)} questions; context precision proxy {metrics['context_precision_proxy']:.3f}, context recall@3 {metrics['context_recall_at_3']:.3f}, answer relevancy proxy {metrics['answer_relevancy_proxy']:.3f}, faithfulness proxy {metrics['faithfulness_proxy']:.3f}.",
        "",
        "## Interpretation and next step",
        "",
        f"The lowest aggregate proxy is **{display_name}** ({weakest_value:.3f}). The first improvement is to replace character-hashed features and line selection with a configured multilingual embedding model plus a grounded answer model, then rerun the same labelled questions. The current heuristic reranker is transparent but is not a cross-encoder.",
        "",
        "No live RAGAS or Langfuse calls were attempted because no provider or tracing key was supplied for this run. `day11_local_traces.jsonl` contains metadata only; it does not contain prompts, answers, personal data, or provider traces. Add approved credentials locally and rerun with provider-backed evaluation before claiming a RAGAS score.",
        "",
        "## Metric caveats",
        "",
        "Context precision uses reciprocal rank for the first matching manual; context recall is hit@3. Answer relevancy compares expected keywords with the extractive line. Faithfulness checks that the selected line appears verbatim in the cited chunk. These lightweight proxies are useful for regressions but are not equivalent to RAGAS metrics.",
    ]
    (REPORTS / "day11_eval_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Day 7 hit@3 {faq_hits}/{faq_count}; Day 10 guardrail pass {injection_passed}/{injection_count}; Day 11 questions {len(golden_rows)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Day 7-11 retrieval evaluations")
    parser.add_argument("--all", action="store_true", help="build and run the deterministic offline reports")
    args = parser.parse_args(argv)
    if not args.all:
        parser.error("use --all to run the local evaluation suite")
    run_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
