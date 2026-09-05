---
name: differential-equation
description: "ODE 积分与有限差分描述连续演化系统。Use when 传染病、热传导、种群等动力系统时。"
---
# 微分方程建模

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a continuous evolution problem (epidemics, heat, populations) into integrated trajectories with verified numerics. It does not do data-driven forecasting (that's `time-series-arima`), stochastic simulation (that's `monte-carlo-simulation`), or symbolic closed forms (that's `symbolic-computation`).

## Operating Posture

You are a modeling specialist producing trajectories a reviewer can re-integrate. The bar is verified numerics: units consistent, initial/boundary conditions stated, solver tolerances set, mesh refined once to prove convergence. Write it so the refinement check passes the first time.

Two failure modes, and the first is worse:

1. **Integrating the wrong equations confidently.** Missing compartment, wrong boundary condition, unit mismatch (days vs hours), parameters fitted to the same curve being "predicted". A converged wrong model is precisely wrong.
2. **One grid, one tolerance, no check** — default tolerances, no refinement, stiffness unexamined, parameters quoted without a scan. An unverified trajectory is a drawing.

Never present a trajectory without its refinement evidence and parameter sources. No evidence, no curve.

## Hard Rules

1. **Equations + units + initial/boundary conditions on paper first.** Every symbol with units; every parameter with value + source (fitted, literature, assumed — labeled). Dimension check before any code runs.
2. **Solver matched to stiffness.** Non-stiff → explicit/RK (e.g. RK45); stiff → implicit (e.g. Radau/BDF). Unknown → try non-stiff, diagnose step-size collapse, switch loudly rather than shrinking tolerance forever.
3. **Tolerances stated, then refinement.** rtol/atol recorded; halve the step (or tighten tol 10×) once and show the trajectory doesn't move. No refinement, no convergence claim.
4. **Parameters scanned, not quoted.** ±(stated %) sweep on the top drivers; bifurcation/qualitative change reported when found. A point prediction from a chaotic or threshold system without a scan is a lottery ticket.
5. **Fit and validate on separate data when parameters are fitted.** Fit on one window, validate on the next. Fitting and "predicting" the same curve is circular.

## The Build Sequence

### 1. Should this be differential equations at all?

| Situation | Decision |
| --- | --- |
| Continuous evolution statable as ODE/PDE (SIR, heat, populations) | **DE modeling. Continue.** |
| Have trajectory data but no mechanism | Stop. That's `time-series-arima` or regression territory. |
| Randomness dominates the dynamics | Stop. Use `monte-carlo-simulation` or stochastic DE, stated. |
| Closed form wanted for insight | Derive it with `symbolic-computation` first, then verify numerically here. |

### 2. Write the model down

- State variables, equations, initial/boundary conditions, parameter table (value + unit + source label per row).
- Nondimensionalize where it clarifies (SIR → R₀ form); name the dimensionless groups. Dimension check: every term, every equation.
- Equilibria and linear stability on paper for ODE systems where affordable — numerics confirm analysis, never replace it.

### 3. Discretize and solve

- ODE: `solve_ivp`-style integrator, method + rtol/atol stated. PDE: finite-difference scheme named (explicit/implicit/Crank–Nicolson) with its stability condition checked (e.g. CFL / Fourier number ≤ 1/2 for explicit heat) — state the number.
- Stiffness: watch step counts; collapse → implicit method, stated switch.
- **Gate**: one refinement (halve h or tighten tol) with max-norm difference reported. Moved → refine again; stable → proceed.

### 4. Scan parameters, validate against data

- Sweep key parameters over plausible ranges; plot the envelope. Threshold behavior (R₀ crossing 1, blow-up, extinction) flagged, not smoothed over.
- Fitted parameters: fit window vs validation window split; report both errors. Same-curve fit-and-predict is circular — forbid it.
- Compare against an analytic limit where one exists (early exponential growth, steady state) as an independent check.

### 5. Plot for the report

- Trajectories with units on axes, conditions/parameters in caption; phase portraits where they illuminate. Follow `scientific-plotting` conventions; numerical evidence (refinement table) goes in as a table, not prose.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Equations without units/conditions | Full statement + dimension check |
| Default tolerances, no refinement | Stated tol + one refinement, difference reported |
| Stiff system on explicit integrator | Implicit method, loud switch |
| Fitted curve presented as prediction | Fit/validation split, both errors |
| Point forecast from threshold system | Parameter scan + envelope + threshold flags |
| Stability condition unchecked (PDE) | CFL/Fourier number stated and satisfied |

## Output

The deliverable is the trajectory **plus its numerics**, in this order:

- **Model** — equations, units, conditions, parameter table with sources.
- **Numerics** — solver/scheme, tolerances, stability number, refinement table.
- **Results** — trajectories/phase plots with captioned conditions.
- **Scan + validation** — parameter envelope, fit-vs-validation errors.
- **Limits** — threshold behavior, valid regime, what breaks the model.

Don't pad this into a report. The refinement table is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "explicit Euler on this stiffness needs a million steps — switch to implicit", give it. When the fit only reproduces the training curve, call it calibration, not prediction.
