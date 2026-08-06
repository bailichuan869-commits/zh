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

import generate_policy_documents_section as generator
from kb_common import parse_frontmatter


class PolicyDocumentGeneratorTests(unittest.TestCase):
    def test_governance_metadata_preserves_editorial_body_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            policy_page = root / "policy.md"
            supporting_page = root / "policy-index.md"
            policy_page.write_text("---\ntitle: Current policy\n---\n\n# Current body\n", encoding="utf-8")
            supporting_page.write_text("---\ntitle: Current index\n---\n\n# Current index body\n", encoding="utf-8")

            pages = {policy_page: "---\ntitle: Stale fallback\n---\n\n# Stale body\n"}
            policy_metadata = {
                policy_page: {
                    "page_role": "knowledge",
                    "answer_ready": False,
                    "review_status": "agent-reviewed",
                }
            }
            supporting_metadata = {
                supporting_page: {
                    "page_role": "index",
                    "answer_ready": False,
                    "review_status": "agent-reviewed",
                }
            }

            with (
                patch.object(generator, "PAGES", pages),
                patch.object(generator, "POLICY_METADATA", policy_metadata),
                patch.object(generator, "SUPPORTING_METADATA", supporting_metadata),
            ):
                generator.main()
                first_policy = policy_page.read_bytes()
                first_supporting = supporting_page.read_bytes()
                generator.main()

            policy_text = policy_page.read_text(encoding="utf-8")
            supporting_text = supporting_page.read_text(encoding="utf-8")
            policy_frontmatter, _ = parse_frontmatter(policy_text)
            supporting_frontmatter, _ = parse_frontmatter(supporting_text)

            self.assertIn("# Current body", policy_text)
            self.assertNotIn("Stale body", policy_text)
            self.assertEqual("knowledge", policy_frontmatter["page_role"])
            self.assertFalse(policy_frontmatter["answer_ready"])
            self.assertEqual("index", supporting_frontmatter["page_role"])
            self.assertFalse(supporting_frontmatter["answer_ready"])
            self.assertEqual(first_policy, policy_page.read_bytes())
            self.assertEqual(first_supporting, supporting_page.read_bytes())
            self.assertFalse(first_policy.startswith(b"\xef\xbb\xbf"))
            self.assertFalse(first_supporting.startswith(b"\xef\xbb\xbf"))


if __name__ == "__main__":
    unittest.main()
