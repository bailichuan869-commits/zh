from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "knowledge-base" / "CPA-ZH" / "raw" / "ethics" / "third-section"

DOCUMENTS = [
    {
        "slug": "professional-ethics-index",
        "title": "中注协专业标准：职业道德规范专题页",
        "document_type": "third-section-official-index",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/history-ethics-independence",
    },
    {
        "slug": "industry-development-report-2024",
        "title": "《中国注册会计师行业发展报告2024》出版发行",
        "document_type": "industry-history-official-page",
        "url": "https://www.cicpa.org.cn/xxfb/vv/202603/t20260317_65861.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/industry-history",
    },
    {
        "slug": "cpa-system-restoration-45th",
        "title": "致敬45年——中国注册会计师制度恢复重建45周年宣传片正式发布",
        "document_type": "industry-history-official-page",
        "url": "https://www.cicpa.org.cn/xxfb/vv/202601/t20260104_65781.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/industry-history",
    },
    {
        "slug": "industry-reform-development-45th",
        "title": "庆祝中国注册会计师制度恢复重建暨行业改革发展45周年",
        "document_type": "industry-history-official-page",
        "url": "https://www.cicpa.org.cn/xxfb/vv/202512/t20251224_65760.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/industry-history",
    },
    {
        "slug": "ethics-code-2020-notice",
        "title": "中国注册会计师协会关于印发《中国注册会计师职业道德守则（2020）》和《中国注册会计师协会非执业会员职业道德守则（2020）》的通知",
        "document_type": "ethics-code-official-notice",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/t20201218_60661.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-release-2009",
        "title": "中注协发布《中国注册会计师职业道德守则》全面推进行业诚信建设",
        "document_type": "ethics-code-release-page",
        "url": "http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/200911/t20091119_233779.htm",
        "official_source": "财政部",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-no1-basic-principles",
        "title": "中国注册会计师职业道德守则第1号——职业道德基本原则",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760737907.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-no2-conceptual-framework",
        "title": "中国注册会计师职业道德守则第2号——职业道德概念框架",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760753750.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-no3-professional-services",
        "title": "中国注册会计师职业道德守则第3号——提供专业服务的具体要求",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760769913.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-no4-audit-review-independence-superseded",
        "title": "中国注册会计师职业道德守则第4号——审计和审阅业务对独立性的要求",
        "document_type": "ethics-code-pdf-superseded",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760795103.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-no5-other-assurance-independence",
        "title": "中国注册会计师职业道德守则第5号——其他鉴证业务对独立性的要求",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760818391.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-glossary",
        "title": "中国注册会计师职业道德守则术语表",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760830251.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-non-practicing-members",
        "title": "中国注册会计师协会非执业会员职业道德守则",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760835552.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "ethics-code-2020-non-practicing-members-glossary",
        "title": "中国注册会计师协会非执业会员职业道德守则术语表",
        "document_type": "ethics-code-pdf",
        "url": "https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760840794.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/ethics-code",
    },
    {
        "slug": "independence-standard-2024-29",
        "title": "关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》的通知",
        "document_no": "财会〔2024〕29号",
        "document_type": "independence-standard-official-page",
        "url": "http://kjs.mof.gov.cn/zhengcefabu/202501/t20250120_3952051.htm",
        "official_source": "财政部",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-standard-2024-29-mof-page",
        "title": "关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》的通知",
        "document_no": "财会〔2024〕29号",
        "document_type": "independence-standard-official-page",
        "url": "http://kjs.mof.gov.cn/zhengcefabu/202501/t20250120_3952051.htm",
        "official_source": "财政部",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-standard-2024-29-cicpa-page",
        "title": "财政部印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》",
        "document_no": "财会〔2024〕29号",
        "document_type": "independence-standard-official-page",
        "url": "https://cicpa.org.cn/xxfb/news/202501/t20250120_65225.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-standard-2024-29-pdf",
        "title": "中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求",
        "document_no": "财会〔2024〕29号",
        "document_type": "independence-standard-pdf",
        "url": "https://cicpa.org.cn/xxfb/news/202501/W020250120543364207300.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-standard-qa-2025",
        "title": "中注协有关负责人就印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》答记者问",
        "document_type": "independence-standard-official-qa",
        "url": "http://www.mof.gov.cn/zhengwuxinxi/zhengcejiedu/202501/t20250120_3952078.htm",
        "official_source": "财政部",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-application-guide-2026-page",
        "title": "中国注册会计师协会关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南的通知",
        "document_type": "independence-application-guide-official-page",
        "url": "https://cicpa.org.cn/xxfb/tzgg/202602/t20260213_65821.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-application-guide-2026-pdf",
        "title": "《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南",
        "document_type": "independence-application-guide-pdf",
        "url": "https://cicpa.org.cn/xxfb/tzgg/202602/W020260213545051441275.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-application-guide-exposure-2025",
        "title": "中国注册会计师独立性准则第1号应用指南（征求意见稿）通知",
        "document_type": "independence-application-guide-exposure-page",
        "url": "https://www.cicpa.org.cn/xxfb/tzgg/202504/t20250430_65411.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-application-guide-exposure-2025-page",
        "title": "中国注册会计师独立性准则第1号应用指南（征求意见稿）通知",
        "document_type": "historical-exposure-page",
        "url": "https://www.cicpa.org.cn/xxfb/tzgg/202504/t20250430_65411.html",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
    },
    {
        "slug": "independence-application-guide-exposure-2025-pdf",
        "title": "《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南（征求意见稿）",
        "document_type": "independence-application-guide-exposure-pdf",
        "url": "https://www.cicpa.org.cn/xxfb/tzgg/202504/W020250430561278327827.pdf",
        "official_source": "中国注册会计师协会",
        "wiki_page": "concepts/independence-standard-1",
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
        with urllib.request.urlopen(request, timeout=45) as response:
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

    (RAW_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"archived={len(manifest)}")
    for item in manifest:
        print(f"{item['slug']} {item['bytes']} {item['local_file']}")


if __name__ == "__main__":
    main()
