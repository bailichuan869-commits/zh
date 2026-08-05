"""Shared, framework-free service for CPA-ZH Agent operations."""
from __future__ import annotations

import hashlib
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
    from kb_common import is_excluded, parse_frontmatter, read_text, update_frontmatter
except ModuleNotFoundError:
    from tools.kb_common import is_excluded, parse_frontmatter, read_text, update_frontmatter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KB_ROOT = PROJECT_ROOT / "knowledge-base" / "CPA-ZH"
DEFAULT_PREVIEW_ROOT = PROJECT_ROOT / "workspace" / "tmp" / "cpa-zh-agent-previews"
PREVIEW_TTL_SECONDS = 600
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".html", ".htm", ".xml", ".yml", ".yaml"}
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
SLUG_RE = re.compile(r"[^a-z0-9-]+")


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

    def search(self, query: str, *, kind: str = "", domain: str = "", limit: int = 10) -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise AgentServiceError("invalid_query", "Search query cannot be empty")
        if kind not in {"", "wiki", "raw"}:
            raise AgentServiceError("invalid_kind", "kind must be empty, wiki, or raw")
        limit = max(1, min(int(limit), 100))
        db_path = self.root / "search" / "kb_search.sqlite"
        if not db_path.exists():
            raise AgentServiceError("index_missing", "Search index is missing; run tools/kb.py index")
        connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            conditions = ["(title LIKE ? OR body LIKE ?)"]
            like = f"%{query}%"
            params: list[Any] = [like, like]
            if kind == "wiki":
                conditions.append("kind = 'wiki'")
            elif kind == "raw":
                conditions.append("kind != 'wiki'")
            if domain:
                conditions.append("domain = ?")
                params.append(domain)
            rows = connection.execute(
                f"""
                SELECT kind, title, path, source_url, domain, topic,
                       substr(body, max(1, instr(lower(body), lower(?)) - 50), 220),
                       page_role, maturity, answer_ready
                FROM documents
                WHERE {' AND '.join(conditions)}
                ORDER BY CASE WHEN title LIKE ? THEN 0 ELSE 1 END, rank_boost DESC
                LIMIT ?
                """,
                [query, *params, like, limit],
            ).fetchall()
        finally:
            connection.close()
        results = [
            {
                "kind": row[0], "title": row[1], "path": row[2], "source_url": row[3] or "",
                "domain": row[4] or "", "topic": row[5] or "", "snippet": row[6] or "",
                "page_role": row[7] or "", "maturity": row[8] or "", "answer_ready": bool(row[9]),
            }
            for row in rows
        ]
        return {"query": query, "kind": kind, "domain": domain, "limit": limit, "results": results, "count": len(results)}

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
