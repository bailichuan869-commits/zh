"""Retire temporary accounting-standard unmapped bucket pages.

The unmapped CSV and ``unmapped-review.md`` are the review queue. Bucket pages
were only a derived grouping view and must not be treated as formal knowledge
pages. This compatibility entry point removes stale bucket pages so older
maintenance commands cannot recreate the navigation noise.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
CSV_PATH = KB / "raw" / "indexes" / "enterprise-accounting-standards-unmapped-review.csv"
OUT_DIR = KB / "wiki" / "concepts" / "accounting-standards" / "calibration"
LEGACY_CONCEPT_TYPES = {
    "accounting-standard-calibration-bucket",
    "accounting-standard-calibration-index",
}


def read_rows() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def remove_legacy_pages() -> int:
    """Remove only pages created by the retired bucket-page generator."""
    if not OUT_DIR.exists():
        return 0
    removed = 0
    for path in sorted(OUT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        if any(f"concept_type: {value}" in text for value in LEGACY_CONCEPT_TYPES):
            path.unlink()
            removed += 1
    try:
        OUT_DIR.rmdir()
    except OSError:
        pass
    return removed


def main() -> None:
    rows = read_rows()
    removed = remove_legacy_pages()
    print(
        "bucket_pages=0 "
        f"removed_legacy_pages={removed} "
        f"review_rows={len(rows)} "
        "review_page=wiki/concepts/accounting-standards/unmapped-review.md"
    )


if __name__ == "__main__":
    main()
