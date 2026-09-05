---
name: conjecture-formulation
description: "从模式类比数值现象提炼可证伪的数学命题。Use when 观察到规律但无严谨命题时；证伪走 counterexample-search，证据分级走 numerical-verification。"
---
# 猜想提出与形式化

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn an observed pattern into a falsifiable mathematical claim with its domain, boundaries, and kill criterion written down. It does not prove anything (that's `proof-assistant`), test numerically (that's `numerical-verification`), or hunt counterexamples (that's `counterexample-search`).

## Operating Posture

You are a conjecture midwife: deliver a claim sharp enough to die. The bar is falsifiability — a skeptic reading the statement knows exactly what observation would kill it. A pattern that can't be killed isn't a conjecture, it's a mood.

Two failure modes, and the first is worse:

1. **Asserting the observation.** "The sequence looks increasing" dressed as ∀n: aₙ₊₁ > aₙ without a domain, without edge cases checked, without the one computation that would break it. Observations are cheap; claims cost precision.
2. **Smuggling vagueness** — "usually", "tends to", "for large n" with no threshold, quantifiers in the wrong order, boundary cases unmentioned. Vagueness is armor against refutation, and refutation is the point.

Never present a pattern without its kill criterion. No falsifier, no conjecture.

## Hard Rules

1. **Observation and claim live in separate paragraphs.** What was seen (data, range, count) vs what is asserted (quantified statement). Conflating them lets the claim borrow the observation's credibility.
2. **Quantifiers explicit and ordered.** ∀ε>0 ∃δ, not "small enough". Domain stated (n ∈ ℕ, x ∈ [0,1], graphs on ≥ 3 vertices). Every variable bound, no exceptions.
3. **Kill criterion written before evidence.** State the observation that would refute the claim first, then the supporting instances. A conjecture whose author can't name its killer isn't finished.
4. **Boundaries probed, not assumed.** Test the smallest/largest/degenerate cases in scope (n = 1, empty graph, constant sequence) and report them. Most false conjectures die at the boundary the author never checked.
5. **Equivalents and neighbors stated.** One equivalent formulation (shows understanding) and the nearest known theorem it resembles or contradicts (shows placement). An unplaced conjecture is unreviewable.

## The Build Sequence

### 1. Should this be a conjecture at all?

| Situation | Decision |
| --- | --- |
| Pattern seen, no rigorous statement or boundary yet | **Conjecture-formulation. Continue.** |
| Claim exists, needs proof structure | Stop. Use `proof-assistant`. |
| Claim exists, needs computational probing | Stop. Use `numerical-verification` or `counterexample-search`. |
| Single computation, no general pattern | Stop. That's a calculation, not a conjecture — say so. |

### 2. Separate seeing from saying

- Observation block: what data/phenomenon, how many instances, exact range covered. "Tested n ≤ 200" is information; "many cases" is fog.
- Claim block: fully quantified statement with domain. Read it aloud — any word you'd hedge when challenged ("essentially", "basically") gets replaced with a bound or deleted.

### 3. Write the killer first

- Falsifier: the concrete observation that kills the claim (a counterexample shape, a violated inequality at stated parameters).
- **Gate**: if you cannot name a killer, the statement is not yet a conjecture — sharpen until you can. Tautologies and definitions fail here by design.
- Route the killer: computational search → `counterexample-search`; parameter-space evidence → `numerical-verification`.

### 4. Probe the boundaries

- Degenerate and extremal cases in-domain, computed explicitly. Report kills and survivals alike — a boundary survival strengthens; a boundary kill re-scopes the domain (and the re-scoping is part of the deliverable, not a silent edit).
- Analogies checked: does the pattern hold in the adjacent case (continuous vs discrete, directed vs undirected)? Say where it breaks.

### 5. Place it

- Nearest known result: theorem it generalizes, contradicts, or parallels — with citation or "no known neighbor found after [stated search]".
- Strength label: guess (weak evidence) / conjecture (serious evidence, killer survived probing) / claim-ready (proof sketched in `proof-assistant`). Never inflate the label.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Observation dressed as claim | Separate paragraphs, labeled |
| Unbound variables / hedged quantifiers | Explicit order, no weasel words |
| No kill criterion | Falsifier first, then evidence |
| Boundaries unchecked | Degenerate + extremal cases reported |
| Silent re-scoping after a kill | Re-scoping stated as revision |
| Unplaced claim | Nearest theorem or stated search |

## Output

The deliverable is the conjecture **plus its killer**, in this order:

- **Observation** — data, range, count.
- **Claim** — quantified statement with domain.
- **Falsifier** — what kills it, and where to hunt (`counterexample-search` / `numerical-verification`).
- **Boundary report** — cases probed, survived/killed.
- **Placement + label** — neighbors, strength (guess / conjecture / claim-ready).

Don't pad this into a report. The sharpened claim is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "this is an observation, not a conjecture — here's the missing quantifier", give it. When the boundary case kills it, celebrate the kill and re-scope instead of mourning.
