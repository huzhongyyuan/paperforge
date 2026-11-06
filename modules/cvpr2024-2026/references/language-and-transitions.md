# 语言与衔接：修改关系，不堆连接词

用于句子通顺但论证跳步、段落重复、名词密集和结论过强的稿件。以下英文前后例均为本模块原创的**假设示例**，不是参考论文原句或已验证实验。

## L1：让下一句接住上一句留下的具体对象

**触发/诊断**：前一句讲任务价值，后一句突然列技术问题；补 `however` 后仍不通。先标出两句的主语和信息焦点，找出中间缺的需求或条件。

**操作**：把前句的新信息变成后句的已知对象；若两者没有真实因果，使用范围转换或对比，不强写因果。

- 前：`Video editing is useful for content creation. However, shadows are difficult.`
- 后：`Removing an object from a video also requires removing the changes it causes in the scene. Shadows can extend beyond the object mask, leaving part of the requested edit unspecified by the mask.`

**来源**：[EffectErase](paper-cards.md#b28e3c265e414c05ffd2213c) pp.1–3 把对象移除、效应和 mask 条件连起来。**边界**：示例只适用于任务确实包含关联效应时；不从中推出所有 mask 方法都无法处理效应。**验收**：遮住连接词，读者仍能指出两句的具体关系。

## L2：把“挑战→模块”之间的缺项写出来

**触发/诊断**：`Temporal consistency is challenging. We introduce module X.` 缺少 X 为什么能影响这个挑战的解释。

**操作**：写出一个已有观察，以及它对所需信息/计算的约束；让设计回应这个约束。观察不足时把原因写为待检验假设。

- 前：`Long videos are challenging. We use a temporal head.`
- 后：`Independent frame predictions can vary even when the scene changes little. A temporal head exchanges features across frames while retaining the pretrained spatial encoder.`

**来源**：[Video Depth Anything](paper-cards.md#b4fa856bef2cee9204ad8cc5) pp.1–3；[PTv3](paper-cards.md#a175f954c059c77aad6dc20d) pp.1–3 的资源诊断。**边界**：实际未冻结 encoder 时不能使用示例后半句；架构机制本身还不证明效果。**验收**：删掉模块名称后，读者仍能解释该设计应接收什么信息、改变什么计算。

## L3：按真实依赖连接段落，不追求对称

**触发/诊断**：两个问题其实是同一问题的重述，或第二设计回应第一设计的副作用，却被写成互不相干的 `First/Second`。

**操作**：先给第一设计解决的对象，再说明其剩余限制，由此引出第二设计；独立需求才并列。段首具体复指上段的输出/未解问题。

- 前：`First, details are important. Second, smoothness is important.`
- 后：`Strengthening the low-frequency branch improves the coarse structure, but can suppress fine detail. The second operation therefore adjusts the complementary high-frequency path.`

**来源**：[FreeU](paper-cards.md#f800a97293edd4ff6088e891) pp.1–2、p.4；[MV-DUSt3R+](paper-cards.md#d4ca9b4dd41280af93097d5c) pp.1–2。**边界**：示例中的改善与副作用需要各自有证据；真正并行模块不能被改成顺序阶段。**验收**：每个 `therefore/these/this limitation` 有明确前件；每段增加一个新的论证动作。

## L4：让动词说明谁对什么做了什么

**触发/诊断**：连续抽象名词、过长定语，读者看不出输入、操作、输出。

**操作**：把关键对象放主语/宾语，把名词化动作改为动词；非必要术语延后。保留真正有技术意义的对象名，不做同义词轮换。

- 前：`The integration of complementary target-evidence representations enables the enhancement of association modeling.`
- 后：`Scene features attend to target descriptors from both views, allowing each location to use the selected object's appearance.`

**来源**：[FoundationPose](paper-cards.md#496072b5afa6e25a53f302c6)、[DUSt3R](paper-cards.md#289aeef0f82b266560ab5e4c)、[VGGT](paper-cards.md#355aab66505b9c4483abd3b7) pp.1–2 对输入、共同表征与输出的区分；具体改句是编辑启发。**边界**：attention 方向必须符合实现；“可使用目标外观”不等于“已正确识别所有关联效应”。**验收**：可画出与句子一致的有向边；连续三个以上抽象名词时检查能否用一个准确动词代替。

## L5：把数据缺口接到需要观察的变化

**触发/诊断**：段落以“缺少大规模数据”结尾，但不解释现有数据缺了什么。

**操作**：先写需要观测的关系或变化，再写数据需提供的对应项，最后才报规模。区分没有此监督、覆盖不足和质量不足。

- 前：`Existing data are insufficient. We collect a large dataset.`
- 后：`Learning which scene changes accompany an edit requires corresponding observations before and after that edit. The dataset pairs these observations while keeping the unaffected scene aligned.`

**来源**：[EffectErase](paper-cards.md#b28e3c265e414c05ffd2213c) pp.1–3；[Ego-Exo4D](paper-cards.md#41ca9fbe640d4a45cca1a3e2) pp.1–3；[GigaHands](paper-cards.md#9e532d6a1fb5f3d41756fcd2) pp.1–2、5–6。**边界**：匹配/对齐质量要有依据，不能从配对文件名推导完美对应。**验收**：不报规模也能解释该数据的独特监督作用；帧、序列、片段、标注对的单位不互换。

## L6：用结果的分辨率决定动词强度

**触发/诊断**：一个指标或几个选例被写成 `proves / eliminates / universally`；或清楚的实测变化被不必要地弱化为“可能略有”。

**操作**：先写可直接观察的量，再给与设计相符的解释；只有受控比较能支持的归因才写因果。把范围嵌入结果句，而非追加防御性长段。

- 前：`The model solves temporal inconsistency.`
- 后：`On the evaluated clips, the model reduces the measured frame-to-frame error while preserving spatial accuracy.`

**来源**：[VBench](paper-cards.md#7408bccff4dcfda8985400df) pp.5–6 的维度评分；[SenCache](paper-cards.md#6462ee844611f804b8e9e9f0) p.8 的质量/计算权衡；[Dataset Distillation](paper-cards.md#f981f123b2ada842bea1db44) p.8 的反例。**边界**：后句也要求空间精度数据；没有就删掉该半句。**验收**：每个比较级能指向同协议比较；总体结论不会与表中反例冲突。

## L7：局部精简不改变信息承诺

**触发/诊断**：为消除孤行而乱添修饰词，或为压页删掉比较条件。

**操作**：优先删重复背景、重复模块清单和已经由图说明的逐步描述；可适当补充真实主语、指代或必要条件，让孤行合并。不要为了满行增加“robust / comprehensive / significant”。

**来源**：上述论文的论证组织与[版面规则](figure-design.md#篇幅与版面让空间服务论证)共同导出的编辑建议，不是全语料因果结论。**验收**：逐句对比改前改后的对象、条件、数量、方向和因果强度；均不因排版改变。保留用户限定的改动范围。

## 实际交付方式

小改动直接给改写；需要解释时只指出“哪一步缺关系→改了什么”。整段先用短标签标明各句职责，合并重复职责，再移除标签交付连续正文。已有事实不足以填补逻辑时指出那一个缺口，不用更响亮的语言遮盖。
