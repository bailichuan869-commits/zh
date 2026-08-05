from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import kb_search
except ModuleNotFoundError:
    from tools import kb_search


DEFAULT_TAGS = ["case", "draft", "audit-practice"]
DEFAULT_RELATED = ["[[concepts/case-analysis]]", "[[concepts/case-topic-index]]"]


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or f"case-{date.today().isoformat()}"


def resolve_source(root: Path, source: str) -> Path:
    path = Path(source)
    candidates = [path]
    if not path.is_absolute():
        candidates = [
            root / path,
            Path.cwd() / path,
            root.parent / path,
            root.parents[1] / path if len(root.parents) > 1 else root / path,
        ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


def split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def first_nonempty(*values: str) -> str:
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def compact_excerpt(text: str, limit: int = 1800) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def guess_questions(text: str) -> list[str]:
    candidates: list[str] = []
    for pattern in [r"问题[：:]\s*([^。；\n]+)", r"争议[：:]\s*([^。；\n]+)", r"是否([^。；\n]+)"]:
        for match in re.finditer(pattern, text):
            question = match.group(0).strip()
            if question and question not in candidates:
                candidates.append(question)
            if len(candidates) >= 3:
                return candidates
    return candidates


def render_case_card(args: argparse.Namespace, root: Path, source_path: Path, raw_path: str, text: str) -> str:
    today = date.today().isoformat()
    title = first_nonempty(args.title, source_path.stem)
    source_id = args.source_id or "local-case-batch"
    tags = dedupe(DEFAULT_TAGS + split_csv(args.tags))
    related = dedupe(DEFAULT_RELATED + split_csv(args.related))
    questions = guess_questions(text)
    excerpt = compact_excerpt(text)

    lines = [
        "---",
        f"title: {title}",
        "type: case",
        f"case_type: {args.case_type}",
        f"created: {today}",
        f"updated: {today}",
        f"sources: [{source_id}]",
        f"raw_path: {raw_path}",
        f"tags: [{', '.join(tags)}]",
        f"related: {', '.join(related)}",
        "---",
        "",
        f"# {title}",
        "",
        "> 本页由 `tools/kb.py case-card` 生成，为案例卡片草稿。事实、准则依据、判断过程和结论均需人工复核后再作为正式案例使用。",
        "",
        "## 一句话结论",
        "",
        "待人工复核后填写。不要在未核对事实和准则依据前直接形成最终结论。",
        "",
        "## 案例来源",
        "",
        "| 项目 | 内容 |",
        "|---|---|",
        f"| 来源批次 | [[sources/{source_id}]] |",
        f"| 原始文件 | `{raw_path}` |",
        f"| 生成方式 | `tools/kb.py case-card` |",
        f"| 草稿日期 | {today} |",
        "",
        "## 原文摘要",
        "",
        excerpt or "未能从原文中抽取可用文本。请打开原始文件人工补充。",
        "",
        "## 事实背景",
        "",
        "待人工从原文中提炼：交易主体、期间、金额、合同安排、控制关系、业务目的、已执行程序等。",
        "",
        "## 争议问题",
        "",
    ]
    if questions:
        lines.extend(f"- {question}" for question in questions)
    else:
        lines.append("- 待人工提炼本案例需要回答的会计、审计或监管问题。")

    lines.extend(
        [
            "",
            "## 准则入口",
            "",
            "| 判断事项 | 准则或专题 |",
            "|---|---|",
            "| 待补充 | 根据案例主题回挂第一板块准则页、专题页或政策页 |",
            "",
            "## 判断过程",
            "",
            "### 1. 识别交易或事项的经济实质",
            "",
            "待补充。",
            "",
            "### 2. 匹配适用规则",
            "",
            "待补充。",
            "",
            "### 3. 分析关键判断条件",
            "",
            "待补充。",
            "",
            "## 会计处理或审计处理建议",
            "",
            "待人工复核后填写。若存在多种观点，应区分事实假设、适用条件和结论边界。",
            "",
            "## 审计关注点",
            "",
            "| 关注点 | 审计动作 |",
            "|---|---|",
            "| 事实完整性 | 核对合同、协议、会议纪要、凭证、银行流水、验收资料等原始证据 |",
            "| 准则适用性 | 回到相关准则、解释、监管规则和专题页核验 |",
            "| 管理层判断 | 评价关键假设、估计、商业理由和一致性 |",
            "| 披露和列报 | 检查财务报表列报、附注披露和重大事项说明 |",
            "",
            "## 底稿留痕建议",
            "",
            "1. 保存原始案例文件和本卡片生成版本。",
            "2. 标明事实来源和人工复核人。",
            "3. 将适用准则、政策、案例页回挂到 `related`。",
            "4. 对关键判断形成单独备忘录。",
            "",
            "## 待人工复核清单",
            "",
            "- [ ] 原文事实是否完整摘录。",
            "- [ ] 争议问题是否准确。",
            "- [ ] 准则入口是否已回挂。",
            "- [ ] 判断过程是否区分事实、规则和结论。",
            "- [ ] 审计关注点是否可执行。",
            "- [ ] 是否需要更新 [[concepts/case-topic-index]]。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Generate a CPA-ZH case card draft from a local source file.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--source", required=True, help="Raw/local source file.")
    parser.add_argument("--slug", default="", help="Output case slug. Defaults to source filename slug.")
    parser.add_argument("--title", default="", help="Case title. Defaults to source filename.")
    parser.add_argument("--source-id", default="local-case-batch", help="Source page id without sources/ prefix.")
    parser.add_argument("--case-type", default="draft-case-card", help="case_type frontmatter value.")
    parser.add_argument("--raw-path", default="", help="Raw path to store in frontmatter. Defaults to path relative to root when possible.")
    parser.add_argument("--tags", default="", help="Comma-separated extra tags.")
    parser.add_argument("--related", default="", help="Comma-separated extra wiki links.")
    parser.add_argument("--commit", action="store_true", help="Write the draft into wiki/cases.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing case page.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source_path = resolve_source(root, args.source)
    if not source_path.exists() or not source_path.is_file():
        print(f"source file not found: {source_path}", file=sys.stderr)
        return 2

    slug = args.slug or slugify(source_path.stem)
    output = root / "wiki" / "cases" / f"{slug}.md"
    raw_path = args.raw_path or rel(root, source_path)
    text = kb_search.extract_file_text(source_path)
    card = render_case_card(args, root, source_path, raw_path, text)

    print(f"mode={'commit' if args.commit else 'dry-run'}")
    print(f"source={source_path}")
    print(f"output={output}")
    print(f"text_chars={len(text)}")
    if not args.commit:
        print()
        print("Dry run preview:")
        print(card[:2000])
        if len(card) > 2000:
            print("...")
        print()
        print("Dry run only. Re-run with --commit to write the case card draft.")
        return 0

    if output.exists() and not args.overwrite:
        print(f"output already exists; use --overwrite if intended: {output}", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(card, encoding="utf-8", newline="\n")
    print(f"written={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
