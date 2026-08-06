"""Scan CPA-ZH wiki pages for repeatable content-completeness gaps."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from kb_common import KB_ROOT, iter_markdown_pages, parse_frontmatter


DEFAULT_REPORT = "wiki/concepts/kb-content-completeness-report.md"
DEFAULT_JSON = "workspace/outputs/kb_completeness.json"
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
PENDING_RE = re.compile(
    r"待补充|待完善|待从[^\n。；]*继续回挂|(?:^|\b)(?:TODO|TBD)(?:\b|$)|占位|"
    r"尚未(?:建立|补充)|后续(?:需|应|再|可)?(?:继续|再)?(?:补充|完善|建立|核验)|"
    r"(?:仍|尚)?(?:需|应|需要)补充|补官方链接"
)
VERIFICATION_RE = re.compile(r"待核验|待官方(?:核对|重新公布)|待确认|建议后续抽样校验|无法直连下载")


def resolve_wiki_target(target: str, pages: set[str], names: dict[str, list[str]]) -> str | None:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target or target.startswith(("raw/", "/")):
        return None
    if target in pages:
        return target
    if "/" in target:
        matches = [slug for slug in pages if slug.endswith("/" + target) or slug.endswith(target)]
        return matches[0] if matches else None
    matches = names.get(target, [])
    return matches[0] if matches else None


def line_matches(body: str, pattern: re.Pattern[str]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for line_no, line in enumerate(body.splitlines(), start=1):
        if pattern.search(line):
            snippet = re.sub(r"\s+", " ", line.strip())
            matches.append({"line": line_no, "text": snippet[:180]})
    return matches


def intentional_reason(path: str, metadata: dict[str, Any]) -> str:
    role = str(metadata.get("page_role") or "")
    if role == "reference":
        return "原文或来源页，短正文不代表知识缺口"
    if role == "index":
        return "目录或全文索引页，职责是导航和稳定锚点"
    if path.startswith("wiki/concepts/laws/") and path.endswith("/index.md"):
        return "法律合并全文索引页，条文通过锚点定位，不拆成一条一个页面"
    return ""


def source_complete(metadata: dict[str, Any]) -> bool:
    return any(
        metadata.get(key)
        for key in ("sources", "raw_path", "source_url", "official_url", "url")
    )


def collect(root: Path, report_path: str = DEFAULT_REPORT) -> dict[str, Any]:
    normalized_report_path = report_path.replace("\\", "/")
    records = [
        record for record in iter_markdown_pages(root) if record[1] != normalized_report_path
    ]
    page_slugs = {rel[len("wiki/") : -len(".md")] for _path, rel, _meta, _body in records}
    page_names: dict[str, list[str]] = {}
    for slug in sorted(page_slugs):
        page_names.setdefault(slug.rsplit("/", 1)[-1], []).append(slug)

    pages: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for path, rel, metadata, body in records:
        raw_metadata, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        role = str(metadata.get("page_role") or "knowledge")
        reason = intentional_reason(rel, metadata)
        issues: list[dict[str, Any]] = []
        pending = line_matches(body, PENDING_RE)
        verification = line_matches(body, VERIFICATION_RE)
        compact_length = len(re.sub(r"\s+", "", body))
        heading_count = len(re.findall(r"^#{2,6}\s+", body, flags=re.MULTILINE))

        if pending and not reason:
            issues.append({"kind": "pending-content", "matches": pending})
        if verification and not reason:
            issues.append({"kind": "pending-verification", "matches": verification})

        is_short = role in {"knowledge", "case"} and (
            str(raw_metadata.get("maturity") or "") == "skeleton"
            or compact_length < 500
            or heading_count < 2
        )
        if is_short and not reason:
            issues.append(
                {
                    "kind": "skeleton",
                    "matches": [
                        {"line": 0, "text": f"正文字符数={compact_length}，二级及以下标题数={heading_count}"}
                    ],
                }
            )

        if role in {"knowledge", "case"} and not source_complete(metadata):
            issues.append(
                {
                    "kind": "missing-source",
                    "matches": [{"line": 0, "text": "frontmatter 未提供 sources、raw_path 或 source_url"}],
                }
            )

        broken: list[dict[str, Any]] = []
        for match in LINK_RE.finditer(body):
            raw_target = match.group(1)
            target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
            if not target or target.startswith(("raw/", "/")):
                continue
            if any(part in {"_drafts", "_maintenance", "_trash", "__pycache__"} for part in target.split("/")):
                continue
            if resolve_wiki_target(raw_target, page_slugs, page_names) is None:
                line_no = body.count("\n", 0, match.start()) + 1
                broken.append({"line": line_no, "text": raw_target})
        if broken:
            issues.append({"kind": "broken-wiki-link", "matches": broken})

        if reason:
            counts[f"intentional-{role}"] += 1
        for issue in issues:
            counts[issue["kind"]] += 1

        pages.append(
            {
                "path": rel,
                "title": str(metadata.get("title") or path.stem),
                "page_role": role,
                "maturity": str(metadata.get("maturity") or ""),
                "characters": compact_length,
                "intentional": bool(reason),
                "intentional_reason": reason,
                "issues": issues,
            }
        )

    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "pages": len(pages),
            "flagged_pages": sum(bool(page["issues"]) for page in pages),
            "pending_content": counts["pending-content"],
            "pending_verification": counts["pending-verification"],
            "skeleton": counts["skeleton"],
            "missing_source": counts["missing-source"],
            "broken_wiki_link": counts["broken-wiki-link"],
            "intentional_reference": counts["intentional-reference"],
            "intentional_index": counts["intentional-index"],
        },
        "pages": pages,
    }


def issue_rows(data: dict[str, Any], kind: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for page in data["pages"]:
        for issue in page["issues"]:
            if issue["kind"] != kind:
                continue
            detail = "；".join(
                f"第{item['line']}行 {item['text']}" if item["line"] else item["text"]
                for item in issue["matches"]
            )
            rows.append((page["path"], page["title"], detail))
    return rows


def render_report(data: dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "---",
        "title: CPA-ZH 知识页完整性报告",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {data['generated_at']}",
        f"updated: {data['generated_at']}",
        "page_role: index",
        "maturity: reviewed",
        "answer_ready: false",
        "sources: [kb-completeness]",
        "tags: [maintenance, completeness, quality-control, cpa]",
        "related: [[concepts/kb-content-maturity-dashboard]], [[concepts/kb-section-upgrade-dashboard]], [[concepts/kb-user-guide]]",
        "---",
        "",
        "# CPA-ZH 知识页完整性报告",
        "",
        "本页由 `tools/kb.py completeness --write-report` 生成，用于发现知识页的显式待补内容、骨架页、来源缺口和 Wiki 断链。它只检查结构与维护信号，不替代法规、准则和政策的官方效力核验。",
        "",
        "## 粒度口径",
        "",
        "法规不按“一条一个知识页”拆分。四部核心法律保留原文和四个合并全文索引页，条文通过 `#article-xxx` 锚点检索和引用；原文页、来源页、目录页及全文索引页属于有意保留的 reference/index，不因正文较短被列为骨架缺口。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| Wiki 页面 | {summary['pages']} |",
        f"| 存在待处理问题的页面 | {summary['flagged_pages']} |",
        f"| 显式待补/待完善 | {summary['pending_content']} |",
        f"| 待官方或待确认 | {summary['pending_verification']} |",
        f"| 骨架页 | {summary['skeleton']} |",
        f"| 缺少来源元数据 | {summary['missing_source']} |",
        f"| Wiki 断链页面 | {summary['broken_wiki_link']} |",
        f"| 有意保留原文/来源页 | {summary['intentional_reference']} |",
        f"| 有意保留目录/全文索引页 | {summary['intentional_index']} |",
        "",
    ]

    sections = [
        ("pending-content", "显式待补内容", "先补正文、来源链或实际案例链接；完成后重新运行本报告。"),
        ("skeleton", "骨架页", "补齐定位、规则/流程、实务影响、证据或交叉引用；原文和全文索引页不在此列。"),
        ("missing-source", "来源缺口", "补充 sources、raw_path 或 source_url；专业结论不能只靠无来源的摘要。"),
        ("pending-verification", "效力或来源待核验", "保留为风险提示，不把本地草案、镜像或未核验版本写成现行官方口径。"),
        ("broken-wiki-link", "Wiki 断链", "修复目标路径、文件名或锚点前缀；raw/ 链接由原文层单独维护。"),
    ]
    for kind, heading, guidance in sections:
        rows = issue_rows(data, kind)
        lines.extend([f"## {heading}", "", guidance, "", "| 页面 | 标题 | 检测结果 |", "|---|---|---|"])
        if rows:
            for path, title, detail in rows:
                safe_detail = detail.replace("|", "\\|")
                lines.append(f"| `{path}` | {title} | {safe_detail} |")
        else:
            lines.append("| 无 |  |  |")
        lines.append("")

    lines.extend(["## 有意保留页面", "", "这些页面承担原文追溯、目录导航或合并全文索引职责，不作为知识正文缺口统计：", ""])
    intentional = [page for page in data["pages"] if page["intentional"]]
    for page in intentional:
        lines.append(f"- `{page['path']}`：{page['intentional_reason']}")
    if not intentional:
        lines.append("- 无")
    lines.extend(
        [
            "",
            "## 建议处理顺序",
            "",
            "1. 先修复 broken-wiki-link 和 missing-source，避免内容补好后无法追溯。",
            "2. 再处理 pending-content 和 skeleton，优先法规/准则/政策入口、流程页和高频专题。",
            "3. 对 pending-verification 保留版本边界；只有获得官方依据后才升级为现行有效结论。",
            "4. Agent 可执行结构、来源和引用复核；人工复核底线仍保留，`agent-reviewed` 不等于 `user-approved`。",
            "",
            f"_JSON 明细：`workspace/outputs/kb_completeness.json`；生成日期：{data['generated_at']}。_",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Scan CPA-ZH wiki content completeness.")
    parser.add_argument("--root", default=str(KB_ROOT), help="Knowledge base root.")
    parser.add_argument("--write-report", action="store_true", help="Write the Markdown and JSON reports.")
    parser.add_argument("--output", default=DEFAULT_REPORT, help="Markdown report path under the knowledge base root.")
    parser.add_argument("--json-output", default=DEFAULT_JSON, help="JSON report path relative to the project root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data = collect(root, args.output)
    for key, value in data["summary"].items():
        print(f"{key}={value}")
    if args.write_report:
        report_path = root / args.output
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_report(data), encoding="utf-8", newline="\n")
        json_path = root.parents[1] / args.json_output
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"report={report_path}")
        print(f"json={json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
