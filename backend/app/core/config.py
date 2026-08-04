from __future__ import annotations

import os
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(os.environ.get("CPA_ZH_PROJECT_ROOT", str(BACKEND_ROOT.parent))).resolve()
KB_ROOT = Path(os.environ.get("CPA_ZH_ROOT", str(PROJECT_ROOT / "knowledge-base" / "CPA-ZH"))).resolve()
DB_PATH = KB_ROOT / "search" / "kb_search.sqlite"
CATEGORIES_PATH = KB_ROOT / "search" / "navigation-tree.json"
ALLOWED_ORIGINS = tuple(
    origin.strip()
    for origin in os.environ.get("CPA_ZH_WEB_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",")
    if origin.strip()
)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_ANSWER_MODEL = os.environ.get("CPA_ZH_ANSWER_MODEL", "gpt-4.1-mini")
DEMO_MODE = os.environ.get("CPA_ZH_DEMO_MODE", "0") == "1"
