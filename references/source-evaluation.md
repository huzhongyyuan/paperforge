# 开源科研与论文技能精选

整理：huzhongyuan。核对日期：**2026-11-06（Asia/Shanghai）**。

这份清单以 **CCF-A 研究与写作为优先方向**，Nature/Science 作为期刊补充。Orchestra、Master-cai、ARIS 和 K-Dense 的选定方法已接入 [功能模块](upstream-integration.md)，其余项目供按需选择。Star 徽章打开页面时自动加载**整个仓库**的关注数；徽章服务与 GitHub 图片缓存可能造成延迟，不是逐秒实时计数。来源 JSON 中的数值保留为核对日期的快照。分组按用途，不是录用率或质量排名；“CCF-A/顶会”“Nature/Science”是使用方向，不代表官方认证，具体会议等级和期刊要求另查当期官方目录／指南。

## 先选用途

| 你要做什么 | 优先参考 | 与 PaperForge 的关系 |
|---|---|---|
| 把 ML/CV 结果写成顶会论文 | Orchestra、Master-cai | 补充章节组织、论证和研究构思；主工作流仍用 PaperForge |
| 面向 Nature 类综合读者解释科学发现 | K-Dense 的 scientific-writing、venue-templates | 补充跨领域叙事、文章类型、Methods 与附加材料安排 |
| 系统文献整理、查 DOI 与 BibTeX | K-Dense 的 literature-review、citation-management | 补充检索记录、筛选和书目验证 |
| 核对论文数字、证据与审稿意见 | ARIS 的 paper-claim-audit、K-Dense 的 peer-review | 补充独立核验思路和审阅工具 |
| 从真实数据生成统计图／多面板图 | K-Dense scientific-visualization、Orchestra academic-plotting | 补充 Matplotlib/Seaborn 等数据绘图流程 |
| 生成概念示意图或重建可编辑 SVG | PaperBanana、AutoFigure-Edit | 可选外部制作工具；与 PaperForge 的结构化 SVG/PPTX 路线配合 |

## 开源技能与工作流

| 项目 | Star（自动更新） | 最相关入口 | 适合做什么 | 许可与依赖 |
|---|---:|---|---|---|
| [Orchestra AI Research SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | [![GitHub stars](https://img.shields.io/github/stars/Orchestra-Research/AI-Research-SKILLs?style=flat&label=stars&cacheSeconds=300)](https://github.com/Orchestra-Research/AI-Research-SKILLs/stargazers) | [ml-paper-writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/ml-paper-writing/SKILL.md)、[academic-plotting](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/academic-plotting/SKILL.md) | ML 论文、研究构思、数据图；覆盖多种 ML/AI 会议写作场景 | [MIT](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/LICENSE)；架构图生成分支使用 Gemini，数据图使用绘图库 |
| [Research Paper Writing Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | [![GitHub stars](https://img.shields.io/github/stars/Master-cai/Research-Paper-Writing-Skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/Master-cai/Research-Paper-Writing-Skills/stargazers) | [research-paper-writing](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/SKILL.md) | ML/CV/NLP 章节、段落衔接与主张—证据一致性 | [MIT](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/LICENSE)；README 说明写作知识主要整理自彭思达公开笔记，复用需保留归属 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | [![GitHub stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&label=stars&cacheSeconds=300)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/stargazers) | [paper-writing](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/2901234ad2954cd2388ced8d3aed2ed9de42803a/skills/paper-writing/SKILL.md)、[paper-claim-audit](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/2901234ad2954cd2388ced8d3aed2ed9de42803a/skills/paper-claim-audit/SKILL.md) | 研究到论文的流程，以及原始结果—论文主张检查 | [MIT](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/2901234ad2954cd2388ced8d3aed2ed9de42803a/LICENSE)；多模型审阅／自动循环需单独配置环境和预算 |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/K-Dense-AI/scientific-agent-skills/stargazers) | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/scientific-writing/SKILL.md)、[venue-templates](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/venue-templates/SKILL.md) | 科学写作、期刊准备、文献与审稿；Nature 方向优先看这里 | [MIT](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/LICENSE.md)；所选写作/审稿本地工具不需模型 API，其他技能各有依赖 |
| [K-Dense Scientific Writer](https://github.com/K-Dense-AI/claude-scientific-writer) | [![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-writer?style=flat&label=stars&cacheSeconds=300)](https://github.com/K-Dense-AI/claude-scientific-writer/stargazers) | [scientific-writing](https://github.com/K-Dense-AI/claude-scientific-writer/blob/529b9f73ab4b48925027145800d7b49e96ccfd3c/.claude/skills/scientific-writing/SKILL.md)、[venue-templates](https://github.com/K-Dense-AI/claude-scientific-writer/blob/529b9f73ab4b48925027145800d7b49e96ccfd3c/.claude/skills/venue-templates/SKILL.md) | 集中的科学写作与期刊格式流程，另提供完整写作应用 | [根 MIT](https://github.com/K-Dense-AI/claude-scientific-writer/blob/529b9f73ab4b48925027145800d7b49e96ccfd3c/LICENSE)，所选写作/模板技能为 MIT；部分打包文档技能另有许可。完整应用有外部 API 依赖 |

K-Dense 两个仓库有重叠资源，可按任务选一套。上表不把大库 star 数说成其中单个 skill 的独立关注数。

## Nature / Science 方向看哪些文件

K-Dense 大库中已核对的具体入口：

| 入口 | 用途 |
|---|---|
| [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/scientific-writing/SKILL.md) | 章节撰写、证据来源、报告要求、图表与声明一致性 |
| [Nature and Science writing reference](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/venue-templates/references/nature_science_style.md) | 面向跨学科读者解释问题与发现，区分 Nature、Science 及其他刊物；具体规则仍核对目标期刊和文章类型 |
| [venue-templates](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/venue-templates/SKILL.md) | 查官方模板、当前格式规则，编译／检查投稿稿件 |
| [scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/scientific-visualization/SKILL.md) | 真实数据、多面板图、不确定性、可访问配色与出版导出 |
| [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/peer-review/SKILL.md) | 方法、统计、可复现性、图表和引用的证据审阅 |
| [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/literature-review/SKILL.md)、[citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/citation-management/SKILL.md) | 可追溯检索、文献筛选、DOI／书目验证 |

这些是社区维护的通用科研技能。PaperForge 当前内置的实证案例库主要是 ML/CV；此清单扩展发现入口，不把 Nature 模板描述为已完成期刊合规验收。

## 可配合使用的开源工具

| 项目 | Star（自动更新） | 类型与用途 | 核对到的边界 |
|---|---:|---|---|
| [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | [![GitHub stars](https://img.shields.io/github/stars/dwzhu-pku/PaperBanana?style=flat&label=stars&cacheSeconds=300)](https://github.com/dwzhu-pku/PaperBanana/stargazers) | 学术示意图生成工具，另有 [skill 入口](https://github.com/dwzhu-pku/PaperBanana/blob/dafc2d41c10395c8bc37faad26836070fef0add8/skill/SKILL.md) | [根 Apache-2.0](https://github.com/dwzhu-pku/PaperBanana/blob/dafc2d41c10395c8bc37faad26836070fef0add8/LICENSE)，skill 头部另标 MIT-0；需模型/图像 API。该版本统计图代码仍列 README TODO，不用它替代真实数据绘图 |
| [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) | [![GitHub stars](https://img.shields.io/github/stars/ResearAI/AutoFigure-Edit?style=flat&label=stars&cacheSeconds=300)](https://github.com/ResearAI/AutoFigure-Edit/stargazers) | 方法文字或栅格图 → 可编辑 SVG；独立应用 | [MIT](https://github.com/ResearAI/AutoFigure-Edit/blob/16f3749e9d512bdf7b7b55c162307bc289750b7a/LICENSE)；需模型/API 与图像处理环境，标签和拓扑仍需检查 |
| [Paper2Any 历史开源实现](https://github.com/OpenDCAI/Paper2Any) | [![GitHub stars](https://img.shields.io/github/stars/OpenDCAI/Paper2Any?style=flat&label=stars&cacheSeconds=300)](https://github.com/OpenDCAI/Paper2Any/stargazers) | 图表、PPT 与文档转换工作台；独立应用 | [Apache-2.0](https://github.com/OpenDCAI/Paper2Any/blob/b538531e25798d9b9d41afd5fa93c9222949b5a5/LICENSE) 适用于公开历史代码；当前 Studio/Nexus 和桌面商业实现未完整开源，新产品功能不再同步到该仓库 |

## 高关注但需按文件区分许可的参考

[Anthropic Skills](https://github.com/anthropics/skills) 的 Star 为 [![GitHub stars](https://img.shields.io/github/stars/anthropics/skills?style=flat&label=stars&cacheSeconds=300)](https://github.com/anthropics/skills/stargazers)，适合了解通用技能和文档生产组织。本次核对的 [PPTX](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/pptx/SKILL.md) 明确声明 Proprietary，[PPTX 许可](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/pptx/LICENSE.txt) 与 [DOCX 许可](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/docx/LICENSE.txt) 有单独使用条款，因此未将这些文档技能列为可直接复制的开源资源。

## 如何与 PaperForge 一起使用

先用 `$paperforge` 完成当前研究材料的写作、图表和审稿，再按缺口选择上面的具体模块。清单提供来源、用途、版本和许可摘要；安装外部技能或把代码合入项目时，检查完整许可、依赖和当前工作流兼容性。外部流程中的模型、自动循环与资源默认值不会因被列入清单而成为当前任务设置。

本次整合了选定写作、文献、核验和数据图指导，具体内容见 [整合记录](upstream-integration.md)。外部项目代码和运行环境未批量导入；来源已核对 GitHub 元数据、固定版本 README、选定技能／参考文件和许可文件。详细提交、star 数和文件哈希见 [机器可读来源记录](upstream-catalog.json)。如后续实测，另记录版本、输入、环境、输出与失败。

较早的比较保留在 [2026-08-04 历史记录](upstream-landscape-20260804.md)，其中 star 和项目状态属于当时快照；当前推荐以本页为准。
