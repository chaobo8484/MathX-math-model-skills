---
name: monte-carlo-simulation
description: "随机抽样估计概率、期望与风险。Use when 解析解困难但随机变量与分布明确时。"
---
# 蒙特卡洛模拟

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: estimate probabilities, expectations, and risk by random sampling — with a convergence curve that earns every decimal. It does not do closed-form statistics, deterministic optimization, or forecasting from data.

## Operating Posture

You are a modeling specialist producing an estimate with a measured Monte Carlo error, not a number with decorative precision. The bar is convergence: the estimate stops moving as N grows, standard error reported, seed fixed. Write it so the convergence plot passes the first time.

Two failure modes, and the first is worse:

1. **Simulating what has a closed form.** Option-style expectations, simple queues, or textbook distributions with analytic answers don't need sampling. Monte Carlo there is slower with wider bands.
2. **Reporting digits the run didn't earn** — N = 1,000 with four decimals, no convergence curve, seed unreported, input correlations invented as independence. Four decimals from a noisy run is fabrication.

Never present an estimate without N, standard error, and seed. No convergence, no decimals.

## Hard Rules

1. **Every random input gets a distribution + source.** Family, parameters, and why (fitted, assumed, expert). "Normal(0,1) by default" is not a source.
2. **Correlations declared, never defaulted.** Independent until proven otherwise is a choice — state it, or supply the copula/correlation matrix with its source.
3. **Vectorize in batches, seed fixed and reported.** Loop-free batch sampling; one master seed in the deliverable. Unseeded runs are irreproducible by definition.
4. **Convergence curve mandatory.** Estimate vs log₁₀(N) with ±2 SE bands; decimals reported only where the curve is flat. SE shrinks as 1/√N — quadrupling N buys one digit, budget accordingly.
5. **Variance reduction where it pays.** Antithetic variates, control variates, or importance sampling for rare events — stated when used, with the variance ratio shown.

## The Build Sequence

### 1. Should this be Monte Carlo at all?

| Situation | Decision |
| --- | --- |
| Closed form hard, but inputs, distributions, and constraints are statable | **Monte Carlo. Continue.** |
| Analytic answer exists (textbook expectation, simple queue) | Stop. Compute it exactly. |
| Distributions unknown and unassumable | Stop. Say so; sampling from invented distributions is fiction. |
| Rare event (p < 1e-4) with plain sampling | Stop or switch to importance sampling — plain MC needs ~1e6+ draws per digit here. |

### 2. Specify the stochastic model

- Random variables table: name, distribution, parameters, source per row. Deterministic parameters with units beside it.
- Dependence structure: independent (stated as a choice) or correlation matrix / copula with source. Correlated inputs sampled independently is a silent model change — forbid it by default.
- Output quantity defined in closed form of the inputs: probability, expectation, quantile (VaR-style), or full histogram. One primary quantity; the rest is supporting.

### 3. Sample in batches with a seed

- Batch-vectorized draws (no Python-loop millions); N schedule doubling (1k → 2k → 4k …) so the convergence curve comes free.
- Master seed fixed, reported, rerunnable. Sensitivity: second seed run to confirm the headline digits don't wobble.

### 4. Convergence — the gate

- Plot estimate ± 2 SE against log₁₀(N). **Gate**: headline decimals only where the band is flat across the last doubling. SE = s/√N for means; binomial SE for probabilities; batch-means or bootstrap for quantiles.
- Rare-event check: fewer than ~100 hits means the relative error is huge — increase N, use importance sampling, or report the wide band honestly.

### 5. Sensitivity and decision use

- Tornado: vary each input's key parameter ±(stated %) and rank output movement. The top driver is a finding — name it.
- Decision framing: if the simulation feeds a choice, report P(option A beats B) and the loss distribution, not just means. Means hide risk; that hiding is the failure this skill exists to prevent.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Digits beyond the flat part of the curve | Decimals earned by convergence only |
| No convergence plot | Estimate ± 2 SE vs log₁₀(N) |
| Unseeded run | Master seed reported, rerunnable |
| Correlations silently independent | Declared or sourced, one line |
| Invented distributions, unstated | Source per input row |
| Mean-only risk reporting | Quantiles / loss distribution where decisions ride on it |
| Plain sampling for rare events | Importance sampling or honest wide bands |

## Output

The deliverable is the estimate **plus its error**, in this order:

- **Stochastic model** — input table with distributions + sources, dependence stated, output defined.
- **Run** — N schedule, seed, sampler/tool, variance-reduction method if any.
- **Convergence** — curve plot, SE, headline digits with band.
- **Sensitivity** — tornado ranking, top driver.
- **Limits** — distribution assumptions most likely to break the answer.

Don't pad this into a report. The convergence plot is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "N = 2,000 earns two decimals, not four — the third digit is noise", give it. When the inputs are invented, refuse the run instead of sampling the fiction precisely.
