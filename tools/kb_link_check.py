from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_urls(root: Path, include_wiki: bool) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}

    def add(url: str, source: Path) -> None:
        cleaned = url.rstrip("`。；，,.;")
        found.setdefault(cleaned, set()).add(source.relative_to(root).as_posix())

    registry = root / "source-registry.yml"
    if registry.exists():
        for url in URL_RE.findall(registry.read_text(encoding="utf-8")):
            add(url, registry)

    for manifest_path in (root / "raw").rglob("manifest.json"):
        data = load_json(manifest_path)
        items = data if isinstance(data, list) else data.get("items", [])
        for item in items:
            url = item.get("url") or item.get("source_url")
            if url:
                add(str(url), manifest_path)

    for source_url in (root / "raw").rglob("source-url.txt"):
        text = source_url.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            add(text, source_url)

    if include_wiki:
        for md in (root / "wiki").rglob("*.md"):
            for url in URL_RE.findall(md.read_text(encoding="utf-8", errors="ignore")):
                add(url, md)

    return found


def check_url(url: str, timeout: int) -> tuple[str, str]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "Mozilla/5.0 CPA-ZH link checker"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return str(response.status), response.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 405}:
            get_request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 CPA-ZH link checker"},
            )
            with urllib.request.urlopen(get_request, timeout=timeout) as response:
                return str(response.status), response.headers.get("content-type", "")
        return str(exc.code), exc.reason
    except Exception as exc:  # noqa: BLE001 - CLI should report any connection failure.
        return "ERROR", str(exc)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Collect or check official URLs in CPA-ZH.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--include-wiki", action="store_true", help="Also collect external URLs in wiki pages.")
    parser.add_argument("--check", action="store_true", help="Perform network checks. Default only collects URLs.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout seconds.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    urls = collect_urls(root, args.include_wiki)
    print(f"root={root}")
    print(f"unique_urls={len(urls)}")

    failures = 0
    for url in sorted(urls):
        sources = ", ".join(sorted(urls[url])[:3])
        if args.check:
            status, detail = check_url(url, args.timeout)
            if status == "ERROR" or status.startswith("4") or status.startswith("5"):
                failures += 1
            print(f"{status}\t{url}\t{sources}\t{detail}")
        else:
            print(f"{url}\t{sources}")

    if args.check and failures:
        print(f"\nlink_check_failures={failures}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
