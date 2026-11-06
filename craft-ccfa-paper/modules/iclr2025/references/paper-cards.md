# ICLR 2025 样本论文卡片

快照：2026-09-18。以下是目的性选样，不代表 3,705 篇的统计随机样本。12 篇均含指定图的人工视觉核验（合计 17 个带编号的图），后六篇正文阅读仍是选段；每卡单独声明阅读边界。全部描述为合作论文中可观察的写作与实验结构，不推断个人作者的私下构思过程。


## 01. Differential Transformer

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/00b67df24009747e8bbed4c2c6f9c825-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/00b67df24009747e8bbed4c2c6f9c825-Paper-Conference.pdf)

**已读范围**：正文 p.1–4；实验 p.4–9 部分段落；未通读附录。人工查看 p.3 Fig.2。

**论证与章节**：Introduction 从注意力噪声建立问题；§2 将双 softmax 差分写成具体运算，并说明 λ 参数化和 head normalization；§3 分开说明语言建模、缩放及长上下文等测试。继承的 decoder、RMSNorm 和 SwiGLU 不应算成新增模块。
**模块与实验**：双分支不是两套独立大模型；输出与归一化位置要对应公式。匹配实验使用不同 head 数保持模型规模／FLOPs，不能仅按 head 数判断预算公平。公开 1T token 模型比较与自训 350B token 比较分开引用。
**图**：Fig.2 左侧自下而上的算子图、右侧等价伪代码共同解释计算。颜色只辅助区分操作；Q/K/V、λ、归一化和拼接的名称应与公式一致。
**迁移与边界**：适合“诊断—最小算子修改—机制与能力验证”。缩放拟合不能写成普遍定律；训练条件不同的横评不能单独证明架构因果优势。


## 02. SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9622163c87b67fd5a4a0ec3247cf356e-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/9622163c87b67fd5a4a0ec3247cf356e-Paper-Conference.pdf)

**已读范围**：Introduction p.1–3；judge 与评测 p.6–10；数据细节 p.4–5 未完整研读。人工查看 p.2 Fig.1。

**论证与章节**：先用已有数据集类别分布说明覆盖不均，继而构造 taxonomy 与数据；§3 定义是否满足请求，再校验评测器；后续才给模型排名与语言变体结果。
**数据与实验**：44 类、440 条均衡基础请求；20 类语言变体产生额外 8,800 条。7,040 条人工标注用于 judge 研究，训练 2,640、测试 4,400；需要保留模型内／外分组。Table 1 将一致性、Cohen κ 和成本并列，不能只用 judge 自己的分数证明 judge 可靠。
**图**：Fig.1 将 10 个已有数据集映射到相同 44 类体系，按类别比较覆盖；分母、映射规则和纳入集合决定能得出的结论。
**迁移与边界**：适合“测量定义—覆盖—测量工具有效性—模型行为”。56 个模型的基础测试不等于所有模型都测过所有变体；无法理解编码导致不满足请求，不自动等于安全能力。模板、解码参数与版本均是协议。


## 03. Framer: Interactive Frame Interpolation

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/801ec05b0aae9fcd2ef35c168bd538e0-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/801ec05b0aae9fcd2ef35c168bd538e0-Paper-Conference.pdf)

**已读范围**：正文 p.1–10 主要内容；未完整研读附录。人工查看 p.4 Fig.2。

**论证与章节**：端点插帧具有多解性，因此引入用户关键点轨迹与 autopilot。§3.1 解释端帧条件，§3.2 解释控制分支，§3.3 解释推理时轨迹更新；§4 分别比较效果、消融和失败。
**模块与实验**：控制分支复制 encoder 并通过 zero convolution 注入。训练总览的 finetune U-Net 必须与 §4.1 对齐：第一阶段更新输入卷积和时间注意力，而非所有 U-Net 层；之后冻结相应底座、训练控制器。GT CoTracker 轨迹行有额外信息，不能与 autopilot 条件混为公平输入比较。
**图**：Fig.2 左侧用户／自动控制示例，右侧框架；冻结底座与控制分支可区分。面板 (d)/(c) 的叙述顺序涉及训练阶段，排版顺序本身不等于执行顺序。
**迁移与边界**：适合“需求歧义—可操作控制—训练状态—控制效果与代价”。Table 1 的 PSNR/FID/FVD 并非处处同时最好；§4.5 缺失语义／对应关系的失败应进入能力边界。作者的 suspect/believe 解释保留假设语气。


## 04. Generalization and Distributed Learning of GFlowNets

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/000eba875068854d5ff003b1fa534cd6-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/000eba875068854d5ff003b1fa534cd6-Paper-Conference.pdf)

**已读范围**：摘要、Introduction、§3 结果概览及 p.6–10 部分定理、算法与讨论；未核验完整证明。人工查看 p.9 Fig.3 与相邻 Algorithm 1。

**论证与章节**：以常见泛化判断及反例开场，即使观察很多状态仍可能失败；§3 先给结果地图，§4 展示失败，§5 建立数据依赖界，§6 从轨迹／状态规模问题导出 SAL 分布式算法。
**理论与模块**：Theorem 5.4 包括 DB loss 的一致界 U、鞅界 K、λ 限制和独立轨迹等条件，涉及数据依赖 posterior；不能省去假设后直接引用结论。SAL 在局部叶子问题训练，再聚合 root reward。
**图**：Fig.3 用颜色标识 DAG 子图，与 Algorithm 1 相邻；图中推理采样结构与算法的训练流程需要分别解读，不能用箭头暗示未经定义的更新顺序。
**迁移与边界**：适合“反例—有条件保证—算法”。固定 wall-clock 比较按最慢 client 加聚合时间定义。Recursive SAL 的合理性讨论不是已完成实验，专业 NLP／药物场景的设想不是本论文验证结果。


## 05. Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/12678c3948153f4bc391f51e2082bd6e-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/12678c3948153f4bc391f51e2082bd6e-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1–2，方法 p.4–5，实验 p.6–8 部分；未完整研读附录。人工查看 p.2 Fig.1。

**论证与章节**：离散文本与连续图像各自的目标不同，先定义表示与损失接口，再解释共享 Transformer，随后分开讲训练、推理和受控比较。
**模块与实验**：文本 next-token prediction 与图像 diffusion 共享主干，但不能把目标或输入可见性写成相同。推理是 LM→BOI→扩散→EOI→LM 的状态切换。Table 3 将 linear/U-Net 适配器与 causal/bidirectional 方式交叉比较；与公开最大模型横评是不同证据层。
**图**：Fig.1 通过输入／输出序列位置、共同主干和边界 token 解释统一接口；详细 attention mask 由 Fig.4 承担，不要把 Fig.1 说成完整掩码定义。
**迁移与边界**：适合“异质表示—共同接口—模态特定目标—交叉消融”。相对纯文本 Llama 的能力损失需要如实保留，作者给出的原因不全是已证机制。


## 06. OmniEdit: Building Image Editing Generalist Models Through Specialist Supervision

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0113ef4642264adc2e6924a3cbbdf532-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/0113ef4642264adc2e6924a3cbbdf532-Paper-Conference.pdf)

**已读范围**：Introduction p.2–3，方法 p.4–5/7，实验 p.9–10；p.6/8 未完整研读。人工查看 p.7 Fig.4。

**论证与章节**：从编辑技能、质量和长宽比三个缺口推导数据构建与模型设计；Fig.2 组织数据管线，方法与训练之后评测，Related Work 位于 §6，说明章节顺序并非固定。
**模块与实验**：专家 proposal q_s 与重要性权重 λ 是数据构建解释，评分近似不等于准确求得真实密度比 p/q。EditNet 复制 DiT blocks、与冻结原模型交互，并处理文本条件；数据筛选与随机等量数据比较、同数据下架构比较分别支撑不同主张。
**图**：Fig.4 将 EditNet、ControlNet、channel concatenation 三个结构按输入层级对齐，以冻结／训练符号和信息流展示区别。自动提取曾漏掉该图，因此不能把机器图数当成全图覆盖证明。
**迁移与边界**：适合“数据与架构共同贡献但分别归因”。1.2M 训练数据与最初约 50 prompts 的动机测试作用不同；底座 SD3 的能力限制不能用编辑模块效果掩盖。


## 07. Kinetix: Investigating the Training of General Agents through Open-Ended Physics-Based Control Tasks

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/936ce22b767cf1a1496083e4725d3b21-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/936ce22b767cf1a1496083e4725d3b21-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1–3，任务定义 p.5，微调 p.8，讨论 p.10 及章节标题；未完整研读正文／附录。人工查看 p.2 Fig.1。

**论证与章节**：先给环境生成空间和高效模拟条件，再定义预训练任务分布；§5 零样本与 §6 微调分开回答迁移问题。
**实验逻辑**：人类设计的 74 个 holdout levels 不参与训练，但仍在训练分布支持内，不能改写成严格分布外泛化。随机任务有质量差异；no-op rejection、不可解任务与 curriculum 会改变有效训练分布。
**图表文字解读**：Fig.5 caption/正文给出 5 seeds 的均值及标准误；MuJoCo-like 任务是 Kinetix 内重实现，不能当成直接在原 MuJoCo benchmark 上的结果。Fig.5 本身未人工视觉核验。
**迁移与边界**：先定义环境、成功标准与 holdout 方式，再谈通用智能。Thruster-Large-Obstacles 上微调更慢的例外保留，不能把平均优势扩展为所有任务。

**人工看图补充**：Fig.1 用虚线分隔随机训练环境与手工测试环境，底部统一目标给出绿／蓝／红物体的语义。迁移时借鉴“训练集合—测试集合—共同任务定义”，但测试集独立仍需协议证明，不能仅凭分隔线宣称分布外。

## 08. Proteina: Scaling Flow-based Protein Structure Generative Models

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/f4e9121ad30cd4e5528042fbfd835b3f-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/f4e9121ad30cd4e5528042fbfd835b3f-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1–2，p.6 架构／采样、p.7 指标及后部部分段落、章节标题；未完整研读方法／实验。人工查看 p.6 Fig.5。

**论证与章节**：§3.1 数据、§3.2 目标、§3.3 架构、§3.4 采样、§3.5 分布评测将“生成什么—怎样训练—怎样生成—怎样量化”分开。使用 scalable flow 生成蛋白骨架，可选 triangle layers 与 CATH 层级条件承担不同功能。
**实验逻辑**：大规模合成结构、参数规模、长链生成和条件控制属于不同证据轴，不能仅用样本图论证全部。fold guidance 改变结构类型也可能影响多样性。
**迁移与边界**：科学应用应分别记录计算代理指标、结构有效性、分布覆盖与实际实验验证；可设计性评估不等于湿实验功能验证。本卡不提供未完整核验的指标公式；作者标注 core contributor 也不自动证明共一身份。

**人工看图补充**：Fig.5 上排 (a)–(c) 分别构造 sequence、condition、pair 三路表示，(d) 展示主处理栈，底排 (e) 展开注意力与 transition；颜色在概览与展开中保持表示对应。optional triangle/pair updates 有明确标签。§3.5 的 FPSD、fJSD、fS 使用 fold classifier 表示／预测，补充 designability 指标，但同样有代理模型依赖。

## 09. Standard Gaussian Process is All You Need for High-Dimensional Bayesian Optimization

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ec9b2a6ad5444caeff75efaa6176b3e4-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/ec9b2a6ad5444caeff75efaa6176b3e4-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1–2，p.6–7 梯度诊断／初始化与 Lemma 5.1，p.10 结果／结论；未核验完整理论证明。人工查看 p.6 Fig.1–2。

**论证与章节**：先质疑“标准 GP 必然不适合高维 BO”的笼统判断，再定位 kernel 和 lengthscale 初始化引发的梯度问题；§4 理论、§5 robust initialization、§6 评测顺序保持机制依赖。
**实验逻辑**：12 个、30–1003 维 benchmark 的比较用于检验解释范围。默认 Matérn 在多个任务有效，但最高维案例例外；更大初始化对两种 kernel 的作用应按论文协议引用。
**迁移与边界**：适合“重新审计强基线—定位默认设置故障—最小修正”。不为凑创新模块而复杂化方法；按迭代数的收益不是 wall-clock 加速。若要引用具体收敛保证，需回到原文核验完整假设。

**人工看图补充**：Fig.1 按列区分任务 × kernel，按行对齐 MSE、lengthscale 改变、梯度范数，颜色与 marker 表示初始化；Fig.2 沿 BO 迭代检查诊断量。部分值低于绘图范围而未展示，caption 说明，不能把缺失线当作未运行。Lemma 5.1 的初值是 ℓ₀=c√d，假设输入为 [0,1]^d 上独立均匀抽样并限制 c 与阈值 τ；不要扩成任意输入分布的保证。

## 10. Data Scaling Laws in Imitation Learning for Robotic Manipulation

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/88b7b2c896506daabc8d3fd587055167-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/88b7b2c896506daabc8d3fd587055167-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1，approach p.3–4，p.7–8 拟合／收集策略，p.10 模型实验与限制；未完整研读全部实验。人工查看 p.7 Fig.4–5。

**论证与章节**：§4 拟合经验规律，§5 用新任务验证数据收集策略，§6 研究模型规模，§7 讨论限制。关键是在数据总量之外区分环境数 M、物体数 N、每组合示范数 K。
**实验逻辑**：UMI 与 Diffusion Policy 及编码器／temporal ensemble 选择构成实际协议；发现规律的任务和验证策略的 Fold Towels、Unplug Charger 两个任务分开。针对同类物体／新环境的单任务迁移，不能写成多任务通用策略。
**迁移与边界**：适合“分解资源轴—控制采样—经验拟合—独立任务决策验证”。power law 是给定数据范围下的经验近似，不能把总数据量作为唯一因果变量，也不能把外推写成理论保证。

**人工看图补充**：Fig.4 先呈现两个任务的原始性能曲线，Fig.5 再以“任务为行、对象／环境／组合为列”组织 log–log 拟合，点和虚线区分观测与拟合。§4.2 脚注明确只有 6 个数据点，故不拟合含不可约误差的三参数模型；不要只学曲线外观而丢掉拟合限制。预测 1,191 个环境–物体对属于尚待验证的外推。

## 11. Retrieval Head Mechanistically Explains Long-Context Factuality

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9b77f07301b1ef1fe810aae96c12cb7b-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/9b77f07301b1ef1fe810aae96c12cb7b-Paper-Conference.pdf)

**已读范围**：Introduction p.1–3，p.7 干预、p.9 讨论；未完整研读全部实验／附录。人工查看 p.7 Fig.6–9。

**论证与章节**：§2 将 retrieval head 变成可测的 token copying score，§3 研究分布与属性，§4 用干预和下游任务检验作用，§5 讨论解释范围。
**实验逻辑**：attention 可视化只建立观察；mask top-K heads 与等量随机 heads 的控制比较更接近因果验证。头部筛选所用的 NIAH 任务和下游 factuality 任务不能混写成同一协议。
**迁移与边界**：适合“现象—操作性定义—控制干预—下游验证”。已测模型家族的共性不能扩成所有 LLM 的定律；检索机制解释不等于完整解释 hallucination 或推理能力。

**人工看图补充**：Fig.6 相关性热图是观察证据；Fig.7 用颜色区分模型、实虚线区分 retrieval/random masking，支撑控制干预；Fig.8 检查下游，Fig.9 给出失败实例。四类图在同页承担不同证据任务。Fig.8 的 y 轴从约 30 起而非 0，改画柱图时优先零基线，避免视觉夸大差异；不盲目复制样本所有排版选择。

## 12. Cut Your Losses in Large-Vocabulary Language Models

[官方论文页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/aa963ac256590bb7ad5fc26c68229a3a-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/aa963ac256590bb7ad5fc26c68229a3a-Paper-Conference.pdf)

**已读范围**：摘要、Introduction p.1–3，p.4 运算分解，backward p.6，稳定性 p.9，讨论 p.10；未完整研读全部数值表。人工查看 p.4 Fig.2。

**论证与章节**：从词表交叉熵内存瓶颈定位到 logits 不必全局物化的代数计算，再分别解释 forward、recompute backward、梯度过滤和词表排序，最后检查速度与训练稳定性。
**实验逻辑**：局部交叉熵 kernel、classifier head、端到端训练的内存／时间是不同分母。过滤与精度会改变稳定性：初始 CCE 的预训练 validation perplexity 变差，CCE-Kahan-FullC 通过补偿求和并不滤 classifier gradient 修正；微调成功不能推出朴素方案预训练稳定。
**迁移与边界**：适合“瓶颈—代数等价—硬件访存—数值误差—完整训练”。§5.3 的受限 OpenWebText 训练验证范围不代表所有规模。实现讨论涉及 Triton，不据此推断作者画图工具。

**人工看图补充**：Fig.2 的 (a) indexed matmul、(b) LSE forward、(c) backward 与 Algorithms 1–3 对应；矩阵块着色表示当前访问位置，实线／虚线、atomic add 与过滤条件解释数据流。图与公式共用 C、E、LSE 的颜色和符号；适合展示访存和重算，不适合改成无具体运算的三个大方框。
