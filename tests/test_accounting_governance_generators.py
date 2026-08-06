from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import apply_accounting_calibration_to_pages as calibration
import generate_accounting_interpretation_pages as interpretations
import generate_accounting_standards_calibration as standards_calibration
import generate_accounting_standards_number_index as standards_index
from kb_common import parse_frontmatter


class AccountingGovernanceGeneratorTests(unittest.TestCase):
    def test_interpretation_update_preserves_body_and_verified_dates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            wiki_dir = Path(temp)
            page = wiki_dir / "interp-10.md"
            page.write_text("---\ntitle: 解释第10号\n---\n\n# 保留正文\n", encoding="utf-8")
            row = {"Title": "企业会计准则解释第10号", "LocalFile": "", "Url": "https://example.test/10"}

            with patch.object(interpretations, "WIKI_DIR", wiki_dir):
                interpretations.write_page(row, "10")
                first = page.read_bytes()
                interpretations.write_page(row, "10")

            metadata, body = parse_frontmatter(page.read_text(encoding="utf-8"))
            self.assertIn("# 保留正文", body)
            self.assertEqual("2017-06-12", metadata["published_on"])
            self.assertEqual("2018-01-01", metadata["effective_from"])
            self.assertEqual("unknown", metadata["lifecycle_status"])
            self.assertFalse(metadata["answer_ready"])
            self.assertEqual(first, page.read_bytes())
            self.assertFalse(first.startswith(b"\xef\xbb\xbf"))

    def test_other_rule_update_is_governed_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "vat-accounting.md"
            page.write_text("---\ntitle: 增值税会计处理规定\n---\n\n# 保留正文\n", encoding="utf-8")
            governance = {
                page: {
                    "page_role": "knowledge",
                    "maturity": "reviewed",
                    "answer_ready": False,
                    "review_status": "agent-reviewed",
                    "version": "caihui-2016-22",
                    "effective_from": "2016-12-03",
                    "lifecycle_status": "unknown",
                }
            }
            rows = [
                {
                    "SourceType": "其他规定",
                    "Title": "关于印发《增值税会计处理规定》的通知",
                    "Confidence": "high",
                    "Reason": "增值税专题规定",
                    "Url": "https://example.test/vat",
                    "LocalPath": "raw/vat.md",
                }
            ]

            with (
                patch.object(calibration, "OTHER_RULE_PAGES", {page: ("增值税会计处理规定", "说明")}),
                patch.object(calibration, "OTHER_RULE_GOVERNANCE", governance),
            ):
                calibration.upsert_supplement(page, [("增值税", rows)])
                first = page.read_bytes()
                calibration.upsert_supplement(page, [("增值税", rows)])

            metadata, body = parse_frontmatter(page.read_text(encoding="utf-8"))
            self.assertIn("# 保留正文", body)
            self.assertEqual("2016-12-03", metadata["effective_from"])
            self.assertEqual("unknown", metadata["lifecycle_status"])
            self.assertFalse(metadata["answer_ready"])
            self.assertEqual(first, page.read_bytes())
            self.assertFalse(first.startswith(b"\xef\xbb\xbf"))

    def test_covid_rule_is_historical_and_boundary_note_is_idempotent(self) -> None:
        covid_page = calibration.OTHER_RULES_DIR / "covid-rent-concessions.md"
        governance = calibration.OTHER_RULE_GOVERNANCE[covid_page]

        self.assertEqual("2020-06-19", governance["effective_from"])
        self.assertEqual("historical", governance["lifecycle_status"])
        self.assertFalse(governance["answer_ready"])
        self.assertNotIn("effective_to", governance)

        original = "---\ntitle: 疫情租金减让\n---\n\n# 正文\n\n<!-- calibration-supplement:start -->\n<!-- calibration-supplement:end -->\n"
        first = calibration.upsert_covid_boundary(original)
        second = calibration.upsert_covid_boundary(first)

        self.assertEqual(first, second)
        self.assertEqual(1, first.count(calibration.COVID_BOUNDARY_START))
        self.assertIn("不作为当前期间会计答疑的默认依据", first)
        self.assertIn("不编造 `effective_to`", first)

    def test_governance_applies_without_calibration_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "cash-pooling.md"
            page.write_text("---\ntitle: 资金集中管理\n---\n\n# 正文\n", encoding="utf-8")
            fields = {
                "version": "application-case-2022-01-24",
                "effective_from": "unknown",
                "lifecycle_status": "unknown",
                "answer_ready": False,
                "review_status": "agent-reviewed",
            }

            self.assertTrue(calibration.apply_page_governance(page, fields))
            first = page.read_bytes()
            self.assertFalse(calibration.apply_page_governance(page, fields))

            metadata, body = parse_frontmatter(page.read_text(encoding="utf-8"))
            self.assertEqual("application-case-2022-01-24", metadata["version"])
            self.assertEqual("unknown", metadata["effective_from"])
            self.assertEqual("unknown", metadata["lifecycle_status"])
            self.assertFalse(metadata["answer_ready"])
            self.assertEqual("agent-reviewed", metadata["review_status"])
            self.assertIn("# 正文", body)
            self.assertEqual(first, page.read_bytes())

    def test_accounting_csv_generators_write_utf8_without_bom(self) -> None:
        writers = (
            interpretations.write_csv,
            standards_calibration.write_csv,
            standards_index.write_csv,
        )
        with tempfile.TemporaryDirectory() as temp:
            for index, writer in enumerate(writers):
                path = Path(temp) / f"output-{index}.csv"
                writer(path, [{"标题": "企业会计准则", "状态": "已复核"}])
                data = path.read_bytes()
                self.assertFalse(data.startswith(b"\xef\xbb\xbf"))
                self.assertIn("企业会计准则", data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
