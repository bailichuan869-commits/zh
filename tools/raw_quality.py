#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raw_quality.py — 扫描 raw/*.md 的抽取质量，识别空/失效/低质页并产出维护清单。

子命令：
  scan                  扫描并产出报告（默认联网实检 source_url）
  scan --no-check-urls  仅结构扫描，不联网

判定：
  EMPTY             正文 <5 字符，或含转换占位串"（无法从原文件提取可识别文本"
  ERROR_PAGE        正文命中 404 / 页面不存在 / 链接已失效 / 该文档不存在 等错误页特征
  LOW_CONTENT       正文 < 80 字符（告警，非错误）
  MISSING_SOURCE_TYPE  frontmatter 缺 source_type（可经 --clean 自动补）
  OK                正常

URL 实检状态：ALIVE / DEAD(404,410) / BLOCKED(401,403,429 疑似反爬) / ERROR(连接/5xx)
  / UNVERIFIED(出网预检失败，未实检) / NO_URL
  —— 实检前先探测基准站点（baidu/qq）；全部失败判定本机出网被沙箱拦截，
     此时所有 URL 标 UNVERIFIED（而非误判 ERROR），需改用浏览器/内置网络通道人工复核。
     经验教训（2026-07-24）：沙箱环境下 urllib/curl 连百度都连不通，32 条 ERROR 全为误报，
     经内置通道抽查 cicpa/gov.cn/mof/csrc 四域名样本均存活。

产出：
  workspace/outputs/raw_quality_report.json
  workspace/outputs/raw_quality_report.md

用法：
  python tools/raw_quality.py scan
  python tools/raw_quality.py scan --no-check-urls
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

# 复用抽取器的清洗/推断逻辑（不触发 bs4 重依赖）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_raw_to_md import strip_boilerplate, TYPE_MAP  # noqa: E402

ROOT = Path("knowledge-base/CPA-ZH")
RAW = ROOT / "raw"
REPORT_JSON = Path("workspace/outputs/raw_quality_report.json")
REPORT_MD = Path("workspace/outputs/raw_quality_report.md")

EMPTY_PLACEHOLDER = "无法从原文件提取可识别文本"
# 错误页特征：仅用文本短语（数字错误码如 404/500 易误判问题编号、税款金额、URL 片段，已去除）
ERROR_PAGE_RE = re.compile(
    r"页面不存在|链接已失效|该文档不存在|您访问的页面|找不到页面|页面出错|Not Found|文件不存在",
    re.IGNORECASE,
)
# 错误页通常是抓取失败的短消息；长正文里的偶发"404/文件不存在"属正常内容，不误判
ERROR_PAGE_MAX_LEN = 300
LOW_CONTENT_THRESHOLD = 80
SHORT_SOURCE_ROLES = {"index-page", "attachment-landing", "source-registry", "reference-page", "auxiliary-attachment"}
URL_TIMEOUT = 8
URL_DELAY = 0.3
# 连通性预检基准站点：全部失败视为本机出网被拦截（沙箱/防火墙），URL 一律标 UNVERIFIED 而非误判 ERROR
PROBE_URLS = ("https://www.baidu.com", "https://www.qq.com")


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if m:
        fm_raw, body = m.group(1), m.group(2)
        meta = {}
        for line in fm_raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        return meta, body
    return {}, text


# 完整浏览器 UA，用于绕过 401/403/429 反爬拦截的复检
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def _classify(code: int, _method: str) -> tuple[str, int, str]:
    if 200 <= code < 400:
        return "ALIVE", code, ""
    if code in (401, 403, 429):
        return "BLOCKED", code, "疑似反爬拦截"
    if code in (404, 410):
        return "DEAD", code, "页面不存在"
    if 500 <= code < 600:
        return "ERROR", code, "服务端错误"
    return "ALIVE", code, ""


def _do_request(url: str, method: str, ua: str) -> tuple[int, Exception | None]:
    """发起请求，返回 (code, exc)。code=0 表示连接/超时失败。"""
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=URL_TIMEOUT) as resp:
            return resp.getcode(), None
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
        return 0, e


def check_url(url: str) -> tuple[str, str, str]:
    """返回 (status, code, note)。status: ALIVE/DEAD/BLOCKED/ERROR/NO_URL。

    命中 401/403/429 时，自动用完整浏览器 UA 复检一次——若复检 2xx/3xx
    则视为反爬拦截而非真死链，标为 ALIVE（note 注明已绕过）。
    """
    if not url or not url.startswith("http"):
        return "NO_URL", "", "无 source_url"
    last_exc: Exception | None = None
    for method in ("HEAD", "GET"):
        code, exc = _do_request(url, method, "Mozilla/5.0 (quality-check)")
        if exc is not None:
            last_exc = exc
            continue
        status, _c, note = _classify(code, method)
        # 反爬拦截复检
        if status == "BLOCKED":
            rcode, rexc = _do_request(url, "GET", BROWSER_UA)
            if rexc is None and 200 <= rcode < 400:
                return "ALIVE", rcode, "反爬拦截(浏览器UA复检存活)"
        return status, code, note
    return "ERROR", "", f"连接失败：{type(last_exc).__name__}"


def network_available() -> bool:
    """预检本机出网能力：基准站点全部失败 → 判定网络不可用（沙箱拦截）。"""
    for u in PROBE_URLS:
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5):
                return True
        except Exception:
            continue
    return False


def scan(check_urls: bool = True) -> list[dict]:
    net_ok = network_available() if check_urls else False
    if check_urls and not net_ok:
        print("[warn] 出网预检失败（基准站点均不可达）：本机网络被拦截，URL 一律标 UNVERIFIED，请改用浏览器/内置网络通道人工复核。")
    records: list[dict] = []
    checked_urls: dict[str, tuple[str, str, str]] = {}
    for p in sorted(RAW.rglob("*.md")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if "raw/" not in rel:
            continue
        if "_archive" in rel or "_trash" in rel or "_maintenance" in rel:
            continue
        if any(part in ("_archive", "_trash", "_maintenance") for part in p.parts):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        meta, body = split_frontmatter(t)
        body_clean = strip_boilerplate(body)
        body_len = len(body_clean.strip())
        source_role = meta.get("source_role", "content")

        if not body.strip() or EMPTY_PLACEHOLDER in body:
            status = "EMPTY"
        elif body_len <= ERROR_PAGE_MAX_LEN and ERROR_PAGE_RE.search(body_clean):
            status = "ERROR_PAGE"
        elif body_len < LOW_CONTENT_THRESHOLD and source_role not in SHORT_SOURCE_ROLES:
            status = "LOW_CONTENT"
        elif "source_type" not in meta:
            status = "MISSING_SOURCE_TYPE"
        else:
            status = "OK"

        url_status = url_code = url_note = ""
        if check_urls:
            url = meta.get("source_url", "")
            if not url or not url.startswith("http"):
                url_status, url_code, url_note = "NO_URL", "", "无 source_url"
            elif not net_ok:
                url_status, url_code, url_note = "UNVERIFIED", "", "本机出网被拦截，未实检"
            else:
                if url not in checked_urls:
                    checked_urls[url] = check_url(url)
                    time.sleep(URL_DELAY)
                url_status, url_code, url_note = checked_urls[url]

        records.append({
            "path": rel,
            "status": status,
            "body_len": body_len,
            "source_type": meta.get("source_type", ""),
            "source_role": source_role,
            "source_url": meta.get("source_url", ""),
            "url_status": url_status,
            "url_code": str(url_code),
            "url_note": url_note,
        })
    return records


def write_reports(records: list[dict], check_urls: bool) -> None:
    REPORT_JSON.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    by_status: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_status[r["status"]].append(r)
    total = len(records)
    cnt = Counter(r["status"] for r in records)

    lines = [
        f"# Raw 抽取质量报告（{date.today().isoformat()}）",
        "",
        f"- 扫描文件总数：**{total}**",
        f"- 联网 URL 实检：{'是' if check_urls else '否'}",
        "",
        "## 汇总",
    ]
    for st in ("EMPTY", "ERROR_PAGE", "LOW_CONTENT", "MISSING_SOURCE_TYPE", "OK"):
        lines.append(f"- {st}: {cnt.get(st, 0)}")
    lines.append("")

    if check_urls:
        bad = [r for r in records if r["url_status"] in ("DEAD", "ERROR", "BLOCKED")]
        unverified = [r for r in records if r["url_status"] == "UNVERIFIED"]
        lines.append(f"## 失效/异常 URL（{len(bad)}）")
        for r in bad:
            lines.append(f"- [{r['url_status']}] {r['path']} — {r['source_url']} ({r['url_note']})")
        lines.append("")
        if unverified:
            lines.append(f"## 未实检 URL（{len(unverified)}，本机出网被拦截）")
            lines.append("> 需改用浏览器或内置网络通道人工抽查复核。")
            for r in unverified:
                lines.append(f"- {r['path']} — {r['source_url']}")
            lines.append("")

    for st in ("EMPTY", "ERROR_PAGE", "LOW_CONTENT", "MISSING_SOURCE_TYPE"):
        items = by_status.get(st, [])
        if not items:
            continue
        lines.append(f"## {st}（{len(items)}）")
        for r in items:
            extra = f" | {r['body_len']}字" if st == "LOW_CONTENT" else ""
            lines.append(f"- {r['path']}{extra}")
        lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    # 控制台摘要
    print(f"[scan] 总文件 {total}")
    for st in ("EMPTY", "ERROR_PAGE", "LOW_CONTENT", "MISSING_SOURCE_TYPE", "OK"):
        print(f"  {st}: {cnt.get(st, 0)}")
    if check_urls:
        bad = [r for r in records if r["url_status"] in ("DEAD", "ERROR", "BLOCKED")]
        unverified = [r for r in records if r["url_status"] == "UNVERIFIED"]
        print(f"  URL 失效/异常: {len(bad)}")
        if unverified:
            print(f"  URL 未实检(出网被拦截): {len(unverified)}")
    print(f"[report] {REPORT_JSON} / {REPORT_MD}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="扫描 raw/*.md 抽取质量并产出维护清单。")
    ap.add_argument("command", choices=["scan"], help="扫描并产出质量报告")
    ap.add_argument("--no-check-urls", action="store_true", help="不联网实检 source_url")
    args = ap.parse_args()
    if args.command == "scan":
        records = scan(check_urls=not args.no_check_urls)
        write_reports(records, check_urls=not args.no_check_urls)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
