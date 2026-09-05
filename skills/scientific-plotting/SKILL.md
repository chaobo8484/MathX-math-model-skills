---
name: scientific-plotting
description: "Matplotlib/Seaborn 色盲安全静态矢量图。Use when 需折线柱状散点直方箱线等投稿插图时；带统计推断标注走 statistical-plot。"
---
# 科学绘图基座

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: produce a colorblind-safe static vector figure from Matplotlib/Seaborn that survives print and projection. It does not do statistical inference display (that's `statistical-plot`), interactivity (that's `plotly-interactive`), or journal assembly (that's `publication-figure`).

## Operating Posture

You are a plotting craftsperson: one style block, one figure, reproducible from code. The bar is print-proof — readable in grayscale, legible at column width, vector output with fonts embedded or noted. Write it so the figure regenerates byte-identically from the script.

Two failure modes, and the first is worse:

1. **Defaults-as-design.** Matplotlib defaults (thin lines, tiny fonts, jet rainbow) projected in a defense or printed two-column are illegible. Defaults are a starting point the author abandoned, not a style.
2. **Raster where vector belongs** — PNG screenshots in papers, 72-dpi exports, transparent backgrounds turning black in print. A figure that degrades in the proceedings failed its job.

Never deliver a figure without its style block and vector export. No script, no figure.

## Hard Rules

1. **One style block per project, reused.** rcParams set once (font family/size, line widths, tick direction, grid style, savefig dpi/bbox). Copy-pasting style lines per figure guarantees drift — import the block.
2. **Colorblind-safe palette, always.** Okabe-Ito for categories (max ~8; group the tail), viridis/cividis for continuous. Jet/rainbow/hsv never. Red-green encoding of critical distinctions never.
3. **Type sizes in points, checked at final size.** Axis labels ≥ 8pt, ticks ≥ 7pt at column width; line widths ≥ 1pt (data) / 0.5pt (grid/axes). If it needs a magnifier at 100%, it's wrong.
4. **Axes honest.** Zero-based bars; labeled units on every axis; no dual axes without a stated reason and matching baselines; legends outside the data region, never covering points.
5. **Vector out, raster only on purpose.** PDF/SVG for papers; PNG only for slides/web at ≥ 300 dpi with the dpi stated. Random seeds fixed where jitter/sampling is involved.

## The Build Sequence

### 1. Should this be static plotting at all?

| Situation | Decision |
| --- | --- |
| Line/bar/scatter/hist/box for paper or 国赛 | **Scientific-plotting. Continue.** |
| Must show N, p-values, CIs, test choices | Route the spec through `statistical-plot`, draw here. |
| Exploration needs zoom/hover, or 10k+ points | Stop. Use `plotly-interactive`. |
| Final multi-panel journal assembly | Draw panels here, assemble in `publication-figure`. |

### 2. Set the style block

- Font: one family project-wide (DejaVu Sans / Arial / Times per venue), sizes fixed: title 10–11pt, labels 9pt, ticks 8pt, legend 8pt.
- Lines: data 1.2–2pt, axes 0.8pt, grid 0.4pt light or off. Markers sized to survive print (≥ 4pt), edge colors where overlap.
- Palette line: Okabe-Ito hexes pasted in code, or viridis for continuous. Background white; transparent=False for print exports.

### 3. Map data to ink, minimally

- One message per figure. Second message → second panel or second figure, never a twin-axis collage.
- Ink budget: remove chartjunk (3-D, gradients, heavy grids, box frames on all sides — top/right spines off by default).
- Direct-label lines where readable; legend only when direct labels collide. Annotate the value the text cites (arrow + number), so figure and prose agree.

### 4. Export and verify — the gate

- Save PDF (papers) + PNG@300dpi (preview). **Gate**: open the PDF at final size, check fonts render, grayscale-print test readable, no clipped labels (bbox_inches='tight' verified, not assumed).
- Script + data version noted beside the file. A figure without its generating script is uneditable — treat as draft.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Default style throughout | Project style block, reused |
| Jet/rainbow or red-green critical encoding | Okabe-Ito / viridis |
| < 7pt type at final size | Point sizes checked at column width |
| Truncated bar axis | Zero-based or chart-type change |
| PNG-only for a paper | PDF/SVG + 300dpi preview |
| Legend over data | Outside or direct labels |
| Clipped labels in export | bbox verified in the opened PDF |

## Output

The deliverable is the figure **plus its recipe**, in this order:

- **Figure files** — PDF (+ preview PNG), named per caption number.
- **Script** — data → style block → plot → export, seed noted.
- **Style record** — palette hexes, font/size/width table.
- **Verification** — final-size check, grayscale check, caption draft with N and units.

Don't pad this into a report. The figure + script is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "this needs two panels, not twin axes", give it. When the palette holds 12 indistinguishable colors, group the tail instead of negotiating with the rainbow.
