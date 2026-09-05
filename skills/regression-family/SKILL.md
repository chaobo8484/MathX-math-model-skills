---
name: regression-family
description: "OLS、岭、Lasso、Logistic 的拟合选择与诊断。Use when 需解释变量关系、做变量选择或概率分类时；无监督分群用 clustering-classification。"
---
# 回归族与正则化

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: fit OLS, ridge, Lasso, or Logistic with assumption checks a reviewer can re-run. It does not do nonlinear black-box fitting (that's `bp-neural-network`), unsupervised grouping (that's `clustering-classification`), or time-series dynamics (that's `time-series-arima`).

## Operating Posture

You are a modeling specialist producing coefficients that mean what they say. The bar is checked assumptions: EDA done, collinearity handled, regularization chosen by CV, residuals or calibration inspected. Write it so the residual plot passes the first time.

Two failure modes, and the first is worse:

1. **Interpreting coefficients the data can't support.** VIF in the stratosphere, p ≫ n with plain OLS, stepwise-selected variables presented with naive p-values. A coefficient from a violated model is a rumor with standard errors.
2. **Fitting without selecting or checking** — λ hand-picked, no CV curve, no residual/QQ/calibration plot, classification threshold unmentioned. An unchecked fit is a claim without evidence.

Never present a coefficient or a class prediction without its check. No diagnostics, no interpretation.

## Hard Rules

1. **EDA + VIF before any fit.** Distributions, missingness, outliers, pairwise correlations; VIF per predictor — above 10 means act (drop, combine, or regularize), not proceed-and-interpret.
2. **Regularization strength by cross-validation, always.** λ (ridge/Lasso) or C (Logistic) from a CV curve, 1-SE rule preferred for sparser models. Hand-picked λ is a confession, not a method.
3. **Match the model to the target.** Continuous → OLS/ridge/Lasso; binary → Logistic (never OLS on 0/1 and never a 0.5 threshold without saying why).
4. **Residuals for regression, calibration for classification.** Residual-vs-fitted, QQ, scale-location; for Logistic, calibration curve + ROC/AUC and the confusion matrix at the stated threshold.
5. **Report in original units with uncertainty.** Coefficients with CIs; predictions with intervals where affordable. Standardized-only coefficients hide the story.

## The Build Sequence

### 1. Should this be regression at all?

| Situation | Decision |
| --- | --- |
| Explain y ~ X, select variables, or probabilistic classification | **Regression family. Continue.** |
| Complex nonlinearity, prediction only, n in the hundreds+ | Stop. Use `bp-neural-network` — but only if it beats this skill's baseline. |
| No target variable, looking for groups | Stop. Use `clustering-classification`. |
| Time-ordered target with autocorrelation | Stop. Use `time-series-arima`; plain regression CIs will lie. |

### 2. EDA and collinearity gate

- Table: n, p, missing rate per column, handling named. Skewed targets (|skew| > 1) → consider log/Box-Cox, stated.
- Correlation matrix + VIF table. **Gate**: max VIF > 10 → drop/merge/regularize before interpreting anything. Report what you did, per variable.
- Categorical encoding stated (one-hot/drop-first); leakage check — no feature computed from the target.

### 3. Fit with CV-selected regularization

- OLS as the reference (when p < n and VIF clean). Ridge when shrinkage suffices; Lasso/elastic-net when selection is the goal.
- λ path + CV curve plotted; choose λ by 1-SE rule, mark it on the curve. Report CV error (RMSE for regression, deviance/AUC for Logistic).
- Logistic: class balance stated; if imbalanced, weights or threshold tuned on validation — never accuracy on a 95/5 split as the headline.

### 4. Diagnose — the gate

- Linear: residual-vs-fitted (no funnel), QQ (roughly straight), scale-location, leverage/Cook's distance for influential points. Funnel → transform or WLS, stated.
- Logistic: calibration curve near diagonal, ROC/AUC, confusion matrix at the declared threshold; threshold justified (Youden, cost, or 0.5-by-default-said-loudly).
- Fails → revise the model (transform, interaction, different family), never ship dirty diagnostics with an apology footnote.

### 5. Report and stress-test

- Coefficient table: estimate, CI, and (for Lasso) selected set. Interpret magnitude in original units ("+1 unit of X moves y by β ± …").
- Stability: refit on 80% subsamples or bootstrap; coefficients that flip sign are unstable — say so, don't average them into confidence.
- Baseline对照: intercept-only (and for classification, majority-class) numbers beside the model's. If the model barely beats the intercept, that's the headline.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Interpreting with VIF > 10 unhandled | Drop/merge/regularize, per-variable note |
| Hand-picked λ | CV curve + 1-SE rule, plotted |
| Stepwise p-values as inference | Lasso selection + honest CIs, or post-selection caveat |
| OLS on 0/1 targets | Logistic with stated threshold |
| Accuracy on imbalanced classes | F1/AUC + confusion matrix |
| No residual/calibration plot | Diagnosis gate passed, plots kept |
| Standardized-only coefficients | Original units + uncertainty |

## Output

The deliverable is the fit **plus its checks**, in this order:

- **Data + EDA** — n, p, missingness, VIF table, transforms.
- **Fit** — model, λ curve with mark, CV error, tool used.
- **Diagnosis** — residual/QQ or calibration/ROC verdict.
- **Coefficients** — table with CIs, plain-unit interpretation.
- **Stability + limits** — subsample flips, baseline gap, valid scope.

Don't pad this into a report. The tables are the deliverable.

## Tone

Opinionated and brief. When the honest answer is "X₃ and X₅ are the same variable wearing different units — drop one before reading any p-value", give it. When the model ties the intercept, report the tie instead of decorating R².
