from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import zipfile
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".html", ".htm", ".xml"}

# 已被新法（2026修订草案）取代、仅作历史版本的旧法文件，不进入常规检索索引。
# 文件物理保留，仍可通过 wiki/concepts/law-cpa.md 的历史链接访问。
SUPERSEDED_SEARCH_EXCLUDES = [
    "wiki/concepts/laws/cpa-law/cpa-law-article-*.md",
    "wiki/concepts/laws/cpa-law/index.md",
    "raw/laws/中华人民共和国注册会计师法.md",
]


def is_search_excluded(rel_path: str) -> bool:
    """True 表示该文件属于已被取代的旧法版本，应从检索索引中排除。"""
    import fnmatch
    return rel_path.endswith(".structure.json") or any(
        fnmatch.fnmatch(rel_path, pat) for pat in SUPERSEDED_SEARCH_EXCLUDES
    )


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        return normalize_text(" ".join(self.parts))


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    return re.sub(r"\s+", " ", text).strip()


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def strip_html(text: str) -> str:
    parser = TextExtractor()
    parser.feed(text)
    return parser.text()


def extract_docx(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
        return strip_html(xml)
    except Exception:
        return ""


def extract_pdf_pymupdf(path: Path) -> str:
    try:
        import fitz  # type: ignore

        document = fitz.open(str(path))
        try:
            return normalize_text("\n".join(page.get_text("text") for page in document))
        finally:
            document.close()
    except Exception:
        return ""


def extract_pdf_pdfplumber(path: Path) -> str:
    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(str(path)) as pdf:
            return normalize_text("\n".join(page.extract_text() or "" for page in pdf.pages))
    except Exception:
        return ""


def extract_pdf_pdfminer(path: Path) -> str:
    try:
        from pdfminer.high_level import extract_text  # type: ignore

        return normalize_text(extract_text(str(path)) or "")
    except Exception:
        return ""


def extract_pdf(path: Path) -> str:
    for extractor in (extract_pdf_pymupdf, extract_pdf_pdfplumber, extract_pdf_pdfminer):
        text = extractor(path)
        if text:
            return text

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return normalize_text(" ".join(page.extract_text() or "" for page in reader.pages))
    except Exception:
        pass

    try:
        from PyPDF2 import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return normalize_text(" ".join(page.extract_text() or "" for page in reader.pages))
    except Exception:
        return ""


def extract_file_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm", ".xml"}:
        return strip_html(read_text(path))
    if suffix in TEXT_SUFFIXES:
        return normalize_text(read_text(path))
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    return ""


def load_text_cache_manifest(root: Path) -> dict[str, dict[str, Any]]:
    manifest_path = root / "cache" / "text" / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    items = data.get("items", []) if isinstance(data, dict) else []
    return {str(item.get("raw_path")): item for item in items if item.get("raw_path")}


def cached_file_text(root: Path, path: Path, cache: dict[str, dict[str, Any]]) -> str:
    try:
        rel_path = path.relative_to(root).as_posix()
    except ValueError:
        return extract_file_text(path)

    item = cache.get(rel_path)
    if not item:
        return extract_file_text(path)

    stat = path.stat()
    if item.get("mtime_ns") != stat.st_mtime_ns or item.get("bytes") != stat.st_size:
        return extract_file_text(path)

    cache_path = root / str(item.get("cache_path") or "")
    if not cache_path.exists():
        return extract_file_text(path)

    text = read_text(cache_path)
    expected = str(item.get("text_sha256") or "")
    if expected:
        actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if actual != expected:
            return extract_file_text(path)
    return text


def frontmatter_title(text: str, fallback: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            frontmatter = text[3:end]
            for line in frontmatter.splitlines():
                if line.startswith("title:"):
                    return line.split(":", 1)[1].strip().strip("\"'")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


_LEAD_NUM_TITLE = re.compile(r"^\s*\d{1,4}[-_.\u3001、\s]+")


def clean_title(title: str) -> str:
    """去掉来源文档标题前缀的编号（如 '058-'、'058、'、'058.'），用于检索结果展示。"""
    if not title:
        return title
    cleaned = _LEAD_NUM_TITLE.sub("", title).strip()
    return cleaned or title


def load_manifest(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    return []


def resolve_local_file(root: Path, local_file: str) -> Path:
    path = Path(local_file)
    if path.is_absolute():
        return path
    normalized = local_file.replace("\\", "/")
    kb_prefix = "knowledge-base/CPA-ZH/"
    if normalized.startswith(kb_prefix):
        normalized = normalized[len(kb_prefix):]
    candidates = [
        root / path,
        root / normalized,
        Path.cwd() / path,
        root.parent / path,
        root.parents[1] / path if len(root.parents) > 1 else root / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _sidecar_metadata(path: Path) -> dict[str, Any]:
    metadata_path = path.parent / "metadata.json"
    if not metadata_path.exists():
        return {}
    try:
        value = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def iter_documents(root: Path) -> Iterable[dict[str, Any]]:
    text_cache = load_text_cache_manifest(root)
    try:
        from kb_common import parse_frontmatter
    except ModuleNotFoundError:
        from tools.kb_common import parse_frontmatter

    wiki_root = root / "wiki"
    for md in sorted(wiki_root.rglob("*.md")):
        if "_trash" in md.parts or "_maintenance" in md.parts:
            continue
        rel = md.relative_to(root).as_posix()
        if is_search_excluded(rel):
            continue
        text = read_text(md)
        metadata, _ = parse_frontmatter(text)
        yield {
            "kind": "wiki",
            "title": clean_title(frontmatter_title(text, md.stem)),
            "path": rel,
            "source_url": "",
            "body": normalize_text(text),
            "metadata": metadata,
            "markdown_path": rel,
            "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }

    pdf_markdown_root = root / "cache" / "pdf-markdown" / "files"
    if pdf_markdown_root.exists():
        for md in sorted(pdf_markdown_root.rglob("*.md")):
            text = read_text(md)
            metadata, _ = parse_frontmatter(text)
            yield {
                "kind": "pdf-markdown",
                "title": clean_title(frontmatter_title(text, md.stem)),
                "path": md.relative_to(root).as_posix(),
                "source_url": str(metadata.get("source_url") or metadata.get("url") or ""),
                "body": normalize_text(text),
                "metadata": metadata,
                "markdown_path": md.relative_to(root).as_posix(),
                "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }

    manifest_files = sorted((root / "raw").rglob("manifest.json"))
    manifest_local_files: set[str] = set()
    for manifest_path in manifest_files:
        for item in load_manifest(manifest_path):
            local_file = str(item.get("local_file") or "")
            if local_file:
                manifest_local_files.add(local_file.replace("\\", "/"))
                manifest_local_files.add(local_file.replace("\\", "/").replace("knowledge-base/CPA-ZH/", ""))
            derived_markdown = str(item.get("derived_markdown") or "")
            if derived_markdown:
                manifest_local_files.add(derived_markdown.replace("\\", "/"))
                manifest_local_files.add(derived_markdown.replace("\\", "/").replace("knowledge-base/CPA-ZH/", ""))
            local_path = resolve_local_file(root, local_file) if local_file else manifest_path
            derived_path = resolve_local_file(root, derived_markdown) if derived_markdown else Path()
            extracted = ""
            if derived_markdown and derived_path.exists():
                extracted = cached_file_text(root, derived_path, text_cache)
            if not extracted and local_path.exists():
                extracted = cached_file_text(root, local_path, text_cache)
            metadata_text = " ".join(
                str(item.get(key, ""))
                for key in [
                    "title",
                    "document_no",
                    "document_type",
                    "official_source",
                    "url",
                    "source_url",
                    "local_file",
                    "derived_markdown",
                    "wiki_page",
                ]
            )
            yield {
                "kind": "raw-manifest",
                "title": clean_title(str(item.get("title") or item.get("slug") or local_path.name)),
                "path": local_file or manifest_path.relative_to(root).as_posix(),
                "source_url": str(item.get("url") or item.get("source_url") or ""),
                "body": normalize_text(metadata_text + " " + extracted),
                "metadata": item,
                "raw_path": local_file,
                "markdown_path": derived_markdown,
                "content_sha256": str(item.get("derived_sha256") or item.get("sha256") or ""),
            }

    for raw_file in sorted((root / "raw").rglob("*")):
        if not raw_file.is_file():
            continue
        rel_path = raw_file.relative_to(root).as_posix()
        if "_archive/" in rel_path or rel_path.startswith("_archive/"):
            continue
        if rel_path in manifest_local_files:
            continue
        if is_search_excluded(rel_path):
            continue
        if raw_file.name in {"metadata.json", "source-url.txt", "manifest.json"}:
            continue
        text = cached_file_text(root, raw_file, text_cache)
        if text:
            metadata = _sidecar_metadata(raw_file)
            yield {
                "kind": "raw-file",
                "title": clean_title(raw_file.stem),
                "path": rel_path,
                "source_url": str(metadata.get("url") or metadata.get("source_url") or ""),
                "body": text,
                "metadata": metadata,
                "raw_path": rel_path,
                "markdown_path": str(metadata.get("derived_markdown") or (rel_path if raw_file.suffix.lower() == ".md" else "")),
                "content_sha256": str(metadata.get("derived_sha256") or metadata.get("sha256") or ""),
            }


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    return connection


def load_classifier(root: Path):
    """Load the repository-level CPA-ZH classification helper when available."""
    tools_dir = Path(__file__).resolve().parent
    if not (tools_dir / "classify_wiki.py").exists():
        return None
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    try:
        import classify_wiki  # type: ignore

        return classify_wiki
    except Exception:
        return None


def classify_document(classifier, document: dict[str, str]) -> tuple[str, str]:
    if classifier is None:
        return "", ""
    try:
        path = document["path"]
        if document["kind"] == "wiki":
            return classifier.classify_wiki(path, {})
        if document["kind"] == "pdf-markdown":
            # cache/pdf-markdown/files 目前全部为审计准则应用指南
            return "audit-standards", "raw-audit"
        prefix = "knowledge-base/CPA-ZH/"
        if path.startswith(prefix):
            path = path[len(prefix):]
        if path.startswith("raw/"):
            return classifier.classify_raw(path)
        return "", ""
    except Exception:
        return "", ""


def build_index(root: Path, db_path: Path) -> None:
    classifier = load_classifier(root)
    kb_tools = root / "tools"
    if str(kb_tools) not in sys.path:
        sys.path.insert(0, str(kb_tools))
    try:
        from kb_common import asset_metadata, page_metadata, parse_frontmatter, section_chunks, is_authoritative_path
    except Exception:
        asset_metadata = page_metadata = parse_frontmatter = section_chunks = is_authoritative_path = None
    connection = connect(db_path)
    connection.executescript(
        """
        DROP TABLE IF EXISTS chunks_fts;
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS documents;
        DROP TABLE IF EXISTS documents_fts;
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY,
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            path TEXT NOT NULL,
            source_url TEXT NOT NULL,
            body TEXT NOT NULL,
            domain TEXT NOT NULL DEFAULT '',
            topic TEXT NOT NULL DEFAULT '',
            page_role TEXT NOT NULL DEFAULT 'reference',
            maturity TEXT NOT NULL DEFAULT 'reviewed',
            answer_ready INTEGER NOT NULL DEFAULT 0,
            authority TEXT NOT NULL DEFAULT 'curated',
            rank_boost REAL NOT NULL DEFAULT 0,
            asset_id TEXT NOT NULL DEFAULT '',
            source_id TEXT NOT NULL DEFAULT '',
            source_type TEXT NOT NULL DEFAULT '',
            knowledge_type TEXT NOT NULL DEFAULT '',
            tags TEXT NOT NULL DEFAULT '',
            authority_level TEXT NOT NULL DEFAULT 'curated',
            version TEXT NOT NULL DEFAULT '',
            published_on TEXT NOT NULL DEFAULT '',
            effective_from TEXT NOT NULL DEFAULT '',
            effective_to TEXT NOT NULL DEFAULT '',
            lifecycle_status TEXT NOT NULL DEFAULT 'valid',
            raw_path TEXT NOT NULL DEFAULT '',
            markdown_path TEXT NOT NULL DEFAULT '',
            content_sha256 TEXT NOT NULL DEFAULT '',
            review_status TEXT NOT NULL DEFAULT '',
            supersedes TEXT NOT NULL DEFAULT '',
            superseded_by TEXT NOT NULL DEFAULT ''
        );
        CREATE VIRTUAL TABLE documents_fts USING fts5(
            title,
            body,
            content='documents',
            content_rowid='id',
            tokenize='trigram'
        );
        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY,
            document_id INTEGER NOT NULL,
            heading TEXT NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            heading,
            body,
            content='chunks',
            content_rowid='id',
            tokenize='trigram'
        );
        CREATE INDEX idx_documents_delivery ON documents(answer_ready, page_role, authority, lifecycle_status);
        CREATE INDEX idx_documents_asset ON documents(asset_id, source_id, version);
        CREATE INDEX idx_documents_dates ON documents(effective_from, effective_to, published_on);
        CREATE INDEX idx_documents_tags ON documents(tags);
        CREATE INDEX idx_chunks_document ON chunks(document_id);
        """
    )
    count = 0
    for document in iter_documents(root):
        domain, topic = classify_document(classifier, document)
        rel_path = document["path"].replace("\\", "/")
        role = "reference"
        maturity = "reviewed"
        answer_ready = False
        authority = "curated"
        chunk_body = document["body"]
        metadata = dict(document.get("metadata") or {})
        if document["kind"] == "wiki" and page_metadata is not None:
            source_text = read_text(root / rel_path)
            frontmatter, chunk_body = parse_frontmatter(source_text)
            page_info = page_metadata(rel_path, source_text)
            metadata = {**frontmatter, **page_info}
            role = str(page_info["page_role"])
            maturity = str(page_info["maturity"])
            answer_ready = bool(page_info["answer_ready"])
            authority = str(page_info["authority"])
            if parse_frontmatter is not None:
                # A curated page can declare a more precise topic than the
                # path-based classifier, especially for cross-domain cases.
                domain = str(frontmatter.get("domain") or domain)
                topic = str(frontmatter.get("topic") or topic)
        elif is_authoritative_path is not None:
            role = str(metadata.get("page_role") or role)
            maturity = str(metadata.get("maturity") or maturity)
            authority = "official" if is_authoritative_path(rel_path, metadata) else str(metadata.get("authority") or "curated")
            explicit_ready = metadata.get("answer_ready")
            if isinstance(explicit_ready, bool):
                answer_ready = explicit_ready
            elif isinstance(explicit_ready, str):
                answer_ready = explicit_ready.lower() == "true"
            else:
                answer_ready = authority == "official"
            domain = str(metadata.get("domain") or domain)
            topic = str(metadata.get("topic") or topic)
        asset = asset_metadata(
            rel_path,
            metadata,
            kind=document["kind"],
            page_role=role,
            domain=domain,
            topic=topic,
            source_url=str(document.get("source_url") or ""),
            raw_path=str(document.get("raw_path") or ""),
            markdown_path=str(document.get("markdown_path") or ""),
            content_sha256=str(document.get("content_sha256") or ""),
            body=source_text if document["kind"] == "wiki" else document["body"],
            answer_ready=answer_ready,
            authority=authority,
        )
        domain = str(asset["domain"])
        topic = str(asset["topic"])
        role = str(asset["page_role"] or role)
        authority = str(asset["authority"] or authority)
        answer_ready = bool(asset["answer_ready"])
        rank_boost = 0.0
        if answer_ready and role in {"knowledge", "case"}:
            rank_boost += 150.0
        elif role == "case":
            rank_boost += 90.0
        elif role == "knowledge":
            rank_boost += 75.0
        if authority == "official":
            rank_boost += 55.0
        if role == "case" and metadata.get("source_scope") == "local-only" and answer_ready:
            # Local workshop cases have no official-authority bonus, but an
            # explicitly Agent-reviewed case should still surface for its
            # concrete scenario instead of losing to generic topic pages.
            rank_boost += 55.0
        if role == "index":
            rank_boost -= 35.0
        if maturity == "skeleton":
            rank_boost -= 60.0
        if asset["lifecycle_status"] in {"superseded", "expired", "historical"}:
            rank_boost -= 120.0
        elif asset["lifecycle_status"] == "enacted-not-effective":
            rank_boost -= 80.0
        cursor = connection.execute(
            "INSERT INTO documents(kind, title, path, source_url, body, domain, topic, page_role, maturity, answer_ready, authority, rank_boost, asset_id, source_id, source_type, knowledge_type, tags, authority_level, version, published_on, effective_from, effective_to, lifecycle_status, raw_path, markdown_path, content_sha256, review_status, supersedes, superseded_by)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                document["kind"],
                document["title"],
                rel_path,
                str(asset["source_url"]),
                document["body"],
                domain,
                topic,
                role,
                maturity,
                int(answer_ready),
                authority,
                rank_boost,
                asset["asset_id"],
                asset["source_id"],
                asset["source_type"],
                asset["knowledge_type"],
                ",".join(asset["tags"]),
                asset["authority_level"],
                asset["version"],
                asset["published_on"],
                asset["effective_from"],
                asset["effective_to"],
                asset["lifecycle_status"],
                asset["raw_path"],
                asset["markdown_path"],
                asset["content_sha256"],
                asset["review_status"],
                asset["supersedes"],
                asset["superseded_by"],
            ),
        )
        row_id = cursor.lastrowid
        connection.execute(
            "INSERT INTO documents_fts(rowid, title, body) VALUES (?, ?, ?)",
            (row_id, document["title"], document["body"]),
        )
        chunks = section_chunks(chunk_body) if section_chunks is not None else [("正文", chunk_body)]
        for heading, chunk_text in chunks:
            if not normalize_text(chunk_text):
                continue
            chunk_cursor = connection.execute(
                "INSERT INTO chunks(document_id, heading, body) VALUES (?, ?, ?)",
                (row_id, heading, normalize_text(chunk_text)),
            )
            connection.execute(
                "INSERT INTO chunks_fts(rowid, heading, body) VALUES (?, ?, ?)",
                (chunk_cursor.lastrowid, heading, normalize_text(chunk_text)),
            )
        count += 1
    connection.commit()
    connection.close()
    print(f"indexed={count}")
    print(f"db={db_path}")


def make_snippet(text: str, query: str, limit: int = 150) -> str:
    text = normalize_text(text)
    index = text.lower().find(query.lower())
    if index == -1:
        terms = [term for term in query.split() if term]
        positions = [text.lower().find(term.lower()) for term in terms]
        positions = [pos for pos in positions if pos != -1]
        index = min(positions) if positions else 0
    start = max(0, index - 45)
    snippet = text[start : start + limit]
    if start > 0:
        snippet = "..." + snippet
    if start + limit < len(text):
        snippet += "..."
    return snippet


def fts_match_query(query: str) -> str:
    """把用户输入转成 FTS5 MATCH 表达式：每个词组加引号，AND 连接。"""
    terms = [term for term in query.split() if term] or [query]
    return " AND ".join('"' + term.replace('"', '""') + '"' for term in terms)


def query_index(db_path: Path, query: str, limit: int) -> int:
    if not db_path.exists():
        print(f"Search index not found: {db_path}", file=sys.stderr)
        print("Run: .\\.venv\\Scripts\\python.exe tools\\kb_search.py index", file=sys.stderr)
        return 2

    connection = sqlite3.connect(db_path)

    # 优先 FTS5 trigram MATCH（要求词长>=3字符；中文3字即3字符）
    if min((len(t) for t in query.split() if t), default=len(query)) >= 3:
        try:
            rows = connection.execute(
                """
                SELECT d.kind, d.title, d.path, d.source_url,
                       snippet(documents_fts, 1, '[', ']', '...', 40) AS snip,
                       bm25(documents_fts) AS score
                FROM documents_fts
                JOIN documents d ON d.id = documents_fts.rowid
                WHERE documents_fts MATCH ?
                ORDER BY score
                LIMIT ?
                """,
                (fts_match_query(query), limit),
            ).fetchall()
            if rows:
                for index, row in enumerate(rows, start=1):
                    kind, title, path, source_url, snip, _score = row
                    print(f"{index}. [{kind}] {title}")
                    print(f"   path: {path}")
                    if source_url:
                        print(f"   url: {source_url}")
                    print(f"   hit: {snip}")
                print(f"results={len(rows)}")
                connection.close()
                return 0
        except sqlite3.OperationalError:
            pass

    like_terms = [term for term in query.split() if term] or [query]
    where = " AND ".join(["(title LIKE ? OR body LIKE ?)" for _ in like_terms])
    score_parts = [
        "CASE WHEN title LIKE ? THEN 50 ELSE 0 END",
        "CASE WHEN body LIKE ? THEN 5 ELSE 0 END",
        "CASE WHEN kind = 'raw-manifest' THEN 8 ELSE 0 END",
    ]
    for _term in like_terms:
        score_parts.append("CASE WHEN title LIKE ? THEN 10 ELSE 0 END")
        score_parts.append("CASE WHEN body LIKE ? THEN 1 ELSE 0 END")
    score_expr = " + ".join(score_parts)

    score_params: list[str] = [f"%{query}%", f"%{query}%"]
    for term in like_terms:
        score_params.extend([f"%{term}%", f"%{term}%"])

    params: list[str | int] = []
    for term in like_terms:
        params.extend([f"%{term}%", f"%{term}%"])
    params.append(limit)
    rows = connection.execute(
        f"""
        SELECT kind, title, path, source_url, body,
               ({score_expr}) AS score
        FROM documents
        WHERE {where}
        ORDER BY score DESC, length(body) ASC
        LIMIT ?
        """,
        score_params + params,
    ).fetchall()

    if not rows:
        try:
            rows = connection.execute(
                """
                SELECT d.kind, d.title, d.path, d.source_url, d.body, bm25(documents_fts) AS score
                FROM documents_fts
                JOIN documents d ON d.id = documents_fts.rowid
                WHERE documents_fts MATCH ?
                ORDER BY score
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []

    for index, row in enumerate(rows, start=1):
        kind, title, path, source_url, body, _score = row
        print(f"{index}. [{kind}] {title}")
        print(f"   path: {path}")
        if source_url:
            print(f"   url: {source_url}")
        print(f"   hit: {make_snippet(body, query)}")

    print(f"results={len(rows)}")
    connection.close()
    return 0


def stats(db_path: Path) -> int:
    if not db_path.exists():
        print(f"Search index not found: {db_path}", file=sys.stderr)
        return 2
    connection = sqlite3.connect(db_path)
    rows = connection.execute("SELECT kind, COUNT(*) FROM documents GROUP BY kind ORDER BY kind").fetchall()
    for kind, count in rows:
        print(f"{kind}\t{count}")
    total = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    print(f"total\t{total}")
    connection.close()
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Build and query the CPA-ZH local search index.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--db", default="", help="SQLite search database path.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("index", help="Rebuild the local search index.")
    query_parser = subparsers.add_parser("query", help="Search the local index.")
    query_parser.add_argument("query")
    query_parser.add_argument("--limit", type=int, default=10)
    subparsers.add_parser("stats", help="Show indexed document counts.")

    args = parser.parse_args()
    root = Path(args.root).resolve()
    db_path = Path(args.db).resolve() if args.db else root / "search" / "kb_search.sqlite"

    if args.command == "index":
        build_index(root, db_path)
        return 0
    if args.command == "query":
        return query_index(db_path, args.query, args.limit)
    if args.command == "stats":
        return stats(db_path)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
