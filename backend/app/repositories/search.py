from __future__ import annotations

import sqlite3

from fastapi import HTTPException

from app.core.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise HTTPException(503, "搜索索引不存在，请先运行 tools/kb.py index")
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
