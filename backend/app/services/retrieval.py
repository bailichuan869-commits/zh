from __future__ import annotations

import json
import re
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

from fastapi import HTTPException

from app.core.config import KB_ROOT
from app.repositories.search import get_connection


PROFILE_PATH = KB_ROOT / "retrieval-profiles.json"
DEFAULT_PROFILE = "general-search"
DEFAULT_PROFILE_VALUES: dict[str, Any] = {
    "allowed_kinds": ["wiki", "raw-manifest", "raw-file", "pdf-markdown"],
    "allowed_roles": [],
    "lifecycle_status": ["valid", "unknown", "draft", "historical", "superseded", "expired", "enacted-not-effective"],
    "answer_ready_only": False,
    "authority_order": ["official", "curated"],
    "top_k": 30,
    "score_threshold": 0.0,
    "require_citations": False,
    "mode": "hybrid",
}
VALID_LIFECYCLE_STATUSES = {
    "valid",
    "unknown",
    "draft",
    "historical",
    "superseded",
    "expired",
    "enacted-not-effective",
}


def load_profiles() -> dict[str, dict[str, Any]]:
    try:
        data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    profiles = data.get("profiles", {}) if isinstance(data, dict) else {}
    return profiles if isinstance(profiles, dict) else {}


def resolve_profile(name: str = DEFAULT_PROFILE) -> tuple[str, dict[str, Any]]:
    profile_name = (name or DEFAULT_PROFILE).strip() or DEFAULT_PROFILE
    values = load_profiles().get(profile_name)
    if not isinstance(values, dict):
        raise HTTPException(400, f"未知检索 profile: {profile_name}")
    profile = {**DEFAULT_PROFILE_VALUES, **values}
    profile["allowed_kinds"] = [str(item) for item in profile.get("allowed_kinds", [])]
    profile["allowed_roles"] = [str(item) for item in profile.get("allowed_roles", [])]
    profile["lifecycle_status"] = [str(item) for item in profile.get("lifecycle_status", [])]
    return profile_name, profile


def validate_as_of(value: str) -> str:
    normalized = (value or "").strip()
    if not normalized:
        return ""
    try:
        date.fromisoformat(normalized)
    except ValueError:
        raise HTTPException(400, "as_of 必须使用 YYYY-MM-DD 格式") from None
    return normalized


def _quote(term: str) -> str:
    return '"' + term.replace('"', '""') + '"'


def _match_variants(query: str) -> list[str]:
    compact = re.sub(r"\s+", "", query)
    variants: list[str] = []
    if compact:
        variants.append(_quote(compact))
    parts = [part for part in query.split() if part]
    if len(parts) > 1:
        fts_parts = [part for part in parts if len(part) >= 3]
        if fts_parts:
            variants.append(" AND ".join(_quote(part) for part in fts_parts))
            variants.append(" OR ".join(_quote(part) for part in fts_parts))
    if len(compact) >= 3:
        grams = [_quote(compact[index : index + 3]) for index in range(len(compact) - 2)]
        variants.append(" OR ".join(dict.fromkeys(grams)))
    return list(dict.fromkeys(variants))


def _table_columns(connection: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in connection.execute(f"PRAGMA table_info({table})").fetchall()}


def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {str(row[0]) for row in connection.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')").fetchall()}


def _filters(
    profile: dict[str, Any],
    columns: set[str],
    *,
    domain: str,
    kind: str,
    topic: str,
    status: str,
    source_type: str,
    tag: str,
    as_of: str,
) -> tuple[list[str], list[Any]]:
    conditions: list[str] = []
    params: list[Any] = []
    allowed_kinds = profile.get("allowed_kinds") or []
    if allowed_kinds:
        placeholders = ",".join("?" for _ in allowed_kinds)
        conditions.append(f"d.kind IN ({placeholders})")
        params.extend(allowed_kinds)
    if kind == "wiki":
        conditions.append("d.kind = 'wiki'")
    elif kind == "raw":
        conditions.append("d.kind <> 'wiki'")
    if domain:
        conditions.append("d.domain = ?")
        params.append(domain)
    if topic and "topic" in columns:
        conditions.append("d.topic = ?")
        params.append(topic)
    roles = profile.get("allowed_roles") or []
    if roles and "page_role" in columns:
        placeholders = ",".join("?" for _ in roles)
        conditions.append(f"d.page_role IN ({placeholders})")
        params.extend(roles)
    if profile.get("answer_ready_only") and "answer_ready" in columns:
        conditions.append("d.answer_ready = 1")
    statuses = [status.strip()] if status.strip() else list(profile.get("lifecycle_status") or [])
    statuses = [item for item in statuses if item]
    if statuses and "lifecycle_status" in columns:
        placeholders = ",".join("?" for _ in statuses)
        conditions.append(f"d.lifecycle_status IN ({placeholders})")
        params.extend(statuses)
    if source_type and "source_type" in columns:
        conditions.append("d.source_type = ?")
        params.append(source_type)
    if tag and "tags" in columns:
        conditions.append("(',' || d.tags || ',') LIKE ?")
        params.append(f"%,{tag.strip()},%")
    if as_of and {"published_on", "effective_from", "effective_to"}.issubset(columns):
        conditions.extend([
            "(d.published_on = '' OR d.published_on <= ?)",
            "(d.effective_from = '' OR d.effective_from <= ?)",
            "(d.effective_to = '' OR d.effective_to >= ?)",
        ])
        params.extend([as_of, as_of, as_of])
    return conditions, params


def _excerpt(body: str, query: str, limit: int = 900) -> str:
    text = " ".join(str(body or "").split())
    compact = re.sub(r"\s+", "", query.lower())
    lower = text.lower()
    positions = [lower.find(term.lower()) for term in query.split() if term and lower.find(term.lower()) >= 0]
    if compact and compact in lower:
        positions.append(lower.find(compact))
    position = min(positions, default=0)
    start = max(0, position - 180)
    excerpt = text[start : start + limit]
    if start:
        excerpt = "..." + excerpt
    if start + limit < len(text):
        excerpt += "..."
    return excerpt


def _section_anchor(heading: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", str(heading or "正文").strip().lower()).strip("-")
    return "section-" + (value[:80] or "body")


def _tags(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def _result(row: sqlite3.Row, query: str, engine: str) -> dict[str, Any]:
    lexical_score = float(row["lexical_score"] or 0.0)
    rank_boost = float(row["rank_boost"] or 0.0)
    result = {
        "kind": row["kind"],
        "title": row["title"],
        "path": row["path"],
        "source_url": row["source_url"] or "",
        "domain": row["domain"] or "",
        "topic": row["topic"] or "",
        "snippet": _excerpt(row["chunk_body"], query),
        "page_role": row["page_role"] or "",
        "maturity": row["maturity"] or "",
        "answer_ready": bool(row["answer_ready"]),
        "asset_id": row["asset_id"] or "",
        "source_id": row["source_id"] or "",
        "source_type": row["source_type"] or "",
        "knowledge_type": row["knowledge_type"] or "",
        "tags": _tags(row["tags"]),
        "authority": row["authority"] or "",
        "authority_level": row["authority_level"] or row["authority"] or "",
        "version": row["version"] or "",
        "published_on": row["published_on"] or "",
        "effective_from": row["effective_from"] or "",
        "effective_to": row["effective_to"] or "",
        "lifecycle_status": row["lifecycle_status"] or "valid",
        "raw_path": row["raw_path"] or "",
        "markdown_path": row["markdown_path"] or "",
        "content_sha256": row["content_sha256"] or "",
        "review_status": row["review_status"] or "",
        "supersedes": row["supersedes"] or "",
        "superseded_by": row["superseded_by"] or "",
        "section": row["heading"] or "正文",
        "section_anchor": _section_anchor(row["heading"] or "正文"),
        "score": round(max(0.0, -lexical_score) + max(0.0, rank_boost) / 100.0, 6),
        "retrieval_path": engine,
        "_sort": (lexical_score - rank_boost, row["path"], row["heading"] or ""),
    }
    return result


def _select_sql(columns: set[str], *, include_chunk: bool = True) -> str:
    optional = {
        name: (f"d.{name}" if name in columns else "''")
        for name in (
            "asset_id", "source_id", "source_type", "knowledge_type", "tags", "authority_level",
            "version", "published_on", "effective_from", "effective_to", "lifecycle_status",
            "raw_path", "markdown_path", "content_sha256", "review_status", "supersedes", "superseded_by",
        )
    }
    chunk = ", c.heading AS heading, c.body AS chunk_body" if include_chunk else ", d.title AS heading, d.body AS chunk_body"
    return f"""
        d.id AS id, d.kind AS kind, d.title AS title, d.path AS path,
        d.source_url AS source_url, d.domain AS domain, d.topic AS topic,
        d.page_role AS page_role, d.maturity AS maturity, d.answer_ready AS answer_ready,
        d.authority AS authority, d.rank_boost AS rank_boost,
        {optional['asset_id']} AS asset_id, {optional['source_id']} AS source_id,
        {optional['source_type']} AS source_type, {optional['knowledge_type']} AS knowledge_type,
        {optional['tags']} AS tags, {optional['authority_level']} AS authority_level,
        {optional['version']} AS version, {optional['published_on']} AS published_on,
        {optional['effective_from']} AS effective_from, {optional['effective_to']} AS effective_to,
        {optional['lifecycle_status']} AS lifecycle_status, {optional['raw_path']} AS raw_path,
        {optional['markdown_path']} AS markdown_path, {optional['content_sha256']} AS content_sha256,
        {optional['review_status']} AS review_status, {optional['supersedes']} AS supersedes,
        {optional['superseded_by']} AS superseded_by{chunk}
    """


def retrieve(
    query: str,
    *,
    profile: str = DEFAULT_PROFILE,
    domain: str = "",
    kind: str = "",
    topic: str = "",
    status: str = "",
    source_type: str = "",
    tag: str = "",
    as_of: str = "",
    limit: int | None = None,
    offset: int = 0,
) -> dict[str, Any]:
    normalized_query = query.strip()
    if not normalized_query:
        raise HTTPException(400, "检索关键词不能为空")
    if kind not in {"", "wiki", "raw"}:
        raise HTTPException(400, "kind 必须为空、wiki 或 raw")
    profile_name, profile_values = resolve_profile(profile)
    normalized_as_of = validate_as_of(as_of)
    requested_limit = limit or int(profile_values.get("top_k") or 30)
    requested_limit = max(1, min(int(requested_limit), 100))
    normalized_offset = max(0, int(offset))

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        columns = _table_columns(connection, "documents")
        tables = _table_names(connection)
        conditions, params = _filters(
            profile_values,
            columns,
            domain=domain.strip(),
            kind=kind,
            topic=topic.strip(),
            status=status,
            source_type=source_type.strip(),
            tag=tag.strip(),
            as_of=normalized_as_of,
        )
        where = " AND ".join(conditions) or "1 = 1"
        rows: list[sqlite3.Row] = []
        engine = "chunks-fts5"
        if {"chunks", "chunks_fts"}.issubset(tables):
            sql = f"""
                SELECT {_select_sql(columns)} , bm25(chunks_fts, 5.0, 1.0) AS lexical_score,
                       'section-' || c.id AS section_anchor
                FROM chunks_fts
                JOIN chunks c ON c.id = chunks_fts.rowid
                JOIN documents d ON d.id = c.document_id
                WHERE chunks_fts MATCH ? AND {where}
                ORDER BY lexical_score - d.rank_boost, d.path, c.id
            """
            variants = _match_variants(normalized_query)
            if profile_name == "answer-current":
                variants = variants[:2] if len(normalized_query.split()) > 1 else variants[:1]
            for expression in variants:
                try:
                    rows = connection.execute(sql, [expression, *params]).fetchall()
                except sqlite3.OperationalError:
                    rows = []
                if rows:
                    break
            if len(normalized_query.split()) > 1:
                terms = [term for term in normalized_query.split() if term]
                like_conditions = " AND ".join("(c.heading LIKE ? OR c.body LIKE ?)" for _ in terms)
                like_params = [value for term in terms for value in (f"%{term}%", f"%{term}%")]
                like_rows = connection.execute(
                    f"SELECT {_select_sql(columns)} , 0.0 AS lexical_score, 'section-' || c.id AS section_anchor FROM chunks c JOIN documents d ON d.id = c.document_id WHERE {like_conditions} AND {where} ORDER BY d.rank_boost DESC, d.path, c.id",
                    [*like_params, *params],
                ).fetchall()
                rows = [*like_rows, *rows]
            if not rows:
                title_like = f"%{normalized_query}%"
                rows = connection.execute(
                    f"SELECT {_select_sql(columns)} , 0.0 AS lexical_score, 'section-' || c.id AS section_anchor FROM chunks c JOIN documents d ON d.id = c.document_id WHERE d.title LIKE ? AND {where} ORDER BY d.rank_boost DESC, d.path, c.id",
                    [title_like, *params],
                ).fetchall()
            if not rows and len(re.sub(r"\s+", "", normalized_query)) < 3:
                like = f"%{normalized_query}%"
                rows = connection.execute(
                    f"SELECT {_select_sql(columns)} , 0.0 AS lexical_score, 'section-' || c.id AS section_anchor FROM chunks c JOIN documents d ON d.id = c.document_id WHERE (c.heading LIKE ? OR c.body LIKE ?) AND {where} ORDER BY d.rank_boost DESC, d.path, c.id",
                    [like, like, *params],
                ).fetchall()
        elif "documents_fts" in tables:
            engine = "documents-fts5-compat"
            sql = f"""
                SELECT {_select_sql(columns, include_chunk=False)}, bm25(documents_fts, 8.0, 1.0) AS lexical_score,
                       '' AS section_anchor
                FROM documents_fts JOIN documents d ON d.id = documents_fts.rowid
                WHERE documents_fts MATCH ? AND {where}
                ORDER BY lexical_score - d.rank_boost, d.path
            """
            variants = _match_variants(normalized_query)
            if profile_name == "answer-current":
                variants = variants[:2] if len(normalized_query.split()) > 1 else variants[:1]
            for expression in variants:
                try:
                    rows = connection.execute(sql, [expression, *params]).fetchall()
                except sqlite3.OperationalError:
                    rows = []
                if rows:
                    break
        else:
            engine = "documents-like-legacy"
            like = f"%{normalized_query}%"
            rows = connection.execute(
                f"SELECT {_select_sql(columns, include_chunk=False)}, 0.0 AS lexical_score, '' AS section_anchor FROM documents d WHERE (d.title LIKE ? OR d.body LIKE ?) AND {where} ORDER BY d.rank_boost DESC, d.path",
                [like, like, *params],
            ).fetchall()

        profile_threshold = float(profile_values.get("score_threshold") or 0.0)
        best: dict[int, dict[str, Any]] = {}
        for row in rows:
            item = _result(row, normalized_query, engine)
            if profile_threshold and item["score"] < profile_threshold:
                continue
            key = int(row["id"])
            current = best.get(key)
            if current is None or item["_sort"] < current["_sort"]:
                best[key] = item
        authority_order = {value: index for index, value in enumerate(profile_values.get("authority_order") or [])}
        ordered = sorted(
            best.values(),
            key=lambda item: (item["_sort"][0], authority_order.get(item["authority"], 99), item["path"], item["section"]),
        )
        for item in ordered:
            item.pop("_sort", None)
        facets: dict[str, int] = {}
        kinds = {"wiki": 0, "raw": 0}
        for item in ordered:
            if item["domain"]:
                facets[item["domain"]] = facets.get(item["domain"], 0) + 1
            kinds["wiki" if item["kind"] == "wiki" else "raw"] += 1
        trace = {
            "profile": profile_name,
            "mode": profile_values.get("mode", "hybrid"),
            "stages": ["chapter-fts5", "metadata-filter", "deterministic-authority-rerank"],
            "engine": engine,
            "query": normalized_query,
            "as_of": normalized_as_of,
            "status": status or ",".join(profile_values.get("lifecycle_status") or []),
            "candidate_count": len(rows),
            "matched_assets": len(ordered),
            "score_threshold": profile_threshold,
        }
        page = ordered[normalized_offset : normalized_offset + requested_limit]
        return {
            "results": page,
            "total": len(ordered),
            "facets": sorted(facets.items(), key=lambda item: (-item[1], item[0])),
            "kinds": kinds,
            "engine": engine,
            "profile": profile_name,
            "retrieval_trace": trace,
        }
    finally:
        connection.close()


def asset_for_path(path: str) -> dict[str, Any]:
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        columns = _table_columns(connection, "documents")
        if "path" not in columns:
            return {}
        row = connection.execute("SELECT * FROM documents WHERE path = ? ORDER BY id LIMIT 1", (path,)).fetchone()
        if row is None:
            return {}
        value = dict(row)
        value["tags"] = _tags(value.get("tags", ""))
        value.pop("body", None)
        value.pop("rank_boost", None)
        value.pop("id", None)
        return value
    finally:
        connection.close()
