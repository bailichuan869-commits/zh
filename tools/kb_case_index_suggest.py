from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPORT_PATH = Path("wiki/concepts/case-index-suggestion-report.md")


TOPIC_RULES = [
    ("收入确认", ["revenue-recognition", "收入确认", "履约义务", "售后回购"]),
    ("政府补助", ["government-grant", "政府补助", "免费使用", "无偿", "补助"]),
    ("长期股权投资", ["long-term-equity-investments", "长期股权投资", "内部重组", "同一控制"]),
    ("固定资产与所得税", ["tax-accounting-difference", "暂估转固", "递延所得税", "税会差异", "发票"]),
]

RISK_RULES = [
    ("收入提前确认", ["revenue-recognition", "收入确认", "履约义务", "售后回购"]),
    ("内部重组确认收益", ["long-term-equity-investments", "内部重组", "投资收益", "商业实质"]),
    ("政府支持收益化", ["government-grant", "政府补助", "免费使用", "其他收益"]),
    ("税务申报与递延所得税", ["tax-accounting-difference", "递延所得税", "汇算清缴", "纳税调增"]),
]

WORKPAPER_RULES = [
    ("控制权转移备忘录", ["revenue-recognition", "收入确认", "履约义务", "售后回购"]),
    ("商业实质判断备忘录", ["long-term-equity-investments", "内部重组", "商业实质"]),
    ("政府补助判断备忘录", ["government-grant", "政府补助", "免费使用"]),
    ("税会差异测算表", ["tax-accounting-difference", "暂估转固", "递延所得税", "税会差异"]),
]


@dataclass
class CasePage:
    path: Path
    rel_path: str
    page_link: str
    title: str
    case_type: str
    topic: str
    tags: list[str]
    related: list[str]
    body: str
    conclusion: str


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_list_value(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("\"'") for part in inner.split(",") if part.strip()]
    return [value.strip().strip("\"'")] if value else []


def parse_frontmatter(text: str) -> tuple[dict[str, str | list[str]], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    frontmatter = text[4:end]
    body = text[end + 4 :].lstrip()
    metadata: dict[str, str | list[str]] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {"tags", "sources"}:
            metadata[key] = parse_list_value(value)
        elif key == "related":
            metadata[key] = re.findall(r"\[\[([^\]]+)\]\]", value)
        else:
            metadata[key] = value.strip().strip("\"'")
    return metadata, body


def first_paragraph_after_heading(body: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if re.match(pattern, line.strip()):
            parts: list[str] = []
            for next_line in lines[index + 1 :]:
                stripped = next_line.strip()
                if stripped.startswith("## "):
                    break
                if not stripped or stripped.startswith("|") or stripped.startswith("---"):
                    continue
                parts.append(stripped)
                if len(" ".join(parts)) >= 120:
                    break
            return " ".join(parts).strip()
    return ""


def load_cases(root: Path) -> list[CasePage]:
    cases_root = root / "wiki" / "cases"
    pages: list[CasePage] = []
    for path in sorted(cases_root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        rel_path = rel(root, path)
        page_slug = rel_path.removeprefix("wiki/").removesuffix(".md").replace("\\", "/")
        title = str(metadata.get("title") or path.stem)
        topic = str(metadata.get("topic") or "")
        tags = [str(tag) for tag in metadata.get("tags", [])] if isinstance(metadata.get("tags"), list) else []
        related = (
            [str(item) for item in metadata.get("related", [])]
            if isinstance(metadata.get("related"), list)
            else []
        )
        conclusion = first_paragraph_after_heading(body, "一句话结论") or title
        pages.append(
            CasePage(
                path=path,
                rel_path=rel_path,
                page_link=f"[[{page_slug}]]",
                title=title,
                case_type=str(metadata.get("case_type") or ""),
                topic=topic,
                tags=tags,
                related=related,
                body=body,
                conclusion=conclusion,
            )
        )
    return pages


def match_labels(case: CasePage, rules: list[tuple[str, list[str]]]) -> list[str]:
    if rules is TOPIC_RULES and case.topic:
        return [case.topic]
    haystack = " ".join([case.title, case.case_type, case.topic, " ".join(case.tags), " ".join(case.related), case.body]).lower()
    labels: list[str] = []
    for label, keywords in rules:
        if any(keyword.lower() in haystack for keyword in keywords):
            labels.append(label)
    return labels


def standard_links(case: CasePage) -> list[str]:
    links = [
        link
        for link in case.related
        if link.startswith("concepts/accounting-standards/")
        or link.startswith("concepts/audit-standards/")
        or link.startswith("concepts/first-section-topics/")
        or link.startswith("concepts/policy-")
    ]
    return links


def short_text(text: str, limit: int = 90) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_report(root: Path, cases: list[CasePage], index_text: str) -> str:
    lines = [
        "---",
        "title: 案例主题索引自动回挂建议报告",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        "sources: [case-index-suggest]",
        "tags: [case, case-index, automation, maintenance]",
        "related: [[concepts/case-topic-index]], [[concepts/cpa-zh-case-index-helper]], [[concepts/case-analysis]]",
        "---",
        "",
        "# 案例主题索引自动回挂建议报告",
        "",
        "本页由 `tools/kb_case_index_suggest.py --write-report` 生成，用于检查 `wiki/cases/` 案例卡片是否已回挂到主题索引，并给出新增索引行建议。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| 案例卡片 | {len(cases)} |",
        f"| 已在主题索引出现 | {sum(1 for case in cases if case.page_link in index_text)} |",
        f"| 待补入主题索引 | {sum(1 for case in cases if case.page_link not in index_text)} |",
        "",
        "## 按会计主题建议",
        "",
        "| 主题 | 案例 | 建议关键判断 | 当前索引状态 |",
        "|---|---|---|---|",
    ]
    for case in cases:
        topics = match_labels(case, TOPIC_RULES) or ["待人工分类"]
        status = "已出现" if case.page_link in index_text else "建议补入"
        for topic in topics:
            lines.append(f"| {topic} | {case.page_link} | {short_text(case.conclusion)} | {status} |")

    lines.extend(
        [
            "",
            "## 按准则入口建议",
            "",
            "| 准则或专题入口 | 案例 | 复用问题 | 当前索引状态 |",
            "|---|---|---|---|",
        ]
    )
    for case in cases:
        links = standard_links(case) or ["待人工指定"]
        status = "已出现" if case.page_link in index_text else "建议补入"
        for link in links:
            display = f"[[{link}]]" if link != "待人工指定" else link
            lines.append(f"| {display} | {case.page_link} | {short_text(case.title)} | {status} |")

    lines.extend(
        [
            "",
            "## 按审计风险建议",
            "",
            "| 风险类型 | 案例 | 建议审计关注点 | 当前索引状态 |",
            "|---|---|---|---|",
        ]
    )
    for case in cases:
        risks = match_labels(case, RISK_RULES) or ["待人工分类"]
        status = "已出现" if case.page_link in index_text else "建议补入"
        for risk in risks:
            lines.append(f"| {risk} | {case.page_link} | {short_text(first_paragraph_after_heading(case.body, '审计关注点') or case.conclusion)} | {status} |")

    lines.extend(
        [
            "",
            "## 按底稿用途建议",
            "",
            "| 底稿用途 | 案例 | 建议留痕材料 | 当前索引状态 |",
            "|---|---|---|---|",
        ]
    )
    for case in cases:
        uses = match_labels(case, WORKPAPER_RULES) or ["待人工分类"]
        status = "已出现" if case.page_link in index_text else "建议补入"
        for use in uses:
            lines.append(f"| {use} | {case.page_link} | {short_text(first_paragraph_after_heading(case.body, '底稿留痕建议') or case.conclusion)} | {status} |")

    lines.extend(
        [
            "",
            "## 使用方式",
            "",
            "1. 若状态为“建议补入”，人工复核后复制对应行到 [[concepts/case-topic-index]]。",
            "2. 若主题、风险或底稿用途不准确，优先修订案例卡片的 `tags`、`related` 和正文关键词。",
            "3. 新增案例后先运行 dry-run，再写入本报告。",
            "",
            "```powershell",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py case-index",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py case-index --write-report",
            "```",
            "",
            f"_生成路径：`{rel(root, root / REPORT_PATH)}`_",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Suggest case-topic-index back-links for CPA-ZH case cards.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--write-report", action="store_true", help="Write the suggestion report into the wiki.")
    parser.add_argument("--output", default=str(REPORT_PATH), help="Output path under the knowledge base root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    index_path = root / "wiki" / "concepts" / "case-topic-index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    cases = load_cases(root)
    report = render_report(root, cases, index_text)

    print(f"cases={len(cases)}")
    print(f"indexed={sum(1 for case in cases if case.page_link in index_text)}")
    print(f"missing={sum(1 for case in cases if case.page_link not in index_text)}")

    if args.write_report:
        output = root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8", newline="\n")
        print(f"written={output}")
    else:
        print()
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
