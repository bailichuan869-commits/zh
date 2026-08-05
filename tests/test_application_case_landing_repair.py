from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import repair_application_case_landing_pages as repair
from kb_common import parse_frontmatter


LANDING_DIR = repair.LANDING_RELATIVE
ATTACHMENT_DIR = repair.ATTACHMENT_RELATIVE


def write_page(path: Path, frontmatter: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}\n", encoding="utf-8", newline="\n")


class ApplicationCaseLandingRepairTests(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def write_landing(self, root: Path, name: str = "001-示例.html.md") -> Path:
        path = root / LANDING_DIR / name
        write_page(
            path,
            """
title: "示例标题"
type: "raw-source"
source_type: "html"
source_role: "attachment-landing"
source_url: "https://kjs.mof.gov.cn/example.htm"
article_id: "1"
original_file: "raw/_archive/example.html"
created: "2026-07-28"
retrieved_at: "2026-07-28"
sha256: "landing-sha"
""",
            """
# 示例标题

参见附件

附件下载：

示例标题.pdf

相关文章：
""",
        )
        return path

    def write_attachment(
        self,
        root: Path,
        name: str = "001-P020000000000000000001.pdf.md",
        status: str = "ok",
    ) -> Path:
        path = root / ATTACHMENT_DIR / name
        write_page(
            path,
            f"""
title: "示例标题"
type: "raw-source"
source_type: "pdf"
source_role: "substantive-attachment"
source_url: "https://kjs.mof.gov.cn/example.htm"
attachment_url: "https://kjs.mof.gov.cn/example.pdf"
article_id: "1"
original_file: "raw/_archive/example.pdf"
sha256: "attachment-sha"
extraction_status: "{status}"
""",
            """
# 示例标题

<!-- source-page: 1 -->

示例标题

第一段文字被

PDF 抽取拆成

多个短行。

分析依据：相关准则条款。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。

本段用于模拟真实附件正文的长度，确保正文明显长于只有附件下载的落地页。
""",
        )
        return path

    def test_dry_run_matches_attachment_without_writing(self) -> None:
        root = self.make_root()
        landing = self.write_landing(root)
        self.write_attachment(root)
        before = landing.read_text(encoding="utf-8")

        result = repair.repair(root, apply=False)

        self.assertEqual(1, result["target_count"])
        self.assertEqual(1, result["changed_count"])
        self.assertEqual(before, landing.read_text(encoding="utf-8"))
        self.assertEqual(
            "raw/standards/accounting/application-case-attachments/001-P020000000000000000001.pdf.md",
            result["targets"][0]["attachment"],
        )

    def test_apply_writes_only_landing_page_with_traceability_metadata(self) -> None:
        root = self.make_root()
        landing = self.write_landing(root)
        attachment = self.write_attachment(root)
        attachment_before = attachment.read_text(encoding="utf-8")

        result = repair.repair(root, apply=True)

        self.assertEqual(1, result["changed_count"])
        self.assertEqual(attachment_before, attachment.read_text(encoding="utf-8"))
        updated = landing.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(updated)
        self.assertEqual("landing-sha", metadata["sha256"])
        self.assertEqual("substantive-attachment", metadata["content_source_role"])
        self.assertEqual("attachment-sha", metadata["content_source_sha256"])
        self.assertEqual("https://kjs.mof.gov.cn/example.pdf", metadata["attachment_url"])
        self.assertIn("第一段文字被PDF 抽取拆成多个短行。", body)
        self.assertNotIn("参见附件", body)
        rerun = repair.repair(root, apply=False)
        self.assertEqual(1, rerun["target_count"])
        self.assertEqual(0, rerun["changed_count"])

    def test_validation_rejects_missing_multiple_and_non_ok_attachments(self) -> None:
        root = self.make_root()
        self.write_landing(root)
        with self.assertRaisesRegex(repair.RepairError, "expected exactly one matching attachment"):
            repair.collect_targets(root)

        root = self.make_root()
        self.write_landing(root)
        self.write_attachment(root, "001-A.pdf.md")
        self.write_attachment(root, "001-B.pdf.md")
        with self.assertRaisesRegex(repair.RepairError, "expected exactly one matching attachment"):
            repair.collect_targets(root)

        root = self.make_root()
        self.write_landing(root)
        self.write_attachment(root, status="needs-review")
        with self.assertRaisesRegex(repair.RepairError, "extraction_status is not ok"):
            repair.collect_targets(root)

    def test_reflow_preserves_markers_lists_entries_and_tables(self) -> None:
        body = """
# 示例标题

<!-- source-page: 1 -->

示例标题

第一段文字被

拆成短行。

1. 账务处理：

借：合同资产

贷：主营业务收入

| 项目 | 金额 |

|---|---:|

| 收入 | 100 |

<!-- source-page: 2 -->

第二页继续

说明。

2
"""

        rendered = repair.reflow_body(body, "示例标题")

        self.assertIn("# 示例标题", rendered)
        self.assertIn("<!-- source-page: 1 -->", rendered)
        self.assertIn("<!-- source-page: 2 -->", rendered)
        self.assertIn("第一段文字被拆成短行。", rendered)
        self.assertIn("1. 账务处理：", rendered)
        self.assertIn("借：合同资产", rendered)
        self.assertIn("贷：主营业务收入", rendered)
        self.assertIn("| 项目 | 金额 |", rendered)
        self.assertIn("|---|---:|", rendered)
        self.assertNotIn("\n\n示例标题\n\n第一段", rendered)
        self.assertNotIn("\n\n2\n", rendered)

    def test_reflow_keeps_compact_pdf_table_rows_separate(self) -> None:
        body = """
# PPP项目合同社会资本方会计处理应用案例——金融资产模式

<!-- source-page: 1 -->

单位：万元

项目年份成本收入

2×21 年-2×22 年4 000 4 200（=4 000×（1+5%））建造服务（每年）

2×23 年-2×30 年80 96（=80×（1+20%））运营服务（每年）

假设合同期间各年的现金流均在年末发生。
"""

        rendered = repair.reflow_body(body, "PPP项目合同社会资本方会计处理应用案例——金融资产模式")

        self.assertIn("\n\n项目年份成本收入\n\n", rendered)
        self.assertIn("\n\n2×21 年-2×22 年4 000 4 200", rendered)
        self.assertIn("\n\n假设合同期间各年的现金流均在年末发生。", rendered)


if __name__ == "__main__":
    unittest.main()
