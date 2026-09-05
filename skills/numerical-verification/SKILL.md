---
name: numerical-verification
description: "边界扫描与可复现实验评估猜想证据强度。Use when 用计算支持质疑或探索命题时；找反例走 counterexample-search。"
---
# 数值验证与证据分级

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: probe a mathematical claim computationally and grade the result supported / open / refuted — with the coverage stated. It does not formulate claims (that's `conjecture-formulation`), prove them (that's `proof-assistant`), or minimize counterexamples (that's `counterexample-search`).

## Operating Posture

You are an evidence grader, not a cheerleader: design the probe to kill the claim, report the coverage honestly, assign the grade the data earns. The bar is stated coverage — parameter ranges, sample counts, edge cases probed — so "supported" means something bounded. Numerical support is not proof and must never be presented as such.

Two failure modes, and the first is worse:

1. **Probing the cozy interior.** Random tests far from boundaries, moderate parameters, the regime where everything works. Claims die at extremes and degeneracies — a probe that avoids them is theater.
2. **Grade inflation.** "Verified" from 50 random points, "confirmed" from one parameter slice, silence about the untested region. The untested region is part of the verdict.

Never present a grade without its coverage map. No coverage, no grade.

## Hard Rules

1. **Claim restated with domain before any code.** Import from `conjecture-formulation` where available; a probe of a vague claim measures nothing — sharpen first.
2. **Adversarial design: extremes first.** Boundary values, degenerate inputs, large/small parameters, near-singularities. The probe budget spends on killers, not confirmations.
3. **Coverage recorded as data.** Ranges swept, grid density or sample counts, seeds. "Extensively tested" without numbers is not a coverage statement.
4. **Three grades only, criteria fixed.** SUPPORTED (all probed points pass incl. extremes) / OPEN (passes interior, extremes untested or ambiguous) / REFUTED (one failing point, reproduced — hand to `counterexample-search` for minimization). No fourth grade like "basically true".
5. **Numerics distinguished from proof, in writing.** The deliverable says what computation shows and what remains unproven, in separate sentences. Conflating them misleads the next reader into citing computation as theorem.

## The Build Sequence

### 1. Should this be numerical verification at all?

| Situation | Decision |
| --- | --- |
| Claim exists, needs computational support/challenge/exploration | **Numerical-verification. Continue.** |
| Hunting a falsifier specifically | Stop. Use `counterexample-search` (it minimizes; this skill grades). |
| Claim needs proof structure | Stop. Use `proof-assistant`. |
| No precise claim yet | Stop. Use `conjecture-formulation` first. |

### 2. Restate and design the probe

- Claim + domain written down. Identify the dangerous regions: boundaries of the domain, degenerate cases, asymptotic regimes, known hard instances.
- Probe plan: grid (ranges + density) and/or random (count + seed + distribution), extreme cases listed individually. Precision/tolerance stated (float error vs genuine violation needs a threshold — set it before running).

### 3. Run with seeds and record coverage

- Fixed seeds, rerunnable scripts. Every number traceable to a run.
- Coverage map filled as runs complete: region × density × verdict cells. Empty cells are OPEN by default, never SUPPORTED.

### 4. Grade — the gate

- **Gate**: grade assigned by the fixed criteria, with the coverage map attached. SUPPORTED requires extremes probed and passing; anything less is OPEN with the untested region named.
- REFUTED: reproduce the failing point independently (fresh seed/run), then hand the instance to `counterexample-search` — do not minimize here.
- Near-misses (failures within numerical tolerance of the boundary) get reported as near-misses with the tolerance analysis, not rounded into passes.

### 5. Report evidence, not proof

- Deliverable states the grade, the coverage, and the precise gap to proof. If the grade is OPEN, the next probe (what region, what method) is specified — an open verdict with no next step is a shrug.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Interior-only probing | Extremes + degeneracies first |
| "Verified/confirmed" from samples | SUPPORTED/OPEN/REFUTED with coverage |
| Unstated coverage | Ranges, counts, seeds recorded |
| Tolerance chosen after seeing results | Threshold set before running |
| Computation presented as proof | Separate sentences, gap named |
| Minimizing a refutation here | Hand to counterexample-search |

## Output

The deliverable is the grade **plus its coverage**, in this order:

- **Claim + domain** — restated, sharpened if needed.
- **Probe design** — dangerous regions, grid/random plan, tolerance.
- **Coverage map** — region × density × verdict.
- **Grade** — SUPPORTED / OPEN / REFUTED with justification.
- **Next step** — gap to proof, or handoff for refutations.

Don't pad this into a report. The graded coverage map is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "passes interior, extremes untested — OPEN, not supported", grade it OPEN. When one point fails, reproduce it and hand it off instead of re-running with a friendlier seed.
