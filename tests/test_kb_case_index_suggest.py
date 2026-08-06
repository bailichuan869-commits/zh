from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))

from kb_case_index_suggest import load_cases


class CaseIndexSuggestTests(unittest.TestCase):
    def test_load_cases_excludes_index_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = root / "wiki" / "cases"
            cases.mkdir(parents=True)
            (cases / "case.md").write_text(
                "---\ntitle: 示例案例\ntype: case\ncase_type: accounting\n---\n\n## 一句话结论\n\n结论。\n",
                encoding="utf-8",
            )
            (cases / "index.md").write_text(
                "---\ntitle: 案例索引\ntype: concept\nconcept_type: index\npage_role: index\n---\n",
                encoding="utf-8",
            )

            loaded = load_cases(root)

        self.assertEqual(["wiki/cases/case.md"], [case.rel_path for case in loaded])


if __name__ == "__main__":
    unittest.main()
