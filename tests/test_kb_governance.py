from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from kb_governance import collect, render_report


class KnowledgeGovernanceTests(unittest.TestCase):
    def test_collect_reports_explicit_metadata_and_admission_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "wiki" / "concepts" / "laws" / "example.md"
            report = root / "wiki" / "concepts" / "kb-governance-dashboard.md"
            raw = root / "raw" / "laws" / "example.md"
            page.parent.mkdir(parents=True)
            raw.parent.mkdir(parents=True)
            raw.write_text("官方原文\n", encoding="utf-8")
            page.write_text(
                "---\n"
                "title: 示例法律\n"
                "type: concept\n"
                "concept_type: regulation\n"
                "page_role: knowledge\n"
                "maturity: reviewed\n"
                "answer_ready: true\n"
                "created: 2026-01-01\n"
                "updated: 2026-01-01\n"
                "sources: [example-source]\n"
                "tags: [law]\n"
                "---\n\n"
                "## 定位\n\n正文\n\n## 规则\n\n规则正文\n",
                encoding="utf-8",
            )
            report.write_text("---\ntitle: 治理仪表盘\npage_role: index\n---\n", encoding="utf-8")
            (root / "source-registry.yml").write_text(
                "verified_documents:\n"
                "  - id: example-source\n"
                "    official_url: https://example.gov/doc\n"
                "    local_raw_path: raw/laws/example.md\n"
                "    status: valid\n"
                "    verified_on: 2026-01-01\n",
                encoding="utf-8",
            )

            data = collect(root)

        summary = data["summary"]
        self.assertEqual(1, summary["pages"])
        self.assertEqual(1, summary["high_risk_pages"])
        self.assertEqual(1, summary["verified_documents"])
        self.assertEqual(0, summary["registry_errors"])
        self.assertEqual(1, summary["issues"]["high-risk-missing-lifecycle"])
        self.assertEqual(1, summary["issues"]["answer-ready-without-review-status"])
        self.assertEqual(1, summary["explicit_field_coverage"]["source_id"])
        self.assertEqual(0, summary["explicit_field_coverage"]["asset_id"])
        self.assertEqual(0, summary["explicit_field_coverage"]["published_on"])
        self.assertEqual(0, summary["explicit_field_coverage"]["lifecycle_status"])
        self.assertNotIn("wiki/concepts/kb-governance-dashboard.md", {page["path"] for page in data["pages"]})

    def test_report_explains_agent_and_human_admission_boundary(self) -> None:
        data = {
            "summary": {
                "generated_at": "2026-08-06",
                "pages": 0,
                "roles": {},
                "high_risk_pages": 0,
                "answer_ready_pages": 0,
                "explicit_field_coverage": {},
                "issues": {},
                "verified_documents": 0,
                "registry_errors": 0,
            },
            "registry": {"verified_documents": [], "errors": []},
            "pages": [],
        }
        report = render_report(data)
        self.assertIn("agent-reviewed", report)
        self.assertIn("人工批准底线", report)
        self.assertIn("不把系统推导的默认值写成已核验事实", report)
