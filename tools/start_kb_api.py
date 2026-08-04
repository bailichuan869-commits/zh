"""Start the separated CPA-ZH FastAPI backend on the local loopback interface."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
PORT = os.environ.get("KB_PORT", "8765")


def main() -> int:
    if not BACKEND.exists():
        print(f"[ERROR] Backend directory not found: {BACKEND}")
        return 1
    command = [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", str(BACKEND), "--host", "127.0.0.1", "--port", PORT]
    print(f"CPA-ZH API: http://127.0.0.1:{PORT}/api/docs")
    print("The Vue frontend is a separate process; run npm run dev in frontend.")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
