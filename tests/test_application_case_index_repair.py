from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import repair_application_case_index_pages as repair
from kb_common import parse_frontmatter


def write_markdown(path: Path, frontmatter: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}\n", encoding="utf-8", newline="\n")


class ApplicationCaseIndexRepairTests(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def write_index(self, root: Path, case_title: str = "收入准则应用案例——运输服务") -> Path:
        path = root / repair.INDEX_RELATIVE / "srzzyy-收入准则应用案例-index.html.md"
        write_markdown(
            path,
            """
title: "srzzyy-收入准则应用案例-index"
type: "raw-source"
source_type: "web-snapshot"
source_role: "index-page"
original_file: "raw/_archive/index.html"
""",
            f"""
# srzzyy-收入准则应用案例-index

财政部视频号财政部
Android下载
企业会计准则>
应用案例>
收入准则应用案例
{case_title}
2018-12-11
联系我们
""",
        )
        return path

    def write_page(self, root: Path, name: str = "001-收入准则应用案例-运输服务.html.md") -> Path:
        path = root / repair.PAGES_RELATIVE / name
        write_markdown(path, 'title: "收入准则应用案例——运输服务"\nsource_role: "attachment-landing"', "# 正文")
        return path

    def write_attachment(self, root: Path, name: str = "001-P020000000000000000001.pdf.md") -> Path:
        path = root / repair.ATTACHMENTS_RELATIVE / name
        write_markdown(path, 'title: "收入准则应用案例——运输服务"\nsource_role: "substantive-attachment"', "# 附件")
        return path

    def write_mapping(self, root: Path, rows: list[tuple[str, str]]) -> None:
        path = root / repair.MAPPING_RELATIVE
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["SourceType", "Title", "LocalPath"])
            writer.writeheader()
            for title, local_path in rows:
                writer.writerow({"SourceType": "application_case", "Title": title, "LocalPath": local_path})

    def prepare_valid_root(self) -> tuple[Path, Path, Path, Path]:
        root = self.make_root()
        index = self.write_index(root)
        page = self.write_page(root)
        attachment = self.write_attachment(root)
        self.write_mapping(root, [("收入准则应用案例——运输服务", page.relative_to(root).as_posix())])
        return root, index, page, attachment

    def test_dry_run_and_apply_only_repair_index_page(self) -> None:
        root, index, page, attachment = self.prepare_valid_root()
        index_before = index.read_text(encoding="utf-8")
        page_before = page.read_text(encoding="utf-8")
        attachment_before = attachment.read_text(encoding="utf-8")

        dry_run = repair.repair(root, apply=False)
        self.assertEqual(1, dry_run["target_count"])
        self.assertEqual(1, dry_run["changed_count"])
        self.assertEqual(index_before, index.read_text(encoding="utf-8"))

        applied = repair.repair(root, apply=True)
        self.assertEqual(1, applied["changed_count"])
        self.assertEqual(page_before, page.read_text(encoding="utf-8"))
        self.assertEqual(attachment_before, attachment.read_text(encoding="utf-8"))

        metadata, body = parse_frontmatter(index.read_text(encoding="utf-8"))
        self.assertEqual("raw/_archive/index.html", metadata["original_file"])
        self.assertEqual("readable-index", metadata["content_repaired_role"])
        self.assertEqual("1", metadata["index_item_count"])
        self.assertIn("# 收入准则应用案例", body)
        self.assertIn("| 案例 | 发布日期 | 本地正文页 | 附件 Markdown |", body)
        self.assertIn(page.relative_to(root).as_posix(), body)
        self.assertIn(attachment.relative_to(root).as_posix(), body)
        self.assertNotIn("财政部视频号", body)
        self.assertNotIn("Android下载", body)
        self.assertNotIn("联系我们", body)

        rerun = repair.repair(root, apply=False)
        self.assertEqual(0, rerun["changed_count"])

    def test_unmatched_case_is_rejected(self) -> None:
        root = self.make_root()
        self.write_index(root, "不存在的案例")
        page = self.write_page(root)
        self.write_mapping(root, [("收入准则应用案例——运输服务", page.relative_to(root).as_posix())])
        with self.assertRaisesRegex(repair.RepairError, "expected exactly one mapping"):
            repair.collect_targets(root)

    def test_missing_local_page_is_rejected(self) -> None:
        root = self.make_root()
        self.write_index(root)
        missing = (repair.PAGES_RELATIVE / "001-不存在.html.md").as_posix()
        self.write_mapping(root, [("收入准则应用案例——运输服务", missing)])
        with self.assertRaisesRegex(repair.RepairError, "mapped local page does not exist"):
            repair.collect_targets(root)

    def test_duplicate_mapping_is_rejected(self) -> None:
        root = self.make_root()
        self.write_index(root)
        first = self.write_page(root)
        second = self.write_page(root, "002-收入准则应用案例-运输服务.html.md")
        self.write_mapping(
            root,
            [
                ("收入准则应用案例——运输服务", first.relative_to(root).as_posix()),
                ("收入准则应用案例——运输服务", second.relative_to(root).as_posix()),
            ],
        )
        with self.assertRaisesRegex(repair.RepairError, "expected exactly one mapping"):
            repair.collect_targets(root)

    def test_missing_attachment_is_reported_as_warning(self) -> None:
        root = self.make_root()
        self.write_index(root)
        page = self.write_page(root)
        self.write_mapping(root, [("收入准则应用案例——运输服务", page.relative_to(root).as_posix())])

        result = repair.repair(root, apply=False)

        self.assertEqual(1, len(result["warnings"]))
        self.assertIn("no attachment Markdown found", result["warnings"][0])


if __name__ == "__main__":
    unittest.main()
