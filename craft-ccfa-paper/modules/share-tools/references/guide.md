# 正文—框架图交接与增量工具

这是 `craft-ccfa-paper` 的内部工具模块，取自用户提供的分享包。沿用统一写作、Mayue 案例、review 和 anti-defensive 流程；只在需要下面的功能时读取。本模块不是另一套论文标准。

## 先复用已有事实来源

优先使用项目已有的权威方法／实验记录和命名表。不搬目录、不因调用工具另造实验账本。若现有 Markdown 已有 `## Modules` 下的 `Name`、`Aliases` 列，以及 `- Name: 方法名`，可直接交给名称检查器。

没有对应记录、且多章节或正文与图需要交接时，可从 [最小事实模板](facts-template.md) 建立 `paper/facts.md`（或用户指定位置）。它只记录必要的方法、名称和状态，实验事实链接原始记录及 Run。不能把原始日志和结果复制成第二份可独立改写的事实。

名称变更先更新权威命名表，再同步正文、公式、图和消融。短标签用已声明的别名。参数是否冻结与组件是否新增是两种属性，分别记录；training-free、缓存和推理优化仍按主技能核对。

`Figure.save(..., facts=...)` **会写事实文件**：替换该图的 `<!-- figure:标题:start -->` 到 `end` 注释块，记录 `schematic()` 声明。已有事实表只读或归其他 writer 时省略 `facts`，由 `labels.json` 提供说明。图注同时核对示意说明和素材来源；“未声明示意”不证明素材是真实结果。

## 可选的章节形式诊断

以下路径相对主技能根目录；在项目中执行请使用解析后的绝对路径：

```bash
python modules/share-tools/scripts/check_section.py abstract /path/to/abstract.tex
python modules/share-tools/scripts/check_section.py intro /path/to/intro.md --json
```

支持 `title/abstract/intro/related/method/experiments/conclusion`，只需 Python 标准库。它做浅层 LaTeX 清理、词数和关键词检查；不能正确解析任意 TeX 宏、验证引用或证明科学主张。`OK` 仅表示某个形式检查命中。

合法输入即使有 `WARN` 也返回 0。样本字数、标题冒号、主题数和贡献条数是诊断线索，不是验收门槛；会议规则与实际论证优先。不因原样本较少使用数字而删除有依据的摘要／结论数字。短摘要、理论论文或合并 Related Work 不需为消除提示改写结构。

原包各章有用的组织操作已并入现有写作路线：方法依赖和实验先稳定，再压缩摘要及标题；引言把具体缺口接到机制；模块说明覆盖目的、操作、接口、状态与验证；图注按真实面板顺序解释符号。贡献条目与模块保持可追踪关系，**不要求条数一一相等**，不强制二分路线、固定公式数或连接词。

## 正文与图的名称检查

```bash
python modules/share-tools/scripts/check_terms.py /path/to/facts.md \
  --text method=/path/to/method.tex --text abstract=/path/to/abstract.tex \
  --figure /path/to/labels.json
```

- 接受登记的全名、别名和大小写差异；空格／连字符漂移报 `FAIL`，相近拼写报 `WARN`。这是字符串诊断，提示需结合上下文核对，不能用机械替换改变技术含义。
- 默认仅对 `method` 和图中未出现的模块提醒；摘要、引言、结论可以只说关键模块。
- 只有核对**完整方法或完整总图**时，按实际范围加 `--require-in method --require-in figure`，将该范围内缺失的登记模块判为 `FAIL`。局部图、损失细节图和单段不默认要求列全模块；必要时用只包含该图相关模块的现有命名视图。
- 没有输入、事实表不符合上述列格式或必查范围没有输入时报告输入错误。不会替用户修正文档。

退出码 0 表示没有 `FAIL`，1 表示名称不一致／明确要求的模块缺失，2 表示 CLI 或事实表格式错误。它无法验证算子依赖、参数状态或实验结论。

## 程序化框架绘图

`scripts/figkit.py` 可组合视频叠帧、图像、编码器、网络层、模块容器、状态图标、公式和连线，输出可独立打开的 HTML、可编辑 SVG、矢量 PDF、PNG 与 `labels.json`。HTML／`framework.svg` 保留可编辑文字；PDF 与额外的 `framework-outlined.svg` 将标签转为所附字体的矢量轮廓，避免平台替换字体，PDF 中的标签不能按普通文字编辑／搜索。Python 绘图源和原始素材必须一并保留。它不是根目录 JSON renderer 的输入，也不提供原生 PPTX 转换。

依赖在 `requirements.txt`。选择已有环境或项目虚拟环境安装，避免修改系统 Python：

```bash
python -m pip install -r /absolute/skill/modules/share-tools/requirements.txt
python /absolute/skill/modules/share-tools/examples/minimal/build.py --output /project/work/figure-demo
```

绘图及静态导出需要 Pillow、Matplotlib 和 CairoSVG；还需要系统 Cairo。macOS 上已安装 Homebrew Cairo、但自带 Python 找不到动态库时，可为**该次命令**设置 `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`（Intel 路径按实际安装位置调整）；不要把找不到 Cairo 当作绘图验收通过。该环境修正不需要改全局 shell 配置。

最小使用：

```python
import sys
sys.path.insert(0, '/absolute/skill/modules/share-tools/scripts')
from figkit import Figure

f = Figure(1200, 400, 'Method overview', print_width_in=6.7, base=24)
a = f.block(50, 100, 300, 160, 'Input representation')
b = f.block(700, 100, 400, 160, 'Registered Module', state='fire')
f.arrow(a.right, b.left)
f.legend(700, 290, [('fire', 'Trainable')])
f.schematic('Entire figure', 'conceptual architecture; no measured results shown')
f.save('/project/figures/overview')
```

将尺寸、拓扑和模块名改成真实方法；`print_width_in` 决定 PDF 的实际宽度和字号检查。示例的 6.7 英寸不是所有会议的栏宽。默认字号提醒下限为 7 pt，仍需以当前模板和实际可读性检查。`load_image(path, size)` 会中心裁方并缩放：证据图应先按可复核的裁剪协议处理，不用隐式裁剪隐藏失败区域。

样式组件和可选布局见 [visual vocabulary](visual-vocabulary.md)。图标表示图例明确的状态；新增模块不必是 temporal 层，DiT 不应画成假 UNet。没有真实素材时可交付明确标注的概念草图，不能伪造结果或把占位图当最终证据。

先逐箭头核对计算，再看 lint 与最终栏宽预览。Lint 检查文字／边框／直线相交、图例和字号；弯曲箭头、zoom 线及样例真实性需人工检查。`strict=True` 只将绘图提示转为失败，不能证明布局或科学语义正确。

## 回归与来源

```bash
python modules/share-tools/tests/test_handoff.py
python -m unittest discover -s modules/share-tools/tests -p 'test_integration.py' -v
```

交接测试需要绘图依赖，集成测试另需 `pypdf`（`tests/requirements.txt`）。它们验证名称／别名、完整与局部范围、事实注释交接、导出尺寸和环境清理；不替代实际论文审稿。来源、原包统计和集成调整见 [source evidence](source-evidence.md)。
