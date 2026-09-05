---
name: publication-figure
description: "按单双栏尺寸 DPI 字体嵌入组装多子图投稿图。Use when 定稿前需合规矢量插图时。"
---
# 期刊级版式与投稿图

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: assemble panel figures that pass a journal's production checks on the first submission — size, DPI, fonts, colorblind safety, LaTeX inline. It does not draw the panels (that's `scientific-plotting` / `statistical-plot` / `diagram-schematic`) and it does not write captions' statistics (that's `figure-table-generation`).

## Operating Posture

You are the last checkpoint before submission: the person production never emails back about. The bar is the spec sheet — every number below verified against the target venue, panel labels consistent, fonts embedded, grayscale-safe. Write it so the compliance table passes the first time.

Two failure modes, and the first is worse:

1. **Assembling without the spec.** Guessed column widths, unknown DPI requirement, Type 3 bitmap fonts from an old toolchain. A figure bounced by production costs a revision cycle for a preventable line in a checklist.
2. **Panels that disagree with each other** — mixed fonts, mixed palettes, (a)(b) labels in three styles, caption citing values the panels don't show. A composite of individually fine panels can still read as three papers stapled together.

Never deliver a composite without the venue spec pinned and the compliance table filled. No spec, no assembly.

## Hard Rules

1. **Pin the venue spec first.** Column widths (single ≈ 89mm / double ≈ 183mm typical — verify per venue), max height, DPI minima (line art 600–1200, halftone 300), accepted formats (PDF/EPS/TIFF), font rules. One spec block, quoted, before any layout.
2. **Panels drawn to size, not scaled into size.** Each panel generated at its final physical dimensions with final point sizes — scaling a 6-inch figure into 89mm shrinks 9pt type to 6pt. Check type at final size, always.
3. **Fonts embedded, Type 3 forbidden.** PDF with embedded subset fonts; LaTeX text via the document's own toolchain where inline math appears. Verify with pdffonts, don't assume.
4. **One visual system across panels.** Same palette, same font family/sizes, panel labels (a), (b), (c) in one style and position logic. A composite reads as one figure or it fails.
5. **LaTeX inline test.** \includegraphics at column width, compiles clean, no overfull boxes, caption numbers match in-text citations. The figure isn't done until the document builds with it.

## The Build Sequence

### 1. Should this be journal assembly at all?

| Situation | Decision |
| --- | --- |
| Final multi-panel vector figure for submission | **Publication-figure. Continue.** |
| Single panel still being iterated | Stop. Finish it in `scientific-plotting` / `statistical-plot` first. |
| Exploration or slides | Stop. Use `plotly-interactive` or plain exports — no spec needed. |
| Schematic/flow content | Panels from `diagram-schematic`, assembled here. |

### 2. Pin spec, plan layout

- Spec block: widths, heights, DPI, formats, font rules, color policy (charges for color? then grayscale-safe is mandatory, not nice).
- Layout sketch: panel order follows the argument order in text; each panel earns its place (cut any panel the text never cites — uncited panels get flagged by reviewers).
- Caption draft started now, not after: numbers the panels must show get listed, so step 4 is verification, not discovery.

### 3. Build panels to size

- Regenerate (not screenshot, not upscale) each panel at final dimensions via its drawing skill, same style block.
- Panel labels (a)(b)(c): same font/size/weight, same corner logic, never covering data. Shared axis labels where panels share scales — repeated labels are clutter, mismatched scales are deception (state either).

### 4. Compliance — the gate

Fill the table, every row verified, not assumed:

| Check | Requirement (per spec) | Actual |
| --- | --- | --- |
| Width / height | ≤ spec | measured |
| DPI (raster parts) | ≥ spec | measured |
| Fonts | embedded, no Type 3 | pdffonts output |
| Grayscale print | readable | printed/converted check |
| Colorblind safety | palette passes | simulator check |
| LaTeX build | clean compile | log checked |
| Caption ↔ panels | every cited value visible | cross-read |
| Caption ↔ text | citations match numbers | grep checked |

Any row failing → fix and re-verify that row. A composite with one unchecked row is a draft.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Guessed venue spec | Pinned spec block, quoted |
| Scale-to-fit assembly | Panels generated at final size |
| Type 3 / unembedded fonts | pdffonts-verified embedding |
| Mixed panel styles | One palette, one font system, one label style |
| Uncited panels | Cut or cite |
| Caption written after | Drafted at layout, verified at gate |

## Output

The deliverable is the composite **plus its compliance**, in this order:

- **Figure files** — final format(s) per spec, named per figure number.
- **Spec block** — venue requirements quoted.
- **Compliance table** — filled, measured values.
- **Panel sources** — regenerating scripts per panel.
- **Caption** — cross-checked against panels and text.

Don't pad this into a report. The passing composite is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "panel (c) is never cited — cut it, the figure gets stronger", cut it. When the venue wants 600 DPI line art and the export is 150, re-export instead of hoping production won't notice.

模板文件见 assets/templates/publication-figure.tex（随本技能分发；改动前先核对 venue spec）。
