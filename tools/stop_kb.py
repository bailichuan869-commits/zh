"""Stop the local CPA-ZH knowledge-base web server.

The starter writes a PID file under workspace/tmp/kb_server.pid. This helper first
tries that PID, then falls back to processes listening on KB_PORT, default 8765.
"""
from __future__ import annotations

import os
import socket
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "workspace" / "tmp"
PORT = int(os.environ.get("KB_PORT", "8765"))


def port_alive() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.settimeout(1.0)
        return handle.connect_ex(("127.0.0.1", PORT)) == 0


def pids_on_port(port: int) -> list[str]:
    output = subprocess.run(["netstat", "-ano"], capture_output=True).stdout.decode(
        "utf-8", errors="replace"
    )
    pids: list[str] = []
    for line in output.splitlines():
        if f":{port}" in line and "LISTENING" in line:
            parts = line.split()
            if parts and parts[-1].isdigit() and parts[-1] not in pids:
                pids.append(parts[-1])
    return pids


def command_line_for_pid(pid: str) -> str:
    script = f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="replace")


def is_kb_backend_pid(pid: str) -> bool:
    command_line = command_line_for_pid(pid).lower()
    return "app.main:app" in command_line and "backend" in command_line


def kill_pid(pid: str) -> bool:
    if not is_kb_backend_pid(pid):
        return False
    result = subprocess.run(["taskkill", "/pid", pid, "/f"], capture_output=True)
    return result.returncode == 0


def main() -> int:
    stopped: list[str] = []

    for pid in pids_on_port(PORT):
        if pid not in stopped and kill_pid(pid):
            stopped.append(pid)

    for _ in range(10):
        if not port_alive():
            break
        time.sleep(0.5)

    if stopped:
        print(f"Stopped CPA-ZH server process(es): {', '.join(stopped)}")
    elif port_alive():
        print(f"Port {PORT} is still occupied, but no CPA-ZH backend process was identified.")
        print("Check the process manually before stopping it.")
        return 1
    else:
        print(f"CPA-ZH server is not running on port {PORT}.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
