"""JSON CLI for the shared CPA-ZH Agent service."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

try:
    from cpa_zh_agent_service import AgentServiceError, CpaZhAgentService
except ModuleNotFoundError:
    from tools.cpa_zh_agent_service import AgentServiceError, CpaZhAgentService


def envelope(
    operation: str,
    *,
    ok: bool,
    data: Any = None,
    preview_token: str = "",
    expires_at: int | None = None,
    warnings: list[str] | None = None,
    error_code: str = "",
    message: str = "",
) -> dict[str, Any]:
    return {
        "ok": ok,
        "operation": operation,
        "data": data,
        "preview_token": preview_token,
        "expires_at": expires_at,
        "warnings": warnings or [],
        "error_code": error_code,
        "message": message,
    }


def emit(payload: dict[str, Any]) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise AgentServiceError("invalid_arguments", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description="Structured CPA-ZH Agent CLI")
    parser.add_argument("--root", default=os.environ.get("CPA_ZH_ROOT", "knowledge-base/CPA-ZH"))
    parser.add_argument(
        "--preview-root",
        default=os.environ.get("CPA_ZH_AGENT_PREVIEW_ROOT", "workspace/tmp/cpa-zh-agent-previews"),
    )
    sub = parser.add_subparsers(dest="operation", required=True)

    search = sub.add_parser("search")
    search.add_argument("query", nargs="?")
    search.add_argument("--query", dest="query_option", default="")
    search.add_argument("--kind", choices=["", "wiki", "raw"], default="")
    search.add_argument("--domain", default="")
    search.add_argument("--limit", type=int, default=10)

    read_page = sub.add_parser("read-page")
    read_page.add_argument("path")
    read_raw = sub.add_parser("read-raw")
    read_raw.add_argument("path")
    sub.add_parser("health")
    sub.add_parser("pending-reviews")
    detail = sub.add_parser("review-detail")
    detail.add_argument("path")

    ingest = sub.add_parser("ingest-preview")
    ingest.add_argument("--source-path", required=True)
    ingest.add_argument("--raw-subdir", required=True)
    ingest.add_argument("--batch-slug", required=True)
    ingest.add_argument("--title", default="")
    ingest.add_argument("--source-type", default="local-source")
    ingest.add_argument("--official-source", default="本地资料")
    ingest.add_argument("--official-url", default="")
    ingest.add_argument("--tags", default="")

    qa = sub.add_parser("qa-preview")
    qa.add_argument("--question", required=True)
    qa.add_argument("--answer", required=True)
    qa.add_argument("--slug", default="")
    qa.add_argument("--title", default="")
    qa.add_argument("--source", default="local-qa-log")
    qa.add_argument("--tags", default="")
    qa.add_argument("--related", default="")

    case = sub.add_parser("case-preview")
    case.add_argument("--source-path", required=True)
    case.add_argument("--slug", default="")
    case.add_argument("--title", default="")
    case.add_argument("--source-id", default="local-case-batch")
    case.add_argument("--raw-path", default="")
    case.add_argument("--tags", default="")
    case.add_argument("--related", default="")

    review = sub.add_parser("review-preview")
    review.add_argument("path")
    review.add_argument("--content-sha256", default="")
    commit = sub.add_parser("commit")
    commit.add_argument("preview_token")
    commit.add_argument("--confirmed", action="store_true")
    return parser


def main() -> int:
    operation = "unknown"
    try:
        args = build_parser().parse_args()
        operation = str(args.operation)
        service = CpaZhAgentService(args.root, preview_root=args.preview_root)
        if operation == "search":
            result = service.search(args.query_option or args.query or "", kind=args.kind, domain=args.domain, limit=args.limit)
        elif operation == "read-page":
            result = service.read_page(args.path)
        elif operation == "read-raw":
            result = service.read_raw(args.path)
        elif operation == "health":
            result = service.health()
        elif operation == "pending-reviews":
            result = service.pending_reviews()
        elif operation == "review-detail":
            result = service.review_detail(args.path)
        elif operation == "ingest-preview":
            result = service.ingest_preview(args.source_path, args.raw_subdir, args.batch_slug, title=args.title, source_type=args.source_type, official_source=args.official_source, official_url=args.official_url, tags=args.tags)
        elif operation == "qa-preview":
            result = service.qa_preview(args.question, args.answer, slug=args.slug, title=args.title, source=args.source, tags=args.tags, related=args.related)
        elif operation == "case-preview":
            result = service.case_preview(args.source_path, slug=args.slug, title=args.title, source_id=args.source_id, raw_path=args.raw_path, tags=args.tags, related=args.related)
        elif operation == "review-preview":
            result = service.review_preview(args.path, args.content_sha256)
        elif operation == "commit":
            result = service.commit(args.preview_token, confirmed=args.confirmed)
        else:
            raise AgentServiceError("unsupported_operation", f"Unsupported operation: {operation}")
        preview_token = str(result.pop("preview_token", "")) if isinstance(result, dict) else ""
        expires_at = result.pop("expires_at", None) if isinstance(result, dict) else None
        warnings = result.pop("warnings", []) if isinstance(result, dict) else []
        message = result.pop("message", "") if isinstance(result, dict) else ""
        response_data = result.get("data") if preview_token and isinstance(result, dict) else result
        emit(envelope(operation, ok=True, data=response_data, preview_token=preview_token, expires_at=expires_at, warnings=warnings, message=message))
        return 0
    except AgentServiceError as error:
        emit(envelope(operation, ok=False, data=error.details or None, error_code=error.code, message=error.message))
        return 2
    except Exception as error:
        emit(envelope(operation, ok=False, error_code="internal_error", message=str(error)))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
