"""Evaluate golden-case retrieval against the local chapter-aware index."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from kb_common import KB_ROOT


DEFAULT_SET = KB_ROOT / "tests" / "golden_retrieval_cases.json"
DB_PATH = KB_ROOT / "search" / "kb_search.sqlite"
DEFAULT_TOP_K = 5
DEFAULT_MIN_RATE = 0.90
DEFAULT_GROUP_BY = ("domain", "category", "tier")


def fts_expr(query: str) -> str:
    terms = [term.strip() for term in query.split() if len(term.strip()) >= 2]
    return " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)


def search(conn: sqlite3.Connection, query: str, limit: int = DEFAULT_TOP_K, include_drafts: bool = True) -> list[str]:
    gate = "" if include_drafts else "AND (d.answer_ready = 1 OR d.authority = 'official')"
    rows = conn.execute(
        f"""
        SELECT d.path, bm25(chunks_fts, 5.0, 1.0) - d.rank_boost score
        FROM chunks_fts
        JOIN chunks c ON c.id = chunks_fts.rowid
        JOIN documents d ON d.id = c.document_id
        WHERE chunks_fts MATCH ? {gate}
        ORDER BY score LIMIT ?
        """,
        (fts_expr(query), limit * 12),
    ).fetchall()
    terms = [term.strip() for term in query.split() if term.strip()]
    if len(terms) > 1:
        like_where = " AND ".join("(c.heading LIKE ? OR c.body LIKE ?)" for _ in terms)
        like_params = [value for term in terms for value in (f"%{term}%", f"%{term}%")]
        like_rows = conn.execute(
            f"""
            SELECT d.path, -d.rank_boost AS score
            FROM chunks c
            JOIN documents d ON d.id = c.document_id
            WHERE {like_where} {gate}
            ORDER BY score, d.path, c.id
            LIMIT ?
            """,
            [*like_params, limit * 12],
        ).fetchall()
        rows = [*like_rows, *rows]
    paths = []
    for row in rows:
        if row[0] not in paths:
            paths.append(row[0])
        if len(paths) >= limit:
            break
    return paths


def summarize_results(
    results: list[dict],
    *,
    top_k: int = DEFAULT_TOP_K,
    min_rate: float = DEFAULT_MIN_RATE,
    group_by: tuple[str, ...] = DEFAULT_GROUP_BY,
) -> dict:
    passed = sum(bool(item["passed"]) for item in results)
    total = len(results)
    rate = passed / total if total else 0.0
    strata: dict[str, list[dict]] = {}
    for field in group_by:
        buckets: dict[str, list[dict]] = {}
        for item in results:
            value = str(item.get(field) or "unclassified")
            buckets.setdefault(value, []).append(item)
        strata[field] = []
        for value in sorted(buckets):
            bucket = buckets[value]
            bucket_passed = sum(bool(item["passed"]) for item in bucket)
            bucket_total = len(bucket)
            bucket_rate = bucket_passed / bucket_total if bucket_total else 0.0
            strata[field].append(
                {
                    "value": value,
                    "passed": bucket_passed,
                    "total": bucket_total,
                    "rate": bucket_rate,
                    "meets_threshold": bucket_rate >= min_rate,
                }
            )
    return {
        "metric": f"query_recall_at_{top_k}",
        "top_k": top_k,
        "threshold": min_rate,
        "passed": passed,
        "total": total,
        "rate": rate,
        "recall_at_k": rate,
        "gate_passed": total > 0 and rate >= min_rate,
        "strata": strata,
        "results": results,
    }


def evaluate(
    dataset: Path = DEFAULT_SET,
    include_drafts: bool = True,
    *,
    top_k: int = DEFAULT_TOP_K,
    min_rate: float = DEFAULT_MIN_RATE,
    group_by: tuple[str, ...] = DEFAULT_GROUP_BY,
) -> dict:
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("评测集必须是 JSON 数组")
    conn = sqlite3.connect(DB_PATH)
    results = []
    try:
        for case in cases:
            if not isinstance(case, dict) or not case.get("id") or not case.get("query"):
                raise ValueError("每个评测用例必须包含 id 和 query")
            expected_values = case.get("expected")
            if not isinstance(expected_values, list) or not expected_values:
                raise ValueError(f"{case['id']}: expected 必须是非空数组")
            hits = search(conn, case["query"], top_k, include_drafts)
            expected = {str(path) for path in expected_values}
            matched = next((path for path in hits if path in expected), "")
            rank = hits.index(matched) + 1 if matched else None
            results.append({**case, "passed": bool(matched), "matched": matched, "rank": rank, "hits": hits})
    finally:
        conn.close()
    return summarize_results(results, top_k=top_k, min_rate=min_rate, group_by=group_by)


def main() -> int:
    parser = argparse.ArgumentParser(description="CPA-ZH golden retrieval evaluation")
    parser.add_argument("--dataset", default=str(DEFAULT_SET))
    parser.add_argument("--reviewed-only", action="store_true")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--min-rate", type=float, default=DEFAULT_MIN_RATE)
    parser.add_argument("--group-by", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.top_k < 1:
        parser.error("--top-k 必须大于等于 1")
    if not 0 <= args.min_rate <= 1:
        parser.error("--min-rate 必须在 0 到 1 之间")
    group_by = tuple(args.group_by) if args.group_by else DEFAULT_GROUP_BY
    report = evaluate(
        Path(args.dataset),
        include_drafts=not args.reviewed_only,
        top_k=args.top_k,
        min_rate=args.min_rate,
        group_by=group_by,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        gate = "PASS" if report["gate_passed"] else "FAIL"
        print(
            f"Recall@{report['top_k']}={report['rate']:.2%} "
            f"passed={report['passed']}/{report['total']} "
            f"threshold={report['threshold']:.2%} gate={gate}"
        )
        for field, buckets in report["strata"].items():
            values = " ".join(
                f"{item['value']}={item['passed']}/{item['total']}({item['rate']:.2%})"
                for item in buckets
            )
            print(f"{field}: {values}")
        for item in report["results"]:
            rank = f"rank={item['rank']}" if item["rank"] else "rank=-"
            print(f"{'PASS' if item['passed'] else 'FAIL'}\t{item['id']}\t{rank}\t{item['matched'] or '-'}")
    return 0 if report["gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
