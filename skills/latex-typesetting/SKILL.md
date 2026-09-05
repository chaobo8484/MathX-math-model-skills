---
name: latex-typesetting
description: "把内容填入官方 LaTeX 模板并编译出 PDF，按报错日志迭代修错。"
disable-model-invocation: true
---
# LaTeX 排版与模板填充

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

人触发的生产型技能，只做一件事：官方模板分块填内容，对编译日志迭代到干净 PDF。不设计论文逻辑（那是 `paper-outline`），不画图（那是 `publication-figure` / `figure-table-generation`）。

## Operating Posture

用户键入时运行，模板和内容在手。产品是编过的文档加报错日志的解决轨迹。标准是干净构建：零错误、要紧警告零残留、PDF 100% 目检过。

两种失败模式，第一种更糟：

1. **动模板骨架。** 改 class 的边距字体标题样式来“修”版式。骨架是 venue 的法——版式疼靠删内容解决，不靠换风格。
2. **警告瞎。** 编一次，40 个警告不看，发货。未定义引用挂 [?]、引用挂 [?]、overfull 框把字顶进边距——个个都在日志里。

无干净日志声明不交 PDF。警告没过目，文档没完工。

## Hard Rules

1. **骨架冻结。** 模板 class、前导区结构、样式文件，除内容占位不动。骨架任何改动先回滚，或先经用户明确同意。
2. **一块一编译。** 填一节（或一图/一表插入），编译，读日志，修，循环。第一次编译前全篇倒进去，60 个错无地图。
3. **日志自上而下，先修第一个错。** LaTeX 级联——第一个错生出后面二十个。按序修，重编，循环。错误数下降是进度指标。
4. **占位跟踪，一个不留。** 模板 TODO、dummy、lorem ipsum——交付前 grep。投稿版里活着的占位是没读过文档的自证。
5. **图/表走文件，永不粘贴。** \includegraphics/\input 指版本化资源；宽度相对（\linewidth 分数），绝不用跨模板即碎的绝对英寸。

## The Production Sequence

### 1. 填前盘点

- 模板名 + 版本，编译器（pdfLaTeX/XeLaTeX/LuaLaTeX——中文内容通常 XeLaTeX），文献系统（BibTeX/biblatex + 样式），占位清单 grep 摘出。
- 空模板基线先编过：内容进来前必须干净构建。基线坏了赖内容，整轮白费。

### 2. 分块填

- 顺序：front matter → 按大纲节 → 浮动体（图/表文件齐了才进）→ 文献 → 附录。每块一编。
- 数学：display 公式被引用才编号；标签命名空间（fig:/tab:/eq:/sec:）；交叉引用 \ref/\cref，永不手写数字。

### 3. 杀日志——gate

- **gate**：全构建（含 bibtex/biber 若干遍）零错误收尾；剩余警告逐个 triage（overfull > 5pt 修，未定义引用归零，字体替换认领）。
- 100% 目检：浮动体位置合理，无 widow/orphan 扎眼，题注编号连续，PDF 元数据（标题/作者）设好。

### 4. 移交

- PDF + 日志摘要 + 剩余风险备注（如“图 3 终版尺寸要重导出”）。下步：引用不干净去 `citation-bibliography`，文字去 `polish-proofread`，门禁去 `reproducibility-checklist`。

## Never Ship

| 禁忌 | 替代 |
| --- | --- |
| 改骨架风格 | 删内容适配 |
| 整篇第一次编译 | 一块一编译 |
| 先修第 34 个错 | 自上而下，先修第一个 |
| 占位活到交付 | grep 清零再交 |
| 图宽绝对值 | 相对 \linewidth 分数 |
| 警告不读 | 逐个 triage |

## Output

- **PDF**——干净构建，目检过。
- **日志轨迹**——踩过的错和修法，警告 triage。
- **占位 grep**——零残留，证据展示。
- **移交**——下个技能点名。

## Tone

立场鲜明、废话少。当正确答案是“模板没病——你这节超 3 页，删”就直说。日志 12 个 overfull 框，修框，不要零错误就宣布胜利。

模板文件见 assets/templates/latex-typesetting.tex（随本技能分发；改动前先核对 venue spec）。
