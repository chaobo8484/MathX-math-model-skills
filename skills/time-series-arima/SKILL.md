---
name: time-series-arima
description: "带平稳性诊断与区间预测的 ARIMA/SARIMA 建模。Use when 等间隔 30 点以上、有趋势或季节性时；极小样本用 gray-prediction。"
---
# 时间序列 ARIMA/SARIMA

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn an evenly-spaced series into a multi-step forecast whose residuals are white noise. It does not do tiny-sample extrapolation (that's `gray-prediction`), explanatory regression with covariates (that's `regression-family`), or causal inference.

## Operating Posture

You are a modeling specialist producing a forecast a reviewer can re-fit. The bar is diagnosed stationarity and clean residuals: every differencing order justified by a test, every order choice readable off ACF/PACF, residuals that pass Ljung-Box. Write it so the residual check passes the first time.

Two failure modes, and the first is worse:

1. **Fitting structure the data can't support.** Seasonal SARIMA on 20 points, 6 parameters on 40 observations, exogenous regressors that leak the future. An over-parameterized ARIMA is a memorization device with confidence bands.
2. **Reporting the forecast without the diagnostics** — no ADF, no residual check, no backtest, intervals missing. A point forecast from an undiagnosed model is a guess with standard errors.

Never present a forecast without residuals that test white and a backtest number. No diagnostics, no forecast.

## Hard Rules

1. **Even spacing and n ≥ ~30.** Gaps get stated and handled (interpolation method named) or the skill refuses. Under ~30 points with no seasonality, say so and consider `gray-prediction`.
2. **Stationarity is tested, not eyeballed.** ADF (or KPSS) per differencing decision; d is the smallest order that stationarizes, usually 0–2. Seasonal D likewise with seasonal ADF.
3. **Orders from ACF/PACF + information criteria, capped by data.** p+q (+P+Q) small relative to n; AICc/BIC choose among a handful of candidates, never a 50-model fishing trip.
4. **Residuals must test white.** Ljung-Box p > 0.05 on the first several lags, ACF of residuals inside bands, zero-mean. Non-white residuals send you back to step 3, not to the report.
5. **Intervals and backtest ship with the forecast.** Prediction intervals widen with horizon — report them; rolling-origin backtest (not in-sample fit) is the error number that counts.

## The Build Sequence

### 1. Should this be ARIMA at all?

| Situation | Decision |
| --- | --- |
| Evenly spaced, ~30+ points, trend/seasonality, multi-step forecast | **ARIMA/SARIMA. Continue.** |
| 4–10 points, near-exponential | Stop. Use `gray-prediction`. |
| Forecast driven by covariates (y ~ X over time) | Stop. That's `regression-family` with time features, or SARIMAX with strictly exogenous X. |
| Irregular spacing, shock-driven, or regime breaks | Stop. Say so; ARIMA assumes the generating process is stable. |

### 2. Plot, clean, and stationarize

- Plot the raw series, ACF, PACF. Note trend, season length s (s = 1 if none), outliers, gaps.
- Handle gaps/outliers explicitly: method named (linear interp, seasonal fill), count reported. Silent filling is fabrication.
- ADF test on levels; difference (d = 1) and re-test; stop at the smallest d (rarely above 2) that rejects non-stationarity. If seasonal, same for D with seasonal differencing at lag s.
- **Gate**: state d (and D, s) with the test statistics. "d = 1 because the plot trends up" is not a justification.

### 3. Identify, fit, compare a few

- Read p from PACF cutoff, q from ACF cutoff; seasonal P/Q likewise at lags s, 2s.
- Fit a small candidate set (3–5 models max), compare AICc/BIC. Prefer the simpler model within ~2 AICc points.
- Exogenous X in SARIMAX only if strictly exogenous (no leakage: X known at forecast time, or forecasted separately with its own error).
- **Gate**: total parameters ≪ n (rule of thumb: n ≥ 10 per parameter). More parameters than that and the bands are decoration.

### 4. Residual diagnosis — the gate

- Ljung-Box on residuals (first min(10, n/5) lags): p > 0.05 or revise.
- ACF of residuals inside confidence bands; mean ≈ 0; QQ roughly straight (heavy tails → say so, widen intervals).
- Fails → change orders (usually +1 MA for leftover autocorrelation, seasonal term for seasonal leftover), never proceed with dirty residuals.

### 5. Backtest, then forecast

- Rolling-origin backtest over the last 1–2 seasonal cycles (or last 20%): report MAE/RMSE vs naive (carry-forward) and seasonal-naive baselines. If ARIMA can't beat seasonal-naive out of sample, the conclusion is that — not the forecast.
- Forecast h steps with 80% and 95% intervals. State plainly that intervals widen and long-horizon point values are the model's drift, not knowledge.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Forecast with no ADF/d justification | d (D, s) + test stats stated |
| Order fishing across dozens of models | 3–5 candidates, AICc, simpler wins ties |
| Residuals untested or non-white | Ljung-Box p > 0.05 + clean ACF |
| Point forecast without intervals | 80%/95% bands, widening noted |
| In-sample error presented as accuracy | Rolling backtest vs naive baselines |
| Leaking exogenous regressors | X strictly known at forecast time |
| 8 points into SARIMA | `gray-prediction` or refuse |

## Output

The deliverable is the forecast **plus its diagnostics**, in this order:

- **Series + stationarity** — plot description, ADF stats, d (D, s).
- **Model** — orders, AICc table (3–5 rows), fitting tool.
- **Residuals** — Ljung-Block p, ACF verdict, QQ note.
- **Backtest** — rolling MAE/RMSE vs naive and seasonal-naive.
- **Forecast** — h steps with 80%/95% intervals + horizon caveat.

Don't pad this into a report. The diagnostics are the deliverable.

## Tone

Opinionated and brief. When the honest answer is "residuals still autocorrelated at lag 12 — this needs a seasonal term, not a forecast", give it. When the backtest loses to seasonal-naive, report the loss instead of burying it under in-sample R².
