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


def extract_pdf(path: Path) -> str:
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
    candidates = [
        root / path,
        Path.cwd() / path,
        root.parent / path,
        root.parents[1] / path if len(root.parents) > 1 else root / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def iter_documents(root: Path) -> Iterable[dict[str, str]]:
    text_cache = load_text_cache_manifest(root)

    wiki_root = root / "wiki"
    for md in sorted(wiki_root.rglob("*.md")):
        text = read_text(md)
        yield {
            "kind": "wiki",
            "title": frontmatter_title(text, md.stem),
            "path": md.relative_to(root).as_posix(),
            "source_url": "",
            "body": normalize_text(text),
        }

    manifest_files = sorted((root / "raw").rglob("manifest.json"))
    manifest_local_files: set[str] = set()
    for manifest_path in manifest_files:
        for item in load_manifest(manifest_path):
            local_file = str(item.get("local_file") or "")
            if local_file:
                manifest_local_files.add(local_file.replace("\\", "/"))
            local_path = resolve_local_file(root, local_file) if local_file else manifest_path
            extracted = cached_file_text(root, local_path, text_cache) if local_path.exists() else ""
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
                    "wiki_page",
                ]
            )
            yield {
                "kind": "raw-manifest",
                "title": str(item.get("title") or item.get("slug") or local_path.name),
                "path": local_file or manifest_path.relative_to(root).as_posix(),
                "source_url": str(item.get("url") or item.get("source_url") or ""),
                "body": normalize_text(metadata_text + " " + extracted),
            }

    for raw_file in sorted((root / "raw").rglob("*")):
        if not raw_file.is_file():
            continue
        rel_path = raw_file.relative_to(root).as_posix()
        if rel_path in manifest_local_files:
            continue
        if raw_file.name in {"metadata.json", "source-url.txt", "manifest.json"}:
            continue
        text = cached_file_text(root, raw_file, text_cache)
        if text:
            yield {
                "kind": "raw-file",
                "title": raw_file.stem,
                "path": rel_path,
                "source_url": "",
                "body": text,
            }


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    return connection


def build_index(root: Path, db_path: Path) -> None:
    connection = connect(db_path)
    connection.executescript(
        """
        DROP TABLE IF EXISTS documents;
        DROP TABLE IF EXISTS documents_fts;
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY,
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            path TEXT NOT NULL,
            source_url TEXT NOT NULL,
            body TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE documents_fts USING fts5(
            title,
            body,
            content='documents',
            content_rowid='id'
        );
        """
    )
    count = 0
    for document in iter_documents(root):
        cursor = connection.execute(
            "INSERT INTO documents(kind, title, path, source_url, body) VALUES (?, ?, ?, ?, ?)",
            (
                document["kind"],
                document["title"],
                document["path"],
                document["source_url"],
                document["body"],
            ),
        )
        row_id = cursor.lastrowid
        connection.execute(
            "INSERT INTO documents_fts(rowid, title, body) VALUES (?, ?, ?)",
            (row_id, document["title"], document["body"]),
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


def query_index(db_path: Path, query: str, limit: int) -> int:
    if not db_path.exists():
        print(f"Search index not found: {db_path}", file=sys.stderr)
        print("Run: .\\.venv\\Scripts\\python.exe tools\\kb_search.py index", file=sys.stderr)
        return 2

    connection = sqlite3.connect(db_path)
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
