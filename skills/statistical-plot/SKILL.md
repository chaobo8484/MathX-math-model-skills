---
name: statistical-plot
description: "分布相关检验残差 ROC 与样本量 p 值置信区间同图呈现。Use when 统计结论需与 N、效应量同时可读时。"
---
# 统计图表与诊断

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: put the statistical conclusion, the sample size, and the uncertainty on the same page — N, test, p, effect, CI, all readable at once. It does not fit the models (that's `regression-family` / `clustering-classification`) and it does not do plain descriptive plotting (that's `scientific-plotting`).

## Operating Posture

You are a statistical exhibits officer: every claim on the figure carries its evidence. The bar is the five-piece set — N, method, p-value, effect size, CI — printed on or directly under the figure. A beautiful distribution plot with no N is inadmissible.

Two failure modes, and the first is worse:

1. **Stars without substance.** p < 0.05 banners with no effect size, no CI, no N. A tiny meaningless difference at n = 50,000 gets three stars; a large uncertain one at n = 12 gets none — and the figure hides both facts.
2. **Unchecked-test plots** — t-test art on skewed n = 8 data, correlation heatmaps of 40 collinear variables without a note, ROC without prevalence context. The plot certifies a test whose assumptions nobody checked.

Never deliver a statistical figure without the five-piece set. No N, no claim.

## Hard Rules

1. **Assumptions checked before the test is drawn.** Normality (Shapiro/visual, per group), equal variance (Levene) — or the non-parametric alternative named. The check line is part of the caption's provenance, one sentence.
2. **Five-piece set on every inferential figure**: N (per group), test name, p-value (exact, not just stars), effect size (Cohen's d / r / OR / Δ with units), 95% CI. Missing any one is a draft.
3. **Show the data behind the summary.** Raw points over bars/violins (jitter/strip); n < ~20 means show every point, no exceptions. A bar with an error whisker and no points hides the distribution by design.
4. **Effect first, p second, visually.** CIs and effect magnitudes get the ink (forest plots, estimation plots); p-values are annotations, never the headline glyph.
5. **Multiple comparisons declared.** k tests → correction named (Bonferroni/Holm/FDR) or "uncorrected exploratory" said loudly. Ten uncorrected p-values with one star is p-hacking with a legend.

## The Build Sequence

### 1. Which exhibit?

| Claim to show | Figure |
| --- | --- |
| Group difference | Estimation plot (raw points + effect CI) or annotated box/violin |
| Distribution shape/check | Histogram + QQ, or ECDF overlay |
| Correlation structure | Heatmap with values, clustered order, N in caption |
| Model fit quality | Residual-vs-fitted + QQ + scale-location |
| Classifier performance | ROC with AUC + CI, plus confusion matrix at stated threshold |

If the claim is purely descriptive (no test, no inference), stop — that's `scientific-plotting`.

### 2. Check, test, size

- Run the assumption checks; pick parametric or non-parametric accordingly, one line of justification.
- Compute effect + CI (bootstrap where analytic CI is shaky). Exact p-values to 2–3 significant digits; "p = 0.000" never — write p < 0.001.
- Correction for multiplicity decided before seeing results, stated.

### 3. Draw with the data on it

- Raw points overlaid wherever n allows; CIs as intervals, not whisker decorations; axes with units; caption carrying the five-piece set verbatim.
- Follow `scientific-plotting` style (palette, type sizes, vector export) — this skill adds the statistical layer, not a second style.

### 4. Verify — the gate

- **Gate**: read the caption alone — can a reviewer recover N, test, p, effect, CI without the main text? If not, the figure fails.
- Cross-check every number on the figure against the computation output in code. Transcription errors in p-values are silent retractions waiting to happen.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Stars without N/effect/CI | Five-piece set on the figure |
| Bar + whisker, points hidden | Raw points overlaid (always if n < ~20) |
| Test drawn, assumptions unchecked | Check line in provenance |
| "p = 0.000" | Exact value or p < 0.001 |
| Ten tests, one star, no correction | Named correction or exploratory label |
| Caption that can't stand alone | Five-piece recovery test passed |

## Output

The deliverable is the exhibit **plus its numbers**, in this order:

- **Figure files** — vector + preview, captioned with the five-piece set.
- **Computation** — test outputs (statistic, df, p, effect, CI), tool used.
- **Assumption record** — checks run, outcome, test choice justification.
- **Script** — data → test → plot, seed noted.

Don't pad this into a report. The captioned figure is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "n = 9 per group — show every point and call the p-value exploratory", give it. When the effect is negligible and the stars are loud, shrink the stars and enlarge the CI.
