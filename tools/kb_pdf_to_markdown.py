from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import kb_search


EXTRACTION_ENGINES = ["pymupdf", "pdfplumber", "pdfminer", "pypdf"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "-", value).strip(" .-_")
    value = re.sub(r"\s+", "-", value)
    return value[:90] or "pdf"


def source_digest(root: Path, path: Path) -> str:
    return hashlib.sha256(rel(root, path).encode("utf-8")).hexdigest()[:12]


def resolve_source(root: Path, source: str) -> Path:
    path = Path(source)
    if path.is_absolute():
        return path.resolve()
    candidates = [
        (Path.cwd() / path).resolve(),
        (root / path).resolve(),
        (root.parent / path).resolve(),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def iter_pdfs(source: Path) -> list[Path]:
    if source.is_file():
        return [source] if source.suffix.lower() == ".pdf" else []
    if source.is_dir():
        return sorted(path for path in source.rglob("*.pdf") if path.is_file())
    return []


def markdown_path(root: Path, output_dir: Path, source_pdf: Path) -> Path:
    stem = slugify(source_pdf.stem)
    digest = source_digest(root, source_pdf)
    return output_dir / f"{stem}-{digest}.md"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\ufeff", "")).strip()


def extract_with_pymupdf(path: Path) -> str:
    import fitz  # type: ignore

    document = fitz.open(str(path))
    try:
        return normalize_text("\n".join(page.get_text("text") for page in document))
    finally:
        document.close()


def extract_with_pdfplumber(path: Path) -> str:
    import pdfplumber  # type: ignore

    with pdfplumber.open(str(path)) as pdf:
        return normalize_text("\n".join(page.extract_text() or "" for page in pdf.pages))


def extract_with_pdfminer(path: Path) -> str:
    from pdfminer.high_level import extract_text  # type: ignore

    return normalize_text(extract_text(str(path)) or "")


def extract_with_pypdf(path: Path) -> str:
    return kb_search.extract_file_text(path)


def text_quality(text: str) -> str:
    if not text:
        return "empty"
    length = len(text)
    replacement_ratio = text.count("\ufffd") / max(length, 1)
    cjk_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    cjk_ratio = cjk_count / max(length, 1)
    mojibake_markers = text.count("��") + text.count("ҵ��") + text.count("̽��")
    if replacement_ratio > 0.01 or mojibake_markers >= 3:
        return "garbled"
    if cjk_ratio < 0.01 and re.search(r"[A-Za-z]", text) and length > 500:
        return "suspect"
    return "ok"


def quality_rank(quality: str) -> int:
    return {"ok": 3, "suspect": 2, "garbled": 1, "empty": 0}.get(quality, 0)


def extract_pdf_best(path: Path, preferred: str = "auto") -> tuple[str, str, str]:
    extractors = {
        "pymupdf": extract_with_pymupdf,
        "pdfplumber": extract_with_pdfplumber,
        "pdfminer": extract_with_pdfminer,
        "pypdf": extract_with_pypdf,
    }
    engine_order = EXTRACTION_ENGINES if preferred == "auto" else [preferred]
    attempts: list[tuple[str, str, str]] = []
    for engine in engine_order:
        extractor = extractors.get(engine)
        if not extractor:
            continue
        try:
            text = extractor(path)
        except Exception:
            text = ""
        quality = text_quality(text)
        attempts.append((engine, text, quality))
        if preferred != "auto":
            return text, engine, quality
        if quality == "ok":
            return text, engine, quality
    if not attempts:
        return "", preferred, "empty"
    best_engine, best_text, best_quality = max(attempts, key=lambda item: (quality_rank(item[2]), len(item[1])))
    return best_text, best_engine, best_quality


def render_markdown(root: Path, source_pdf: Path, text: str, title: str, extraction_method: str, quality: str) -> str:
    source_rel = rel(root, source_pdf)
    return "\n".join(
        [
            "---",
            f"title: {title}",
            "type: extracted-text",
            "source_type: pdf-markdown",
            f"created: {date.today().isoformat()}",
            f"updated: {date.today().isoformat()}",
            f"source_pdf: {source_rel}",
            f"source_sha256: {sha256_file(source_pdf)}",
            f"extraction_method: {extraction_method}",
            f"text_quality: {quality}",
            f"text_length: {len(text)}",
            f"ocr_status: {'review_required' if quality in {'garbled', 'suspect'} else 'not_required'}",
            "tags: [pdf, markdown, extracted-text]",
            "---",
            "",
            f"# {title}",
            "",
            f"> 来源 PDF：`{source_rel}`",
            "",
            "## 抽取正文",
            "",
            text,
            "",
        ]
    )


def load_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    if isinstance(data, list):
        return data
    return []


def write_manifest(path: Path, items: list[dict[str, Any]]) -> None:
    manifest = {
        "schema": "cpa-zh-pdf-markdown-v1",
        "generated_at": utc_now(),
        "items": items,
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight_write(root: Path, converted: list[dict[str, Any]], pending: list[dict[str, Any]], manifest_path: Path, overwrite: bool) -> int:
    if overwrite:
        return 0

    for item in converted:
        path = root / item["markdown_path"]
        if path.exists():
            print(f"output exists; use --overwrite if intended: {path}", file=sys.stderr)
            return 2

    existing = load_manifest(manifest_path)
    existing_keys = {str(item.get("source_pdf")) for item in existing}
    new_keys = {str(item.get("source_pdf")) for item in [*converted, *pending]}
    if existing_keys.intersection(new_keys):
        print(f"manifest already has one or more source PDFs; use --overwrite if intended: {manifest_path}", file=sys.stderr)
        return 2
    return 0


def build_items(root: Path, pdfs: list[Path], output_dir: Path, engine: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    converted: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    for pdf in pdfs:
        text, extraction_method, quality = extract_pdf_best(pdf, preferred=engine)
        out_path = markdown_path(root, output_dir, pdf)
        base_item: dict[str, Any] = {
            "source_pdf": rel(root, pdf),
            "source_sha256": sha256_file(pdf),
            "bytes": pdf.stat().st_size,
            "title": pdf.stem,
            "text_length": len(text),
            "text_quality": quality,
        }
        if text:
            converted.append(
                {
                    **base_item,
                    "markdown_path": rel(root, out_path),
                    "extraction_method": extraction_method,
                    "ocr_status": "review_required" if quality in {"garbled", "suspect"} else "not_required",
                    "_text": text,
                }
            )
        else:
            pending.append(
                {
                    **base_item,
                    "markdown_path": "",
                    "extraction_method": extraction_method,
                    "ocr_status": "pending",
                    "action": "ocr-required",
                }
            )
    return converted, pending


def render_pending_report(root: Path, pending: list[dict[str, Any]]) -> str:
    lines = [
        "# PDF OCR 待处理清单",
        "",
        "本清单由 `tools/kb_pdf_to_markdown.py` 生成。列出的 PDF 使用当前本地抽取器未取得正文，需要后续使用 OCR 工具、文档解析 API 或手工补正文。",
        "",
        "| PDF | 字节数 | SHA256 | 状态 |",
        "|---|---:|---|---|",
    ]
    if not pending:
        lines.append("| 无 |  |  |  |")
    else:
        for item in pending:
            lines.append(
                f"| `{item['source_pdf']}` | {item['bytes']} | `{str(item['source_sha256'])[:16]}` | `{item['ocr_status']}` |"
            )
    lines.extend(["", f"_生成日期：{date.today().isoformat()}_", ""])
    return "\n".join(lines)


def print_plan(source: Path, output_dir: Path, converted: list[dict[str, Any]], pending: list[dict[str, Any]], commit: bool) -> None:
    print(f"mode={'commit' if commit else 'dry-run'}")
    print(f"source={source}")
    print(f"output_dir={output_dir}")
    print(f"pdfs={len(converted) + len(pending)}")
    print(f"convertible={len(converted)}")
    print(f"ocr_pending={len(pending)}")
    quality_counts: dict[str, int] = {}
    for item in converted:
        quality = str(item.get("text_quality") or "unknown")
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    for quality, count in sorted(quality_counts.items()):
        print(f"text_quality_{quality}={count}")
    for item in converted[:10]:
        print(
            f"convert: {item['source_pdf']} -> {item['markdown_path']} "
            f"engine={item['extraction_method']} quality={item.get('text_quality')} chars={item['text_length']}"
        )
    if len(converted) > 10:
        print(f"convert_more={len(converted) - 10}")
    for item in pending[:10]:
        print(f"pending_ocr: {item['source_pdf']}")
    if len(pending) > 10:
        print(f"pending_more={len(pending) - 10}")
    if not commit:
        print()
        print("Dry run only. Re-run with --commit to write Markdown files and manifest.")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Convert text-based PDF files into Markdown and flag OCR-needed PDFs.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--source", required=True, help="PDF file or directory containing PDFs.")
    parser.add_argument(
        "--output-subdir",
        default="cache/pdf-markdown/files",
        help="Output directory under the knowledge base root.",
    )
    parser.add_argument("--commit", action="store_true", help="Actually write Markdown files and manifest.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing Markdown files.")
    parser.add_argument(
        "--engine",
        default="auto",
        choices=["auto", *EXTRACTION_ENGINES],
        help="Extraction engine. Default auto tries pymupdf, pdfplumber, pdfminer, then pypdf.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source = resolve_source(root, args.source)
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 2

    output_subdir = Path(args.output_subdir)
    if output_subdir.is_absolute() or ".." in output_subdir.parts:
        print("--output-subdir must be a safe relative path under the knowledge base root.", file=sys.stderr)
        return 2
    output_dir = root / output_subdir

    pdfs = iter_pdfs(source)
    converted, pending = build_items(root, pdfs, output_dir, args.engine)
    print_plan(source, output_dir, converted, pending, args.commit)
    if not args.commit:
        return 0

    manifest_path = output_dir.parent / "manifest.json"
    preflight_status = preflight_write(root, converted, pending, manifest_path, args.overwrite)
    if preflight_status:
        return preflight_status

    output_dir.mkdir(parents=True, exist_ok=True)
    for item in converted:
        path = root / item["markdown_path"]
        path.write_text(
            render_markdown(
                root,
                source if source.is_file() else (root / item["source_pdf"]),
                item["_text"],
                item["title"],
                str(item["extraction_method"]),
                str(item.get("text_quality") or "unknown"),
            ),
            encoding="utf-8",
            newline="\n",
        )
        item.pop("_text", None)

    existing = load_manifest(manifest_path) if args.overwrite else []
    new_items = [{key: value for key, value in item.items() if not key.startswith("_")} for item in [*converted, *pending]]
    merged = [item for item in existing if str(item.get("source_pdf")) not in {str(new.get("source_pdf")) for new in new_items}]
    merged.extend(new_items)
    write_manifest(manifest_path, merged)
    (output_dir.parent / "ocr-pending.md").write_text(render_pending_report(root, pending), encoding="utf-8", newline="\n")

    print()
    print(f"written_markdown={len(converted)}")
    print(f"manifest={manifest_path}")
    print(f"ocr_pending_report={output_dir.parent / 'ocr-pending.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
