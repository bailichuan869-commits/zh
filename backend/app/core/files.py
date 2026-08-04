from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException

from app.core.config import KB_ROOT


def safe_resolve(relative_path: str, *, allowed_prefix: str | None = None) -> Path:
    if not relative_path or relative_path.startswith(("/", "\\")) or ":" in relative_path:
        raise HTTPException(400, "非法路径")
    normalized = relative_path.replace("\\", "/")
    target = (KB_ROOT / normalized).resolve()
    allowed_root = (KB_ROOT / allowed_prefix).resolve() if allowed_prefix else KB_ROOT.resolve()
    try:
        target.relative_to(allowed_root)
    except ValueError:
        raise HTTPException(400, "非法路径") from None
    return target


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")
