# 图幅与调色板规范（公共引用）

> 供 `scientific-plotting` / `statistical-plot` / `publication-figure` / `figure-table-generation` / `diagram-schematic` 共用，避免三处各写一遍（见自检 `docs/self-diagnosis-2026-09-06.md:3`）。

## 图幅

- 单栏约 **89 mm**，双栏约 **183 mm**，以 `publication-figure` 的 venue 核验为准（`CONTEXT.md:22`）。
- `scientific-plotting` / `statistical-plot` 终版尺寸下：标签 ≥8 pt、刻度 ≥7 pt、数据线 ≥1 pt。

## 调色板

- 分类：`Okabe-Ito`（最多约 8 类，尾部合并，见 `CONTEXT.md:30`），十六进制按项目样式块贴码。
- 连续：`viridis` / `cividis`。
- 禁用：`jet` / `rainbow` / `hsv`；红绿编码关键区分永不。

## E 题实战补充（2026-CUMCM E 题 `generate_charts.py` 沉淀）

- 中文字体链：`SimHei → Microsoft YaHei → PingFang SC → Noto Sans CJK SC → Arial Unicode MS → DejaVu Sans`，`axes.unicode_minus=False`。模板见 `skills/scientific-plotting/assets/templates/cumcm_style_block.py`，模式表见 `skills/scientific-plotting/assets/references/etime-patterns.md`。
- 语义色跨图复用不换义：主体 `steelblue`、强调 `crimson`、次强调 `darkorange`、占比 `coral`、噪声 `gray`（细淡只衬托）；三态场景固定 `#e74c3c/#3498db/#f39c12`。
- 网格二选一：全图 `alpha=0.3` 或仅 y 轴，不混用。

## 导出校验

- 矢量 `PDF`/`SVG`，字体嵌入（`pdffonts` 验证），`DPI ≥300`（预览）/`600`（印刷）按 `publication-figure` 规格块声明。
- `DPI 150` 只做草稿预览，不交终稿；文件编号 `问号_序号_题义`，收尾打印清单对稿。
