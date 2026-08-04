from __future__ import annotations

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    kind: str
    title: str
    path: str
    source_url: str = ""
    domain: str = ""
    topic: str = ""
    snippet: str = ""
    page_role: str = ""
    maturity: str = ""
    answer_ready: bool = False


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    facets: list[tuple[str, int]]
    kinds: dict[str, int]
    engine: str


class Backlink(BaseModel):
    path: str
    title: str


class DocumentResponse(BaseModel):
    path: str
    frontmatter: dict[str, str]
    markdown: str
    backlinks: list[Backlink]


class BacklinksResponse(BaseModel):
    path: str
    backlinks: list[Backlink]


class SummaryResponse(BaseModel):
    kinds: dict[str, int]
    roles: dict[str, int]
    maturity: dict[str, int]
    answer_ready: int
    total: int
    wiki_pages: int
    backlink_targets: int


class HealthResponse(BaseModel):
    status: str
    index_ready: bool
    wiki_pages: int
    backlink_targets: int


class AnswerRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    topic: str = Field(default="", max_length=100)


class AnswerCitation(BaseModel):
    path: str
    title: str
    excerpt: str
    source_url: str = ""
    maturity: str = ""
    authority: str = ""
    answer_ready: bool = False


class AnswerResponse(BaseModel):
    answer: str = ""
    citations: list[AnswerCitation]
    confidence: str
    insufficient_evidence: bool
