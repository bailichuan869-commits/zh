from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path


DEFAULT_SOURCE = "local-qa-log"
DEFAULT_TAGS = ["question", "qa-log", "writeback"]

RELATED_RULES = [
    (
        ["收入", "收入确认", "售后回购", "履约义务", "控制权"],
        [
            "concepts/accounting-standards/cas-14",
            "concepts/first-section-topics/revenue-recognition-misstatement",
            "concepts/case-topic-index",
        ],
    ),
    (
        ["政府补助", "免费使用", "其他收益"],
        [
            "concepts/accounting-standards/cas-16",
            "concepts/first-section-topics/government-grants-special-funds",
            "cases/2026-07-first-issue-government-grant-free-use-equipment",
        ],
    ),
    (
        ["长期股权投资", "长投", "内部重组", "商业实质"],
        [
            "concepts/accounting-standards/cas-02",
            "concepts/accounting-standards/cas-07",
            "concepts/first-section-topics/long-term-equity-investments",
            "cases/2026-07-first-issue-long-term-equity-investment-confirmation",
        ],
    ),
    (
        ["研发费用", "研发人员", "研发投入"],
        [
            "concepts/securities-issuance-rd-staff-investment",
            "concepts/policy-documents",
        ],
    ),
    (
        ["独立性", "职业道德", "非鉴证", "轮换"],
        [
            "concepts/independence-standard-1",
            "concepts/ethics-code",
            "concepts/history-ethics-independence",
        ],
    ),
    (
        ["案例", "案例卡片", "案例索引"],
        [
            "concepts/case-analysis",
            "concepts/case-topic-index",
            "concepts/cpa-zh-case-index-helper",
        ],
    ),
    (
        ["知识库", "维护", "检索", "索引", "问答"],
        [
            "concepts/kb-maintenance-workflow",
            "concepts/kb-user-guide",
            "concepts/ai-coding-tool-registry",
        ],
    ),
]


def read_optional_text(value: str, file_value: str, label: str) -> str:
    if value:
        return value.strip()
    if file_value:
        path = Path(file_value)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"{label} file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    return ""


def split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def normalize_related(value: str) -> str:
    value = value.strip()
    if value.startswith("[[") and value.endswith("]]"):
        value = value[2:-2]
    return value.strip()


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def suggest_related(question: str, answer: str, explicit_related: str) -> list[str]:
    haystack = f"{question}\n{answer}".lower()
    related = [normalize_related(value) for value in split_csv(explicit_related)]
    for keywords, links in RELATED_RULES:
        if any(keyword.lower() in haystack for keyword in keywords):
            related.extend(links)
    return dedupe(related)


def slugify(value: str, question: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if value:
        return value[:80]
    digest = hashlib.sha256(question.encode("utf-8")).hexdigest()[:10]
    return f"qa-{date.today().isoformat()}-{digest}"


def title_from_question(question: str, explicit_title: str) -> str:
    if explicit_title.strip():
        return explicit_title.strip()
    first_line = question.strip().splitlines()[0] if question.strip() else "本地问答记录"
    first_line = re.sub(r"\s+", " ", first_line).strip(" #")
    return first_line[:70] or "本地问答记录"


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def wiki_related(values: list[str]) -> str:
    return ", ".join(f"[[{value}]]" for value in values)


def render_page(
    *,
    title: str,
    question: str,
    answer: str,
    source: str,
    tags: list[str],
    related: list[str],
    status: str,
    asked_on: str,
) -> str:
    today = date.today().isoformat()
    lines = [
        "---",
        f"title: {title}",
        "type: question",
        "question_type: local-qa-writeback",
        f"created: {today}",
        f"updated: {today}",
        f"asked_on: {asked_on}",
        f"sources: [{source}]",
        f"status: {status}",
        f"tags: {yaml_list(tags)}",
        f"related: {wiki_related(related)}",
        "---",
        "",
        f"# {title}",
        "",
        "> 本页由 `tools/kb.py qa-capture` 生成，用于把本地问答沉淀为可检索、可回挂、可继续加工的知识库页面。专业判断仍需结合原文和人工复核。",
        "",
        "## 原问题",
        "",
        question,
        "",
        "## 回答记录",
        "",
        answer,
        "",
        "## 知识库关联",
        "",
    ]
    if related:
        lines.extend(f"- [[{link}]]" for link in related)
    else:
        lines.append("- 待补充。")

    lines.extend(
        [
            "",
            "## 可复用价值",
            "",
            "- 可作为后续相似问题检索入口。",
            "- 可进一步升级为案例卡片、专题页、检查清单或底稿模板。",
            "- 若涉及法规、准则或政策最新效力，应回到官方原文和本地归档核验。",
            "",
            "## 后续动作",
            "",
            "- [ ] 核对回答中引用的准则、政策、案例是否准确。",
            "- [ ] 补充或修正 `related` 链接。",
            "- [ ] 判断是否需要升级为案例卡片或专题页。",
            "- [ ] 必要时更新 [[concepts/case-topic-index]] 或相关专题页。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Capture a local Q&A into CPA-ZH wiki/questions.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--question", default="", help="Question text.")
    parser.add_argument("--answer", default="", help="Answer text.")
    parser.add_argument("--question-file", default="", help="UTF-8 file containing the question.")
    parser.add_argument("--answer-file", default="", help="UTF-8 file containing the answer.")
    parser.add_argument("--title", default="", help="Page title. Defaults to the first line of the question.")
    parser.add_argument("--slug", default="", help="Output slug. Defaults to a date+hash slug.")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Source id stored in frontmatter.")
    parser.add_argument("--tags", default="", help="Comma-separated extra tags.")
    parser.add_argument("--related", default="", help="Comma-separated wiki links or slugs.")
    parser.add_argument("--status", default="draft", help="Status value, e.g. draft/reviewed/structured.")
    parser.add_argument("--asked-on", default=date.today().isoformat(), help="Question date.")
    parser.add_argument("--commit", action="store_true", help="Write the question page.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing question page.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        question = read_optional_text(args.question, args.question_file, "question")
        answer = read_optional_text(args.answer, args.answer_file, "answer")
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not question:
        print("question is required; use --question or --question-file", file=sys.stderr)
        return 2
    if not answer:
        print("answer is required; use --answer or --answer-file", file=sys.stderr)
        return 2

    title = title_from_question(question, args.title)
    slug = slugify(args.slug, question)
    output = root / "wiki" / "questions" / f"{slug}.md"
    tags = dedupe(DEFAULT_TAGS + split_csv(args.tags))
    related = suggest_related(question, answer, args.related)
    page = render_page(
        title=title,
        question=question,
        answer=answer,
        source=args.source,
        tags=tags,
        related=related,
        status=args.status,
        asked_on=args.asked_on,
    )

    print(f"mode={'commit' if args.commit else 'dry-run'}")
    print(f"output={output}")
    print(f"title={title}")
    print(f"related={len(related)}")
    if not args.commit:
        print()
        print("Dry run preview:")
        print(page[:2400])
        if len(page) > 2400:
            print("...")
        print()
        print("Dry run only. Re-run with --commit to write the Q&A page.")
        return 0

    if output.exists() and not args.overwrite:
        print(f"output already exists; use --overwrite if intended: {output}", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8", newline="\n")
    print(f"written={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
