"""Start the loopback-only CPA-ZH maintenance API."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    port = os.environ.get("KB_MAINTENANCE_PORT", "8766")
    raise SystemExit(subprocess.call([sys.executable, "-m", "uvicorn", "tools.kb_maintenance_api:app", "--host", "127.0.0.1", "--port", port], cwd=ROOT))
