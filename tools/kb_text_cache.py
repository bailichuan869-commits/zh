from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import kb_search


SKIP_NAMES = {"metadata.json", "source-url.txt", "manifest.json"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_name(raw_rel_path: str) -> str:
    digest = hashlib.sha256(raw_rel_path.encode("utf-8")).hexdigest()
    return f"{digest[:2]}/{digest}.txt"


def cache_paths(root: Path, raw_rel_path: str) -> tuple[Path, str]:
    cache_rel = f"cache/text/files/{cache_name(raw_rel_path)}"
    return root / cache_rel, cache_rel


def iter_raw_files(root: Path) -> Iterable[Path]:
    raw_root = root / "raw"
    for path in sorted(raw_root.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        yield path


def load_existing_manifest(manifest_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        return {}
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = data.get("items", []) if isinstance(data, dict) else []
    return {str(item.get("raw_path")): item for item in items if item.get("raw_path")}


def build(root: Path, force: bool = False) -> dict[str, int]:
    cache_root = root / "cache" / "text"
    manifest_path = cache_root / "manifest.json"
    existing = load_existing_manifest(manifest_path)

    items: list[dict[str, Any]] = []
    stats = {
        "files_seen": 0,
        "cached": 0,
        "updated": 0,
        "unchanged": 0,
        "empty": 0,
        "errors": 0,
    }

    for raw_file in iter_raw_files(root):
        stats["files_seen"] += 1
        raw_rel_path = rel(root, raw_file)
        file_stat = raw_file.stat()
        cache_file, cache_rel_path = cache_paths(root, raw_rel_path)
        old = existing.get(raw_rel_path, {})
        should_reuse = (
            not force
            and cache_file.exists()
            and old.get("mtime_ns") == file_stat.st_mtime_ns
            and old.get("bytes") == file_stat.st_size
        )

        if should_reuse:
            text_length = int(old.get("text_length") or 0)
            text_sha256 = str(old.get("text_sha256") or "")
            source_sha256 = str(old.get("sha256") or "")
            stats["unchanged"] += 1
        else:
            try:
                text = kb_search.extract_file_text(raw_file)
                text_length = len(text)
                text_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
                source_sha256 = sha256_file(raw_file)
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(text, encoding="utf-8", newline="\n")
                stats["updated"] += 1
                if not text:
                    stats["empty"] += 1
            except Exception as exc:
                stats["errors"] += 1
                text_length = 0
                text_sha256 = ""
                source_sha256 = ""
                cache_file = root / cache_rel_path
                print(f"ERROR {raw_rel_path}: {exc}", file=sys.stderr)

        if text_length:
            stats["cached"] += 1

        items.append(
            {
                "raw_path": raw_rel_path,
                "cache_path": cache_rel_path,
                "sha256": source_sha256,
                "mtime_ns": file_stat.st_mtime_ns,
                "bytes": file_stat.st_size,
                "text_length": text_length,
                "text_sha256": text_sha256,
            }
        )

    manifest = {
        "schema": "cpa-zh-text-cache-v1",
        "generated_at": utc_now(),
        "root": root.as_posix(),
        "items": items,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return stats


def stats(root: Path) -> int:
    manifest_path = root / "cache" / "text" / "manifest.json"
    if not manifest_path.exists():
        print(f"missing={manifest_path}")
        return 2
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = data.get("items", [])
    cached = sum(1 for item in items if int(item.get("text_length") or 0) > 0)
    empty = len(items) - cached
    total_chars = sum(int(item.get("text_length") or 0) for item in items)
    print(f"schema={data.get('schema', '')}")
    print(f"generated_at={data.get('generated_at', '')}")
    print(f"items={len(items)}")
    print(f"cached={cached}")
    print(f"empty={empty}")
    print(f"text_chars={total_chars}")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Build or inspect CPA-ZH raw text cache.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build", help="Build the raw text cache.")
    build_parser.add_argument("--force", action="store_true", help="Refresh all cache entries.")
    subparsers.add_parser("stats", help="Show text cache statistics.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.command == "build":
        result = build(root, force=args.force)
        for key, value in result.items():
            print(f"{key}={value}")
        print(f"manifest={root / 'cache' / 'text' / 'manifest.json'}")
        return 1 if result["errors"] else 0
    if args.command == "stats":
        return stats(root)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
