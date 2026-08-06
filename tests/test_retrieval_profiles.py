from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi import HTTPException

PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.services.retrieval import asset_for_path, resolve_profile, retrieve
from tools.kb_common import asset_metadata


class RetrievalProfileTests(unittest.TestCase):
    def test_profiles_are_versioned_and_expose_distinct_governance(self) -> None:
        name, current = resolve_profile("answer-current")
        self.assertEqual("answer-current", name)
        self.assertTrue(current["answer_ready_only"])
        self.assertEqual(["valid"], current["lifecycle_status"])
        self.assertNotEqual(current, resolve_profile("general-search")[1])

    def test_asset_projection_preserves_source_and_version_fields(self) -> None:
        asset = asset_metadata(
            "wiki/cases/example.md",
            {
                "sources": ["official-source"],
                "tags": ["case", "revenue"],
                "effective_date": "2026-01-01",
                "status": "superseded",
            },
            kind="wiki",
            page_role="case",
            body="正文",
            answer_ready=False,
        )
        self.assertEqual("official-source", asset["source_id"])
        self.assertEqual(["case", "revenue"], asset["tags"])
        self.assertEqual("2026-01-01", asset["effective_from"])
        self.assertEqual("superseded", asset["lifecycle_status"])
        self.assertTrue(asset["content_sha256"])

    def test_current_retrieval_returns_chapter_trace_and_filters(self) -> None:
        response = retrieve("收入确认", profile="answer-current", limit=3)
        self.assertEqual("answer-current", response["profile"])
        self.assertEqual("chunks-fts5", response["engine"])
        self.assertTrue(response["retrieval_trace"]["stages"])
        self.assertTrue(response["results"])
        self.assertTrue(all(item["lifecycle_status"] == "valid" for item in response["results"]))
        self.assertTrue(all(item["answer_ready"] for item in response["results"]))
        self.assertTrue(all(item["section_anchor"].startswith("section-") for item in response["results"]))

    def test_invalid_date_and_profile_are_rejected(self) -> None:
        with self.assertRaises(HTTPException) as date_error:
            retrieve("收入确认", as_of="2026/01/01")
        self.assertEqual(400, date_error.exception.status_code)
        with self.assertRaises(HTTPException) as profile_error:
            retrieve("收入确认", profile="unknown-profile")
        self.assertEqual(400, profile_error.exception.status_code)

    def test_asset_projection_is_available_for_document_reads(self) -> None:
        asset = asset_for_path("wiki/cases/2026-08-first-issue-medical-distributor-revenue.md")
        self.assertTrue(asset["asset_id"])
        self.assertEqual("wiki/cases/2026-08-first-issue-medical-distributor-revenue.md", asset["path"])
        self.assertIn("lifecycle_status", asset)


if __name__ == "__main__":
    unittest.main()
