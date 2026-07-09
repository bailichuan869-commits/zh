from __future__ import annotations

import html
import re
import sys
import urllib.parse
import urllib.request


QUERIES = [
    '"中国注册会计师独立性准则第1号" "财会〔2024〕29号"',
    '"中国注册会计师独立性准则第1号" "财会[2024]29号"',
    '"中国注册会计师职业道德守则" "财会"',
    '"中国注册会计师职业道德守则" "财政部"',
    '"中国注册会计师行业发展报告2024"',
    '"中国注册会计师制度恢复重建45周年"',
]


def safe_print(text: str) -> None:
    sys.stdout.buffer.write((text + "\n").encode("utf-8", "replace"))


def main() -> None:
    for query in QUERIES:
        safe_print(f"QUERY {query}")
        url = "https://www.bing.com/search?format=rss&q=" + urllib.parse.quote(query)
        data = urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "ignore")
        for item in re.findall(r"<item>(.*?)</item>", data, re.S)[:10]:
            title = re.search(r"<title>(.*?)</title>", item, re.S)
            link = re.search(r"<link>(.*?)</link>", item, re.S)
            item_title = html.unescape(title.group(1)) if title else ""
            item_link = html.unescape(link.group(1)) if link else ""
            safe_print(f"{item_title} | {item_link}")
        safe_print("---")


if __name__ == "__main__":
    main()
