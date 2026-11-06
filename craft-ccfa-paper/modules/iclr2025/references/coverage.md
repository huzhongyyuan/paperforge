# ICLR 2025 覆盖账本

快照日期：2026-09-18。这里的“去年”以请求日期 2026 年解释为 2025 年。只包含 ICLR 2025 主会，不包含 workshop、BlogPosts、TMLR 或 JMLR 展示论文。

## 三层证据，不能相互替代

1. **全量官方索引**：3,705 条独立主会录用事件记录，均有题目、作者、摘要和链接；3,112 poster、380 spotlight、213 oral。对 oral 的重复展示事件去重，排除 122 条非主会记录。3,281 条有官方 topic，424 条未提供，未擅自补成官方分类。
2. **全文自动结构提取**：从 PDF 提取顶层章节、段落信号、caption、图表定位与图像特征。逐篇状态见 [机器进度](../corpus/progress.json)；统计与提取结果见 [自动报告](../corpus/report.md)。只有 `done` 表示自动解析成功，不表示语义精读或全图人工审查。下载失败、被阻止、待处理均不得计入已分析。
3. **有范围的样本研读**：12 篇目的性样本，前 6 篇有较深入的正文阅读，后 6 篇为跨领域的选段阅读；12 篇共人工查看 17 个带编号的指定图；全部没有宣称逐段核验所有正文与附录。精确范围见 [论文卡片](paper-cards.md) 和 [PDF 版本账本](../corpus/sample-ledger.json)。写作规则主要源自这层，不能称为全部论文共同规律。

## 官方源之间的差异

- [ICLR 官方论文集](https://proceedings.iclr.cc/paper_files/paper/2025)：3,703 篇。
- [官方日程数据](https://iclr.cc/static/virtual/data/iclr-2025-orals-posters.json)：筛选主会 source group 并去重后 3,705 篇。
- 两篇主会事件在论文集标题匹配中未找到：*Straightness of Rectified Flow: A Theoretical Insight into Wasserstein Convergence*；*The adaptive complexity of parallelized log-concave sampling*。仅记录源差异，不推断撤稿或拒稿。
- 数量、presentation、topic、差异记录和源文件 SHA256 见 [对账结果](../corpus/scope-reconciliation.json)。两篇额外记录保留公共 OpenReview PDF 链接；本轮两条链接均返回 HTTP 403，记为 `blocked`，不计入成功解析，也不绕过访问限制。

### 两条差异记录的预印本线索

2026-09-18 查公开 arXiv 记录找到以下候选来源，未把它们悄悄替换成会议 PDF：

- Rectified Flow 论文对应作者集合出现在 [arXiv:2410.14949](https://arxiv.org/abs/2410.14949)。[v5](https://arxiv.org/abs/2410.14949v5)（2025-02-23）标题为 *2-Rectifications are Enough for Straight Flows: A Theoretical Insight into Wasserstein Convergence*；[v6](https://arxiv.org/abs/2410.14949v6)（2025-04-13）为 *On the Wasserstein Convergence and Straightness of Rectified Flow*；[v8](https://arxiv.org/abs/2410.14949v8)（2026-06-07）为 *On the Convergence and Straightness of Rectified Flow*。标题、作者顺序与摘要中的保证表述存在版本差异，不能用最新版来断言会议版的定理内容。
- Parallelized log-concave sampling 的 [arXiv:2408.13045v2](https://arxiv.org/abs/2408.13045v2)（2025-05-19）与官方事件记录标题、作者相符；仅此仍不证明 PDF 与会议定稿逐字一致。

以上是摘要／版本记录核对，不是新增全文精读；也不据此解释两篇为何未在论文集标题匹配中找到。

## 使用与复查

从任何工作目录执行 skill 目录下的 `modules/iclr2025/scripts/query.py`：

```sh
python3 /path/to/craft-ccfa-paper/modules/iclr2025/scripts/query.py 'video generation' --abstract --limit 8
python3 /path/to/craft-ccfa-paper/modules/iclr2025/scripts/query.py --topic 'Theory' --presentation oral
python3 /path/to/craft-ccfa-paper/modules/iclr2025/scripts/query.py 'Differential Transformer' --phrase --evidence --limit 1 --captions 5
```

搜索是标题、作者与摘要的大小写不敏感 AND 匹配，排序为原索引顺序，不是相关性排名或质量评分。要引用具体技术结论，继续查原文。题目／摘要语料打包于 `corpus/papers.jsonl.gz`，不包含整批论文 PDF 或正文文本；样本 SHA256 用于绑定本次阅读版本。

`--phrase` 改为连续短语匹配，例如避免将分散出现的“world”和“model”误当作 world model 研究。`--evidence` 加载最近导出的解析状态、章节标题及前若干条图表 caption；`--captions` 控制每篇输出条数。提取项仍需回原文核验，状态快照在全量运行中可能略晚于实时进度。

需重新执行自动提取时，在用户工作区创建输出，安装 `pymupdf numpy` 后使用附带 `scripts/analyze_iclr.py`；它接受压缩 JSONL，支持 SQLite 断点恢复，默认解析后删除临时 PDF。`scripts/report_full_corpus.py` 生成可移植报告及压缩章节／图表特征。不要将网络批量抓取作为普通改段落任务的前置步骤。

## 解析局限

- 规则解析主要覆盖顶层章节，章节归类和段落修辞信号是启发式，不是逐小节语义标注。
- 字数／页数含参考文献和附录；不能据此推荐正文长度。
- caption 检测、图块边界、图类型与配色统计可能漏检或错配。OmniEdit Fig.4 已发现一次漏检；人工看过的 17 个图也不等于样本所有图都核验。
- 矢量图的自动边界可能夹入相邻文字，造成异常宽高比；自动几何中位数、面积和色彩比例只用于定位待检查样本，不能直接变成画图尺寸或版式建议。
- 版本 `2.6-iclr-appendix` 加入字母附录标题检测；仍不能保证所有排版均识别正确。多版本结果应按报告区分。
- 先处理 oral／spotlight 的中途统计有优先级偏差，不代表全会分布；只有最终状态账本才能说明实际分母。
- 全部来自接收论文，缺少拒稿对照与控制变量。不能从频率推导“怎样写就能中稿”。不推断作者真实构思经历、个人执笔归属或未经核实的作图软件。
