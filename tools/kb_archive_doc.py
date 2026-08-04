from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


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


def resolve_source(source: str) -> Path:
    return Path(source).resolve()


def official_filename(source: Path) -> str:
    suffix = source.suffix.lower()
    return f"official{suffix or '.bin'}"


def infer_content_type(path: Path, override: str = "") -> str:
    if override:
        return override
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def infer_text_status(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm", ".md", ".txt", ".csv", ".json", ".xml"}:
        return "text"
    if suffix == ".pdf":
        return "pending_text_cache"
    if suffix in {".docx", ".doc"}:
        return "office_document"
    return "unknown"


def infer_ocr_status(path: Path, override: str = "") -> str:
    if override:
        return override
    return "pending" if path.suffix.lower() == ".pdf" else "not_required"


def load_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    raise ValueError(f"Unsupported manifest shape: {path}")


def manifest_item(args: argparse.Namespace, root: Path, source: Path, local_path: Path) -> dict[str, Any]:
    item: dict[str, Any] = {
        "slug": args.slug,
        "title": args.title or source.stem,
        "document_no": args.document_no,
        "url": args.official_url,
        "official_source": args.official_source,
        "wiki_page": args.wiki_page,
        "archived_on": args.archived_on,
        "content_type": infer_content_type(source, args.content_type),
        "bytes": source.stat().st_size,
        "sha256": sha256_file(source),
        "local_file": rel(root, local_path),
        "official_page_status": args.official_page_status,
        "text_extraction_status": args.text_extraction_status or infer_text_status(source),
        "ocr_status": infer_ocr_status(source, args.ocr_status),
    }
    if args.source_note:
        item["source_note"] = args.source_note
    if args.attachment_url:
        item["attachment_url"] = args.attachment_url
    return item


def write_json(path: Path, data: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_plan(args: argparse.Namespace, root: Path, source: Path, item_dir: Path, local_path: Path, manifest_path: Path) -> None:
    print(f"mode={'commit' if args.commit else 'dry-run'}")
    print(f"root={root}")
    print(f"source={source}")
    print(f"target={item_dir}")
    print(f"local_file={rel(root, local_path)}")
    print(f"manifest={manifest_path}")
    print(f"title={args.title or source.stem}")
    print(f"document_no={args.document_no}")
    print(f"official_url={args.official_url or 'not-provided'}")
    print(f"bytes={source.stat().st_size}")
    print(f"sha256={sha256_file(source)}")
    if not args.commit:
        print()
        print("Dry run only. Re-run with --commit to copy the document and write manifest/metadata/source-url.")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Archive one official/local source document into CPA-ZH raw.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--source", required=True, help="Local source file to archive.")
    parser.add_argument("--raw-subdir", required=True, help="Target manifest directory under raw/.")
    parser.add_argument("--slug", required=True, help="Item slug directory.")
    parser.add_argument("--title", required=True, help="Document title.")
    parser.add_argument("--document-no", default="", help="Document number.")
    parser.add_argument("--official-url", default="", help="Official page URL.")
    parser.add_argument("--attachment-url", default="", help="Official attachment URL when different from page URL.")
    parser.add_argument("--official-source", default="本地资料", help="Official/source label.")
    parser.add_argument("--official-page-status", default="local", help="verified/local/pending/etc.")
    parser.add_argument("--wiki-page", default="", help="Wiki page to link the item to.")
    parser.add_argument("--source-note", default="", help="Source note.")
    parser.add_argument("--content-type", default="", help="Override content type.")
    parser.add_argument("--text-extraction-status", default="", help="Override text extraction status.")
    parser.add_argument("--ocr-status", default="", help="Override OCR status.")
    parser.add_argument("--archived-on", default=date.today().isoformat(), help="Archive date.")
    parser.add_argument("--append", action="store_true", help="Append to existing manifest.")
    parser.add_argument("--commit", action="store_true", help="Actually write files.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source = resolve_source(args.source)
    if not source.exists() or not source.is_file():
        print(f"source file not found: {source}", file=sys.stderr)
        return 2

    raw_subdir = Path(args.raw_subdir)
    if raw_subdir.is_absolute() or ".." in raw_subdir.parts:
        print("--raw-subdir must be a safe relative path under raw/", file=sys.stderr)
        return 2

    batch_dir = root / "raw" / raw_subdir
    item_dir = batch_dir / args.slug
    local_path = item_dir / official_filename(source)
    manifest_path = batch_dir / "manifest.json"

    print_plan(args, root, source, item_dir, local_path, manifest_path)
    if not args.commit:
        return 0

    if item_dir.exists():
        print(f"item directory already exists: {item_dir}", file=sys.stderr)
        return 2
    if manifest_path.exists() and not args.append:
        print(f"manifest already exists; use --append if intended: {manifest_path}", file=sys.stderr)
        return 2

    batch_dir.mkdir(parents=True, exist_ok=True)
    item_dir.mkdir(parents=True)
    shutil.copy2(source, local_path)

    existing_items = load_manifest(manifest_path)
    item = manifest_item(args, root, source, local_path)
    manifest = {
        "schema": "cpa-zh-archive-doc-v1",
        "generated_at": utc_now(),
        "items": [*existing_items, item],
    }
    write_json(manifest_path, manifest)
    write_json(item_dir / "metadata.json", {**item, "metadata_schema": "cpa-zh-archive-doc-v1"})
    (item_dir / "source-url.txt").write_text((args.official_url or str(source)) + "\n", encoding="utf-8")
    print()
    print(f"written={item_dir}")
    print(f"manifest_items={len(existing_items) + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
