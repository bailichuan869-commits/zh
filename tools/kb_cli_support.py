from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = PROJECT_ROOT / "tools"


def run_script(script_name: str, root: str, script_args: list[str]) -> int:
    command = [
        sys.executable,
        str(TOOLS_ROOT / script_name),
        "--root",
        root,
        *script_args,
    ]
    return subprocess.call(command, cwd=PROJECT_ROOT)


def add_present_options(target: list[str], option_pairs: dict[str, Any]) -> None:
    for option, value in option_pairs.items():
        if value:
            target.extend([option, str(value)])


def add_enabled_flags(target: list[str], flag_pairs: dict[str, bool]) -> None:
    for flag, enabled in flag_pairs.items():
        if enabled:
            target.append(flag)
