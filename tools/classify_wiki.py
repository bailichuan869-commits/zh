"""CPA-ZH 知识库语义分类模块。

职责：
1. 按路径规则为 wiki 页 / raw 文件推断语义化专题分类（domain 一级 / topic 二级）。
2. `apply` 子命令：把 domain/topic 写回 wiki 页 frontmatter（增量、幂等）。
3. `build` 子命令：扫描 wiki + raw，生成 search/navigation-tree.json（两级语义树 + 页面清单）。
4. `report` 子命令：只打印覆盖率报告，不写任何文件。

人工修正：tools/classify_overrides.json，格式 {"wiki/concepts/foo.md": {"domain": "...", "topic": "...", "short_title": "..."}}
运行（venv 绝对路径）：
  /d/ai-audit/.venv/Scripts/python.exe tools/classify_wiki.py report|apply|build
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = PROJECT_ROOT / "knowledge-base" / "CPA-ZH"
OVERRIDES_PATH = Path(__file__).resolve().parent / "classify_overrides.json"

# ---------------------------------------------------------------------------
# 分类体系定义：domain(一级) -> topics(二级)，顺序即展示顺序
# ---------------------------------------------------------------------------

DOMAINS: list[dict[str, Any]] = [
    {"key": "accounting-standards", "label": "会计准则", "icon": "📗", "topics": [
        ("overview", "体系总览"),
        ("basic", "基本准则"),
        ("cas", "具体准则（CAS）"),
        ("interpretations", "准则解释"),
        ("accounting-judgments", "会计判断专题"),
        ("other-rules", "其他会计规定"),
        ("raw-standards", "原文·准则文本"),
        ("raw-app-cases", "原文·应用案例"),
        ("raw-impl-qa", "原文·实施问答"),
        ("raw-interp", "原文·准则解释"),
        ("raw-other", "原文·其他资料"),
    ]},
    {"key": "audit-standards", "label": "审计准则", "icon": "📘", "topics": [
        ("overview", "体系总览"),
        ("assurance", "鉴证业务基本准则"),
        ("csa", "审计准则（CSA）"),
        ("review", "审阅准则"),
        ("other-assurance", "其他鉴证业务"),
        ("related-services", "相关服务"),
        ("raw-audit", "原文资料"),
    ]},
    {"key": "laws", "label": "法律法规", "icon": "⚖️", "topics": [
        ("overview", "法规总览"),
        ("cpa-law", "注册会计师法"),
        ("accounting-law", "会计法"),
        ("company-law", "公司法"),
        ("securities-law", "证券法"),
        ("raw-laws", "法律原文"),
    ]},
    {"key": "ethics", "label": "职业道德与独立性", "icon": "🧭", "topics": [
        ("code", "职业道德守则"),
        ("independence", "独立性要求"),
        ("history", "行业史与综述"),
        ("raw-ethics", "原文资料"),
    ]},
    {"key": "policies", "label": "监管政策", "icon": "📋", "topics": [
        ("supervision", "财会监督与审计秩序"),
        ("registration", "注册与考试"),
        ("firm", "事务所监管"),
        ("integrity", "诚信建设"),
        ("trackers", "政策工具页"),
        ("raw-policies", "原文资料"),
    ]},
    {"key": "practice", "label": "实务专题", "icon": "🛠️", "topics": [
        ("first-section", "重点实务专题"),
        ("topic-index", "专题索引与地图"),
        ("audit-practice", "审计实务方法"),
        ("question-bank", "练习题库材料"),
    ]},
    {"key": "cases", "label": "案例库", "icon": "📂", "topics": [
        ("index", "案例索引"),
        ("revenue-recognition", "收入确认"),
        ("share-based-payment", "股份支付"),
        ("lease", "租赁"),
        ("financial-instruments", "金融工具"),
        ("business-combination", "企业合并"),
        ("debt-restructuring", "债务重组"),
        ("accounting-judgment", "综合会计判断"),
        ("intangible-assets", "无形资产"),
        ("case-other", "其他案例"),
        ("raw-cases", "案例原始材料"),
    ]},
    {"key": "sources", "label": "知识来源", "icon": "🗃️", "topics": [
        ("batches", "来源批次归档"),
        ("dashboards", "状态面板"),
        ("raw-indexes", "索引与来源文件"),
    ]},
    {"key": "tools", "label": "工具与自动化", "icon": "🤖", "topics": [
        ("ai-coding", "AI 编程讲义"),
        ("helpers", "知识库助手"),
        ("kb-ops", "知识库运维"),
        ("raw-lectures", "讲义原文"),
    ]},
    {"key": "qa", "label": "问答沉淀", "icon": "💬", "topics": [
        ("questions", "问答页"),
    ]},
    {"key": "meta", "label": "知识库导航", "icon": "🏠", "topics": [
        ("root", "导航页"),
    ]},
]

DOMAIN_LABELS = {d["key"]: d["label"] for d in DOMAINS}
TOPIC_LABELS = {(d["key"], key): label for d in DOMAINS for key, label in d["topics"]}

CASE_TYPE_LABELS = {
    "revenue-recognition": "收入确认",
}

# ---------------------------------------------------------------------------
# wiki 页分类规则（输入：相对 KB 根路径，如 wiki/concepts/accounting-standards/cas-14.md）
# ---------------------------------------------------------------------------

_ETHICS_ROOT = {"ethics-code": ("ethics", "code"),
                "independence-standard-1": ("ethics", "independence"),
                "industry-history": ("ethics", "history"),
                "history-ethics-independence": ("ethics", "history")}

_POLICY_TOPIC = {
    "policy-caihui-supervision": "supervision",
    "policy-audit-order": "supervision",
    "policy-cpa-registration": "registration",
    "policy-cpa-exam": "registration",
    "policy-firm-inspection": "firm",
    "policy-firm-license-supervision": "firm",
    "policy-integrity": "integrity",
}

_PRACTICE_ROOT = {"audit-process", "audit-practice-operations", "practice-skills-cases",
                  "comprehensive-competency", "securities-issuance-rd-staff-investment"}

_CASE_INDEX = {"case-analysis", "case-topic-index", "case-index-suggestion-report"}

_LAW_OVERVIEW = {"regulations-and-standards", "core-laws-official-verification"}

_LAW_PAGE = {"law-accounting": "accounting-law", "law-company": "company-law",
             "law-cpa": "cpa-law", "law-securities": "securities-law"}


def classify_wiki(rel: str, fm: dict[str, str]) -> tuple[str, str]:
    """返回 (domain, topic)。rel 形如 wiki/concepts/xxx.md（posix 分隔）。"""
    p = rel[len("wiki/"):] if rel.startswith("wiki/") else rel
    stem = Path(p).stem

    if "/" not in p:  # 根级 index/overview/log
        return "meta", "root"

    if p.startswith("cases/"):
        ct = fm.get("case_type", "")
        if stem.startswith("index") or stem in _CASE_INDEX:
            return "cases", "index"
        return "cases", ct if ("cases", ct) in TOPIC_LABELS else "case-other"

    if p.startswith("sources/"):
        return "sources", "batches"

    if p.startswith("questions/"):
        return "qa", "questions"

    if p.startswith("concepts/accounting-judgments/"):
        return "accounting-standards", "accounting-judgments"

    if p.startswith("concepts/accounting-standards/"):
        sub = p[len("concepts/accounting-standards/"):]
        if sub.startswith("interpretations/"):
            return "accounting-standards", "interpretations"
        if sub.startswith("other-rules/"):
            return "accounting-standards", "other-rules"
        if stem == "basic":
            return "accounting-standards", "basic"
        if re.match(r"^cas-\d+", stem):
            return "accounting-standards", "cas"
        return "accounting-standards", "overview"

    if p.startswith("concepts/audit-standards/"):
        if stem == "assurance-basic":
            return "audit-standards", "assurance"
        if stem.startswith("csa-"):
            return "audit-standards", "csa"
        if stem.startswith("crs-svc-"):
            return "audit-standards", "related-services"
        if stem.startswith("crs-"):
            return "audit-standards", "review"
        if stem.startswith("coa-"):
            return "audit-standards", "other-assurance"
        return "audit-standards", "overview"

    if p.startswith("concepts/laws/"):
        sub = p[len("concepts/laws/"):]
        for law in ("cpa-law", "accounting-law", "company-law", "securities-law"):
            if sub.startswith(law + "/") or stem.startswith(law):
                return "laws", law
        return "laws", "overview"

    if p.startswith("concepts/first-section-topics/"):
        return "practice", "first-section"

    if p.startswith("concepts/"):
        if stem in _LAW_PAGE:
            return "laws", _LAW_PAGE[stem]
        if stem in _LAW_OVERVIEW:
            return "laws", "overview"
        if stem in _ETHICS_ROOT:
            return _ETHICS_ROOT[stem]
        if stem in _POLICY_TOPIC:
            return "policies", _POLICY_TOPIC[stem]
        if stem.startswith("policy-"):
            return "policies", "trackers"
        if stem in _PRACTICE_ROOT:
            return "practice", "audit-practice"
        if stem.startswith("first-section-"):
            return "practice", "topic-index"
        if stem in _CASE_INDEX:
            return "cases", "index"
        if stem == "accounting-standards-system":
            return "accounting-standards", "overview"
        if stem == "audit-standards-system":
            return "audit-standards", "overview"
        if stem.startswith("ai-coding"):
            return "tools", "ai-coding"
        if stem.startswith("cpa-zh-") or stem == "intelligent-tools":
            return "tools", "helpers"
        if stem.startswith("kb-"):
            return "tools", "kb-ops"
        if stem == "source-status-dashboard":
            return "sources", "dashboards"
        # 兜底：实务专题
        return "practice", "audit-practice"

    return "practice", "audit-practice"


# ---------------------------------------------------------------------------
# raw 文件分类规则（输入：相对 KB 根路径，如 raw/standards/accounting/standards-pages/x.html）
# ---------------------------------------------------------------------------

def classify_raw(rel: str) -> tuple[str, str]:
    p = rel[len("raw/"):] if rel.startswith("raw/") else rel
    if p.startswith("standards/accounting/"):
        sub = p[len("standards/accounting/"):]
        if sub.startswith("standards-pages"):
            return "accounting-standards", "raw-standards"
        if sub.startswith("application-cases"):
            return "accounting-standards", "raw-app-cases"
        if sub.startswith("implementation-qa"):
            return "accounting-standards", "raw-impl-qa"
        if sub.startswith("interpretations-pages"):
            return "accounting-standards", "raw-interp"
        return "accounting-standards", "raw-other"
    if p.startswith("standards/audit"):
        return "audit-standards", "raw-audit"
    if p.startswith("laws/"):
        return "laws", "raw-laws"
    if p.startswith("ethics/"):
        return "ethics", "raw-ethics"
    if p.startswith("policies/"):
        return "policies", "raw-policies"
    if p.startswith("lectures/"):
        return "tools", "raw-lectures"
    if p.startswith("cases/"):
        return "cases", "raw-cases"
    if p.startswith(("indexes/", "outlines/", "sources/")):
        if p.startswith("outlines/practice-question-bank"):
            return "practice", "question-bank"
        return "sources", "raw-indexes"
    return "sources", "raw-indexes"


# ---------------------------------------------------------------------------
# 标题清洗 / 短标题
# ---------------------------------------------------------------------------

_MOF_SUFFIX = re.compile(r"[-—–\s]*(中华人民共和国财政部|财政部会计司|中国财政部)\s*$")
_LEAD_NUM = re.compile(r"^\d{2,4}[-_.、\s]+")


def clean_raw_title(name: str) -> str:
    """清洗 raw 文件名为可读标题。"""
    title = Path(name).stem
    title = _LEAD_NUM.sub("", title)
    title = _MOF_SUFFIX.sub("", title)
    title = title.replace("-", " ").strip()
    if len(title) > 60:
        title = title[:57] + "…"
    return title or Path(name).stem


_ARTICLE_RE = re.compile(r"(第[一二三四五六七八九十百千零〇\d]+条(?:之[一二三四五六七八九十]+)?)\s*$")
_NO_DASH_RE = re.compile(r"第\d+号[——\-—]*(.+)$")


def short_title(title: str, rel: str) -> str:
    """为超长标题生成展示短名；无需缩短时返回空串。"""
    m = _ARTICLE_RE.search(title)
    if m and ("law" in rel):
        return m.group(1)
    if len(title) > 28:
        m2 = _NO_DASH_RE.search(title)
        if m2:
            num = re.search(r"第\d+号", title)
            return (num.group(0) + " " + m2.group(1))[:28] if num else title[:28]
        return title[:26] + "…"
    return ""


# ---------------------------------------------------------------------------
# frontmatter 解析与写回
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str], int, int]:
    """返回 (fm字典, fm起始行后偏移, fm结束偏移('\n---'处))；无 fm 返回 ({}, -1, -1)。"""
    if not text.startswith("---"):
        return {}, -1, -1
    end = text.find("\n---", 3)
    if end == -1:
        return {}, -1, -1
    fm: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("\"'")
    return fm, 3, end


def upsert_fm_fields(text: str, fields: dict[str, str]) -> str:
    """把 fields 写入 frontmatter：已有键替换，无则插入在关闭 --- 之前。"""
    fm, start, end = parse_frontmatter(text)
    if start == -1:
        return text
    block = text[start:end]
    lines = block.split("\n")
    remaining = dict(fields)
    for i, line in enumerate(lines):
        key = line.partition(":")[0].strip()
        if key in remaining:
            lines[i] = f"{key}: {remaining.pop(key)}"
    for key, value in remaining.items():
        lines.append(f"{key}: {value}")
    return text[:start] + "\n".join(lines) + text[end:]


# ---------------------------------------------------------------------------
# 扫描与构建
# ---------------------------------------------------------------------------

def load_overrides() -> dict[str, dict[str, str]]:
    if OVERRIDES_PATH.exists():
        try:
            return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
        except Exception:
            print(f"[warn] overrides 解析失败: {OVERRIDES_PATH}", file=sys.stderr)
    return {}


def iter_wiki_files() -> list[Path]:
    files = []
    for md in sorted((KB_ROOT / "wiki").rglob("*.md")):
        if "_trash" in md.parts or "_maintenance" in md.parts:
            continue
        files.append(md)
    return files


RAW_SKIP_NAMES = {"metadata.json", "source-url.txt", "manifest.json"}
RAW_BROWSE_SUFFIXES = {".md", ".txt", ".html", ".htm", ".pdf", ".docx", ".csv", ".json", ".xlsx"}
RETIRED_CONCEPT_TYPES = {
    "accounting-standard-calibration-bucket",
    "accounting-standard-calibration-index",
}


def iter_raw_files() -> list[Path]:
    files = []
    for f in sorted((KB_ROOT / "raw").rglob("*")):
        if not f.is_file() or f.name in RAW_SKIP_NAMES:
            continue
        if f.suffix.lower() not in RAW_BROWSE_SUFFIXES:
            continue
        files.append(f)
    return files


def natural_key(s: str) -> list:
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def scan(apply: bool = False) -> dict[str, Any]:
    """扫描全库并分类。apply=True 时写回 wiki frontmatter。"""
    overrides = load_overrides()
    stats = {"wiki_total": 0, "wiki_rule": 0, "wiki_fallback": 0, "wiki_override": 0,
             "wiki_written": 0, "raw_total": 0}
    entries: list[dict[str, Any]] = []

    for md in iter_wiki_files():
        rel = md.relative_to(KB_ROOT).as_posix()
        text = md.read_text(encoding="utf-8")
        fm, _, _ = parse_frontmatter(text)
        if fm.get("concept_type", "") in RETIRED_CONCEPT_TYPES:
            continue
        stats["wiki_total"] += 1
        ov = overrides.get(rel, {})
        if ov.get("domain"):
            domain, topic = ov["domain"], ov.get("topic", "")
            stats["wiki_override"] += 1
        else:
            domain, topic = classify_wiki(rel, fm)
            if (domain, topic) == ("practice", "audit-practice") and \
                    Path(rel).stem not in _PRACTICE_ROOT:
                stats["wiki_fallback"] += 1
            else:
                stats["wiki_rule"] += 1
        title = fm.get("title") or md.stem
        st = ov.get("short_title") or short_title(title, rel)
        if apply and (fm.get("domain") != domain or fm.get("topic") != topic):
            new_text = upsert_fm_fields(text, {"domain": domain, "topic": topic})
            if new_text != text:
                md.write_text(new_text, encoding="utf-8")
                stats["wiki_written"] += 1
        entries.append({
            "kind": "wiki", "path": rel, "title": title, "short": st,
            "domain": domain, "topic": topic,
            "type": fm.get("type", ""), "updated": fm.get("updated", ""),
            "page_role": fm.get("page_role", ""), "maturity": fm.get("maturity", ""),
            "answer_ready": str(fm.get("answer_ready", "")).lower() == "true",
        })

    for f in iter_raw_files():
        rel = f.relative_to(KB_ROOT).as_posix()
        stats["raw_total"] += 1
        domain, topic = classify_raw(rel)
        entries.append({
            "kind": "raw", "path": rel, "title": clean_raw_title(f.name), "short": "",
            "domain": domain, "topic": topic, "type": f.suffix.lower().lstrip("."),
            "updated": "",
        })

    return {"stats": stats, "entries": entries}


def build_categories(result: dict[str, Any]) -> dict[str, Any]:
    """把扫描结果聚合为两级语义树。"""
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for e in result["entries"]:
        grouped.setdefault((e["domain"], e["topic"]), []).append(e)

    domains_out = []
    for d in DOMAINS:
        topics_out = []
        for tkey, tlabel in d["topics"]:
            pages = grouped.pop((d["key"], tkey), [])
            if not pages:
                continue
            pages.sort(key=lambda e: natural_key(e["path"]))
            topics_out.append({
                "key": tkey, "label": tlabel, "count": len(pages),
                "pages": [{"path": p["path"], "title": p["title"], "short": p["short"],
                           "kind": p["kind"], "type": p["type"], "updated": p["updated"],
                           "page_role": p.get("page_role", ""), "maturity": p.get("maturity", ""),
                           "answer_ready": p.get("answer_ready", False)}
                          for p in pages],
            })
        # 未在预定义 topic 列表中的兜底组
        stray = [(k, v) for k, v in grouped.items() if k[0] == d["key"]]
        for (dk, tk), pages in sorted(stray):
            grouped.pop((dk, tk))
            pages.sort(key=lambda e: natural_key(e["path"]))
            topics_out.append({
                "key": tk, "label": tk or "未分组", "count": len(pages),
                "pages": [{"path": p["path"], "title": p["title"], "short": p["short"],
                           "kind": p["kind"], "type": p["type"], "updated": p["updated"],
                           "page_role": p.get("page_role", ""), "maturity": p.get("maturity", ""),
                           "answer_ready": p.get("answer_ready", False)}
                          for p in pages],
            })
        if topics_out:
            domains_out.append({
                "key": d["key"], "label": d["label"], "icon": d["icon"],
                "count": sum(t["count"] for t in topics_out),
                "topics": topics_out,
            })

    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "domains": domains_out,
    }


def print_report(result: dict[str, Any]) -> None:
    s = result["stats"]
    print("=== CPA-ZH 分类覆盖率报告 ===")
    print(f"wiki 页总数        : {s['wiki_total']}")
    print(f"  路径规则命中     : {s['wiki_rule']}")
    print(f"  兜底(实务专题)   : {s['wiki_fallback']}")
    print(f"  人工 overrides   : {s['wiki_override']}")
    if s.get("wiki_written"):
        print(f"  frontmatter 写回 : {s['wiki_written']}")
    print(f"raw 文件纳入       : {s['raw_total']}")
    counts: dict[str, int] = {}
    for e in result["entries"]:
        counts[e["domain"]] = counts.get(e["domain"], 0) + 1
    print("--- 按 domain 分布 ---")
    for d in DOMAINS:
        if d["key"] in counts:
            print(f"  {d['label']:<10} {counts[d['key']]}")


def main() -> int:
    global KB_ROOT
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="CPA-ZH 语义分类工具")
    parser.add_argument("--root", default=str(KB_ROOT), help="Knowledge base root.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("report", help="只打印覆盖率报告")
    sub.add_parser("apply", help="写回 wiki frontmatter (domain/topic)")
    sub.add_parser("build", help="生成 search/navigation-tree.json（含 frontmatter 写回）")
    sub.add_parser("categories", help="生成 search/navigation-tree.json（不写回 frontmatter）")
    args = parser.parse_args()
    KB_ROOT = Path(args.root).resolve()

    if args.command == "report":
        print_report(scan(apply=False))
        return 0
    if args.command == "apply":
        result = scan(apply=True)
        print_report(result)
        return 0
    if args.command == "build":
        result = scan(apply=True)
        categories = build_categories(result)
        out = KB_ROOT / "search" / "navigation-tree.json"
        out.write_text(json.dumps(categories, ensure_ascii=False), encoding="utf-8")
        print_report(result)
        total = sum(d["count"] for d in categories["domains"])
        print(f"navigation-tree.json 写入: {out} (domains={len(categories['domains'])}, entries={total})")
        return 0
    if args.command == "categories":
        result = scan(apply=False)
        categories = build_categories(result)
        out = KB_ROOT / "search" / "navigation-tree.json"
        out.write_text(json.dumps(categories, ensure_ascii=False), encoding="utf-8")
        print_report(result)
        total = sum(d["count"] for d in categories["domains"])
        print(f"navigation-tree.json 写入: {out} (domains={len(categories['domains'])}, entries={total})")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
