"""Shared metadata, Markdown, and path helpers for the CPA-ZH delivery features."""
from __future__ import annotations

import hashlib
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
LIFECYCLE_STATUSES = {
    "valid",
    "unknown",
    "draft",
    "historical",
    "superseded",
    "expired",
    "enacted-not-effective",
}
CORE_LAW_ARTICLE_LINK_RE = re.compile(
    r"\[\[concepts/laws/(?P<slug>accounting-law|company-law|cpa-law|securities-law)/"
    r"(?P=slug)-article-(?P<number>\d{3})(?P<duplicate>-\d+)?"
    r"(?:#[^|\]]+)?(?P<label>\|[^\]]+)?\]\]"
)


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


def metadata_text(value: Any) -> str:
    """Render scalar or simple frontmatter collections into stable text."""
    if isinstance(value, (list, tuple, set)):
        return ",".join(str(item).strip() for item in value if str(item).strip())
    return str(value or "").strip()


def metadata_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        values = [str(item).strip() for item in value]
    else:
        values = [item.strip() for item in str(value or "").split(",")]
    return [item for item in values if item]


def normalize_core_law_article_links(text: str) -> tuple[str, int]:
    """Point legacy article links at the consolidated law-index anchors."""
    def replace(match: re.Match[str]) -> str:
        slug = match.group("slug")
        number = match.group("number")
        duplicate = match.group("duplicate") or ""
        label = match.group("label") or ""
        return f"[[concepts/laws/{slug}/index#article-{number}{duplicate}{label}]]"

    return CORE_LAW_ARTICLE_LINK_RE.subn(replace, text)


def lifecycle_status(metadata: dict[str, Any]) -> str:
    """Map existing status vocabulary onto the retrieval lifecycle contract."""
    explicit = metadata_text(metadata.get("lifecycle_status")).lower()
    if explicit in LIFECYCLE_STATUSES:
        return explicit
    status = metadata_text(metadata.get("status")).lower()
    if status in LIFECYCLE_STATUSES:
        return status
    if "supersed" in status or "replace" in status:
        return "superseded"
    if "expire" in status:
        return "expired"
    if "histor" in status:
        return "historical"
    if "draft" in status or "pending" in status:
        return "draft"
    if "enacted-not-effective" in status:
        return "enacted-not-effective"
    return "valid"


def asset_metadata(
    rel_path: str,
    metadata: dict[str, Any] | None = None,
    *,
    kind: str = "",
    page_role: str = "",
    domain: str = "",
    topic: str = "",
    source_url: str = "",
    raw_path: str = "",
    markdown_path: str = "",
    content_sha256: str = "",
    body: str = "",
    answer_ready: bool = False,
    authority: str = "curated",
) -> dict[str, Any]:
    """Build the stable asset projection used by the SQLite retrieval index."""
    values = metadata or {}
    normalized_path = rel_path.replace("\\", "/")
    role = page_role or metadata_text(values.get("page_role"))
    resolved_domain = domain or metadata_text(values.get("domain"))
    resolved_topic = topic or metadata_text(values.get("topic"))
    resolved_source_url = source_url or metadata_text(
        values.get("source_url") or values.get("url") or values.get("official_url")
    )
    source_values = metadata_list(values.get("source_id") or values.get("sources"))
    resolved_raw_path = raw_path or metadata_text(values.get("raw_path") or values.get("local_file"))
    resolved_markdown_path = markdown_path or metadata_text(values.get("markdown_path") or values.get("derived_markdown"))
    resolved_hash = content_sha256 or metadata_text(values.get("content_sha256") or values.get("derived_sha256") or values.get("sha256"))
    if not resolved_hash and body:
        resolved_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    resolved_authority = metadata_text(values.get("authority_level") or values.get("authority")) or authority
    return {
        "asset_id": metadata_text(values.get("asset_id")) or f"cpa-zh:{kind or 'asset'}:{normalized_path}",
        "source_id": source_values[0] if source_values else "",
        "source_type": metadata_text(values.get("source_type") or values.get("document_type")) or kind,
        "knowledge_type": metadata_text(values.get("knowledge_type") or values.get("type")) or role or kind,
        "domain": resolved_domain,
        "topic": resolved_topic,
        "tags": metadata_list(values.get("tags")),
        "authority_level": resolved_authority,
        "version": metadata_text(values.get("version") or values.get("version_label")),
        "published_on": metadata_text(values.get("published_on") or values.get("issued_date") or values.get("created") or values.get("imported_on")),
        "effective_from": metadata_text(values.get("effective_from") or values.get("effective_on") or values.get("effective_date")),
        "effective_to": metadata_text(values.get("effective_to") or values.get("expiry_date") or values.get("expired_on")),
        "lifecycle_status": lifecycle_status(values),
        "raw_path": resolved_raw_path,
        "markdown_path": resolved_markdown_path,
        "source_url": resolved_source_url,
        "content_sha256": resolved_hash,
        "review_status": metadata_text(values.get("review_status")),
        "supersedes": metadata_text(values.get("supersedes")),
        "superseded_by": metadata_text(values.get("superseded_by")),
        "page_role": role,
        "answer_ready": bool(answer_ready),
        "authority": resolved_authority,
    }


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
