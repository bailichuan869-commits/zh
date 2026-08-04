---
title: 来源状态仪表盘
type: concept
concept_type: maintenance-dashboard
created: 2026-07-27
updated: 2026-07-27
sources: [kb-source-status]
tags: [maintenance, source-status, archive, ocr, official-link, dual-track]
related: [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]]
domain: sources
topic: dashboards
---

# 来源状态仪表盘

本页由 `tools/kb_source_status.py write-report` 生成，用于追踪 raw manifest 来源的官方链接、原件、Markdown 派生件、文本缓存和后续维护动作。

## 总览

| 指标 | 数量 |
|---|---:|
| manifest 条目 | 98 |
| 有 URL 条目 | 32 |
| 官方页面已核验 | 1 |
| 有 Markdown 派生件 | 40 |
| 已进入文本缓存 | 98 |
| 缓存中有可检索正文 | 98 |

## 文件类型

| 类型 | 数量 |
|---|---:|
| `.docx` | 5 |
| `.html` | 21 |
| `.md` | 58 |
| `.pdf` | 14 |

## 待办类型

| 待办 | 数量 |
|---|---:|
| `missing-official-url` | 1 |

## 待处理条目

| 条目 | 文号 | 来源 | 状态 | 待办 | wiki |
|---|---|---|---|---|---|
| 练习题库（试卷一）答案解析 |  | 北京国家会计学院国会在线 | source=local; text=ok; ocr=not-required; derived=ok | `missing-official-url` | [[sources/practice-question-bank-paper-1-answer-explanations-2026-07-13]] |

## 全部 manifest 条目

| 条目 | 原件 | Markdown 派生件 | URL | 缓存正文长度 | wiki |
|---|---|---|---|---:|---|
| 11部研讨会议题【暂估转固税会差异问题】（7月-第1期） | `raw/cases/2026-07-first-issue/11部研讨会议题【暂估转固税会差异问题】（7月-第1期）.docx` | `raw/cases/2026-07-first-issue/11部研讨会议题【暂估转固税会差异问题】（7月-第1期）.docx.md` |  | 2796 |  |
| 29部研讨会议题【政府补助确认】（7月-第一期） | `raw/cases/2026-07-first-issue/29部研讨会议题【政府补助确认】（7月-第一期）.docx` | `raw/cases/2026-07-first-issue/29部研讨会议题【政府补助确认】（7月-第一期）.docx.md` |  | 2558 |  |
| 2部研讨会议题【收入确认】（7月-第一期） | `raw/cases/2026-07-first-issue/2部研讨会议题【收入确认】（7月-第一期）.docx` | `raw/cases/2026-07-first-issue/2部研讨会议题【收入确认】（7月-第一期）.docx.md` |  | 2363 |  |
| 32部研讨会议题【长期股权投资的确认】（7月-第一期） | `raw/cases/2026-07-first-issue/32部研讨会议题【长期股权投资的确认】（7月-第一期）.docx` | `raw/cases/2026-07-first-issue/32部研讨会议题【长期股权投资的确认】（7月-第一期）.docx.md` |  | 1349 |  |
| 天津分所审计6部研讨会议题【收入确认】（7月-第一期） | `raw/cases/2026-07-first-issue/天津分所审计6部研讨会议题【收入确认】（7月-第一期）.docx` | `raw/cases/2026-07-first-issue/天津分所审计6部研讨会议题【收入确认】（7月-第一期）.docx.md` |  | 2575 |  |
| 中注协专业标准：职业道德规范专题页 | `raw/ethics/third-section/professional-ethics-index/official.html` | `raw/ethics/third-section/professional-ethics-index/official.html.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/ | 1343 | [[concepts/history-ethics-independence]] |
| 《中国注册会计师行业发展报告2024》出版发行 | `raw/ethics/third-section/industry-development-report-2024/official.html` | `raw/ethics/third-section/industry-development-report-2024/official.html.md` | https://www.cicpa.org.cn/xxfb/vv/202603/t20260317_65861.html | 576 | [[concepts/industry-history]] |
| 致敬45年——中国注册会计师制度恢复重建45周年宣传片正式发布 | `raw/ethics/third-section/cpa-system-restoration-45th/official.html` | `raw/ethics/third-section/cpa-system-restoration-45th/official.html.md` | https://www.cicpa.org.cn/xxfb/vv/202601/t20260104_65781.html | 610 | [[concepts/industry-history]] |
| 庆祝中国注册会计师制度恢复重建暨行业改革发展45周年 | `raw/ethics/third-section/industry-reform-development-45th/official.html` | `raw/ethics/third-section/industry-reform-development-45th/official.html.md` | https://www.cicpa.org.cn/xxfb/vv/202512/t20251224_65760.html | 590 | [[concepts/industry-history]] |
| 中国注册会计师协会关于印发《中国注册会计师职业道德守则（2020）》和《中国注册会计师协会非执业会员职业道德守则（2020）》的通知 | `raw/ethics/third-section/ethics-code-2020-notice/official.html` | `raw/ethics/third-section/ethics-code-2020-notice/official.html.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/t20201218_60661.html | 1511 | [[concepts/ethics-code]] |
| 中注协发布《中国注册会计师职业道德守则》全面推进行业诚信建设 | `raw/ethics/third-section/ethics-code-release-2009/official.html` | `raw/ethics/third-section/ethics-code-release-2009/official.html.md` | http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/200911/t20091119_233779.htm | 2385 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则第1号——职业道德基本原则 | `raw/ethics/third-section/ethics-code-2020-no1-basic-principles/official.pdf` | `raw/ethics/third-section/ethics-code-2020-no1-basic-principles/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760737907.pdf | 6756 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则第2号——职业道德概念框架 | `raw/ethics/third-section/ethics-code-2020-no2-conceptual-framework/official.pdf` | `raw/ethics/third-section/ethics-code-2020-no2-conceptual-framework/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760753750.pdf | 6626 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则第3号——提供专业服务的具体要求 | `raw/ethics/third-section/ethics-code-2020-no3-professional-services/official.pdf` | `raw/ethics/third-section/ethics-code-2020-no3-professional-services/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760769913.pdf | 23349 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则第4号——审计和审阅业务对独立性的要求 | `raw/ethics/third-section/ethics-code-2020-no4-audit-review-independence-superseded/official.pdf` | `raw/ethics/third-section/ethics-code-2020-no4-audit-review-independence-superseded/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760795103.pdf | 45034 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则第5号——其他鉴证业务对独立性的要求 | `raw/ethics/third-section/ethics-code-2020-no5-other-assurance-independence/official.pdf` | `raw/ethics/third-section/ethics-code-2020-no5-other-assurance-independence/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760818391.pdf | 19680 | [[concepts/ethics-code]] |
| 中国注册会计师职业道德守则术语表 | `raw/ethics/third-section/ethics-code-2020-glossary/official.pdf` | `raw/ethics/third-section/ethics-code-2020-glossary/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760830251.pdf | 4972 | [[concepts/ethics-code]] |
| 中国注册会计师协会非执业会员职业道德守则 | `raw/ethics/third-section/ethics-code-2020-non-practicing-members/official.pdf` | `raw/ethics/third-section/ethics-code-2020-non-practicing-members/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760835552.pdf | 23704 | [[concepts/ethics-code]] |
| 中国注册会计师协会非执业会员职业道德守则术语表 | `raw/ethics/third-section/ethics-code-2020-non-practicing-members-glossary/official.pdf` | `raw/ethics/third-section/ethics-code-2020-non-practicing-members-glossary/official.pdf.md` | https://cicpa.org.cn/ztzl1/Professional_standards/Professional_ethics/202012/W020210421541760840794.pdf | 1260 | [[concepts/ethics-code]] |
| 关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》的通知 | `raw/ethics/third-section/independence-standard-2024-29/official.html` | `raw/ethics/third-section/independence-standard-2024-29/official.html.md` | http://kjs.mof.gov.cn/zhengcefabu/202501/t20250120_3952051.htm | 698 | [[concepts/independence-standard-1]] |
| 关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》的通知 | `raw/ethics/third-section/independence-standard-2024-29-mof-page/official.html` | `raw/ethics/third-section/independence-standard-2024-29-mof-page/official.html.md` | http://kjs.mof.gov.cn/zhengcefabu/202501/t20250120_3952051.htm | 707 | [[concepts/independence-standard-1]] |
| 财政部印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》 | `raw/ethics/third-section/independence-standard-2024-29-cicpa-page/official.html` | `raw/ethics/third-section/independence-standard-2024-29-cicpa-page/official.html.md` | https://cicpa.org.cn/xxfb/news/202501/t20250120_65225.html | 742 | [[concepts/independence-standard-1]] |
| 中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求 | `raw/ethics/third-section/independence-standard-2024-29-pdf/official.pdf` | `raw/ethics/third-section/independence-standard-2024-29-pdf/official.pdf.md` | https://cicpa.org.cn/xxfb/news/202501/W020250120543364207300.pdf | 23706 | [[concepts/independence-standard-1]] |
| 中注协有关负责人就印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》答记者问 | `raw/ethics/third-section/independence-standard-qa-2025/official.html` | `raw/ethics/third-section/independence-standard-qa-2025/official.html.md` | http://www.mof.gov.cn/zhengwuxinxi/zhengcejiedu/202501/t20250120_3952078.htm | 4958 | [[concepts/independence-standard-1]] |
| 中国注册会计师协会关于印发《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南的通知 | `raw/ethics/third-section/independence-application-guide-2026-page/official.html` | `raw/ethics/third-section/independence-application-guide-2026-page/official.html.md` | https://cicpa.org.cn/xxfb/tzgg/202602/t20260213_65821.html | 925 | [[concepts/independence-standard-1]] |
| 《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南 | `raw/ethics/third-section/independence-application-guide-2026-pdf/official.pdf` | `raw/ethics/third-section/independence-application-guide-2026-pdf/official.pdf.md` | https://cicpa.org.cn/xxfb/tzgg/202602/W020260213545051441275.pdf | 45589 | [[concepts/independence-standard-1]] |
| 中国注册会计师独立性准则第1号应用指南（征求意见稿）通知 | `raw/ethics/third-section/independence-application-guide-exposure-2025/official.html` | `raw/ethics/third-section/independence-application-guide-exposure-2025/official.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202504/t20250430_65411.html | 795 | [[concepts/independence-standard-1]] |
| 中国注册会计师独立性准则第1号应用指南（征求意见稿）通知 | `raw/ethics/third-section/independence-application-guide-exposure-2025-page/official.html` | `raw/ethics/third-section/independence-application-guide-exposure-2025-page/official.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202504/t20250430_65411.html | 800 | [[concepts/independence-standard-1]] |
| 《中国注册会计师独立性准则第1号——财务报表审计和审阅业务对独立性的要求》应用指南（征求意见稿） | `raw/ethics/third-section/independence-application-guide-exposure-2025-pdf/official.pdf` | `raw/ethics/third-section/independence-application-guide-exposure-2025-pdf/official.pdf.md` | https://www.cicpa.org.cn/xxfb/tzgg/202504/W020250430561278327827.pdf | 42711 | [[concepts/independence-standard-1]] |
| Agent第01课_Agent入门概述 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第01课_Agent入门概述.md` | `` |  | 7335 | [[concepts/ai-coding-lectures]] |
| Agent第02课_Skill使用和创建 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第02课_Skill使用和创建.md` | `` |  | 4121 | [[concepts/ai-coding-lectures]] |
| Agent第03课_ExcelAgent使用入门 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第03课_ExcelAgent使用入门.md` | `` |  | 5244 | [[concepts/ai-coding-lectures]] |
| Agent第04课_AI写HTML幻灯片 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第04课_AI写HTML幻灯片.md` | `` |  | 5196 | [[concepts/ai-coding-lectures]] |
| Agent第05课_Agent框架注入了什么内容 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第05课_Agent框架注入了什么内容.md` | `` |  | 6463 | [[concepts/ai-coding-lectures]] |
| Agent第06课_这么多Agent到底怎么选 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第06课_这么多Agent到底怎么选.md` | `` |  | 7331 | [[concepts/ai-coding-lectures]] |
| Agent第07课_Agent接管浏览器-操作小红书 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第07课_Agent接管浏览器-操作小红书.md` | `` |  | 6539 | [[concepts/ai-coding-lectures]] |
| Agent第08课_用Agent搭建第一个本地知识库 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第08课_用Agent搭建第一个本地知识库.md` | `` |  | 6085 | [[concepts/ai-coding-lectures]] |
| Agent第09课_LLM-WIKI打造自己的AI知识库 | `raw/lectures/ai-coding-lectures-2026-07-09/Agent篇/Agent第09课_LLM-WIKI打造自己的AI知识库.md` | `` |  | 10048 | [[concepts/ai-coding-lectures]] |
| Python第00课_课前环境准备 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第00课_课前环境准备.md` | `` |  | 1879 | [[concepts/ai-coding-lectures]] |
| Python第01课_让AI做出第一个PDF合并工具 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第01课_让AI做出第一个PDF合并工具.md` | `` |  | 1220 | [[concepts/ai-coding-lectures]] |
| Python第02课_命令行路径和稳定运行 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第02课_命令行路径和稳定运行.md` | `` |  | 3571 | [[concepts/ai-coding-lectures]] |
| Python第03课_虚拟环境和依赖 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第03课_虚拟环境和依赖.md` | `` |  | 3508 | [[concepts/ai-coding-lectures]] |
| Python第04课_PDF工具GUI界面 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第04课_PDF工具GUI界面.md` | `` |  | 1183 | [[concepts/ai-coding-lectures]] |
| Python第05课_README忽略文件和Git提交 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第05课_README忽略文件和Git提交.md` | `` |  | 1236 | [[concepts/ai-coding-lectures]] |
| Python第06课_JSON配置PDF路径 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第06课_JSON配置PDF路径.md` | `` |  | 1060 | [[concepts/ai-coding-lectures]] |
| Python第07课_从PDF合并到PDF工具箱 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第07课_从PDF合并到PDF工具箱.md` | `` |  | 1248 | [[concepts/ai-coding-lectures]] |
| Python第08课_打包PDF工具箱为EXE | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第08课_打包PDF工具箱为EXE.md` | `` |  | 1380 | [[concepts/ai-coding-lectures]] |
| Python第09课_Claude Code安装 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第09课_Claude Code安装.md` | `` |  | 657 | [[concepts/ai-coding-lectures]] |
| Python第10课_Excel处理的两种模式COM和XML | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第10课_Excel处理的两种模式COM和XML.md` | `` |  | 2808 | [[concepts/ai-coding-lectures]] |
| Python第11课_AI操作Excel原理 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第11课_AI操作Excel原理.md` | `` |  | 2658 | [[concepts/ai-coding-lectures]] |
| Python第12课_从临时脚本到分享EXE解决同事问题 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第12课_从临时脚本到分享EXE解决同事问题.md` | `` |  | 3115 | [[concepts/ai-coding-lectures]] |
| Python第13课_打造带GUI的Excel工具箱 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第13课_打造带GUI的Excel工具箱.md` | `` |  | 2827 | [[concepts/ai-coding-lectures]] |
| Python第14课_Skill是什么以及如何安装和编写 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第14课_Skill是什么以及如何安装和编写.md` | `` |  | 3275 | [[concepts/ai-coding-lectures]] |
| Python第15课_AGENTS项目说明文件 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第15课_AGENTS项目说明文件.md` | `` |  | 4317 | [[concepts/ai-coding-lectures]] |
| Python第16课_Python操作Word的2种方式 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第16课_Python操作Word的2种方式.md` | `` |  | 4039 | [[concepts/ai-coding-lectures]] |
| Python第17课_Word工具箱集成 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第17课_Word工具箱集成.md` | `` |  | 4561 | [[concepts/ai-coding-lectures]] |
| Python第18课_让AI调用第一个中文汇率API | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第18课_让AI调用第一个中文汇率API.md` | `` |  | 6151 | [[concepts/ai-coding-lectures]] |
| Python第19课_用AkShare获取A股报表数据 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第19课_用AkShare获取A股报表数据.md` | `` |  | 2615 | [[concepts/ai-coding-lectures]] |
| Python第20课_Markdown结构化写作和AI提示词 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第20课_Markdown结构化写作和AI提示词.md` | `` |  | 4155 | [[concepts/ai-coding-lectures]] |
| Python第21课_MinerU文档解析API请求 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第21课_MinerU文档解析API请求.md` | `` |  | 2159 | [[concepts/ai-coding-lectures]] |
| Python第22课_本地桌面路线React和pywebview | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第22课_本地桌面路线React和pywebview.md` | `` |  | 3150 | [[concepts/ai-coding-lectures]] |
| Python第23课_Web服务路线FastAPI和前端 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第23课_Web服务路线FastAPI和前端.md` | `` |  | 2676 | [[concepts/ai-coding-lectures]] |
| Python第24课_Python篇阶段回顾从脚本到产品化 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第24课_Python篇阶段回顾从脚本到产品化.md` | `` |  | 3446 | [[concepts/ai-coding-lectures]] |
| Python第25课_Web小案例PDF转Markdown网站 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第25课_Web小案例PDF转Markdown网站.md` | `` |  | 3647 | [[concepts/ai-coding-lectures]] |
| Python第26课_合同字段AI抽取助手 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第26课_合同字段AI抽取助手.md` | `` |  | 6130 | [[concepts/ai-coding-lectures]] |
| Python第27课_Agent工具调用和固定代码边界判断 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第27课_Agent工具调用和固定代码边界判断.md` | `` |  | 6078 | [[concepts/ai-coding-lectures]] |
| Python第28课_CPAHelper Agent的工具设计 | `raw/lectures/ai-coding-lectures-2026-07-09/Python篇/Python第28课_CPAHelper Agent的工具设计.md` | `` |  | 3739 | [[concepts/ai-coding-lectures]] |
| VBA第01课_先导课_VBA和Python怎么选 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第01课_先导课_VBA和Python怎么选.md` | `` |  | 3194 | [[concepts/ai-coding-lectures]] |
| VBA第02课_初识VBA和加载宏按钮运行原理 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第02课_初识VBA和加载宏按钮运行原理.md` | `` |  | 2389 | [[concepts/ai-coding-lectures]] |
| VBA第03课_两种方式运行AI写的VBA代码 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第03课_两种方式运行AI写的VBA代码.md` | `` |  | 2911 | [[concepts/ai-coding-lectures]] |
| VBA第04课_Excel功能区设计器概览 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第04课_Excel功能区设计器概览.md` | `` |  | 2389 | [[concepts/ai-coding-lectures]] |
| VBA第05课_功能区按钮的实现原理 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第05课_功能区按钮的实现原理.md` | `` |  | 2881 | [[concepts/ai-coding-lectures]] |
| VBA第06课_AI完成功能区按钮的实现 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第06课_AI完成功能区按钮的实现.md` | `` |  | 3936 | [[concepts/ai-coding-lectures]] |
| VBA第07课_把按钮收进菜单 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第07课_把按钮收进菜单.md` | `` |  | 3915 | [[concepts/ai-coding-lectures]] |
| VBA第08课_用下拉框保存状态 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第08课_用下拉框保存状态.md` | `` |  | 4973 | [[concepts/ai-coding-lectures]] |
| VBA第09课_输入框和复选框增加交互逻辑 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第09课_输入框和复选框增加交互逻辑.md` | `` |  | 4009 | [[concepts/ai-coding-lectures]] |
| VBA第10课_让加载项对所有工作簿生效 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第10课_让加载项对所有工作簿生效.md` | `` |  | 2917 | [[concepts/ai-coding-lectures]] |
| VBA第11课_功能收进VBA窗体 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第11课_功能收进VBA窗体.md` | `` |  | 4088 | [[concepts/ai-coding-lectures]] |
| VBA第12课_VBA工程保护和加密边界 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第12课_VBA工程保护和加密边界.md` | `` |  | 3358 | [[concepts/ai-coding-lectures]] |
| VBA第13课_加载项实战1_套ROUND提取字符清除非公式 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第13课_加载项实战1_套ROUND提取字符清除非公式.md` | `` |  | 5009 | [[concepts/ai-coding-lectures]] |
| VBA第14课_加载项实战2_引用转换和批量更换链接 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第14课_加载项实战2_引用转换和批量更换链接.md` | `` |  | 5251 | [[concepts/ai-coding-lectures]] |
| VBA第15课_加载项实战3_生成目录和另存Sheet | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第15课_加载项实战3_生成目录和另存Sheet.md` | `` |  | 4167 | [[concepts/ai-coding-lectures]] |
| VBA第16课_加载项实战4_断链删表和显隐Sheet | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第16课_加载项实战4_断链删表和显隐Sheet.md` | `` |  | 4926 | [[concepts/ai-coding-lectures]] |
| VBA第17课_加载项实战5_重命名和拆分工作簿 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第17课_加载项实战5_重命名和拆分工作簿.md` | `` |  | 2439 | [[concepts/ai-coding-lectures]] |
| VBA第18课_加载项实战6_一键格式 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第18课_加载项实战6_一键格式.md` | `` |  | 2798 | [[concepts/ai-coding-lectures]] |
| VBA第19课_加载项实战7_拆分按钮优化 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第19课_加载项实战7_拆分按钮优化.md` | `` |  | 2149 | [[concepts/ai-coding-lectures]] |
| VBA第20课_加载项实战8_批量重命名和打包发布 | `raw/lectures/ai-coding-lectures-2026-07-09/VBA插件篇/VBA第20课_加载项实战8_批量重命名和打包发布.md` | `` |  | 3193 | [[concepts/ai-coding-lectures]] |
| 练习题库（试卷一）答案解析 | `raw/outlines/practice-question-bank-2026-07-13/practice-question-bank-paper-1-answer-explanations/official.pdf` | `raw/outlines/practice-question-bank-2026-07-13/practice-question-bank-paper-1-answer-explanations/official.pdf.md` |  | 9848 | [[sources/practice-question-bank-paper-1-answer-explanations-2026-07-13]] |
| 监管规则适用指引——发行类第9号：研发人员及研发投入 | `raw/policies/issuance-guidance/issuance-class-09-rd-staff-investment/official.pdf` | `raw/policies/issuance-guidance/issuance-class-09-rd-staff-investment/official.pdf.md` | https://www.csrc.gov.cn/csrc/c101802/c7445462/content.shtml | 4092 | [[concepts/securities-issuance-rd-staff-investment]] |
| 关于进一步加强财会监督工作的意见 | `raw/policies/second-section/caihui-supervision-2023-4/official.html` | `raw/policies/second-section/caihui-supervision-2023-4/official.html.md` | https://www.gov.cn/zhengce/2023-02/15/content_5741628.htm | 367 | [[concepts/policy-caihui-supervision]] |
| 关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见 | `raw/policies/second-section/audit-order-2021-30/official.html` | `raw/policies/second-section/audit-order-2021-30/official.html.md` | https://www.gov.cn/zhengce/content/2021-08/23/content_5632714.htm | 396 | [[concepts/policy-audit-order]] |
| 注册会计师全国统一考试办法 | `raw/policies/second-section/cpa-exam-2024-115/official.html` | `raw/policies/second-section/cpa-exam-2024-115/official.html.md` | https://www.gov.cn/gongbao/2024/issue_11286/202404/content_6945588.html | 365 | [[concepts/policy-cpa-exam]] |
| 注册会计师注册办法 | `raw/policies/second-section/cpa-registration-2019-99/official.html` | `raw/policies/second-section/cpa-registration-2019-99/official.html.md` | https://www.mof.gov.cn/gkml/caizhengwengao/wg201901/wg201912/202005/t20200522_3518260.htm | 4275 | [[concepts/policy-cpa-registration]] |
| 会计师事务所执业许可和监督管理办法 | `raw/policies/second-section/firm-license-supervision-2019-97/official.html` | `raw/policies/second-section/firm-license-supervision-2019-97/official.html.md` | https://www.gov.cn/gongbao/content/2019/content_5392297.htm | 375 | [[concepts/policy-firm-license-supervision]] |
| 注册会计师行业诚信建设纲要 | `raw/policies/second-section/integrity-2023-5/official.html` | `raw/policies/second-section/integrity-2023-5/official.html.md` | https://www.gov.cn/zhengce/zhengceku/2023-04/02/content_5749779.htm | 361 | [[concepts/policy-integrity]] |
| 会计师事务所监督检查办法 | `raw/policies/second-section/firm-inspection-2022-23/official.html` | `raw/policies/second-section/firm-inspection-2022-23/official.html.md` | https://www.gov.cn/zhengce/zhengceku/2022-05/16/content_5690682.htm | 367 | [[concepts/policy-firm-inspection]] |
| 首届全国注册会计师行业胜任能力青年挑战赛考察知识清单文件来源汇总 | `raw/sources/challenge-knowledge-source-summary-2026-07-13/file-source-summary/official.html` | `raw/sources/challenge-knowledge-source-summary-2026-07-13/file-source-summary/official.html.md` |  | 2793 | [[sources/challenge-knowledge-source-summary-verification-2026-07-13]] |

## 使用说明

- `missing-local-file`：manifest 指向的原件不存在，应恢复官方 PDF/HTML/DOCX 或补来源说明。
- `missing-derived-markdown`：原件存在但缺少 Markdown 派生件，检索和加工体验会下降。
- `ocr-pending`：PDF 已归档但文本为空，适合后续 OCR 或手工补正文。
- `verify-official-url`：已有来源但官方具体原文页仍需复核。
- `missing-official-url`：manifest 中没有 URL，应补官方来源或本地来源说明。
- `not-in-text-cache`：raw 文件还没有进入 `cache/text/`，运行 `tools/kb.py cache build`。

_生成路径：`wiki/concepts/source-status-dashboard.md`_
