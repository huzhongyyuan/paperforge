# ICLR 2025 自动结构分析：本轮完成

成功 3703/3705；状态分布 `{"done": 3703, "blocked": 2}`。自动解析 ≠ 逐篇精读。样本写作结论见 [论文卡片](../references/paper-cards.md)。

自动图块边界可能夹入相邻文字，尤其是矢量图；宽高比、面积、配色等统计仅供定位复查，不能直接用作画图规格。

# Full-corpus paper writing and figure analysis

This report is descriptive. It does not claim that a layout or phrase causes acceptance.

## Coverage

- Report state: **complete**
- Papers analyzed: 3,703
- Priority papers analyzed: 593
- Status counts: `{"blocked": 2, "done": 3703}`
- Analyzer versions: `{"2.6-iclr-appendix": 3703, "unprocessed": 2}`

| Venue-year | Records | Done | Blocked | Error | Figures | Tables |
|---|---:|---:|---:|---:|---:|---:|
| ICLR 2025 | 3,705 | 3,703 | 2 | 0 | 40,917 | 31,800 |

## Extraction quality diagnostics

These are parser review flags, not evidence that the paper lacks the underlying content. Named method sections may not match canonical headings; some genres legitimately omit a canonical section.

- `missing_experiments`: 528
- `missing_conclusion`: 425
- `missing_method`: 308
- `missing_introduction`: 60
- `zero_detected_figures`: 50
- `missing_references`: 22
- `oversized_main_section`: 9
- `missing_abstract`: 4
- `low_section_count`: 2

## Section construction

Medians are shown as `poster / priority`, where priority means oral or spotlight. Presentation groups are descriptive, not controlled comparisons of writing quality. Counts apply to detected categories, not necessarily all papers.

| Section | Paper count | Words | Sentences | Sentence length | Citations | Figure refs |
|---|---:|---:|---:|---:|---:|---:|
| abstract | 3,107 / 592 | 199.0 / 199.0 | 8.0 / 8.0 | 23.86 / 24.53 | 0.0 / 0.0 | 0.0 / 0.0 |
| introduction | 3,061 / 582 | 902.0 / 882.0 | 30.0 / 29.0 | 29.45 / 30.04 | 3.0 / 3.0 | 2.0 / 2.0 |
| related_work | 2,308 / 414 | 566.0 / 543.0 | 21.0 / 20.0 | 27.16 / 27.46 | 5.0 / 4.0 | 0.0 / 0.0 |
| background | 1,183 / 224 | 671.0 / 734.0 | 22.0 / 24.5 | 29.51 / 28.91 | 1.0 / 1.0 | 0.0 / 0.0 |
| method | 2,857 / 538 | 1339.0 / 1302.5 | 45.0 / 44.0 | 29.01 / 28.65 | 2.0 / 2.0 | 2.0 / 3.0 |
| theory | 212 / 33 | 1170.0 / 1697.0 | 42.0 / 53.0 | 29.3 / 29.12 | 0.0 / 1.0 | 0.0 / 1.0 |
| data | 186 / 40 | 1152.0 / 1162.0 | 44.0 / 46.5 | 26.06 / 26.55 | 2.0 / 4.0 | 3.0 / 2.5 |
| experiments | 2,696 / 479 | 1828.0 / 1859.5 | 64.0 / 65.0 | 28.03 / 27.63 | 6.0 / 6.0 | 5.0 / 6.0 |
| limitations | 454 / 86 | 218.0 / 249.0 | 9.0 / 11.0 | 22.88 / 22.59 | 0.0 / 0.0 | 0.0 / 0.0 |
| conclusion | 2,770 / 508 | 215.0 / 221.0 | 8.0 / 9.0 | 25.09 / 24.81 | 0.0 / 0.0 | 0.0 / 0.0 |

Common detected section orders:

- `abstract > introduction > related_work > method > experiments > conclusion` — 636 papers
- `abstract > introduction > related_work > background > method > experiments > conclusion` — 238 papers
- `abstract > introduction > related_work > method > method > experiments > conclusion` — 183 papers
- `abstract > introduction > background > method > experiments > conclusion` — 141 papers
- `abstract > introduction > background > method > experiments > related_work > conclusion` — 112 papers
- `abstract > introduction > method > experiments > conclusion` — 109 papers
- `abstract > introduction > method > experiments > related_work > conclusion` — 104 papers
- `abstract > introduction > background > method > method > experiments > conclusion` — 64 papers
- `abstract > introduction > related_work > background > method > method > experiments > conclusion` — 52 papers
- `abstract > introduction > experiments > related_work > conclusion` — 39 papers
- `abstract > introduction > related_work > method > experiments > experiments > conclusion` — 38 papers
- `abstract > introduction > background > method > method > experiments > related_work > conclusion` — 36 papers

## Figure construction

| Figure type | Poster / priority count | Median page | Median width/page | Median aspect | Caption words | Takeaway % |
|---|---:|---:|---:|---:|---:|---:|
| other | 8,032 / 1,706 | 18.0 / 20.0 | 0.63 / 0.65 | 4.06 / 5.41 | 23.0 / 25.0 | 10.2 / 11.6 |
| quantitative_plot | 6,467 / 1,446 | 15.0 / 15.0 | 0.65 / 0.65 | 6.31 / 14.6 | 40.0 / 44.0 | 24.0 / 25.2 |
| dataset_examples | 5,417 / 1,304 | 19.0 / 23.0 | 0.62 / 0.61 | 1.9 / 1.7 | 30.0 / 28.0 | 13.1 / 13.7 |
| diagram_or_plot | 3,856 / 878 | 17.0 / 20.0 | 0.59 / 0.57 | 2.92 / 2.95 | 20.0 / 24.0 | 9.7 / 10.7 |
| architecture_pipeline | 2,305 / 424 | 4.0 / 5.0 | 0.59 / 0.6 | 2.59 / 2.66 | 52.0 / 50.0 | 11.6 / 11.8 |
| visual_examples | 1,812 / 473 | 19.0 / 21.0 | 0.58 / 0.59 | 1.21 / 1.25 | 21.5 / 23.0 | 11.9 / 10.6 |
| ablation_sensitivity | 1,686 / 327 | 16.0 / 19.0 | 0.64 / 0.63 | 4.45 / 12.22 | 32.0 / 35.0 | 20.0 / 20.2 |
| qualitative_comparison | 1,604 / 260 | 18.0 / 21.0 | 0.62 / 0.63 | 1.12 / 1.04 | 27.0 / 27.0 | 17.3 / 12.3 |
| representation_visualization | 1,205 / 299 | 14.0 / 17.0 | 0.61 / 0.62 | 2.2 / 2.47 | 38.0 / 44.0 | 17.6 / 22.1 |
| motivation_teaser | 902 / 175 | 5.0 / 6.0 | 0.57 / 0.57 | 2.54 / 2.37 | 36.0 / 39.0 | 10.6 / 8.6 |
| failure_case | 298 / 41 | 20.0 / 21.0 | 0.61 / 0.62 | 1.63 / 2.98 | 29.0 / 30.0 | 20.1 / 24.4 |

First-figure roles:

- architecture_pipeline: 791
- quantitative_plot: 628
- other: 614
- dataset_examples: 548
- motivation_teaser: 423
- diagram_or_plot: 272
- representation_visualization: 151
- visual_examples: 105
- ablation_sensitivity: 56
- qualitative_comparison: 44
- failure_case: 21

## Table construction

| Table role | Poster / priority count | Median page | Caption words | Protocol % | Comparison % |
|---|---:|---:|---:|---:|---:|
| other | 10,249 / 1,893 | 19.0 / 20.0 | 15.0 / 17.0 | 8.7 / 9.2 | 17.1 / 15.2 |
| quantitative_plot | 6,856 / 1,135 | 17.0 / 18.0 | 28.0 / 29.0 | 49.7 / 45.6 | 29.2 / 28.5 |
| dataset_examples | 3,094 / 554 | 19.0 / 20.0 | 23.0 / 23.0 | 67.4 / 63.4 | 16.0 / 9.9 |
| diagram_or_plot | 2,525 / 526 | 18.0 / 19.0 | 14.0 / 15.0 | 8.1 / 9.3 | 16.7 / 15.4 |
| ablation_sensitivity | 2,403 / 352 | 15.0 / 15.0 | 19.0 / 21.0 | 25.6 / 24.4 | 7.9 / 8.5 |
| qualitative_comparison | 582 / 71 | 15.0 / 10.0 | 27.0 / 27.0 | 30.2 / 35.2 | 78.9 / 74.6 |
| architecture_pipeline | 499 / 108 | 18.0 / 18.0 | 26.0 / 23.0 | 24.8 / 19.4 | 19.4 / 15.7 |
| visual_examples | 361 / 84 | 16.0 / 16.5 | 17.0 / 16.5 | 10.5 / 7.1 | 30.2 / 21.4 |
| representation_visualization | 288 / 62 | 18.0 / 18.0 | 28.5 / 30.5 | 13.2 / 16.1 | 20.8 / 19.4 |
| motivation_teaser | 62 / 18 | 16.5 / 20.5 | 15.0 / 27.5 | 1.6 / 5.6 | 14.5 / 11.1 |
| failure_case | 65 / 13 | 19.0 / 37.0 | 32.0 / 16.0 | 20.0 / 0.0 | 16.9 / 7.7 |

## How to use the figure evidence

The following are general design guidance, not conclusions established by these automatic counts. Figure roles and caption signals are heuristic labels; inferred vector bounds may include text and make geometric statistics unreliable.

- Make Figure 1 carry the problem contrast, central mechanism, or end-to-end promise.
- Use architecture figures to show input-to-output flow, stage boundaries, train/test differences, and the claimed novelty.
- Use qualitative grids with fixed rows/columns, identical crops, visible failure cases, and captions that state the comparison protocol.
- Use quantitative plots for one question per panel; expose uncertainty, axes, units, and compute/data conditions.
- Use ablations to map one visual intervention to one method claim; avoid panels that merely repeat the main table.
- Use table groups and protocol columns to expose which numbers are genuinely comparable; bold only within valid groups.
- Treat the median dimensions above as diagnostics, not templates. The scientific question determines the layout.

## Files

- `summary.json`: machine-readable aggregates
- `figures.jsonl.gz`: one row per detected figure/table with caption and visual features
- `sections.jsonl.gz`: one row per detected section with writing features
