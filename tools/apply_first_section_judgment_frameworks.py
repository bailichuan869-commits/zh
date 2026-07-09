from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge-base" / "CPA-ZH" / "wiki"
CONCEPTS = WIKI / "concepts"
ACCOUNTING = CONCEPTS / "accounting-standards"
AUDIT = CONCEPTS / "audit-standards"

START = "<!-- judgment-framework:start -->"
END = "<!-- judgment-framework:end -->"


FRAMEWORKS: dict[Path, str] = {
    ACCOUNTING / "cas-14.md": """
## 判断框架

收入准则页后续判断可以围绕“五步法”展开：识别合同、识别履约义务、确定交易价格、分摊交易价格、在履约义务满足时确认收入。实务中不要只看发票、回款或合同名称，应回到客户取得商品或服务控制权的时间点。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 合同是否真实、完整、可执行 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 履约义务拆分是否恰当 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1231]] |
| 某一时点或某一时段确认收入是否有证据支持 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1313]] |
| 可变对价、重大融资成分、主要责任人和代理人判断 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1301]] |
| 合同资产、合同负债和应收账款列报 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将收入政策、合同条款、履约证据、结算记录和期后回款串成同一条证据链。
- 对新业务模式、平台交易、预售、定制开发、代理销售等场景单独形成判断备忘。
- 对截止性测试保留发货、签收、验收、服务完成、客户上线或结算节点等关键证据。
""",
    ACCOUNTING / "cas-22.md": """
## 判断框架

金融工具页应优先区分“分类计量、减值、终止确认、套期或衍生工具、金融负债与权益工具区分”几条主线。判断时先看合同现金流量特征和业务模式，再看计量属性和列报披露。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 金融资产分类是否符合业务模式和现金流量特征 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 公允价值估值模型、参数和层次是否合理 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] |
| 预期信用损失模型、阶段划分和前瞻性调整 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1301]] |
| 终止确认、结构化主体、证券化和清仓回购安排 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1211]] |
| 永续债、可转债、特殊条款工具的负债权益区分 | [[concepts/accounting-standards/cas-37]], [[concepts/audit-standards/csa-1301]] |

## 底稿提示

- 对金融工具清单、合同条款、估值输入、减值模型和管理层审批记录建立勾稽。
- 对模型参数来源、敏感性分析和管理层覆盖调整保留复核轨迹。
- 对新增复杂产品或重大重分类事项形成单独技术备忘。
""",
    ACCOUNTING / "cas-21.md": """
## 判断框架

租赁准则判断先看合同是否让渡已识别资产在一定期间内的使用控制权，再区分承租人和出租人处理。承租人侧重点是租赁期、租赁付款额、折现率、使用权资产和租赁负债；出租人侧重点是融资租赁与经营租赁分类。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 租赁识别是否完整，服务合同中是否嵌入租赁 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 租赁期、续租选择权和终止选择权判断 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1301]] |
| 折现率、付款额、可变租赁付款额和租赁变更 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1231]] |
| 售后租回、疫情租金减让等特殊事项 | [[concepts/accounting-standards/other-rules/covid-rent-concessions]], [[concepts/audit-standards/csa-1301]] |
| 现金流量表和财务报表列报 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将租赁合同台账、付款计划、折现率依据、资产清单和会计分录保持一致。
- 对续租选择权、重大改良支出、复原义务等估计判断保留管理层意图和历史行为证据。
- 对新增门店、厂房、设备、数据中心等重大租赁安排执行完整性检查。
""",
    ACCOUNTING / "cas-33.md": """
## 判断框架

合并报表判断核心是控制：是否拥有对被投资方的权力、是否享有可变回报、是否有能力运用权力影响回报。结构化主体、委托代理、潜在表决权和合同安排不能只看股权比例。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 合并范围完整性和控制判断 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1401]] |
| 结构化主体、基金、信托、资管计划等特殊主体 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 内部交易抵销、权益法与合并报表衔接 | [[concepts/accounting-standards/cas-02]], [[concepts/audit-standards/csa-1401]] |
| 处置子公司、丧失控制权和期初比较信息 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1301]] |
| 集团组成部分重要性和组成部分审计程序 | [[concepts/audit-standards/csa-1401]], [[concepts/audit-standards/csa-1201]] |

## 底稿提示

- 保留集团架构图、投资协议、章程、董事会安排、合同权利和实际决策记录。
- 对未纳入合并范围的主体列明排除理由，尤其关注结构化主体和代持安排。
- 将合并范围变化与股权交易、工商信息、资金往来、关联方清单交叉核对。
""",
    ACCOUNTING / "cas-25.md": """
## 判断框架

保险合同判断应先识别重大保险风险，再围绕合同组合、计量模型、履约现金流、合同服务边际和保险财务损益列报展开。对具有直接参与分红特征的合同，应特别关注基础项目和金融变动额分解政策。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 保险合同边界和合同组合划分 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 精算假设、折现率、风险调整和合同服务边际 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] |
| 保险财务损益和其他综合收益列报政策 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1501]] |
| 与金融工具减值、权益法核算的交叉 | [[concepts/accounting-standards/cas-22]], [[concepts/accounting-standards/cas-02]] |

## 底稿提示

- 对精算模型、关键假设、数据质量和管理层复核形成独立底稿。
- 对会计政策选择权记录决策依据、适用层级和一致性检查。
- 对保险合同和非保险组成部分分拆保留合同条款分析。
""",
    ACCOUNTING / "cas-30.md": """
## 判断框架

财务报表列报页关注报表项目分类、流动与非流动区分、重要性聚合、附注披露和比较信息。列报判断通常不是单独问题，而是收入、金融工具、租赁、保险合同、或有事项等具体准则的结果呈现。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 流动与非流动分类是否符合资产负债表日权利义务 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1501]] |
| 报表格式和附注披露是否完整、清晰、可理解 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |
| 重要项目是否恰当单列或合并列示 | [[concepts/audit-standards/csa-1251]], [[concepts/audit-standards/csa-1501]] |
| 其他信息与财务报表是否一致 | [[concepts/audit-standards/csa-1521]], [[concepts/audit-standards/csa-1151]] |

## 底稿提示

- 将试算平衡表、报表项目映射、附注披露清单和审定调整表保持一致。
- 对重分类调整、列报变化和重要披露缺失保留复核意见。
- 对管理层说明书、年报其他信息和财务报表进行一致性检查。
""",
    ACCOUNTING / "cas-02.md": """
## 判断框架

长期股权投资判断先看投资方对被投资单位是否具有控制、共同控制或重大影响，再确定成本法、权益法或金融工具准则路径。实务中应同步考虑个别报表、合并报表和处置时点的影响。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 控制、共同控制、重大影响证据是否充分 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 权益法核算、内部交易抵销和利润分配 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1401]] |
| 投资减值和可收回金额估计 | [[concepts/accounting-standards/cas-08]], [[concepts/audit-standards/csa-1321]] |
| 重大投资、处置和信息披露 | [[concepts/first-section-topics/long-term-equity-investments]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将投资协议、章程、表决权安排、董事会席位、实际决策记录和工商信息交叉核验。
- 对权益法调整保留被投资单位报表、审计情况、调整分录和未实现内部交易抵销依据。
- 对处置或丧失控制权事项，单独形成个别报表和合并报表影响分析。
""",
    ACCOUNTING / "cas-08.md": """
## 判断框架

资产减值判断应从减值迹象、资产组划分、可收回金额、现金流预测和折现率入手。商誉、长期资产和亏损资产组通常需要单独形成估计判断闭环。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 减值迹象识别是否完整 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 资产组划分、现金流预测和折现率 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] |
| 商誉减值、重大长期资产减值 | [[concepts/first-section-topics/asset-impairment]], [[concepts/audit-standards/csa-1504]] |
| 减值披露和业绩压力 | [[concepts/audit-standards/csa-1141]], [[concepts/accounting-standards/cas-30]] |

## 底稿提示

- 将减值迹象、资产组边界、预算批准、历史预测偏差和敏感性分析放在同一索引。
- 对关键假设保留外部市场证据、专家复核记录和管理层复核痕迹。
- 对未计提或少计提减值的重大项目，记录反证和项目组结论。
""",
    ACCOUNTING / "cas-09.md": """
## 判断框架

职工薪酬页应区分短期薪酬、离职后福利、辞退福利和其他长期职工福利。判断重点是义务是否已经形成、金额是否可靠计量、费用或资产化归属是否合理。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 薪酬完整性、截止和分配 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1231]] |
| 奖金、辞退福利和长期福利估计 | [[concepts/audit-standards/csa-1321]], [[concepts/first-section-topics/employee-benefits]] |
| 管理层奖金和舞弊诱因 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 披露和其他信息一致性 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |

## 底稿提示

- 将花名册、合同、工资表、考勤、银行流水、社保公积金和费用分配表勾稽一致。
- 对资本化人员成本检查受益对象、工时记录和分配基础。
- 对裁员、重组或长期激励计划保留批准文件和条件满足判断。
""",
    ACCOUNTING / "cas-13.md": """
## 判断框架

或有事项判断要区分预计负债、或有负债、或有资产和披露事项。核心是现时义务是否存在、经济利益流出是否很可能、金额是否能够可靠计量。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 未决诉讼、担保和承诺完整性 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1323]] |
| 预计负债金额估计和律师意见 | [[concepts/audit-standards/csa-1321]], [[concepts/first-section-topics/contingencies-major-litigation]] |
| 或有事项披露充分性 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1501]] |
| 重大诉讼对持续经营和报告意见影响 | [[concepts/audit-standards/csa-1324]], [[concepts/audit-standards/csa-1503]] |

## 底稿提示

- 将诉讼清单、律师函、法院文书、担保合同、董事会决议和期后进展统一索引。
- 对未确认但披露的事项，保留不确认理由和披露充分性评价。
- 对管理层未提供完整诉讼或担保资料的情况，评估范围受限和诚信风险。
""",
    ACCOUNTING / "cas-16.md": """
## 判断框架

政府补助判断先看交易是否来自政府、是否附带条件、与资产还是收益相关，再确定总额法或净额法、递延收益摊销和列报披露。专项资金还要关注用途限制和退回风险。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 补助批文、拨款和条件满足证据 | [[concepts/audit-standards/csa-1301]], [[concepts/first-section-topics/government-grants-special-funds]] |
| 与资产相关补助和递延收益摊销 | [[concepts/audit-standards/csa-1321]], [[concepts/accounting-standards/cas-30]] |
| 期末集中确认和业绩调节风险 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 专项资金使用限制和退回义务 | [[concepts/accounting-standards/cas-13]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将批文、申报材料、拨款流水、验收文件、资金使用台账和会计分录勾稽一致。
- 对附条件补助，记录条件满足证据、摊销期间和退回风险判断。
- 对重大补助披露，检查年报其他信息和财务报表的一致性。
""",
    ACCOUNTING / "cas-18.md": """
## 判断框架

所得税判断应区分当期所得税、递延所得税资产和负债、可抵扣亏损、税收优惠和不确定税务事项。递延所得税资产确认必须回到未来应纳税所得额的可实现性。

## 审计关注点

| 关注点 | 审计连接 |
|---|---|
| 暂时性差异和税会差异明细 | [[concepts/audit-standards/csa-1301]], [[concepts/first-section-topics/income-tax-deferred-tax]] |
| 递延所得税资产可实现性 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1324]] |
| 税收优惠、税务争议和或有事项 | [[concepts/accounting-standards/cas-13]], [[concepts/audit-standards/csa-1301]] |
| 所得税披露和关键审计事项 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1504]] |

## 底稿提示

- 将纳税申报表、税务优惠文件、可抵扣亏损到期表、盈利预测和递延所得税明细勾稽一致。
- 对亏损企业确认递延所得税资产，保留未来盈利预测、税法限制和敏感性分析。
- 对重大税务争议，结合或有事项和披露要求单独收口。
""",
    AUDIT / "csa-1211.md": """
## 程序设计框架

风险评估不是填表动作，而是后续审计程序的发动机。应从行业、监管、商业模式、内部控制、会计政策、信息系统和舞弊诱因出发，识别财务报表层次和认定层次重大错报风险。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 收入舞弊和截止风险 | [[concepts/accounting-standards/cas-14]], [[concepts/audit-standards/csa-1141]] |
| 金融工具估值和减值复杂性 | [[concepts/accounting-standards/cas-22]], [[concepts/audit-standards/csa-1321]] |
| 合并范围、结构化主体和关联方 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1323]] |
| 持续经营不确定性 | [[concepts/audit-standards/csa-1324]], [[concepts/audit-standards/csa-1501]] |
| 信息系统、数据接口和自动控制 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1231]] |

## 底稿提示

- 风险描述应落到“什么认定、为什么可能错、可能怎么错、错报可能多大”。
- 对特别风险说明判断依据，并明确不能只依赖实质性分析程序。
- 风险评估结论应能追踪到后续审计程序和审计证据。
""",
    AUDIT / "csa-1301.md": """
## 程序设计框架

审计证据关注充分性和适当性。充分性看数量，适当性看相关性和可靠性；外部证据通常强于内部证据，直接获取通常强于间接获取，但都要结合风险和认定判断。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 证据是否覆盖关键认定 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1231]] |
| 外部证据、函证和替代程序 | [[concepts/audit-standards/csa-1312]], [[concepts/audit-standards/csa-1311]] |
| 分析程序能否作为实质性程序 | [[concepts/audit-standards/csa-1313]], [[concepts/audit-standards/csa-1251]] |
| 抽样方法、样本量和偏差评价 | [[concepts/audit-standards/csa-1314]], [[concepts/audit-standards/csa-1251]] |

## 底稿提示

- 每个重大风险至少应能对应到具体程序、样本、结果和结论。
- 证据矛盾时不要只保留支持性证据，应记录矛盾处理和追加程序。
- 对电子证据保留来源、导出路径、完整性检查和字段解释。
""",
    AUDIT / "csa-1312.md": """
## 程序设计框架

函证程序应从认定、风险和被询证者可靠性出发设计。是否函证、函证什么、向谁函证、采用积极式还是消极式、如何控制发出和收回，都应能回到重大错报风险和相关认定。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 银行存款、借款、担保、受限资金和理财完整性 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1211]] |
| 应收账款、合同资产和收入真实性 | [[concepts/accounting-standards/cas-14]], [[concepts/audit-standards/csa-1311]] |
| 往来款、关联方和异常交易背景 | [[concepts/audit-standards/csa-1323]], [[concepts/audit-standards/csa-1141]] |
| 回函差异、未回函和替代程序充分性 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1314]] |

## 底稿提示

- 函证控制应覆盖询证信息生成、地址核验、发函、跟函、收函和差异处理全过程。
- 对电子函证、平台函证和被审计单位协助环节保留独立控制证据。
- 未回函不能自动等同于无异常，应按风险和认定设计替代程序并评价结论。
""",
    AUDIT / "csa-1314.md": """
## 程序设计框架

审计抽样页关注样本设计、样本选取、测试执行和偏差评价。抽样不是机械比例问题，应先明确总体、抽样单元、可容忍错报或偏差率、预期错报或偏差率，以及抽样风险。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 总体完整性和分层是否支持测试目标 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1251]] |
| 控制测试中的偏差性质和偏差率评价 | [[concepts/audit-standards/csa-1231]], [[concepts/audit-standards/csa-1211]] |
| 细节测试中错报投影和异常项目处理 | [[concepts/audit-standards/csa-1251]], [[concepts/audit-standards/csa-1301]] |
| 函证、收入截止、费用完整性等样本设计 | [[concepts/audit-standards/csa-1312]], [[concepts/accounting-standards/cas-14]] |

## 底稿提示

- 底稿应说明总体来源、抽样方法、样本量依据和选样过程，避免只保留样本清单。
- 发现偏差或错报后，应评价性质、原因、是否系统性以及是否需要扩大程序。
- 对关键项目、异常项目和随机样本分别说明选取逻辑，避免混同统计抽样和非统计抽样。
""",
    AUDIT / "csa-1321.md": """
## 程序设计框架

会计估计审计应从估计不确定性、模型复杂程度、主观性和管理层偏向风险入手。重点不是替管理层重新做一个数字，而是评价方法、假设、数据、模型和披露是否共同支持估计结果。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 金融工具公允价值和预期信用损失 | [[concepts/accounting-standards/cas-22]], [[concepts/audit-standards/csa-1421]] |
| 存货跌价、资产减值和长期资产可收回金额 | [[concepts/accounting-standards/cas-08]], [[concepts/audit-standards/csa-1301]] |
| 收入可变对价、退货、质保和履约进度估计 | [[concepts/accounting-standards/cas-14]], [[concepts/audit-standards/csa-1211]] |
| 保险合同精算假设和合同服务边际 | [[concepts/accounting-standards/cas-25]], [[concepts/audit-standards/csa-1421]] |
| 管理层偏向、敏感性分析和披露充分性 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将估计方法、关键假设、数据来源、模型计算和管理层复核证据连成闭环。
- 对高度不确定估计保留敏感性分析、事后复核和专家参与记录。
- 对管理层覆盖调整、乐观假设和与历史结果不一致的输入保持职业怀疑。
""",
    AUDIT / "csa-1401.md": """
## 程序设计框架

集团审计应先理解集团结构、组成部分、合并流程和共享服务安排，再确定组成部分重要性、工作范围、沟通要求和复核深度。集团项目组不能只收集组成部分报告，应对集团层面风险和组成部分工作承担充分评价责任。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 合并范围完整性、控制判断和结构化主体 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1211]] |
| 组成部分重要性、特别风险和工作范围 | [[concepts/audit-standards/csa-1201]], [[concepts/audit-standards/csa-1251]] |
| 组成部分注册会计师胜任能力和沟通 | [[concepts/audit-standards/csa-1121]], [[concepts/audit-standards/csa-1151]] |
| 合并抵销、内部交易和期后范围变化 | [[concepts/accounting-standards/cas-02]], [[concepts/audit-standards/csa-1301]] |

## 底稿提示

- 保留集团架构、组成部分识别、重要性分配、工作指令和回函沟通记录。
- 对重大组成部分和存在特别风险的组成部分，应能看到集团项目组参与和复核痕迹。
- 将组成部分发现事项、合并调整、未更正错报和集团层面结论统一收口。
""",
    AUDIT / "csa-1501.md": """
## 程序设计框架

审计报告不是写作环节，而是审计结论的收口。形成意见前应评价已获取证据、未更正错报、披露完整性、持续经营、其他信息和管理层责任表述。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 未更正错报是否重大或广泛 | [[concepts/audit-standards/csa-1251]], [[concepts/audit-standards/csa-1503]] |
| 披露是否足以支持无保留意见 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1521]] |
| 是否需要关键审计事项 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1151]] |
| 持续经营事项如何影响意见和段落 | [[concepts/audit-standards/csa-1324]], [[concepts/audit-standards/csa-1503]] |

## 底稿提示

- 报告意见应能回溯到重大事项汇总、审计差异汇总和项目合伙人复核结论。
- 对强调事项段、其他事项段、关键审计事项分别说明触发原因。
- 报告日前后事项、其他信息和治理层沟通应有收口记录。
""",
    AUDIT / "csa-1504.md": """
## 程序设计框架

关键审计事项来自与治理层沟通过的事项，并从本期审计中最为重要的事项中确定。判断重点是重大错报风险、管理层重大判断、重大交易或事项，以及审计中投入的资源和遇到的困难。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 收入确认、截止和舞弊风险是否构成关键事项 | [[concepts/accounting-standards/cas-14]], [[concepts/audit-standards/csa-1141]] |
| 金融工具估值、减值和模型复杂性 | [[concepts/accounting-standards/cas-22]], [[concepts/audit-standards/csa-1321]] |
| 合并范围、重大收购处置和集团审计判断 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1401]] |
| 持续经营、强调事项段和审计意见类型边界 | [[concepts/audit-standards/csa-1324]], [[concepts/audit-standards/csa-1503]] |

## 底稿提示

- 关键审计事项应能追溯到风险评估、治理层沟通、审计应对和最终报告文字。
- 描述事项时避免替代管理层披露，应说明审计中如何应对该事项。
- 不应把无法获取充分适当证据的事项简单包装成关键审计事项，应先评价意见类型影响。
""",
    AUDIT / "csa-1141.md": """
## 程序设计框架

舞弊准则页应围绕舞弊三角、收入舞弊假定、管理层凌驾控制和非常规交易展开。程序设计要能回应“哪里可能被人为操纵、谁有动机和机会、证据如何反证”。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 收入确认和截止操纵 | [[concepts/first-section-topics/revenue-recognition-misstatement]], [[concepts/accounting-standards/cas-14]] |
| 关联方、资金占用和利益输送 | [[concepts/first-section-topics/related-parties-fund-occupation]], [[concepts/audit-standards/csa-1323]] |
| 估计偏向、减值和递延所得税资产 | [[concepts/audit-standards/csa-1321]], [[concepts/first-section-topics/asset-impairment]] |
| 证券服务责任和信息披露风险 | [[concepts/law-securities]], [[concepts/first-section-topics/securities-service-liability]] |

## 底稿提示

- 记录舞弊风险讨论、管理层访谈、异常分录测试和重大非常规交易检查。
- 对管理层解释不能只记录口头说明，应取得外部证据或后续反证。
- 舞弊风险结论应能回到具体认定和审计程序。
""",
    AUDIT / "csa-1151.md": """
## 程序设计框架

治理层沟通不是形式性会议纪要，而是重大风险、审计调整、独立性、关键审计事项和内部控制缺陷的收口机制。沟通对象、时间、内容和反馈都应留痕。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 关键审计事项来源和治理层沟通 | [[concepts/audit-standards/csa-1504]], [[concepts/first-section-topics/key-audit-matters]] |
| 公司治理和财务报告责任 | [[concepts/law-company]], [[concepts/law-accounting]] |
| 未更正错报和重大事项收口 | [[concepts/audit-standards/csa-1251]], [[concepts/audit-standards/csa-1501]] |
| 独立性和职业道德事项 | [[concepts/ethics-code]], [[concepts/independence-standard-1]] |

## 底稿提示

- 治理层沟通应列明沟通事项、项目组判断、治理层反馈和后续处理。
- 对关键审计事项和非无保留意见事项，应有治理层沟通轨迹。
- 对管理层与治理层角色重叠的客户，应说明沟通对象适当性。
""",
    AUDIT / "csa-1231.md": """
## 程序设计框架

控制测试应从相关认定和预期控制目标出发。不是有流程图就等于测试控制，应评价控制设计、执行、频率、责任人、证据和信息系统依赖。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 收入、采购、资金和薪酬循环控制 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1301]] |
| 信息系统自动控制和数据接口 | [[concepts/audit-standards/csa-1301]], [[concepts/first-section-topics/revenue-recognition-misstatement]] |
| 控制偏差评价和样本设计 | [[concepts/audit-standards/csa-1314]], [[concepts/audit-standards/csa-1251]] |
| 资金占用、关联方和管理层凌驾 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1323]] |

## 底稿提示

- 保留控制目标、关键控制点、穿行测试、样本测试和偏差评价。
- 对依赖系统报表的控制，应测试报表完整性和准确性。
- 控制测试失败后，应重新评价实质性程序范围。
""",
    AUDIT / "csa-1251.md": """
## 程序设计框架

重要性贯穿计划、执行和评价错报全过程。应区分财务报表整体重要性、实际执行重要性、明显微小错报临界值和特定类别交易或披露的重要性。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 未更正错报评价和报告意见 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1503]] |
| 抽样样本量和错报投影 | [[concepts/audit-standards/csa-1314]], [[concepts/audit-standards/csa-1301]] |
| 低于金额但性质重要事项 | [[concepts/law-securities]], [[concepts/audit-standards/csa-1504]] |
| 披露重要性和其他信息 | [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1521]] |

## 底稿提示

- 记录基准选择、百分比、调整理由和实际执行重要性分配。
- 对性质敏感事项，如关联方、舞弊、监管指标和债务契约，不能只看金额。
- 未更正错报汇总应与管理层书面声明和报告意见一致。
""",
    AUDIT / "csa-1323.md": """
## 程序设计框架

关联方审计应从关系识别、交易商业实质、披露完整性和舞弊风险四条线展开。关联方清单不应只依赖管理层提供，应结合工商、股权、资金、合同和人员信息交叉核验。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 关联方及资金占用 | [[concepts/first-section-topics/related-parties-fund-occupation]], [[concepts/accounting-standards/cas-36]] |
| 合并范围和结构化主体 | [[concepts/first-section-topics/consolidation-scope-control]], [[concepts/accounting-standards/cas-33]] |
| 异常交易和舞弊风险 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 披露和证券服务责任 | [[concepts/law-securities]], [[concepts/audit-standards/csa-1501]] |

## 底稿提示

- 将关联方清单、工商查询、银行流水、往来函证、合同和公告披露交叉核对。
- 对非经营性资金占用、代垫费用、无商业实质交易和期后反向流出重点追查。
- 对未披露关联方或重大关联交易，应评价管理层诚信和报告影响。
""",
    AUDIT / "csa-1324.md": """
## 程序设计框架

持续经营审计应评价管理层使用持续经营假设是否适当，以及是否存在需要披露的重大不确定性。程序重点是现金流、融资、债务契约、经营计划和期后事项。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 持续经营重大不确定性 | [[concepts/first-section-topics/going-concern-uncertainty]], [[concepts/accounting-standards/cas-30]] |
| 债务违约、流动性和融资计划 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1503]] |
| 递延所得税资产和盈利预测 | [[concepts/first-section-topics/income-tax-deferred-tax]], [[concepts/audit-standards/csa-1321]] |
| 报告段落和披露充分性 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |

## 底稿提示

- 获取现金流预测、债务到期表、授信续展、违约豁免和经营计划。
- 对管理层计划评价可执行性和历史兑现情况。
- 报告收口时区分充分披露下的重大不确定性段落和披露不足导致的意见修改。
""",
    AUDIT / "csa-1421.md": """
## 程序设计框架

利用专家工作时，项目组仍需对审计结论负责。应评价专家胜任能力、专业素质、客观性、工作范围、使用的数据和假设，以及专家结果与其他审计证据是否一致。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 金融工具估值和模型 | [[concepts/first-section-topics/financial-instruments-valuation-impairment]], [[concepts/accounting-standards/cas-22]] |
| 资产减值和商誉估值 | [[concepts/first-section-topics/asset-impairment]], [[concepts/accounting-standards/cas-08]] |
| 保险合同和精算估计 | [[concepts/accounting-standards/cas-25]], [[concepts/audit-standards/csa-1321]] |
| 重大诉讼律师意见 | [[concepts/first-section-topics/contingencies-major-litigation]], [[concepts/audit-standards/csa-1301]] |

## 底稿提示

- 保留专家资质、独立性评价、委托范围、关键假设和项目组复核记录。
- 专家结论不能直接粘贴为审计结论，应说明项目组如何评价其适当性。
- 对专家结论与其他证据不一致的情况，记录追加程序。
""",
    AUDIT / "csa-1521.md": """
## 程序设计框架

其他信息审计关注年报、管理层讨论、公告等非财务报表信息是否与已审财务报表或审计中了解到的情况存在重大不一致。公众公司项目尤其要把其他信息检查纳入报告收口。

## 高频审计关注点

| 关注点 | 相关页面 |
|---|---|
| 年报其他信息和财务报表一致性 | [[concepts/law-securities]], [[concepts/accounting-standards/cas-30]] |
| 收入、减值、关联方和持续经营披露 | [[concepts/first-section-topic-matrix]], [[concepts/audit-standards/csa-1501]] |
| 关键审计事项与年报描述一致性 | [[concepts/audit-standards/csa-1504]], [[concepts/first-section-topics/key-audit-matters]] |
| 证券服务责任和重大遗漏风险 | [[concepts/first-section-topics/securities-service-liability]], [[concepts/law-securities]] |

## 底稿提示

- 保留其他信息版本、阅读范围、差异清单、管理层修改和最终结论。
- 对年报中经营数据、行业信息、风险描述与财务报表不一致的事项，应追问并记录处理。
- 其他信息重大错报未改正时，应评价审计报告和沟通影响。
""",
}


def upsert_framework(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    full = START + "\n" + block.strip() + "\n\n" + END
    pattern = re.compile(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.S)
    if pattern.search(text):
        text = pattern.sub("\n\n" + full + "\n", text).rstrip() + "\n"
    else:
        text = text.rstrip() + "\n\n" + full + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for path, block in FRAMEWORKS.items():
        if not path.exists():
            raise FileNotFoundError(path)
        upsert_framework(path, block)
    print(f"framework_pages={len(FRAMEWORKS)}")


if __name__ == "__main__":
    main()
