# 按贡献选择论证，而不是套固定段数

本文件是 18 篇定向研读的可迁移归纳，非 9,629 篇逐篇语义评审。来源和实际阅读范围见 [paper cards](paper-cards.md)，全库机器统计见 [coverage](coverage.md)。Oral/Highlight 用于研读优先级与描述性加权；不使个别写法成为规范。

## 路由：稿件究竟新增了什么

先用一句话回答“删去方法名，读者还会记住什么新增知识或能力”。用真实材料选择下面一条主线，混合型论文可有从线，但每条贡献须有独立证据。

| 新增内容 | 核心论证动作 | 最容易漏掉的证据 | 定向来源 |
|---|---|---|---|
| 新机制/算子 | 观察到的限制 → 计算中的原因 → 可操作干预 → 机制与结果验证 | 只提高主分数，未测预期中间变化 | [FreeU](paper-cards.md#f800a97293edd4ff6088e891)；[VideoGigaGAN](paper-cards.md#71ca4dbb84e8c875682c2ccf) |
| 统一表征/框架 | 原输入或任务差异 → 共同接口 → 从接口导出的能力 | 测试输入假设、后处理成本、输出头角色 | [FoundationPose](paper-cards.md#496072b5afa6e25a53f302c6)、[DUSt3R](paper-cards.md#289aeef0f82b266560ab5e4c)、[VGGT](paper-cards.md#355aab66505b9c4483abd3b7) |
| 模型向新域/新时序扩展 | 继承的能力 → 新条件打破的假设 → 保留旧能力的改造 | 新能力收益与旧能力退化是否同时测量 | [Video Depth Anything](paper-cards.md#b4fa856bef2cee9204ad8cc5) |
| 效率/系统 | 实测瓶颈 → 近似或重用条件 → 资源转化为能力 | 同质量/同预算比较、代理量与误差关系 | [PTv3](paper-cards.md#a175f954c059c77aad6dc20d)、[SenCache](paper-cards.md#6462ee844611f804b8e9e9f0) |
| 数据集 | 目标能力缺少哪些观测 → 采集/标注选择 → 质量与覆盖 → 下游用途 | 数据单位、质量误差、评测子集及限制 | [Ego-Exo4D](paper-cards.md#41ca9fbe640d4a45cca1a3e2)、[GigaHands](paper-cards.md#9e532d6a1fb5f3d41756fcd2)、[OLATverse](paper-cards.md#2a6d999de916b800b3bea578) |
| Benchmark/评价 | 宽泛能力 → 可测维度 → 输入/评分 → 评分有效性 → 模型诊断 | 排名之前先证明评分测到了什么 | [VBench](paper-cards.md#7408bccff4dcfda8985400df)、[PAI-Bench](paper-cards.md#123d97c0f1c7d1b78f3fa8bb) |
| 经验发现/协议纠偏 | 竞争解释 → 控制变量 → 可操作测量 → 发现及反例 | 正规化是否合理；混杂是否排除 | [Neural Redshift](paper-cards.md#5f99ee9084cbfb119efdf058)、[Task Transfer](paper-cards.md#fecf4b9fa84210facabbf931)、[Dataset Distillation](paper-cards.md#f981f123b2ada842bea1db44) |

## A1. 设计顺序由依赖决定

**触发**：为凑“两大挑战/两大模块”把同一个问题重复说两遍，或几个模块各自有动机却无法连起来。

**诊断与操作**：判断 B 是解决 A 后暴露的问题，还是独立分支。前者写“干预 A 改善 X，但留下 Y；B 作用于 Y”；后者给共同输入及不同职责。FreeU 的 backbone/skip 分工和 VideoGigaGAN 的一致性/细节处理支持递进路线；MV-DUSt3R+ 的多视图与 cross-reference 需求也呈现残留问题引出下一设计。不要为文风改动实际计算依赖。

**来源**：[FreeU pp.1–2/4](paper-cards.md#f800a97293edd4ff6088e891)、[VideoGigaGAN Fig.4](paper-cards.md#71ca4dbb84e8c875682c2ccf)、[MV-DUSt3R+ pp.1–2](paper-cards.md#d4ca9b4dd41280af93097d5c)。**边界**：叙事先后不证明模块因果；累加消融不能估出所有交互。**验收**：每个“因此/但/为此”的下一动作由上一事实推出，模块顺序与代码一致。

## A2. 找到迁移时真正改变的条件

**触发**：扩展论文只写“已有方法不能处理我们的任务”。

**操作**：先承认已有能力，再指出新增输入/几何/时长条件改变哪项假设，解释保留哪些部件、改动哪个接口。VDA 从单帧空间先验转向时序一致性；FoundationPose 按 CAD/参考图像等可用信息划分输入。不能把已存在的 effect removal、几何恢复等能力重新包装成空白。

**来源**：[VDA pp.1–3](paper-cards.md#b4fa856bef2cee9204ad8cc5)、[FoundationPose pp.1–2](paper-cards.md#496072b5afa6e25a53f302c6)。**边界**：只有实测失败或原文适用条件才可写已有方法的局限；任务差异不自动证明某模块必要。**验收**：能用一条受控比较检验这个“条件变化”，而不只比较最终系统。

## A3. 数据需求是可观测量的缺口

**触发**：突然从几何/语义问题跳到“所以我们构建大数据集”。

**操作**：补足所缺观测：需要同时看到哪些状态、视角、动作、结果；采集决定如何提供它们；质量控制保护哪一对应关系。数据规模随后说明覆盖，不代替监督含义。EffectErase 将目标—效应问题与 before/after 监督相连；Ego-Exo4D 把第一/第三视角与技能任务相连。

**来源**：[EffectErase pp.1–3](paper-cards.md#b28e3c265e414c05ffd2213c)、[Ego-Exo4D pp.1–3](paper-cards.md#41ca9fbe640d4a45cca1a3e2)。**边界**：配对观测提供训练信号，不自动消除混杂或证明因果识别；未经检索不写“现有数据完全没有”。**验收**：从监督对象能直接推出所需数据字段与评价问题。

## A4. Contributions 写可检查的新内容

不要硬性规定三条或把“进行了实验”单独算创新。按本稿最主要的新增内容分条；同一框架的阶段名、子模块、实验收益不要换名字重复计数。

- **机制型**：提出什么操作/表征，改变什么计算关系，支持什么经过验证的能力。
- **数据型**：提供什么以前缺少的观测/标注与覆盖，允许什么训练或评价；帧、序列、小时分别表达。
- **经验型**：控制哪些因素，发现什么关系，给什么可复用测量/协议。Task Transfer 的测量与关系研究不需要编造一个新网络。
- **统一型**：共享什么接口，涵盖哪些输入假设/输出；不要把后处理能力混入单次前向能力。

**来源**：[FoundationPose](paper-cards.md#496072b5afa6e25a53f302c6)、[Task Transfer](paper-cards.md#fecf4b9fa84210facabbf931)、[GigaHands](paper-cards.md#9e532d6a1fb5f3d41756fcd2) 的引言。**边界**：数据/框架/技术三条不是通用公式；结果可能是科学发现本身。**验收**：给每条找到不同的主要证据位置，删去方法名称后仍可辨别贡献。

## A5. 论证闭环不是重复措辞

建立小型映射：Intro 的问题 → Method 中改变的对象 → 实验中比较的变量 → 图中可见的现象 → 结论的范围。缺边时补证据或缩小主张，不把同一句“有效提升”写五遍。

**来源**：[PTv3](paper-cards.md#a175f954c059c77aad6dc20d) 的瓶颈与效率证据、[VBench](paper-cards.md#7408bccff4dcfda8985400df) 的维度与人评验证。**边界**：这是案例归纳后的编辑操作，不是已测得的录用规律。**验收**：每项关键 claim 有唯一可定位的支撑；代理指标不被改名为真实能力。
