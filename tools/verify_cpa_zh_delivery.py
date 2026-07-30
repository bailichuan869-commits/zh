"""Run the repeatable CPA-ZH delivery gate from the repository root."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"[verify] {' '.join(command)}")
    try:
        result = subprocess.run(command, cwd=cwd)
    except OSError as exc:
        raise RuntimeError(f"could not start {' '.join(command)}: {exc}") from exc
    if result.returncode:
        raise RuntimeError(f"verification failed with exit code {result.returncode}: {' '.join(command)}")


def frontend_commands() -> list[list[str]]:
    node = shutil.which("node")
    frontend = ROOT / "frontend"
    if not node:
        raise RuntimeError("Node.js is required for frontend verification")
    commands = [
        [node, "node_modules/vitest/vitest.mjs", "run"],
        [node, "node_modules/vue-tsc/bin/vue-tsc.js", "-b"],
        [node, "node_modules/vite/bin/vite.js", "build"],
    ]
    for command in commands:
        if not (frontend / command[1]).exists():
            raise RuntimeError("frontend dependencies are missing; run npm install in frontend")
    return commands


def verify_navigation_tree(kb_root: Path) -> None:
    tree_path = kb_root / "search" / "navigation-tree.json"
    if not tree_path.exists():
        raise RuntimeError("missing search/navigation-tree.json; run tools/kb.py classify build")
    try:
        tree = json.loads(tree_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid navigation tree: {exc}") from exc
    if not isinstance(tree, dict) or not tree.get("domains"):
        raise RuntimeError("navigation tree has no domains")

    newest_asset = max(
        (path.stat().st_mtime for directory in (kb_root / "raw", kb_root / "wiki") for path in directory.rglob("*") if path.is_file()),
        default=0,
    )
    if tree_path.stat().st_mtime < newest_asset:
        raise RuntimeError("navigation tree is stale; run tools/kb.py classify build")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CPA-ZH migration and release verification.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root relative to the project root.")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend Vitest and production build checks.")
    args = parser.parse_args()
    kb_root = (ROOT / args.root).resolve()

    try:
        verify_navigation_tree(kb_root)
        run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
        run([sys.executable, "-B", "tools/kb.py", "health"])
        if not args.skip_frontend:
            for command in frontend_commands():
                run(command, cwd=ROOT / "frontend")
    except RuntimeError as exc:
        print(f"[verify] FAILED: {exc}", file=sys.stderr)
        return 1

    print("[verify] PASSED: navigation tree, API contracts, knowledge health, and frontend checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
