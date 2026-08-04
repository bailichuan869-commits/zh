"""Evaluate golden-case retrieval against the local chapter-aware index."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from kb_common import KB_ROOT


DEFAULT_SET = KB_ROOT / "tests" / "golden_retrieval_cases.json"
DB_PATH = KB_ROOT / "search" / "kb_search.sqlite"


def fts_expr(query: str) -> str:
    terms = [term.strip() for term in query.split() if len(term.strip()) >= 2]
    return " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)


def search(conn: sqlite3.Connection, query: str, limit: int = 8, include_drafts: bool = True) -> list[str]:
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
    paths = []
    for row in rows:
        if row[0] not in paths:
            paths.append(row[0])
        if len(paths) >= limit:
            break
    return paths


def evaluate(dataset: Path = DEFAULT_SET, include_drafts: bool = True) -> dict:
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB_PATH)
    results = []
    try:
        for case in cases:
            hits = search(conn, case["query"], 8, include_drafts)
            expected = set(case["expected"])
            matched = next((path for path in hits if path in expected), "")
            results.append({**case, "passed": bool(matched), "matched": matched, "hits": hits})
    finally:
        conn.close()
    passed = sum(item["passed"] for item in results)
    return {"passed": passed, "total": len(results), "rate": passed / len(results) if results else 0, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="CPA-ZH golden retrieval evaluation")
    parser.add_argument("--dataset", default=str(DEFAULT_SET))
    parser.add_argument("--reviewed-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = evaluate(Path(args.dataset), include_drafts=not args.reviewed_only)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"passed={report['passed']}/{report['total']}")
        for item in report["results"]:
            print(f"{'PASS' if item['passed'] else 'FAIL'}\t{item['id']}\t{item['matched'] or '-'}")
    return 0 if report["passed"] >= min(18, report["total"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
