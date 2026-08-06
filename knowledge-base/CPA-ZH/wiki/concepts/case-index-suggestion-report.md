---
title: 案例主题索引自动回挂建议报告
type: concept
concept_type: maintenance-dashboard
page_role: index
maturity: reviewed
answer_ready: false
created: 2026-08-06
updated: 2026-08-06
sources: [case-index-suggest]
tags: [case, case-index, automation, maintenance]
related: [[concepts/case-topic-index]], [[concepts/cpa-zh-case-index-helper]], [[concepts/case-analysis]]
domain: cases
topic: index
---

# 案例主题索引自动回挂建议报告

本页由 `tools/kb_case_index_suggest.py --write-report` 生成，用于检查 `wiki/cases/` 案例卡片是否已回挂到主题索引，并给出新增索引行建议。

## 总览

| 指标 | 数量 |
|---|---:|
| 案例卡片 | 24 |
| 已在主题索引出现 | 24 |
| 待补入主题索引 | 0 |

## 按会计主题建议

| 主题 | 案例 | 建议关键判断 | 当前索引状态 |
|---|---|---|---|
| revenue-recognition | [[cases/2026-07-first-issue-equipment-sales-revenue-recognition]] | 个人意见：本案回购条款触发条件偏质保属性，且客户未必具有重大经济动因行使要求权，通常可以按附有销售退回条款的销售交易处理；但是否在交付时点确认全部收入，仍要看控制权是否已经转移以… | 已出现 |
| accounting-judgment | [[cases/2026-07-first-issue-government-grant-free-use-equipment]] | 个人意见：这类“免费使用设备、但设备所有权并未转移”的安排，通常不宜直接按政府补助确认。实务中更常见的处理是：不确认政府补助，按实际发生的相关费用和租赁/使用安排处理。 | 已出现 |
| accounting-judgment | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | 个人意见：A 公司原持有 D 公司的长期股权投资转为对 C 公司的长期股权投资时，应按原账面价值结转，不宜按公允价值重新计量，也不应确认投资收益。 | 已出现 |
| revenue-recognition | [[cases/2026-07-first-issue-overseas-sales-revenue-recognition]] | 个人意见：这类案件的核心不在于“有没有出口”和“回款是不是到位”，而在于产品交付与组装调试是否真的构成两个可明确区分的履约义务，以及供货部分在交付时点是否已经转移控制权。若组装调… | 已出现 |
| case-other | [[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]] | 个人意见：税法对暂估转固 12 个月取得发票的要求是刚性的。超过保护期仍未取得发票的，实务上更稳妥的处理是先做纳税调增，并就由此形成的可抵扣暂时性差异确认递延所得税资产；待后续取… | 已出现 |
| case-other | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 现有材料不足以支持 A 公司实现出表。不能仅凭 A 无单方表决权得出不控制结论；应分别识别正常期、预警期和违约期最显著影响回报的相关活动，再判断 A 的运营处置权、B 的预警处置… | 已出现 |
| case-other | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 应先判断交易是真实租赁还是融资公司仅代付购置款的“以租代买”。真实租赁下，设备于 2025 年 7 月交付且由承租人主导安装时，很可能已到租赁期开始日；以租代买下则应确认在建工程… | 已出现 |
| revenue-recognition | [[cases/2026-08-first-issue-medical-distributor-revenue]] | 实际买断成立时，一级经销商签收可作为控制权转移时点，不必等终端纯销；但企业必须在签收时估计纯销折扣和预期退货，不能先全额确认再按实际数冲减。持续接受非质量滞销退货可能形成惯例性退… | 已出现 |
| case-other | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 收费试车是达到预定可使用状态的强证据，但不是自动结论。应锁定首次证明试车台能够按设计目的安全、稳定提供服务的日期；转固前必要测试不计折旧，转固后发生的试车应按工作量法在对应期间计… | 已出现 |
| business-combination | [[cases/golden-business-combination-indemnification-asset]] | 企业合并补偿性资产 | 已出现 |
| revenue-recognition | [[cases/golden-contract-modification-variable-consideration]] | 合同变更与可变对价 | 已出现 |
| revenue-recognition | [[cases/golden-custom-software-revenue]] | 定制软件开发服务收入确认 | 已出现 |
| intangible-assets | [[cases/golden-data-resource-rd-capitalisation]] | 数据资源研发支出资本化 | 已出现 |
| financial-instruments | [[cases/golden-expected-credit-loss-simplified]] | 预期信用损失简化模型 | 已出现 |
| debt-restructuring | [[cases/golden-inventory-settles-debt]] | 以存货清偿债务 | 已出现 |
| financial-instruments | [[cases/golden-liability-equity-investor-protection]] | 投资者保护条款下负债与权益区分 | 已出现 |
| accounting-judgment | [[cases/golden-long-term-equity-investment-scope]] | 长期股权投资适用范围 | 已出现 |
| revenue-recognition | [[cases/golden-presale-property-revenue]] | 预售商品房收入确认 | 已出现 |
| revenue-recognition | [[cases/golden-principal-agent-department-store]] | 百货联营主要责任人与代理人 | 已出现 |
| share-based-payment | [[cases/golden-restricted-shares]] | 授予限制性股票 | 已出现 |
| lease | [[cases/golden-sale-and-leaseback-variable-payments]] | 含可变付款的售后租回 | 已出现 |
| share-based-payment | [[cases/golden-shareholder-backstop-incentive]] | 大股东兜底式股权激励 | 已出现 |
| lease | [[cases/golden-short-term-lease-purchase-option]] | 含购买选择权的短期租赁 | 已出现 |
| revenue-recognition | [[cases/golden-standard-software-revenue-timing]] | 标准化软件收入确认时点 | 已出现 |

## 按准则入口建议

| 准则或专题入口 | 案例 | 复用问题 | 当前索引状态 |
|---|---|---|---|
| [[concepts/accounting-standards/cas-14]] | [[cases/2026-07-first-issue-equipment-sales-revenue-recognition]] | 骨科手术导航设备销售的收入确认 | 已出现 |
| [[concepts/accounting-standards/cas-16]] | [[cases/2026-07-first-issue-government-grant-free-use-equipment]] | 免费使用设备是否属于政府补助 | 已出现 |
| [[concepts/first-section-topics/long-term-equity-investments]] | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | A公司持有D公司长期股权投资转换为C公司投资的确认 | 已出现 |
| [[concepts/accounting-standards/cas-02]] | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | A公司持有D公司长期股权投资转换为C公司投资的确认 | 已出现 |
| [[concepts/accounting-standards/cas-07]] | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | A公司持有D公司长期股权投资转换为C公司投资的确认 | 已出现 |
| [[concepts/first-section-topics/consolidation-scope-control]] | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | A公司持有D公司长期股权投资转换为C公司投资的确认 | 已出现 |
| [[concepts/accounting-standards/cas-14]] | [[cases/2026-07-first-issue-overseas-sales-revenue-recognition]] | 海外销售定制化产品的收入确认 | 已出现 |
| [[concepts/accounting-standards/cas-18]] | [[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]] | 暂估转固超过12个月的税会差异处理 | 已出现 |
| [[concepts/accounting-standards/cas-08]] | [[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]] | 暂估转固超过12个月的税会差异处理 | 已出现 |
| [[concepts/accounting-standards/cas-33]] | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 结构化不良资产平台能否实现原地产项目出表 | 已出现 |
| [[concepts/accounting-standards/cas-40]] | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 结构化不良资产平台能否实现原地产项目出表 | 已出现 |
| [[concepts/first-section-topics/consolidation-scope-control]] | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 结构化不良资产平台能否实现原地产项目出表 | 已出现 |
| [[concepts/accounting-standards/cas-21]] | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 未达预定可使用状态的融资租赁设备如何确认和折旧 | 已出现 |
| [[concepts/accounting-standards/cas-17]] | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 未达预定可使用状态的融资租赁设备如何确认和折旧 | 已出现 |
| [[concepts/accounting-standards/cas-04]] | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 未达预定可使用状态的融资租赁设备如何确认和折旧 | 已出现 |
| [[concepts/accounting-standards/cas-14]] | [[cases/2026-08-first-issue-medical-distributor-revenue]] | 医疗经销模式下签收、纯销折扣与滞销退货的收入确认 | 已出现 |
| [[concepts/accounting-standards/cas-04]] | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 商业航天动力试车台的转固时点与工作量法折旧 | 已出现 |
| [[concepts/accounting-standards/cas-17]] | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 商业航天动力试车台的转固时点与工作量法折旧 | 已出现 |
| [[concepts/accounting-standards/interpretations/interp-15]] | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 商业航天动力试车台的转固时点与工作量法折旧 | 已出现 |
| 待人工指定 | [[cases/golden-business-combination-indemnification-asset]] | 企业合并补偿性资产 | 已出现 |
| 待人工指定 | [[cases/golden-contract-modification-variable-consideration]] | 合同变更与可变对价 | 已出现 |
| 待人工指定 | [[cases/golden-custom-software-revenue]] | 定制软件开发服务收入确认 | 已出现 |
| 待人工指定 | [[cases/golden-data-resource-rd-capitalisation]] | 数据资源研发支出资本化 | 已出现 |
| 待人工指定 | [[cases/golden-expected-credit-loss-simplified]] | 预期信用损失简化模型 | 已出现 |
| 待人工指定 | [[cases/golden-inventory-settles-debt]] | 以存货清偿债务 | 已出现 |
| 待人工指定 | [[cases/golden-liability-equity-investor-protection]] | 投资者保护条款下负债与权益区分 | 已出现 |
| 待人工指定 | [[cases/golden-long-term-equity-investment-scope]] | 长期股权投资适用范围 | 已出现 |
| 待人工指定 | [[cases/golden-presale-property-revenue]] | 预售商品房收入确认 | 已出现 |
| 待人工指定 | [[cases/golden-principal-agent-department-store]] | 百货联营主要责任人与代理人 | 已出现 |
| 待人工指定 | [[cases/golden-restricted-shares]] | 授予限制性股票 | 已出现 |
| 待人工指定 | [[cases/golden-sale-and-leaseback-variable-payments]] | 含可变付款的售后租回 | 已出现 |
| 待人工指定 | [[cases/golden-shareholder-backstop-incentive]] | 大股东兜底式股权激励 | 已出现 |
| 待人工指定 | [[cases/golden-short-term-lease-purchase-option]] | 含购买选择权的短期租赁 | 已出现 |
| 待人工指定 | [[cases/golden-standard-software-revenue-timing]] | 标准化软件收入确认时点 | 已出现 |

## 按审计风险建议

| 风险类型 | 案例 | 建议审计关注点 | 当前索引状态 |
|---|---|---|---|
| 收入提前确认 | [[cases/2026-07-first-issue-equipment-sales-revenue-recognition]] | 个人意见：本案回购条款触发条件偏质保属性，且客户未必具有重大经济动因行使要求权，通常可以按附有销售退回条款的销售交易处理；但是否在交付时点确认全部收入，仍要看控制权是否已经转移以… | 已出现 |
| 政府支持收益化 | [[cases/2026-07-first-issue-government-grant-free-use-equipment]] | 个人意见：这类“免费使用设备、但设备所有权并未转移”的安排，通常不宜直接按政府补助确认。实务中更常见的处理是：不确认政府补助，按实际发生的相关费用和租赁/使用安排处理。 | 已出现 |
| 内部重组确认收益 | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | 个人意见：A 公司原持有 D 公司的长期股权投资转为对 C 公司的长期股权投资时，应按原账面价值结转，不宜按公允价值重新计量，也不应确认投资收益。 | 已出现 |
| 收入提前确认 | [[cases/2026-07-first-issue-overseas-sales-revenue-recognition]] | 个人意见：这类案件的核心不在于“有没有出口”和“回款是不是到位”，而在于产品交付与组装调试是否真的构成两个可明确区分的履约义务，以及供货部分在交付时点是否已经转移控制权。若组装调… | 已出现 |
| 税务申报与递延所得税 | [[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]] | 个人意见：税法对暂估转固 12 个月取得发票的要求是刚性的。超过保护期仍未取得发票的，实务上更稳妥的处理是先做纳税调增，并就由此形成的可抵扣暂时性差异确认递延所得税资产；待后续取… | 已出现 |
| 待人工分类 | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 现有材料不足以支持 A 公司实现出表。不能仅凭 A 无单方表决权得出不控制结论；应分别识别正常期、预警期和违约期最显著影响回报的相关活动，再判断 A 的运营处置权、B 的预警处置… | 已出现 |
| 待人工分类 | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 应先判断交易是真实租赁还是融资公司仅代付购置款的“以租代买”。真实租赁下，设备于 2025 年 7 月交付且由承租人主导安装时，很可能已到租赁期开始日；以租代买下则应确认在建工程… | 已出现 |
| 收入提前确认 | [[cases/2026-08-first-issue-medical-distributor-revenue]] | 实际买断成立时，一级经销商签收可作为控制权转移时点，不必等终端纯销；但企业必须在签收时估计纯销折扣和预期退货，不能先全额确认再按实际数冲减。持续接受非质量滞销退货可能形成惯例性退… | 已出现 |
| 待人工分类 | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 收费试车是达到预定可使用状态的强证据，但不是自动结论。应锁定首次证明试车台能够按设计目的安全、稳定提供服务的日期；转固前必要测试不计折旧，转固后发生的试车应按工作量法在对应期间计… | 已出现 |
| 待人工分类 | [[cases/golden-business-combination-indemnification-asset]] | 企业合并补偿性资产 | 已出现 |
| 收入提前确认 | [[cases/golden-contract-modification-variable-consideration]] | 合同变更与可变对价 | 已出现 |
| 收入提前确认 | [[cases/golden-custom-software-revenue]] | 定制软件开发服务收入确认 | 已出现 |
| 待人工分类 | [[cases/golden-data-resource-rd-capitalisation]] | 数据资源研发支出资本化 | 已出现 |
| 待人工分类 | [[cases/golden-expected-credit-loss-simplified]] | 预期信用损失简化模型 | 已出现 |
| 政府支持收益化 | [[cases/golden-inventory-settles-debt]] | 以存货清偿债务 | 已出现 |
| 待人工分类 | [[cases/golden-liability-equity-investor-protection]] | 投资者保护条款下负债与权益区分 | 已出现 |
| 待人工分类 | [[cases/golden-long-term-equity-investment-scope]] | 长期股权投资适用范围 | 已出现 |
| 收入提前确认 | [[cases/golden-presale-property-revenue]] | 预售商品房收入确认 | 已出现 |
| 收入提前确认 | [[cases/golden-principal-agent-department-store]] | 百货联营主要责任人与代理人 | 已出现 |
| 待人工分类 | [[cases/golden-restricted-shares]] | 授予限制性股票 | 已出现 |
| 待人工分类 | [[cases/golden-sale-and-leaseback-variable-payments]] | 含可变付款的售后租回 | 已出现 |
| 待人工分类 | [[cases/golden-shareholder-backstop-incentive]] | 大股东兜底式股权激励 | 已出现 |
| 待人工分类 | [[cases/golden-short-term-lease-purchase-option]] | 含购买选择权的短期租赁 | 已出现 |
| 收入提前确认 | [[cases/golden-standard-software-revenue-timing]] | 标准化软件收入确认时点 | 已出现 |

## 按底稿用途建议

| 底稿用途 | 案例 | 建议留痕材料 | 当前索引状态 |
|---|---|---|---|
| 控制权转移备忘录 | [[cases/2026-07-first-issue-equipment-sales-revenue-recognition]] | 1. 保留购销合同、回购条款、验收记录。 2. 形成控制权转移判断备忘录。 3. 对退回概率、返修概率和回购条款实质形成估计底稿。 | 已出现 |
| 政府补助判断备忘录 | [[cases/2026-07-first-issue-government-grant-free-use-equipment]] | 1. 保存采购合同、代管协议、园区管理文件。 2. 记录设备所有权和使用权的法律安排。 3. 明确不确认政府补助的判断依据。 | 已出现 |
| 商业实质判断备忘录 | [[cases/2026-07-first-issue-long-term-equity-investment-confirmation]] | 1. 保存吸收合并协议、换股方案、股东会或董事会决议。 2. 保存交易前后股权结构图，并标明 A、B、C、D 的控制链条。 3. 保存评估报告和定价协商资料，但单独说明“公允价值… | 已出现 |
| 控制权转移备忘录 | [[cases/2026-07-first-issue-overseas-sales-revenue-recognition]] | 1. 保存原合同和补充协议。 2. 保存发运、报关、交付和回款证据。 3. 形成履约义务拆分判断备忘录。 4. 对供货和调试收入分拆的测算和依据留痕。 | 已出现 |
| 税会差异测算表 | [[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]] | 1. 保存暂估转固依据、验收资料和设备清单。 2. 保存发票取得时间表和超期说明。 3. 保存税会差异测算表和汇算清缴申报调整表。 4. 保存递延所得税资产确认依据和可实现性判断。 | 已出现 |
| 待人工分类 | [[cases/2026-08-first-issue-consolidation-structured-platform]] | 现有材料不足以支持 A 公司实现出表。不能仅凭 A 无单方表决权得出不控制结论；应分别识别正常期、预警期和违约期最显著影响回报的相关活动，再判断 A 的运营处置权、B 的预警处置… | 已出现 |
| 待人工分类 | [[cases/2026-08-first-issue-lease-asset-not-ready]] | 应先判断交易是真实租赁还是融资公司仅代付购置款的“以租代买”。真实租赁下，设备于 2025 年 7 月交付且由承租人主导安装时，很可能已到租赁期开始日；以租代买下则应确认在建工程… | 已出现 |
| 控制权转移备忘录 | [[cases/2026-08-first-issue-medical-distributor-revenue]] | 实际买断成立时，一级经销商签收可作为控制权转移时点，不必等终端纯销；但企业必须在签收时估计纯销折扣和预期退货，不能先全额确认再按实际数冲减。持续接受非质量滞销退货可能形成惯例性退… | 已出现 |
| 税会差异测算表 | [[cases/2026-08-first-issue-space-test-bench-capitalization]] | 收费试车是达到预定可使用状态的强证据，但不是自动结论。应锁定首次证明试车台能够按设计目的安全、稳定提供服务的日期；转固前必要测试不计折旧，转固后发生的试车应按工作量法在对应期间计… | 已出现 |
| 待人工分类 | [[cases/golden-business-combination-indemnification-asset]] | 企业合并补偿性资产 | 已出现 |
| 控制权转移备忘录 | [[cases/golden-contract-modification-variable-consideration]] | 合同变更与可变对价 | 已出现 |
| 控制权转移备忘录 | [[cases/golden-custom-software-revenue]] | 定制软件开发服务收入确认 | 已出现 |
| 待人工分类 | [[cases/golden-data-resource-rd-capitalisation]] | 数据资源研发支出资本化 | 已出现 |
| 待人工分类 | [[cases/golden-expected-credit-loss-simplified]] | 预期信用损失简化模型 | 已出现 |
| 待人工分类 | [[cases/golden-inventory-settles-debt]] | 以存货清偿债务 | 已出现 |
| 待人工分类 | [[cases/golden-liability-equity-investor-protection]] | 投资者保护条款下负债与权益区分 | 已出现 |
| 待人工分类 | [[cases/golden-long-term-equity-investment-scope]] | 长期股权投资适用范围 | 已出现 |
| 控制权转移备忘录 | [[cases/golden-presale-property-revenue]] | 预售商品房收入确认 | 已出现 |
| 控制权转移备忘录 | [[cases/golden-principal-agent-department-store]] | 百货联营主要责任人与代理人 | 已出现 |
| 待人工分类 | [[cases/golden-restricted-shares]] | 授予限制性股票 | 已出现 |
| 待人工分类 | [[cases/golden-sale-and-leaseback-variable-payments]] | 含可变付款的售后租回 | 已出现 |
| 待人工分类 | [[cases/golden-shareholder-backstop-incentive]] | 大股东兜底式股权激励 | 已出现 |
| 待人工分类 | [[cases/golden-short-term-lease-purchase-option]] | 含购买选择权的短期租赁 | 已出现 |
| 控制权转移备忘录 | [[cases/golden-standard-software-revenue-timing]] | 标准化软件收入确认时点 | 已出现 |

## 使用方式

1. 若状态为“建议补入”，由 Agent 复核案例标签、来源和判断边界后回挂到 [[concepts/case-topic-index]]；`agent-reviewed` 不等于人工批准。
2. 若主题、风险或底稿用途不准确，优先修订案例卡片的 `tags`、`related` 和正文关键词。
3. 新增案例后先运行 dry-run，再写入本报告。

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-index
.\.venv\Scripts\python.exe tools\kb.py case-index --write-report
```

_生成路径：`wiki/concepts/case-index-suggestion-report.md`_
