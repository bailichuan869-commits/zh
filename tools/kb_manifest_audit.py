from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    raise ValueError(f"Unsupported manifest shape: {path}")


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_local_file(root: Path, local_file: str) -> Path:
    path = Path(local_file)
    if path.is_absolute():
        return path

    candidates = [
        root / path,
        Path.cwd() / path,
        root.parent / path,
        root.parents[1] / path if len(root.parents) > 1 else root / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def audit_manifest(root: Path, manifest_path: Path) -> list[str]:
    issues: list[str] = []
    items = load_manifest(manifest_path)
    manifest_dir = manifest_path.parent

    slugs = [str(item.get("slug", "")).strip() for item in items]
    filenames = [str(item.get("filename", "")).strip() for item in items]
    slug_manifest = any(slugs)
    batch_file_manifest = not slug_manifest and all(filenames)

    if slug_manifest:
        for slug, count in Counter(slugs).items():
            if not slug:
                issues.append(f"{rel(root, manifest_path)} has item without slug")
            elif count > 1:
                issues.append(f"{rel(root, manifest_path)} duplicate slug: {slug}")
    elif batch_file_manifest:
        for filename, count in Counter(filenames).items():
            if count > 1:
                issues.append(f"{rel(root, manifest_path)} duplicate filename: {filename}")
    else:
        issues.append(f"{rel(root, manifest_path)} has neither slug items nor filename batch items")

    if slug_manifest:
        manifest_slugs = {slug for slug in slugs if slug}
        dir_slugs = {p.name for p in manifest_dir.iterdir() if p.is_dir()}
        for slug in sorted(dir_slugs - manifest_slugs):
            issues.append(f"{rel(root, manifest_path)} extra directory not in manifest: {slug}")
        for slug in sorted(manifest_slugs - dir_slugs):
            issues.append(f"{rel(root, manifest_path)} manifest item missing directory: {slug}")

    for item in items:
        item_id = str(item.get("slug") or item.get("filename") or "<unknown>").strip()
        local_file = str(item.get("local_file", "")).strip()
        if not local_file:
            issues.append(f"{rel(root, manifest_path)} {item_id}: missing local_file")
            continue
        local_path = resolve_local_file(root, local_file)
        if not local_path.exists():
            issues.append(f"{rel(root, manifest_path)} {item_id}: local_file does not exist: {local_file}")
            continue
        expected_bytes = item.get("bytes")
        if isinstance(expected_bytes, int):
            actual_bytes = local_path.stat().st_size
            if actual_bytes != expected_bytes:
                issues.append(
                    f"{rel(root, manifest_path)} {item_id}: byte mismatch "
                    f"manifest={expected_bytes} actual={actual_bytes}"
                )

        if slug_manifest:
            slug = str(item.get("slug", "")).strip()
            metadata_path = manifest_dir / slug / "metadata.json"
            if not metadata_path.exists():
                issues.append(f"{rel(root, manifest_path)} {slug}: missing metadata.json")
            else:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                metadata_file = str(metadata.get("local_file", "")).strip()
                if metadata_file and metadata_file != local_file:
                    issues.append(
                        f"{rel(root, manifest_path)} {slug}: metadata local_file differs "
                        f"metadata={metadata_file} manifest={local_file}"
                    )

            source_url_path = manifest_dir / slug / "source-url.txt"
            if not source_url_path.exists():
                issues.append(f"{rel(root, manifest_path)} {slug}: missing source-url.txt")

    return issues


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Audit CPA-ZH raw manifest consistency.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    raw_root = root / "raw"
    manifests = sorted(raw_root.rglob("manifest.json"))
    all_issues: list[str] = []

    print(f"root={root}")
    print(f"manifests={len(manifests)}")
    for manifest_path in manifests:
        items = load_manifest(manifest_path)
        issues = audit_manifest(root, manifest_path)
        all_issues.extend(issues)
        print(f"- {rel(root, manifest_path)} items={len(items)} issues={len(issues)}")

    if all_issues:
        print("\nIssues:")
        for issue in all_issues:
            print(f"- {issue}")
        return 1

    print("\nManifest audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
