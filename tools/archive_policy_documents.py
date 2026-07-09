from __future__ import annotations

import json
import re
import urllib.request
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "knowledge-base" / "CPA-ZH" / "raw" / "policies" / "second-section"

DOCUMENTS = [
    {
        "slug": "caihui-supervision-2023-4",
        "title": "关于进一步加强财会监督工作的意见",
        "document_no": "中办发〔2023〕4号",
        "url": "https://www.gov.cn/zhengce/2023-02/15/content_5741628.htm",
        "official_source": "中国政府网",
        "wiki_page": "concepts/policy-caihui-supervision",
    },
    {
        "slug": "audit-order-2021-30",
        "title": "关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见",
        "document_no": "国办发〔2021〕30号",
        "url": "https://www.gov.cn/zhengce/content/2021-08/23/content_5632714.htm",
        "official_source": "中国政府网",
        "wiki_page": "concepts/policy-audit-order",
    },
    {
        "slug": "cpa-exam-2024-115",
        "title": "注册会计师全国统一考试办法",
        "document_no": "财政部令第115号",
        "url": "https://www.gov.cn/gongbao/2024/issue_11286/202404/content_6945588.html",
        "official_source": "中国政府网国务院公报",
        "wiki_page": "concepts/policy-cpa-exam",
    },
    {
        "slug": "cpa-registration-2019-99",
        "title": "注册会计师注册办法",
        "document_no": "财政部令第99号",
        "url": "https://www.mof.gov.cn/gkml/caizhengwengao/wg201901/wg201912/202005/t20200522_3518260.htm",
        "official_source": "财政部",
        "wiki_page": "concepts/policy-cpa-registration",
    },
    {
        "slug": "firm-license-supervision-2019-97",
        "title": "会计师事务所执业许可和监督管理办法",
        "document_no": "财政部令第97号",
        "url": "https://www.gov.cn/gongbao/content/2019/content_5392297.htm",
        "official_source": "中国政府网国务院公报",
        "wiki_page": "concepts/policy-firm-license-supervision",
    },
    {
        "slug": "integrity-2023-5",
        "title": "注册会计师行业诚信建设纲要",
        "document_no": "财会〔2023〕5号",
        "url": "https://www.gov.cn/zhengce/zhengceku/2023-04/02/content_5749779.htm",
        "official_source": "中国政府网",
        "wiki_page": "concepts/policy-integrity",
    },
    {
        "slug": "firm-inspection-2022-23",
        "title": "会计师事务所监督检查办法",
        "document_no": "财办〔2022〕23号",
        "url": "https://www.gov.cn/zhengce/zhengceku/2022-05/16/content_5690682.htm",
        "official_source": "中国政府网",
        "wiki_page": "concepts/policy-firm-inspection",
    },
]


def suffix_for_url(url: str) -> str:
    lowered = url.lower()
    if lowered.endswith(".pdf"):
        return ".pdf"
    if lowered.endswith(".doc") or lowered.endswith(".docx"):
        return Path(lowered).suffix
    return ".html"


def main() -> None:
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for doc in DOCUMENTS:
        doc_dir = RAW_ROOT / doc["slug"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        suffix = suffix_for_url(doc["url"])
        raw_file = doc_dir / f"official{suffix}"

        request = urllib.request.Request(
            doc["url"],
            headers={"User-Agent": "Mozilla/5.0 CPA-ZH knowledge-base archiver"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()
            content_type = response.headers.get("content-type", "")
        raw_file.write_bytes(content)

        metadata = {
            **doc,
            "archived_on": date.today().isoformat(),
            "content_type": content_type,
            "bytes": len(content),
            "local_file": str(raw_file.relative_to(ROOT)).replace("\\", "/"),
        }
        (doc_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (doc_dir / "source-url.txt").write_text(doc["url"] + "\n", encoding="utf-8")
        manifest.append(metadata)

    manifest_path = RAW_ROOT / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"archived={len(manifest)}")
    for item in manifest:
        print(f"{item['slug']} {item['bytes']} {item['local_file']}")


if __name__ == "__main__":
    main()
