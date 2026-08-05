"""Local stdio MCP server for CPA-ZH."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

from mcp.server.fastmcp import FastMCP

try:
    from cpa_zh_agent_service import AgentServiceError, CpaZhAgentService, DEFAULT_KB_ROOT, DEFAULT_PREVIEW_ROOT
except ModuleNotFoundError:
    from tools.cpa_zh_agent_service import AgentServiceError, CpaZhAgentService, DEFAULT_KB_ROOT, DEFAULT_PREVIEW_ROOT


mcp = FastMCP("CPA-ZH", instructions="Search, read, and maintain the local CPA-ZH knowledge base. Every write requires preview followed by explicit commit confirmation.")


def _service() -> CpaZhAgentService:
    root = Path(os.environ.get("CPA_ZH_ROOT", str(DEFAULT_KB_ROOT)))
    preview_root = Path(os.environ.get("CPA_ZH_AGENT_PREVIEW_ROOT", str(DEFAULT_PREVIEW_ROOT)))
    return CpaZhAgentService(root, preview_root=preview_root)


def _call(operation: str, callback: Callable[[CpaZhAgentService], dict[str, Any]]) -> dict[str, Any]:
    try:
        result = callback(_service())
        preview_token = str(result.pop("preview_token", ""))
        expires_at = result.pop("expires_at", None)
        warnings = result.pop("warnings", [])
        message = result.pop("message", "")
        response_data = result.get("data") if preview_token else result
        return {"ok": True, "operation": operation, "data": response_data, "preview_token": preview_token, "expires_at": expires_at, "warnings": warnings, "error_code": "", "message": message}
    except AgentServiceError as error:
        return {"ok": False, "operation": operation, "data": error.details or None, "preview_token": "", "expires_at": None, "warnings": [], "error_code": error.code, "message": error.message}
    except Exception as error:
        return {"ok": False, "operation": operation, "data": None, "preview_token": "", "expires_at": None, "warnings": [], "error_code": "internal_error", "message": str(error)}


@mcp.tool()
def cpa_search(query: str, kind: str = "", domain: str = "", limit: int = 10) -> dict[str, Any]:
    """Search CPA-ZH wiki and raw sources with optional kind/domain filters."""
    return _call("search", lambda service: service.search(query, kind=kind, domain=domain, limit=limit))


@mcp.tool()
def cpa_read_page(path: str) -> dict[str, Any]:
    """Read a wiki Markdown page, metadata, links, and content hash."""
    return _call("read-page", lambda service: service.read_page(path))


@mcp.tool()
def cpa_read_raw(path: str) -> dict[str, Any]:
    """Read a raw text source or its required Markdown facade."""
    return _call("read-raw", lambda service: service.read_raw(path))


@mcp.tool()
def cpa_health() -> dict[str, Any]:
    """Run the CPA-ZH health gate and return structured counts plus the report."""
    return _call("health", lambda service: service.health())


@mcp.tool()
def cpa_pending_reviews() -> dict[str, Any]:
    """List source-verified knowledge and case pages pending human review."""
    return _call("pending-reviews", lambda service: service.pending_reviews())


@mcp.tool()
def cpa_review_detail(path: str) -> dict[str, Any]:
    """Read the complete body and metadata of one pending review page."""
    return _call("review-detail", lambda service: service.review_detail(path))


@mcp.tool()
def cpa_ingest_preview(
    source_path: str,
    raw_subdir: str,
    batch_slug: str,
    title: str = "",
    source_type: str = "local-source",
    official_source: str = "本地资料",
    official_url: str = "",
    tags: str = "",
) -> dict[str, Any]:
    """Preview a raw source ingest without writing files."""
    return _call("ingest-preview", lambda service: service.ingest_preview(source_path, raw_subdir, batch_slug, title=title, source_type=source_type, official_source=official_source, official_url=official_url, tags=tags))


@mcp.tool()
def cpa_qa_preview(
    question: str,
    answer: str,
    slug: str = "",
    title: str = "",
    source: str = "local-qa-log",
    tags: str = "",
    related: str = "",
) -> dict[str, Any]:
    """Preview a sourced Q&A wiki page; explicit commit is still required."""
    return _call("qa-preview", lambda service: service.qa_preview(question, answer, slug=slug, title=title, source=source, tags=tags, related=related))


@mcp.tool()
def cpa_case_preview(
    source_path: str,
    slug: str = "",
    title: str = "",
    source_id: str = "local-case-batch",
    raw_path: str = "",
    tags: str = "",
    related: str = "",
) -> dict[str, Any]:
    """Preview creation of a draft case card from a local source file."""
    return _call("case-preview", lambda service: service.case_preview(source_path, slug=slug, title=title, source_id=source_id, raw_path=raw_path, tags=tags, related=related))


@mcp.tool()
def cpa_review_preview(path: str, content_sha256: str = "") -> dict[str, Any]:
    """Preview the exact frontmatter changes for a pending human review page."""
    return _call("review-preview", lambda service: service.review_preview(path, content_sha256))


@mcp.tool()
def cpa_commit(preview_token: str, confirmed: bool) -> dict[str, Any]:
    """Commit an unexpired preview after explicit user confirmation."""
    return _call("commit", lambda service: service.commit(preview_token, confirmed=confirmed))


if __name__ == "__main__":
    mcp.run(transport="stdio")
