# PaperForge

一个按功能组织的研究与写作技能：研究设计、论文写作、可编辑图表、排版、科学审稿和直接表达。只安装一个 `paperforge`，按当前任务读取相关资源。

## 这是什么，什么时候用

PaperForge 是给 AI 助手使用的科研与写作工作包，包含工作步骤、参考资料和可执行工具。你提供草稿、代码、方法说明或实验结果，它帮助助手按任务完成实际修改和产物。技能这种形式由说明、资源和可选脚本组成，见 [OpenAI 官方说明](https://developers.openai.com/codex/skills)。

| 你手上有什么 | 可以让 PaperForge 做什么 |
|---|---|
| 一个 idea 或问题观察 | 整理研究问题、待验证假设和最小实验方案 |
| 方法代码、实验记录 | 组织方法和实验叙事，建立主张与证据对应关系 |
| 论文初稿 | 修改摘要、引言、方法和实验，统一术语与图文 |
| 方法说明或真实实验数据 | 画可编辑框架图、数据图，写 caption |
| LaTeX 稿件 | 调整双栏、图表和分页，并在环境允许时编译检查 |
| 审稿意见 | 检查证据缺口，修改论文并起草 rebuttal |
| 冗长的技术说明、周报或交付汇报 | 精简表达，保留事实、验证结果和未完成项 |

已有案例主要覆盖 ML/CV 研究。生成科学结论需要你的实际证据；idea 阶段输出的是假设和计划。

## 功能

| 功能 | 用途 |
|---|---|
| 研究与实验 | 问题、可检验假设、模块接口、最小对照和证据链 |
| 写作与修改 | 标题、摘要、引言、方法、实验、局限、附录与逐段改稿 |
| 图表与制作 | 方法图、动机图、真实结果拼版、caption、可编辑 SVG／原生 PPTX 和程序化框架图 |
| 论文排版 | 页数预算、双栏、浮动体、分页和编译检查 |
| 审稿与 rebuttal | 新颖性、协议、对比公平性、消融、归因及主张范围 |
| 直接表达 | 普通回答、技术说明和交付汇报去冗余；论文先审科学含义，再精简表达 |
| 语料与案例 | 按技术问题选择相关案例，查询有日期和阅读深度记录的 ML/CV 资源 |

## 安装

在 Codex 中请求：

> 从 https://github.com/huzhongyyuan/paperforge 安装 paperforge 路径。已有同名版本时先备份再更新。

或使用 Codex 自带安装器（全新安装；已有同名技能时拒绝覆盖）：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo huzhongyyuan/paperforge --path paperforge
```

技能及所需资源均在 [paperforge/](paperforge/SKILL.md)，不需要安装其他入口，也不要只下载单个 Markdown。

## 使用

```text
使用 $paperforge，结合我的代码、方法与实验，实际修改 Introduction，
让问题、机制、模块和证据对应；缺失结果明确指出。
```

```text
使用 $paperforge，根据已确认的方法画一张框架图，
交付可编辑源、预览和 caption，并核对训练状态与计算路径。
```

```text
使用 $paperforge，审阅并修改这份论文，核对主张、实验协议和消融，
再精简重复辩解，保留必要条件与真实不确定性。
```

```text
使用 $paperforge，把这份技术说明或交付汇报改得直接清楚，
保留事实、失败、未完成项与实际验证程度。
```

## 精选开源科研技能

[按功能浏览推荐清单](paperforge/references/source-evaluation.md)：ML/CV 顶会写作、Nature/Science 类科学写作、文献与引用、科学审稿、数据可视化和可编辑图表。已核对 9 个相关项目，保留具体 skill 链接、star 快照、固定版本和许可信息，并区分开源技能、独立工具及有单独许可的参考。

优先查看 **K-Dense Scientific Agent Skills**（综合科研与期刊写作）、**Orchestra**（ML 研究和论文）、**Master-cai**（章节写作）及 **ARIS**（研究流程与主张核对）。清单是可按需选用的资源导航；当前安装仍是一个 PaperForge 入口。

## 资源与工具

入口按功能路由到 [写作](paperforge/references/integrated-writing.md)、[图表](paperforge/references/integrated-figures.md)、[排版](paperforge/references/manuscript-layout.md)、[审稿](paperforge/references/review-gates.md)、[通用表达](paperforge/references/direct-writing.md) 和 [论文表达](paperforge/references/anti-defensive-writing.md)。案例按任务、失效原因、计算成本和证据类型匹配，见 [案例选择](paperforge/references/case-library.md)。

Python 标准库可运行 SVG 模板和结构化绘图及术语／形式检查。原生 PPTX 需要 Node.js 与 `pptxgenjs`；组件框架绘图需要 Pillow、Matplotlib、CairoSVG 和系统 Cairo，见 [工具指南](paperforge/modules/share-tools/references/guide.md)。HTML／主 SVG 保留文字，静态 PDF 使用字体轮廓。数值图需要真实数据，定性图需要真实结果素材。

## 覆盖与来源

会议库包含 2026-08-04 快照的 25,421 条元数据与 55 篇全文结构样本；增补 ICLR 2025 的 3,705 条元数据、12 篇有范围研读及 17 处图示检查，以及 CVPR 2024–2026 的 9,629 条元数据、9,038 篇自动提取、18 篇定向研读及 15 处图表检查。案例库保留 24 篇方法论文与 1 篇综述的核心研读、33 篇合作作品结构概览、25 张有归属图摘录和 4 张原创 SVG 模板。

不同库有重叠；元数据、自动提取和定向阅读不能相加为全文精读总数。来源、日期、固定版本、失败和阅读深度见 [覆盖记录](paperforge/references/merged-evidence.md)。本次统一未刷新语料或复现实验。工具和格式验证不代表科学结论或写作效果验收。

通用表达原则整合自用户指定的 [anti-defensive-writing](https://github.com/huzhongyyuan/anti-defensive-writing)，固定版本与适配说明见 [直接表达](paperforge/references/direct-writing.md)。

## 许可

保留原有 [MIT 许可](paperforge/LICENSE.txt) 和第三方归属。论文、图摘录、分享包及新增表达原则依各自来源与许可处理，详见 [来源说明](THIRD_PARTY_NOTICES.md)。仓库不附完整论文 PDF、私人会话、实验日志或原作者编辑工程。
