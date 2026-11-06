# Mayue Paper Skill

将 Yue Ma（马跃）一作／共一论文的写作与图表案例，接入 CCF-A 研究、实验、改稿和排版流程的 Codex 技能包。

这是独立整理的学习工具，与 Yue Ma 及其合作者无隶属或官方背书关系。学习公开论文中的论证与视觉组织，用于撰写用户自己的原创研究。

## 能做什么

- **研究与 idea：** 明确问题、机制假设、模块接口和最小对照实验。
- **逐节写作与改稿：** 标题、摘要、引言、相关工作、方法各模块、训练／推理、实验、局限与附录。
- **写图与画图：** 动机图、框架图、模块放大、时间轴、真实结果拼版、数值与消融图、caption。
- **可编辑制作：** SVG 模板、结构化 JSON→SVG／原生 PowerPoint，以及程序化组件框架图的 HTML／SVG／PDF／PNG 导出。
- **正文与图交接：** 可复用现有记录的共享事实表、模块全名／别名检查，以及只作提醒的章节形式诊断。
- **整篇论文：** 页数预算、双栏排版、浮动体、证据检查、rebuttal 与报告准备。

## 安装

本仓库包含四个并列技能目录。`mayue-paper-skill/SKILL.md` 是入口，必须同时安装 `craft-ccfa-paper`；不要只下载单个 Markdown 文件。

在 Codex 中可直接请求：

> 从 https://github.com/huzhongyyuan/mayue-paper-skill 安装 craft-ccfa-paper、mayue-paper-skill、write-top-ml-paper 和 yue-ma-paper-style 四个路径，保持它们在同一个技能根目录下。若已有旧版本，先保留备份再更新。

或者使用 Codex 自带的技能安装器（全新安装；已有同名技能时安装器会拒绝覆盖）：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo huzhongyyuan/mayue-paper-skill \
  --path craft-ccfa-paper mayue-paper-skill write-top-ml-paper yue-ma-paper-style
```

## 使用

```text
使用 $mayue-paper-skill，基于我的方法和实验逐节修改 Introduction，
让问题、洞察、模块和证据对应。给出实际改写，不补造结果。
```

```text
使用 $mayue-paper-skill，读取方法说明和代码，实际画一张论文框架图。
参考匹配的一作／共一案例，交付可编辑 SVG、原生形状 PPTX、预览和 caption。
```

```text
使用 $craft-ccfa-paper，检查并修改我的 LaTeX 双栏布局、图表位置和分页，
编译检查最终 PDF。
```

| 入口 | 行为 |
|---|---|
| [craft-ccfa-paper](craft-ccfa-paper/SKILL.md) | 统一研究、写作、图表与排版流程；按任务选择模式 |
| [mayue-paper-skill](mayue-paper-skill/SKILL.md) | 统一流程 + Mayue 一作／共一案例 |
| [write-top-ml-paper](write-top-ml-paper/SKILL.md) | 顶会通用模式；延续对话中已经选择的作者模式 |
| [yue-ma-paper-style](yue-ma-paper-style/SKILL.md) | 旧名称兼容入口 |

## 画图如何学习和执行

颜色表达稳定语义；总图定位模块，局部放大解释计算；显式表示训练状态、时间与缓存；动机图回应方法设计；正文、公式、箭头、图注与消融保持一致。

参见 [统一图表流程](craft-ccfa-paper/references/integrated-figures.md)、[作者图表案例](craft-ccfa-paper/modules/mayue/references/figure-playbook.md) 和 [逐节写作流程](craft-ccfa-paper/references/integrated-writing.md)。

Python 标准库即可生成四张原创 SVG 模板、运行结构化 SVG 工具及正文形式／术语检查。原生 PPTX 工具需要 Node.js 与 `pptxgenjs`。新增组件绘图工具需要 Pillow、Matplotlib、CairoSVG 和系统 Cairo；依赖及命令见 [共享事实与框架绘图指南](craft-ccfa-paper/modules/share-tools/references/guide.md)。HTML／主 SVG 保留文字，静态 PDF 使用字体轮廓。数值图需要真实数据，定性图需要真实结果素材。

## 覆盖与验证边界

截至 2026-09-16，作者资料记录 24 篇一作／共一方法论文及 1 篇综述的章节、主要模块和实验研读；合作作品另有结构概览。Canvas、Emoji、Motion 有逐段图谱。图形资料包含 25 张带归属的代表性图摘录与 4 张原创 SVG 模板。

会议库快照为 2026-08-04：25,421 条官方源元数据与 55 篇成功提取 PDF 结构特征的样本。元数据不等于精读全文；以上范围不代表全网穷尽、所有图逐张研读或实验已复现。未取得原作者的 PPTX／FIG／AI 编辑工程。

后续增补包括 [ICLR 2025](craft-ccfa-paper/modules/iclr2025/references/coverage.md) 的 3,705 条主会事件元数据、12 篇有范围的研读及 17 处图示检查；[CVPR 2024–2026](craft-ccfa-paper/modules/cvpr2024-2026/references/coverage.md) 的 9,629 条主会元数据、9,038 篇成功的自动提取、18 篇定向研读及 15 处图表检查。不同库有重叠，以上数量不相加为精读总数。

2026-11-06 新增共享事实／术语检查与框架图工具；已通过 30 项交接检查、12 项集成回归，并检查 HTML 与渲染后的 PDF 示例。形式检查不替代科学审阅，样本词数和句数不作为论文验收门槛。原有合并曾检查四个技能格式、101 个内部链接、语料查询、初始化防覆盖及 SVG／原生 PPTX 结构；这些历史检查不代表本次重新进行了 PowerPoint 应用内测试或全量语料分析。

详情见 [证据与维护说明](craft-ccfa-paper/references/merged-evidence.md) 和 [固定版本来源账本](craft-ccfa-paper/modules/mayue/references/source-manifest.json)。

## 来源与许可

保留原 `craft-ccfa-paper` 的 [MIT 许可](craft-ccfa-paper/LICENSE.txt)。第三方论文、图摘录及来源资料保留各自权利，不因收录而改为 MIT；详见 [来源归属说明](THIRD_PARTY_NOTICES.md)。仓库不附完整论文 PDF、私人会话、实验日志或原作者编辑工程。
