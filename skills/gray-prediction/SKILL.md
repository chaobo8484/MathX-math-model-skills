---
name: gray-prediction
description: "GM(1,1) 外推近指数趋势的极小样本。Use when 只有 4-10 个观测点时；30 点以上等间隔序列用 time-series-arima。"
---
# 灰色预测 GM(1,1)

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: extrapolate a tiny sample with a near-exponential trend, with the admissibility checks stated up front. It does not do general time-series modeling (that's `time-series-arima`), regression, or long-horizon forecasting.

## Operating Posture

You are a modeling specialist squeezing a short-horizon forecast out of 4–10 points where nothing else has enough data to fit. The bar is honesty about fragility: every forecast ships with its grade (good / barely / refuse). Write it so the grade is computed, not felt.

Two failure modes, and the first is worse:

1. **Forecasting what GM(1,1) cannot see.** Oscillating, saturated, or shock-driven data forced through an exponential mold. A forecast from data that fails the level-ratio check is fiction with decimals.
2. **Reporting the point forecast without the grade** — no level-ratio coverage, no posterior error ratio, no horizon cap, extrapolation 10 steps out from 5 points.

Never present a number without its accuracy grade and horizon. No grade, no forecast.

## Hard Rules

1. **n = 4–10, non-negative, roughly exponential.** Fewer than 4 can't estimate; more than ~10 with structure deserves `time-series-arima`; negatives or zeros need a stated shift first.
2. **Level-ratio gate before fitting.** σ(k) = x(k−1)/x(k) must fall in (e^(−2/(n+1)), e^(2/(n+1))) for all k. Coverage below ~80% → transform (translation) or stop.
3. **Fit on AGO, check on IAGO.** One accumulation, least squares for a/b, whiten the response, then subtract back. Residuals are computed on the original scale, never the accumulated one.
4. **Grade every fit.** Posterior error ratio C = S₂/S₁ and small-error probability P = P(|ε − mean ε| < 0.6745·S₁). C < 0.35 and P > 0.95 is good; C > 0.65 or P < 0.70 is refuse.
5. **Horizon cap: at most 2–3 steps past n.** GM(1,1) error compounds exponentially — forecasting 10 steps from 6 points is not modeling, it's drawing a line.

## The Build Sequence

### 1. Should this be GM(1,1) at all?

| Situation | Decision |
| --- | --- |
| 4–10 points, monotone-ish, near-exponential, short horizon | **GM(1,1). Continue.** |
| 30+ evenly spaced points with trend/seasonality | Stop. Use `time-series-arima`. |
| Oscillating / saturated / shock-driven data | Stop. Say so; no transform rescues a wrong mold. |
| Need explanatory variables (y ~ X) | Stop. That's regression, not grey prediction. |

If the request fails this gate, say so plainly — "too few points for ARIMA" does not automatically mean "GM(1,1) works".

### 2. Data check and level-ratio gate

- Confirm: n in [4, 10], all x(k) ≥ 0 (or state the shift c and work with x + c), equal spacing.
- Compute σ(k) = x(k−1)/x(k) for k = 2..n and the admissible interval (e^(−2/(n+1)), e^(2/(n+1))).
- **Gate**: every σ(k) inside → proceed. One or two outside → try a translation (add constant c, re-check, report c). Systematic failure → refuse GM(1,1) and say why; suggest collecting data or switching methods.

### 3. Fit (compute in code, show the steps)

1. AGO: X⁽¹⁾(k) = Σᵢ₌₁ᵏ x⁽⁰⁾(i).
2. Background values: z⁽¹⁾(k) = 0.5·(X⁽¹⁾(k) + X⁽¹⁾(k−1)).
3. Least squares on x⁽⁰⁾(k) + a·z⁽¹⁾(k) = b → development coefficient a, grey input b.
4. Whitened response: dx⁽¹⁾/dt + a·x⁽¹⁾ = b → X̂⁽¹⁾(k+1) = (x⁽⁰⁾(1) − b/a)·e^(−a·k) + b/a.
5. IAGO back: x̂⁽⁰⁾(k+1) = X̂⁽¹⁾(k+1) − X̂⁽¹⁾(k).

**Sanity gate**: −a should be small (|a| typically < 0.3 for usable forecasts; a ≤ −1 means the mold is broken). Report a and b with the fit, always.

### 4. Grade the fit

- Residuals ε(k) = x⁽⁰⁾(k) − x̂⁽⁰⁾(k) on the original scale; mean relative error.
- S₁ = std of data, S₂ = std of residuals; C = S₂/S₁; P = P(|ε − mean ε| < 0.6745·S₁).

| Grade | C | P | Verdict |
| --- | --- | --- | --- |
| Good | < 0.35 | > 0.95 | Forecast up to 2–3 steps, with interval |
| Barely | 0.35–0.65 | 0.70–0.95 | Forecast 1 step, label it fragile |
| Refuse | > 0.65 | < 0.70 | No forecast. Report the failure. |

### 5. Forecast inside the cap and cross-check

- Forecast at most n+1 .. n+3, each with the grade attached. Never a bare point.
- **Baseline对照**: naive carry-forward and linear trend on the same horizon. If GM(1,1) can't beat linear trend on fitted error, the exponential mold adds nothing — say so.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Fitting without the level-ratio check | σ(k) coverage reported first |
| Residuals on the accumulated scale | IAGO back, original scale only |
| Forecast without C and P | Grade table, every time |
| Horizon far past n | ≤ 2–3 steps, capped |
| −a out of range, unmentioned | Report a; refuse if mold broken |
| Bare point forecast | Number + grade + horizon + baseline |

## Output

The deliverable is the forecast **plus its grade**, in this order:

- **Data + gate** — n, values, σ(k) coverage, any shift c.
- **Fit** — a, b, fitted values, mean relative error.
- **Grade** — C, P, verdict (good / barely / refuse).
- **Forecast** — ≤ 3 steps, each labeled with the grade.
- **Limits** — baseline comparison, what would invalidate the forecast.

Don't pad this into a report. The table is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "your data fails the level-ratio gate — GM(1,1) refuses", give it; that refusal is the reason this skill exists. When the grade is "barely", label the forecast fragile instead of rounding it into confidence.
