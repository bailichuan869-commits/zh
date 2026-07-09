from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request


QUERIES = [
    "中国注册会计师职业道德守则 中注协",
    "中国注册会计师职业道德守则 财会 2020",
    "中国注册会计师独立性准则第1号 财务报表审计和审阅业务对独立性的要求 中注协",
    "中国注册会计师独立性准则第1号 应用指南 中注协",
    "中国注册会计师行业发展基础知识 中注协",
    "中国注册会计师协会 行业发展 历史",
]

OFFICIAL_DOMAINS = ("cicpa.org.cn", "mof.gov.cn", "gov.cn")


def main() -> None:
    for query in QUERIES:
        print(f"QUERY {query}")
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
        data = urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "ignore")
        links: list[str] = []
        for match in re.finditer(r'href="(https?://[^"]+)"', data):
            link = html.unescape(match.group(1))
            if any(domain in link for domain in OFFICIAL_DOMAINS) and link not in links:
                links.append(link)
        for link in links[:20]:
            print(link)
        print()


if __name__ == "__main__":
    main()
