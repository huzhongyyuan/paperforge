# 开源指导的功能整合

整理：huzhongyuan；日期：2026-11-06。主线为 CCF-A 研究与论文写作，Nature/Science 按需作为期刊补充。

这些内容已写入统一技能的功能参考，而不仅是外部链接。保留各来源的固定版本和许可；star 用于资源发现，不作为科学可靠性或写作效果的证明。

## 已接入的功能

| 功能 | 本地模块 | 主要来源 |
|---|---|---|
| CCF-A 论证、实验叙事与数字核对 | [会议论文主线](top-conference-writing.md) | Orchestra、Master-cai、ARIS |
| Nature/Science 期刊写作补充 | [期刊写作](journal-writing.md) | K-Dense |
| 相关工作、文献整理与引用核验 | [文献与引用](literature-and-citations.md) | K-Dense、Orchestra |
| 真实数据图、统计单位与多面板导出 | [科学数据图](scientific-data-figures.md) | K-Dense 与已有图表流程 |

## 固定版本、来源文件与许可

### Orchestra-Research/AI-Research-SKILLs

版本：`773a52944ba4747a18bd4ae9ade53fff041adcbc`；[保留的 MIT 许可](licenses/orchestra-MIT.txt)。

来源：[20-ml-paper-writing/ml-paper-writing/SKILL.md](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/ml-paper-writing/SKILL.md)。

采用：研究仓库到论点、章节组织、实验问题及书目信息核验。

适配：将固定句数/页码/贡献数量视为示例；不导入统一录用断言、未核实统计或外部服务安装要求。

### Master-cai/Research-Paper-Writing-Skills

版本：`77e7c2c1ba06f7d71844873147665437a03aac1b`；[保留的 MIT 许可](licenses/research-paper-writing-MIT.txt)。

来源：[research-paper-writing/SKILL.md](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/SKILL.md)。

采用：反向提纲、段落职责、术语稳定与主张—证据一致性。

适配：按请求规模执行，不强制每次附整套提纲、角色标签或审稿问卷。保留其公开笔记来源归属。

原项目 README 说明其写作知识主要来自彭思达的[公开研究笔记](https://github.com/pengsida/learning_research)。本次依据 Master-cai 的技能整理保留这层归属，不声称独立核验了所有原始笔记。

### wanshuiyin/Auto-claude-code-research-in-sleep

版本：`2901234ad2954cd2388ced8d3aed2ed9de42803a`；[保留的 MIT 许可](licenses/aris-MIT.txt)。

来源：[skills/paper-claim-audit/SKILL.md](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/2901234ad2954cd2388ced8d3aed2ed9de42803a/skills/paper-claim-audit/SKILL.md)。

采用：直接从原始结果核对数值、配置、聚合、舍入和主张范围。

适配：保留核验方法；独立审阅沿用既有授权，不移入新Agent、模型固定值、自动循环或生产调度配置。

### K-Dense-AI/scientific-agent-skills

版本：`a25cf9ec00e2745d03f8704acf6f6919694ccd9a`；[保留的 MIT 许可](licenses/k-dense-MIT.txt)。

来源：[skills/scientific-writing/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/scientific-writing/SKILL.md)、[skills/venue-templates/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/venue-templates/SKILL.md)、[skills/venue-templates/references/nature_science_style.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/venue-templates/references/nature_science_style.md)、[skills/peer-review/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/peer-review/SKILL.md)、[skills/literature-review/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/literature-review/SKILL.md)、[skills/citation-management/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/citation-management/SKILL.md)、[skills/scientific-visualization/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/scientific-visualization/SKILL.md)。

采用：期刊与文章类型核对、研究设计/统计、可追溯文献、引用支持与真实数据图。

适配：期刊路线按请求加载，精确规则需读当前官方文件；复用现有记录，不强加独立账本或无关操作流程。

## 使用与验证范围

继续使用 `$paperforge`。普通论文任务先进入 CCF-A 主线，文献和数据图按需调用，指定期刊时读取期刊补充。保持单一技能入口，已有研究事实、图表工具、审稿与反防御写作共同使用。

本次整合的是指导内容；没有复制上游执行脚本、安装整套外部运行环境或更换模型。技能格式、引用路径、来源与许可可作结构核验；这些检查不等于第三方运行测试、写作效果评测或投稿质量验收。文件哈希和映射见 [机器记录](upstream-integration.json)，完整资源导航见 [精选目录](source-evaluation.md)。
