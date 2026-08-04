#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_inline_parens.py —— 一次性回滚脚本。

把"形如 '（X）至' / '（X）和' / '（X）的规定进行披露' " 这种被 format_legal()
第 4 条规则错误升级成独立 bullet 的**行中引用片段**合并回上一段尾部。

触发背景：format_legal() 旧规则在正文中每次匹配到"（X）"就插入独立 bullet，但
法律/会计准则里大量"按本条（一）至（二）项规定进行披露"这种行中引用片段被切碎。

判断 inline 引用片段的特征：
  - 行以 "- " 开头（被升级为 bullet）
  - body 长度 ≤ 15 字（不会太长）
  - body 以 "（中文数字）" 开头
  - 末位是"和/或/，/、/至"等连词；或形如 "（X）的规定/项/条款" + 短后续

合并策略：把 inline 引用片段直接拼到上一段尾部（去掉 "- " 前缀），
多次扫描直到稳定（连续 inline 引用会被串行合并）。

用法：
  python tools/merge_inline_parens.py                  # dry-run
  python tools/merge_inline_parens.py --apply          # 全量合并并写回
  python tools/merge_inline_parens.py --dir raw/cases  # 子目录
  python tools/merge_inline_parens.py --path raw/.../x.md  # 单文件
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 形如 "（X）" 开头
PAREN_HEAD = r"^（[一二三四五六七八九十百零0-9]+）"
# inline 引用片段特征（三种模式）：
#   1) 末尾是连词："和/或/，/、/至"
#   2) "（X）的规定/披露/项/条款" + 任意后续（含句号）
#   3) 范围引用："（X）至（Y）"
INLINE_REF_PATTERNS = [
    re.compile(r"^（[一二三四五六七八九十百零0-9]+）[和或，、至]\s*$"),
    re.compile(r"^（[一二三四五六七八九十百零0-9]+）[的项条款项目].{0,40}?$"),
    re.compile(r"^（[一二三四五六七八九十百零0-9]+）至（[一二三四五六七八九十百零0-9]+）"),
]


def looks_like_inline_ref(line: str) -> bool:
    """判断一行是否是被错误升级的 inline 引用片段。
    关键区分：独立项以"（X）"+ 动词/名词短语开头（如"履行""最终确定"），长度通常 ≥ 10 字；
    引用片段以"（X）"+ 弱连词/特定引用名词开头（如"和""至""的规定""项""条款"）。
    """
    s = line.rstrip()
    if not s.startswith("- "):
        return False
    body = s[2:].strip()
    if not body:
        return False
    if not re.match(PAREN_HEAD, body):
        return False
    # 守卫：含粗体文章标题"**第X条**"的不是 inline 引用（是被误升级的伪 bullet，需独立成行）
    if re.match(r"^\*\*第[一二三四五六七八九十百零0-9]+条\*\*", body):
        return False
    # 长度上限 60：避免误伤长独立项
    if len(body) > 60:
        return False
    for pat in INLINE_REF_PATTERNS:
        if pat.match(body):
            return True
    return False


def merge_one_pass(text: str) -> tuple[str, int]:
    """一轮合并：每个 inline 引用片段向上一段尾部合并。返回 (新文本, 合并数)。"""
    lines = text.splitlines()
    out: list[str] = []
    merged = 0
    for ln in lines:
        if looks_like_inline_ref(ln) and out:
            prev = out[-1].rstrip()
            inline = ln.strip()[2:].strip()  # 去掉 "- "
            if prev:
                out[-1] = prev + inline
            else:
                out[-1] = inline
            merged += 1
        else:
            out.append(ln)
    return "\n".join(out), merged


def merge_until_stable(text: str, max_passes: int = 5) -> tuple[str, int]:
    """多次扫描直到没有可合并的 inline 引用片段（处理连续多段）。"""
    total = 0
    for _ in range(max_passes):
        text, n = merge_one_pass(text)
        total += n
        if n == 0:
            break
    return text, total


def iter_md(subdir: str) -> list[Path]:
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
    ap.add_argument("--path", default="", help="仅处理单个文件")
    args = ap.parse_args()

    if args.path:
        p = Path(args.path)
        if not p.is_absolute():
            p = ROOT / p
        targets = [p]
    else:
        targets = iter_md(args.dir)

    total_files = 0
    total_merged = 0
    sample_log: list[tuple[Path, int]] = []

    for md_path in targets:
        if not md_path.exists() or not md_path.is_file():
            continue
        text = md_path.read_text(encoding="utf-8")
        new_text, merged = merge_until_stable(text)
        if merged > 0:
            total_files += 1
            total_merged += merged
            sample_log.append((md_path, merged))
            if args.apply:
                md_path.write_text(new_text, encoding="utf-8")

    mode = "APPLY" if args.apply else "DRY"
    print(f"[{mode}] 扫描 {len(targets)} 个文件 | 命中 {total_files} 个 | 合并 {total_merged} 处 inline 引用片段")
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
