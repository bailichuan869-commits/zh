from __future__ import annotations

import csv
import html
import re
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Iterable

from kb_common import parse_frontmatter, update_frontmatter


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
AUDIT_RAW = KB / "raw" / "standards" / "audit"
INDEX_DIR = KB / "raw" / "indexes"
WIKI_DIR = KB / "wiki" / "concepts" / "audit-standards"

DIRECT_PDFS = AUDIT_RAW / "downloaded-cicpa-professional-standards-pdfs.csv"
TOPIC_ITEMS = AUDIT_RAW / "cicpa-professional-standards-topic-items.csv"
GUIDELINES_34_HTML = AUDIT_RAW / "cicpa-guidelines-34-20230410.html"
ZIP_DIR = AUDIT_RAW / "archives" / "2023-23-audit-standards"


TYPE_LABELS = {
    "standard": "准则原文",
    "guideline": "应用指南",
    "topic_entry": "专题条目",
    "archive_pdf": "ZIP解压准则",
}


AUDIT_SUPPLEMENTS: dict[str, list[str]] = {
    "csa-1311": [
        "## 实务定位",
        "",
        "本页用于把存货、诉讼和索赔、分部信息等特定项目的证据要求接入审计项目计划。不同项目的重大错报风险、证据来源和专家参与程度可能不同，不能用单一程序替代具体风险评估。",
        "",
        "## 重点任务",
        "",
        "- 存货：结合盘点安排、存货地点、截止性、所有权和跌价迹象设计观察与替代程序。",
        "- 诉讼和索赔：取得管理层清单、律师函或法律沟通资料，核对案件状态、金额、预计损失和披露。",
        "- 分部信息：将分部划分、内部交易抵销、收入成本和资产负债数据与总账及合并报表勾稽。",
        "",
        "## 证据与输出",
        "",
        "底稿应记录项目范围、风险判断、程序执行、异常事项、未解决差异和结论依据。应用指南原文与项目事实不一致时，应保留差异说明并升级复核。",
    ],
    "csa-1331": [
        "## 实务定位",
        "",
        "首次审计业务的核心是为期初余额和比较期间信息取得充分、适当的审计证据，并处理前任注册会计师、会计政策连续性和期初错报之间的衔接。",
        "",
        "## 重点任务",
        "",
        "- 了解前任审计、上期财务报表和上期审计报告，识别可能影响本期的保留事项和未更正错报。",
        "- 检查期初余额是否已正确结转，重大会计政策是否连续，必要时对存货、固定资产、长期合同和金融工具实施替代程序。",
        "- 对无法取得充分证据的重大期初余额，评估对审计范围、审计意见和治理层沟通的影响。",
        "",
        "## 证据与输出",
        "",
        "保存前任沟通、上期报告、期初余额勾稽、替代程序、差异评价和意见影响分析；不得仅以本期发生额测试替代所有期初余额证据。",
    ],
    "csa-1503": [
        "## 实务定位",
        "",
        "强调事项段和其他事项段是审计报告中的特定沟通位置。它们不能替代应发表的非无保留意见，也不能替代管理层在财务报表中的确认、计量和披露责任。",
        "",
        "## 重点任务",
        "",
        "- 先判断事项是否已经在财务报表中充分披露，以及是否需要改变审计意见类型。",
        "- 区分与理解财务报表使用者相关的重大事项和与审计业务、比较信息或报告结构相关的其他事项。",
        "- 将拟沟通事项与治理层沟通、关键审计事项和审计报告草稿交叉核对，保持表述、位置和引用一致。",
        "",
        "## 证据与输出",
        "",
        "底稿应保留事项识别、披露核对、意见类型判断、治理层沟通和报告用语复核记录；最终表述以适用审计准则和项目报告版本为准。",
    ],
    "csa-1602": [
        "## 实务定位",
        "",
        "验资业务关注出资、注册资本及相关变更事项的真实性、合法性和可验证性。业务范围、报告对象和证据要求应先依据委托目的和适用业务准则确定。",
        "",
        "## 重点任务",
        "",
        "- 核对出资人、出资方式、出资期限、银行流水、验资账户和工商登记或变更文件。",
        "- 对货币、实物、知识产权或其他非货币资产出资，分别检查权属、评估、交付、计价和限制条件。",
        "- 对资金回流、借款代垫、关联方安排和验资后立即转出等异常事项实施延伸核查。",
        "",
        "## 证据与输出",
        "",
        "形成资金链、权属链和登记链的勾稽表，记录限制事项、异常交易、未获取资料及其对报告结论的影响；不得把银行余额证明单独视为完整出资证据。",
    ],
    "csa-1611": [
        "## 实务定位",
        "",
        "商业银行财务报表审计需要把金融工具、信用风险、流动性风险、监管指标和表外业务放在同一风险框架中。银行业务数据量大，抽样和模型审计必须与内部控制测试相互衔接。",
        "",
        "## 重点任务",
        "",
        "- 关注贷款及垫款、投资、同业业务、表外承诺、利息收入、预期信用损失和公允价值计量。",
        "- 了解授信审批、风险分类、核销、抵债资产、资金交易和监管报送流程，检查系统数据到总账及披露的接口。",
        "- 对模型、估值、抵押物和法律权利依赖专家或内部审计时，明确专家工作范围和审计师责任。",
        "",
        "## 证据与输出",
        "",
        "底稿应连接业务系统样本、合同与抵押资料、函证、模型参数、监管报表、总账和附注披露；重大估计不确定性和流动性风险应单独形成结论备忘录。",
    ],
    "crs-2101": [
        "## 实务定位",
        "",
        "财务报表审阅是与审计不同的鉴证业务，程序重点通常围绕询问和分析程序展开，结论表达不能扩张为审计意见或保证不存在所有重大错报。",
        "",
        "## 重点任务",
        "",
        "- 明确业务约定、报表期间、适用财务报告框架和预期使用者。",
        "- 通过询问、分析和必要的追加程序识别重大错报迹象，对异常波动和不一致信息追查原因。",
        "- 对管理层未更正事项、范围限制和财务报表修订评估其对审阅结论及报告的影响。",
        "",
        "## 证据与输出",
        "",
        "保留询问对象、分析基准、异常事项、追加程序和报告结论之间的对应关系，并在报告中清楚区分审阅提供的保证程度。",
    ],
    "coa-3111": [
        "## 实务定位",
        "",
        "预测性财务信息审核关注编制基础、关键假设、预测期间和呈现方式。审核证据支持的是假设和编制过程是否有合理基础，不是保证预测结果一定实现。",
        "",
        "## 重点任务",
        "",
        "- 区分基于最佳估计的预测与基于假设情景的预计，检查假设与历史数据、行业信息和管理层计划的一致性。",
        "- 复核收入、成本、资本性支出、融资、税费和营运资金等关键驱动因素，实施敏感性和反向压力分析。",
        "- 检查预测性财务信息的列报、期间、比较基础和重要假设披露，评价重大不确定性是否被遮蔽。",
        "",
        "## 证据与输出",
        "",
        "保存模型版本、假设来源、计算复核、管理层批准和报告日后信息；将事实基础、假设局限和报告措辞分开记录。",
    ],
    "crs-svc-4101": [
        "## 实务定位",
        "",
        "商定程序业务由业务相关方共同确定程序，注册会计师报告执行程序和事实发现，不对整体财务信息发表审计或审阅结论。",
        "",
        "## 重点任务",
        "",
        "- 在业务约定中明确程序、对象、期间、样本、允许的偏差和报告使用范围。",
        "- 按约定程序逐项执行并记录实际结果；发现超出约定范围的事项时先沟通，不擅自扩大结论。",
        "- 将事实发现与管理层提供的资料、原始凭证和计算表逐项勾稽，避免使用带有保证性质的结论性措辞。",
        "",
        "## 证据与输出",
        "",
        "报告应让使用者能够复现已执行程序和事实发现，并明确业务不提供审计或审阅保证；未执行的程序不得在报告中暗示已经完成。",
    ],
    "crs-svc-4111": [
        "## 实务定位",
        "",
        "代编财务信息业务以管理层提供的信息为基础进行收集、分类和呈现，注册会计师不承担管理层编制和治理职责，也不因此获得审计或审阅保证。",
        "",
        "## 重点任务",
        "",
        "- 明确财务信息编制基础、期间、报表范围、资料来源和管理层责任。",
        "- 检查资料是否完整、分类是否一致、计算和格式是否存在明显矛盾；发现重大缺失或不合理信息时要求澄清或修订。",
        "- 区分代编工作与鉴证、咨询或管理决策，避免替管理层作出会计政策选择而不保留其责任记录。",
        "",
        "## 证据与输出",
        "",
        "保存管理层提供资料、关键沟通、调整清单和最终财务信息版本；报告中明确代编性质、管理层责任和不提供保证的边界。",
    ],
    "assurance-basic": [
        "## 实务定位",
        "",
        "鉴证业务基本准则是审计、审阅和其他鉴证业务的共同框架，核心是明确责任主体、预期使用者、鉴证对象、评价标准、证据和报告之间的关系。",
        "",
        "## 重点任务",
        "",
        "- 在承接阶段确认鉴证对象、适用标准、责任方和预期使用者，检查业务是否具备合理基础。",
        "- 按风险设计证据程序，评价证据的充分性和适当性，处理管理层声明、专家工作和相互矛盾的信息。",
        "- 根据保证程度和结论类型编制报告，清楚区分合理保证、有限保证和不提供保证的服务。",
        "",
        "## 证据与输出",
        "",
        "底稿应把业务约定、对象标准、风险、证据、责任方声明和报告结论逐项勾稽；具体业务仍须回到对应准则和项目事实。",
    ],
    "csa-1142": [
        "## 实务定位",
        "",
        "财务报表审计中对法律法规的考虑，重点是识别违反法律法规可能导致的重大错报、处罚、诉讼、持续经营或报告影响，并区分直接影响金额的法规与主要影响经营许可或披露的法规。",
        "",
        "## 重点任务",
        "",
        "- 了解行业监管、许可、税务、环保、劳动、安全和证券发行等与被审计单位相关的法规环境。",
        "- 通过询问管理层、检查监管沟通、处罚记录、律师函和会议纪要识别不合规迹象。",
        "- 对发现或怀疑的违反法规事项追加程序，评估会计处理、或有事项、持续经营、治理层沟通和审计报告影响。",
        "",
        "## 证据与输出",
        "",
        "记录法规来源、事实、法律意见、管理层处理和审计师判断；不能把没有发现违规事项等同于已经证明不存在违规。",
    ],
    "csa-1241": [
        "## 实务定位",
        "",
        "被审计单位使用服务机构时，审计师需要理解服务机构提供的业务、对财务报告相关控制的影响以及使用服务机构报告或替代程序的条件。",
        "",
        "## 重点任务",
        "",
        "- 识别服务机构处理的交易、账户和披露，了解数据接口、权限、变更和异常处理控制。",
        "- 判断服务机构报告的类型、期间和覆盖范围，检查报告是否包含控制设计、运行有效性及例外事项信息。",
        "- 对报告覆盖不足、控制缺陷或高风险流程实施现场、替代或追加程序，并评价对总体风险的影响。",
        "",
        "## 证据与输出",
        "",
        "保存服务合同、流程和控制了解、报告评估、替代程序、例外事项和与管理层沟通的记录；不得只凭服务机构名称降低风险评价。",
    ],
    "csa-1251": [
        "## 实务定位",
        "",
        "识别出的错报需要从单项、汇总、性质、原因和对财务报表使用者的影响进行综合评价，并与重要性、管理层调整和审计意见判断相连接。",
        "",
        "## 重点任务",
        "",
        "- 按性质和金额记录除明显微小事项以外的错报，区分事实错报、判断错报和抽样推断错报。",
        "- 将已更正和未更正错报汇总，评价单项错报、汇总错报、前期错报和可能的管理层偏向。",
        "- 向管理层和治理层沟通错报，检查更正后的报表和附注，并评估未更正错报对审计意见的影响。",
        "",
        "## 证据与输出",
        "",
        "底稿应保留错报来源、调整分录、重要性比较、汇总评价、管理层回应和最终意见影响，不能只保留净额结果。",
    ],
    "csa-1301": [
        "## 实务定位",
        "",
        "审计证据是支持审计结论的基础。证据评价应同时考虑充分性、适当性、相关性、可靠性和不同来源之间的一致性，不能只按资料数量判断。",
        "",
        "## 重点任务",
        "",
        "- 根据认定和风险选择检查、观察、询问、函证、重新计算、重新执行和分析程序的组合。",
        "- 评价外部证据、系统生成数据、管理层编制资料和专家工作的可靠性，检查资料完整性与权限控制。",
        "- 对相互矛盾的信息、异常样本和无法取得资料的事项实施追加程序，并记录对风险和意见的影响。",
        "",
        "## 证据与输出",
        "",
        "每项结论都应能回溯到程序、样本、原始资料、异常处理和复核人；高风险判断应保留反向证据和未解决事项。",
    ],
    "csa-1312": [
        "## 实务定位",
        "",
        "函证程序用于从外部来源获取与账户余额、交易和合同条款有关的审计证据。函证的可靠性取决于设计、控制、发出和回收全过程，而不是回函数量。",
        "",
        "## 重点任务",
        "",
        "- 根据风险、认定和总体程序确定函证对象、内容、期间、样本和积极或消极函证方式。",
        "- 保持对函证过程的控制，核对地址、联系人、发函渠道、回函来源和异常回复。",
        "- 对未回函、退回、差异和可疑回函设计替代程序，追查关联方、期后收款和合同条款。",
        "",
        "## 证据与输出",
        "",
        "底稿应记录函证总体、选择依据、发收控制、回函评价、替代程序和异常结论；管理层拒绝函证时要评估理由及范围影响。",
    ],
    "csa-1313": [
        "## 实务定位",
        "",
        "分析程序通过财务和非财务信息之间的合理关系识别异常、支持实质性结论并在完成阶段形成总体复核。程序有效性取决于预期精度和数据可靠性。",
        "",
        "## 重点任务",
        "",
        "- 建立独立或可验证的预期，明确比较期间、预算、行业指标、业务驱动因素和可接受差异。",
        "- 评价数据来源、完整性、可比性和分解程度，针对重大差异询问并取得佐证。",
        "- 在总体复核阶段识别此前未发现的异常关系，并将结果反馈到风险、估计和追加程序。",
        "",
        "## 证据与输出",
        "",
        "保存预期模型、数据来源、阈值、差异解释、追加程序和结论；不能用事后解释替代事前可验证的预期。",
    ],
    "csa-1314": [
        "## 实务定位",
        "",
        "审计抽样通过从总体中选取具有代表性的项目，对控制偏差或金额错报作出结论。抽样风险、非抽样风险、总体界定和样本选择必须在底稿中清楚呈现。",
        "",
        "## 重点任务",
        "",
        "- 明确审计目标、总体、抽样单元、可接受风险、可容忍错报或偏差和预期错报。",
        "- 选择能够代表总体的样本，执行替代程序并记录无法检查项目、偏差和异常项目。",
        "- 将样本结果投射到总体，结合偏差性质、金额、原因和其他程序评价是否需要扩大样本或修改风险。",
        "",
        "## 证据与输出",
        "",
        "底稿应让复核人重现总体、样本、程序、例外、投射和结论；样本数量本身不能证明抽样结论可靠。",
    ],
    "csa-1323": [
        "## 实务定位",
        "",
        "关联方和关联方交易具有隐蔽性、非正常商业条款和管理层操纵风险。审计重点是完整识别关系和交易，并评价会计处理及披露是否充分。",
        "",
        "## 重点任务",
        "",
        "- 获取关联方清单、股权和控制结构、董事高管关系、重大合同及治理层会议资料。",
        "- 将总账、银行流水、往来、担保、资金占用、异常供应商客户和期后交易与清单交叉比对。",
        "- 对超出正常经营范围或缺少商业理由的交易检查授权、定价、资金流、会计处理和披露。",
        "",
        "## 证据与输出",
        "",
        "保留关联方识别过程、完整性测试、管理层声明、治理层沟通和披露核对；不能仅依据管理层提供的名单排除未披露关系。",
    ],
    "csa-1401": [
        "## 实务定位",
        "",
        "集团财务报表审计需要在集团层面评价重大错报风险，并协调组成部分注册会计师、合并过程和集团层面控制。集团项目合伙人对集团审计结论承担总体责任。",
        "",
        "## 重点任务",
        "",
        "- 了解集团结构、组成部分、共享服务、内部交易和合并调整，确定重要组成部分及其审计范围。",
        "- 向组成部分审计团队下达指令，统一重要性、风险沟通、截止日和报告要求，评价其胜任能力和独立性。",
        "- 检查合并抵销、未审组成部分、集团层面调整和跨组成部分异常事项，并完成集团层面分析。",
        "",
        "## 证据与输出",
        "",
        "保存集团审计策略、组成部分清单、指令与回报、沟通记录、合并底稿和集团层面复核；组成部分报告不能自动替代集团审计师的评价。",
    ],
}


NOTICE_URLS = {
    "2022-鉴证业务基本准则等15项应用指南": "https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63335.html",
    "2022-鉴证业务基本准则等11项准则": "https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63336.html",
    "2023-重大错报风险识别和评估等准则": "https://www.cicpa.org.cn/xxfb/tzgg/202301/t20230103_63902.html",
    "2023-34项审计准则应用指南": "https://www.cicpa.org.cn/xxfb/tzgg/202304/t20230410_64066.html",
}

NOTICE_DATES = {
    NOTICE_URLS["2022-鉴证业务基本准则等15项应用指南"]: "2022-01-20",
    NOTICE_URLS["2022-鉴证业务基本准则等11项准则"]: "2022-01-20",
    NOTICE_URLS["2023-重大错报风险识别和评估等准则"]: "2023-01-03",
    NOTICE_URLS["2023-34项审计准则应用指南"]: "2023-04-10",
}

AUDIT_INDEX_SOURCE_ID = "cicpa-professional-standards-number-index-2026-06-26"
GOVERNANCE_UPDATED = "2026-08-06"


STANDARD_RE = re.compile(
    r"中国注册会计师(?P<family>审计准则|审阅准则|其他鉴证业务准则|相关服务准则|鉴证业务准则|质量管理准则|独立性准则|职业道德守则|可持续信息鉴证业务准则)"
    r"第\s*(?P<number>[0-9０-９Xx]+)\s*号(?:[—\-－]+(?P<name>[^》\)\]（(]*))?"
)


def fullwidth_to_ascii(text: str) -> str:
    return text.translate(str.maketrans("０１２３４５６７８９", "0123456789"))


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


def rel(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    try:
        return path.relative_to(KB).as_posix()
    except ValueError:
        return path.as_posix()


def clean_text(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"^[0-9０-９]+[\.．、]?", "", text)
    return text.strip()


def strip_title(title: str) -> str:
    title = clean_text(title)
    title = title.replace("》《", "》 《")
    return title


def parse_standard(title: str) -> tuple[str, str, str]:
    text = fullwidth_to_ascii(strip_title(title))
    if "中国注册会计师鉴证业务基本准则" in text and "第" not in text:
        return "assurance-basic", "鉴证业务基本准则", "中国注册会计师鉴证业务基本准则"
    match = STANDARD_RE.search(text)
    if not match:
        return "", "", ""
    family = match.group("family")
    number = match.group("number").upper()
    name = (match.group("name") or "").strip()
    if "应用指南" in name:
        name = name.replace("应用指南", "")
    key_prefix = {
        "审计准则": "csa",
        "审阅准则": "crs",
        "其他鉴证业务准则": "coa",
        "相关服务准则": "crs-svc",
        "鉴证业务准则": "cabs",
        "质量管理准则": "cqms",
        "独立性准则": "independence",
        "职业道德守则": "ethics",
        "可持续信息鉴证业务准则": "sustainability-assurance",
    }.get(family, "standard")
    key = f"{key_prefix}-{number.lower()}"
    title_base = f"中国注册会计师{family}第{number}号"
    if name:
        title_base += f"——{name}"
    return key, family, title_base


def infer_source_type(title: str, group: str, local_path: str) -> str:
    text = f"{title} {group} {local_path}"
    if "应用指南" in text:
        return "guideline"
    if "ZIP" in group or "2023-23" in local_path:
        return "archive_pdf"
    return "standard"


def parse_guidelines_34_titles() -> dict[str, str]:
    if not GUIDELINES_34_HTML.exists():
        return {}
    raw = GUIDELINES_34_HTML.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(r'<a\s+[^>]*href="\./(?P<file>W[^"]+\.pdf)"[^>]*>(?P<label>.*?)</a>', re.I | re.S)
    title_by_file: dict[str, str] = {}
    for match in pattern.finditer(raw):
        file_name = match.group("file")
        label = clean_text(match.group("label"))
        if not label:
            continue
        existing = title_by_file.get(file_name, "")
        if "准则第" in label or "鉴证业务基本准则" in label:
            title_by_file[file_name] = label
        elif not existing:
            title_by_file[file_name] = label
    return title_by_file


def pdf_article_id(url: str) -> str:
    match = re.search(r"/([^/]+\.pdf)$", url, re.I)
    return match.group(1) if match else url


def make_record(
    source_type: str,
    title: str,
    group: str,
    url: str,
    local_path: str,
    status: str = "",
    source_note: str = "",
) -> dict[str, str]:
    key, family, standard_title = parse_standard(title)
    return {
        "StandardKey": key or "unmapped",
        "StandardFamily": family,
        "StandardTitle": standard_title,
        "SourceType": source_type,
        "SourceTypeLabel": TYPE_LABELS[source_type],
        "Title": strip_title(title),
        "Group": group,
        "Url": url,
        "LocalPath": rel(local_path),
        "Status": status,
        "SourceNote": source_note,
        "MappingMethod": "title-standard-number" if key else "unmapped",
        "Confidence": "high" if key else "low",
    }


def load_direct_pdf_records() -> list[dict[str, str]]:
    rows = []
    title_by_pdf = parse_guidelines_34_titles()
    for row in read_csv(DIRECT_PDFS):
        title = row.get("Title", "")
        url = row.get("Url", "")
        pdf_name = pdf_article_id(url)
        title_is_only_seq = bool(re.fullmatch(r"\s*[0-9０-９]+[\.．]?\s*", title or ""))
        if pdf_name in title_by_pdf and (title_is_only_seq or not parse_standard(title)[0]):
            title = title_by_pdf[pdf_name]
        group = row.get("Group", "")
        local_path = row.get("LocalFile", "")
        source_type = infer_source_type(title, group, local_path)
        rows.append(
            make_record(
                source_type=source_type,
                title=title,
                group=group,
                url=url,
                local_path=local_path,
                status=row.get("Status", ""),
                source_note="direct-pdf-csv",
            )
        )
    return rows


def load_archive_pdf_records() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not ZIP_DIR.exists():
        return rows
    for path in sorted(ZIP_DIR.rglob("*.pdf")):
        title = path.stem
        if "." in title:
            title = title.split(".", 1)[1]
        title = re.sub(r"（?2022年12月22日修订）?", "", title)
        rows.append(
            make_record(
                source_type="archive_pdf",
                title=title,
                group="2023-23项审计准则ZIP解压",
                url=NOTICE_URLS["2023-重大错报风险识别和评估等准则"],
                local_path=str(path),
                status="ok",
                source_note="zip-extracted-pdf",
            )
        )
    return rows


def load_topic_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    if not TOPIC_ITEMS.exists():
        return records
    for row in read_csv(TOPIC_ITEMS):
        title = row.get("Title", "")
        key, _, _ = parse_standard(title)
        if not key:
            continue
        records.append(
            make_record(
                source_type="topic_entry",
                title=title,
                group="中注协执业准则专题条目",
                url=row.get("Url", ""),
                local_path="",
                status=row.get("Date", ""),
                source_note="topic-entry",
            )
        )
    return records


def row_preference(row: dict[str, str]) -> tuple[int, int]:
    type_score = {"standard": 4, "archive_pdf": 3, "guideline": 2, "topic_entry": 1}.get(row["SourceType"], 0)
    path_score = 1 if row["LocalPath"] else 0
    return type_score, path_score


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    best: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if row["StandardKey"] == "unmapped":
            key = (row["SourceType"], row["StandardKey"], row["Title"] or row["LocalPath"])
        else:
            key = (row["SourceType"], row["StandardKey"], pdf_article_id(row["Url"]) or row["Title"])
        current = best.get(key)
        if current is None or row_preference(row) > row_preference(current):
            best[key] = row
    return list(best.values())


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def page_role_for_key(key: str) -> str:
    """Only pages with an editorial practice framework are answer-bearing candidates."""
    return "knowledge" if key in AUDIT_SUPPLEMENTS else "index"


def notice_date_for_rows(rows: list[dict[str, str]]) -> str:
    for row in rows:
        if row.get("Url") in NOTICE_DATES:
            return NOTICE_DATES[row["Url"]]
    for row in rows:
        group = row.get("Group", "")
        if group.startswith("2022-鉴证业务基本准则等15项应用指南"):
            return "2022-01-20"
        if group.startswith("2022-鉴证业务基本准则等11项准则"):
            return "2022-01-20"
        if group.startswith("2023-34项审计准则应用指南"):
            return "2023-04-10"
        if group.startswith("2023-23项审计准则"):
            return "2023-01-03"
    return "unknown"


def primary_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return max(rows, key=row_preference)


def audit_governance_metadata(
    key: str,
    rows: list[dict[str, str]],
    body: str,
) -> dict[str, object]:
    source = primary_row(rows) if rows else {}
    local_path = source.get("LocalPath", "")
    return {
        "page_role": page_role_for_key(key),
        "maturity": "reviewed",
        "asset_id": f"cpa-zh:audit-standard:{key}",
        "source_id": f"cicpa-audit-standard:{key}",
        "knowledge_type": "audit-standard",
        "source_type": source.get("SourceType", "audit-standard") or "audit-standard",
        "version": "unknown",
        "published_on": notice_date_for_rows(rows),
        "effective_from": "unknown",
        "effective_to": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": local_path or "unknown",
        "markdown_path": "unknown",
        "source_url": source.get("Url", "") or "unknown",
        "content_sha256": sha256(body.encode("utf-8")).hexdigest(),
        "review_status": "agent-reviewed",
        "answer_ready": False,
        "updated": GOVERNANCE_UPDATED,
    }


def update_page_governance(
    page: Path,
    key: str,
    rows: list[dict[str, str]],
    text: str,
) -> str:
    _, body = parse_frontmatter(text)
    return update_frontmatter(text, audit_governance_metadata(key, rows, body))


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_standard_page(key: str, rows: list[dict[str, str]]) -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    page = WIKI_DIR / f"{key}.md"
    if page.exists():
        existing = page.read_text(encoding="utf-8-sig", errors="ignore")
        updated = existing
        _, body = parse_frontmatter(updated)
        supplement = AUDIT_SUPPLEMENTS.get(key)
        if supplement and "## 实务定位" not in body:
            updated = updated.rstrip() + "\n\n" + "\n".join(supplement) + "\n"
        updated = update_page_governance(page, key, rows, updated)
        if updated != existing:
            page.write_text(updated, encoding="utf-8", newline="\n")
        return

    title = next((row["StandardTitle"] for row in rows if row["StandardTitle"]), key)
    family = next((row["StandardFamily"] for row in rows if row["StandardFamily"]), "")
    counts = Counter(row["SourceTypeLabel"] for row in rows)
    lines = [
        "---",
        f"title: {title}",
        "type: concept",
        "concept_type: audit-standard",
        "maturity: draft",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [cicpa-professional-standards-number-index-2026-06-26]",
        "tags: [audit, standards, cicpa, p1-core]",
        "related: [[concepts/audit-standards-system]], [[sources/cicpa-professional-standards-number-index-2026-06-26]]",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        f"- 准则类型：{family or '未识别'}",
        f"- 索引键：`{key}`",
        f"- 资料记录数：{len(rows)}",
        "",
        "## 资料分布",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for label, count in sorted(counts.items()):
        lines.append(f"| {label} | {count} |")
    lines.extend(["", "## 关联资料", "", "| 类型 | 标题 | 来源分组 | 官方链接 | 本地文件 |", "|---|---|---|---|---|"])
    for row in rows:
        lines.append(
            "| {type} | {title} | {group} | {url} | `{local}` |".format(
                type=md_escape(row["SourceTypeLabel"]),
                title=md_escape(row["Title"]),
                group=md_escape(row["Group"]),
                url=row["Url"],
                local=md_escape(row["LocalPath"]),
            )
        )
    supplement = AUDIT_SUPPLEMENTS.get(key)
    if supplement:
        lines.extend(["", *supplement])
    generated = "\n".join(lines) + "\n"
    page.write_text(update_page_governance(page, key, rows, generated), encoding="utf-8", newline="\n")


def write_unmapped_page(rows: list[dict[str, str]]) -> None:
    page = WIKI_DIR / "unmapped.md"
    lines = [
        "---",
        "title: 中国注册会计师执业准则未映射资料",
        "type: concept",
        "concept_type: audit-standard-unmapped",
        "page_role: index",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [cicpa-professional-standards-number-index-2026-06-26]",
        "tags: [audit, standards, cicpa, unmapped, p1-core]",
        "related: [[concepts/audit-standards-system]], [[sources/cicpa-professional-standards-number-index-2026-06-26]]",
        "---",
        "",
        "# 中国注册会计师执业准则未映射资料",
        "",
        f"本页是准则编号映射的回退队列，本次索引生成 {len(rows)} 条未能稳定解析到具体准则编号的记录。Agent 先做候选归属和来源核对，正式纳入知识页仍保留人工复核底线。",
        "",
        "## 处理规则",
        "",
        "- 只有标题、官方栏目或原文内容能够稳定支持准则编号时，才回挂到具体准则页。",
        "- 无法稳定归类的资料保留官方链接和本地门面，不通过标题猜测适用准则。",
        "- 复核完成后应更新编号映射明细、来源状态和关联页面，再重建缓存与索引。",
        "",
        "## 当前队列",
        "",
        "| 类型 | 标题 | 来源分组 | 官方链接 | 本地文件 |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {type} | {title} | {group} | {url} | `{local}` |".format(
                type=md_escape(row["SourceTypeLabel"]),
                title=md_escape(row["Title"]),
                group=md_escape(row["Group"]),
                url=row["Url"],
                local=md_escape(row["LocalPath"]),
            )
        )
    generated = "\n".join(lines) + "\n"
    metadata = {
        "page_role": "index",
        "maturity": "reviewed",
        "asset_id": "cpa-zh:audit-standard:unmapped",
        "source_id": AUDIT_INDEX_SOURCE_ID,
        "knowledge_type": "audit-standard-unmapped",
        "source_type": "index",
        "version": "unknown",
        "published_on": "2026-06-26",
        "effective_from": "unknown",
        "effective_to": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/indexes/cicpa-professional-standards-number-mapping.csv.md",
        "markdown_path": "unknown",
        "source_url": "unknown",
        "content_sha256": sha256(parse_frontmatter(generated)[1].encode("utf-8")).hexdigest(),
        "review_status": "agent-reviewed",
        "answer_ready": False,
        "updated": GOVERNANCE_UPDATED,
    }
    page.write_text(update_frontmatter(generated, metadata), encoding="utf-8", newline="\n")


def ensure_audit_supplements() -> None:
    """Keep practice notes on existing pages even when a source row is opaque."""
    for key, supplement in AUDIT_SUPPLEMENTS.items():
        page = WIKI_DIR / f"{key}.md"
        if not page.exists():
            continue
        existing = page.read_text(encoding="utf-8-sig", errors="ignore")
        updated = existing
        _, body = parse_frontmatter(updated)
        if "## 实务定位" not in updated:
            updated = updated.rstrip() + "\n\n" + "\n".join(supplement) + "\n"
        if updated != existing:
            page.write_text(updated, encoding="utf-8", newline="\n")


def write_markdown_index(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    unmapped: list[dict[str, str]] = []
    for row in rows:
        if row["StandardKey"] == "unmapped":
            unmapped.append(row)
        else:
            grouped[row["StandardKey"]].append(row)

    existing_keys = {
        path.stem
        for path in WIKI_DIR.glob("*.md")
        if path.stem not in {"topics", "unmapped"}
    }
    all_keys = sorted(set(grouped) | existing_keys)
    for key in all_keys:
        write_standard_page(key, grouped.get(key, []))
    write_unmapped_page(unmapped)

    summary_rows: list[dict[str, str]] = []
    for key in all_keys:
        group_rows = grouped.get(key, [])
        counts = Counter(row["SourceType"] for row in group_rows)
        title = next((row["StandardTitle"] for row in group_rows if row["StandardTitle"]), "")
        if not title:
            page = WIKI_DIR / f"{key}.md"
            if page.exists():
                metadata, _ = parse_frontmatter(page.read_text(encoding="utf-8-sig", errors="ignore"))
                title = str(metadata.get("title") or key)
            else:
                title = key
        family = next((row["StandardFamily"] for row in group_rows if row["StandardFamily"]), "")
        summary_rows.append(
            {
                "StandardKey": key,
                "StandardFamily": family,
                "StandardTitle": title,
                "WikiPage": f"concepts/audit-standards/{key}",
                "StandardCount": str(counts["standard"] + counts["archive_pdf"]),
                "GuidelineCount": str(counts["guideline"]),
                "TopicEntryCount": str(counts["topic_entry"]),
                "TotalMappedRecords": str(len(group_rows)),
            }
        )

    index_lines = [
        "# 中国注册会计师执业准则编号级索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 文件",
        "",
        "- 编号汇总 CSV：`raw/indexes/cicpa-professional-standards-number-index.csv`",
        "- 映射明细 CSV：`raw/indexes/cicpa-professional-standards-number-mapping.csv`",
        "- 分准则 wiki 页：`wiki/concepts/audit-standards/`",
        "",
        "## 汇总",
        "",
        "| 准则 | 准则类型 | 准则原文/ZIP | 应用指南 | 专题条目 | 合计 | 页面 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        index_lines.append(
            "| {title} | {family} | {standard} | {guide} | {topic} | {total} | [[{page}]] |".format(
                title=md_escape(row["StandardTitle"]),
                family=md_escape(row["StandardFamily"]),
                standard=row["StandardCount"],
                guide=row["GuidelineCount"],
                topic=row["TopicEntryCount"],
                total=row["TotalMappedRecords"],
                page=row["WikiPage"],
            )
        )
    index_lines.extend(
        [
            f"| 未映射资料 |  |  |  |  | {len(unmapped)} | [[concepts/audit-standards/unmapped]] |",
            "",
            "## 映射说明",
            "",
            "- 直接 PDF 清单优先采用 CSV 标题；如 2023 年 34 项应用指南附件标题仅为序号，则从通知 HTML 的附件链接补全标题。",
            "- ZIP 解压 PDF 依据文件名解析准则编号和标题。",
            "- 专题条目仅在标题中能稳定识别准则编号时纳入对应准则页。",
            "- 无法稳定解析准则编号的资料保留在未映射页。",
        ]
    )
    (INDEX_DIR / "cicpa-professional-standards-number-index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )
    return summary_rows


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_direct_pdf_records() + load_archive_pdf_records() + load_topic_records()
    rows = dedupe_rows(rows)
    write_csv(INDEX_DIR / "cicpa-professional-standards-number-mapping.csv", rows)
    summary_rows = write_markdown_index(rows)
    ensure_audit_supplements()
    write_csv(INDEX_DIR / "cicpa-professional-standards-number-index.csv", summary_rows)
    mapped = sum(1 for row in rows if row["StandardKey"] != "unmapped")
    unmapped = len(rows) - mapped
    print(f"standards={len(summary_rows)} mapped_records={mapped} unmapped={unmapped} total_rows={len(rows)}")


if __name__ == "__main__":
    main()
