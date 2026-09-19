# E 题图表模式手册（`generate_charts.py` 实战沉淀）

> 样式块见 `../templates/cumcm_style_block.py`（先 import 那块再画）。
> 注释只用整块分节头（`═══ 一、…`），不用行尾小字——行尾注释是本仓库明令不学的风格。

## 模式表：场景 → 画法 → 关键参数

| 场景 | 画法 | 关键参数（照抄） |
|---|---|---|
| 分组散点（如上位占比 vs CTR，按月着色） | `scatter` 分组循环 | `alpha=0.7, s=35`，`legend(ncol=3, fontsize=8)`，`grid(alpha=0.3)` |
| TOPn 对比 | 横向条形 `barh` | 只取前 10，`invert_yaxis()` 置顶，`color="steelblue"` |
| 占比条 + 均线双轴（如消费占比 vs CPA） | `bar(alpha=0.6)` + `twinx().plot("o-")` | 双 y 轴同色标注（蓝/红），`twin_legends()` 合并图例，`set_xticks(range(1,13))` |
| 全年双轴时序（注册数 & 消费额） | `fill_between(alpha=0.4)` + `plot(linewidth=1)` | `figsize=(14,4)`，`month_axis()`，`fig.autofmt_xdate()` |
| 噪声 + 信号分层（如日 CPA + 7 日均线） | 原始线 + 滚动均线 | 原始 `gray, linewidth=0.8, alpha=0.6`，均线 `crimson, linewidth=1.8`，`rolling(7).mean()` |
| 月度分布箱线 | `boxplot(patch_artist=True)` | 中位线 `red, linewidth=2`，箱体 `Blues` 渐变（`np.linspace(0.3,0.8,12)`），`grid(axis="y", alpha=0.3)` |
| 星期效应 | 数字序 + 中文映射 | `dayofweek` 0–6 配 `周一..周日`，柱 + 双轴线，`twin_legends()` |
| 事件窗口（如节假日 ±7 天） | `axvspan(alpha=0.15, red)` + `axvline(--)` 标界 | 最长连续段定位（`diff != 1D` 分组取最大），窗口前后各延 7 天 |
| 分组柱状（月 × 类型） | `pivot.plot(kind="bar")` | 三态色 `TRISTATE` 固定映射，`width=0.7, alpha=0.85, rotation=0`，`legend(title="日期类型")` |

## 数据先行（画前算好）

- 派生指标（CTR/CPA/占比/千次转化）进 DataFrame 后再画，画图代码不做业务运算。
- 除零一律 `.replace(0, np.nan)`，不在图上藏 inf。
- 读 CSV 用 `encoding="utf-8-sig"`（防 BOM 表头错位）。

## 网格与导出纪律

- 网格二选一：全图 `grid(alpha=0.3)` 或仅 y 轴 `grid(axis="y", alpha=0.3)`，不混用。
- 每图 `tight_layout()`，双轴图 `fig.autofmt_xdate()`。
- 分级导出：150 = 草稿预览，300 = PNG 下限，600+ = 印刷终稿（见 `docs/figure-spec.md`）。
- 文件编号 `问号_序号_题义`（如 `2_1_日注册_消费_时序.png`），收尾打印清单对稿。

## 不学清单（E 题里有，技能里禁）

| E 题做法 | 为什么不学 | 替代 |
|---|---|---|
| 行尾灰色小字注释（如 `... # 0=Monday`） | 信息碎、易过期，review 时看不见 | 整块分节头 + 自解释变量名 |
| `warnings.filterwarnings("ignore")` | 掩盖警告，违反日志门禁 | 警告逐个 triage，该修修 |
| `dpi=150` 交终稿 | 低于出版下限（线图 600+） | 150 只做草稿，终稿按 spec |
| `tab10` 硬画 12 类 | 超 Okabe-Ito 8 类上限，色相撞车 | 连续渐变（Blues）或尾部合并 |
