#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_legal_md.py —— 把 raw/ 下已转换的 .md 重排成"参考法规版式"的语义化结构。

用法：
  python tools/format_legal_md.py                 # 默认 dry-run（只报告，不写）
  python tools/format_legal_md.py --apply         # 全量重写
  python tools/format_legal_md.py --dir raw/standards/accounting/standards-pages --apply   # 子目录
  python tools/format_legal_md.py --from-archive  # 从 _archive 原文件重新抽取再格式化（最确定性）

规则：
  - 默认只重排 raw/ 下已生成的 .md；不动 _archive 原文件（可逆）。
  - 幂等 guard：正文已以 '# ' 开头则跳过，防重复格式化。
  - legal 型（含章/条/项）：补 # 标题、## 章、### 节、**第X条** 加粗独立成段、（一）项转列表。
  - general 型（PDF 答疑/讲义/索引）：补 # 标题、目录点线墙折叠为引用块、编号议题升二级标题、表格转标准 md 表。
"""
import argparse, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "knowledge-base" / "CPA-ZH" / "raw"
ARCHIVE = RAW / "_archive"

ZH_NUM = r"[一二三四五六七八九十百零]+"
ART_RE = r"第([0-9]{1,3}|" + ZH_NUM + r"|[XIV]+)条"

# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------
def split_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end]
    body = text[end + 4:]
    fm = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"\'')
    return fm, body.lstrip("\n")

def dump_frontmatter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if v is None or v == "":
            continue
        lines.append(f'{k}: "{v}"' if (":" in str(v) or "\"" in str(v)) else f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"

# ---------------------------------------------------------------------------
# 取标题：优先 frontmatter.title，否则从文件名推断
# ---------------------------------------------------------------------------
def get_title(fm: dict, md_path: Path) -> str:
    t = (fm.get("title") or "").strip()
    if t:
        return t
    return md_path.stem

# ---------------------------------------------------------------------------
# legal 型排版
# ---------------------------------------------------------------------------
def format_legal(body: str, title: str) -> str:
    # 1) 章 -> ## 第X章 章名
    body = re.sub(
        r"第(" + ZH_NUM + r")章[ \u3000]*(.*)",
        lambda m: f"\n\n## 第{m.group(1)}章 {m.group(2).strip()}\n\n",
        body,
    )
    # 2) 节 -> ### 第X节 节名
    body = re.sub(
        r"第(" + ZH_NUM + r")节[ \u3000]*(.*)",
        lambda m: f"\n\n### 第{m.group(1)}节 {m.group(2).strip()}\n\n",
        body,
    )
    # 3) 条 -> **第X条** 加粗独立成段（仅在句界/行首/空白后切分，避免误切正文中的"第X条"引用）
    body = re.sub(
        r"(^|[。；、\s])(" + ART_RE + r")",
        lambda m: f"{m.group(1)}\n\n**{m.group(2)}** ",
        body,
    )
    # 4) 项 (一)(二)… -> 转列表项（**仅在行首/段首**才升级，避免切碎"按本条（一）至（二）"这种行中引用片段；
    #                          同时排除"**第X条**（Y）..."这种含粗体文章标题的伪 bullet——它本应独立成行而非被升级）
    def _paren_to_bullet(m):
        head, n = m.group(1), m.group(2)
        # 窥探后续 30 字，若以"**第X条**"开头则跳过升级
        rest = m.string[m.end():m.end()+30] if hasattr(m, 'string') else ""
        if re.match(r"\s*\*\*第[一二三四五六七八九十百零0-9]+条\*\*", rest):
            return m.group(0)
        return f"{head}- （{n}）"
    body = re.sub(
        r"(^|\n)[ \t\u3000]*（([一二三四五六七八九十百零0-9]+)）",
        _paren_to_bullet,
        body,
    )
    # 5) 清理多余空行
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return f"# {title}\n\n{body}\n"

def is_title_candidate(text: str) -> bool:
    """判断一行是否真的像"短标题"（用于编号议题 1./1、 的升级与降级判断）。
    规则（全部必须满足）：
      1. 字符数 ≤ 40（短句才像标题）
      2. 不含句末/问号/感叹号/分号（。？！；）
      3. 逗号/顿号（，,、）总数 ≤ 1（多逗号必是陈述句）
    长句、多重逗号、含问号的必不是标题，应保持正文。
    """
    if not text or len(text) > 40:
        return False
    if re.search(r"[。？?！!；;]", text):
        return False
    sep = text.count("，") + text.count(",") + text.count("、")
    if sep > 1:
        return False
    return True


# ---------------------------------------------------------------------------
# general 型排版
# ---------------------------------------------------------------------------
def format_general(body: str, title: str) -> str:
    lines = body.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        # 目录 / TOC 点线墙：文字 + 多个点 + 页码 -> 折叠为引用块（去点线去页码）
        m = re.match(r"^(.*?)[．.．]{3,}\s*\d+\s*$", s)
        if m:
            topic = m.group(1).strip()
            if topic:
                out.append(f"> {topic}")
            continue
        # 升级：1．/1、/1.  -> ## 标题（仅在非表格行时）
        m2 = re.match(r"^(\d{1,3})[．、.]\s*(.+)$", s)
        if m2 and " | " not in s:
            out.append(f"## {m2.group(1)}．{m2.group(2).strip()}")
            continue
        # 降级：已存在的 ## 1.xxx 行若不像标题（历史错误升级） -> 退为正文（去掉 ## 前缀）
        m3 = re.match(r"^##\s+(\d{1,3})[．、.]\s*(.+?)\s*$", s)
        if m3 and not is_title_candidate(m3.group(2).strip()):
            out.append(f"{m3.group(1)}．{m3.group(2).strip()}")
            continue
        out.append(ln)
    body = "\n".join(out)

    # 表格：连续 >=2 行含相同数量 ' | ' -> 标准 md 表
    body = rebuild_tables(body)

    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return f"# {title}\n\n{body}\n"

def rebuild_tables(text: str) -> str:
    lines = text.split("\n")
    i = 0
    res = []
    while i < len(lines):
        ln = lines[i]
        cnt = ln.count(" | ")
        if cnt >= 1 and i + 1 < len(lines) and lines[i + 1].count(" | ") == cnt:
            # Already a Markdown table. Preserve the existing separator and do not add another one.
            if re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
                res.append(ln)
                res.append(lines[i + 1])
                i += 2
                while i < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i]):
                    i += 1
                continue
            # 连续表格行
            block = [ln]
            j = i + 1
            while j < len(lines) and lines[j].count(" | ") == cnt:
                block.append(lines[j])
                j += 1
            header = block[0]
            sep = "| " + " | ".join("---" for _ in range(cnt + 1)) + " |"
            res.append(header)
            res.append(sep)
            res.extend(block[1:])
            res.append("")  # 表后空行
            i = j
        else:
            res.append(ln)
            i += 1
    return "\n".join(res)

# ---------------------------------------------------------------------------
# 判定 profile
# ---------------------------------------------------------------------------
def detect_profile(body: str) -> str:
    # 真正的法规/准则中，"第X章"是行首的章节标题；问答汇编只在正文里零星引用"第X章"（非行首）。
    # 故以"行首 第X章"作为 legal 判定信号。
    if re.search(r"(?m)^[\s\u3000]*第" + ZH_NUM + r"章", body):
        return "legal"
    return "general"

# ---------------------------------------------------------------------------
# 单文件处理
# ---------------------------------------------------------------------------
def reformat_one(md_path: Path, apply: bool, from_archive: bool, reapply: bool = False):
    text = md_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    stripped = body.lstrip()
    # 幂等 guard：已格式化过（正文以 '# ' 开头）则跳过；--reapply 时强制重处理（用于回滚历史错误升级的标题）
    if not reapply and stripped.startswith("# "):
        return "skip", md_path, ""
    title = get_title(fm, md_path)
    profile = detect_profile(body)
    new_body = format_legal(body, title) if profile == "legal" else format_general(body, title)
    new_text = dump_frontmatter(fm) + new_body
    if not apply:
        return "dry", md_path, profile
    # 写回（覆盖；不删除原，原在 _archive）
    md_path.write_text(new_text, encoding="utf-8")
    return "done", md_path, profile

def iter_md(subdir: str):
    rel = subdir
    if rel.startswith("raw/"):
        rel = rel[4:]
    base = RAW / rel if rel else RAW
    for p in sorted(base.rglob("*.md")):
        if "_archive" in p.parts:
            continue
        yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="", help="仅处理该子目录（相对 raw/）")
    ap.add_argument("--apply", action="store_true", help="实际写回（默认 dry-run）")
    ap.add_argument("--from-archive", action="store_true", help="从 _archive 原文件重新抽取再格式化")
    ap.add_argument("--reapply", action="store_true", help="跳过幂等 guard，对已格式化的 md 重新校验（用于回滚历史错误升级的标题）")
    args = ap.parse_args()

    if args.from_archive:
        # 用 convert_raw_to_md 的抽取函数，从 _archive 取原文件重新生成 body
        sys.path.insert(0, str(ROOT / "tools"))
        import convert_raw_to_md as C
        done = skip = 0
        for md_path in iter_md(args.dir):
            text = md_path.read_text(encoding="utf-8")
            fm, _ = split_frontmatter(text)
            orig = fm.get("original_file", "")
            src = ARCHIVE / Path(orig).relative_to("raw") if orig.startswith("raw/") else None
            if not src or not src.exists():
                skip += 1
                continue
            ext = src.suffix.lower()
            if ext in (".html", ".htm", ".xml"):
                body = C.extract_html(src)
            elif ext == ".pdf":
                body = C.extract_pdf(src)
            elif ext == ".docx":
                body = C.extract_docx(src)
            elif ext == ".txt":
                body = C.extract_txt(src)
            elif ext == ".csv":
                body = C.extract_csv(src)
            else:
                skip += 1
                continue
            title = get_title(fm, md_path)
            profile = detect_profile(body)
            new_body = format_legal(body, title) if profile == "legal" else format_general(body, title)
            if args.apply:
                md_path.write_text(dump_frontmatter(fm) + new_body, encoding="utf-8")
                done += 1
            else:
                done += 1
        print(f"[from-archive] {'APPLY' if args.apply else 'DRY'} 处理 {done} 个, 跳过 {skip} 个")
        return

    counts = {"legal": 0, "general": 0, "skip": 0, "done": 0, "demoted": 0, "upgraded": 0, "unchanged": 0}
    for md_path in iter_md(args.dir):
        if args.reapply:
            # 重处理前先估算降级/升级数（在不写盘的情况下跑一次，得到新 body）
            text = md_path.read_text(encoding="utf-8")
            fm, body = split_frontmatter(text)
            old_h2 = sum(1 for ln in body.splitlines() if re.match(r"^##\s+\d[．、.]\s*", ln.strip()))
            title = get_title(fm, md_path)
            profile = detect_profile(body)
            new_body = format_legal(body, title) if profile == "legal" else format_general(body, title)
            new_h2 = sum(1 for ln in new_body.splitlines() if re.match(r"^##\s+\d[．、.]\s*", ln.strip()))
            d = old_h2 - new_h2
            if d > 0:
                counts["demoted"] += d
            elif d < 0:
                counts["upgraded"] += -d
            else:
                counts["unchanged"] += 1
        status, _, profile = reformat_one(md_path, args.apply, False, args.reapply)
        if status == "skip":
            counts["skip"] += 1
        elif status == "dry":
            counts[profile] += 1
        elif status == "done":
            counts["done"] += 1
            counts[profile] = counts.get(profile, 0)  # dry 时统计，apply 时再记
    if args.apply:
        if args.reapply:
            print(f"[apply --reapply] 已重写 {counts['done']} 个 md；降级错标题 {counts['demoted']} 处，升级 {counts['upgraded']} 处，无变化 {counts['unchanged']} 处；跳过(非 # 开头) {counts['skip']} 个")
        else:
            print(f"[apply] 已重写 {counts['done']} 个 md（legal/general 见上方 dry 统计）；跳过已格式化 {counts['skip']} 个")
    else:
        if args.reapply:
            print(f"[dry-run --reapply] 降级错标题预估 {counts['demoted']} 处，升级 {counts['upgraded']} 处，无变化 {counts['unchanged']} 处；跳过(非 # 开头) {counts['skip']} 个")
        else:
            print(f"[dry-run] legal 型待处理: {counts.get('legal',0)} | general 型待处理: {counts.get('general',0)} | 已跳过(已格式化): {counts['skip']}")

if __name__ == "__main__":
    main()
