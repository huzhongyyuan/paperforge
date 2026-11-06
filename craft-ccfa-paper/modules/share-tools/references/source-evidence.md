# 分享包来源、范围与集成记录

来源：用户在本会话提供 `paper-skills-share.zip`。
集成日期：2026-11-06（Asia/Shanghai）。
源 ZIP SHA-256：`400323d31c45e7a7e08a2c3003351350be72842f7a4c96b3f59dc4defc67d138`。

## 如何接入现有 Mayue 蒸馏

- 保留 `craft-ccfa-paper` 为唯一维护入口，现有 Mayue 一作／共一卡片、会议样本、review 和 anti-defensive 层继续适用。没有增加两套独立 SKILL，也没有重写兼容入口。
- 导入 `figkit.py`、章节／名称检查器、共享事实交接、字体、示例和原测试材料。章节写法与视觉组件按需接入统一路线，不重复安装完整原文规则。
- 形式检查中的语料范围改为提示；不禁止有依据的摘要／结论数字。模块缺失仅在用户指定完整范围时失败；短段落与局部图可以只展示相关模块。修正空／不完整事实表的错误信息。
- 事实表优先复用项目记录；参数状态与新增／继承分列，避免将 `new` 当作训练状态。示意声明保留在每张图的注释块和 `labels.json`，不把“未声明示意”当作真实性证明。
- PDF 物理宽度与 `print_width_in` 对齐；静态导出使用所附字体的矢量轮廓，消除 macOS Cairo 的 Helvetica 替换与临时字体配置残留；HTML／主 SVG 保留可编辑文字，PDF 与 `framework-outlined.svg` 的字为轮廓。默认字号检查按现有指南使用 7 pt 提醒。示例输出改由 `--output` 指定，避免写入技能安装目录。

原包仅提供统计说明，未附完整论文清单、固定版本 PDF 或编码原始表。本次未重新阅读原包声称的 21 篇论文或复算统计，不新增已验证作者语料数量，也不把混合署名语料归为个人文笔。现有 Mayue 库有自己的身份、共一与版本核验记录；两者不相加。

## 许可与分发

字体和 `OFL.txt` 一起保留，字体使用 SIL OFL 1.1。源 ZIP 未附 Python 代码／参考文字的明确许可；本模块取自用户提供的材料，保留来源和本地修改记录；本仓库不据此替上游授予 MIT 或其他再使用许可。主技能自己的许可不自动消除第三方材料的权利归属。

## 原包写作统计说明（原文，未独立复核）

# 依据与偏差

语料是 Yue Ma 署名的 21 篇论文，部分为二作、合作或通讯，因此不全是其本人的文笔。统计来自 PDF 自动抽取，有噪声，只应作为范围参考。

## 复核

| 项目 | 原分析 | 复算 | 处理 |
|---|---|---|---|
| 摘要词数中位 | 223 | 220（口径略不同） | 采用 223 |
| 挑战句 / 断言 / 数字 / SOTA | 17 / 18 / 4 / 3 | 相同 | 保留 |
| 引言词数中位 | 751 | 750 | 保留 |
| `we propose` 类 | 21/21 | 相同 | 保留 |
| “the first” | 11/21 | 相同 | 保留 |
| 转折句 | 18/21 | 19/21 | 写成 18–19 |
| 基线 / 消融 / user study | 20 / 20 / 12 | 相同 | 保留 |
| “硬件与耗时每篇都有” | 全部 | 13/21 提到硬件 | **已更正** |
| 不列贡献的论文 | Shape、Preference | Creation、Preference | **已更正** |

## 新增统计

相关工作、结论和图注是这次新做的，都基于同一批 Markdown 缓存：

- 综述和 MultiPose 没有 Related Work 章，相关工作的分母是 19。
- 结论有 3 篇抽取失败（两篇串入后续内容，一篇被表格截断），词数和句数统计时已排除。其中 LiveLight 的“提及实验”也可能漏计。
- “结尾提及自身或对比”是关键词判断，只是近似。

## 局限

- 这些是一位作者及其合作者的习惯，不是顶会的通用标准。目标会议的页数和格式要求优先。
- 语料偏扩散模型和视频生成。其他方向可以用结构，但模块和指标要换。
- 比例描述的是这批论文，不能证明照此写就更容易中稿。


## 原包绘图统计说明（原文，未独立复核）

# Evidence

Source: the main framework figure of 19 of the 21 papers. The survey has only a taxonomy figure and Follow-Your-Preference is an analysis paper, so both are excluded.

Counts come from one reader coding the figures by eye. Treat them as strong tendencies, not exact rates. Sizes and colours are measured from 300 dpi renders; 18 figures were measured, as Canvas was only read from its page render.

## Features

| Feature | Count | Exceptions |
|---|---|---|
| Real images as input and output | 19/19 | none |
| Rounded comic-style font | 16/19 | MagicStick (Calibri-like), Canvas (Arial), SimVTP (Times) |
| Stacked cards for video | 16/19 | Creation, Shape, Color |
| Trapezoid encoder or decoder | 15/19 | Ego, MultiPose, SimVTP, Instruction |
| Fire or snow state icons | 14/19 | Shape, MultiPose, MagicStick, SimVTP, Instruction |
| Legend | 14/19 | Creation, Group, Ego, SimVTP, Instruction |
| Network drawn as tall bars | 14/19 | Group, Ego, Shape, SimVTP, Instruction |
| Dashed pastel container | 10/19 | Others use solid or unfilled frames |

## Layout

| Layout | Figures |
|---|---|
| Main pipeline + detail column, split by a divider | Pose, Creation, FastVMT, Group, MagicStick, Shape, LiveLight, Color, Canvas |
| Training over inference | Click, Emoji, Emoji-Faster |
| Stacked stages | Motion, EasyVFX |
| Pipeline over zoomed modules | Ego (Emoji-Faster adds this too) |
| One left-to-right row | MultiPose, Pose v2, SimVTP |
| Numbered agent loop | Instruction |

## Measurements

- Aspect ratio: median 2.25, range 0.89 to 5.89.
- Printed width: median 6.7 in, about 79% of the page width.
- Label size: roughly 4.5 to 7 pt in print, estimated from a few figures.
- Largest image: roughly 8 to 15% of the figure width, estimated from a few figures.
- Strongly saturated pixels: 1 to 11% of the area. Colour is an accent.

## Limits

- Style differs by role and year. Canvas is a second-author paper and SimVTP and MagicStick are early work, so the rules follow the 2024-2026 first-author figures.
- Palette values were sampled from Follow-Your-Emoji-Faster. Other figures vary, for example the container stroke of Click is yellow.
- Comic Neue stands in for the original handwriting font, whose identity was not confirmed.


## 本机集成验证

`2026-11-06T14:00:53+08:00｜工具增补验证｜30 项交接检查与 12 项集成回归通过，示例 lint clean；浏览器检查 HTML、Poppler 渲染并检查 PDF；本条验证工具交接与导出，不验证论文主张。`

运行入口为 `tests/test_handoff.py`、`python -m unittest discover -s tests -p test_integration.py -v` 及 `examples/minimal/build.py --output ...`（相对本模块）。本次使用独立虚拟环境和已有 Homebrew Cairo，未修改系统 Python 或 shell 配置。导入文件的原始／本地哈希见 [source manifest](source-manifest.json)。
