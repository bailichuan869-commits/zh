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

import generate_cicpa_professional_standards_number_index as generator
from kb_common import parse_frontmatter


def source_row(
    key: str,
    *,
    source_type: str = "standard",
    local_path: str = "raw/standards/audit/official.pdf",
    url: str = "https://www.cicpa.org.cn/xxfb/tzgg/202201/example.pdf",
) -> dict[str, str]:
    return {
        "StandardKey": key,
        "StandardFamily": "审计准则",
        "StandardTitle": "中国注册会计师审计准则测试页",
        "SourceType": source_type,
        "SourceTypeLabel": generator.TYPE_LABELS[source_type],
        "Title": "中国注册会计师审计准则测试页",
        "Group": "2022-鉴证业务基本准则等11项准则",
        "Url": url,
        "LocalPath": local_path,
        "Status": "ok",
        "SourceNote": "test",
        "MappingMethod": "title-standard-number",
        "Confidence": "high",
    }


class CicpaProfessionalStandardsGeneratorTests(unittest.TestCase):
    def test_existing_body_is_preserved_and_governance_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            wiki_dir = Path(temp)
            page = wiki_dir / "csa-1101.md"
            page.write_text(
                "---\ntitle: 原标题\nmaturity: draft\n---\n\n# 保留正文\n\n这里是已经形成的编辑内容。\n",
                encoding="utf-8",
            )
            rows = [source_row("csa-1101")]

            with patch.object(generator, "WIKI_DIR", wiki_dir):
                generator.write_standard_page("csa-1101", rows)
                first = page.read_bytes()
                generator.write_standard_page("csa-1101", rows)

            text = page.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(text)
            self.assertIn("# 保留正文", body)
            self.assertIn("这里是已经形成的编辑内容。", body)
            self.assertEqual("index", metadata["page_role"])
            self.assertEqual("reviewed", metadata["maturity"])
            self.assertEqual("agent-reviewed", metadata["review_status"])
            self.assertFalse(metadata["answer_ready"])
            self.assertEqual("unknown", metadata["lifecycle_status"])
            self.assertEqual("unknown", metadata["effective_from"])
            self.assertEqual(first, page.read_bytes())
            self.assertFalse(first.startswith(b"\xef\xbb\xbf"))

    def test_current_numbered_pages_split_into_19_knowledge_and_21_indexes(self) -> None:
        keys = {
            path.stem
            for path in generator.WIKI_DIR.glob("*.md")
            if path.stem not in {"topics", "unmapped"}
        }
        knowledge = {key for key in keys if generator.page_role_for_key(key) == "knowledge"}
        indexes = keys - knowledge

        self.assertEqual(40, len(keys))
        self.assertEqual(set(generator.AUDIT_SUPPLEMENTS), knowledge)
        self.assertEqual(19, len(knowledge))
        self.assertEqual(21, len(indexes))

    def test_primary_standard_source_wins_and_validity_stays_unknown(self) -> None:
        rows = [
            source_row(
                "csa-1101",
                source_type="guideline",
                local_path="raw/standards/audit/guideline.pdf",
            ),
            source_row(
                "csa-1101",
                source_type="standard",
                local_path="raw/standards/audit/standard.pdf",
            ),
        ]

        metadata = generator.audit_governance_metadata("csa-1101", rows, "正文")

        self.assertEqual("standard", metadata["source_type"])
        self.assertEqual("raw/standards/audit/standard.pdf", metadata["raw_path"])
        self.assertEqual("unknown", metadata["version"])
        self.assertEqual("unknown", metadata["effective_from"])
        self.assertEqual("unknown", metadata["lifecycle_status"])
        self.assertNotEqual("valid", metadata["lifecycle_status"])


if __name__ == "__main__":
    unittest.main()
