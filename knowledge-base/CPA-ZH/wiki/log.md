---
title: CPA-ZH 知识库日志
type: source
source_type: activity-log
created: 2026-06-26
updated: 2026-06-26
tags: [cpa, log, structured]
---

# CPA-ZH 知识库日志

## 2026-06-26 | bootstrap

- 建立知识库根目录与三层结构。
- 补齐四部核心法律条款级索引。
- 生成企业会计准则编号索引与 42 个准则页。
- 生成中国注册会计师执业准则编号索引与 40 个准则页。
- 生成企业会计准则解释页 20 个，并记录官方有效链接。
- 生成企业会计准则未映射资料校准专题页 26 个，入口为 [[concepts/accounting-standards/calibration/index]]。
- 将校准补充资料回挂到正式准则页、解释页和其他规定专题页；新增 [[concepts/accounting-standards/other-rules/index]]。
- 新增 [[concepts/audit-standards/topics]]，按审计流程和高频实务问题组织中注协执业准则入口。
- 新增 [[concepts/first-section-completion-map]]，汇总第一板块完成度、关键索引文件和后续完善清单。
- 升级第一板块 14 个高频准则页：为 6 个企业会计准则页补充判断框架，为 8 个审计准则页补充程序设计框架、审计关注点和底稿提示。
- 升级四部核心法律概览页：为 [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]] 补充有效版本线索、核心义务地图、审计实务连接和风险提示。
- 新增 [[concepts/first-section-topic-matrix]] 和 6 个第一板块实务专题页：收入确认错报风险、金融工具估值与减值、合并范围与控制判断、持续经营、关键审计事项、证券服务责任。
- 扩展第一板块专题矩阵：新增 [[concepts/first-section-topics/related-parties-fund-occupation]], [[concepts/first-section-topics/asset-impairment]], [[concepts/first-section-topics/profit-distribution-equity-transactions]]，专题页总数增至 9 个。
- 一次性维护第一板块剩余项目：专题矩阵扩展至 14 个实务专题；高频判断/程序框架页增至 28 个；新增 [[concepts/core-laws-official-verification]] 和 [[concepts/first-section-responsibility-risk-map]]。
- 维护第二板块行业重要政策性文件：升级 7 份政策文件页，新增 [[concepts/policy-document-comparison]], [[concepts/policy-implementation-map]], [[concepts/policy-official-link-checklist]]，用于政策对照、执行落地和官方链接核验。
- 核验第二板块 7 份政策文件官方链接，更新 [[concepts/policy-official-link-checklist]] 和各政策页“官方来源”，新增 [[sources/policy-documents-official-links-2026-06-29]]。
- 执行第二板块 2.0：归档 7 份官方原文至 `raw/policies/second-section/`，新增 [[sources/policy-documents-raw-archive-2026-06-29]], [[concepts/policy-version-validity-tracker]], [[concepts/policy-execution-checklist]]，并将本地归档路径回写至各政策页。
- 执行第三板块 1.0：以中注协“职业道德规范”专题页为主入口，归档行业史、职业道德守则（2020）、独立性准则第1号、2026 应用指南等 24 个官方来源/附件及历史补充归档；升级 [[concepts/history-ethics-independence]], [[concepts/industry-history]], [[concepts/ethics-code]], [[concepts/independence-standard-1]]；新增 [[sources/third-section-official-archive-2026-06-29]]。
- 升级知识库检索与维护能力：新增官方来源注册表 `source-registry.yml`，新增本地检索、manifest 审计和链接汇总工具；建立 [[concepts/kb-maintenance-workflow]] 和 [[sources/kb-retrieval-upgrade-2026-06-29]]；初始索引 1385 条记录，manifest 审计通过。
- 导入 2026年7月第一期实务案例 5 个 Word 文件至 `raw/cases/2026-07-first-issue/`；新增 [[sources/case-batch-2026-07-first-issue]]，升级 [[concepts/case-analysis]] 的案例库维护结构。
- 加工首张实务案例卡片：[[cases/2026-07-first-issue-long-term-equity-investment-confirmation]]，沉淀 A 公司持有 D 公司长期股权投资转换为 C 公司投资的确认判断，并回挂 [[concepts/first-section-topics/long-term-equity-investments]] 和 [[sources/case-batch-2026-07-first-issue]]。
- 继续加工 4 张实务案例卡片：[[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]]、[[cases/2026-07-first-issue-government-grant-free-use-equipment]]、[[cases/2026-07-first-issue-equipment-sales-revenue-recognition]]、[[cases/2026-07-first-issue-overseas-sales-revenue-recognition]]，分别覆盖暂估转固税会差异、免费使用设备政府补助判断、设备销售售后回购收入确认和海外销售履约义务拆分。
- 增加技术维护工具：新增 `tools/kb_health_check.py` 一键体检和 `tools/kb_update_readme_stats.py` README 统计刷新；更新 `README.md` 和 [[concepts/kb-maintenance-workflow]] 的维护命令。
- 升级 raw 正文处理能力：新增 `tools/kb_text_cache.py` 文本抽取缓存，`kb_search.py` 重建索引时优先复用 `cache/text/`，`kb_health_check.py` 增加文本缓存状态检查；同步更新 `README.md` 和 [[concepts/kb-maintenance-workflow]]。
- 增强案例库可用性：新增 [[concepts/case-topic-index]]，将 5 张案例卡片按会计主题、准则入口、审计风险和底稿用途重新组织，并回挂 [[concepts/case-analysis]] 与总索引。
- 增加新手使用入口：新增 [[concepts/kb-user-guide]]，用操作手册形式说明 CPA-ZH 的三层结构、四大板块、检索方法、新增资料规则、案例使用方式和维护命令；并回挂 README 与总索引。
- 归档发行监管规则：从用户提供的本地底稿目录归档 `发行类第9号.pdf` 至 `raw/policies/issuance-guidance/issuance-class-09-rd-staff-investment/official.pdf`；按用户提供的证监会官方链接 `https://www.csrc.gov.cn/csrc/c101802/c7445462/content.shtml` 更新来源信息；新增 [[sources/issuance-guidance-rd-staff-investment-archive-2026-07-09]] 和 [[concepts/securities-issuance-rd-staff-investment]]，并回挂政策入口、证券服务责任专题和总索引。该 PDF 常规文本抽取为空，已标注为待 OCR。
- 增加来源状态仪表盘：新增 `tools/kb_source_status.py` 和 [[concepts/source-status-dashboard]]，按 manifest 条目追踪官方链接、文本缓存和 OCR 状态；当前 37 个 manifest 条目均已进入文本缓存，其中 12 个 PDF 待 OCR。
