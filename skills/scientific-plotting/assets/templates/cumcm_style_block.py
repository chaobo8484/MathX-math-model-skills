"""cumcm-style-block.py — 国赛 Matplotlib 样式块（E 题实战沉淀）

用法：在绘图脚本头 `from cumcm_style_block import twin_legends, month_axis, savefig`
（文件随稿走，`import` 那块，见 scientific-plotting Hard Rules 1）。
本块只定风格与导出，不碰数据；派生指标（CTR/CPA/占比）先算好，
除零用 `.replace(0, np.nan)`，CSV 用 `encoding="utf-8-sig"` 读（防 BOM）。

字体链按平台自动降级：Windows 走 SimHei；macOS/Linux 用系统现有黑体，
全缺时 DejaVu Sans（中文变方框即缺字体，先装字体再画）。
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---- 字体与字号（终版尺寸验收：标签>=9pt、刻度>=8pt、数据线>=1pt）----
plt.rcParams["font.sans-serif"] = [
    "SimHei", "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC",
    "Arial Unicode MS", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.titlesize"] = 11
plt.rcParams["axes.labelsize"] = 9
plt.rcParams["xtick.labelsize"] = 8
plt.rcParams["ytick.labelsize"] = 8
plt.rcParams["legend.fontsize"] = 8
plt.rcParams["lines.linewidth"] = 1.2
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["figure.autolayout"] = False  # 用显式 tight_layout，逐图验收

# ---- 色板：分类 Okabe-Ito（<=8 类，尾部合并）；连续 viridis ----
PALETTE_OI = [
    "#0072B2", "#E69F00", "#009E73", "#CC79A7",
    "#56B4E9", "#D55E00", "#F0E442", "#000000",
]

# ---- 语义色（E 题验证过的一套，跨图复用不换义）----
# 主体柱/面/主线、强调均线关键线、次强调金额线、占比条、噪声细淡只衬托
SEMANTIC = {
    "main": "steelblue",
    "accent": "crimson",
    "warm": "darkorange",
    "soft": "coral",
    "neutral": "gray",
    "median": "red",
}
# 三态语义（假日/工作日/调休类场景照抄，勿自创映射）
TRISTATE = {"放假": "#e74c3c", "正常": "#3498db", "调休": "#f39c12"}


def twin_legends(ax1, ax2, **kw):
    """双轴图合并图例（E 题 1-3/2-1/2-4 模式）。"""
    kw.setdefault("fontsize", 8)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    return ax1.legend(h1 + h2, l1 + l2, **kw)


def month_axis(ax, fmt="%m-%d"):
    """全年时序横轴：按月定位、日月格式、防重叠。"""
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))


def savefig(fig, stem, formats=("pdf",), png_dpi=300):
    """按输出格式门禁导出（默认论文 PDF；PNG 预览 >=300dpi）。

    每图 tight_layout 后逐个验收：字体渲染、灰度可读、标签无裁切。
    收尾打印文件清单（E 题 generate_charts.py 末尾做法）。
    """
    import os

    fig.tight_layout()
    outs = []
    for fmt in formats:
        path = f"{stem}.{fmt}"
        kw = {"dpi": png_dpi} if fmt == "png" else {}
        fig.savefig(path, **kw)
        outs.append(path)
    return outs
