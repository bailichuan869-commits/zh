from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


SKIP_NAMES = {"manifest.json", "metadata.json", "source-url.txt"}


@dataclass
class PlannedItem:
    source_path: Path
    slug: str
    title: str
    filename: str
    item_dir: Path
    local_path: Path
    local_file: str
    bytes: int
    sha256: str
    derived_markdown_source: Path | None = None
    derived_markdown_path: Path | None = None


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


def slugify(value: str, fallback: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def unique_slug(base: str, used: set[str]) -> str:
    candidate = base
    counter = 2
    while candidate in used:
        candidate = f"{base}-{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def iter_source_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]
    if not source.is_dir():
        raise FileNotFoundError(f"source not found: {source}")
    files: list[Path] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        files.append(path)
    return files


def load_existing_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    raise ValueError(f"Unsupported manifest shape: {path}")


def document_type(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "file"


def text_extraction_status(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".csv", ".json", ".html", ".htm"}:
        return "text"
    if suffix in {".docx", ".doc"}:
        return "office_document"
    if suffix == ".pdf":
        return "pdf_pending_cache"
    return "unknown"


def ocr_status(path: Path) -> str:
    return "pending" if path.suffix.lower() == ".pdf" else "not_required"


def plan_items(*, root: Path, source: Path, batch_dir: Path, existing_items: list[dict[str, Any]]) -> list[PlannedItem]:
    used_slugs = {str(item.get("slug")) for item in existing_items if item.get("slug")}
    planned: list[PlannedItem] = []
    for index, source_path in enumerate(iter_source_files(source), start=1):
        digest = sha256_file(source_path)
        fallback = f"item-{index:03d}-{digest[:8]}"
        base_slug = slugify(source_path.stem, fallback)
        slug = unique_slug(base_slug, used_slugs)
        item_dir = batch_dir / slug
        local_path = item_dir / source_path.name
        planned.append(
            PlannedItem(
                source_path=source_path,
                slug=slug,
                title=source_path.stem,
                filename=source_path.name,
                item_dir=item_dir,
                local_path=local_path,
                local_file=rel(root, local_path),
                bytes=source_path.stat().st_size,
                sha256=digest,
            )
        )
    return planned


def manifest_item(
    *,
    item: PlannedItem,
    args: argparse.Namespace,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "slug": item.slug,
        "filename": item.filename,
        "title": item.title,
        "source_type": args.source_type,
        "source_local_path": args.source_label or str(item.source_path),
        "local_file": item.local_file,
        "imported_on": args.imported_on,
        "bytes": item.bytes,
        "sha256": item.sha256,
        "document_type": document_type(item.source_path),
        "official_source": args.official_source,
        "official_page_status": args.official_page_status,
        "text_extraction_status": text_extraction_status(item.source_path),
        "ocr_status": ocr_status(item.source_path),
        "status": "raw-imported",
    }
    if args.document_no:
        data["document_no"] = args.document_no
    if args.official_url:
        data["url"] = args.official_url
    if args.wiki_page:
        data["wiki_page"] = args.wiki_page
    if args.tags:
        data["tags"] = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if item.derived_markdown_path:
        data["derived_markdown"] = item.local_file.rsplit("/", 1)[0] + "/" + item.derived_markdown_path.name
        data["text_extraction_status"] = "extracted-markdown"
    return data


def metadata_for_item(item: PlannedItem, manifest_item_data: dict[str, Any]) -> dict[str, Any]:
    metadata = dict(manifest_item_data)
    metadata["metadata_schema"] = "cpa-zh-local-ingest-v1"
    return metadata


def render_source_page(*, args: argparse.Namespace, root: Path, batch_dir: Path, manifest_rel: str, item_count: int) -> str:
    today = date.today().isoformat()
    source_title = args.title or args.batch_slug
    lines = [
        "---",
        f"title: {source_title}",
        "type: source",
        "source_type: local-ingest-batch",
        f"created: {today}",
        f"updated: {today}",
        f"raw_path: {rel(root, batch_dir)}/",
        "tags: [local-ingest, raw-archive, automation]",
        "related: [[concepts/ai-coding-project-roadmap]], [[concepts/ai-coding-tool-template-library]]",
        "---",
        "",
        f"# {source_title}",
        "",
        "本页由 `tools/kb.py ingest-local` 生成，用于记录一次本地资料入库批次。",
        "",
        "## 归档信息",
        "",
        "| 项目 | 内容 |",
        "|---|---|",
        f"| 来源路径 | `{args.source}` |",
        f"| 本地归档 | `{rel(root, batch_dir)}/` |",
        f"| manifest | `{manifest_rel}` |",
        f"| 文件数量 | {item_count} |",
        f"| 来源类型 | `{args.source_type}` |",
        f"| 官方来源 | {args.official_source} |",
        f"| 官方链接 | {args.official_url or '不适用或待补充'} |",
        "",
        "## 后续处理",
        "",
        "1. 核对 manifest、metadata 和 source-url 是否完整。",
        "2. 运行 `tools/kb.py manifest` 和 `tools/kb.py sources summary`。",
        "3. 需要检索正文时运行 `tools/kb.py cache build` 和 `tools/kb.py index`。",
        "4. 按资料性质生成或更新对应 wiki/concepts、wiki/sources 或 wiki/cases 页面。",
    ]
    return "\n".join(lines) + "\n"


def write_batch(*, root: Path, batch_dir: Path, manifest_path: Path, existing_items: list[dict[str, Any]], planned: list[PlannedItem], args: argparse.Namespace) -> None:
    if batch_dir.exists() and not args.append:
        raise FileExistsError(f"target batch already exists; use --append if intended: {batch_dir}")
    batch_dir.mkdir(parents=True, exist_ok=True)

    new_manifest_items: list[dict[str, Any]] = []
    for item in planned:
        if item.item_dir.exists():
            raise FileExistsError(f"item directory already exists: {item.item_dir}")
        item.item_dir.mkdir(parents=True)
        shutil.copy2(item.source_path, item.local_path)
        if item.derived_markdown_source and item.derived_markdown_path:
            shutil.copy2(item.derived_markdown_source, item.derived_markdown_path)
        item_data = manifest_item(item=item, args=args)
        new_manifest_items.append(item_data)
        (item.item_dir / "metadata.json").write_text(
            json.dumps(metadata_for_item(item, item_data), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        source_url = args.official_url or str(item.source_path)
        (item.item_dir / "source-url.txt").write_text(source_url + "\n", encoding="utf-8")

    manifest = {
        "schema": "cpa-zh-local-ingest-v1",
        "generated_at": utc_now(),
        "batch_slug": args.batch_slug,
        "title": args.title or args.batch_slug,
        "source": args.source_label or str(args.source),
        "items": [*existing_items, *new_manifest_items],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.source_page:
        source_page_path = root / "wiki" / "sources" / f"{args.source_page}.md"
        if source_page_path.exists() and not args.append:
            raise FileExistsError(f"source page already exists; use --append if intended: {source_page_path}")
        source_page_path.parent.mkdir(parents=True, exist_ok=True)
        source_page_path.write_text(
            render_source_page(
                args=args,
                root=root,
                batch_dir=batch_dir,
                manifest_rel=rel(root, manifest_path),
                item_count=len([*existing_items, *new_manifest_items]),
            ),
            encoding="utf-8",
            newline="\n",
        )


def print_plan(root: Path, batch_dir: Path, manifest_path: Path, planned: list[PlannedItem], args: argparse.Namespace) -> None:
    print(f"mode={'commit' if args.commit else 'dry-run'}")
    print(f"root={root}")
    print(f"source={args.source}")
    print(f"target={batch_dir}")
    print(f"manifest={manifest_path}")
    print(f"items={len(planned)}")
    for item in planned:
        print(f"- {item.source_path} -> {item.local_file} bytes={item.bytes} sha256={item.sha256[:12]}")
        if item.derived_markdown_source and item.derived_markdown_path:
            print(f"  markdown: {item.derived_markdown_source} -> {rel(root, item.derived_markdown_path)}")
    if not args.commit:
        print()
        print("Dry run only. Re-run with --commit to copy files and write manifest/metadata/source-url.")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Ingest local files into CPA-ZH raw archive.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--source", required=True, help="Local file or directory to ingest.")
    parser.add_argument("--raw-subdir", required=True, help="Target subdirectory under raw/, for example cases/new-batch.")
    parser.add_argument("--batch-slug", required=True, help="Batch slug used in manifest metadata.")
    parser.add_argument("--title", default="", help="Human-readable batch title.")
    parser.add_argument("--source-type", default="local-source", help="Source type stored in manifest.")
    parser.add_argument("--official-source", default="本地资料", help="Official/source label.")
    parser.add_argument("--official-url", default="", help="Official URL when available.")
    parser.add_argument("--official-page-status", default="local", help="official_page_status value.")
    parser.add_argument("--document-no", default="", help="Document number when all files share one.")
    parser.add_argument("--wiki-page", default="", help="Wiki page to link manifest items to.")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument("--source-page", default="", help="Optional wiki/sources page slug to create.")
    parser.add_argument("--source-label", default="", help="Portable source label stored instead of the local path.")
    parser.add_argument("--imported-on", default=date.today().isoformat(), help="Import date.")
    parser.add_argument("--append", action="store_true", help="Append to an existing batch manifest.")
    parser.add_argument("--derived-markdown", default="", help="Extracted Markdown for a single source file.")
    parser.add_argument("--commit", action="store_true", help="Actually copy files and write metadata.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source = Path(args.source).resolve()
    args.source = str(source)
    raw_subdir = Path(args.raw_subdir)
    if raw_subdir.is_absolute() or ".." in raw_subdir.parts:
        print("--raw-subdir must be a safe relative path under raw/", file=sys.stderr)
        return 2
    batch_dir = root / "raw" / raw_subdir
    manifest_path = batch_dir / "manifest.json"
    existing_items = load_existing_manifest(manifest_path) if manifest_path.exists() else []
    planned = plan_items(root=root, source=source, batch_dir=batch_dir, existing_items=existing_items)
    if args.derived_markdown:
        derived_source = Path(args.derived_markdown).resolve()
        if not source.is_file() or len(planned) != 1:
            print("--derived-markdown requires --source to be one file", file=sys.stderr)
            return 2
        if not derived_source.is_file() or derived_source.suffix.lower() != ".md":
            print("--derived-markdown must point to an existing Markdown file", file=sys.stderr)
            return 2
        planned[0].derived_markdown_source = derived_source
        planned[0].derived_markdown_path = planned[0].item_dir / "extracted.md"
    print_plan(root, batch_dir, manifest_path, planned, args)
    if args.commit:
        write_batch(
            root=root,
            batch_dir=batch_dir,
            manifest_path=manifest_path,
            existing_items=existing_items,
            planned=planned,
            args=args,
        )
        print()
        print(f"written={batch_dir}")
        print(f"manifest_items={len(existing_items) + len(planned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
