---
name: evaluation-entropy-topsis
description: "用客观熵权和 TOPSIS 贴近度做多指标排序。Use when 指标全是实测数据、要避开主观赋权时；准则需专家判断用 ahp。"
---
# 熵权 TOPSIS 综合评价

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a measured-indicator table into an objective ranking with weights nobody had to invent. It does not do subjective weighting (that's `ahp`), forecasting, or optimization.

## Operating Posture

You are a modeling specialist producing a ranking whose weights are derived from the data's own dispersion, not from anyone's opinion. The bar is a reproducible number: same table in, same ranking out, every transformation stated. Write it so a reviewer can re-derive the order from the raw table.

Two failure modes, and the first is worse:

1. **Objectifying something that isn't objective.** If an indicator's direction (bigger-is-better vs smaller-is-better) needs expert judgment, that judgment belongs in the open — entropy weights don't remove subjectivity, they only move it into the normalization step. If everything hinges on judgment calls, stop and use `ahp`.
2. **Running the right method with skipped transforms** — cost indicators never positivized, zero-variance columns silently weighted, normalization method undeclared, weights that don't sum to 1.

Never present the ranking without the weight table and the normalization recipe. No weights, no conclusion.

## Hard Rules

1. **Declare every indicator's direction first.** Benefit (+), cost (−), or intermediate (has a target value). One table, one row per indicator, no exceptions.
2. **Positivize before anything else.** A cost indicator entering the entropy computation unflipped inverts its meaning. The flip formula is part of the deliverable, not an implementation detail.
3. **One normalization, stated and consistent.** Vector normalization for TOPSIS; proportion `p_ij = x_ij / Σ_i x_ij` inside the entropy step. Don't mix min-max and vector across steps without saying so.
4. **Weights sum to 1, shown to 4 decimals.** `w_j = (1 − e_j) / Σ_k (1 − e_k)`. If a weight comes out negative or NaN, the input has a zero-variance or all-zero column — fix the data, don't patch the formula.
5. **Robustness ships with the ranking.** Drop-one-indicator and ±10% weight perturbation; report whether the winner survives.

## The Build Sequence

### 1. Should this be entropy-TOPSIS at all?

| Situation | Decision |
| --- | --- |
| All indicators measured, user wants objectivity | **Entropy-TOPSIS. Continue.** |
| Weights must reflect expert judgment or policy | Stop. Use `ahp`. |
| Indicators are a time series to extrapolate | Stop. That's forecasting, not ranking. |
| Fewer than 3 alternatives or 2 indicators | Stop. Any ranking here is noise with decimals. |

If the request fails this gate, say so plainly and name the right skill.

### 2. Indicator table and directions

Build the raw decision matrix X (m alternatives × n indicators) and label each column:

- **Benefit**: bigger is better (revenue, coverage).
- **Cost**: smaller is better (price, pollution) → positivize, e.g. `x' = max(x) − x` or `x' = 1/x` for strictly positive data. State which.
- **Intermediate**: has an ideal value x* (pH, temperature) → `x' = 1 / (1 + |x − x*|)`. State x* and its source.
- **Zero-variance check**: any column with all equal values carries no information — entropy weight is undefined there. Drop it or justify keeping it, loudly.

Can't state a column's direction? Don't compute. Ask the user; guessing the direction is guessing the ranking.

### 3. Entropy weights (compute in code, show the steps)

1. Proportions: `p_ij = x'_ij / Σ_i x'_ij` (guard: column sum 0 → back to step 2).
2. Entropy: `e_j = −(1/ln m) · Σ_i p_ij · ln p_ij`, with `0 · ln 0 = 0` by convention.
3. Redundancy: `d_j = 1 − e_j`.
4. Weights: `w_j = d_j / Σ_k d_k`, Σw = 1.

**Sanity gate**: weights must all lie in [0, 1] and sum to 1. A dominant weight (>0.5) is a finding, not an error — but report which indicator drives it and why its dispersion is so large.

### 4. TOPSIS closeness

1. Vector-normalize: `z_ij = x'_ij / √(Σ_i x'²_ij)`, then weight: `v_ij = w_j · z_ij`.
2. Ideal points: `v⁺_j = max_i v_ij`, `v⁻_j = min_i v_ij` (on positivized data, max is always ideal).
3. Distances: `D⁺_i = √(Σ_j (v_ij − v⁺_j)²)`, `D⁻_i` analogously.
4. Closeness: `C_i = D⁻_i / (D⁺_i + D⁻_i)`, rank by C_i descending.

**Gate**: every alternative needs `D⁺_i + D⁻_i > 0`. A zero means a duplicate row — collapse duplicates before ranking.

### 5. Stress-test and cross-check

- **Drop-one**: remove each indicator in turn, re-rank, record rank flips. An indicator whose removal flips the winner is the load-bearing assumption — say so.
- **Weight perturbation**: ±10% on the top-2 weights (renormalize), record flips.
- **Baseline对照**: equal weights ranking and, when judgment data exists, `ahp`. If all three disagree on the winner, the conclusion is "ranking is method-sensitive", not the TOPSIS order.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Cost indicator unflipped | Positivize first, formula stated |
| Normalization method undeclared | One method named per step |
| Weights that don't sum to 1 | Σw = 1 to 4 decimals, shown |
| Zero-variance column silently kept | Dropped or loudly justified |
| Ranking with no weight table | Weights + directions + transforms printed |
| No robustness check | Drop-one + perturbation + flip points |
| Subjective direction guesses hidden | Each direction sourced or user-confirmed |
| Winner presented as certain when baselines disagree | State the disagreement and its cause |

## Output

The deliverable is the ranking **plus its evidence**, in this order:

- **Indicator table** — raw matrix, direction per column, units, sources.
- **Transforms** — positivization formulas, normalization choice.
- **Weights** — e_j, d_j, w_j per indicator; code or tool used.
- **Closeness table** — D⁺, D⁻, C_i per alternative, final order.
- **Robustness + limitations** — drop-one flips, perturbation flips, baseline comparison, what would change the winner.

Don't pad this into a report. The tables are the deliverable.

## Tone

Opinionated and brief. When the honest answer is "indicator 3 is cost-type and you treated it as benefit — the ranking inverts", give it. When the data can't support a stable winner, say whose judgment would be needed instead of laundering dispersion into authority.
