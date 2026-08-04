#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本一致性语义扫描（Version-Consistency Semantic Scan）

目标：识别「注册会计师法 / 注会法」相关页面中，把法律当现行/最新/有效来引用，
却没有携带 2026 修订（主席令第七十八号，2026-06-26 通过，2027-01-01 施行）信号的页面。

分类：
  A. LAW_STRUCTURE_PAGE  已知法律结构页（条款页 / 概念页 / 草案页 / 来源页），版本意图明确，仅做信号自检。
  B. AWARE_OF_2026       提及法律且含 2026 修订信号 —— 视为已意识到新版本，OK。
  C. CURRENT_CLAIM_NO_SIGNAL  在法条附近做出「现行/最新/有效」等版本性声明但无 2026 信号 —— 高优先级。
  D. CITES_NO_SIGNAL     仅引用法律、无版本声明、无 2026 信号 —— 中低优先级（可能需脚注）。

运行：D:/ai-audit/.venv/Scripts/python.exe tools/version_consistency_scan.py
输出：workspace/outputs/version_consistency_scan.json 和 .md
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE = PROJECT_ROOT / "knowledge-base" / "CPA-ZH"
WIKI = BASE / "wiki"
REPORT_DIR = PROJECT_ROOT / "workspace" / "outputs"

LAW_TOKENS = ["注册会计师法", "注会法"]

# 2026 修订信号（与注会法 2026 修订强相关）
AMEND_SIGNALS = [
    "2026年", "2026 修订", "2026修订", "2026 修正", "2026修正",
    "2027年1月1日", "2027-01-01", "2027年",
    "主席令第七十八号", "第七十八号", "主席令78号", "主席令第78号",
    "修订草案", "修正草案",
    "cpa-law-2026-draft", "2026-amendment-highlights",
    "2026 修订草案", "2026修订草案",
    "草案（手工套用）", "手工套用",
    "2027年1月1日起施行",
]

# 法条附近的「版本性声明」关键词
CURRENT_CLAIM_KW = ["现行", "最新", "目前有效", "目前", "截至", "生效中",
                    "现.*有效", "施行中", "有效版本", "现行有效", "现行版本",
                    "最新版本", "本法自", "自1994", "2014年修正", "2014 修正"]

# 已知法律结构页（版本意图明确，不做 stale 判定）
LAW_STRUCTURE_PATHS = [
    "wiki/concepts/law-cpa.md",
    "wiki/concepts/laws/cpa-law/index.md",
    "wiki/concepts/laws/cpa-law-2026-draft.md",
    "wiki/concepts/laws/cpa-law/2026-amendment-highlights.md",
    "wiki/sources/cpa-law-amendment-2026.md",
]
LAW_STRUCTURE_RE = re.compile(r"cpa-law-article-\d+\.md$|注册会计师法-修改决定-2026\.md$")


def has_amend_signal(text: str) -> bool:
    return any(s in text for s in AMEND_SIGNALS)


def current_claim_near_law(text: str, window: int = 60):
    """返回所有命中法条附近的版本性声明片段。"""
    hits = []
    for tok in LAW_TOKENS:
        for m in re.finditer(re.escape(tok), text):
            start = max(0, m.start() - window)
            end = min(len(text), m.end() + window)
            ctx = text[start:end]
            for kw in CURRENT_CLAIM_KW:
                if re.search(kw, ctx):
                    hits.append(ctx.replace("\n", " ").strip())
                    break
    return hits


def classify(rel: str, text: str):
    is_structure = rel in LAW_STRUCTURE_PATHS or bool(LAW_STRUCTURE_RE.search(rel))
    aware = has_amend_signal(text)
    claims = current_claim_near_law(text)
    if is_structure:
        cat = "A.LAW_STRUCTURE_PAGE"
    elif aware:
        cat = "B.AWARE_OF_2026"
    elif claims:
        cat = "C.CURRENT_CLAIM_NO_SIGNAL"
    else:
        cat = "D.CITES_NO_SIGNAL"
    return cat, aware, claims, is_structure


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for md in sorted(WIKI.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not any(t in text for t in LAW_TOKENS):
            continue
        rel = str(md.relative_to(BASE)).replace("\\", "/")
        cat, aware, claims, is_structure = classify(rel, text)
        # 统计该页提及次数（粗）
        mention = sum(text.count(t) for t in LAW_TOKENS)
        rows.append({
            "rel": rel,
            "category": cat,
            "mentions": mention,
            "aware_2026": aware,
            "current_claim_snippets": claims[:3],
        })

    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1

    # 报告
    out_json = REPORT_DIR / "version_consistency_scan.json"
    out_json.write_text(json.dumps(
        {"total_law_pages": len(rows), "by_category": cats, "rows": rows},
        ensure_ascii=False, indent=2), encoding="utf-8")

    lines = []
    lines.append("# 版本一致性语义扫描报告（注册会计师法）\n")
    lines.append(f"- 扫描目录：`{WIKI}`")
    lines.append(f"- 提及「注册会计师法/注会法」的页面总数：**{len(rows)}**")
    lines.append(f"- 分类统计：{cats}\n")
    lines.append("## 高优先级：现行声明但无 2026 信号 (C)\n")
    c_rows = [r for r in rows if r["category"] == "C.CURRENT_CLAIM_NO_SIGNAL"]
    if not c_rows:
        lines.append("（无）\n")
    for r in c_rows:
        lines.append(f"### {r['rel']}  （提及 {r['mentions']} 次）")
        for s in r["current_claim_snippets"]:
            lines.append(f"> …{s}…")
        lines.append("")
    lines.append("## 中低优先级：仅引用无信号 (D)\n")
    d_rows = [r for r in rows if r["category"] == "D.CITES_NO_SIGNAL"]
    lines.append(f"共 {len(d_rows)} 页：\n")
    for r in d_rows:
        lines.append(f"- {r['rel']}（提及 {r['mentions']} 次）")
    lines.append("")
    lines.append("## 已感知 2026 修订 (B) 与法律结构页 (A)\n")
    lines.append(f"- A 法律结构页：{cats.get('A.LAW_STRUCTURE_PAGE',0)} 页")
    lines.append(f"- B 已含 2026 信号：{cats.get('B.AWARE_OF_2026',0)} 页\n")

    out_md = REPORT_DIR / "version_consistency_scan.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")

    # 控制台摘要
    print(f"[scan] total law pages = {len(rows)}")
    print(f"[scan] by category    = {cats}")
    print(f"[scan] C (high)       = {len(c_rows)}")
    print(f"[scan] D (mid/low)    = {len(d_rows)}")
    print(f"[scan] reports -> {out_json.name}, {out_md.name}")


if __name__ == "__main__":
    main()
