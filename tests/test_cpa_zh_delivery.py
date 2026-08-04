from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
KB = PROJECT / "knowledge-base" / "CPA-ZH"
TOOLS = PROJECT / "tools"
BACKEND = PROJECT / "backend"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from kb_common import parse_frontmatter
from kb_health_check import case_card_paths, case_link_issues, count_wiki_links
from app.core.files import safe_resolve
from app.main import app
from app.services.library import LibraryService


class GoldenContentTests(unittest.TestCase):
    def test_twenty_topics_and_cases_exist(self):
        topics = [p for p in (KB / "wiki" / "concepts" / "accounting-judgments").glob("*.md") if p.name != "index.md"]
        golden = [p for p in (KB / "wiki" / "cases").glob("golden-*.md") if p.name != "golden-cases-index.md"]
        existing = list((KB / "wiki" / "cases").glob("2026-07-first-issue-*.md"))
        self.assertEqual(20, len(topics))
        self.assertEqual(20, len(golden) + len(existing))

    def test_topic_schema_and_citations(self):
        required = ["适用范围", "决定性事实", "准则入口", "判断路径", "分支结论", "会计处理", "列报与披露", "审计风险", "证据与底稿", "易错点", "案例链接", "时效与不确定性边界"]
        for path in (KB / "wiki" / "concepts" / "accounting-judgments").glob("*.md"):
            if path.name == "index.md":
                continue
            text = path.read_text(encoding="utf-8")
            metadata, _ = parse_frontmatter(text)
            self.assertEqual("knowledge", metadata.get("page_role"), path)
            self.assertEqual("draft", metadata.get("maturity"), path)
            self.assertFalse(metadata.get("answer_ready"), path)
            for heading in required:
                self.assertIn(f"## {heading}", text, f"{path}: {heading}")
            raw = KB / str(metadata["raw_path"])
            self.assertTrue(raw.exists(), raw)

    def test_case_citations_resolve(self):
        cases = list((KB / "wiki" / "cases").glob("golden-*.md")) + list((KB / "wiki" / "cases").glob("2026-07-first-issue-*.md"))
        cases = [p for p in cases if p.name != "golden-cases-index.md"]
        self.assertEqual(20, len(cases))
        for path in cases:
            metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            self.assertEqual("case", metadata.get("page_role"), path)
            self.assertIn("## 缺失事实", body, path)
            self.assertIn("## 结论确定性", body, path)
            self.assertTrue((KB / str(metadata["raw_path"])).exists(), metadata["raw_path"])


class RetrievalIndexTests(unittest.TestCase):
    def test_chapter_schema(self):
        conn = sqlite3.connect(KB / "search" / "kb_search.sqlite")
        try:
            columns = {row[1] for row in conn.execute("PRAGMA table_info(documents)")}
            self.assertTrue({"page_role", "maturity", "answer_ready", "authority", "rank_boost"}.issubset(columns))
            self.assertGreater(conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0], 1000)
            self.assertEqual(0, conn.execute("SELECT COUNT(*) FROM documents WHERE maturity='draft' AND answer_ready=1").fetchone()[0])
        finally:
            conn.close()

    def test_golden_eval_threshold(self):
        spec = importlib.util.spec_from_file_location("kb_eval", TOOLS / "kb_eval.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
        report = module.evaluate(include_drafts=True)
        self.assertGreaterEqual(report["passed"], 18, json.dumps(report, ensure_ascii=False))

    def test_natural_chinese_question_retrieves_official_evidence(self):
        service = LibraryService()
        hits = service.search("收入确认", "", "", 30, 0)
        self.assertTrue(hits["results"])


class BackendContractTests(unittest.TestCase):
    def test_v1_routes_are_registered(self):
        routes = {getattr(route, "path", "") for route in app.routes}
        for route in app.routes:
            nested = getattr(getattr(route, "original_router", None), "routes", ())
            prefix = getattr(getattr(route, "include_context", None), "prefix", "")
            routes.update(prefix + getattr(child, "path", "") for child in nested)
        self.assertTrue({"/api/v1/health", "/api/v1/search", "/api/v1/documents", "/api/v1/files"}.issubset(routes))

    def test_file_paths_are_restricted_to_raw_assets(self):
        self.assertTrue(safe_resolve("raw/README.md", allowed_prefix="raw/").is_relative_to(KB))
        with self.assertRaises(Exception):
            safe_resolve("wiki/index.md", allowed_prefix="raw/")


class HealthCheckTests(unittest.TestCase):
    def test_raw_links_and_nested_golden_case_index_are_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "wiki" / "cases").mkdir(parents=True)
            (root / "wiki" / "concepts").mkdir(parents=True)
            (root / "raw").mkdir()
            (root / "raw" / "source.md").write_text("source", encoding="utf-8")
            (root / "wiki" / "index.md").write_text("[[cases/golden-cases-index]]", encoding="utf-8")
            (root / "wiki" / "concepts" / "case-analysis.md").write_text("", encoding="utf-8")
            (root / "wiki" / "concepts" / "case-topic-index.md").write_text("", encoding="utf-8")
            (root / "wiki" / "cases" / "golden-cases-index.md").write_text(
                "[[cases/example|Example case]]", encoding="utf-8"
            )
            (root / "wiki" / "cases" / "example.md").write_text(
                "---\npage_role: case\n---\n\n[[raw/source.md]]", encoding="utf-8"
            )
            _count, missing = count_wiki_links(root)
            self.assertEqual([], missing)
            self.assertEqual([], case_link_issues(root))
            self.assertEqual([root / "wiki" / "cases" / "example.md"], case_card_paths(root))


if __name__ == "__main__":
    unittest.main()
