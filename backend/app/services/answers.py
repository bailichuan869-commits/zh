from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from fastapi import HTTPException

from app.core.ai_config import load_ai_config
from app.core.config import DEMO_MODE, OPENAI_ANSWER_MODEL
from app.services.library import library_service

MAX_CITATIONS = 8
MAX_EXCERPT = 900

# Keep older browser clients that posted display labels compatible with the
# canonical topics stored in the search index.
TOPIC_ALIASES = {
    "收入确认": "revenue-recognition",
    "租赁": "leases",
    "金融工具": "financial-instruments",
    "长期股权投资与合并": "consolidation",
    "合并": "consolidation",
    "现金流量表": "cash-flow",
    "现金流量与列报": "cash-flow",
}


def _excerpt(body: str, question: str) -> str:
    body = " ".join(body.split())
    terms = [term for term in question.split() if term]
    position = min((body.find(term) for term in terms if body.find(term) >= 0), default=0)
    start = max(0, position - 160)
    return body[start : start + MAX_EXCERPT]


def _response_text(data: object) -> str:
    if not isinstance(data, dict):
        return ""
    direct = data.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    fragments: list[str] = []
    for output in data.get("output", []):
        if not isinstance(output, dict):
            continue
        for content in output.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str) and text.strip():
                    fragments.append(text.strip())
    return "\n".join(fragments)


class AnswerService:
    def retrieve_evidence(
        self,
        question: str,
        topic: str = "",
        *,
        profile: str = "answer-current",
        as_of: str = "",
        depth: str = "standard",
    ) -> dict[str, Any]:
        normalized_topic = TOPIC_ALIASES.get(topic.strip(), topic.strip())
        limit = 12 if depth == "deep" else MAX_CITATIONS
        return library_service.search(
            question,
            topic=normalized_topic,
            profile=profile,
            as_of=as_of,
            limit=limit,
        )

    def evidence(
        self,
        question: str,
        topic: str,
        *,
        profile: str = "answer-current",
        as_of: str = "",
        depth: str = "standard",
    ) -> list[dict[str, Any]]:
        return self._citation_items(self.retrieve_evidence(question, topic, profile=profile, as_of=as_of, depth=depth))

    @staticmethod
    def _citation_items(retrieval: dict[str, Any]) -> list[dict[str, Any]]:
        citations: list[dict[str, Any]] = []
        for item in retrieval.get("results", []):
            citations.append({
                "path": item["path"],
                "title": item["title"],
                "excerpt": item.get("snippet", ""),
                "source_url": item.get("source_url", ""),
                "maturity": item.get("maturity", ""),
                "authority": item.get("authority", ""),
                "answer_ready": bool(item.get("answer_ready")),
                "asset_id": item.get("asset_id", ""),
                "source_id": item.get("source_id", ""),
                "source_type": item.get("source_type", ""),
                "version": item.get("version", ""),
                "published_on": item.get("published_on", ""),
                "effective_from": item.get("effective_from", ""),
                "effective_to": item.get("effective_to", ""),
                "lifecycle_status": item.get("lifecycle_status", ""),
                "raw_path": item.get("raw_path", ""),
                "markdown_path": item.get("markdown_path", ""),
                "content_sha256": item.get("content_sha256", ""),
                "review_status": item.get("review_status", ""),
                "section": item.get("section", ""),
                "section_anchor": item.get("section_anchor", ""),
                "score": item.get("score", 0.0),
                "retrieval_path": item.get("retrieval_path", ""),
            })
        return citations

    def answer(
        self,
        question: str,
        topic: str = "",
        *,
        profile: str = "answer-current",
        as_of: str = "",
        depth: str = "standard",
    ) -> dict[str, Any]:
        retrieval = self.retrieve_evidence(question, topic, profile=profile, as_of=as_of, depth=depth)
        citations = self._citation_items(retrieval)
        risk_flags: list[str] = []
        if not citations:
            risk_flags.append("no-matching-evidence")
        if any(not item["source_url"] for item in citations):
            risk_flags.append("citation-source-url-missing")
        if any(not item["section"] for item in citations):
            risk_flags.append("citation-section-missing")
        if DEMO_MODE and citations:
            return {
                "answer": f"开发模拟答复：根据本地检索到的资料，建议沿着适用准则、事实条件和判断边界逐项核验。相关依据见 [1]。问题：{question}",
                "citations": citations,
                "confidence": "demo",
                "insufficient_evidence": False,
                "profile": profile,
                "as_of": as_of,
                "depth": depth,
                "retrieval_trace": retrieval.get("retrieval_trace", {}),
                "risk_flags": risk_flags,
            }
        has_reviewed_knowledge = any(
            citation["answer_ready"] and citation["path"].startswith("wiki/")
            for citation in citations
        )
        if not has_reviewed_knowledge:
            risk_flags.append("reviewed-wiki-evidence-missing")
            return {
                "answer": "现有已复核资料不足以形成可引用答复。以下仅列出可继续核验的资料。",
                "citations": citations,
                "confidence": "insufficient",
                "insufficient_evidence": True,
                "profile": profile,
                "as_of": as_of,
                "depth": depth,
                "retrieval_trace": retrieval.get("retrieval_trace", {}),
                "risk_flags": risk_flags,
            }
        saved_config = load_ai_config()
        use_saved_config = bool(saved_config["enabled"] and saved_config["api_key"])
        api_key = str(saved_config["api_key"]) if use_saved_config else os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise HTTPException(503, "答疑服务尚未配置 OPENAI_API_KEY")
        model = str(saved_config["model"]) if use_saved_config else OPENAI_ANSWER_MODEL
        base_url = str(saved_config["base_url"]) if use_saved_config else "https://api.openai.com/v1"
        evidence_text = "\n\n".join(
            f"[{index + 1}] {item['title']} ({item['path']}#{item['section_anchor']})\n"
            f"版本={item['version'] or '未声明'}，生效={item['effective_from'] or '未声明'}至{item['effective_to'] or '未声明'}，"
            f"来源={item['source_url'] or '未声明'}\n{item['excerpt']}"
            for index, item in enumerate(citations)
        )
        prompt = (
            "你是中国注册会计师知识库的答疑助手。只可基于提供的证据回答；"
            "证据不足时明确说明，不得补充外部事实。用中文作答，简洁说明判断路径和边界，"
            "并在相关句末使用 [编号] 引用。\n\n问题：" + question + "\n\n证据：\n" + evidence_text
        )
        payload = json.dumps({"model": model, "input": prompt}).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url.rstrip('/')}/responses", data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise HTTPException(502, "答疑模型服务请求失败") from error
        except (urllib.error.URLError, TimeoutError):
            raise HTTPException(503, "答疑模型服务暂时不可用") from None
        text = _response_text(data)
        if not text:
            raise HTTPException(502, "答疑模型未返回可用文本")
        return {
            "answer": text,
            "citations": citations,
            "confidence": "source-backed",
            "insufficient_evidence": False,
            "profile": profile,
            "as_of": as_of,
            "depth": depth,
            "retrieval_trace": retrieval.get("retrieval_trace", {}),
            "risk_flags": risk_flags,
        }


answer_service = AnswerService()
