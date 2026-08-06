from __future__ import annotations

from typing import Any, Literal

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
    asset_id: str = ""
    source_id: str = ""
    source_type: str = ""
    knowledge_type: str = ""
    tags: list[str] = Field(default_factory=list)
    authority: str = ""
    authority_level: str = ""
    version: str = ""
    published_on: str = ""
    effective_from: str = ""
    effective_to: str = ""
    lifecycle_status: str = ""
    raw_path: str = ""
    markdown_path: str = ""
    content_sha256: str = ""
    review_status: str = ""
    section: str = ""
    section_anchor: str = ""
    score: float = 0.0
    retrieval_path: str = ""


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    facets: list[tuple[str, int]]
    kinds: dict[str, int]
    engine: str
    profile: str = "general-search"
    retrieval_trace: dict[str, Any] = Field(default_factory=dict)


class Backlink(BaseModel):
    path: str
    title: str


class DocumentResponse(BaseModel):
    path: str
    frontmatter: dict[str, str]
    markdown: str
    backlinks: list[Backlink]
    asset: dict[str, Any] = Field(default_factory=dict)


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
    profile: str = Field(default="answer-current", max_length=50)
    as_of: str = Field(default="", max_length=10)
    depth: Literal["standard", "deep"] = "standard"


class AnswerCitation(BaseModel):
    path: str
    title: str
    excerpt: str
    source_url: str = ""
    maturity: str = ""
    authority: str = ""
    answer_ready: bool = False
    asset_id: str = ""
    source_id: str = ""
    source_type: str = ""
    version: str = ""
    published_on: str = ""
    effective_from: str = ""
    effective_to: str = ""
    lifecycle_status: str = ""
    raw_path: str = ""
    markdown_path: str = ""
    content_sha256: str = ""
    review_status: str = ""
    section: str = ""
    section_anchor: str = ""
    score: float = 0.0
    retrieval_path: str = ""


class AnswerResponse(BaseModel):
    answer: str = ""
    citations: list[AnswerCitation]
    confidence: str
    insufficient_evidence: bool
    profile: str = "answer-current"
    as_of: str = ""
    depth: str = "standard"
    retrieval_trace: dict[str, Any] = Field(default_factory=dict)
    risk_flags: list[str] = Field(default_factory=list)
