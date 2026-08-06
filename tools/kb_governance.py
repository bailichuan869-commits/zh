"""Audit CPA-ZH asset metadata, admission gates, and source-registry coverage."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from kb_common import KB_ROOT, iter_markdown_pages, parse_frontmatter, read_text


DEFAULT_REPORT = "wiki/concepts/kb-governance-dashboard.md"
DEFAULT_JSON = "workspace/outputs/kb_governance.json"

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "asset_id": ("asset_id",),
    "source_id": ("source_id", "sources"),
    "knowledge_type": ("knowledge_type", "concept_type", "type"),
    "domain": ("domain",),
    "topic": ("topic",),
    "tags": ("tags",),
    "authority_level": ("authority_level", "authority"),
    "version": ("version", "version_label"),
    "published_on": ("published_on", "issued_date"),
    "effective_from": ("effective_from", "effective_on", "effective_date"),
    "effective_to": ("effective_to", "expiry_date", "expired_on"),
    "lifecycle_status": ("lifecycle_status",),
    "raw_path": ("raw_path", "local_file"),
    "markdown_path": ("markdown_path", "derived_markdown"),
    "source_url": ("source_url", "official_url", "url"),
    "content_sha256": ("content_sha256", "derived_sha256", "sha256"),
    "review_status": ("review_status",),
    "supersedes": ("supersedes",),
    "superseded_by": ("superseded_by",),
}

HIGH_RISK_SIGNALS = (
    "wiki/concepts/laws/",
    "wiki/concepts/accounting-standards",
    "wiki/concepts/audit-standards",
    "wiki/concepts/policy-",
    "wiki/concepts/regulations-",
)


def has_value(metadata: dict[str, Any], aliases: tuple[str, ...]) -> bool:
    for key in aliases:
        value = metadata.get(key)
        if isinstance(value, (list, tuple, set)) and value:
            return True
        if value not in (None, "", []):
            return True
    return False


def is_high_risk(rel_path: str, role: str) -> bool:
    normalized = rel_path.replace("\\", "/").lower()
    return role in {"knowledge", "case"} and any(signal in normalized for signal in HIGH_RISK_SIGNALS)


def _clean(value: str) -> str:
    return value.strip().strip("\"'")


def read_verified_documents(root: Path) -> list[dict[str, str]]:
    """Read the small, stable verified_documents subset without adding PyYAML."""
    registry = root / "source-registry.yml"
    if not registry.exists():
        return []
    records: list[dict[str, str]] = []
    active = False
    current: dict[str, str] | None = None
    for raw_line in registry.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() == "verified_documents:":
            active = True
            continue
        if active and line and not line.startswith(" "):
            break
        if not active:
            continue
        match = re.match(r"^\s*-\s+id:\s*(.+)$", line)
        if match:
            if current:
                records.append(current)
            current = {"id": _clean(match.group(1))}
            continue
        if current:
            field = re.match(r"^\s{4,}([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if field:
                current[field.group(1)] = _clean(field.group(2))
    if current:
        records.append(current)
    return records


def registry_issues(root: Path, records: list[dict[str, str]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required = ("official_url", "local_raw_path", "status", "verified_on")
    for record in records:
        identifier = record.get("id", "<missing-id>")
        for field in required:
            if not record.get(field):
                issues.append({"id": identifier, "issue": f"missing:{field}"})
        local_path = record.get("local_raw_path", "")
        if local_path and not (root / local_path).exists():
            issues.append({"id": identifier, "issue": f"missing-local:{local_path}"})
    return issues


def collect(root: Path = KB_ROOT, report_path: str = DEFAULT_REPORT) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    field_counts: Counter[str] = Counter({field: 0 for field in FIELD_ALIASES})
    role_counts: Counter[str] = Counter()
    issue_counts: Counter[str] = Counter()
    for path, rel_path, derived, _body in iter_markdown_pages(root):
        if rel_path == report_path.replace("\\", "/"):
            continue
        explicit, _ = parse_frontmatter(read_text(path))
        role = str(derived.get("page_role") or "knowledge")
        role_counts[role] += 1
        for field, aliases in FIELD_ALIASES.items():
            if has_value(explicit, aliases):
                field_counts[field] += 1
        high_risk = is_high_risk(rel_path, role)
        issues: list[str] = []
        if high_risk and not has_value(explicit, FIELD_ALIASES["lifecycle_status"]):
            issues.append("high-risk-missing-lifecycle")
        if high_risk and not has_value(explicit, FIELD_ALIASES["effective_from"]):
            issues.append("high-risk-missing-effective-from")
        if high_risk and not has_value(explicit, FIELD_ALIASES["version"]):
            issues.append("high-risk-missing-version")
        if bool(derived.get("answer_ready")) and role in {"knowledge", "case"} and not explicit.get("review_status"):
            issues.append("answer-ready-without-review-status")
        if explicit.get("review_status") == "agent-reviewed":
            issue_counts["agent-reviewed"] += 1
        if explicit.get("review_status") == "user-approved":
            issue_counts["user-approved"] += 1
        for issue in issues:
            issue_counts[issue] += 1
        pages.append(
            {
                "path": rel_path,
                "title": str(explicit.get("title") or path.stem),
                "role": role,
                "high_risk": high_risk,
                "answer_ready": bool(derived.get("answer_ready")),
                "review_status": str(explicit.get("review_status") or ""),
                "issues": issues,
            }
        )

    verified_documents = read_verified_documents(root)
    registry_errors = registry_issues(root, verified_documents)
    summary = {
        "generated_at": date.today().isoformat(),
        "pages": len(pages),
        "roles": dict(role_counts),
        "high_risk_pages": sum(1 for page in pages if page["high_risk"]),
        "answer_ready_pages": sum(1 for page in pages if page["answer_ready"]),
        "explicit_field_coverage": dict(field_counts),
        "issues": dict(issue_counts),
        "verified_documents": len(verified_documents),
        "registry_errors": len(registry_errors),
    }
    return {
        "summary": summary,
        "registry": {"verified_documents": verified_documents, "errors": registry_errors},
        "pages": pages,
    }


def _issue_rows(data: dict[str, Any], limit: int = 120) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for page in data["pages"]:
        if page["issues"]:
            rows.append((page["path"], page["title"], ", ".join(page["issues"])))
    return rows[:limit]


def render_report(data: dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "---",
        "title: CPA-ZH 知识资产治理仪表盘",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {summary['generated_at']}",
        f"updated: {summary['generated_at']}",
        "page_role: index",
        "maturity: reviewed",
        "answer_ready: false",
        "sources: [kb-governance]",
        "tags: [maintenance, governance, metadata, lifecycle, admission]",
        "related: [[concepts/kb-content-maturity-dashboard]], [[concepts/source-status-dashboard]], [[concepts/kb-content-completeness-report]]",
        "---",
        "",
        "# CPA-ZH 知识资产治理仪表盘",
        "",
        "本页检查知识资产元数据、版本生命周期、来源注册表和答疑准入状态。字段未显式记录时只统计为缺口，不把系统推导的默认值写成已核验事实。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| Wiki 页面 | {summary['pages']} |",
        f"| 高风险法规/准则/政策页 | {summary['high_risk_pages']} |",
        f"| 当前推导为 answer_ready | {summary['answer_ready_pages']} |",
        f"| Agent 复核页 | {summary['issues'].get('agent-reviewed', 0)} |",
        f"| 人工已批准页 | {summary['issues'].get('user-approved', 0)} |",
        f"| 已登记官方核验文档 | {summary['verified_documents']} |",
        f"| 来源注册表错误 | {summary['registry_errors']} |",
        "",
        "## 显式元数据覆盖率",
        "",
        "覆盖率按原始 frontmatter 统计；`asset_id`、内容哈希和默认生命周期可以由索引构建，但仍应在后续治理批次中决定哪些字段需要写回源页面。",
        "",
        "| 字段 | 已显式记录 | 页面总数 |",
        "|---|---:|---:|",
    ]
    for field, count in summary["explicit_field_coverage"].items():
        lines.append(f"| `{field}` | {count} | {summary['pages']} |")
    lines.extend([
        "",
        "## 需要治理的页面",
        "",
        "| 页面 | 标题 | 问答状态 | 治理问题 |",
        "|---|---|---|---|",
    ])
    rows = _issue_rows(data)
    if rows:
        for path, title, issues in rows:
            safe_title = title.replace("|", "\\|")
            ready = "ready" if any(
                page["path"] == path and page["answer_ready"] for page in data["pages"]
            ) else "not-ready"
            lines.append(f"| `{path}` | {safe_title} | {ready} | `{issues}` |")
    else:
        lines.append("| 无 |  |  |  |")
    lines.extend([
        "",
        "## 官方注册表",
        "",
        "`source-registry.yml` 当前只对明确登记的文档执行完整字段和本地路径检查；未登记的来源不会被自动视为已核验。",
        "",
        "| 文档 ID | 状态 | 本地原文 | 官方 URL |",
        "|---|---|---|---|",
    ])
    for record in data["registry"]["verified_documents"]:
        lines.append(
            f"| `{record.get('id', '')}` | `{record.get('status', '')}` | `{record.get('local_raw_path', '')}` | {record.get('official_url', '')} |"
        )
    if not data["registry"]["verified_documents"]:
        lines.append("| 无 |  |  |  |")
    if data["registry"]["errors"]:
        lines.extend(["", "注册表错误："])
        for item in data["registry"]["errors"]:
            lines.append(f"- `{item['id']}`：`{item['issue']}`")
    lines.extend([
        "",
        "## 下一步",
        "",
        "1. 先为高风险法规、会计准则、审计准则和政策页补入有证据支撑的版本、生效日期、生命周期和来源 ID。",
        "2. 再为 Agent 已复核内容生成稳定 `asset_id`、内容哈希和来源映射；不补写无法从来源确认的日期或效力。",
        "3. `agent-reviewed` 只表示 Agent 完成结构、引用和边界复核；正式高风险答疑仍保留人工批准底线。",
        "4. 新版本采用新资产并记录 `supersedes`/`superseded_by`，历史查询通过 `as_of` 显式指定日期。",
        "",
        f"_JSON 明细：`workspace/outputs/kb_governance.json`；生成日期：{summary['generated_at']}。_",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit CPA-ZH knowledge asset governance.")
    parser.add_argument("--root", default=str(KB_ROOT), help="Knowledge base root.")
    parser.add_argument("--write-report", action="store_true", help="Write Markdown and JSON reports.")
    parser.add_argument("--output", default=DEFAULT_REPORT, help="Markdown report path under the knowledge base root.")
    parser.add_argument("--json-output", default=DEFAULT_JSON, help="JSON report path relative to the project root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data = collect(root, args.output)
    summary = data["summary"]
    print(f"pages={summary['pages']}")
    print(f"high_risk_pages={summary['high_risk_pages']}")
    print(f"answer_ready_pages={summary['answer_ready_pages']}")
    print(f"registry_documents={summary['verified_documents']}")
    print(f"registry_errors={summary['registry_errors']}")
    for key, value in sorted(summary["issues"].items()):
        print(f"issue_{key}={value}")
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
