# CVPR 2024–2026：覆盖、分母与使用边界

本模块已安装，可离线检索和用于写作。**官方目录覆盖 9,629 篇，自动提取成功 9,038 篇；实际定向研读 18 篇，查看 11 篇中的 15 处图表。** 自动提取完成不等于逐篇理解或文本质量通过。

元数据快照：`2026-10-19T09:43:00.399912+00:00`；最终统计：`2026-10-19T10:52:25.906220+00:00`。权威数据为 [manifest](corpus/manifest.json)、[statistics](corpus/statistics.json)、[阅读范围](reading-ledger.json) 和 [逐篇提取缺口](corpus/extraction-gaps.json)。

## 官方范围与标签

统计总体为 [CVF 2024](https://openaccess.thecvf.com/CVPR2024?day=all)、[2025](https://openaccess.thecvf.com/CVPR2025?day=all)、[2026](https://openaccess.thecvf.com/CVPR2026?day=all) 主会 proceedings；排除 workshops。Oral/Highlight 从官方 accepted/event 页面匹配，十份网页压缩快照及其原始字节哈希保留在 [manifest](corpus/manifest.json) 所列 `corpus/sources/`。

| 年份 | CVF 论文 | Oral | Highlight | Poster | 标签未知 | 自动提取成功 | 保留旧失败 | 本轮失败 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024 | 2,716 | 90 | 324 | 2,301 | 1 | 2,712 | 0 | 4 |
| 2025 | 2,871 | 95 | 388 | 2,385 | 3 | 2,814 | 57 | 0 |
| 2026 | 4,042 | 141 | 564 | 3,305 | 32 | 3,512 | 530 | 0 |
| 合计 | 9,629 | 326 | 1,276 | 7,991 | 36 | 9,038 | 587 | 4 |

- 三年官方 Oral 均与 proceedings 匹配；自动提取完成其中 323/326 篇，Highlight 为 1,262/1,276 篇，Poster 为 7,420/7,991 篇，未知标签为 33/36 篇。
- 2026 官方事件目录有 5,023 条，而 CVF proceedings 有 4,042 篇；本模块以 CVF 为总体，不把额外事件条目自动解释为漏收论文。2026 Highlight 名单 575 条，匹配到本总体 564 条。未匹配项保留在 [unmatched](corpus/unmatched.json)，不猜测最终发表状态。
- 2026 `AcceptedPapers` 路径返回 404，已使用可访问的官方 papers/oral/highlight 页面；[原始错误](corpus/source-errors.json)保留，没有重试该 404。
- 标签权重为 **Oral 3 / Highlight 2 / Poster 1**，不叠加。36 篇未知标签保留在未加权视图，排除出加权视图。原 manifest 的 unknown=1 兜底字段保留为历史记录，统计导出器明确覆盖这一点。

## 自动提取覆盖及质量

复用了 **6,294** 条论文身份、URL 与 analyzer 2.6 相符的成功结果；新增 **2,744** 条成功结果。最终没有 pending/processing 行。导出包含 9,629 条论文状态、69,189 个检测章节块及 91,563 个检测图表项，全部成功提取使用 analyzer 2.6。

这里的章节和图表是启发式检测项，不等于人工确认的真实章节/图数。PDF 词数和页数可包含参考文献及附录；章节分段、caption 匹配、修辞正则、像素代理特征尚未做全库准确率评测。不能将颜色、留白或 edge density 当作审美分数。

**14 篇成功记录的提取词数少于 1,000**，已显式标记 `low_extracted_word_count_under_1000`。这是待检查筛选阈值，不是质量合格线；原始分布保留这些记录，没有静默删除。任何单篇写法归因仍须回到原文。

保留的缺口：587 条历史非 429 失败没有重试；本轮 4 条失败中，一条超过 80 MiB 下载上限，三条只留下 `cannot pickle 'BufferedReader' instances`，原始异常原因无法恢复，不能猜为 429。已修复 worker 异常跨进程序列化，并以无网络合成用例核验；这不补回历史论文提取。只对明确 HTTP 429 最多重试两次，保留 10/30 秒退避及 Retry-After 上限。

## 描述性分布，不是写作配额

三年按论文合并，不按年份等权。先把同篇同类章节块相加；图注先取每篇均值，再对论文聚合。未检测到类别表示缺失，不能填零。分位数采用逆经验分布；加权分母排除标签未知论文。下表为**中位数 [P25, P75]**，单位为自动检测词数。

| 检测对象 | 未加权检测篇数 / 成功篇数 | 未加权分布 | 加权检测篇数 / 有标签成功篇数 | 3/2/1 加权分布 |
|---|---:|---:|---:|---:|
| 摘要词数 | 9,005 / 9,038 | 196 [174, 220] | 8,972 / 9,005 | 195 [173, 219] |
| 引言词数 | 9,004 / 9,038 | 788 [672, 909] | 8,971 / 9,005 | 787 [669, 908] |
| method 类块合计词数 | 8,806 / 9,038 | 1,833 [1,508, 2,228] | 8,773 / 9,005 | 1,839 [1,511, 2,241] |
| experiments 类块合计词数 | 8,698 / 9,038 | 1,828 [1,493, 2,198] | 8,665 / 9,005 | 1,825 [1,485, 2,195] |
| 每篇平均图注词数 | 9,012 / 9,038 | 45.8 [34.9, 58.5] | 8,979 / 9,005 | 46 [35, 58.6] |

这些值帮助发现明显偏长/偏短后再读稿，不规定摘要必须 195 词、引言必须 787 词，更不规定固定段数。method/experiments 分类可能混入小节或附录，不能用上述合计推导主文页配额。按年份/标签分组及检测权重分母均可从查询工具查看。

## 实际阅读和图表检查

[18 张 paper cards](paper-cards.md)涵盖机制、几何表征、视频扩展、效率、数据、benchmark 和经验发现：2024 年 7 篇、2025 年 5 篇、2026 年 6 篇；11 Oral、5 Highlight、2 Poster。全部阅读摘要/引言，其中 8 篇进一步阅读选定的方法、实验或讨论位置。该样本按可迁移决策选择，不是随机代表样本。

15 处实际看图来自 11 篇，包含框架、动机、数据统计、定性对比、时空切片、热图、曲线与表格；部分只查看局部裁剪，caption 覆盖情况记在 [reading-ledger](reading-ledger.json)。不声称已视觉检查其余九千余篇。规则中的设计建议、案例观察及机器统计分开标识；没有逐篇精读所有 Related Work 或 supplementary。

Oral/Highlight 优先级用于发现值得研读的案例和描述性统计。已录用论文有选择偏差；这些资料不能证明某种段落、配色或句式导致高分或录用。

## 离线使用

以下命令从 skill 根目录运行，或把脚本替换为绝对路径。查询不下载 PDF；日常修改按任务只加载 1–3 个匹配案例。

```bash
python3 modules/cvpr2024-2026/scripts/query.py search --year 2026 --query EffectErase
python3 modules/cvpr2024-2026/scripts/query.py cards --query FreeU
python3 modules/cvpr2024-2026/scripts/query.py stats --year 2025 --presentation oral --metric section.introduction.word_count
python3 modules/cvpr2024-2026/scripts/query.py features --id b28e3c265e414c05ffd2213c --limit 1
```

检索元数据用于找到论文；cards 显示实际阅读范围；stats/features 返回启发式数据。新主题优先复用决策结构，再读取匹配原文，不将 CVPR 双栏布局硬套到 ICLR。

## 版本与验证

- 语料未压缩 JSONL SHA-256：`b85b6ecbf01d59590a6035baba768ffd1cffbec48befcb6906a73f2033524f1c`。
- 语料 gzip 文件 SHA-256：`0e940cb768aa5867342b3f58833633d9a7aa5224fec9531c123ed6f510fc342b`。
- 导出文件哈希、分析器版本、来源分类与状态保存在 [statistics](corpus/statistics.json)。`corpus_sha256` 在 manifest 和统计中均指解压后的 JSONL，压缩字节另用 `corpus_gzip_sha256`。
- 已用独立于导出器实现的 SQL 与整数权重展开计算复算 180 个分组/指标分布，核对 ID、状态、行数、哈希与缺口集合；源数据库未改变。这是同一执行者的复算，不称独立审稿。
- 15 项导出器功能检查与 4 种 worker 合成场景通过。另有 6 个原创复用场景自检，覆盖消融归因、预算比较、动态证据、句段语义和阅读范围；尚无独立盲测，不以此宣称写作质量或录用率提升。
- 最终离线交付检查通过：11 份 Markdown 中的 137 个本地链接和 70 个锚点有效；6 个 Python 脚本语法、分组统计与单篇特征查询、9 种无效参数处理以及 skill 结构验证通过。外部网页未在这一步重新抓取。

技能可复用部分是“情境 → 诊断 → 写作/视觉操作 → 来源 → 适用边界 → 验收”，不是九千篇文章句式的机械混合。


## GitHub 可移植发布 — 2026-11-06

发布包将历史数据库的绝对机器路径替换为 `source-corpus:top-ml/full-analysis`。该标识只改变 `features-paper.jsonl.gz` 中的来源位置表达；论文、指标、状态、时间、权重和其余字段保持原值。压缩文件哈希已同步到 `statistics.json`，原始／发布哈希与替换数量见 [publication.json](corpus/publication.json)。没有在本次发布中重跑提取或补齐历史缺口。
