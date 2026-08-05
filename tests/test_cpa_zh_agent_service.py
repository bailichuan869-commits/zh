from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from tools.cpa_zh_agent_service import AgentServiceError, CommandResult, CpaZhAgentService


class AgentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "CPA-ZH"
        self.preview_root = Path(self.temp.name) / "previews"
        (self.root / "wiki" / "cases").mkdir(parents=True)
        (self.root / "wiki" / "questions").mkdir(parents=True)
        (self.root / "raw" / "cases").mkdir(parents=True)
        (self.root / "search").mkdir()
        self.review_page = self.root / "wiki" / "cases" / "pending.md"
        self.review_page.write_text(
            """---
title: 待复核案例
page_role: case
maturity: draft
answer_ready: false
review_status: pending-human-review
source_verified: true
raw_path: raw/cases/source.md
---
# 正文

需要人工复核。
""",
            encoding="utf-8",
        )
        (self.root / "raw" / "cases" / "source.md").write_text("---\ntitle: 来源\n---\n原始资料", encoding="utf-8")
        self._create_index()
        self.commands: list[list[str]] = []

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _create_index(self) -> None:
        connection = sqlite3.connect(self.root / "search" / "kb_search.sqlite")
        connection.execute(
            """CREATE TABLE documents (
                kind TEXT, title TEXT, path TEXT, source_url TEXT, domain TEXT, topic TEXT,
                body TEXT, page_role TEXT, maturity TEXT, answer_ready INTEGER, rank_boost REAL
            )"""
        )
        connection.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("wiki", "收入确认", "wiki/cases/pending.md", "", "accounting", "revenue", "控制权转移后确认收入", "case", "draft", 0, 10.0),
        )
        connection.commit()
        connection.close()

    def _runner(self, args: list[str]) -> CommandResult:
        self.commands.append(args)
        return CommandResult(args, "ok", "", 0)

    def service(self, *, demo: bool = False) -> CpaZhAgentService:
        return CpaZhAgentService(self.root, preview_root=self.preview_root, demo_mode=demo, runner=self._runner)

    def test_search_and_read_contracts(self) -> None:
        service = self.service()
        results = service.search("收入", domain="accounting")
        self.assertEqual(1, results["count"])
        page = service.read_page("wiki/cases/pending.md")
        self.assertEqual("待复核案例", page["title"])
        raw = service.read_raw("raw/cases/source.md")
        self.assertIn("原始资料", raw["text"])

    def test_health_count_matches_all_wiki_markdown(self) -> None:
        maintenance = self.root / "wiki" / "_maintenance" / "README.md"
        maintenance.parent.mkdir()
        maintenance.write_text("# 维护说明", encoding="utf-8")
        health = self.service().health()
        self.assertEqual(2, health["wiki_pages"])

    def test_paths_cannot_escape_owned_layers(self) -> None:
        with self.assertRaises(AgentServiceError) as context:
            self.service().read_page("../raw/cases/source.md")
        self.assertEqual("invalid_path", context.exception.code)

    def test_review_preview_and_real_commit_are_two_stage(self) -> None:
        service = self.service()
        preview = service.review_preview("wiki/cases/pending.md")
        with self.assertRaises(AgentServiceError) as context:
            service.commit(preview["preview_token"], confirmed=False)
        self.assertEqual("confirmation_required", context.exception.code)

        result = service.commit(preview["preview_token"], confirmed=True)
        self.assertTrue(result["written"])
        content = self.review_page.read_text(encoding="utf-8")
        self.assertIn("review_status: user-approved", content)
        self.assertIn("answer_ready: true", content)
        self.assertEqual([["index"], ["health"]], self.commands)

        with self.assertRaises(AgentServiceError) as duplicate:
            service.commit(preview["preview_token"], confirmed=True)
        self.assertEqual("preview_not_found", duplicate.exception.code)

    def test_review_commit_rejects_changed_content(self) -> None:
        service = self.service()
        preview = service.review_preview("wiki/cases/pending.md")
        self.review_page.write_text(self.review_page.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        with self.assertRaises(AgentServiceError) as context:
            service.commit(preview["preview_token"], confirmed=True)
        self.assertEqual("content_changed", context.exception.code)

    def test_expired_preview_is_rejected(self) -> None:
        service = self.service()
        preview = service.review_preview("wiki/cases/pending.md")
        record_path = self.preview_root / f"{preview['preview_token']}.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["expires_at"] = int(time.time()) - 1
        record_path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaises(AgentServiceError) as context:
            service.commit(preview["preview_token"], confirmed=True)
        self.assertEqual("preview_expired", context.exception.code)

    def test_demo_commit_never_writes(self) -> None:
        service = self.service(demo=True)
        before = self.review_page.read_bytes()
        preview = service.review_preview("wiki/cases/pending.md")
        result = service.commit(preview["preview_token"], confirmed=True)
        self.assertTrue(result["simulated"])
        self.assertFalse(result["written"])
        self.assertEqual(before, self.review_page.read_bytes())
        self.assertEqual([], self.commands)

    def test_qa_preview_contains_complete_rendered_page(self) -> None:
        long_answer = "完整回答。" * 700
        preview = self.service().qa_preview("如何确认收入？", long_answer, slug="full-preview")
        markdown = preview["data"]["preview_markdown"]
        self.assertGreater(len(markdown), 2400)
        self.assertIn(long_answer, markdown)
        self.assertEqual(["create_wiki_question_draft"], preview["data"]["changes"])
        self.assertTrue(preview["warnings"])

    def test_default_qa_slug_is_bound_to_question(self) -> None:
        first = self.service().qa_preview("第一个问题是什么？", "第一个完整回答。")
        second = self.service().qa_preview("第二个问题是什么？", "第二个完整回答。")
        self.assertNotEqual(first["data"]["target"], second["data"]["target"])

    def test_cli_returns_stable_json_envelope(self) -> None:
        command = [
            str(Path(__file__).resolve().parents[1] / ".venv" / "Scripts" / "python.exe"),
            str(Path(__file__).resolve().parents[1] / "tools" / "cpa_zh_agent.py"),
            "--root", str(self.root), "--preview-root", str(self.preview_root),
            "search", "收入", "--limit", "1",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
        payload = json.loads(completed.stdout)
        self.assertEqual(0, completed.returncode)
        self.assertTrue(payload["ok"])
        self.assertEqual("search", payload["operation"])
        self.assertIn("error_code", payload)
        self.assertIn("warnings", payload)

        preview_command = [
            str(Path(__file__).resolve().parents[1] / ".venv" / "Scripts" / "python.exe"),
            str(Path(__file__).resolve().parents[1] / "tools" / "cpa_zh_agent.py"),
            "--root", str(self.root), "--preview-root", str(self.preview_root),
            "qa-preview", "--question", "完整预览？", "--answer", "这是完整回答。", "--slug", "cli-preview",
        ]
        completed = subprocess.run(preview_command, capture_output=True, text=True, encoding="utf-8", check=False)
        payload = json.loads(completed.stdout)
        self.assertEqual(0, completed.returncode)
        self.assertIn("preview_markdown", payload["data"])
        self.assertNotIn("data", payload["data"])
        self.assertEqual("qa-preview", payload["operation"])

        command[-3:] = ["search", "--query", "收入"]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
        payload = json.loads(completed.stdout)
        self.assertEqual(0, completed.returncode)
        self.assertTrue(payload["ok"])

    def test_cli_argument_errors_are_json(self) -> None:
        command = [
            str(Path(__file__).resolve().parents[1] / ".venv" / "Scripts" / "python.exe"),
            str(Path(__file__).resolve().parents[1] / "tools" / "cpa_zh_agent.py"),
            "search", "--limit", "not-a-number",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
        payload = json.loads(completed.stdout)
        self.assertEqual(2, completed.returncode)
        self.assertFalse(payload["ok"])
        self.assertEqual("invalid_arguments", payload["error_code"])
        self.assertEqual("", completed.stderr)

    def test_commit_failure_is_structured_and_consumes_token(self) -> None:
        def failing_runner(args: list[str]) -> CommandResult:
            return CommandResult(args, "", "index failed", 1)

        service = CpaZhAgentService(
            self.root,
            preview_root=self.preview_root,
            demo_mode=False,
            runner=failing_runner,
        )
        preview = service.review_preview("wiki/cases/pending.md")
        with self.assertRaises(AgentServiceError) as context:
            service.commit(preview["preview_token"], confirmed=True)
        self.assertEqual("post_commit_failed", context.exception.code)
        self.assertTrue(context.exception.details["written"])
        self.assertTrue(context.exception.details["preview_token_consumed"])
        with self.assertRaises(AgentServiceError) as duplicate:
            service.commit(preview["preview_token"], confirmed=True)
        self.assertEqual("preview_not_found", duplicate.exception.code)

    def test_mcp_registers_expected_tools(self) -> None:
        from tools.cpa_zh_mcp import mcp

        names = {tool.name for tool in mcp._tool_manager.list_tools()}
        self.assertEqual(
            {
                "cpa_search", "cpa_read_page", "cpa_read_raw", "cpa_health",
                "cpa_pending_reviews", "cpa_review_detail", "cpa_ingest_preview",
                "cpa_qa_preview", "cpa_case_preview", "cpa_review_preview", "cpa_commit",
            },
            names,
        )

    def test_mcp_preview_envelope_is_flat(self) -> None:
        from unittest.mock import patch

        from tools import cpa_zh_mcp

        with patch.object(cpa_zh_mcp, "_service", return_value=self.service()):
            payload = cpa_zh_mcp.cpa_qa_preview(
                "MCP 完整预览？",
                "这是 MCP 完整回答。",
                slug="mcp-preview",
            )
        self.assertTrue(payload["ok"])
        self.assertIn("preview_markdown", payload["data"])
        self.assertNotIn("data", payload["data"])

    def test_mcp_stdio_starts_and_returns_structured_response(self) -> None:
        async def exercise() -> None:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            environment = os.environ.copy()
            environment["CPA_ZH_ROOT"] = str(self.root)
            environment["CPA_ZH_AGENT_PREVIEW_ROOT"] = str(self.preview_root)
            parameters = StdioServerParameters(
                command=str(Path(__file__).resolve().parents[1] / ".venv" / "Scripts" / "python.exe"),
                args=[str(Path(__file__).resolve().parents[1] / "tools" / "cpa_zh_mcp.py")],
                env=environment,
            )
            async with stdio_client(parameters) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    response = await session.call_tool("cpa_search", {"query": "收入", "limit": 1})
                    self.assertFalse(response.isError)
                    self.assertTrue(response.structuredContent["ok"])
                    self.assertEqual("search", response.structuredContent["operation"])

        import asyncio

        asyncio.run(exercise())


if __name__ == "__main__":
    unittest.main()
