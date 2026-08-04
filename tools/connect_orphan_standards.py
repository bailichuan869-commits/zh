"""Batch-connect the 27 orphaned CAS/CSA standard pages into their domain index pages.

Approach:
- 17 CAS pages + 7 interpretation pages -> wiki/concepts/accounting-standards-system.md (重点入口)
- 3 CSA pages -> wiki/concepts/audit-standards-system.md (重点入口)

Each page title is read from its frontmatter `title:` (fallback to first `# ` heading),
and a `- [[link]] - <title>.` line is appended right before the `## 待补充` section.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "knowledge-base" / "CPA-ZH" / "wiki"

CAS = [
    "concepts/accounting-standards/cas-03",
    "concepts/accounting-standards/cas-05",
    "concepts/accounting-standards/cas-10",
    "concepts/accounting-standards/cas-12",
    "concepts/accounting-standards/cas-23",
    "concepts/accounting-standards/cas-24",
    "concepts/accounting-standards/cas-26",
    "concepts/accounting-standards/cas-27",
    "concepts/accounting-standards/cas-29",
    "concepts/accounting-standards/cas-32",
    "concepts/accounting-standards/cas-34",
    "concepts/accounting-standards/cas-35",
    "concepts/accounting-standards/cas-38",
    "concepts/accounting-standards/cas-39",
    "concepts/accounting-standards/cas-40",
    "concepts/accounting-standards/cas-41",
    "concepts/accounting-standards/cas-42",
]
INTERP = [
    "concepts/accounting-standards/interpretations/interp-04",
    "concepts/accounting-standards/interpretations/interp-05",
    "concepts/accounting-standards/interpretations/interp-06",
    "concepts/accounting-standards/interpretations/interp-07",
    "concepts/accounting-standards/interpretations/interp-08",
    "concepts/accounting-standards/interpretations/interp-11",
    "concepts/accounting-standards/interpretations/interp-19",
]
CSA = [
    "concepts/audit-standards/csa-1152",
    "concepts/audit-standards/csa-1241",
    "concepts/audit-standards/csa-1331",
]


def get_title(rel_path: str) -> str:
    fp = BASE / f"{rel_path}.md"
    text = fp.read_text(encoding="utf-8")
    m = re.search(r"^title:\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    return rel_path.split("/")[-1]


def build_block(rel_paths, label):
    lines = [f"<!-- 补充接入：{label}（原孤立页，2026-07-23 接入） -->"]
    for p in rel_paths:
        title = get_title(p)
        lines.append(f"- [[{p}]] - {title}。")
    return "\n".join(lines) + "\n"


def insert_before_todo(system_path: str, block: str, marker="\n## 待补充"):
    fp = BASE / system_path  # system_path is e.g. concepts/accounting-standards-system.md
    text = fp.read_text(encoding="utf-8")
    if "<!-- 补充接入" in text:
        print(f"SKIP {system_path} (already connected, idempotent guard)")
        return
    marker = "\n## 待补充"
    if marker not in text:
        raise SystemExit(f"marker not found in {system_path}")
    head, sep, tail = text.partition(marker)
    new_text = head.rstrip() + "\n\n" + block + sep + tail
    fp.write_text(new_text, encoding="utf-8")
    print(f"UPDATED {system_path} (+{block.count(chr(10))} lines)")


acct_block = build_block(CAS + INTERP, "企业会计准则及解释（CAS/interp）")
audit_block = build_block(CSA, "审计准则（CSA）")

insert_before_todo("concepts/accounting-standards-system.md", acct_block)
insert_before_todo("concepts/audit-standards-system.md", audit_block)
print("DONE")
