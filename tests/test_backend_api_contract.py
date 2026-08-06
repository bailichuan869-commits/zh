from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException


PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.api.v1.routers import library
from app.main import app
from app.schemas.library import AnswerRequest, AnswerResponse, DocumentResponse, HealthResponse, SearchResponse, SummaryResponse
from app.services import answers as answer_service
from app.services.library import plain_snippet


class BackendApiContractTests(unittest.TestCase):
    def setUp(self) -> None:
        library.library_service.build_backlinks()

    def test_active_api_routes_are_read_only_and_versioned(self) -> None:
        routes = {route.path: route.methods for route in app.routes if hasattr(route, "methods")}
        for route in app.routes:
            prefix = getattr(getattr(route, "include_context", None), "prefix", "")
            for child in getattr(getattr(route, "original_router", None), "routes", ()):
                routes[prefix + child.path] = child.methods
        expected = {
            "/api/v1/health",
            "/api/v1/library/summary",
            "/api/v1/navigation/tree",
            "/api/v1/search",
            "/api/v1/documents",
            "/api/v1/documents/backlinks",
            "/api/v1/files",
        }
        self.assertTrue(expected.issubset(routes))
        for path in expected:
            self.assertEqual({"GET"}, routes[path])
        self.assertEqual({"POST"}, routes["/api/v1/answers"])
        self.assertNotIn("/ui", routes)
        self.assertNotIn("/wiki", routes)
        self.assertNotIn("/raw", routes)

    def test_health_summary_search_and_document_match_declared_schemas(self) -> None:
        health = HealthResponse.model_validate(library.health())
        self.assertTrue(health.index_ready)
        self.assertEqual("ok", health.status)

        summary = SummaryResponse.model_validate(library.summary())
        self.assertGreater(summary.total, 0)
        self.assertGreater(summary.wiki_pages, 0)

        search = SearchResponse.model_validate(library.search("收入确认", domain="", kind="", limit=5, offset=0))
        self.assertGreater(search.total, 0)
        self.assertLessEqual(len(search.results), 5)
        self.assertTrue(all(result.path.startswith(("wiki/", "raw/")) for result in search.results))

        document = DocumentResponse.model_validate(library.document("wiki/index.md"))
        self.assertEqual("wiki/index.md", document.path)
        self.assertTrue(document.markdown)

    def test_law_index_backlinks_hide_same_family_pages(self) -> None:
        document = DocumentResponse.model_validate(library.document("wiki/concepts/laws/accounting-law/index.md"))
        self.assertEqual(
            [
                "concepts/law-accounting",
                "index",
                "sources/core-laws-article-index-2026-06-26",
            ],
            [item.path for item in document.backlinks],
        )

    def test_navigation_excludes_retired_calibration_bucket_pages(self) -> None:
        payload = json.loads(library.tree().body)
        accounting = next(domain for domain in payload["domains"] if domain["key"] == "accounting-standards")
        self.assertNotIn("calibration", {topic["key"] for topic in accounting["topics"]})
        self.assertFalse(
            any(
                page["path"].startswith("wiki/concepts/accounting-standards/calibration/")
                for topic in accounting["topics"]
                for page in topic["pages"]
            )
        )

    def test_search_snippets_are_plain_text(self) -> None:
        malicious = '<mark>收入</mark><img src=x onerror="alert(1)"><script>bad()</script>'
        snippet = plain_snippet(malicious)
        self.assertEqual("收入bad()", snippet)
        self.assertNotIn("<", snippet)

    def test_answers_return_evidence_gap_without_model_access(self) -> None:
        answer = AnswerResponse.model_validate(library.answer(AnswerRequest(question="不存在的虚构会计事项")))
        self.assertTrue(answer.insufficient_evidence)
        self.assertEqual("insufficient", answer.confidence)

    def test_answers_demo_mode_returns_local_citations_without_model_access(self) -> None:
        original = answer_service.DEMO_MODE
        answer_service.DEMO_MODE = True
        try:
            answer = AnswerResponse.model_validate(library.answer(AnswerRequest(question="收入确认")))
        finally:
            answer_service.DEMO_MODE = original
        self.assertFalse(answer.insufficient_evidence)
        self.assertEqual("demo", answer.confidence)
        self.assertTrue(answer.citations)

    def test_answers_require_model_key_when_reviewed_evidence_exists(self) -> None:
        with patch.object(answer_service, "DEMO_MODE", False), patch.object(
            answer_service, "load_ai_config", return_value={"enabled": False, "api_key": "", "model": "", "base_url": ""}
        ), patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False), self.assertRaises(HTTPException) as context:
            library.answer(AnswerRequest(question="医疗经销模式下签收", topic="revenue-recognition"))
        self.assertEqual(503, context.exception.status_code)

    def test_answer_topic_uses_canonical_and_legacy_topic_values(self) -> None:
        canonical = answer_service.answer_service.evidence("与标题无关的具体事实", "revenue-recognition")
        legacy = answer_service.answer_service.evidence("与标题无关的具体事实", "收入确认")
        self.assertEqual([], canonical)
        self.assertEqual([item["path"] for item in canonical], [item["path"] for item in legacy])

    def test_topic_does_not_make_an_unrelated_question_answerable(self) -> None:
        answer = AnswerResponse.model_validate(
            library.answer(AnswerRequest(question="火星矿产权益如何计量", topic="revenue-recognition"))
        )
        self.assertTrue(answer.insufficient_evidence)
        self.assertEqual([], answer.citations)

    def test_responses_api_text_is_read_from_rest_response_shape(self) -> None:
        payload = {"output": [{"content": [{"type": "output_text", "text": "第一段"}, {"type": "output_text", "text": "第二段"}]}]}
        self.assertEqual("第一段\n第二段", answer_service._response_text(payload))

    def test_navigation_tree_and_raw_file_access_stay_within_asset_boundaries(self) -> None:
        tree = library.tree()
        payload = json.loads(tree.body)
        self.assertTrue(payload["domains"])

        raw = library.file("raw/README.md")
        self.assertEqual("text/plain; charset=utf-8", raw.media_type)
        self.assertIn("no-store", raw.headers["cache-control"])

        for invalid_path in ("wiki/index.md", "../README.md", "raw/../wiki/index.md", "raw\\..\\wiki\\index.md", "C:/Windows/win.ini"):
            with self.assertRaises(HTTPException) as context:
                library.file(invalid_path)
            self.assertEqual(400, context.exception.status_code)

        for invalid_path in ("raw/README.md", "wiki/../raw/README.md", "wiki\\..\\raw\\README.md"):
            with self.assertRaises(HTTPException) as context:
                library.document(invalid_path)
            self.assertEqual(400, context.exception.status_code)


if __name__ == "__main__":
    unittest.main()
