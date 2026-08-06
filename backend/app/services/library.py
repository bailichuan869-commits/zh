from __future__ import annotations

import re
import sqlite3
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from app.core.config import KB_ROOT
from app.core.files import read_text
from app.repositories.search import get_connection
from app.services.retrieval import asset_for_path, retrieve

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]*))?(?:\|[^\]]*)?\]\]")


class _SnippetTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_snippet(value: str) -> str:
    parser = _SnippetTextExtractor()
    parser.feed(value)
    parser.close()
    return "".join(parser.parts)


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
        self.direct_backlinks: dict[str, set[str]] = {}
        self.titles: dict[str, str] = {}
        self.wiki_page_count = 0

    def build_backlinks(self) -> None:
        self.backlinks.clear()
        self.direct_backlinks.clear()
        self.titles.clear()
        self.wiki_page_count = 0
        pages: list[tuple[str, str, str]] = []
        for page in sorted((KB_ROOT / "wiki").rglob("*.md")):
            if "_trash" in page.parts:
                continue
            self.wiki_page_count += 1
            if "_maintenance" in page.parts:
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
                if match.group(2) is None:
                    self.direct_backlinks.setdefault(target, set()).add(source)

    def search(
        self,
        q: str,
        domain: str = "",
        kind: str = "",
        limit: int = 30,
        offset: int = 0,
        *,
        profile: str = "general-search",
        as_of: str = "",
        status: str = "",
        source_type: str = "",
        tag: str = "",
        topic: str = "",
    ) -> dict[str, Any]:
        if not q.strip():
            return {
                "results": [],
                "total": 0,
                "facets": [],
                "kinds": {"wiki": 0, "raw": 0},
                "engine": "chunks-fts5",
                "profile": profile or "general-search",
                "retrieval_trace": {"profile": profile or "general-search", "matched_assets": 0},
            }
        return retrieve(
            q,
            profile=profile,
            domain=domain,
            kind=kind,
            topic=topic,
            limit=limit,
            offset=offset,
            as_of=as_of,
            status=status,
            source_type=source_type,
            tag=tag,
        )

    def asset(self, path: str) -> dict[str, Any]:
        return asset_for_path(path)

    def summary(self) -> dict:
        connection = get_connection()
        try:
            kinds = dict(connection.execute("SELECT kind, COUNT(*) FROM documents GROUP BY kind"))
            roles = dict(connection.execute("SELECT page_role, COUNT(*) FROM documents GROUP BY page_role"))
            maturity = dict(connection.execute("SELECT maturity, COUNT(*) FROM documents GROUP BY maturity"))
            answer_ready = connection.execute("SELECT COUNT(*) FROM documents WHERE answer_ready = 1").fetchone()[0]
            return {"kinds": kinds, "roles": roles, "maturity": maturity, "answer_ready": answer_ready, "total": sum(kinds.values()), "wiki_pages": self.wiki_page_count, "backlink_targets": len(self.backlinks)}
        finally:
            connection.close()


library_service = LibraryService()
