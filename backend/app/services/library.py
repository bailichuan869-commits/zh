from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from app.core.config import KB_ROOT
from app.core.files import read_text
from app.repositories.search import get_connection

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    values: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            values[key.strip()] = value.strip().strip("\"'")
    return values, text[end + 4 :].lstrip("\n")


def normalize_link(link: str) -> str:
    link = link.strip().replace("\\", "/")
    if link.startswith("wiki/"):
        link = link[5:]
    return link.removesuffix(".md")


class LibraryService:
    def __init__(self) -> None:
        self.backlinks: dict[str, list[dict[str, str]]] = {}
        self.titles: dict[str, str] = {}

    def build_backlinks(self) -> None:
        self.backlinks.clear()
        self.titles.clear()
        pages: list[tuple[str, str, str]] = []
        for page in sorted((KB_ROOT / "wiki").rglob("*.md")):
            if "_trash" in page.parts or "_maintenance" in page.parts:
                continue
            key = page.relative_to(KB_ROOT / "wiki").as_posix()[:-3]
            frontmatter, _ = parse_frontmatter(read_text(page))
            title = frontmatter.get("title") or page.stem
            self.titles[key] = title
            pages.append((key, title, read_text(page)))
        for source, title, text in pages:
            for match in WIKILINK_RE.finditer(text):
                target = normalize_link(match.group(1))
                if target.startswith("raw/") or target == source:
                    continue
                bucket = self.backlinks.setdefault(target, [])
                if not any(item["path"] == source for item in bucket):
                    bucket.append({"path": source, "title": title})

    def search(self, q: str, domain: str, kind: str, limit: int, offset: int) -> dict:
        query = q.strip()
        if not query:
            return {"results": [], "total": 0, "facets": [], "kinds": {"wiki": 0, "raw": 0}, "engine": "like"}
        conditions: list[str] = []
        params: list[str] = []
        if domain:
            conditions.append("d.domain = ?")
            params.append(domain)
        if kind == "wiki":
            conditions.append("d.kind = 'wiki'")
        elif kind == "raw":
            conditions.append("d.kind != 'wiki'")
        extra = (" AND " + " AND ".join(conditions)) if conditions else ""
        connection = get_connection()
        try:
            rows: list[tuple] = []
            fts = min((len(term) for term in query.split() if term), default=len(query)) >= 3
            if fts:
                expression = " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in query.split() if term)
                try:
                    rows = connection.execute(f"""
                        SELECT d.kind, d.title, d.path, d.source_url, d.domain, d.topic,
                               snippet(documents_fts, 1, '<mark>', '</mark>', '...', 40),
                               d.page_role, d.maturity, d.answer_ready
                        FROM documents_fts JOIN documents d ON d.id = documents_fts.rowid
                        WHERE documents_fts MATCH ?{extra}
                        ORDER BY bm25(documents_fts, 8.0, 1.0) - d.rank_boost
                    """, [expression, *params]).fetchall()
                except sqlite3.OperationalError:
                    rows = []
            if not rows:
                like = f"%{query}%"
                rows = connection.execute(f"""
                    SELECT d.kind, d.title, d.path, d.source_url, d.domain, d.topic,
                           substr(d.body, max(1, instr(lower(d.body), lower(?)) - 40), 160),
                           d.page_role, d.maturity, d.answer_ready
                    FROM documents d WHERE (d.title LIKE ? OR d.body LIKE ?){extra}
                    ORDER BY CASE WHEN d.title LIKE ? THEN 0 ELSE 1 END, d.rank_boost DESC
                """, [query, like, like, *params, like]).fetchall()
            facets: dict[str, int] = {}
            kinds = {"wiki": 0, "raw": 0}
            for row in rows:
                facets[row[4]] = facets.get(row[4], 0) + 1
                kinds["wiki" if row[0] == "wiki" else "raw"] += 1
            return {
                "results": [{"kind": row[0], "title": row[1], "path": row[2], "source_url": row[3] or "", "domain": row[4] or "", "topic": row[5] or "", "snippet": row[6] or "", "page_role": row[7] or "", "maturity": row[8] or "", "answer_ready": bool(row[9])} for row in rows[offset:offset + limit]],
                "total": len(rows), "facets": sorted(facets.items(), key=lambda item: -item[1]), "kinds": kinds,
                "engine": "fts5-trigram" if fts and rows else "like",
            }
        finally:
            connection.close()

    def summary(self) -> dict:
        connection = get_connection()
        try:
            kinds = dict(connection.execute("SELECT kind, COUNT(*) FROM documents GROUP BY kind"))
            roles = dict(connection.execute("SELECT page_role, COUNT(*) FROM documents GROUP BY page_role"))
            maturity = dict(connection.execute("SELECT maturity, COUNT(*) FROM documents GROUP BY maturity"))
            answer_ready = connection.execute("SELECT COUNT(*) FROM documents WHERE answer_ready = 1").fetchone()[0]
            return {"kinds": kinds, "roles": roles, "maturity": maturity, "answer_ready": answer_ready, "total": sum(kinds.values()), "wiki_pages": len(self.titles), "backlink_targets": len(self.backlinks)}
        finally:
            connection.close()


library_service = LibraryService()
