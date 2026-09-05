---
name: plotly-interactive
description: "缩放悬停联动的 Plotly 探索图。Use when 数据探索需交互或上万点需 WebGL 时；定稿矢量图走 scientific-plotting。"
---
# 交互式 Plotly 图表

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: build a zoom/hover/linked Plotly chart for data exploration — light spec, fast load, honest about what was sampled away. It does not do print figures (that's `scientific-plotting`) or journal assembly (that's `publication-figure`).

## Operating Posture

You are building an instrument, not an illustration: the user will interrogate data through it. The bar is responsiveness with provenance — hover shows values with units, every filter/aggregation stated, downsampling disclosed on the chart. Write it so the file opens fast on a cold load.

Two failure modes, and the first is worse:

1. **A 40-MB HTML "exploration".** Full-resolution millions of points inline, frozen browser, unshareable file. An interactive chart nobody can open is a failed export with buttons.
2. **Silent aggregation.** Downsampled, binned, or filtered data presented as the raw data. Exploration on hidden transforms produces discoveries about the transform.

Never deliver an interactive chart without its data budget line (N shown vs N total, method). No budget line, no chart.

## Hard Rules

1. **Point budget: ~10k SVG, WebGL beyond.** Under ~10k points standard traces are fine; above it use scattergl (or datashader-style raster + hover) — decided by count, not by hope.
2. **Downsampling disclosed on the chart.** Method named (stratified/random/every-kth, seed where random) plus "showing X of N". Undisclosed sampling is misrepresentation at zoom.
3. **Hover carries units and identity.** Every trace: what the point is, values with units. Hover showing bare numbers without labels is a missed instrument reading.
4. **Spec lean, data external where big.** Keep the generating script; inline data only when small. A chart that can't be regenerated from its script is a dead end.
5. **Exploration-only by default.** If a view from this chart ends up in the paper, redraw it statically via `scientific-plotting` — screenshots of interactive charts print badly and carry no style contract.

## The Build Sequence

### 1. Should this be interactive at all?

| Situation | Decision |
| --- | --- |
| Exploration needs zoom/hover/filter, or 10k+ points | **Plotly interactive. Continue.** |
| Final paper figure | Stop. Use `scientific-plotting` (panels) then `publication-figure`. |
| Statistical claim to exhibit | Route through `statistical-plot` for the numbers; interactivity is optional chrome. |
| n < ~500, one static message | Stop. A static figure loads instantly and prints. |

### 2. Budget the points

- Count N. ≤ ~10k → standard traces. Above → scattergl for scatter; aggregation (2-D histogram/hexbin) for density; level-of-detail or server-side for millions — and say which.
- Downsampling method chosen and written into the chart subtitle/legend: "showing 10,000 of 2.4M (stratified by class, seed 7)".

### 3. Build the instrument

- Traces minimal: one per series/class, named in the legend as a human would say it. Linked views (brush across panels) only when the question genuinely spans panels.
- Axes with units, ranges sane (no 40 empty decades), log declared where used. Buttons/sliders only if they answer a question — chrome that answers nothing is clutter.
- Colors from the project palette (`scientific-plotting` rules apply: Okabe-Ito, no rainbow).

### 4. Verify — the gate

- **Gate**: cold-load the exported HTML, time it; zoom to full depth, hover edge points, check the budget line matches the data. Slow load or wrong hover labels → fix before delivery.
- Confirm each number visible on hover against the source row in code. Hover text is generated text — it can be wrong like any other.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| 100k SVG points inline | scattergl / aggregation, decided by count |
| Silent downsampling | Method + "X of N" on the chart |
| Bare-number hovers | Identity + values + units per trace |
| Unregenerable HTML blob | Generating script kept, seed noted |
| Paper screenshot of the widget | Redraw statically via scientific-plotting |
| Chrome answering nothing | Every control tied to a question |

## Output

The deliverable is the instrument **plus its budget**, in this order:

- **Chart file** — HTML (+ generating script), cold-load time noted.
- **Budget line** — N shown vs N total, sampling method, seed.
- **Reading guide** — what to hover/filter, what the views answer (3 lines max).
- **Limits** — what sampling hides, valid exploration scope.

Don't pad this into a report. The fast-loading chart is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "2.4M points need aggregation — plotting them all helps no one", aggregate and disclose. When the user wants the widget in the paper, redraw it statically instead of screenshotting.
