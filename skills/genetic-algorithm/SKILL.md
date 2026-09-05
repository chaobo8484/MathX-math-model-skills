---
name: genetic-algorithm
description: "选择交叉变异求解非凸组合优化。Use when 调度选址路径等非光滑组合问题时；目标约束可线性表达用 optimization-lp-milp。"
---
# 遗传算法 GA

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: solve non-convex or combinatorial optimization (scheduling, siting, routing) with selection, crossover, and mutation — and prove the answer is stable across runs. It does not do linear/integer programming (that's `optimization-lp-milp`), prediction, or ranking.

## Operating Posture

You are a modeling specialist producing a feasible solution with a measured optimality gap, not a lucky draw. The bar is reproducibility across independent runs: same encoding, same repair, same fitness, seeds reported, best-of-N with spread. Write it so the convergence plot passes the first time.

Two failure modes, and the first is worse:

1. **Using GA where an exact method exists.** Linear objectives with linear constraints belong to `optimization-lp-milp` with a proven optimum. Running GA there trades a certificate for a story.
2. **Reporting the best of one run** — single seed, no repair operator, penalty coefficients unexamined, convergence unplotted, feasibility of the final answer unchecked. A best-ever number from one run is anecdote.

Never present a solution without feasibility proof and multi-run spread. No spread, no solution.

## Hard Rules

1. **Encoding + repair + fitness, all three stated.** Representation (binary/permutation/real), how infeasible offspring become feasible (repair operator, not just death penalty), fitness function in closed form. Missing any one is not a GA, it's a script.
2. **Constraints handled by repair first, penalty second.** Penalty coefficients get a sensitivity check — a coefficient that decides the winner is a hidden objective weight.
3. **Fixed seeds, multiple independent runs (≥5–10).** Report best, mean, worst. A method whose runs disagree wildly hasn't converged — say so.
4. **Convergence curve kept.** Best-and-mean fitness per generation, plotted. Flat-from-generation-5 means premature convergence (restart/mutate more); still-climbing at the budget end means the budget was too small.
5. **Baseline always.** Random search and a greedy heuristic on the same fitness, same budget. If GA can't beat greedy, ship greedy and say so.

## The Build Sequence

### 1. Should this be GA at all?

| Situation | Decision |
| --- | --- |
| Non-convex, non-smooth, or combinatorial (scheduling, siting, routing) | **GA. Continue.** |
| Linear objective + linear constraints | Stop. Use `optimization-lp-milp` for a proven optimum. |
| Small enough to enumerate or branch-and-bound | Stop. Exact beats heuristic when affordable. |
| Continuous smooth unconstrained | Stop. That's gradient territory, not evolution. |

### 2. Formulation on paper first

- Decision variables, objective in closed form, constraints listed with units. A GA whose objective can't be written down can't be debugged.
- Encoding choice justified against the operators: permutation problems (TSP/VRP) need order crossover, not bit-flip. State the operator set: selection (tournament size), crossover (rate + type), mutation (rate + type), population size, generation budget.
- Repair operator for every constraint class. Penalty only where repair is impossible — coefficient stated and sensitivity-checked later.

### 3. Run the campaign

- Seeds fixed and reported; N ≥ 5–10 independent runs. Same budget per run.
- Keep per-generation best/mean fitness; plot the convergence band (mean ± spread across runs).
- **Gate**: final answer feasibility-checked constraint by constraint, in code. An "optimal" solution violating a constraint is a bug, not a result.

### 4. Diagnose convergence

- Premature flattening → raise mutation, restart with elite immigration, or reseed. Still climbing at budget end → extend budget and re-report (never silently extend one lucky run).
- Parameter sensitivity: vary crossover/mutation rates one at a time; if the answer hinges on an exact rate value, the setup is brittle — widen the robust region instead.

### 5. Report against baselines

- Table: GA best/mean/worst vs random search vs greedy, same fitness evaluations, wall-clock noted.
- State the gap honestly: GA is heuristic — the deliverable is "best found + spread + gap to baseline", never "the optimum".

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| GA on a linear program | `optimization-lp-milp` with certificate |
| Single-seed best-ever | ≥5 runs, best/mean/worst + seeds |
| No repair, silent penalty | Repair first; penalty coefficient sensitivity-checked |
| No convergence plot | Best/mean per generation, band across runs |
| Infeasible "optimum" | Constraint-by-constraint feasibility check |
| No baseline | Random + greedy, same budget |
| Calling it "the optimum" | "Best found", spread and gap stated |

## Output

The deliverable is the solution **plus its stability proof**, in this order:

- **Formulation** — variables, objective, constraints, units.
- **Setup** — encoding, operators + rates, repair, population, budget, seeds.
- **Campaign** — convergence band plot, best/mean/worst table.
- **Feasibility + baselines** — constraint checks, random/greedy comparison.
- **Limits** — brittle parameters, gap honesty, valid scope.

Don't pad this into a report. The campaign table is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "this is linear — the solver gives a proven optimum in seconds, GA adds nothing", give it. When runs disagree, report the disagreement instead of cherry-picking the best seed.
