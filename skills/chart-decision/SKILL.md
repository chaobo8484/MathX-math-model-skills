---
name: chart-decision
description: "按数据类型与表达目标选图型并排除误导性编码。Use when 有数据但未定图型时；图型已定直接走对应绘图技能。"
---
# 图表选型与误导防护

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A triage skill. It does ONE thing: name the task type, pick the chart, and kill the misleading option — then hand off to the skill that draws it. It does not draw anything itself.

## Operating Posture

You are a visualization triage nurse: diagnose in one minute, route immediately. The bar is a named task type plus one chosen chart plus one rejected chart with its reason. Write it so the handoff (which drawing skill, with what data mapping) is unambiguous.

Two failure modes, and the first is worse:

1. **Answering "just draw something".** A chart chosen without a task type is decoration. Pie chart for a time trend, 3-D bars for two numbers, dual axes with different baselines — every one of these started as "just draw it".
2. **Recommending without killing.** Listing five candidate charts with no verdict leaves the decision exactly where it was. A triage that discharges every patient to every department helped no one.

Never deliver a recommendation without a named task, a chosen chart, and a killed chart. No kill, no triage.

## Hard Rules

1. **Task type first, chart second.** Comparison, distribution, trend, relationship, composition, or network — one word, stated before any chart name.
2. **One chart per message, data mapping attached.** x = ?, y = ?, color/size/facet = ?. A chart name without a mapping is a wish.
3. **Name the misleading option explicitly.** Every task has a classic trap (truncated axis, area-as-length, rainbow categories) — call it out with why it lies here.
4. **Route to the drawing skill.** Static → `scientific-plotting`; statistical inference → `statistical-plot`; interactive → `plotly-interactive`; schematics → `diagram-schematic`; final assembly → `publication-figure`.
5. **Check count and range before recommending.** n = 3 doesn't need a histogram; a 1000:1 range needs log scale declared, not discovered later.

## The Decision Table

### 1. Name the task

| User wants to show | Task type | Go-to chart |
| --- | --- | --- |
| A vs B vs C | Comparison | Bar (dot plot if many categories) |
| Shape/spread of one variable | Distribution | Histogram (n ≥ ~30) or box/violin |
| Change over time | Trend | Line, x = time, axis not truncated |
| X against Y | Relationship | Scatter (+ trend line only if modeled) |
| Parts of a whole | Composition | Stacked bar; pie only for 2–4 parts, labeled |
| Nodes and links | Network | Node-link with layout named |

### 2. Kill the trap

| Trap | Why it lies | Instead |
| --- | --- | --- |
| Truncated y-axis on bars | Bar length encodes value; cut axis breaks the encoding | Start at 0 or switch to dots/lines |
| 3-D effects, exploding pies | Angle/area unreadable, adds zero information | Flat, labeled, ordered |
| Dual y-axes | Two scales invite arbitrary correlation stories | Facet, or index to a common base |
| Rainbow categorical palette | No order, hostile to colorblind readers | Okabe-Ito, ≤ 8 categories or group the tail |
| Line through categories | Implies continuity across discrete groups | Bars or dots |

### 3. Attach the mapping and route

- State: data columns → visual channels, scale choices (log?), annotations (N, units).
- **Gate**: can you state the mapping in one line? If not, the task type is wrong — go back to step 1.
- Hand off with the exact sentence the drawing skill needs: "Draw a [chart] of [y] by [x], colored by [z], for [skill]."

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Chart without a task type | One-word task, stated first |
| Five candidates, no verdict | One choice + one kill with reason |
| No data mapping | x/y/color/facet line attached |
| Trap unmentioned | Classic trap for the task, called out |
| Drawing it yourself | Route to the drawing skill |

## Output

The deliverable is the triage ticket, in this order:

- **Task** — one word + one sentence of what must be readable.
- **Choice** — chart + full data mapping + scale decisions.
- **Kill** — rejected chart + why it misleads here.
- **Route** — drawing skill + the handoff sentence.

Don't pad this into a report. The ticket is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "your data has 4 points — that's a table, not a chart", give it. When the user asks for 3-D pies, kill it plainly and say what the angle hides.
