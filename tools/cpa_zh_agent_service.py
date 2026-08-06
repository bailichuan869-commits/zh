"""Shared, framework-free service for CPA-ZH Agent operations."""
from __future__ import annotations

import hashlib
import csv
import json
import os
import re
import secrets
import sqlite3
import subprocess
import sys
import time
from argparse import Namespace
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable

try:
    from kb_common import is_excluded, metadata_list, parse_frontmatter, read_text, update_frontmatter
except ModuleNotFoundError:
    from tools.kb_common import is_excluded, metadata_list, parse_frontmatter, read_text, update_frontmatter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KB_ROOT = PROJECT_ROOT / "knowledge-base" / "CPA-ZH"
DEFAULT_PREVIEW_ROOT = PROJECT_ROOT / "workspace" / "tmp" / "cpa-zh-agent-previews"
PREVIEW_TTL_SECONDS = 600
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".html", ".htm", ".xml", ".yml", ".yaml"}
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
SLUG_RE = re.compile(r"[^a-z0-9-]+")
AGENT_REVIEW_SECTIONS = {
    "case": (
        "## 原始事实", "## 缺失事实", "## 争议点", "## 适用准则", "## 判断分支",
        "## 核心结论", "## 结论确定性", "## 会计处理", "## 审计程序",
        "## 底稿证据", "## 原文引用", "## 时效与限制",
    ),
    "knowledge": (
        "## 适用范围", "## 决定性事实", "## 准则入口", "## 判断路径",
        "## 分支结论", "## 会计处理", "## 列报与披露", "## 审计风险",
        "## 证据与底稿", "## 易错点", "## 案例链接", "## 时效与不确定性边界",
        "## 原文引用",
    ),
}
AGENT_REVIEW_LEGACY_SECTIONS = {
    "wiki/concepts/cash-flow-classification-and-presentation.md": (
        "## 适用范围", "## 决定性事实", "## 准则入口", "## 判断路径",
        "## 审计关注与底稿", "## 结论边界", "## 原文引用",
    ),
}
LOCAL_CASE_REVIEW_SECTIONS = (
    "## 案例来源", "## 事实背景", "## 争议问题", "## 准则入口",
    "## 判断过程", "## 会计处理建议", "## 审计关注点", "## 底稿留痕建议",
    "## 缺失事实", "## 结论确定性", "## 原文引用与边界",
)


class AgentServiceError(RuntimeError):
    def __init__(self, code: str, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


@dataclass(frozen=True)
class CommandResult:
    args: list[str]
    stdout: str
    stderr: str
    returncode: int


Runner = Callable[[list[str]], CommandResult]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(_sha256(item).encode("ascii"))
    return digest.hexdigest()


def _slug(value: str, fallback: str) -> str:
    candidate = value.strip().lower().replace("_", "-")
    candidate = SLUG_RE.sub("-", candidate).strip("-")
    return candidate or fallback


class CpaZhAgentService:
    def __init__(
        self,
        root: str | Path = DEFAULT_KB_ROOT,
        *,
        preview_root: str | Path = DEFAULT_PREVIEW_ROOT,
        demo_mode: bool | None = None,
        runner: Runner | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.preview_root = Path(preview_root).resolve()
        self.demo_mode = (os.environ.get("CPA_ZH_DEMO_MODE", "0") == "1") if demo_mode is None else demo_mode
        self.runner = runner or self._subprocess_runner
        if not (self.root / "wiki").is_dir() or not (self.root / "raw").is_dir():
            raise AgentServiceError("invalid_root", f"CPA-ZH root is incomplete: {self.root}")

    def _subprocess_runner(self, args: list[str]) -> CommandResult:
        command = [sys.executable, str(PROJECT_ROOT / "tools" / "kb.py"), "--root", str(self.root), *args]
        completed = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return CommandResult(command, completed.stdout.strip(), completed.stderr.strip(), completed.returncode)

    def _run_kb(self, args: list[str]) -> dict[str, Any]:
        result = self.runner(args)
        data = {"args": result.args, "stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
        if result.returncode != 0:
            raise AgentServiceError("command_failed", f"kb.py command failed: {' '.join(args)}", details=data)
        return data

    def _safe_kb_path(self, value: str, prefix: str, *, must_exist: bool = True) -> Path:
        normalized = value.strip().replace("\\", "/")
        if normalized.startswith(f"{prefix}/"):
            normalized = normalized[len(prefix) + 1 :]
        candidate = (self.root / prefix / normalized).resolve()
        allowed = (self.root / prefix).resolve()
        try:
            candidate.relative_to(allowed)
        except ValueError:
            raise AgentServiceError("invalid_path", f"Path must stay under {prefix}/") from None
        if must_exist and not candidate.exists():
            raise AgentServiceError("not_found", f"Path does not exist: {prefix}/{normalized}")
        return candidate

    def _preview_path(self, token: str) -> Path:
        if not re.fullmatch(r"[A-Za-z0-9_-]{24,120}", token):
            raise AgentServiceError("invalid_token", "Preview token is malformed")
        return self.preview_root / f"{token}.json"

    def _cleanup_previews(self) -> None:
        if not self.preview_root.exists():
            return
        now = int(time.time())
        for path in self.preview_root.glob("*.json"):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                if int(record.get("expires_at", 0)) <= now:
                    path.unlink(missing_ok=True)
            except (OSError, ValueError, TypeError):
                path.unlink(missing_ok=True)

    def _create_preview(
        self,
        operation: str,
        payload: dict[str, Any],
        data: dict[str, Any],
        *,
        targets: list[Path],
        inputs: list[Path] | None = None,
        commit_args: list[str] | None = None,
        changes: dict[str, Any] | None = None,
        changes_by_path: dict[str, dict[str, Any]] | None = None,
        body_replacements_by_path: dict[str, list[list[str]]] | None = None,
        warnings: list[str] | None = None,
    ) -> dict[str, Any]:
        self.preview_root.mkdir(parents=True, exist_ok=True)
        self._cleanup_previews()
        token = secrets.token_urlsafe(32)
        created_at = int(time.time())
        expires_at = created_at + PREVIEW_TTL_SECONDS
        record = {
            "version": 1,
            "token": token,
            "root": str(self.root),
            "operation": operation,
            "payload": payload,
            "data": data,
            "targets": [self._path_state(path) for path in targets],
            "inputs": [self._path_state(path) for path in (inputs or [])],
            "commit_args": commit_args or [],
            "changes": changes or {},
            "changes_by_path": changes_by_path or {},
            "body_replacements_by_path": body_replacements_by_path or {},
            "warnings": warnings or [],
            "created_at": created_at,
            "expires_at": expires_at,
        }
        self._preview_path(token).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "operation": operation,
            "data": data,
            "preview_token": token,
            "expires_at": expires_at,
            "warnings": warnings or [],
            "message": "Preview created; explicit confirmation is required before commit.",
        }

    def _path_state(self, path: Path) -> dict[str, Any]:
        resolved = path.resolve()
        state: dict[str, Any] = {"path": str(resolved), "exists": resolved.exists(), "kind": "missing"}
        if resolved.is_file():
            state.update({"kind": "file", "sha256": _sha256(resolved)})
        elif resolved.is_dir():
            state.update({"kind": "directory", "sha256": _tree_sha256(resolved)})
        return state

    def _validate_state(self, expected: dict[str, Any]) -> None:
        current = self._path_state(Path(expected["path"]))
        if current.get("exists") != expected.get("exists") or current.get("kind") != expected.get("kind"):
            raise AgentServiceError("content_changed", f"Path state changed after preview: {expected['path']}")
        if current.get("sha256") != expected.get("sha256"):
            raise AgentServiceError("content_changed", f"Path content changed after preview: {expected['path']}")

    def _load_preview(self, token: str) -> tuple[Path, dict[str, Any]]:
        path = self._preview_path(token)
        if not path.exists():
            raise AgentServiceError("preview_not_found", "Preview token does not exist or was already used")
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise AgentServiceError("preview_invalid", "Preview record cannot be read") from error
        if record.get("root") != str(self.root):
            raise AgentServiceError("preview_root_mismatch", "Preview belongs to another knowledge base")
        if int(record.get("expires_at", 0)) <= int(time.time()):
            path.unlink(missing_ok=True)
            raise AgentServiceError("preview_expired", "Preview token has expired")
        return path, record

    def search(
        self,
        query: str,
        *,
        kind: str = "",
        domain: str = "",
        limit: int = 10,
        profile: str = "general-search",
        as_of: str = "",
        status: str = "",
        source_type: str = "",
        tag: str = "",
    ) -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise AgentServiceError("invalid_query", "Search query cannot be empty")
        if kind not in {"", "wiki", "raw"}:
            raise AgentServiceError("invalid_kind", "kind must be empty, wiki, or raw")
        if as_of:
            try:
                date.fromisoformat(as_of)
            except ValueError:
                raise AgentServiceError("invalid_date", "as_of must use YYYY-MM-DD format") from None
        limit = max(1, min(int(limit), 100))
        db_path = self.root / "search" / "kb_search.sqlite"
        if not db_path.exists():
            raise AgentServiceError("index_missing", "Search index is missing; run tools/kb.py index")
        connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        try:
            columns = {str(row[1]) for row in connection.execute("PRAGMA table_info(documents)").fetchall()}
            tables = {str(row[0]) for row in connection.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')").fetchall()}
            profile_values: dict[str, Any] = {}
            profile_path = self.root / "retrieval-profiles.json"
            if profile_path.exists():
                try:
                    payload = json.loads(profile_path.read_text(encoding="utf-8"))
                    profiles = payload.get("profiles", {}) if isinstance(payload, dict) else {}
                    if not isinstance(profiles, dict) or profile not in profiles:
                        raise AgentServiceError("invalid_profile", f"Unknown retrieval profile: {profile}")
                    profile_values = dict(profiles[profile])
                except (OSError, ValueError):
                    raise AgentServiceError("invalid_profile", "Retrieval profiles cannot be read") from None
            conditions: list[str] = []
            params: list[Any] = []
            allowed_kinds = [str(item) for item in profile_values.get("allowed_kinds", [])]
            if allowed_kinds:
                conditions.append("d.kind IN (" + ",".join("?" for _ in allowed_kinds) + ")")
                params.extend(allowed_kinds)
            if kind == "wiki":
                conditions.append("d.kind = 'wiki'")
            elif kind == "raw":
                conditions.append("d.kind <> 'wiki'")
            if domain:
                conditions.append("d.domain = ?")
                params.append(domain)
            allowed_roles = [str(item) for item in profile_values.get("allowed_roles", [])]
            if allowed_roles and "page_role" in columns:
                conditions.append("d.page_role IN (" + ",".join("?" for _ in allowed_roles) + ")")
                params.extend(allowed_roles)
            if status and "lifecycle_status" in columns:
                conditions.append("d.lifecycle_status = ?")
                params.append(status)
            elif profile_values.get("lifecycle_status") and "lifecycle_status" in columns:
                statuses = [str(item) for item in profile_values["lifecycle_status"]]
                conditions.append("d.lifecycle_status IN (" + ",".join("?" for _ in statuses) + ")")
                params.extend(statuses)
            if profile_values.get("answer_ready_only") and "answer_ready" in columns:
                conditions.append("d.answer_ready = 1")
            if source_type and "source_type" in columns:
                conditions.append("d.source_type = ?")
                params.append(source_type)
            if tag and "tags" in columns:
                conditions.append("(',' || d.tags || ',') LIKE ?")
                params.append(f"%,{tag},%")
            if as_of and {"published_on", "effective_from", "effective_to"}.issubset(columns):
                conditions.extend([
                    "(d.published_on = '' OR d.published_on <= ?)",
                    "(d.effective_from = '' OR d.effective_from <= ?)",
                    "(d.effective_to = '' OR d.effective_to >= ?)",
                ])
                params.extend([as_of, as_of, as_of])
            where = " AND ".join(conditions) or "1 = 1"
            rows: list[sqlite3.Row] = []
            engine = "chunks-fts5"
            compact = re.sub(r"\s+", "", query)
            if {"chunks", "chunks_fts"}.issubset(tables):
                variants = ['"' + compact.replace('"', '""') + '"'] if compact else []
                if len(compact) >= 3:
                    variants.append(" OR ".join('"' + compact[i:i + 3].replace('"', '""') + '"' for i in range(len(compact) - 2)))
                sql = f"SELECT d.*, c.heading AS heading, c.body AS chunk_body, bm25(chunks_fts, 5.0, 1.0) AS lexical_score FROM chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid JOIN documents d ON d.id = c.document_id WHERE chunks_fts MATCH ? AND {where} ORDER BY lexical_score - d.rank_boost, d.path, c.id"
                for expression in variants:
                    try:
                        rows = connection.execute(sql, [expression, *params]).fetchall()
                    except sqlite3.OperationalError:
                        rows = []
                    if rows:
                        break
                if not rows and len(compact) < 3:
                    like = f"%{query}%"
                    rows = connection.execute(
                        f"SELECT d.*, c.heading AS heading, c.body AS chunk_body, 0.0 AS lexical_score FROM chunks c JOIN documents d ON d.id = c.document_id WHERE (c.heading LIKE ? OR c.body LIKE ?) AND {where} ORDER BY d.rank_boost DESC, d.path, c.id",
                        [like, like, *params],
                    ).fetchall()
            else:
                # Only legacy indexes without the chapter tables use this compatibility path.
                engine = "documents-like-legacy"
                like = f"%{query}%"
                rows = connection.execute(
                    f"SELECT d.*, d.title AS heading, d.body AS chunk_body, 0.0 AS lexical_score FROM documents d WHERE (d.title LIKE ? OR d.body LIKE ?) AND {where} ORDER BY d.rank_boost DESC, d.path LIMIT ?",
                    [like, like, *params, limit],
                ).fetchall()
        finally:
            connection.close()
        best: dict[str, sqlite3.Row] = {}
        for row in rows:
            current = best.get(str(row["path"]))
            row_score = float(row["lexical_score"] or 0) - float(row["rank_boost"] or 0)
            current_score = float(current["lexical_score"] or 0) - float(current["rank_boost"] or 0) if current is not None else 0
            if current is None or row_score < current_score:
                best[str(row["path"])] = row
        results: list[dict[str, Any]] = []
        for row in best.values():
            body = " ".join(str(row["chunk_body"] or "").split())
            results.append({
                "kind": row["kind"], "title": row["title"], "path": row["path"], "source_url": row["source_url"] or "",
                "domain": row["domain"] or "", "topic": row["topic"] or "", "snippet": body[:420],
                "page_role": row["page_role"] or "", "maturity": row["maturity"] or "", "answer_ready": bool(row["answer_ready"]),
                "authority": row["authority"] if "authority" in row.keys() else "", "asset_id": row["asset_id"] if "asset_id" in row.keys() else "",
                "source_id": row["source_id"] if "source_id" in row.keys() else "", "source_type": row["source_type"] if "source_type" in row.keys() else "",
                "version": row["version"] if "version" in row.keys() else "", "published_on": row["published_on"] if "published_on" in row.keys() else "",
                "effective_from": row["effective_from"] if "effective_from" in row.keys() else "", "effective_to": row["effective_to"] if "effective_to" in row.keys() else "",
                "lifecycle_status": row["lifecycle_status"] if "lifecycle_status" in row.keys() else "", "raw_path": row["raw_path"] if "raw_path" in row.keys() else "",
                "markdown_path": row["markdown_path"] if "markdown_path" in row.keys() else "", "content_sha256": row["content_sha256"] if "content_sha256" in row.keys() else "",
                "review_status": row["review_status"] if "review_status" in row.keys() else "", "section": row["heading"] or "正文",
                "score": round(max(0.0, -float(row["lexical_score"] or 0)) + max(0.0, float(row["rank_boost"] or 0)) / 100.0, 6),
                "retrieval_path": engine,
            })
        score_threshold = float(profile_values.get("score_threshold") or 0.0)
        if score_threshold:
            results = [item for item in results if item["score"] >= score_threshold]
        authority_order = {str(value): index for index, value in enumerate(profile_values.get("authority_order", []))}
        results.sort(key=lambda item: (-item["score"], authority_order.get(item["authority"], 99), item["path"], item["section"]))
        results = results[:limit]
        return {
            "query": query,
            "kind": kind,
            "domain": domain,
            "limit": limit,
            "results": results,
            "count": len(results),
            "profile": profile,
            "retrieval_trace": {
                "profile": profile,
                "engine": engine,
                "stages": ["chapter-fts5", "metadata-filter", "deterministic-authority-rerank"],
                "candidate_count": len(rows),
                "matched_assets": len(results),
                "as_of": as_of,
                "score_threshold": score_threshold,
            },
        }

    def read_page(self, path: str) -> dict[str, Any]:
        target = self._safe_kb_path(path, "wiki")
        if target.suffix.lower() != ".md" or not target.is_file():
            raise AgentServiceError("invalid_page", "Wiki page must be a Markdown file")
        text = read_text(target)
        metadata, body = parse_frontmatter(text)
        links = sorted({match.group(1).strip() for match in WIKILINK_RE.finditer(body)})
        return {
            "path": target.relative_to(self.root).as_posix(),
            "title": str(metadata.get("title") or target.stem),
            "frontmatter": metadata,
            "markdown": body,
            "links": links,
            "sha256": _sha256(target),
        }

    def read_raw(self, path: str) -> dict[str, Any]:
        target = self._safe_kb_path(path, "raw")
        if not target.is_file():
            raise AgentServiceError("invalid_raw", "Raw path must identify a file")
        readable = target
        if target.suffix.lower() not in TEXT_SUFFIXES:
            sidecar = target.with_name(target.name + ".md")
            if not sidecar.exists():
                raise AgentServiceError("binary_without_facade", "Binary raw file has no Markdown facade")
            readable = sidecar
        text = read_text(readable)
        metadata, body = parse_frontmatter(text)
        return {
            "path": target.relative_to(self.root).as_posix(),
            "facade_path": readable.relative_to(self.root).as_posix(),
            "metadata": metadata,
            "text": body,
            "size": target.stat().st_size,
            "sha256": _sha256(target),
        }

    def health(self) -> dict[str, Any]:
        wiki_pages = sum(1 for path in (self.root / "wiki").rglob("*.md") if path.is_file())
        raw_files = sum(1 for path in (self.root / "raw").rglob("*") if path.is_file() and not is_excluded(path))
        manifests = list((self.root / "raw").rglob("manifest.json"))
        db_path = self.root / "search" / "kb_search.sqlite"
        indexed = 0
        if db_path.exists():
            connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            try:
                indexed = int(connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0])
            finally:
                connection.close()
        command = self._run_kb(["health"])
        return {
            "healthy": True,
            "wiki_pages": wiki_pages,
            "raw_files": raw_files,
            "manifests": len(manifests),
            "indexed_documents": indexed,
            "search_index_present": db_path.exists(),
            "report": command["stdout"],
        }

    def pending_reviews(self) -> dict[str, Any]:
        items: list[dict[str, Any]] = []
        for target in sorted((self.root / "wiki").rglob("*.md")):
            if is_excluded(target):
                continue
            metadata, body = parse_frontmatter(read_text(target))
            if metadata.get("review_status") != "pending-human-review":
                continue
            if not metadata.get("source_verified") or metadata.get("page_role") not in {"knowledge", "case"}:
                continue
            items.append({
                "path": target.relative_to(self.root).as_posix(),
                "title": str(metadata.get("title") or target.stem),
                "page_role": str(metadata.get("page_role")),
                "maturity": str(metadata.get("maturity") or "draft"),
                "raw_path": str(metadata.get("raw_path") or ""),
                "body_preview": body[:4000],
                "content_sha256": _sha256(target),
            })
        return {"items": items, "count": len(items)}

    def review_detail(self, path: str) -> dict[str, Any]:
        target, metadata, body = self._review_page(path)
        return {
            "path": target.relative_to(self.root).as_posix(),
            "title": str(metadata.get("title") or target.stem),
            "page_role": str(metadata.get("page_role")),
            "maturity": str(metadata.get("maturity") or "draft"),
            "raw_path": str(metadata.get("raw_path") or ""),
            "markdown": body,
            "frontmatter": metadata,
            "content_sha256": _sha256(target),
        }

    def _review_page(self, path: str) -> tuple[Path, dict[str, Any], str]:
        target = self._safe_kb_path(path, "wiki")
        if target.suffix.lower() != ".md":
            raise AgentServiceError("invalid_review", "Review target must be a wiki Markdown page")
        metadata, body = parse_frontmatter(read_text(target))
        if metadata.get("review_status") != "pending-human-review":
            raise AgentServiceError("not_pending", "Page is not pending human review")
        if not metadata.get("source_verified") or metadata.get("page_role") not in {"knowledge", "case"}:
            raise AgentServiceError("not_reviewable", "Page does not satisfy review admission conditions")
        return target, metadata, body

    def _agent_review_candidates(self, scope: str) -> list[tuple[Path, dict[str, Any], str]]:
        if scope not in {"golden", "all-pending"}:
            raise AgentServiceError("invalid_scope", "scope must be golden or all-pending")
        candidates: list[tuple[Path, dict[str, Any], str]] = []
        for target in sorted((self.root / "wiki").rglob("*.md")):
            if is_excluded(target):
                continue
            metadata, body = parse_frontmatter(read_text(target))
            if metadata.get("review_status") != "pending-human-review":
                continue
            if metadata.get("page_role") not in {"knowledge", "case"}:
                continue
            raw_path = str(metadata.get("raw_path") or "").replace("\\", "/")
            if not metadata.get("source_verified") and not (scope == "all-pending" and raw_path.startswith("raw/cases/")):
                continue
            tags = set(metadata_list(metadata.get("tags")))
            if scope == "golden" and not tags.intersection({"golden-case", "golden-topic"}):
                continue
            candidates.append((target, metadata, body))
        return candidates

    def _resolve_agent_raw_path(self, raw_path: str) -> tuple[Path, str]:
        normalized = raw_path.strip().replace("\\", "/")
        if not normalized.endswith(".md"):
            try:
                facade = self._safe_kb_path(normalized + ".md", "raw")
                return facade, facade.relative_to(self.root).as_posix()
            except AgentServiceError:
                pass
        try:
            target = self._safe_kb_path(normalized, "raw")
            return target, target.relative_to(self.root).as_posix()
        except AgentServiceError as first_error:
            if normalized.endswith(".md"):
                raise first_error
            try:
                target = self._safe_kb_path(normalized + ".md", "raw")
                return target, target.relative_to(self.root).as_posix()
            except AgentServiceError:
                raise first_error

    def _local_source_verified(self, raw_path: str, resolved_raw_path: str, raw_target: Path) -> bool:
        """Verify a local case through its batch manifest and derived facade."""
        if not resolved_raw_path.startswith("raw/cases/"):
            return False
        manifest_path = raw_target.parent / "manifest.json"
        if not manifest_path.is_file():
            return False
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return False
        items = data if isinstance(data, list) else data.get("items", []) if isinstance(data, dict) else []
        normalized_raw = raw_path.replace("\\", "/")
        for item in items:
            if not isinstance(item, dict):
                continue
            local_file = str(item.get("local_file") or "").replace("\\", "/")
            derived = str(item.get("derived_markdown") or "").replace("\\", "/")
            if normalized_raw not in {local_file, derived} and resolved_raw_path not in {local_file, derived}:
                continue
            original = self.root / local_file if local_file else raw_target.with_suffix("")
            declared_original = str(item.get("sha256") or "").lower()
            declared_derived = str(item.get("derived_sha256") or "").lower()
            if declared_original and (not original.is_file() or _sha256(original) != declared_original):
                return False
            if declared_derived and _sha256(raw_target) != declared_derived:
                return False
            return raw_target.is_file()
        return False

    def _official_source_url(self, raw_path: str) -> str:
        mapping_path = self.root / "raw" / "indexes" / "enterprise-accounting-standards-number-mapping.csv"
        if not mapping_path.exists():
            return ""
        target = raw_path.replace("\\", "/")
        target_without_md = target[:-3] if target.endswith(".md") else target
        try:
            with mapping_path.open("r", encoding="utf-8-sig", newline="") as stream:
                for row in csv.DictReader(stream):
                    local_path = str(row.get("LocalPath") or "").replace("\\", "/")
                    if local_path == target or local_path == target_without_md:
                        return str(row.get("Url") or "").strip()
        except (OSError, UnicodeError, csv.Error):
            return ""
        return ""

    def _agent_review_page(self, target: Path, metadata: dict[str, Any], body: str) -> dict[str, Any]:
        role = str(metadata.get("page_role") or "")
        raw_path = str(metadata.get("raw_path") or "").replace("\\", "/")
        errors: list[str] = []
        warnings = ["Agent 复核确认来源链和页面结构，不等同于官方最新效力确认或人工职业判断。"]
        raw_target: Path | None = None
        raw_metadata: dict[str, Any] = {}
        raw_body = ""
        resolved_raw_path = raw_path
        if not raw_path:
            errors.append("missing-raw-path")
        else:
            try:
                raw_target, resolved_raw_path = self._resolve_agent_raw_path(raw_path)
                raw_metadata, raw_body = parse_frontmatter(read_text(raw_target))
            except AgentServiceError:
                errors.append("raw-path-not-found-or-unsafe")

        rel_path = target.relative_to(self.root).as_posix()
        if role == "case" and rel_path.startswith("wiki/cases/2026-07-first-issue-"):
            required_sections = LOCAL_CASE_REVIEW_SECTIONS
        else:
            required_sections = AGENT_REVIEW_LEGACY_SECTIONS.get(rel_path, AGENT_REVIEW_SECTIONS.get(role, ()))
        missing_sections = [section for section in required_sections if section not in body]
        if missing_sections:
            errors.append("missing-required-sections")
        if not body.strip() or len(body.strip()) < 300:
            errors.append("body-too-short")
        local_source = resolved_raw_path.startswith("raw/cases/")
        source_verified = bool(metadata.get("source_verified"))
        if not source_verified and raw_target is not None:
            source_verified = self._local_source_verified(raw_path, resolved_raw_path, raw_target)
        if not source_verified:
            errors.append("source-not-verified")
        raw_linked = bool(raw_path and raw_path in body) or bool(resolved_raw_path and resolved_raw_path in body)
        source_heading_match = re.search(r"## 原文引用\r?\n", body)
        can_add_source_link = source_heading_match is not None
        if not raw_linked and not can_add_source_link:
            errors.append("raw-path-not-linked-in-page")
        source_url = str(raw_metadata.get("source_url") or "").strip() or self._official_source_url(resolved_raw_path)
        if not source_url and not local_source:
            errors.append("raw-source-url-missing")
        declared_sha256 = str(raw_metadata.get("sha256") or "").strip().lower()
        declared_sha_valid = bool(re.fullmatch(r"[0-9a-f]{64}", declared_sha256))
        raw_file_sha256 = _sha256(raw_target) if raw_target and raw_target.is_file() else ""
        if not declared_sha_valid and not raw_file_sha256:
            errors.append("raw-source-sha256-missing-or-facade-hash-unavailable")
        if not raw_body.strip():
            errors.append("raw-body-empty")
        if not raw_metadata.get("source_url") and source_url:
            warnings.append("raw 门面未声明 source_url，已从企业会计准则官方映射补足。")
        if not declared_sha_valid and raw_file_sha256:
            warnings.append("raw 门面未声明原始文件 sha256，报告记录了当前 Markdown 门面哈希。")

        checks = {
            "source_verified": source_verified,
            "raw_path_exists": raw_target is not None and raw_target.exists(),
            "raw_source_url": bool(source_url),
            "raw_declared_sha256": declared_sha_valid,
            "raw_facade_sha256": bool(raw_file_sha256),
            "raw_linked": raw_linked,
            "required_sections": not missing_sections,
            "complete_body": bool(body.strip()) and len(body.strip()) >= 300,
            "raw_body": bool(raw_body.strip()),
        }
        if local_source and not source_url:
            warnings.append("本地研讨材料无官方 URL；仅按 local raw、manifest 和 Markdown 门面哈希验证，不视为官方来源。")
        body_replacements: list[list[str]] = []
        pending_note = "> 复核状态：本页已按现有财政部原文结构化，尚待人工逐项复核。复核前不进入 AI 主检索集。"
        reviewed_note = "> 复核状态：Agent 已完成正文结构、raw 来源链和原文哈希复核；本页进入 AI 主检索集，但不替代报告期有效准则核验。"
        if pending_note in body:
            body_replacements.append([pending_note, reviewed_note])
        case_pending_note = "现有结论属于对所列事实的专业判断意见，尚待指定复核人对原始材料和报告期准则逐项复核；复核前不进入 AI 主检索集。"
        case_reviewed_note = "现有结论属于对所列事实的专业判断意见；Agent 已完成正文结构、raw 来源链和原文哈希复核，进入 AI 主检索集时仍须结合报告期准则和项目事实，不替代专业判断。"
        if case_pending_note in body:
            body_replacements.append([case_pending_note, case_reviewed_note])
        if resolved_raw_path and resolved_raw_path not in body:
            source_heading = source_heading_match.group(0) if source_heading_match else ""
            line_ending = "\r\n" if source_heading.endswith("\r\n") else "\n"
            source_link = f"## 原文引用{line_ending}{line_ending}- [S0] [[{resolved_raw_path}|准则原文]]{line_ending}"
            if source_heading:
                body_replacements.append([source_heading, source_link])
        return {
            "path": rel_path,
            "title": str(metadata.get("title") or target.stem),
            "page_role": role,
            "raw_path": resolved_raw_path,
            "content_sha256": _sha256(target),
            "raw_file_sha256": raw_file_sha256,
            "raw_declared_sha256": declared_sha256,
            "source_url": source_url,
            "source_scope": "local-only" if local_source and not source_url else "official-or-curated",
            "checks": checks,
            "missing_sections": missing_sections,
            "errors": errors,
            "warnings": warnings,
            "passed": not errors,
            "body_replacements": body_replacements,
        }

    def agent_review(
        self,
        scope: str = "golden",
        *,
        commit: bool = False,
        report_path: str = "",
    ) -> dict[str, Any]:
        candidates = self._agent_review_candidates(scope)
        reviewed_items = [self._agent_review_page(target, metadata, body) for target, metadata, body in candidates]
        passed = [item for item in reviewed_items if item["passed"]]
        rejected = [item for item in reviewed_items if not item["passed"]]
        today = date.today().isoformat()
        if report_path:
            report_file = Path(report_path).resolve()
        else:
            report_file = self.root.parent.parent / "workspace" / "outputs" / f"cpa-zh-agent-review-{today}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            report_rel = report_file.relative_to(self.root.parent.parent).as_posix()
        except ValueError:
            report_rel = str(report_file)
        report = {
            "version": 1,
            "mode": "agent-structural-source-review",
            "scope": scope,
            "reviewed_at": today,
            "policy_note": "agent-reviewed is an explicit Agent decision and is not user-approved or official validity confirmation.",
            "candidate_count": len(reviewed_items),
            "passed_count": len(passed),
            "rejected_count": len(rejected),
            "items": reviewed_items,
        }
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        data = {
            "scope": scope,
            "report_path": report_rel,
            "candidate_count": len(reviewed_items),
            "passed_count": len(passed),
            "rejected_count": len(rejected),
            "items": reviewed_items,
        }
        if not passed:
            return {"operation": "agent-review", "data": data, "warnings": ["No candidate passed the Agent review gate."]}

        fields_by_path: dict[str, dict[str, Any]] = {}
        body_replacements_by_path: dict[str, list[list[str]]] = {}
        for item in passed:
            target = (self.root / item["path"]).resolve()
            fields_by_path[str(target)] = {
                "maturity": "reviewed",
                "answer_ready": True,
                "review_status": "agent-reviewed",
                "source_verified": True,
                "review_actor": "cpa-zh-agent",
                "review_method": "structured-source-review-v1",
                "reviewed_at": today,
                "review_basis": "complete-markdown-raw-source-section-hash-check",
                "review_report": report_rel,
                "raw_path": item["raw_path"],
                "source_url": item["source_url"],
                "updated": today,
            }
            if item.get("source_scope") == "local-only":
                fields_by_path[str(target)]["source_scope"] = "local-only"
                fields_by_path[str(target)]["source_verification"] = "agent-raw-manifest-facade-check"
            if item["body_replacements"]:
                body_replacements_by_path[str(target)] = item["body_replacements"]
        targets = [(self.root / item["path"]).resolve() for item in passed]
        preview = self._create_preview(
            "agent-review",
            {"scope": scope, "report_path": report_rel, "paths": [item["path"] for item in passed]},
            data,
            targets=targets,
            changes_by_path=fields_by_path,
            body_replacements_by_path=body_replacements_by_path,
            warnings=[
                "Agent review passed structural and source-traceability checks.",
                "agent-reviewed is not user-approved and does not establish the latest official effectiveness.",
            ],
        )
        if not commit:
            return preview
        result = self.commit(preview["preview_token"], confirmed=True)
        result["report_path"] = report_rel
        result["reviewed_count"] = len(passed)
        result["rejected_count"] = len(rejected)
        return result

    def ingest_preview(
        self,
        source_path: str,
        raw_subdir: str,
        batch_slug: str,
        *,
        title: str = "",
        source_type: str = "local-source",
        official_source: str = "本地资料",
        official_url: str = "",
        tags: str = "",
    ) -> dict[str, Any]:
        source = Path(source_path).resolve()
        if not source.exists():
            raise AgentServiceError("source_not_found", f"Source path does not exist: {source}")
        if not re.fullmatch(r"[A-Za-z0-9/_-]{1,160}", raw_subdir):
            raise AgentServiceError("invalid_raw_subdir", "raw_subdir contains unsupported characters")
        target = self._safe_kb_path(raw_subdir, "raw", must_exist=False)
        if target.exists():
            raise AgentServiceError("target_exists", f"Target raw directory already exists: {target}")
        slug = _slug(batch_slug, "source-batch")
        args = ["ingest-local", "--source", str(source), "--raw-subdir", raw_subdir, "--batch-slug", slug]
        for flag, value in (("--title", title), ("--source-type", source_type), ("--official-source", official_source), ("--official-url", official_url), ("--tags", tags)):
            if value:
                args.extend([flag, value])
        dry_run = self._run_kb(args)
        try:
            from kb_ingest_local import manifest_item, plan_items
        except ModuleNotFoundError:
            from tools.kb_ingest_local import manifest_item, plan_items

        helper_args = Namespace(
            source_type=source_type,
            source_label="",
            imported_on=date.today().isoformat(),
            official_source=official_source,
            official_page_status="local",
            document_no="",
            official_url=official_url,
            wiki_page="",
            tags=tags,
        )
        planned = plan_items(root=self.root, source=source, batch_dir=target, existing_items=[])
        items = [
            {
                "source_path": str(item.source_path),
                "target_path": item.local_file,
                "bytes": item.bytes,
                "sha256": item.sha256,
                "metadata": manifest_item(item=item, args=helper_args),
            }
            for item in planned
        ]
        payload = {"source_path": str(source), "raw_subdir": raw_subdir, "batch_slug": slug, "title": title, "source_type": source_type, "official_source": official_source, "official_url": official_url, "tags": tags}
        data = {
            "source": str(source),
            "target": target.relative_to(self.root).as_posix(),
            "manifest_path": target.relative_to(self.root).as_posix() + "/manifest.json",
            "items": items,
            "changes": ["copy_raw_files", "write_manifest", "write_item_metadata"],
            "diagnostics": dry_run,
        }
        return self._create_preview(
            "ingest",
            payload,
            data,
            targets=[target],
            inputs=[source],
            commit_args=args,
            warnings=["Verify source authority, effective version, and target classification before archiving raw materials."],
        )

    def qa_preview(
        self,
        question: str,
        answer: str,
        *,
        slug: str = "",
        title: str = "",
        source: str = "local-qa-log",
        tags: str = "",
        related: str = "",
    ) -> dict[str, Any]:
        if len(question.strip()) < 2 or len(answer.strip()) < 2:
            raise AgentServiceError("invalid_qa", "Question and answer must both contain meaningful text")
        question_digest = hashlib.sha256(question.strip().encode("utf-8")).hexdigest()[:10]
        page_slug = _slug(slug, f"qa-{date.today().isoformat()}-{question_digest}")
        target = self._safe_kb_path(f"questions/{page_slug}.md", "wiki", must_exist=False)
        if target.exists():
            raise AgentServiceError("target_exists", f"Question page already exists: {target}")
        args = ["qa-capture", "--question", question, "--answer", answer, "--slug", page_slug, "--source", source]
        for flag, value in (("--title", title), ("--tags", tags), ("--related", related)):
            if value:
                args.extend([flag, value])
        dry_run = self._run_kb(args)
        try:
            from kb_qa_capture import DEFAULT_TAGS, dedupe, render_page, split_csv, suggest_related, title_from_question
        except ModuleNotFoundError:
            from tools.kb_qa_capture import DEFAULT_TAGS, dedupe, render_page, split_csv, suggest_related, title_from_question

        page_title = title_from_question(question, title)
        preview_markdown = render_page(
            title=page_title,
            question=question,
            answer=answer,
            source=source,
            tags=dedupe(DEFAULT_TAGS + split_csv(tags)),
            related=suggest_related(question, answer, related),
            status="draft",
            asked_on=date.today().isoformat(),
        )
        payload = {"question": question, "answer": answer, "slug": page_slug, "title": title, "source": source, "tags": tags, "related": related}
        data = {
            "target": target.relative_to(self.root).as_posix(),
            "title": page_title,
            "preview_markdown": preview_markdown,
            "changes": ["create_wiki_question_draft"],
            "diagnostics": dry_run,
        }
        return self._create_preview(
            "qa",
            payload,
            data,
            targets=[target],
            commit_args=args,
            warnings=["The Q&A page remains a draft and must not be treated as a formal professional conclusion before review."],
        )

    def case_preview(
        self,
        source_path: str,
        *,
        slug: str = "",
        title: str = "",
        source_id: str = "local-case-batch",
        raw_path: str = "",
        tags: str = "",
        related: str = "",
    ) -> dict[str, Any]:
        source = Path(source_path).resolve()
        if not source.is_file():
            raise AgentServiceError("source_not_found", f"Case source file does not exist: {source}")
        page_slug = _slug(slug or source.stem, "draft-case")
        target = self._safe_kb_path(f"cases/{page_slug}.md", "wiki", must_exist=False)
        if target.exists():
            raise AgentServiceError("target_exists", f"Case page already exists: {target}")
        args = ["case-card", "--source", str(source), "--slug", page_slug, "--source-id", source_id]
        for flag, value in (("--title", title), ("--raw-path", raw_path), ("--tags", tags), ("--related", related)):
            if value:
                args.extend([flag, value])
        dry_run = self._run_kb(args)
        try:
            from kb_case_card import rel as case_rel, render_case_card
            from kb_search import extract_file_text
        except ModuleNotFoundError:
            from tools.kb_case_card import rel as case_rel, render_case_card
            from tools.kb_search import extract_file_text

        resolved_raw_path = raw_path or case_rel(self.root, source)
        preview_markdown = render_case_card(
            Namespace(
                title=title,
                source_id=source_id,
                case_type="draft-case-card",
                tags=tags,
                related=related,
            ),
            self.root,
            source,
            resolved_raw_path,
            extract_file_text(source),
        )
        payload = {"source_path": str(source), "slug": page_slug, "title": title, "source_id": source_id, "raw_path": raw_path, "tags": tags, "related": related}
        data = {
            "source": str(source),
            "target": target.relative_to(self.root).as_posix(),
            "raw_path": resolved_raw_path,
            "preview_markdown": preview_markdown,
            "changes": ["create_wiki_case_draft"],
            "diagnostics": dry_run,
        }
        return self._create_preview(
            "case",
            payload,
            data,
            targets=[target],
            inputs=[source],
            commit_args=args,
            warnings=["The generated case card is a draft; facts, applicable rules, reasoning, and evidence must be reviewed."],
        )

    def review_preview(self, path: str, content_sha256: str = "") -> dict[str, Any]:
        target, metadata, body = self._review_page(path)
        current_hash = _sha256(target)
        if content_sha256 and content_sha256 != current_hash:
            raise AgentServiceError("content_changed", "Page changed after it was listed; reload review details")
        changes = {"maturity": "reviewed", "answer_ready": True, "review_status": "user-approved", "updated": date.today().isoformat()}
        before = {key: metadata.get(key) for key in changes}
        data = {
            "path": target.relative_to(self.root).as_posix(),
            "title": str(metadata.get("title") or target.stem),
            "raw_path": str(metadata.get("raw_path") or ""),
            "content_sha256": current_hash,
            "markdown": body,
            "changes": {key: {"from": before[key], "to": value} for key, value in changes.items()},
        }
        payload = {"path": data["path"], "content_sha256": current_hash}
        return self._create_preview(
            "review",
            payload,
            data,
            targets=[target],
            changes=changes,
            warnings=["Commit marks this page reviewed and answer-ready; approve only after reading the complete Markdown and source."],
        )

    def commit(self, preview_token: str, *, confirmed: bool) -> dict[str, Any]:
        if not confirmed:
            raise AgentServiceError("confirmation_required", "Commit requires confirmed=true after explicit user approval")
        preview_path, record = self._load_preview(preview_token)
        for state in [*record.get("inputs", []), *record.get("targets", [])]:
            self._validate_state(state)
        operation = str(record.get("operation"))
        if self.demo_mode:
            preview_path.unlink(missing_ok=True)
            return {"operation": operation, "simulated": True, "written": False, "preview": record.get("data", {}), "maintenance": []}

        # Consume before the first mutation so concurrent callers cannot reuse a token.
        preview_path.unlink(missing_ok=True)
        maintenance: list[dict[str, Any]] = []
        written = False
        try:
            if operation == "review":
                target = Path(record["targets"][0]["path"])
                target.write_text(update_frontmatter(read_text(target), record["changes"]), encoding="utf-8", newline="\n")
                written = True
                maintenance.append(self._run_kb(["index"]))
                maintenance.append(self._run_kb(["health"]))
            elif operation == "agent-review":
                changes_by_path = record.get("changes_by_path") or {}
                originals = {
                    Path(state["path"]): Path(state["path"]).read_bytes()
                    for state in record.get("targets", [])
                }
                try:
                    for state in record.get("targets", []):
                        target = Path(state["path"])
                        fields = changes_by_path.get(str(target))
                        if not isinstance(fields, dict):
                            raise AgentServiceError("preview_invalid", f"Missing agent review changes for {target}")
                        updated = update_frontmatter(read_text(target), fields)
                        for replacement in (record.get("body_replacements_by_path") or {}).get(str(target), []):
                            if not isinstance(replacement, list) or len(replacement) != 2:
                                raise AgentServiceError("preview_invalid", f"Invalid body replacement for {target}")
                            old, new = str(replacement[0]), str(replacement[1])
                            if old not in updated:
                                raise AgentServiceError("content_changed", f"Expected review note is missing from {target}")
                            updated = updated.replace(old, new, 1)
                        target.write_text(updated, encoding="utf-8", newline="\n")
                        written = True
                except Exception:
                    for target, content in originals.items():
                        target.write_bytes(content)
                    written = False
                    raise
                maintenance.append(self._run_kb(["index"]))
                maintenance.append(self._run_kb(["health"]))
            elif operation in {"ingest", "qa", "case"}:
                commit_args = list(record.get("commit_args") or [])
                if not commit_args:
                    raise AgentServiceError("preview_invalid", "Preview has no commit command")
                maintenance.append(self._run_kb([*commit_args, "--commit"]))
                written = True
                maintenance.append(self._run_kb(["cache", "build"]))
                maintenance.append(self._run_kb(["index"]))
                maintenance.append(self._run_kb(["health"]))
            else:
                raise AgentServiceError("unsupported_operation", f"Unsupported preview operation: {operation}")
        except AgentServiceError as error:
            details = {
                **error.details,
                "operation": operation,
                "written": written,
                "preview_token_consumed": True,
                "maintenance": maintenance,
            }
            code = "post_commit_failed" if written else "commit_failed"
            message = (
                "Knowledge content was written, but a post-write maintenance command failed"
                if written
                else "Commit failed before a successful knowledge-base write was confirmed"
            )
            raise AgentServiceError(code, message, details=details) from error
        except Exception as error:
            raise AgentServiceError(
                "post_commit_failed" if written else "commit_failed",
                "Commit did not complete; create a new preview before retrying",
                details={
                    "operation": operation,
                    "written": written,
                    "preview_token_consumed": True,
                    "maintenance": maintenance,
                    "exception": str(error),
                },
            ) from error
        return {"operation": operation, "simulated": False, "written": True, "preview": record.get("data", {}), "maintenance": maintenance}
