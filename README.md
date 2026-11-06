# PaperForge

以 **CCF-A 研究与论文写作为主线**的技能：研究设计、论文写作、文献核验、可编辑图表、排版、科学审稿和直接表达。Nature/Science 作为按需加载的期刊补充。只安装一个 `paperforge`。

## 精选开源科研技能

按 **CCF-A 优先**整理。Star 徽章自动更新，徽章服务及 GitHub 图片缓存可能造成延迟；来源记录仍保留核对日期与固定版本。

| 项目 | Star | 用途 | 与 PaperForge 的关系 |
|---|---|---|---|
| [Orchestra](https://github.com/Orchestra-Research/AI-Research-SKILLs) | [![GitHub stars](https://img.shields.io/github/stars/Orchestra-Research/AI-Research-SKILLs?style=flat&label=stars&cacheSeconds=300)](https://github.com/Orchestra-Research/AI-Research-SKILLs/stargazers) | ML 研究、方法论证与顶会论文 | 写作／引用方法已整合 |
| [Research Paper Writing](https://github.com/Master-cai/Research-Paper-Writing-Skills) | [![GitHub stars](https://img.shields.io/github/stars/Master-cai/Research-Paper-Writing-Skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/Master-cai/Research-Paper-Writing-Skills/stargazers) | 章节写作、反向提纲与段落衔接 | 写作方法已整合 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | [![GitHub stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&label=stars&cacheSeconds=300)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/stargazers) | 研究流程、论文主张与原始结果核对 | 核验方法已整合 |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) | 文献、数据图、审稿与 Nature/Science 补充 | 选定指导已整合 |
| [Scientific Writer](https://github.com/K-Dense-AI/claude-scientific-writer) | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-writer?style=flat&label=stars&cacheSeconds=300)](https://github.com/K-Dense-AI/claude-scientific-writer/stargazers) | 科学写作与期刊格式工作流 | 可选补充，与 K-Dense 大库有重叠 |
| [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | [![GitHub stars](https://img.shields.io/github/stars/dwzhu-pku/PaperBanana?style=flat&label=stars&cacheSeconds=300)](https://github.com/dwzhu-pku/PaperBanana/stargazers) | 学术概念示意图生成 | 可选工具／skill，有模型 API 依赖 |
| [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) | [![GitHub stars](https://img.shields.io/github/stars/ResearAI/AutoFigure-Edit?style=flat&label=stars&cacheSeconds=300)](https://github.com/ResearAI/AutoFigure-Edit/stargazers) | 方法文字或已有图转可编辑 SVG | 可选独立工具 |
| [Paper2Any](https://github.com/OpenDCAI/Paper2Any) | [![GitHub stars](https://img.shields.io/github/stars/OpenDCAI/Paper2Any?style=flat&label=stars&cacheSeconds=300)](https://github.com/OpenDCAI/Paper2Any/stargazers) | 论文图表、PPT 与文档转换 | 历史开源实现；当前商业产品另计 |

另有公开参考 [Anthropic Skills](https://github.com/anthropics/skills) [![GitHub stars](https://img.shields.io/github/stars/anthropics/skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/anthropics/skills/stargazers)；其 PPTX/DOCX 技能有专有许可，未作为可复制的开源模块收录。

[查看具体 skill、版本与许可](references/source-evaluation.md) · [查看已整合的方法与来源](references/upstream-integration.md)

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

> 从 https://github.com/huzhongyyuan/paperforge 从仓库根目录安装为 paperforge。已有同名版本时先备份再更新。

或使用 Codex 自带安装器（全新安装；已有同名技能时拒绝覆盖）：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo huzhongyyuan/paperforge --path . --name paperforge
```

仓库根目录就是技能目录，入口为 [SKILL.md](SKILL.md)。安装时保留同目录的 `references/`、`modules/`、`scripts/` 和 `assets/`。

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

## 已整合的高关注开源指导

| 功能 | 已接入内容 | 来源 |
|---|---|---|
| **CCF-A 主线** | 贡献组织、反向提纲、方法与实验论证、原始结果到论文数字核对 | Orchestra、Master-cai、ARIS |
| 文献与引用 | 相关工作综合、检索记录、文献身份与引用支持核验 | K-Dense、Orchestra |
| 科学数据图 | 统计单位、误差线、缺失数据、多面板和可复现导出 | K-Dense |
| 期刊补充 | Nature/Science 读者、文章类型、结果叙事与格式核对 | K-Dense |

这些指导已接入 [统一技能](SKILL.md)，通过一个入口按需使用。[整合说明与许可](references/upstream-integration.md) 记录采用的内容、固定版本及适配方式。

```text
使用 $paperforge，按 CCF-A 流程检查这份论文的贡献、方法论证和实验，
核对原始结果，再修改引言和 rebuttal。
```

## 资源与工具

入口按功能路由到 [写作](references/integrated-writing.md)、[图表](references/integrated-figures.md)、[排版](references/manuscript-layout.md)、[审稿](references/review-gates.md)、[通用表达](references/direct-writing.md) 和 [论文表达](references/anti-defensive-writing.md)。案例按任务、失效原因、计算成本和证据类型匹配，见 [案例选择](references/case-library.md)。

Python 标准库可运行 SVG 模板和结构化绘图及术语／形式检查。原生 PPTX 需要 Node.js 与 `pptxgenjs`；组件框架绘图需要 Pillow、Matplotlib、CairoSVG 和系统 Cairo，见 [工具指南](modules/share-tools/references/guide.md)。HTML／主 SVG 保留文字，静态 PDF 使用字体轮廓。数值图需要真实数据，定性图需要真实结果素材。

## 覆盖与来源

会议库包含 2026-08-04 快照的 25,421 条元数据与 55 篇全文结构样本；增补 ICLR 2025 的 3,705 条元数据、12 篇有范围研读及 17 处图示检查，以及 CVPR 2024–2026 的 9,629 条元数据、9,038 篇自动提取、18 篇定向研读及 15 处图表检查。案例库保留 24 篇方法论文与 1 篇综述的核心研读、33 篇合作作品结构概览、25 张有归属图摘录和 4 张原创 SVG 模板。

不同库有重叠；元数据、自动提取和定向阅读不能相加为全文精读总数。来源、日期、固定版本、失败和阅读深度见 [覆盖记录](references/merged-evidence.md)。本次统一未刷新语料或复现实验。工具和格式验证不代表科学结论或写作效果验收。

通用表达原则整合自用户指定的 [anti-defensive-writing](https://github.com/huzhongyyuan/anti-defensive-writing)，固定版本与适配说明见 [直接表达](references/direct-writing.md)。

## 许可

保留原有 [MIT 许可](LICENSE.txt) 和第三方归属。论文、图摘录、分享包及新增表达原则依各自来源与许可处理，详见 [来源说明](THIRD_PARTY_NOTICES.md)。仓库不附完整论文 PDF、私人会话、实验日志或原作者编辑工程。
