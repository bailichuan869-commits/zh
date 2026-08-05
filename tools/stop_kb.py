"""Stop the local CPA-ZH knowledge-base web services."""
from __future__ import annotations

import json
import os
import socket
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "workspace" / "tmp"
PORT = int(os.environ.get("KB_PORT", "8765"))
FRONTEND_PORT = int(os.environ.get("KB_FRONTEND_PORT", "5173"))
STATE_FILE = TMP / "kb_web_launch.json"


def port_alive(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.settimeout(1.0)
        return handle.connect_ex(("127.0.0.1", port)) == 0


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


def is_kb_frontend_pid(pid: str) -> bool:
    command_line = command_line_for_pid(pid).lower()
    return "vite" in command_line and str(FRONTEND_PORT) in command_line


def load_state() -> dict[str, dict[str, int]]:
    if not STATE_FILE.exists():
        return {}
    try:
        payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    state: dict[str, dict[str, int]] = {}
    for key in ("backend", "frontend"):
        entry = payload.get(key)
        if isinstance(entry, dict) and isinstance(entry.get("pid"), int):
            state[key] = {"pid": int(entry["pid"])}
    return state


def kill_pid(pid: str, predicate) -> bool:
    if not predicate(pid):
        return False
    result = subprocess.run(["taskkill", "/pid", pid, "/t", "/f"], capture_output=True)
    return result.returncode == 0


def kill_from_state(name: str, predicate) -> list[str]:
    stopped: list[str] = []
    state = load_state()
    entry = state.get(name)
    if not entry:
        return stopped
    pid = str(entry["pid"])
    if kill_pid(pid, predicate):
        stopped.append(pid)
    return stopped


def stop_port(port: int, predicate) -> list[str]:
    stopped: list[str] = []
    for pid in pids_on_port(port):
        if pid not in stopped and kill_pid(pid, predicate):
            stopped.append(pid)
    return stopped


def clear_state() -> None:
    STATE_FILE.unlink(missing_ok=True)


def main() -> int:
    stopped: list[str] = []

    for name, predicate in (("frontend", is_kb_frontend_pid), ("backend", is_kb_backend_pid)):
        for pid in kill_from_state(name, predicate):
            if pid not in stopped:
                stopped.append(pid)

    for pid in stop_port(FRONTEND_PORT, is_kb_frontend_pid):
        if pid not in stopped:
            stopped.append(pid)

    for pid in stop_port(PORT, is_kb_backend_pid):
        if pid not in stopped:
            stopped.append(pid)

    for _ in range(10):
        if not port_alive(PORT) and not port_alive(FRONTEND_PORT):
            break
        time.sleep(0.5)

    alive_ports = [str(port) for port in (PORT, FRONTEND_PORT) if port_alive(port)]
    if stopped and alive_ports:
        print(f"Stopped CPA-ZH server process(es): {', '.join(stopped)}")
        print(f"Port(s) still occupied: {', '.join(alive_ports)}")
        print("Check the remaining process manually before stopping it.")
        return 1
    if stopped:
        clear_state()
        print(f"Stopped CPA-ZH server process(es): {', '.join(stopped)}")
    elif alive_ports:
        print(f"Port(s) {', '.join(alive_ports)} are still occupied, but no CPA-ZH process was identified.")
        print("Check the process manually before stopping it.")
        return 1
    else:
        clear_state()
        print("CPA-ZH services are not running.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
