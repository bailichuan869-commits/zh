from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Import a local batch of case files into CPA-ZH raw/cases.")
    parser.add_argument("source_dir", help="Local directory containing case files.")
    parser.add_argument(
        "--batch",
        default="2026-07-first-issue",
        help="Destination batch directory under knowledge-base/CPA-ZH/raw/cases.",
    )
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    root = Path(args.root).resolve()
    dest_dir = root / "raw" / "cases" / args.batch

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"source directory not found: {source_dir}", file=sys.stderr)
        return 2

    dest_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in source_dir.iterdir() if path.is_file())
    manifest = []

    for source_file in files:
        dest_file = dest_dir / source_file.name
        shutil.copy2(source_file, dest_file)
        manifest.append(
            {
                "filename": source_file.name,
                "title": source_file.stem,
                "case_batch": args.batch,
                "source_local_path": str(source_file),
                "local_file": str(dest_file.relative_to(root)).replace("\\", "/"),
                "imported_on": date.today().isoformat(),
                "bytes": dest_file.stat().st_size,
                "sha256": sha256(dest_file),
                "document_type": source_file.suffix.lower().lstrip(".") or "unknown",
                "status": "raw-imported",
            }
        )

    (dest_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"source={source_dir}")
    print(f"destination={dest_dir}")
    print(f"imported={len(manifest)}")
    for item in manifest:
        print(f"- {item['filename']} {item['bytes']} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
