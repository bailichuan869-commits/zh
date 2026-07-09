from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

TITLE_RE = re.compile(r"^中华人民共和国.+法$")
CHAPTER_RE = re.compile(r"^第[一二三四五六七八九十百千]+章")
SECTION_RE = re.compile(r"^第[一二三四五六七八九十百千]+节")
ARTICLE_RE = re.compile(r"^第[一二三四五六七八九十百千]+条")


def read_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))

    paragraphs: list[str] = []
    for para in root.findall(".//w:p", NS):
        text = "".join((node.text or "") for node in para.findall(".//w:t", NS)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def to_markdown(paragraphs: list[str]) -> str:
    lines: list[str] = []
    title_used = False

    for para in paragraphs:
        if not title_used and TITLE_RE.match(para):
            lines.append(f"# {para}")
            lines.append("")
            title_used = True
            continue

        if CHAPTER_RE.match(para):
            lines.append(f"## {para}")
            lines.append("")
            continue

        if SECTION_RE.match(para):
            lines.append(f"### {para}")
            lines.append("")
            continue

        if ARTICLE_RE.match(para):
            lines.append(para)
            lines.append("")
            continue

        lines.append(para)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def convert(docx_path: Path, output_path: Path) -> None:
    paragraphs = read_paragraphs(docx_path)
    markdown = to_markdown(paragraphs)
    output_path.write_text(markdown, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python tools/docx_to_markdown.py <input.docx> <output.md>")
        return 1

    docx_path = Path(argv[1])
    output_path = Path(argv[2])
    convert(docx_path, output_path)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
