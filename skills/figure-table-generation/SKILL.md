---
name: figure-table-generation
description: "把分析结果整理成带题注引用的投稿级图表和 booktabs 表格。"
disable-model-invocation: true
---
# 论文图表生成与规范化

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: convert analysis outputs into captioned, cited, column-sized figures and booktabs tables ready for the manuscript. It does not draw exploratory plots (that's `scientific-plotting` et al.) and it does not assemble the final composite (that's `publication-figure`).

## Operating Posture

You run this when the user types it, with results in hand. The product is a numbered figure/table set where every number traces to its computation and every caption stands alone. The bar is the caption test: figure + caption + table notes must convey the result without the main text.

Two failure modes, and the first is worse:

1. **Numbers without provenance.** A table of RMSEs nobody can re-derive, a bar chart from a spreadsheet nobody kept. Every cell traces to code + data + seed, or the cell doesn't ship.
2. **Caption decoration.** "Results of the experiment" as a caption, units missing, N missing, table rules from the spreadsheet era (vertical lines everywhere). A caption that says nothing forces the reader to decode the graphic raw.

Never deliver a figure/table without its source trace and a standalone caption. No trace, no exhibit.

## Hard Rules

1. **One message per exhibit.** If the figure needs two captions, it's two figures. Combined mega-figures that serve three arguments serve none.
2. **Captions standalone.** What is shown, N, method in one clause, key reading in one clause, units everywhere. "As shown in Fig. 3" must never be load-bearing in the main text either — but that's `polish-proofread`'s fight; here the caption carries its weight.
3. **booktabs tables, no vertical rules.** \toprule/\midrule/\bottomrule only; units in the header row, not repeated per cell; significant digits matched to the error (a ±0.02 effect reported to 4 decimals is noise cosplay).
4. **Column-sized vector exports.** Widths per the venue (single ≈ 89mm typical — confirm), type sizes final, palette from the project system. Regenerate at size; never scale screenshots.
5. **Text-cites-figure consistency.** Every number the prose quotes appears identically in the exhibit (same rounding!). Grep the prose figures against the tables before delivery — transcription drift is the classic silent retraction.

## The Production Sequence

### 1. Inventory the exhibits

- List from the outline: which claim needs which figure/table. Uncited exhibits get cut or assigned — never produced "just in case".

### 2. Build each exhibit

- Figures: spec the drawing (chart type per `chart-decision` if undecided), draw via the plotting skills, export vector at column size.
- Tables: booktabs, header units, digit discipline, notes row for methods/abbreviations.

### 3. Caption + trace — the gate

- **Gate per exhibit**: standalone-caption read (a colleague gets the result from caption + graphic alone?) + provenance line (code + data + seed) + prose-consistency grep (quoted numbers match to the digit).

### 4. Hand off

- Numbered files (fig03.pdf, tab02.tex) with the caption catalog; forward to `latex-typesetting` for inclusion, `publication-figure` for multi-panel assembly, `polish-proofread` for prose around them.

## Never Ship

| Never | Instead |
| --- | --- |
| Tracless numbers | Code + data + seed per cell |
| "Results of…" captions | Standalone: what + N + method + reading |
| Vertical-ruled tables | booktabs, header units |
| Digits beyond the error | Digit discipline per column |
| Prose/exhibit drift | Grep-to-match before delivery |
| Screenshot scaling | Regenerate at column size |

## Output

- **Exhibit files** — numbered vectors + table sources.
- **Caption catalog** — standalone captions, all exhibits.
- **Trace table** — exhibit → code + data + seed.
- **Consistency grep** — prose numbers match, evidence shown.

## Tone

Opinionated and brief. When the honest answer is "this table's fourth decimal is noise — cut two digits", cut them. When a figure serves no outline claim, cut the figure instead of writing a caption to justify it.

模板文件见 assets/templates/figure-table-generation.tex（随本技能分发；改动前先核对 venue spec）。
