"""Build the CPA-ZH content maturity dashboard and optional metadata updates."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from kb_common import KB_ROOT, iter_markdown_pages, update_frontmatter


REPORT_PATH = KB_ROOT / "wiki" / "concepts" / "kb-content-maturity-dashboard.md"
JSON_PATH = KB_ROOT.parents[1] / "workspace" / "outputs" / "kb_maturity.json"


def classify_domain(rel_path: str, metadata: dict) -> str:
    rel = rel_path.lower()
    if "accounting-judgments" in rel or "accounting-standards" in rel:
        return "会计准则与判断"
    if "/cases/" in "/" + rel:
        return "案例库"
    if "audit-standards" in rel or "audit-practice" in rel:
        return "审计准则与实务"
    if "ethic" in rel or "independence" in rel:
        return "职业道德与独立性"
    if "law" in rel or str(metadata.get("page_role")) == "reference":
        return "法规与原文"
    return "其他知识"


def collect() -> tuple[list[dict], dict]:
    pages: list[dict] = []
    roles: Counter[str] = Counter()
    maturity: Counter[str] = Counter()
    domains: dict[str, Counter[str]] = defaultdict(Counter)
    answer_ready = 0
    for path, rel, metadata, body in iter_markdown_pages():
        domain = classify_domain(rel, metadata)
        item = {
            "path": rel,
            "title": metadata.get("title") or path.stem,
            "domain": domain,
            "page_role": metadata["page_role"],
            "role_label": metadata["role_label"],
            "maturity": metadata["maturity"],
            "answer_ready": bool(metadata["answer_ready"]),
            "source_complete": bool(metadata.get("raw_path") or metadata.get("sources") or metadata["page_role"] == "index"),
            "characters": len(body.strip()),
        }
        pages.append(item)
        roles[item["page_role"]] += 1
        maturity[item["maturity"]] += 1
        domains[domain][item["maturity"]] += 1
        domains[domain][item["page_role"]] += 1
        if item["answer_ready"]:
            answer_ready += 1
    summary = {
        "generated_at": date.today().isoformat(),
        "total": len(pages),
        "answer_ready": answer_ready,
        "roles": dict(roles),
        "maturity": dict(maturity),
        "domains": {key: dict(value) for key, value in sorted(domains.items())},
    }
    return pages, summary


def render_markdown(pages: list[dict], summary: dict) -> str:
    golden_topics = [p for p in pages if "/accounting-judgments/" in p["path"] and not p["path"].endswith("/index.md")]
    golden_cases = [p for p in pages if p["path"].startswith("wiki/cases/golden-")]
    gaps = [p for p in pages if p["maturity"] == "skeleton" and p["page_role"] not in {"reference", "index"}]
    lines = [
        "---",
        "title: CPA-ZH 内容成熟度仪表盘",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {summary['generated_at']}",
        f"updated: {summary['generated_at']}",
        "page_role: index",
        "maturity: reviewed",
        "answer_ready: false",
        "sources: [kb-maturity]",
        "tags: [maintenance, maturity, answer-readiness, quality-control]",
        "related: [[concepts/accounting-judgments/index]], [[cases/golden-cases-index]]",
        "---",
        "",
        "# CPA-ZH 内容成熟度仪表盘",
        "",
        "本页由 `kb_maturity.py dashboard` 生成。法规合并全文索引页即使较短也按原文索引处理，不计入知识骨架缺口；条文通过稳定锚点检索，不按一条一个知识页拆分。`answer_ready` 只表示允许进入问答主检索集；`agent-reviewed` 表示 Agent 已按结构、来源链和结论边界完成复核并留下记录，不等于人工批准，也不等于官方效力已由 Agent 自动核验。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| 有效 Wiki 页面 | {summary['total']} |",
        f"| 可进入问答主检索 | {summary['answer_ready']} |",
        f"| 黄金专题 | {len(golden_topics)} |",
        f"| 黄金案例 | {len(golden_cases)} |",
        f"| 待补知识骨架 | {len(gaps)} |",
        "",
        "## 页面角色",
        "",
        "| 角色 | 数量 | 用途 |",
        "|---|---:|---|",
        f"| 原文 reference | {summary['roles'].get('reference', 0)} | 权威原文或原子资料 |",
        f"| 目录 index | {summary['roles'].get('index', 0)} | 导航，不单独产出结论 |",
        f"| 知识专题 knowledge | {summary['roles'].get('knowledge', 0)} | 结构化判断 |",
        f"| 案例 case | {summary['roles'].get('case', 0)} | 事实到结论的应用 |",
        "",
        "## 主题成熟度",
        "",
        "| 主题 | 骨架 | 草稿 | 已复核 | 原文 | 目录 | 专题 | 案例 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for domain, counts in summary["domains"].items():
        lines.append(
            f"| {domain} | {counts.get('skeleton', 0)} | {counts.get('draft', 0)} | "
            f"{counts.get('reviewed', 0)} | {counts.get('reference', 0)} | {counts.get('index', 0)} | "
            f"{counts.get('knowledge', 0)} | {counts.get('case', 0)} |"
        )
    lines.extend([
        "",
        "## 黄金内容复核队列",
        "",
        "| 页面 | 类型 | 原文 | 成熟度 | 问答就绪 |",
        "|---|---|---|---|---|",
    ])
    for item in sorted(golden_topics + golden_cases, key=lambda p: p["path"]):
        link = item["path"][len("wiki/"):-3]
        lines.append(
            f"| [[{link}|{item['title']}]] | {item['role_label']} | "
            f"{'完整' if item['source_complete'] else '缺失'} | {item['maturity']} | "
            f"{'是' if item['answer_ready'] else '否'} |"
        )
    lines.extend([
        "",
        "## 下一步缺口",
        "",
        "1. 新增或变更的黄金专题和案例先由 Agent 按来源、事实、准则版本、分支、引用和不确定性边界执行复核；通过后记录 `review_status: agent-reviewed`。",
        "2. Agent 复核不替代官方来源效力核验；来源为本地研讨材料的页面必须保持 `source_scope: local-only`，不得冒充官方依据。",
        "3. 未通过复核的草稿仍可浏览和普通搜索，但不会进入 AI 主检索集；`user-approved` 仅是另一路显式人工确认状态，不是 Agent 复核的前置条件。",
        "4. 目录页只负责导航；不得仅依据目录页生成专业结论。",
        "",
    ])
    return "\n".join(lines)


def write_dashboard() -> None:
    pages, summary = collect()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown(pages, summary), encoding="utf-8")
    JSON_PATH.write_text(json.dumps({"summary": summary, "pages": pages}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pages={summary['total']}")
    print(f"answer_ready={summary['answer_ready']}")
    print(f"report={REPORT_PATH}")


def apply_metadata() -> None:
    changed = 0
    for path, rel, metadata, _body in iter_markdown_pages():
        text = path.read_text(encoding="utf-8")
        updated = update_frontmatter(text, {
            "page_role": metadata["page_role"],
            "maturity": metadata["maturity"],
            "answer_ready": bool(metadata["answer_ready"]),
        })
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"changed={changed}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CPA-ZH content maturity tooling")
    parser.add_argument("command", choices=("dashboard", "apply"))
    args = parser.parse_args()
    if args.command == "dashboard":
        write_dashboard()
    else:
        apply_metadata()


if __name__ == "__main__":
    main()
