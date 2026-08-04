from __future__ import annotations

import asyncio
import io
import os
import sys
import time
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException, UploadFile

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from tools import kb_maintenance_api as maintenance
from app.core import ai_config


class MaintenanceApiTests(unittest.TestCase):
    def setUp(self) -> None:
        maintenance.PREVIEWS.clear()
        self.token = maintenance.TOKEN
        maintenance.TOKEN = "test-token"

    def tearDown(self) -> None:
        maintenance.TOKEN = self.token
        maintenance.PREVIEWS.clear()
        maintenance.UPLOAD_SESSIONS.clear()

    def test_preview_requires_valid_token(self) -> None:
        with self.assertRaises(HTTPException) as context:
            maintenance._auth("Bearer incorrect")
        self.assertEqual(401, context.exception.status_code)

    @patch("tools.kb_maintenance_api._run", return_value="dry-run")
    def test_preview_does_not_commit_and_matching_payload_is_required(self, run) -> None:
        payload = {"question": "收入何时确认？", "answer": "需判断控制权转移。", "title": "", "slug": "revenue-qa", "source": "local-qa-log", "tags": "", "related": ""}
        preview = maintenance._preview("qa", payload, ["qa-capture", "--question", payload["question"]])
        self.assertEqual(1, run.call_count)
        with self.assertRaises(HTTPException) as context:
            maintenance._commit(preview["preview_token"], "qa", {**payload, "answer": "不同内容"})
        self.assertEqual(409, context.exception.status_code)

    def test_pending_review_preview_requires_explicit_confirmation(self) -> None:
        pending = maintenance.pending_review("Bearer test-token")
        self.assertTrue(pending["items"])
        path = pending["items"][0]["path"]
        with self.assertRaises(HTTPException) as context:
            maintenance.review_preview(maintenance.ReviewPreview(path=path, confirmed=False), "Bearer test-token")
        self.assertEqual(400, context.exception.status_code)

        preview = maintenance.review_preview(maintenance.ReviewPreview(path=path, confirmed=True), "Bearer test-token")
        self.assertEqual("review", preview["kind"])
        self.assertIn("answer_ready", preview["output"])
        self.assertTrue(preview["review"]["body"])
        self.assertEqual(pending["items"][0]["content_sha256"], preview["review"]["content_sha256"])

    def test_review_commit_rejects_content_changed_after_preview(self) -> None:
        item = maintenance.pending_review("Bearer test-token")["items"][0]
        payload = maintenance.ReviewPreview(path=item["path"], confirmed=True, content_sha256=item["content_sha256"])
        preview = maintenance.review_preview(payload, "Bearer test-token")
        with patch("tools.kb_maintenance_api._file_sha256", return_value="0" * 64), self.assertRaises(HTTPException) as context:
            maintenance.review_commit(payload, preview["preview_token"], "Bearer test-token")
        self.assertEqual(409, context.exception.status_code)

    @patch("tools.kb_maintenance_api._run")
    def test_demo_mode_accepts_demo_token_without_writing(self, run) -> None:
        original_demo = maintenance.DEMO_MODE
        original_token = maintenance.TOKEN
        maintenance.DEMO_MODE = True
        maintenance.TOKEN = ""
        payload = {"question": "收入何时确认？", "answer": "需判断控制权转移。", "title": "", "slug": "revenue-qa", "source": "local-qa-log", "tags": "", "related": ""}
        try:
            maintenance._auth("Bearer demo")
            preview = maintenance._preview("qa", payload, ["qa-capture"])
            result = maintenance._commit(preview["preview_token"], "qa", payload)
        finally:
            maintenance.DEMO_MODE = original_demo
            maintenance.TOKEN = original_token
        self.assertEqual("committed", result["status"])
        self.assertIn("未写入知识库", result["output"])
        run.assert_not_called()

    def test_demo_ai_config_does_not_persist_secret(self) -> None:
        original_demo = maintenance.DEMO_MODE
        maintenance.DEMO_MODE = True
        try:
            result = maintenance.update_ai_config(
                maintenance.AIConfigPayload(base_url="https://example.com/v1", model="demo-model", enabled=True, api_key="secret"),
                "Bearer demo",
            )
        finally:
            maintenance.DEMO_MODE = original_demo
        self.assertTrue(result["simulated"])
        self.assertTrue(result["key_configured"])
        self.assertNotIn("secret", result)

    def test_saved_ai_config_returns_status_without_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"CPA_ZH_AI_CONFIG_PATH": str(Path(directory) / "ai-config.json")}):
            saved = ai_config.save_ai_config("openai-compatible", "https://example.com/v1", "demo-model", True, "secret")
            loaded = ai_config.public_ai_config()
        self.assertTrue(saved["key_configured"])
        self.assertEqual("demo-model", loaded["model"])
        self.assertNotIn("api_key", loaded)

    def test_ai_config_rejects_remote_http_and_clears_key_when_host_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"CPA_ZH_AI_CONFIG_PATH": str(Path(directory) / "ai-config.json")}):
            with self.assertRaises(ValueError):
                ai_config.save_ai_config("openai-compatible", "http://example.com/v1", "demo-model", True, "secret")
            ai_config.save_ai_config("openai-compatible", "https://first.example/v1", "demo-model", True, "secret")
            changed = ai_config.save_ai_config("openai-compatible", "https://second.example/v1", "demo-model", True, "")
        self.assertFalse(changed["key_configured"])

    def test_ai_config_allows_loopback_http(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"CPA_ZH_AI_CONFIG_PATH": str(Path(directory) / "ai-config.json")}):
            saved = ai_config.save_ai_config("openai-compatible", "http://127.0.0.1:11434/v1", "local-model", True, "local-secret")
        self.assertTrue(saved["key_configured"])

    def test_markdown_upload_is_extracted_named_and_committed_in_demo(self) -> None:
        original_demo = maintenance.DEMO_MODE
        maintenance.DEMO_MODE = True
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(maintenance, "UPLOAD_ROOT", Path(directory)):
                preview = asyncio.run(
                    maintenance.upload_ingest(
                        [UploadFile(file=io.BytesIO("# 收入确认案例\n\n控制权已经转移。".encode("utf-8")), filename="case.md")],
                        "Bearer demo",
                    )
                )
                self.assertEqual("收入确认案例", preview["items"][0]["batch_name"])
                self.assertIn("控制权已经转移", preview["items"][0]["markdown_preview"])
                staged_item = maintenance.UPLOAD_SESSIONS[preview["session_token"]]["items"][0]
                self.assertEqual("case.md", staged_item["source_path"].name)

                commit = maintenance.batch_ingest_commit(
                    maintenance.UploadCommit(
                        session_token=preview["session_token"],
                        items=[maintenance.UploadCommitItem(id=preview["items"][0]["id"], batch_name="收入确认复核批次")],
                    ),
                    "Bearer demo",
                )
                self.assertEqual(1, commit["imported_count"])
                self.assertIn("未写入知识库", commit["output"])
        finally:
            maintenance.DEMO_MODE = original_demo

    def test_upload_commit_rejects_tampered_staged_markdown(self) -> None:
        original_demo = maintenance.DEMO_MODE
        maintenance.DEMO_MODE = True
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(maintenance, "UPLOAD_ROOT", Path(directory)):
                preview = asyncio.run(maintenance.upload_ingest([UploadFile(file=io.BytesIO(b"# Source\n\nBody"), filename="source.md")], "Bearer demo"))
                staged = maintenance.UPLOAD_SESSIONS[preview["session_token"]]["items"][0]
                staged["markdown_path"].write_text("# Changed\n", encoding="utf-8")
                with self.assertRaises(HTTPException) as context:
                    maintenance.batch_ingest_commit(
                        maintenance.UploadCommit(session_token=preview["session_token"], items=[maintenance.UploadCommitItem(id=staged["id"], batch_name="tamper-check")]),
                        "Bearer demo",
                    )
                self.assertEqual(409, context.exception.status_code)
        finally:
            maintenance.DEMO_MODE = original_demo

    def test_cleanup_removes_expired_directories_left_by_previous_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.object(maintenance, "UPLOAD_ROOT", Path(directory)):
            expired = Path(directory) / "expired-session"
            expired.mkdir()
            old = time.time() - maintenance.UPLOAD_TTL_SECONDS - 10
            os.utime(expired, (old, old))
            maintenance._cleanup_upload_sessions()
            self.assertFalse(expired.exists())

    def test_batch_name_prefers_markdown_heading(self) -> None:
        name = maintenance._batch_name_from_markdown("---\ntitle: ignored\n---\n\n## 长期股权投资判断\n\n正文", "fallback.md")
        self.assertEqual("长期股权投资判断", name)

    def test_extracted_document_batch_name_uses_content_instead_of_filename(self) -> None:
        name = maintenance._batch_name_from_markdown("# generic-file\n\n企业会计准则第十四号收入确认\n\n正文", "generic-file.pdf")
        self.assertEqual("企业会计准则第十四号收入确认", name)


if __name__ == "__main__":
    unittest.main()
