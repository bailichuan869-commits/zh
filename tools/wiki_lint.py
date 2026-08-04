#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CPA-ZH wiki lint: 检测断链(broken links)与孤立页(orphan pages)。

链接约定：[[concepts/foo/bar]] 表示从 wiki/ 根起的相对路径（不含 .md）。
解析优先级：
  1) 精确 slug 匹配（wiki/<link>.md 存在）
  2) 含 "/" 时尝试 endswith 后缀匹配（兼容省略前缀的写法）
  3) 裸名匹配（link 不含 "/"，按文件名匹配）
不解析指向 raw/ 的链接（那是合法外部引用，非 wiki 页）。
"""
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WIKI = PROJECT_ROOT / "knowledge-base" / "CPA-ZH" / "wiki"
REPORT_PATH = PROJECT_ROOT / "workspace" / "outputs" / "wiki_lint_report.md"

pages = {}          # slug(相对wiki/的posix,无.md) -> Path
name_to_slugs = {}  # 末级文件名 -> [slug,...]
for md in sorted(WIKI.rglob("*.md")):
    if "_trash" in md.parts:   # 暂存区卡片内部互链无意义，跳过
        continue
    slug = md.relative_to(WIKI).as_posix()[:-3]
    pages[slug] = md
    name = slug.rsplit("/", 1)[-1]
    name_to_slugs.setdefault(name, []).append(slug)

link_re = re.compile(r"\[\[([^\]]+)\]\]")


def normalize(raw):
    raw = raw.split("|")[0].split("#")[0].strip()
    return raw


def resolve(target):
    if target.startswith("raw/") or target.startswith("/"):
        return ("external", None)
    if target in pages:
        return ("ok", target)
    if "/" in target:
        matches = [s for s in pages if s == target or s.endswith("/" + target) or s.endswith(target)]
        if matches:
            return ("ok", matches[0])
    else:
        if target in name_to_slugs:
            return ("ok", name_to_slugs[target][0])
    return ("broken", target)


inbound = {}      # slug -> set(来源slug)
broken = {}       # 来源slug -> [(target, raw)]
ambiguous = {}    # 来源slug -> [target]

for slug, md in pages.items():
    try:
        text = md.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    seen = set()
    for m in link_re.findall(text):
        tgt = normalize(m)
        if not tgt or tgt in seen:
            continue
        seen.add(tgt)
        status, resolved = resolve(tgt)
        if status == "ok":
            inbound.setdefault(resolved, set()).add(slug)
        elif status == "external":
            continue
        else:
            broken.setdefault(slug, []).append(tgt)

orphans = [s for s in pages if s not in inbound]

# 汇总输出
out = []
out.append(f"# Wiki Lint Report")
out.append(f"")
out.append(f"- wiki 页总数: {len(pages)}")
out.append(f"- 断链来源页数: {len(broken)}")
out.append(f"- 孤立页数: {len(orphans)}")
out.append(f"")

out.append(f"## 断链明细 (broken links)")
total_broken = sum(len(v) for v in broken.values())
out.append(f"共 {total_broken} 条断链，分布在 {len(broken)} 个页面：")
out.append(f"")
for slug in sorted(broken.keys()):
    out.append(f"- **{slug}** ({len(broken[slug])}条)")
    for t in broken[slug]:
        out.append(f"  - `[[{t}]]`")
out.append(f"")

out.append(f"## 孤立页明细 (orphan pages, 无入链)")
out.append(f"共 {len(orphans)} 页（仅列前 60）：")
out.append(f"")
for s in sorted(orphans)[:60]:
    out.append(f"- {s}")
if len(orphans) > 60:
    out.append(f"- ... 其余 {len(orphans)-60} 页略")

report = "\n".join(out)
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.write_text(report, encoding="utf-8")
print("DONE pages=%d broken_src=%d total_broken=%d orphans=%d" % (
    len(pages), len(broken), total_broken, len(orphans)))
