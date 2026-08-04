#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demote_bad_h2.py —— 一次性回滚脚本。

把已被 format_legal_md.py 错误升级成 ## 二级标题的长句正文（以"1. xxx"/"1、xxx"开头，
但内容像法规条款/陈述句）降级回正文：去掉 "## " 前缀。

触发背景：format_general() 旧规则无差别升级"1. xxx"开头的行为"二级标题"，但法规问答
里的"处理方式条款"刚好以"1. xxx"形式出现且长达数百字，造成正文被错误放大加粗。

判断函数复用 format_legal_md.is_title_candidate：
  - 字符数 ≤ 40
  - 无句末/问号/感叹号/分号
  - 逗号/顿号总数 ≤ 1

用法：
  python tools/demote_bad_h2.py                  # 默认 dry-run
  python tools/demote_bad_h2.py --apply          # 全量降级并写回
  python tools/demote_bad_h2.py --dir raw/cases  # 子目录
  python tools/demote_bad_h2.py --path raw/.../x.md  # 单文件
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from format_legal_md import is_title_candidate  # 复用同一判断

# 匹配 "## 1.xxx" / "## 1、xxx" / "## 1．xxx"（行首）
H2_BAD_RE = re.compile(r"^##\s+(\d{1,3})[．、.]\s*(.+?)\s*$")


def demote_text(text: str) -> tuple[str, int]:
    """在文本上执行降级，返回 (new_text, demoted_count)。"""
    out_lines = []
    demoted = 0
    for ln in text.splitlines():
        m = H2_BAD_RE.match(ln.strip())
        if m and not is_title_candidate(m.group(2).strip()):
            # 降级：去掉 "## " 前缀，保留编号与正文
            out_lines.append(f"{m.group(1)}．{m.group(2).strip()}")
            demoted += 1
        else:
            out_lines.append(ln)
    return "\n".join(out_lines), demoted


def iter_md(subdir: str) -> list[Path]:
    """枚举 raw/ 子目录下所有活跃 .md（排除 _archive）。"""
    base = ROOT / "knowledge-base" / "CPA-ZH" / "raw"
    if subdir:
        if subdir.startswith("raw/"):
            subdir = subdir[4:]
        base = base / subdir
    return [p for p in sorted(base.rglob("*.md")) if "_archive" not in p.parts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="实际写回（默认 dry-run）")
    ap.add_argument("--dir", default="", help="仅处理该子目录（相对 raw/）")
    ap.add_argument("--path", default="", help="仅处理单个文件（绝对路径或相对仓库根）")
    args = ap.parse_args()

    if args.path:
        p = Path(args.path)
        if not p.is_absolute():
            p = ROOT / p
        targets = [p]
    else:
        targets = iter_md(args.dir)

    total_files = 0
    total_demoted = 0
    sample_log: list[tuple[Path, int]] = []

    for md_path in targets:
        if not md_path.exists() or not md_path.is_file():
            continue
        text = md_path.read_text(encoding="utf-8")
        new_text, demoted = demote_text(text)
        if demoted > 0:
            total_files += 1
            total_demoted += demoted
            sample_log.append((md_path, demoted))
            if args.apply:
                md_path.write_text(new_text, encoding="utf-8")

    mode = "APPLY" if args.apply else "DRY"
    print(f"[{mode}] 扫描 {len(targets)} 个文件 | 命中 {total_files} 个 | 降级 {total_demoted} 处错标题")
    if sample_log:
        print("受影响文件 Top 10：")
        for p, n in sorted(sample_log, key=lambda x: -x[1])[:10]:
            try:
                rel = p.relative_to(ROOT)
            except ValueError:
                rel = p
            print(f"  {n:3d}处  {rel}")


if __name__ == "__main__":
    main()
