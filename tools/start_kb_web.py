"""Start the CPA-ZH backend and frontend together."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
TMP = ROOT / "workspace" / "tmp"
STATE_FILE = TMP / "kb_web_launch.json"
BACKEND_PORT = int(os.environ.get("KB_PORT", "8765"))
FRONTEND_PORT = int(os.environ.get("KB_FRONTEND_PORT", "5173"))
STARTUP_TIMEOUT = int(os.environ.get("KB_STARTUP_TIMEOUT", "45"))


def port_alive(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.settimeout(1.0)
        return handle.connect_ex(("127.0.0.1", port)) == 0


def wait_for_port(port: int, *, timeout: int, process: subprocess.Popen[str] | None = None) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process is not None and process.poll() is not None:
            return port_alive(port)
        if port_alive(port):
            return True
        time.sleep(0.5)
    return port_alive(port)


def npm_command() -> str | None:
    return shutil.which("npm.cmd") or shutil.which("npm")


def write_state(backend_pid: int | None, frontend_pid: int | None) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    payload = {
        "backend": {"pid": backend_pid, "port": BACKEND_PORT},
        "frontend": {"pid": frontend_pid, "port": FRONTEND_PORT},
        "updated_at": int(time.time()),
    }
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def clear_state() -> None:
    STATE_FILE.unlink(missing_ok=True)


def terminate_tree(pid: int) -> bool:
    result = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True)
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the CPA-ZH backend and frontend together")
    parser.add_argument("--dry-run", action="store_true", help="Print the commands without starting anything")
    args = parser.parse_args()

    if not BACKEND.is_dir():
        print(f"[ERROR] Backend directory not found: {BACKEND}")
        return 1
    if not FRONTEND.is_dir():
        print(f"[ERROR] Frontend directory not found: {FRONTEND}")
        return 1

    backend_running = port_alive(BACKEND_PORT)
    frontend_running = port_alive(FRONTEND_PORT)

    if backend_running:
        print(f"[INFO] Backend already running on http://127.0.0.1:{BACKEND_PORT}/api/docs")
    if frontend_running:
        print(f"[INFO] Frontend already running on http://127.0.0.1:{FRONTEND_PORT}")

    backend_proc: subprocess.Popen[str] | None = None
    frontend_proc: subprocess.Popen[str] | None = None

    if not backend_running:
        backend_command = [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--app-dir",
            str(BACKEND),
            "--host",
            "127.0.0.1",
            "--port",
            str(BACKEND_PORT),
        ]
        print(f"[INFO] Backend command: {subprocess.list2cmdline(backend_command)}")
        if not args.dry_run:
            backend_proc = subprocess.Popen(backend_command, cwd=ROOT)
            print(f"[INFO] Backend pid: {backend_proc.pid}")
            if not wait_for_port(BACKEND_PORT, timeout=STARTUP_TIMEOUT, process=backend_proc):
                terminate_tree(backend_proc.pid)
                clear_state()
                print(f"[ERROR] Backend failed to start on port {BACKEND_PORT}.")
                return 1

    if not frontend_running:
        npm = npm_command()
        if not npm:
            if backend_proc is not None:
                terminate_tree(backend_proc.pid)
                clear_state()
            print("[ERROR] npm was not found on PATH.")
            return 1
        if not (FRONTEND / "node_modules").is_dir():
            if backend_proc is not None:
                terminate_tree(backend_proc.pid)
                clear_state()
            print(f"[ERROR] Frontend dependencies are missing: {FRONTEND / 'node_modules'}")
            print("Run `npm install` in `frontend/` first.")
            return 1
        frontend_command = [
            npm,
            "run",
            "dev",
            "--",
            "--host",
            "127.0.0.1",
            "--port",
            str(FRONTEND_PORT),
        ]
        print(f"[INFO] Frontend command: {subprocess.list2cmdline(frontend_command)}")
        if not args.dry_run:
            frontend_proc = subprocess.Popen(frontend_command, cwd=FRONTEND)
            print(f"[INFO] Frontend pid: {frontend_proc.pid}")
            if not wait_for_port(FRONTEND_PORT, timeout=STARTUP_TIMEOUT, process=frontend_proc):
                terminate_tree(frontend_proc.pid)
                if backend_proc is not None:
                    terminate_tree(backend_proc.pid)
                clear_state()
                print(f"[ERROR] Frontend failed to start on port {FRONTEND_PORT}.")
                return 1

    if args.dry_run:
        return 0

    if backend_proc is None and frontend_proc is None:
        clear_state()
        print("CPA-ZH backend and frontend are already running.")
        return 0

    write_state(backend_proc.pid if backend_proc else None, frontend_proc.pid if frontend_proc else None)
    print(f"CPA-ZH API: http://127.0.0.1:{BACKEND_PORT}/api/docs")
    print(f"CPA-ZH Frontend: http://127.0.0.1:{FRONTEND_PORT}")
    print("Press Ctrl+C to stop the launched services.")

    running: dict[str, subprocess.Popen[str]] = {}
    if backend_proc is not None:
        running["backend"] = backend_proc
    if frontend_proc is not None:
        running["frontend"] = frontend_proc

    try:
        while running:
            for name, process in list(running.items()):
                return_code = process.poll()
                if return_code is None:
                    continue
                running.pop(name)
                if return_code != 0:
                    print(f"[ERROR] {name} exited with code {return_code}.")
                    for other_name, other_process in running.items():
                        terminate_tree(other_process.pid)
                        print(f"[INFO] Stopped {other_name} after {name} exited.")
                    clear_state()
                    return return_code
                print(f"[INFO] {name} exited cleanly.")
                for other_name, other_process in running.items():
                    terminate_tree(other_process.pid)
                    print(f"[INFO] Stopped {other_name} after {name} exited.")
                clear_state()
                return 0
            time.sleep(1)
    except KeyboardInterrupt:
        for process in running.values():
            terminate_tree(process.pid)
        clear_state()
        print("\nStopped CPA-ZH backend and frontend.")
        return 130

    clear_state()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
