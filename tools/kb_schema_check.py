from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPORT_PATH = Path("wiki/concepts/kb-section-upgrade-dashboard.md")


SECTION_NAMES = {
    "section-1": "一、行业重要法规与准则",
    "section-2": "二、行业重要政策性文件",
    "section-3": "三、行业史与职业道德",
    "section-4": "四、实务技能与案例分析",
    "section-5": "五、AI 编程与自动化",
    "maintenance": "维护、索引与来源页",
    "unclassified": "未分类页面",
}


SECTION_TARGETS = {
    "section-1": [
        "官方来源、原文归档、本地索引三者一致",
        "核心法律、会计准则、审计准则页面保留效力状态和更新时间",
        "将高频准则继续沉淀为实务专题、审计程序和底稿提示",
    ],
    "section-2": [
        "政策原文、版本效力、执行检查清单持续联动",
        "按月或遇监管新规时复核官方链接和有效状态",
        "把政策要求拆成事务所治理、项目执行、人员管理和监督检查动作",
    ],
    "section-3": [
        "职业道德守则、独立性准则和应用指南保持官方原文可追溯",
        "补充独立性情景、威胁类型和防范措施矩阵",
        "将职业道德要求连接到审计项目承接、人员轮换和非鉴证服务判断",
    ],
    "section-4": [
        "案例卡片统一保留事实、规则、判断、审计关注点和底稿留痕",
        "按会计主题、审计风险和准则入口建立跨案例索引",
        "把成熟案例沉淀为程序模板、复核清单和问答口径",
    ],
    "section-5": [
        "讲义保留原始 Markdown，wiki 层提炼学习线和工具模板",
        "按 Agent、Python、VBA、审计自动化场景维护索引",
        "记录自动化工具的数据边界、控制点、证据留痕和适用风险",
    ],
}


SECTION_RULES = {
    "section-1": {
        "signals": [
            "law",
            "laws/",
            "regulation",
            "regulations",
            "standard",
            "standards",
            "accounting-standards",
            "audit-standards",
            "first-section",
            "core-laws",
            "securities-service",
            "revenue-recognition",
            "financial-instruments",
            "consolidation",
            "going-concern",
            "asset-impairment",
            "long-term-equity-investments",
        ],
    },
    "section-2": {
        "signals": [
            "policy",
            "policies/",
            "caihui",
            "audit-order",
            "integrity",
            "inspection",
            "issuance-guidance",
            "securities-issuance",
        ],
    },
    "section-3": {
        "signals": [
            "ethics",
            "independence",
            "history-ethics",
            "industry-history",
            "professional-ethics",
        ],
    },
    "section-4": {
        "signals": [
            "case",
            "cases/",
            "practice",
            "audit-practice",
            "audit-process",
            "intelligent-tools",
            "comprehensive-competency",
            "case-analysis",
            "case-topic-index",
        ],
    },
    "section-5": {
        "signals": [
            "ai-coding",
            "automation",
            "lecture",
            "lectures/",
            "agent",
            "python",
            "vba",
        ],
    },
}


MAINTENANCE_SIGNALS = [
    "kb-",
    "source-status",
    "overview",
    "log",
    "maintenance",
    "user-guide",
    "qa-log",
    "question",
]


@dataclass
class PageCheck:
    path: Path
    rel_path: str
    page_type: str
    section: str
    metadata: dict[str, Any]
    warnings: list[str]


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("'\"") for part in inner.split(",")]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value.strip("'\"")


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    metadata: dict[str, Any] = {}
    current_key = ""
    for raw_line in text[4:end].splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            metadata.setdefault(current_key, [])
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(line[4:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        metadata[key] = parse_scalar(value)
        current_key = key
    return metadata


def values_for_classification(rel_path: str, metadata: dict[str, Any]) -> str:
    parts: list[str] = [rel_path.lower()]
    for key in ("title", "type", "concept_type", "source_type", "case_type", "raw_path"):
        value = metadata.get(key)
        if value:
            parts.append(str(value).lower())
    for key in ("tags", "sources", "related"):
        value = metadata.get(key)
        if isinstance(value, list):
            parts.extend(str(item).lower() for item in value)
        elif value:
            parts.append(str(value).lower())
    return " ".join(parts)


def classify_section(rel_path: str, metadata: dict[str, Any]) -> str:
    signal_text = values_for_classification(rel_path, metadata)
    if rel_path in {"wiki/index.md", "wiki/overview.md", "wiki/log.md"}:
        return "maintenance"
    if rel_path.startswith("wiki/questions/"):
        return "maintenance"
    if rel_path.startswith("wiki/concepts/ai-coding") or rel_path == "wiki/concepts/cpa-zh-local-ingest-helper.md":
        return "section-5"
    if rel_path == "wiki/sources/ai-coding-lectures-archive-2026-07-09.md":
        return "section-5"
    if str(metadata.get("concept_type") or "") == "automation-tool":
        return "section-5"
    if any(signal in signal_text for signal in MAINTENANCE_SIGNALS):
        return "maintenance"

    # Cases and local lectures are strong path signals.
    if rel_path.startswith("wiki/cases/") or " raw/cases/" in signal_text:
        return "section-4"
    if " raw/lectures/" in signal_text or rel_path.startswith("wiki/concepts/ai-coding"):
        return "section-5"

    scores: Counter[str] = Counter()
    for section, rule in SECTION_RULES.items():
        for signal in rule["signals"]:
            if signal in signal_text:
                scores[section] += 1
    if not scores:
        return "unclassified"
    return scores.most_common(1)[0][0]


def page_type_from_path(rel_path: str, metadata: dict[str, Any]) -> str:
    explicit_type = str(metadata.get("type") or "").strip()
    if explicit_type:
        return explicit_type
    if rel_path.startswith("wiki/cases/"):
        return "case"
    if rel_path.startswith("wiki/questions/"):
        return "question"
    if rel_path.startswith("wiki/sources/"):
        return "source"
    if rel_path.startswith("wiki/concepts/"):
        return "concept"
    if rel_path.endswith("index.md"):
        return "index"
    return "unknown"


def require_fields(metadata: dict[str, Any], fields: list[str]) -> list[str]:
    missing = []
    for field in fields:
        value = metadata.get(field)
        if value is None or value == "" or value == []:
            missing.append(f"missing-frontmatter:{field}")
    return missing


def check_page(root: Path, path: Path) -> PageCheck:
    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    rel_path = rel(root, path)
    page_type = page_type_from_path(rel_path, metadata)
    section = classify_section(rel_path, metadata)

    warnings: list[str] = []
    if not metadata:
        warnings.append("missing-frontmatter")
    else:
        warnings.extend(require_fields(metadata, ["title", "type", "created", "updated", "tags"]))
        if page_type == "concept":
            warnings.extend(require_fields(metadata, ["concept_type"]))
        elif page_type == "source":
            warnings.extend(require_fields(metadata, ["source_type"]))
            if not metadata.get("raw_path") and not metadata.get("sources"):
                warnings.append("missing-frontmatter:raw_path-or-sources")
        elif page_type == "case":
            warnings.extend(require_fields(metadata, ["case_type", "sources", "raw_path"]))
        elif page_type == "question":
            warnings.extend(require_fields(metadata, ["question_type", "sources", "status"]))

    if section == "unclassified":
        warnings.append("section-unclassified")
    return PageCheck(path=path, rel_path=rel_path, page_type=page_type, section=section, metadata=metadata, warnings=warnings)


def collect_checks(root: Path) -> list[PageCheck]:
    wiki_root = root / "wiki"
    checks: list[PageCheck] = []
    for page in sorted(wiki_root.rglob("*.md")):
        checks.append(check_page(root, page))
    return checks


def summarize(checks: list[PageCheck]) -> tuple[Counter[str], Counter[str], dict[str, Counter[str]], list[PageCheck]]:
    section_counts = Counter(check.section for check in checks)
    warning_counts = Counter(warning for check in checks for warning in check.warnings)
    section_warning_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for check in checks:
        for warning in check.warnings:
            section_warning_counts[check.section][warning] += 1
    flagged = [check for check in checks if check.warnings]
    return section_counts, warning_counts, section_warning_counts, flagged


def print_summary(checks: list[PageCheck]) -> None:
    section_counts, warning_counts, section_warning_counts, flagged = summarize(checks)
    print(f"pages={len(checks)}")
    print(f"flagged={len(flagged)}")
    print()
    print("## Sections")
    for section, label in SECTION_NAMES.items():
        print(f"{section}={section_counts.get(section, 0)} # {label}")
    print()
    print("## Warnings")
    if warning_counts:
        for warning, count in sorted(warning_counts.items()):
            print(f"{warning}={count}")
    else:
        print("none=0")
    print()
    print("## Section warnings")
    for section, label in SECTION_NAMES.items():
        counter = section_warning_counts.get(section, Counter())
        if not counter:
            continue
        warning_text = ", ".join(f"{warning}:{count}" for warning, count in sorted(counter.items()))
        print(f"{section} # {label}: {warning_text}")


def render_report(root: Path, checks: list[PageCheck]) -> str:
    section_counts, warning_counts, section_warning_counts, flagged = summarize(checks)
    top_flagged = flagged[:60]
    today = date.today().isoformat()

    lines = [
        "---",
        "title: CPA-ZH 分板块技术升级仪表盘",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {today}",
        f"updated: {today}",
        "sources: [kb-schema-check]",
        "tags: [maintenance, schema, section-upgrade, quality-control, cpa]",
        "related: [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]], [[concepts/source-status-dashboard]]",
        "---",
        "",
        "# CPA-ZH 分板块技术升级仪表盘",
        "",
        "本页由 `tools/kb.py schema --write-report` 生成，用于按五个业务板块检查 wiki 页面元数据、来源结构和后续升级重点。它是治理看板，不替代具体法规、准则和案例页面的专业判断。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| wiki 页面 | {len(checks)} |",
        f"| 需关注页面 | {len(flagged)} |",
        f"| 警告类型 | {len(warning_counts)} |",
        "",
        "## 分板块现状",
        "",
        "| 板块 | 页面数 | 主要治理目标 | 当前提示 |",
        "|---|---:|---|---|",
    ]
    for section, label in SECTION_NAMES.items():
        targets = "；".join(SECTION_TARGETS.get(section, ["保持元数据、来源和索引可追溯"]))
        warnings = section_warning_counts.get(section, Counter())
        warning_text = "无" if not warnings else "；".join(f"`{key}` {value}" for key, value in sorted(warnings.items()))
        lines.append(f"| {label} | {section_counts.get(section, 0)} | {targets} | {warning_text} |")

    lines.extend(
        [
            "",
            "## 升级路线",
            "",
            "| 板块 | 下一步维护动作 | 推荐命令或入口 |",
            "|---|---|---|",
            "| 一、行业重要法规与准则 | 继续补齐核心准则专题页的有效版本、原文路径、实务影响、审计程序和底稿提示 | `tools/kb.py search \"收入确认 审计程序\"`；[[concepts/first-section-topic-matrix]] |",
            "| 二、行业重要政策性文件 | 每次政策变动后更新原文归档、版本效力跟踪和执行检查清单 | [[concepts/policy-version-validity-tracker]]；[[concepts/policy-execution-checklist]] |",
            "| 三、行业史与职业道德 | 将职业道德、独立性准则加工为情景库、威胁类型和防范措施矩阵 | [[concepts/ethics-code]]；[[concepts/independence-standard-1]] |",
            "| 四、实务技能与案例分析 | 新增案例统一加工为案例卡片，并回挂到主题索引和相关准则专题 | [[concepts/case-analysis]]；[[concepts/case-topic-index]] |",
            "| 五、AI 编程与自动化 | 将讲义沉淀为审计自动化工具模板、脚本边界、数据要求和证据留痕清单 | [[concepts/ai-coding-lectures]]；[[concepts/intelligent-tools]] |",
            "",
            "## 技术治理命令",
            "",
            "```powershell",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py schema",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py schema --write-report",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py sources write-report",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py index",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py readme",
            ".\\.venv\\Scripts\\python.exe tools\\kb.py health",
            "```",
            "",
            "## 警告类型说明",
            "",
            "| 类型 | 含义 | 处理方式 |",
            "|---|---|---|",
            "| `missing-frontmatter:*` | 页面缺少统一元数据字段 | 补充对应字段，优先补 `title`、`type`、`updated`、`tags`、来源字段 |",
            "| `section-unclassified` | 工具无法判断页面属于哪个板块 | 补充更明确的 tags、concept_type、source_type 或 related 链接 |",
            "| `missing-frontmatter` | 页面没有 YAML frontmatter | 按 WIKI.md 规范补齐页面头部 |",
            "",
            "## 需关注页面",
            "",
            "| 页面 | 板块 | 类型 | 提示 |",
            "|---|---|---|---|",
        ]
    )
    if top_flagged:
        for check in top_flagged:
            warnings = ", ".join(f"`{warning}`" for warning in check.warnings)
            lines.append(f"| `{check.rel_path}` | {SECTION_NAMES.get(check.section, check.section)} | `{check.page_type}` | {warnings} |")
    else:
        lines.append("| 无 |  |  |  |")

    if len(flagged) > len(top_flagged):
        lines.extend(["", f"_仅展示前 {len(top_flagged)} 个需关注页面；完整结果请运行 `tools/kb.py schema`。_"])

    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 本检查只覆盖 wiki 页面的结构化元数据和板块归类，不判断法规准则内容是否最新。",
            "- 涉及最新效力、官方链接和原文变动时，仍需结合 [[concepts/source-status-dashboard]] 和官方来源复核。",
            "- 批量新增资料后，应先刷新文本缓存和检索索引，再运行本检查和健康检查。",
            "",
            f"_生成路径：`{rel(root, root / REPORT_PATH)}`_",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Check CPA-ZH wiki schema and section governance.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--write-report", action="store_true", help="Write the section upgrade dashboard.")
    parser.add_argument("--output", default=str(REPORT_PATH), help="Output path under the knowledge base root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    checks = collect_checks(root)
    print_summary(checks)

    if args.write_report:
        output = root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_report(root, checks), encoding="utf-8", newline="\n")
        print()
        print(f"written={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
