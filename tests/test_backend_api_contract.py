from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from fastapi import HTTPException


PROJECT = Path(__file__).resolve().parents[1]
BACKEND = PROJECT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.api.v1.routers import library
from app.main import app
from app.schemas.library import DocumentResponse, HealthResponse, SearchResponse, SummaryResponse


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

    def test_navigation_tree_and_raw_file_access_stay_within_asset_boundaries(self) -> None:
        tree = library.tree()
        payload = json.loads(tree.body)
        self.assertTrue(payload["domains"])

        raw = library.file("raw/README.md")
        self.assertEqual("text/plain; charset=utf-8", raw.media_type)
        self.assertIn("no-store", raw.headers["cache-control"])

        for invalid_path in ("wiki/index.md", "../README.md", "C:/Windows/win.ini"):
            with self.assertRaises(HTTPException) as context:
                library.file(invalid_path)
            self.assertEqual(400, context.exception.status_code)


if __name__ == "__main__":
    unittest.main()
