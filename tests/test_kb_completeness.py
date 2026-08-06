import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from kb_completeness import collect, render_report


class KnowledgeCompletenessTests(unittest.TestCase):
    def write_page(self, root: Path, relative: str, text: str) -> None:
        path = root / "wiki" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_flags_content_source_and_link_gaps_but_exempts_law_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_page(
                root,
                "concepts/complete.md",
                """---
title: 完整专题
type: concept
page_role: knowledge
sources: [source-a]
---
# 完整专题
## 定位
有完整的来源和判断内容。
## 判断
这里是足够长的结构化正文，用于验证完整性扫描不会把正常页面标记为骨架。
""",
            )
            self.write_page(
                root,
                "concepts/pending.md",
                """---
title: 待补专题
type: concept
page_role: knowledge
---
# 待补专题
## 待补充
后续可继续补充来源和实际案例。
""",
            )
            self.write_page(
                root,
                "concepts/laws/sample-law/index.md",
                """---
title: 合并全文索引
type: concept
page_role: index
---
# 合并全文索引
### 第一条 {#article-001}
原文。
""",
            )
            self.write_page(
                root,
                "concepts/broken.md",
                """---
title: 断链专题
type: concept
page_role: knowledge
sources: [source-a]
---
# 断链专题
## 定位
这是一个结构完整的页面。
## 判断
内容足够长，且指向 [[concepts/missing-page]]。
""",
            )
            self.write_page(
                root,
                "concepts/kb-content-completeness-report.md",
                "---\ntitle: 完整性报告\npage_role: index\n---\n",
            )

            data = collect(root)
            by_path = {page["path"]: page for page in data["pages"]}
            pending_kinds = {item["kind"] for item in by_path["wiki/concepts/pending.md"]["issues"]}
            broken_kinds = {item["kind"] for item in by_path["wiki/concepts/broken.md"]["issues"]}
            law_index = by_path["wiki/concepts/laws/sample-law/index.md"]

            self.assertIn("pending-content", pending_kinds)
            self.assertIn("missing-source", pending_kinds)
            self.assertIn("skeleton", pending_kinds)
            self.assertIn("broken-wiki-link", broken_kinds)
            self.assertTrue(law_index["intentional"])
            self.assertFalse(law_index["issues"])
            self.assertNotIn("wiki/concepts/kb-content-completeness-report.md", by_path)

            report = render_report(data)
            self.assertIn("不按“一条一个知识页”拆分", report)
            self.assertIn("completeness --write-report", report)


if __name__ == "__main__":
    unittest.main()
