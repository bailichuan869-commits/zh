#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将财政部企业会计准则解释第N号附件正文合并进通知壳 .md。

- .doc / .pdf 正文已用 antiword / pymupdf 抽成 解释第NN号_body.txt
- .docx 正文用 docx_to_markdown.py 抽成 解释第NN号_body.txt (markdown)
本脚本负责清理 + 追加到对应的 *通知.html.md，并在 frontmatter 打标。
"""
import os, re

BASE = r"D:/ai-audit/knowledge-base/CPA-ZH/raw/standards/accounting/interpretations-pages"
SKIP = {"06"}  # #6 壳已含正文，跳过
NUMBERS = ["01","02","03","09","10","11","12","13","14","15","16","17","18"]


def find_shell(num):
    alt = str(int(num))  # 去掉前导零，如 01->1
    pat = re.compile(r"解释第(?:" + num + r"|" + alt + r")号")
    for f in os.listdir(BASE):
        if f.endswith(".html.md") and pat.search(f):
            return os.path.join(BASE, f)
    return None


def find_attach_ext(num):
    for ext in ("doc", "docx", "pdf"):
        p = os.path.join(BASE, f"解释第{num}号_附件.{ext}")
        if os.path.exists(p):
            return ext
    return None


PARA_START = re.compile(r"^     [^ ]")  # antiword 段落起始：恰好 5 空格 + 非空


def unwrap_antiword(text):
    """解 antiword 的硬换行。
    antiword 把每段折成约 30 字符一行的物理折行；段起始是『5 空格 + 文字』，续行无缩进，空行为段间隔。
    解完后每个语义段（『一、』『答：』『（一）』等）独占一行段，段与段之间空一行隔断。
    """
    lines = text.split("\n")
    paragraphs = []
    cur = []
    for line in lines:
        if line.strip() == "":
            if cur:
                paragraphs.append("".join(cur))
                cur = []
        elif PARA_START.match(line):
            if cur:
                paragraphs.append("".join(cur))
            cur = [line.strip()]
        else:
            cur.append(line.rstrip())
    if cur:
        paragraphs.append("".join(cur))
    return "\n\n".join(p for p in paragraphs if p)


def clean_body(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 检测 antiword 输出：有 ≥3 行以『5 空格 + 非空』开头 → 先解硬换行
    if sum(1 for ln in text.split("\n") if PARA_START.match(ln)) >= 3:
        text = unwrap_antiword(text)
    lines = text.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    # 去 PDF 页眉：开头的孤立页码数字（如 "1"）
    while lines and re.match(r"^\d+$", lines[0].strip()):
        lines.pop(0)
    # 去掉开头的 “附件：” 行
    if lines and lines[0].strip().startswith("附件"):
        lines.pop(0)
        while lines and lines[0].strip() == "":
            lines.pop(0)
    # 去掉开头的 markdown 标题重复（docx 自带 “# 企业会计准则解释第N号”）
    if lines and re.match(r"^#+\s*.*解释第.*号", lines[0]):
        lines.pop(0)
        while lines and lines[0].strip() == "":
            lines.pop(0)
    # 去掉纯文本重复标题（antiword 抽出后 .strip() 过的 “企业会计准则解释第N号”，允许中间有空格）
    if lines and re.match(r"^\s*企业会计准则解释第\s*\d+\s*号\s*$", lines[0]):
        lines.pop(0)
        while lines and lines[0].strip() == "":
            lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_frontmatter(raw):
    if not raw.startswith("---"):
        return "", raw
    idx = raw.find("\n---", 3)
    if idx == -1:
        return "", raw
    fm = raw[3:idx].strip()
    rest = raw[idx + 4:].lstrip("\n")
    return fm, rest


def strip_existing_merge(raw, title_num):
    """移除已合并的正文块与 frontmatter 标记，便于强制重合并。"""
    # 移除正文块
    raw = re.sub(r"\n## 企业会计准则解释第" + title_num + r"号（正文）[\s\S]*$", "", raw)
    # 移除 frontmatter 标记行
    raw = re.sub(r"\nbody_merged:.*\nbody_source:.*\nmerged_at:.*\n", "\n", raw)
    return raw


def main():
    FORCE = set(os.environ.get("FORCE", "").split(",")) if os.environ.get("FORCE") else set()
    for num in NUMBERS:
        if num in SKIP:
            print(f"#{num} 跳过(壳已含正文)")
            continue
        shell = find_shell(num)
        ext = find_attach_ext(num)
        bodyf = os.path.join(BASE, f"解释第{num}号_body.txt")
        if not shell:
            print(f"#{num} 未找到壳文件！")
            continue
        if not ext or not os.path.exists(bodyf):
            print(f"#{num} 缺少正文(body.txt / 附件)")
            continue
        raw = open(shell, encoding="utf-8").read()
        title_num = str(int(num))
        if num in FORCE:
            raw = strip_existing_merge(raw, title_num)
        elif "body_merged:" in raw or "（正文）" in raw:
            print(f"#{num} 已合并，跳过")
            continue
        fm, rest = split_frontmatter(raw)
        body = clean_body(open(bodyf, encoding="utf-8").read())
        if not body:
            print(f"#{num} 正文体为空，跳过")
            continue
        fm += f"\nbody_merged: true\nbody_source: 解释第{num}号_附件.{ext}\nmerged_at: 2026-07-26"
        merged = (
            "---\n" + fm + "\n---\n\n"
            + rest.rstrip("\n")
            + f"\n\n## 企业会计准则解释第{title_num}号（正文）\n\n"
            + body + "\n"
        )
        open(shell, "w", encoding="utf-8").write(merged)
        print(f"#{num} 已合并 -> {os.path.basename(shell)} (正文 {len(body)} 字, 附件 .{ext})")


if __name__ == "__main__":
    main()
