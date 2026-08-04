#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CPA-ZH 知识库浏览界面本地服务。

托管 CPA-ZH 根目录，使 ui/ 与 wiki/ 均可被前端 fetch（克服 file:// 禁止
fetch 的限制）。启动后浏览器打开打印的 URL 即可使用。

运行（虚拟环境，绝对路径，不 cd、不变量）：
    PYTHONFAULTHANDLER=1 /d/ai-audit/.venv/Scripts/python.exe \\
        /d/ai-audit/knowledge-base/CPA-ZH/tools/serve_kb_ui.py
"""

from __future__ import annotations

import atexit
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../knowledge-base/CPA-ZH
TMP = Path(__file__).resolve().parents[3] / "workspace" / "tmp"
BASE_PORT = 8765
MAX_PORT_TRIES = 20


def _is_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform.startswith("win"):
        try:
            import ctypes
            h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)  # PROCESS_QUERY_INFORMATION
            alive = bool(h)
            if h:
                ctypes.windll.kernel32.CloseHandle(h)
        except Exception:
            return False
        return alive
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _rm_lock(lock: "Path") -> None:
    try:
        lock.unlink()
    except Exception:
        pass


def main() -> int:
    # 单实例保护：避免重复启动导致多进程竞争同一端口、前端偶发加载失败
    # 锁放在 workspace/tmp/，不污染知识库根目录（知识库根零散落单文件）
    TMP.mkdir(parents=True, exist_ok=True)
    lock = TMP / ".kb_serve.lock"
    if lock.exists():
        try:
            old_pid = int(lock.read_text(encoding="utf-8").strip())
        except Exception:
            old_pid = -1
        if _is_alive(old_pid):
            print(f"知识库服务已在运行（旧进程 PID={old_pid}）。请勿重复启动。")
            print(f"  访问: http://localhost:{BASE_PORT}/ui/index.html")
            print(f"  如需重启，请先结束旧进程，或删除锁文件: {lock}")  # lock 位于 workspace/tmp/
            return 0
        try:
            lock.unlink()
        except Exception:
            pass
    lock.write_text(str(os.getpid()), encoding="utf-8")
    atexit.register(_rm_lock, lock)

    # 以 CPA-ZH 为根目录托管，前端用相对路径 ../wiki/... 与 ui/... 访问
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    ThreadingHTTPServer.allow_reuse_address = False
    port = BASE_PORT
    server = None
    for _ in range(MAX_PORT_TRIES):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            port += 1
    if server is None:
        print("无法绑定端口（8765 起连续 20 个均被占用），请释放后重试。", file=sys.stderr)
        return 1

    url = f"http://localhost:{port}/ui/index.html"
    print("CPA-ZH 知识库浏览器已启动")
    print(f"  根目录: {ROOT}")
    print(f"  访问  : {url}")
    print("  按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
