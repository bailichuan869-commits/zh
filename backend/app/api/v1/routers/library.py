from __future__ import annotations

import json
import mimetypes
import sys

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from app.core.config import CATEGORIES_PATH, DB_PATH
from app.core.files import read_text, safe_resolve
from app.schemas.library import AnswerRequest, AnswerResponse, BacklinksResponse, DocumentResponse, HealthResponse, SearchResponse, SummaryResponse
from app.services.answers import answer_service
from app.services.library import library_service, normalize_link, parse_frontmatter

router = APIRouter(tags=["knowledge-base"])
LAW_CONCEPT_TYPES = {"law-article", "law-article-index", "law-draft"}


def _clean_html(path):
    """Reuse raw extraction's navigation removal before returning an HTML snapshot."""
    project_tools = path.parents[4] / "tools"
    if str(project_tools) not in sys.path:
        sys.path.insert(0, str(project_tools))
    try:
        from bs4 import BeautifulSoup
        from convert_raw_to_md import decompose_nav

        soup = BeautifulSoup(read_text(path), "html.parser")
        decompose_nav(soup)
        return str(soup)
    except Exception:
        return read_text(path)


def _visible_backlinks(path: str, frontmatter: dict[str, str]) -> list[dict[str, str]]:
    backlinks = library_service.backlinks.get(normalize_link(path), [])
    if frontmatter.get("concept_type") not in LAW_CONCEPT_TYPES:
        return backlinks
    normalized = normalize_link(path)
    if not normalized.startswith("concepts/laws/"):
        return backlinks
    family_prefix = normalized.rsplit("/", 1)[0] + "/"
    filtered = [item for item in backlinks if not item["path"].startswith(family_prefix)]
    direct_sources = library_service.direct_backlinks.get(normalized, set())
    if direct_sources:
        filtered = [item for item in filtered if item["path"] in direct_sources]
    return filtered or backlinks


@router.get("/health", response_model=HealthResponse)
def health() -> dict:
    return {"status": "ok" if DB_PATH.exists() else "degraded", "index_ready": DB_PATH.exists(), "wiki_pages": library_service.wiki_page_count, "backlink_targets": len(library_service.backlinks)}


@router.get("/library/summary", response_model=SummaryResponse)
def summary() -> dict:
    return library_service.summary()


@router.get("/navigation/tree")
def tree() -> JSONResponse:
    if not CATEGORIES_PATH.exists():
        raise HTTPException(503, "分类树不存在，请先运行 classify_wiki.py build")
    return JSONResponse(json.loads(CATEGORIES_PATH.read_text(encoding="utf-8")))


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1),
    domain: str = "",
    kind: str = "",
    profile: str = "general-search",
    as_of: str = "",
    status: str = "",
    source_type: str = "",
    tag: str = "",
    limit: int = Query(30, le=100),
    offset: int = Query(0, ge=0),
) -> dict:
    return library_service.search(
        q,
        domain,
        kind,
        limit,
        offset,
        profile=profile,
        as_of=as_of,
        status=status,
        source_type=source_type,
        tag=tag,
    )


@router.post("/answers", response_model=AnswerResponse)
def answer(payload: AnswerRequest) -> dict:
    return answer_service.answer(
        payload.question,
        payload.topic,
        profile=payload.profile,
        as_of=payload.as_of,
        depth=payload.depth,
    )


@router.get("/documents", response_model=DocumentResponse)
def document(path: str) -> dict:
    target = safe_resolve(path, allowed_prefix="wiki/")
    if not target.exists() or target.suffix.lower() != ".md":
        raise HTTPException(404, f"页面不存在: {path}")
    frontmatter, markdown = parse_frontmatter(read_text(target))
    return {
        "path": path,
        "frontmatter": frontmatter,
        "markdown": markdown,
        "backlinks": _visible_backlinks(path, frontmatter),
        "asset": library_service.asset(path),
    }


@router.get("/documents/backlinks", response_model=BacklinksResponse)
def backlinks(path: str) -> dict:
    target = safe_resolve(path, allowed_prefix="wiki/")
    if not target.exists() or target.suffix.lower() != ".md":
        raise HTTPException(404, f"页面不存在: {path}")
    frontmatter, _ = parse_frontmatter(read_text(target))
    return {"path": path, "backlinks": _visible_backlinks(path, frontmatter)}


@router.get("/files")
def file(path: str):
    target = safe_resolve(path, allowed_prefix="raw/")
    if not target.exists() or not target.is_file():
        raise HTTPException(404, f"文件不存在: {path}")
    media_type, _ = mimetypes.guess_type(str(target))
    headers = {"Cache-Control": "no-store, must-revalidate", "Pragma": "no-cache"}
    suffix = target.suffix.lower()
    if suffix in {".md", ".txt"}:
        media_type = "text/plain; charset=utf-8"
    if suffix in {".html", ".htm"}:
        headers["Content-Security-Policy"] = "default-src 'self'; script-src 'none'; style-src 'unsafe-inline' 'self'; img-src 'self' data:"
        return HTMLResponse(_clean_html(target), media_type="text/html", headers=headers)
    return FileResponse(target, media_type=media_type, headers=headers)
