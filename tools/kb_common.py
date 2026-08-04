"""Shared metadata, Markdown, and path helpers for the CPA-ZH delivery features."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(os.environ.get("CPA_ZH_PROJECT_ROOT", str(Path(__file__).resolve().parents[1]))).resolve()
KB_ROOT = Path(os.environ.get("CPA_ZH_ROOT", str(PROJECT_ROOT / "knowledge-base" / "CPA-ZH"))).resolve()
EXCLUDED_PARTS = {"_drafts", "_maintenance", "_trash", "__pycache__"}
ROLE_LABELS = {
    "reference": "原文",
    "index": "目录",
    "knowledge": "知识专题",
    "case": "案例",
}


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def parse_scalar(value: str) -> Any:
    value = value.strip().strip("\"'")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [item.strip().strip("\"'") for item in inner.split(",")]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, re.S)
    if not match:
        return {}, text
    metadata: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)
    return metadata, text[match.end():]


def render_frontmatter(metadata: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, list):
            rendered = "[" + ", ".join(str(item) for item in value) + "]"
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def update_frontmatter(text: str, fields: dict[str, Any]) -> str:
    metadata, body = parse_frontmatter(text)
    metadata.update(fields)
    return render_frontmatter(metadata) + body.lstrip("\r\n")


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in path.parts)


def infer_page_role(rel_path: str, metadata: dict[str, Any]) -> str:
    explicit = str(metadata.get("page_role") or "").strip()
    if explicit in ROLE_LABELS:
        return explicit
    page_type = str(metadata.get("type") or "").strip()
    concept_type = str(metadata.get("concept_type") or "").strip()
    rel = rel_path.replace("\\", "/").lower()
    if page_type == "case" or "/cases/" in "/" + rel:
        return "case"
    if page_type in {"source", "raw-source", "law-article"} or "law-article" in concept_type:
        return "reference"
    if rel.endswith("/index.md") or concept_type in {
        "accounting-standard", "source-index", "maintenance-dashboard", "index"
    }:
        return "index"
    return "knowledge"


def infer_maturity(rel_path: str, metadata: dict[str, Any], body: str) -> str:
    explicit = str(metadata.get("maturity") or "").strip()
    if explicit in {"skeleton", "draft", "reviewed"}:
        return explicit
    role = infer_page_role(rel_path, metadata)
    status = str(metadata.get("status") or "").lower()
    if role == "reference":
        return "reviewed"
    if "reviewed" in status or "verified" in status:
        return "reviewed"
    compact = re.sub(r"\s+", "", body)
    if role == "index":
        return "reviewed" if len(compact) >= 250 else "skeleton"
    required = ("## 适用范围", "## 判断", "## 会计处理")
    if len(compact) < 500 or sum(section in body for section in required) < 2:
        return "skeleton"
    return "draft"


def infer_answer_ready(rel_path: str, metadata: dict[str, Any], body: str) -> bool:
    explicit = metadata.get("answer_ready")
    if isinstance(explicit, bool):
        return explicit
    if isinstance(explicit, str) and explicit.lower() in {"true", "false"}:
        return explicit.lower() == "true"
    role = infer_page_role(rel_path, metadata)
    maturity = infer_maturity(rel_path, metadata, body)
    if role == "reference":
        return is_authoritative_path(rel_path, metadata)
    return maturity == "reviewed" and role in {"knowledge", "case"}


def is_authoritative_path(rel_path: str, metadata: dict[str, Any] | None = None) -> bool:
    rel = rel_path.replace("\\", "/").lower()
    metadata = metadata or {}
    source_url = str(metadata.get("source_url") or "").lower()
    official_tree = rel.startswith(("raw/laws/", "raw/standards/", "raw/policies/", "raw/ethics/"))
    official_host = any(host in source_url for host in ("mof.gov.cn", "gov.cn", "cicpa.org.cn", "csrc.gov.cn"))
    return official_tree or official_host


def page_metadata(rel_path: str, text: str) -> dict[str, Any]:
    metadata, body = parse_frontmatter(text)
    role = infer_page_role(rel_path, metadata)
    maturity = infer_maturity(rel_path, metadata, body)
    return {
        **metadata,
        "page_role": role,
        "role_label": ROLE_LABELS[role],
        "maturity": maturity,
        "answer_ready": infer_answer_ready(rel_path, metadata, body),
        "authority": "official" if is_authoritative_path(rel_path, metadata) else "curated",
    }


def iter_markdown_pages(root: Path = KB_ROOT) -> Iterable[tuple[Path, str, dict[str, Any], str]]:
    for path in sorted((root / "wiki").rglob("*.md")):
        if is_excluded(path):
            continue
        text = read_text(path)
        metadata, body = parse_frontmatter(text)
        rel = path.relative_to(root).as_posix()
        yield path, rel, page_metadata(rel, text), body


def section_chunks(body: str, max_chars: int = 1800) -> list[tuple[str, str]]:
    """Split Markdown at headings, retaining bounded chunks for retrieval."""
    heading = "正文"
    current: list[str] = []
    sections: list[tuple[str, str]] = []

    def flush() -> None:
        nonlocal current
        content = "\n".join(current).strip()
        if content:
            while len(content) > max_chars:
                split_at = content.rfind("\n", 0, max_chars)
                if split_at < max_chars // 2:
                    split_at = max_chars
                sections.append((heading, content[:split_at].strip()))
                content = content[split_at:].strip()
            if content:
                sections.append((heading, content))
        current = []

    for line in body.splitlines():
        match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if match:
            flush()
            heading = match.group(2).strip()
        else:
            current.append(line)
    flush()
    return sections or [("正文", body.strip())]
