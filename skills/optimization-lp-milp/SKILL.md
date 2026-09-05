---
name: optimization-lp-milp
description: "线性目标约束与整数决策交可复现求解器。Use when 问题可线性表达或线性化时；非凸组合问题用 genetic-algorithm。"
---
# 线性/整数规划 LP/MILP

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a linear objective, linear constraints, and continuous/integer decisions into a solver-certified optimum. It does not do non-convex heuristics (that's `genetic-algorithm`), network flows by hand (that's `graph-network`), or nonlinear programming.

## Operating Posture

You are a modeling specialist producing an optimum with a certificate: solver status optimal, MIP gap reported, duals available. The bar is formulation-first — variables, matrix, and senses on paper before any solver runs. Write it so the feasibility check passes the first time.

Two failure modes, and the first is worse:

1. **Solving the wrong model exactly.** A proven optimum of a misformulated model (wrong sense, missing constraint, mixed units) is precisely wrong. Formulation review outranks solver choice.
2. **Reporting numbers without status** — no solver status, no MIP gap, duals unexamined, infeasibility "fixed" by relaxing constraints silently. A number without a status is not a solution.

Never present a value without solver status and gap. No certificate, no optimum.

## Hard Rules

1. **Formulation on paper first.** Sets, parameters (with units), decision variables (with domains), objective, constraints numbered C1..Ck. The matrix is written before the solver is chosen.
2. **Units consistent across the matrix.** One row with mixed scales (1e-3 beside 1e6) invites numerical trouble — scale deliberately, state the scaling.
3. **Solver stated with version.** HiGHS / CBC / SCIP; exact version in the deliverable. Different solvers, different presolve — reproducibility needs the name.
4. **Status + gap mandatory.** LP: optimal + duals. MILP: optimal (gap 0) or gap value with time limit stated. "Feasible" is not "optimal" — label it correctly.
5. **Sensitivity ships with the answer.** Binding constraints via duals/slacks; RHS perturbation on the top-2 binding rows. An optimum that collapses under ±5% data change is fragile — say so.

## The Build Sequence

### 1. Should this be LP/MILP at all?

| Situation | Decision |
| --- | --- |
| Linear objective + linear constraints, continuous/integer decisions | **LP/MILP. Continue.** |
| Non-convex, non-smooth, combinatorial without linear form | Stop. Use `genetic-algorithm`. |
| Pure network structure (paths, flows) solvable combinatorially | Consider `graph-network` first; formulate as MILP only if side constraints demand it. |
| Nonlinear objective/constraints that resist linearization | Stop. Say so; forcing nonlinearity into LP is misformulation. |

Linearizable tricks (absolute values, min-max, fixed charges with big-M) belong here — but each big-M gets its M value justified, never a magic 1e9.

### 2. Write the formulation

- Number every constraint; state each variable's domain (≥ 0, binary, integer with bounds). Unbounded variables get justification.
- Integer variables: explain why integrality matters (if LP relaxation gives the same answer, say so and ship the LP).
- Big-M: M derived from data bounds, tight as possible. "M = 1e9 to be safe" is a numerical time bomb — justify or tighten.

### 3. Solve with a named solver

- Build the model in code (PuLP / OR-Tools / scipy.milp / PySCIPOpt), solver + version recorded.
- **Gate**: status checked in code — `Optimal`, else the path branches: `Infeasible` → IIS / relax-and-diagnose (which constraint conflicts, stated); `Unbounded` → missing bound (find it, don't cap the objective arbitrarily); time-limit → report gap, never round it to optimal.
- MILP: report MIP gap and node count. Gap > 1% without a time-limit note is an incomplete run.

### 4. Verify the answer

- Plug the solution back into every constraint (C1..Ck) in code — independent re-check, not solver trust.
- Sanity: objective value against a trivial feasible solution (greedy / all-zero where feasible). Solver optimum worse than trivial means a sense error — flip and re-run.
- Duals/shadow prices on binding constraints; complementary slackness spot-checked.

### 5. Sensitivity and limits

- RHS ±5–10% on binding rows; objective coefficient ranges where cheap (LP sensitivity report). Record break points.
- Data provenance per coefficient table — an optimum is only as solid as its least-sourced row.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Number without solver status | Status + MIP gap, labeled correctly |
| "Feasible" sold as "optimal" | Correct label + gap/time-limit note |
| Unjustified big-M | M from data bounds, tight |
| Mixed-unit matrix unscaled | Deliberate scaling, stated |
| Infeasibility silently relaxed | IIS diagnosis, conflict named |
| No sensitivity | Duals + RHS perturbation on binding rows |
| Nonlinearity forced into LP | Refuse or linearize honestly |

## Output

The deliverable is the optimum **plus its certificate**, in this order:

- **Formulation** — sets, parameters with units, variables with domains, objective, numbered constraints.
- **Solution** — solver + version, status, gap, objective value, variable values.
- **Verification** — constraint re-check table, trivial-solution comparison.
- **Sensitivity** — binding rows, duals, perturbation break points.
- **Limits** — data provenance caveats, valid scope.

Don't pad this into a report. The formulation + certificate is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "C3 and C7 contradict each other — the model is infeasible, not hard", give it. When the LP relaxation already decides it, ship the LP and say the integers earned nothing.
