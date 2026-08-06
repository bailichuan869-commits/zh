"""Generate the reviewable 20-topic and 20-case CPA-ZH golden content set."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from kb_common import KB_ROOT, parse_frontmatter, update_frontmatter


TODAY = date.today().isoformat()
TOPIC_ROOT = KB_ROOT / "wiki" / "concepts" / "accounting-judgments"
CASE_ROOT = KB_ROOT / "wiki" / "cases"
STANDARD_ROOT = "raw/standards/accounting/standards-pages"


TOPICS = [
    ("inventory-recognition-cost-nrv", "存货确认、成本与可变现净值", "01", "企业会计准则第1号-存货.html.md",
     "存货是否由企业控制、成本归集是否完整、售价和至完工销售成本是否有可靠证据",
     "先确认资产定义和存货范围；再区分采购、加工及其他成本；期末逐项或按适当组合比较成本与可变现净值。",
     "可直接出售的，以估计售价减销售税费确定可变现净值；需加工的，再减至完工成本；已签合同数量与超出部分分别测试。",
     "按成本初始计量；成本高于可变现净值时计提跌价准备，影响因素消失后在原计提范围内转回。"),
    ("long-term-equity-investment-scope-conversion", "长期股权投资适用范围与核算方法转换", "02", "企业会计准则第2号-长期股权投资.html.md",
     "表决权及潜在表决权、董事会安排、共同控制合同、重大影响迹象、取得或丧失控制的准确日期",
     "先判断控制、共同控制或重大影响；不满足时转入金融工具准则；再按权益变化类型选择成本法、权益法或金融资产转换路径。",
     "控制看权力、可变回报和运用权力影响回报的能力；共同控制须经分享控制权各方一致同意；重大影响不只看持股比例。",
     "按转换日规则处理原投资、追加或处置对价及其他综合收益；不同转换路径不得混用计量基础。"),
    ("fixed-assets-initial-subsequent-provisional", "固定资产初始确认、后续支出与暂估转固", "04", "企业会计准则第4号-固定资产.html.md",
     "达到预定可使用状态日期、工程决算状态、后续支出带来的未来经济利益、替换部件账面价值",
     "先判断是否达到预定可使用状态，再确定成本；决算未完成不推迟折旧；后续支出分别判断资本化或费用化。",
     "已可使用但未决算的按估计价值转固并折旧，决算后调整原值但通常不追溯调整已提折旧；替换部件资本化时终止确认旧部件。",
     "暂估转固、开始折旧并持续更新估计；日常修理计入损益，满足确认条件的改良支出计入资产成本。"),
    ("intangibles-rd-capitalisation", "无形资产及研发支出资本化", "06", "企业会计准则第6号-无形资产.html.md",
     "研究与开发阶段分界、技术可行性、完成和使用意图、市场或内部有用性、资源保障、支出可靠计量",
     "先识别可辨认无形资产；内部研发先区分研究阶段和开发阶段；开发支出仅从全部资本化条件同时满足之日起确认。",
     "研究支出和无法区分阶段的支出费用化；此前已费用化金额不得以后转回资本化；数据资源还需核实来源与使用合法合规。",
     "满足条件后的直接相关支出计入开发支出并在达到预定用途后转为无形资产；其余计入当期损益。"),
    ("asset-and-goodwill-impairment", "资产减值与商誉减值", "08", "企业会计准则第8号-资产减值.html.md",
     "减值迹象、资产组边界、现金流预测、预算期及长期增长率、折现率、商誉分摊和协同效应",
     "先识别减值迹象和测试单元；商誉及使用寿命不确定无形资产至少年度测试；比较账面价值与可收回金额。",
     "可收回金额取公允价值减处置费用净额与预计未来现金流量现值较高者；资产组应与内部管理和监测方式一致。",
     "按顺序先冲减商誉，再按比例冲减资产组其他资产；本准则范围内已确认减值通常不得转回。"),
    ("share-based-payment-recognition-modification", "股份支付识别、授予日与计划修改", "11", "企业会计准则第11号-股份支付.html.md",
     "服务对价、结算义务主体、授予日批准条件、可行权条件、修改前后公允价值、集团内安排",
     "先判断交易是否为取得服务而授予权益工具或承担以权益工具为基础的负债；再确定结算分类、授予日、等待期和修改影响。",
     "有利修改至少确认原授予日价值并确认增量；不利修改通常不减少原费用；结算义务决定接受服务企业的分类。",
     "权益结算以授予日公允价值为基础，现金结算负债持续重估；按可行权数量最佳估计确认等待期费用。"),
    ("debt-restructuring-recognition-measurement", "债务重组确认时点与损益计量", "12", "企业会计准则第12号-债务重组.html.md",
     "债权债务终止确认时点、清偿资产账面价值、修改后合同现金流、权益工具公允价值、是否属于日常活动",
     "先按金融工具准则判断原债权债务是否终止确认，再按清偿方式计量重组损益；资产清偿通常不按收入销售处理。",
     "以资产清偿、转为权益工具、修改条款或组合方式分别判断；存货清偿债务通常不是日常销售。",
     "债务人以清偿债务账面价值与转让资产或权益工具相关计量金额的差额确认重组损益，并按准则列报。"),
    ("contingencies-and-provisions", "或有事项与预计负债", "13", "企业会计准则第13号-或有事项.html.md",
     "现时义务是否存在、经济利益流出可能性、金额能否可靠计量、最佳估计和补偿权利",
     "先区分过去事项形成的现时义务与未来经营风险；同时满足义务、很可能流出和可靠计量时确认预计负债。",
     "连续范围内按各种结果及概率确定最佳估计；补偿只有基本确定收到且不超过预计负债时单独确认资产。",
     "确认预计负债及相关费用或资产成本；每个资产负债表日复核并按当前最佳估计调整。"),
    ("revenue-contract-control-transfer", "收入合同识别与控制权转移", "14", "企业会计准则第14号-收入.html.md",
     "合同批准、权利和付款条款、商业实质、客户支付能力、履约义务、控制权证据",
     "先验证合同五项条件并识别客户；识别可明确区分的履约义务；最后以客户取得商品控制权而非开票或收款作为确认基础。",
     "不满足合同条件的收款通常先确认为负债；控制权迹象包括现时收款权、法定所有权、实物占有、风险报酬和客户接受。",
     "按分摊至履约义务的交易价格，在时段或时点履约时确认收入，并同步处理合同资产、合同负债和应收款。"),
    ("revenue-over-time-point-contract-costs", "收入按时段或时点确认及合同成本", "14", "企业会计准则第14号-收入.html.md",
     "客户是否同步取得利益、在建资产控制、替代用途、可执行收款权、履约进度、增量取得成本和履约成本可收回性",
     "逐项测试三个时段条件；不满足则按时点确认；时段履约选择能够如实反映进度的投入法或产出法，并单独判断合同成本资产。",
     "不可替代用途必须与整个合同期内就累计履约部分享有可执行收款权同时满足；仅有里程碑付款不当然构成收款权。",
     "可靠计量进度时按进度确认，否则在已发生成本预计可收回范围确认；符合条件的合同成本资本化并系统摊销、减值。"),
    ("principal-versus-agent", "主要责任人和代理人判断", "14", "企业会计准则第14号-收入.html.md",
     "向客户承诺的特定商品、转让前控制、首要履约责任、存货风险、定价自主权、供应商替换权",
     "先识别特定商品，再判断企业在转让给客户前是否控制该商品；责任、存货风险和定价权只是支持控制结论的迹象。",
     "企业取得商品后再转让、控制他方服务权或整合投入形成组合时可能为主要责任人；只安排他方提供通常为代理人。",
     "主要责任人按总额确认收入，代理人按佣金或净额确认；不得只因开票、收款或承担信用风险得出结论。"),
    ("variable-consideration-modification-returns-repurchase", "可变对价、合同变更、退货与回购", "14", "企业会计准则第14号-收入.html.md",
     "可变条款及惯例、重大转回约束、变更批准、剩余商品是否可明确区分、退货概率、回购价格与客户经济动因",
     "先判断合同开始日是否已经存在可变对价；合同后新权利义务按变更模型处理；退货和回购分别按专门规则分析。",
     "新增可区分商品且价格反映单独售价时作为独立合同；否则按原合同终止加新合同或累计追补；回购可能实质为租赁或融资。",
     "按高度可能不会重大转回的金额计入交易价格；退货确认退款负债和收回商品权利；回购按实质处理。"),
    ("government-grants-non-cash-support", "政府补助与非货币性支持", "16", "企业会计准则第16号-政府补助.html.md",
     "政府身份、是否无偿、是否附条件、企业能否满足并收到、与资产或收益相关、非货币资产公允价值",
     "先排除政府资本性投入和正常交易；满足条件并能够收到时确认；再区分与资产相关或与收益相关。",
     "免费使用设备也需判断企业是否取得资产控制及补助；无法可靠取得公允价值时按名义金额计量并披露。",
     "资产相关补助采用递延收益或冲减资产账面价值；收益相关补助按补偿期间计入其他收益或冲减成本费用。"),
    ("borrowing-cost-capitalisation", "借款费用资本化", "17", "企业会计准则第17号-借款费用.html.md",
     "符合资本化条件的资产、资产支出发生、借款费用发生、购建活动开始、中断性质和达到预定可使用状态",
     "同时满足资产支出、借款费用和必要购建活动已经发生才开始资本化；非正常中断超过三个月暂停；达到预定状态停止。",
     "专门借款按实际利息减未用资金收益；一般借款按累计资产支出超过专门借款部分乘资本化率。",
     "资本化金额计入相关资产成本，其他借款费用计入当期损益，并披露资本化金额和资本化率。"),
    ("income-and-deferred-tax", "所得税与递延所得税", "18", "企业会计准则第18号-所得税.html.md",
     "资产负债账面价值与计税基础、暂时性差异转回方式、可抵扣亏损可利用性、税率、初始确认和合并例外",
     "以资产负债表债务法识别暂时性差异；判断递延所得税负债或资产及例外；按预期收回或清偿期间适用税率计量。",
     "递延所得税资产只在未来很可能取得足够应纳税所得额范围确认；与直接计入权益或其他综合收益事项保持同源列报。",
     "确认当期所得税和递延所得税；每期复核递延所得税资产账面价值、税率变化和抵销条件。"),
    ("business-combinations-purchase-date-contingent-consideration", "企业合并、购买日与或有对价", "20", "企业会计准则第20号-企业合并.html.md",
     "是否构成业务、控制取得日、同一控制关系、对价组成、或有对价条款、补偿性资产、购买日前关系",
     "先判断是否为企业合并及同一控制分类；非同一控制确定购买日和购买方，识别计量可辨认资产负债及对价；单独分析或有对价。",
     "购买日是控制实际转移日而非机械采用协议日或付款日；后续或有对价变动须区分计量期间调整与购买日后事项。",
     "同一控制以账面价值为基础；非同一控制采用购买法确认商誉或廉价购买利得，按分类处理或有对价后续计量。"),
    ("lease-term-modification-sale-leaseback", "租赁期、租赁变更与售后租回", "21", "企业会计准则第21号-租赁.html.md",
     "可执行期间、续租和终止选择权经济动因、购买选择权、变更范围和对价、转让是否满足收入准则",
     "确定不可撤销期间并评估合理确定选择权；变更先判断是否构成单独租赁；售后租回先判断资产转让是否为销售。",
     "含购买选择权的租赁不属于短期租赁；租赁期变化和范围缩减的重新计量路径不同；售后租回只确认转让权利相关利得。",
     "承租人确认使用权资产和租赁负债并按变更重估；售后租回按保留使用权比例计量，不确认与保留权利相关损益。"),
    ("financial-assets-classification-derecognition-ecl", "金融资产分类、终止确认与预期信用损失", "22-23", "企业会计准则第22号-金融工具确认和计量-财会〔2017〕7号.html.md",
     "合同现金流特征、业务模式、权利是否到期或转移、风险报酬和控制、信用风险显著增加、前瞻性情景",
     "初始确认后按业务模式和SPPI测试分类；转移时依次判断权利到期、风险报酬和控制；减值按适用范围选择一般或简化模型。",
     "业务模式在事实层面确定；终止确认不能只看法律转让；ECL需概率加权、货币时间价值及合理可支持前瞻信息。",
     "按摊余成本、其他综合收益或损益计量；符合条件时终止确认；确认或转回信用减值损失并充分披露模型和假设。"),
    ("financial-liability-equity-distinction", "金融负债与权益工具区分", "37", "企业会计准则第37号-金融工具列报-财会〔2017〕14号.html.md",
     "合同是否要求交付现金、发行人能否无条件避免、结算股数和金额、或有结算条款、清算顺序、补充协议",
     "从发行方合同义务出发判断是否存在交付现金或其他金融资产义务；再分析自身权益工具结算是否满足固定换固定。",
     "法律名称、无固定到期日或管理层主观意图不能替代合同分析；不由发行人控制的或有结算义务通常导致金融负债。",
     "按整体或复合工具分类确认负债和权益成分；负债利息计入损益，权益分派按权益交易处理并披露关键判断。"),
    ("consolidation-control-loss-of-control", "合并范围、实质控制与丧失控制权", "33", "企业会计准则第33号-合并财务报表.html.md",
     "被投资方相关活动、现时权利、可变回报、权力影响回报能力、代理人关系、结构化主体、处置安排整体性",
     "围绕权力、可变回报和影响回报能力三要素判断控制；持续重估事实变化；处置时判断是否丧失控制及多步交易是否一揽子。",
     "持股比例不是唯一标准；实质性潜在表决权、合同安排和事实上的主导能力均需考虑；保护性权利不产生控制。",
     "取得控制纳入合并；未丧失控制的权益变化作为权益交易；丧失控制时终止确认并按公允价值重新计量保留投资。"),
]


CASE_DATA = [
    ("custom-software-revenue", "定制软件开发服务收入确认", "revenue-recognition", "006-P020200717333926647357.pdf.md",
     "甲公司在客户现场开发不可替代的定制软件；客户拥有代码知识产权但开发中无法合理利用，中途更换供应商需重做；付款按里程碑，违约仅付合同价10%。",
     "客户在建控制权的法律可执行性、任一时点终止合同时对累计履约成本及合理利润的求偿权。",
     "是否满足时段履约三项条件。",
     "所给事实下三项条件均不满足，属于某一时点履约；尤其不可替代用途虽满足，但甲公司没有覆盖累计履约部分成本和合理利润的可执行收款权。",
     "按控制权在终验或其他实质转移时点确认收入；此前收款列合同负债。"),
    ("principal-agent-department-store", "百货联营主要责任人与代理人", "revenue-recognition", "009-P020201211394278955107.pdf.md",
     "专柜模式下供应商控制未售商品、负责定价并承担存货风险，百货公司统一收款并扣取10%；直营模式下百货公司验收、统一定价并承担客户责任。",
     "向客户承诺的特定商品、转让前调配权、退换货和滞销品最终风险。",
     "百货公司在不同经营模式下应按总额还是净额确认收入。",
     "控制而非收款开票决定身份。专柜例中供应商为主要责任人、百货公司为代理人；直营及验收后可主导商品的例中百货公司为主要责任人。",
     "主要责任人按总额，代理人按佣金净额确认收入；供应商向主要责任人的供货另按附退货条款处理。"),
    ("contract-modification-variable-consideration", "合同变更与可变对价", "revenue-recognition", "010-P020201211508217975565.pdf.md",
     "标准配件或广告服务合同履行中发生降价、折让或服务范围变化；案例分别设置合同开始日无折让预期和存在惯例两类事实。",
     "合同开始日是否已有导致隐含可变对价的惯例；新增商品是否可明确区分；新增价格是否反映单独售价。",
     "后续降价应作为可变对价重估还是合同变更，以及变更采用哪一路径。",
     "合同开始日没有可变对价事实时，新增权利义务通常是合同变更；已有折让惯例时是可变对价估计更新。剩余商品可区分时通常按原合同终止及新合同订立处理。",
     "可变对价变动按分摊规则调整已履约和未履约部分；合同变更按独立合同、未来法或累计追补法处理。"),
    ("standard-software-revenue-timing", "标准化软件收入确认时点", "revenue-recognition", "029-P020230103520876378094.pdf.md",
     "软件授权和介质已交付。例1客户可自动获得激活码，未激活仅因自身硬件未完成；例2必须付款并经供应商审核才可取得激活码。",
     "激活码是否只是行政步骤，供应商是否保留实质审核权，付款是否是取得控制的前提。",
     "交付、付款、生成激活码或实际使用何时构成控制权转移。",
     "例1激活无实质障碍，交付日即转移控制；例2供应商保留实质批准权，付款并批准生成激活码时才转移控制。",
     "在各自控制权转移日确认软件授权收入，不以客户实际开始使用为统一标准。"),
    ("presale-property-revenue", "预售商品房收入确认", "revenue-recognition", "034-P020231031581964779044.pdf.md",
     "房地产企业预售指定房号；购房人不能控制在建工程；房屋虽无替代用途，但客户违约仅支付合同价20%违约金。",
     "当地法律下对累计履约部分是否具有可执行收款权、购房人是否控制在建资产、解除合同的司法实践。",
     "预售房建造期间是否满足时段履约条件。",
     "案例事实下客户不控制在建商品房，企业也没有就累计履约部分取得成本加合理利润的可执行收款权，属于某一时点履约。",
     "通常在交付并转移控制权时确认收入；预收房款在此前列合同负债。"),
    ("shareholder-backstop-incentive", "大股东兜底式股权激励", "share-based-payment", "013-P020210518378130607194.pdf.md",
     "员工按公允价值取得公司回购股份，需连续服务三年；股价上涨归员工，股价下跌由控股股东以现金补偿。",
     "兜底安排是否以员工持续服务为条件、结算义务主体、控股股东是否代表集团提供激励。",
     "员工按公允价值购股但有下跌兜底，是否仍构成股份支付及如何分类。",
     "兜底使员工只享受上涨且与持续服务密切相关，整体构成股份支付；控股股东合并报表按现金结算，接受服务的甲公司无结算义务时按权益结算。",
     "分别在相关报表主体按现金结算或权益结算股份支付确认服务成本及负债或权益。"),
    ("restricted-shares", "授予限制性股票", "share-based-payment", "014-P020210518384054233794.pdf.md",
     "公司以每股5元向高管和技术人员授予附服务和业绩条件的限制性股票，未满足条件时公司按授予价回购。",
     "限制性股票类别、授予日是否完成批准、回购义务、可行权条件及预计可行权数量。",
     "限制性股票的股份支付计量与回购义务如何并行处理。",
     "取得员工服务构成权益结算股份支付，授予日确定公允价值并在等待期按最佳估计确认；回购义务按金融工具列报要求确认负债。",
     "等待期确认管理费用等及资本公积；收到认购款和库存股、回购义务按相关规定核算。"),
    ("sale-and-leaseback-variable-payments", "含可变付款的售后租回", "lease", "035-P020231207298200718851.pdf.md",
     "卖方兼承租人以180万元出售账面110万元建筑物并租回，租金含不取决于指数或比率的可变付款；案例分别设置可否合理估计预期付款。",
     "转让是否满足收入准则销售、租回权利比例、预期付款能否合理估计、实际付款与估计差异。",
     "售后租回初始及后续如何避免确认保留使用权相关损益。",
     "转让构成销售时，仅确认转让给买方权利相关利得；按预期租赁付款或保留权利比例计量使用权资产和租赁负债，后续不得确认保留权利相关损益。",
     "按解释第17号给定路径初始计量和后续调整，实际与估计差异按准则处理。"),
    ("liability-equity-investor-protection", "投资者保护条款下负债与权益区分", "financial-instruments", "028-P020220913413509669238.pdf.md",
     "无固定到期日票据在特定应急事件发生时由持有人大会要求回购或担保，发行人必须无条件接受；应急事件并非均由发行人控制。",
     "触发事件是否真实、是否由发行人控制、持有人大会决议是否对发行人具有合同约束力。",
     "无固定期限票据是否因投资者保护条款形成现金交付义务。",
     "发行人不能无条件避免交付现金或其他金融资产的合同义务，应确认为金融负债。",
     "按金融负债初始和后续计量，相关利息计入损益并披露关键合同条款。"),
    ("expected-credit-loss-simplified", "预期信用损失简化模型", "financial-instruments", "033-P020231025658077557643.pdf.md",
     "银行缺少内部评级体系，对公贷款采用迁徙率估计PD并用清收数据估计LGD，零售贷款采用损失率法，同时引入宏观情景。",
     "组合是否具有共同信用风险特征、历史数据质量、违约定义、处置周期、宏观变量相关性和情景权重。",
     "没有内部评级体系时如何形成概率加权、前瞻性的ECL。",
     "可采用迁徙率、历史清收和损失率等简化方法，但仍须反映PD、LGD、EAD或等价损失率、前瞻性情景和货币时间价值。",
     "按阶段或简化法计提损失准备，模型局限另以有依据的管理层叠加调整并披露。"),
    ("business-combination-indemnification-asset", "企业合并补偿性资产", "business-combination", "039-P020260618436842966610.pdf.md",
     "购买方取得目标公司100%股权，出售方承诺补偿购买日已存在未决诉讼损失；案例分别为全额补偿和仅补偿超过100万元部分。",
     "购买日被补偿项目是否确认、补偿权是否可收回、赔付门槛、个别和合并报表层次、后续判决信息属于何时事实。",
     "何时以及在哪一报表层面确认补偿性资产。",
     "合并报表在确认被补偿项目且补偿权满足确认条件时，以与被补偿项目一致的基础确认补偿性资产；个别报表需另按或有资产条件判断。",
     "补偿性资产与被补偿负债采用一致基础并受可收回性限制；结算时终止确认，区分计量期间调整与后续损益。"),
    ("inventory-settles-debt", "以存货清偿债务", "debt-restructuring", "qa-010.html.md",
     "债务人以存货清偿债务，交易属于债务重组而非企业日常销售活动。",
     "交易是否确属日常活动、原债务是否终止确认、存货账面价值及相关税费。",
     "是否应按存货销售确认收入和成本。",
     "通常不适用收入准则，不作为存货销售；所清偿债务账面价值与存货账面价值之间差额计入其他收益。",
     "终止确认债务和存货，差额按债务重组准则计入其他收益；税务处理另行判断。"),
    ("long-term-equity-investment-scope", "长期股权投资适用范围", "accounting-judgment", "qa-022.html.md",
     "企业持有被投资单位权益性投资，需要先判断控制、共同控制或重大影响。",
     "表决权、潜在表决权、董事会席位、合同一致同意安排、参与财务经营决策的事实。",
     "投资应适用长期股权投资准则还是金融工具准则。",
     "存在控制、共同控制或重大影响时适用长期股权投资准则；否则按金融工具准则。风险投资机构等明确例外按金融工具准则。",
     "根据适用准则选择成本法、权益法或金融资产分类计量，不以持股比例单一指标替代判断。"),
    ("short-term-lease-purchase-option", "含购买选择权的短期租赁", "lease", "qa-032.html.md",
     "租赁期不超过12个月，但合同包含购买选择权。",
     "购买选择权是否真实存在及合同整体是否为租赁；不因预计不行权而忽略明文排除。",
     "是否可作为短期租赁采用简化处理。",
     "包含购买选择权的租赁不属于短期租赁，即使租赁期不超过12个月。",
     "承租人不得采用短期租赁豁免，应按一般租赁规定确认使用权资产和租赁负债。"),
    ("data-resource-rd-capitalisation", "数据资源研发支出资本化", "intangible-assets", "qa-080.html.md",
     "内部数据资源研发项目需区分研究和开发阶段；开发阶段涉及技术可行性、完成意图、经济利益、资源保障和可靠计量。",
     "立项审批、技术验证、业务模式和市场、合法数据来源、资金团队、项目化成本归集和多项目分摊。",
     "开发阶段支出何时可以资本化为数据资源无形资产。",
     "研究阶段费用化；开发阶段只有五项条件同时满足才从满足之日起资本化，无法合理分摊的支出费用化。",
     "符合条件的支出归集为开发支出并在达到预定用途时转无形资产；建立项目台账和一致分摊方法。"),
]


EXISTING_CASES = [
    "2026-07-first-issue-long-term-equity-investment-confirmation.md",
    "2026-07-first-issue-temporary-fixed-asset-tax-difference.md",
    "2026-07-first-issue-government-grant-free-use-equipment.md",
    "2026-07-first-issue-equipment-sales-revenue-recognition.md",
    "2026-07-first-issue-overseas-sales-revenue-recognition.md",
]


def topic_page(item: tuple[str, ...]) -> str:
    slug, title, cas, source_name, facts, path, branches, accounting = item
    raw = f"{STANDARD_ROOT}/{source_name}"
    cases = [c for c in CASE_DATA if any(key in c[0] for key in slug.split("-")[:2])]
    case_links = "\n".join(f"- [[cases/golden-{c[0]}|{c[1]}]]" for c in cases) or "- 待从黄金案例库继续回挂。"
    return f"""---
title: {title}
type: concept
concept_type: accounting-judgment
created: {TODAY}
updated: {TODAY}
page_role: knowledge
maturity: draft
answer_ready: false
review_status: pending-human-review
source_verified: true
sources: [cas-{cas}]
raw_path: {raw}
tags: [accounting, judgment, golden-topic, cas-{cas}]
related: [[concepts/accounting-standards/cas-{cas.split('-')[0]}]], [[concepts/accounting-judgments/index]]
domain: accounting-standards
topic: accounting-judgments
---

# {title}

> 复核状态：本页已按现有财政部原文结构化，尚待人工或明确授权的 Agent 逐项复核。复核前不进入 AI 主检索集。

## 适用范围

用于判断与“{title}”直接相关的确认、计量、列报和披露问题。涉及税务、法律可执行性、估值或其他准则交叉事项时，应同时取得相应专业证据，不能把本专题替代具体合同和最新有效准则。

## 决定性事实

{facts}。信息不足时，应先补齐这些事实并给出条件化回答，不强行输出唯一结论。

## 准则入口

- [[concepts/accounting-standards/cas-{cas.split('-')[0]}|企业会计准则第{cas.split('-')[0]}号入口]]
- [[{raw}|财政部准则原文]]

## 判断路径

{path}

判断顺序固定为：确认交易实质和准则范围 -> 收集决定性事实 -> 选择适用条款 -> 对照各分支条件 -> 分别形成个别报表与合并报表结论（如适用）。

## 分支结论

{branches}

若合同权利、控制安排、估值输入或可执行性存在两种以上合理解释，应并列展示各分支、触发条件和报表影响。

## 会计处理

{accounting}

具体分录必须以企业科目表、计量数据和报告层次为基础；本页不给信息不足的交易虚构金额。

## 列报与披露

披露重大会计政策、关键判断、主要估计不确定性及其敏感性；对金额重大或高度依赖判断的事项，应说明事实、判断依据、变动原因和报表影响。涉及抵销、净额列报或不同报表层次时，应分别说明。

## 审计风险

- 管理层以合同形式或单一比例替代交易实质判断。
- 确认时点跨期、计量模型或关键参数偏向有利结果。
- 个别报表与合并报表处理混同，或遗漏关联方和特殊安排。
- 只保留结论，未保留反向证据、替代分支及否决理由。

## 证据与底稿

1. 保存完整合同、补充协议、审批文件和交易流程图。
2. 建立决定性事实清单，并将每项事实链接到原始证据。
3. 编制准则适用和分支判断备忘录，记录支持与反向证据。
4. 复核计算、分录、列报披露及期后事项，保留复核人和日期。

## 易错点

- 先确定目标会计结果，再选择支持性条款。
- 把官方原文、财政部案例和个人实务意见混在同一层次。
- 在关键事实缺失时输出无条件确定结论。
- 忽略准则版本、过渡安排和报告期适用日期。

## 案例链接

{case_links}

## 时效与不确定性边界

原文依据为本地财政部快照，检索日期以 raw frontmatter 为准。正式出具意见前应核验报告期适用版本及后续解释、实施问答和监管规则。上述“判断路径、审计风险和底稿”属于专业判断框架，不冒充准则原文。

## 原文引用

- [S1] [[{raw}|企业会计准则原文]]
- [S2] [[concepts/accounting-standards/cas-{cas.split('-')[0]}|准则资料入口]]
"""


def case_raw_path(slug: str, attachment: str) -> str:
    if attachment.startswith("qa-"):
        return f"raw/standards/accounting/implementation-qa-pages-v2/{attachment}"
    return f"raw/standards/accounting/application-case-attachments/{attachment}"


def case_page(item: tuple[str, ...]) -> str:
    slug, title, case_type, attachment, facts, missing, issue, conclusion, accounting = item
    raw = case_raw_path(slug, attachment)
    topic = {
        "revenue-recognition": "revenue-contract-control-transfer",
        "share-based-payment": "share-based-payment-recognition-modification",
        "lease": "lease-term-modification-sale-leaseback",
        "financial-instruments": "financial-assets-classification-derecognition-ecl",
        "business-combination": "business-combinations-purchase-date-contingent-consideration",
        "debt-restructuring": "debt-restructuring-recognition-measurement",
        "accounting-judgment": "long-term-equity-investment-scope-conversion",
        "intangible-assets": "intangibles-rd-capitalisation",
    }.get(case_type, "index")
    return f"""---
title: {title}
type: case
case_type: {case_type}
created: {TODAY}
updated: {TODAY}
page_role: case
maturity: draft
answer_ready: false
review_status: pending-human-review
source_verified: true
conclusion_certainty: high-for-stated-facts
sources: [mof-official-source]
raw_path: {raw}
tags: [case, golden-case, accounting, official-application]
related: [[concepts/accounting-judgments/{topic}]], [[cases/golden-cases-index]]
domain: cases
topic: {case_type}
---

# {title}

> 来源层级：财政部原文加工。下述事实和结论来自本地 raw 快照；审计程序和底稿建议是专业实务补充，二者分层展示。

## 原始事实

{facts}

## 缺失事实

{missing} 在将本案例迁移到实际项目时，还必须取得完整合同、报告期、交易金额、关联关系和期后变化；缺少这些事实时只能给条件化结论。

## 争议点

{issue}

## 适用准则

- [[concepts/accounting-judgments/{topic}|对应黄金专题]]
- [[{raw}|财政部原文]]

## 判断分支

1. 先确认原始事实是否与案例相同；任一决定性事实不同，都应回到专题判断路径。
2. 若缺失事实支持原文案例分支，则采用案例结论。
3. 若出现相反合同权利、控制证据或可执行性证据，则切换分支并重新评估确认时点和计量。

## 核心结论

{conclusion}

## 结论确定性

对原文列明事实为“高”；对其他企业的类比应用为“条件性”。本页不能证明实际合同的法律可执行性，也不替代报告期最新准则核验。

## 会计处理

{accounting}

## 审计程序

1. 将合同关键条款与本案例决定性事实逐项对照，检查是否存在未提供的补充协议或惯例。
2. 访谈业务、法务和财务人员，并以外部或系统证据验证管理层陈述。
3. 对确认时点、金额和报表层次重新执行，检查截止性、列报和披露。
4. 搜索反向证据和期后事项，评价是否需要改变分支或降低结论确定性。

## 底稿证据

- 完整合同、补充协议、审批和履约记录。
- 关键时点证据、计算表、分录及披露核对表。
- 决定性事实矩阵、替代分支及否决理由。
- 原文快照及其 `source_url`、`retrieved_at`、`sha256` 元数据。

## 原文引用

- [S1] [[{raw}|财政部案例或实施问答原文]]

## 时效与限制

本页整理日期为 {TODAY}。正式使用前应核验报告期适用准则和财政部后续更新。审计程序与底稿建议属于专业判断补充，不是财政部原文内容。
"""


def write_topics() -> None:
    TOPIC_ROOT.mkdir(parents=True, exist_ok=True)
    for item in TOPICS:
        (TOPIC_ROOT / f"{item[0]}.md").write_text(topic_page(item), encoding="utf-8")
    links = "\n".join(f"{i}. [[concepts/accounting-judgments/{item[0]}|{item[1]}]]" for i, item in enumerate(TOPICS, 1))
    index = f"""---
title: 会计判断黄金专题
type: concept
concept_type: index
created: {TODAY}
updated: {TODAY}
page_role: index
maturity: reviewed
answer_ready: false
sources: [golden-topic-program]
tags: [accounting, judgment, index, golden-topics]
related: [[cases/golden-cases-index]], [[concepts/kb-content-maturity-dashboard]]
---

# 会计判断黄金专题

本目录承载首版 20 个会计判断专题。目录页只负责导航，不作为独立专业结论。专题经人工或明确授权的 Agent 复核后才能将 `answer_ready` 设为 `true`。

{links}
"""
    (TOPIC_ROOT / "index.md").write_text(index, encoding="utf-8")


def write_cases() -> None:
    CASE_ROOT.mkdir(parents=True, exist_ok=True)
    for item in CASE_DATA:
        (CASE_ROOT / f"golden-{item[0]}.md").write_text(case_page(item), encoding="utf-8")
    for name in EXISTING_CASES:
        path = CASE_ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = update_frontmatter(text, {
            "page_role": "case",
            "maturity": "draft",
            "answer_ready": False,
            "review_status": "pending-human-review",
        })
        metadata, _ = parse_frontmatter(text)
        if "## 缺失事实" not in text:
            raw = metadata.get("raw_path", "")
            text += f"""

## 缺失事实

将本案例用于其他项目时，需补齐完整合同及补充协议、交易时间线、金额、关联关系、审批和期后执行情况。任何影响控制、可执行权利或计量基础的事实变化，均可能改变结论。

## 结论确定性

现有结论属于对所列事实的专业判断意见，尚待指定复核人对原始材料和报告期准则逐项复核；复核前不进入 AI 主检索集。

## 原文引用与边界

- [S1] [[{raw}|本案例原始材料]]

原始材料来自内部研讨，不属于财政部准则原文；页面中的个人意见必须与官方准则依据分层使用。
"""
        path.write_text(text, encoding="utf-8")
    all_cases = [(p.stem, parse_frontmatter(p.read_text(encoding="utf-8"))[0].get("title", p.stem)) for p in sorted(CASE_ROOT.glob("golden-*.md")) if p.name != "golden-cases-index.md"]
    existing = [(Path(name).stem, parse_frontmatter((CASE_ROOT / name).read_text(encoding="utf-8"))[0].get("title", name)) for name in EXISTING_CASES if (CASE_ROOT / name).exists()]
    links = "\n".join(f"{i}. [[cases/{slug}|{title}]]" for i, (slug, title) in enumerate(existing + all_cases, 1))
    index = f"""---
title: 会计判断黄金案例
type: concept
concept_type: index
created: {TODAY}
updated: {TODAY}
page_role: index
maturity: reviewed
answer_ready: false
sources: [golden-case-program]
tags: [cases, accounting, index, golden-cases]
related: [[concepts/accounting-judgments/index]], [[concepts/kb-content-maturity-dashboard]]
---

# 会计判断黄金案例

首版共 20 个案例：5 个内部研讨案例升级稿、11 个财政部应用案例、4 个财政部实施问答。内部研讨意见与官方原文分层展示。全部案例在人工或明确授权的 Agent 复核前保持草稿状态。

{links}
"""
    (CASE_ROOT / "golden-cases-index.md").write_text(index, encoding="utf-8")


def append_cas_backlinks() -> None:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for slug, title, cas, *_ in TOPICS:
        grouped.setdefault(cas.split("-")[0], []).append((slug, title))
    marker = "<!-- golden-judgments:start -->"
    end_marker = "<!-- golden-judgments:end -->"
    for cas, items in grouped.items():
        path = KB_ROOT / "wiki" / "concepts" / "accounting-standards" / f"cas-{cas}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        block = marker + "\n\n## 会计判断专题\n\n" + "\n".join(
            f"- [[concepts/accounting-judgments/{slug}|{title}]]" for slug, title in items
        ) + "\n\n" + end_marker
        if marker in text and end_marker in text:
            start = text.index(marker)
            end = text.index(end_marker, start) + len(end_marker)
            text = text[:start] + block + text[end:]
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
        path.write_text(text, encoding="utf-8")


def main() -> None:
    write_topics()
    write_cases()
    append_cas_backlinks()
    print(f"topics={len(TOPICS)}")
    print(f"cases={len(CASE_DATA) + len(EXISTING_CASES)}")


if __name__ == "__main__":
    main()
