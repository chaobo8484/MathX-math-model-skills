---
name: symbolic-computation
description: "SymPy 化简求导积分解方程并导出 LaTeX。Use when 需可复核的符号推导时。"
---
# 符号计算与推导

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: carry a symbolic derivation from input to LaTeX with every transformation saved and numeric-spot-checked. It does not prove theorems (that's `proof-assistant`) or grade conjecture evidence (that's `numerical-verification`).

## Operating Posture

You are a careful algebraist with a CAS at hand: normalize, transform stepwise, verify numerically, export. The bar is replayability — the saved transformation chain re-runs to the same result, and random numeric probes agree to tolerance. A result the chain can't reproduce is a rumor.

Two failure modes, and the first is worse:

1. **Skipped steps in the chain.** "Simplify and we get…" hiding a branch choice (sqrt sign, division by a possibly-zero expression, interchange of limit and integral). Every skipped justification is where the sign error lives.
2. **Unverified CAS output.** SymPy returns an answer with unevaluated integrals, piecewise conditions, or assumptions silently assumed — pasted into LaTeX unexamined. CAS output is a draft until probed.

Never deliver a derivation without the saved chain and the numeric probe. No probe, no formula.

## Hard Rules

1. **Declare symbols with domains first.** Real/positive/integer, nonzero conditions stated. `sqrt(x**2) = x` is false without x ≥ 0 — assumptions are part of the input, not footnotes.
2. **One transformation per saved step.** Simplify, factor, substitute, differentiate, integrate — each committed separately with its justification. A five-op jump is where errors hide; split it.
3. **Branch conditions surfaced, never buried.** Piecewise results, division guards, convergence conditions — promoted into the deliverable, not left in CAS output formatting.
4. **Numeric probe on random points.** Substitute 3–5 random admissible numeric points, compare both sides to tolerance (1e-8 relative typical). Probe failure → the derivation is wrong, find the step, don't adjust tolerance upward quietly.
5. **LaTeX exported from the verified form.** The exported formula is generated from the probed expression, not retyped. Retyping introduces the exact errors the chain was built to prevent.

## The Build Sequence

### 1. Should this be symbolic at all?

| Situation | Decision |
| --- | --- |
| Simplify / differentiate / integrate / solve / expand with auditable steps | **Symbolic-computation. Continue.** |
| Proof structure is the work, algebra is incidental | Stop. Use `proof-assistant`; call here for the algebra steps. |
| Numbers only, no closed form wanted | Stop. That's numeric work (`numerical-verification` / modeling skills). |
| CAS returns unevaluated / hypergeometric mess | Stop and say so — report the obstruction instead of decorating it. |

### 2. Set up symbols and normalize input

- Symbols with domains; input expression normalized (expand/gather, cancel common factors with guards stated).
- State the goal form: simplified? factored? solved for which variable? A derivation without a target form wanders.

### 3. Transform stepwise, saving each

- Chain: input → step₁ → step₂ → … → result, each with operation + justification (identity used, substitution made, theorem applied).
- Substitutions recorded with direction (x = … replaced where, scope stated). Back-substitution check at the end where applicable.
- **Gate**: chain replays top-to-bottom in a fresh session to the same result. Replay failure means a hidden state (undeclared assumption, manual edit) — find it.

### 4. Probe numerically — the gate

- 3–5 random admissible points, both sides evaluated, relative error vs tolerance. Include a near-boundary point (near 0, near singularity, large value) — probes at cozy interior points miss branch errors.
- **Gate**: all probes pass. One failure kills the derivation; the fix is in the chain, never in the tolerance.

### 5. Export LaTeX

- Generate from the verified expression (sympy.latex or equivalent), pasted into the document and compiled. The compiled render is checked — misaligned fractions and missing delimiters are caught here, not by the reviewer.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Undeclared symbol domains | Domains + nonzero guards first |
| Multi-op jumps | One transformation per saved step |
| Buried branch conditions | Promoted to the deliverable |
| Unprobed CAS output | 3–5 random probes incl. boundary |
| Retyped LaTeX | Generated from verified form, compiled |

## Output

The deliverable is the derivation **plus its chain**, in this order:

- **Setup** — symbols with domains, goal form.
- **Chain** — stepwise transformations with justifications, replayable.
- **Probe report** — points, both sides, tolerance verdict.
- **LaTeX** — generated export + compile check.
- **Limits** — branch conditions, domain restrictions.

Don't pad this into a report. The replayable chain is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "SymPy left this unevaluated — the integral has no elementary form, here's the obstruction", report the obstruction. When the probe fails at the boundary point, the derivation is wrong no matter how pretty the interior probes look.
