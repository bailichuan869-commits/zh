from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request


QUERIES = [
    "注册会计师全国统一考试办法 财政部令第115号",
    "注册会计师注册办法 财政部令第99号",
    "会计师事务所执业许可和监督管理办法 财政部令第97号",
    "注册会计师行业诚信建设纲要 财会〔2023〕5号",
    "会计师事务所监督检查办法 财办〔2022〕23号",
    "关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见 国办发〔2021〕30号",
]

OFFICIAL_DOMAINS = ("mof.gov.cn", "gov.cn", "cicpa.org.cn")


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
