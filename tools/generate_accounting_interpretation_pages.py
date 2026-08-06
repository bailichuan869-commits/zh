from __future__ import annotations

import csv
import re
from pathlib import Path

from kb_common import update_frontmatter


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
ACCOUNTING_RAW = KB / "raw" / "standards" / "accounting"
WIKI_DIR = KB / "wiki" / "concepts" / "accounting-standards" / "interpretations"
INDEX_DIR = KB / "raw" / "indexes"

CSV_PATH = ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-interpretations.csv"


INTERPRETATION_SUPPLEMENTS: dict[str, list[str]] = {
    "10": [
        "",
        "## 核心问题",
        "",
        "解释第10号处理固定资产折旧方法能否以使用固定资产的经济活动收入作为折旧基础。原文将判断标准落在固定资产相关经济利益的预期消耗方式，而不是收入金额本身。",
        "",
        "## 规则要点",
        "",
        "- 企业应根据固定资产相关经济利益的预期实现方式选择折旧方法。",
        "- 收入还会受到投入、生产过程和销售等因素影响，这些因素不一定反映固定资产经济利益的消耗，因此不应以包含使用固定资产在内的经济活动收入作为折旧基础。",
        "- 本解释自2018年1月1日起施行，不要求追溯调整；施行前已确认的相关固定资产，自施行日起按重新评估后的折旧方法处理未来期间。",
        "",
        "## 实务核查",
        "",
        "- 获取固定资产用途、产能、使用寿命和运行数据，说明所选折旧方法如何对应经济利益消耗方式。",
        "- 对以收入、销量或合同金额作为折旧驱动因素的安排，拆分收入形成原因，检查是否混入价格、市场需求或销售渠道等非资产消耗因素。",
        "- 检查方法变更的批准、会计估计依据、折旧重算和前后期间衔接，避免把未来适用误写成追溯调整。",
        "",
        "## 关联入口与边界",
        "",
        "- [[concepts/accounting-standards/cas-04|企业会计准则第4号——固定资产]]",
        "- [[concepts/accounting-judgments/fixed-assets-initial-subsequent-provisional|固定资产初始确认、后续支出与暂估转固]]",
        "- 本页是基于财政部原文的结构化摘要；合同事实、资产消耗模式和报告期适用版本仍须人工复核后才能形成正式专业结论。",
    ],
    "11": [
        "",
        "## 核心问题",
        "",
        "解释第11号处理无形资产摊销方法能否以包括使用无形资产在内的经济活动收入作为摊销基础。原文要求先判断无形资产经济利益的预期消耗方式，不能仅用收入变化替代该判断。",
        "",
        "## 规则要点",
        "",
        "- 无形资产摊销方法应反映与该资产有关的经济利益预期实现方式；无法可靠确定时采用直线法。",
        "- 通常不应以相关经济活动收入作为摊销基础，因为收入可能受投入、生产过程和销售等因素影响。",
        "- 例外仅限于极其有限的情形：合同对无形资产作出固有的根本性限制且固定收入总额反映该限制，或有确凿证据证明收入金额与经济利益消耗高度相关。",
        "- 高速公路经营权采用车流量法摊销，不属于以经济活动收入为基础的摊销方法；本解释自2018年1月1日起施行，不要求追溯调整。",
        "",
        "## 实务核查",
        "",
        "- 获取许可、特许经营或技术合同，识别使用期限、产量、固定收入总额等固有约束，并区分固定约束与一般销售收入。",
        "- 对主张收入法或类似方法的项目，保留收入与资产经济利益消耗高度相关的可验证证据，并复核替代方法的合理性。",
        "- 检查方法变更、未来适用和摊销年限重估的审批记录，避免将本解释的生效衔接误处理为以前期间追溯调整。",
        "",
        "## 关联入口与边界",
        "",
        "- [[concepts/accounting-standards/cas-06|企业会计准则第6号——无形资产]]",
        "- [[concepts/accounting-judgments/intangibles-rd-capitalisation|无形资产及研发支出资本化]]",
        "- 本页是基于财政部原文的结构化摘要；合同限制、相关性证据和报告期适用版本仍须人工复核后才能形成正式专业结论。",
    ],
}
VERIFIED_LIFECYCLE = {"20": "valid"}
VERIFIED_DATES: dict[str, dict[str, str]] = {
    "10": {"published_on": "2017-06-12", "effective_from": "2018-01-01"},
    "11": {"published_on": "2017-06-12", "effective_from": "2018-01-01"},
}

CHINESE_SECTION_RE = re.compile(
    r"(?:^|\s{3,})([一二三四五六七八九十百]+)、\s*(.+?)"
    r"(?=\s{3,}(?:[一二三四五六七八九十百]+、|答[:：])|$)"
)
SECTION_CONTINUATION_STOPS = ("（", "(", "答：", "答:", "该问题", "企业在", "企业应", "本解释")


def read_csv(path: Path) -> list[dict[str, str]]:
    source = path
    if not source.exists() and Path(f"{source}.md").exists():
        source = Path(f"{source}.md")
    if source.suffix.lower() != ".md":
        with source.open("r", encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    table_lines = [
        line.strip()
        for line in source.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        if line.strip().startswith("|")
    ]
    if len(table_lines) < 2:
        return []

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    headers = cells(table_lines[0])
    headers[0] = headers[0].lstrip("\ufeff").strip().strip('"')
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        values = cells(line)
        if not values or all(re.fullmatch(r":?-+:?", value or "") for value in values):
            continue
        values.extend([""] * (len(headers) - len(values)))
        rows.append(dict(zip(headers, values[: len(headers)])))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rel(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    try:
        return path.relative_to(KB).as_posix()
    except ValueError:
        return path.as_posix()


def normalize(title: str) -> str:
    return re.sub(r"\s+", "", title).replace("《", "").replace("》", "")


def parse_number(title: str) -> str:
    match = re.search(r"解释第([0-9０-９]+)号", title)
    if not match:
        return ""
    return match.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def short_topic(title: str, number: str) -> str:
    if "——" in title:
        return re.sub(r"》?的通知$", "", title.split("——", 1)[1]).rstrip("》")
    if "关于印发" in title:
        return f"企业会计准则解释第{number}号"
    return title


def page_key(number: str) -> str:
    return f"interp-{int(number):02d}"


def markdown_facade(local_path: str) -> Path | None:
    if not local_path:
        return None
    candidate = KB / Path(local_path.replace("\\", "/"))
    if candidate.exists():
        return candidate
    facade = Path(f"{candidate}.md")
    return facade if facade.exists() else None


def extract_major_topics(local_path: str) -> list[str]:
    facade = markdown_facade(local_path)
    if not facade:
        return []
    lines = facade.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
    topics: list[str] = []
    for index, line in enumerate(lines):
        for match in CHINESE_SECTION_RE.finditer(line):
            topic = match.group(2).strip()
            if not topic:
                continue
            if (
                match.end() == len(line)
                and not topic.endswith(("？", "?", "。", "；", ";", "）"))
                and index + 1 < len(lines)
            ):
                continuation = lines[index + 1].strip()
                if continuation and not continuation.startswith(SECTION_CONTINUATION_STOPS):
                    topic += continuation
            if any(marker in topic for marker in ("生效日期", "本解释自", "本解释中除")):
                continue
            normalized = re.sub(r"\s+", "", topic)
            if normalized and normalized not in topics:
                topics.append(normalized)
    return topics


def write_page(row: dict[str, str], number: str) -> str:
    key = page_key(number)
    page = WIKI_DIR / f"{key}.md"
    title = short_topic(row["Title"], number)
    local_path = rel(row.get("LocalFile", ""))
    topics = extract_major_topics(local_path)
    supplement = INTERPRETATION_SUPPLEMENTS.get(number)
    page_role = "knowledge" if supplement else "index"
    lifecycle = VERIFIED_LIFECYCLE.get(number, "unknown")
    governance: dict[str, object] = {
        "page_role": page_role,
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": f"interpretation-{int(number)}",
        "lifecycle_status": lifecycle,
        "authority_level": "official",
        "raw_path": f"{local_path}.md",
        "source_url": row["Url"],
    }
    governance.update(VERIFIED_DATES.get(number, {}))
    lines = [
        "---",
        f"title: 企业会计准则解释第{number}号",
        "type: concept",
        "concept_type: accounting-interpretation",
        f"page_role: {page_role}",
        "maturity: reviewed",
        "answer_ready: false",
        "review_status: agent-reviewed",
        "created: 2026-06-26",
        "updated: 2026-08-06",
        "sources: [enterprise-accounting-standards-interpretations-download-2026-06-26]",
        f"version: interpretation-{int(number)}",
        f"lifecycle_status: {lifecycle}",
        "authority_level: official",
        f"raw_path: {local_path}.md",
        f"source_url: {row['Url']}",
        "tags: [accounting, standards, interpretation, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-interpretations-download-2026-06-26]]",
        "---",
        "",
        f"# 企业会计准则解释第{number}号",
        "",
        "## 定位",
        "",
        f"- 解释编号：{number}",
        f"- 标题：{title}",
        f"- 本地文件：`{local_path}`",
        f"- 官方链接：{row['Url']}",
        "",
        "## 原文入口",
        "",
        f"- 通知/原文页面：{row['Url']}",
        f"- 本地 HTML：`{local_path}`",
    ]
    if supplement:
        lines.extend(supplement)
    else:
        lines.extend(
            [
                "",
                "## 说明",
                "",
                "本页是解释编号级事项索引，不重复存放财政部完整正文。检索和引用应回到下列事项及原文门面。",
                "",
                "## 事项索引",
                "",
                *([f"- {topic}" for topic in topics] or ["- 事项标题未能稳定提取，请直接查阅上方财政部原文门面。"]),
                "",
                "## 使用边界",
                "",
                "本页仅提供原文定位和事项导航，`agent-reviewed` 不等于人工批准。涉及具体交易时，应回到完整原文、报告期适用版本和交易事实。"
                + (
                    "当前生命周期已有官方注册表证据支持。"
                    if lifecycle != "unknown"
                    else "当前生命周期按 `unknown` 记录，不据此宣称现行有效。"
                ),
            ]
        )
    generated = "\n".join(lines) + "\n"
    base = page.read_text(encoding="utf-8-sig", errors="ignore") if page.exists() else generated
    content = update_frontmatter(base, governance)
    if not page.exists() or content != base:
        page.write_text(content, encoding="utf-8", newline="\n")
    return f"concepts/accounting-standards/interpretations/{key}"


def main() -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(CSV_PATH)
    page_rows: list[dict[str, str]] = []
    for row in rows:
        number = parse_number(normalize(row["Title"]))
        if not number:
            continue
        page_link = write_page(row, number)
        page_rows.append(
            {
                "InterpretationNo": number,
                "Title": row["Title"],
                "Url": row["Url"],
                "LocalPath": rel(row.get("LocalFile", "")),
                "WikiPage": page_link,
            }
        )

    write_csv(INDEX_DIR / "accounting-interpretations-index.csv", page_rows)

    index_lines = [
        "# 企业会计准则解释编号索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 文件",
        "",
        "- 索引 CSV：`raw/indexes/accounting-interpretations-index.csv`",
        "- 解释页目录：`wiki/concepts/accounting-standards/interpretations/`",
        "",
        "## 列表",
        "",
        "| 编号 | 标题 | 页面 |",
        "|---:|---|---|",
    ]
    for row in sorted(page_rows, key=lambda r: int(r["InterpretationNo"])):
        index_lines.append(f"| {row['InterpretationNo']} | {row['Title']} | [[{row['WikiPage']}]] |")
    (INDEX_DIR / "accounting-interpretations-index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"interpretations={len(page_rows)}")


if __name__ == "__main__":
    main()
