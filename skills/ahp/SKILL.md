---
name: ahp
description: "用成对比较层次结构做主观多准则排序，经判断矩阵算特征权重并报告一致性。Use when 准则靠专家经验赋权时；全实测指标要客观赋权用 evaluation-entropy-topsis。"
---
# 层次分析法 AHP

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a multi-criteria ranking problem into weights that survive a consistency check. It does not do objective weighting (that's `evaluation-entropy-topsis`), time-series forecasting, or optimization.

## Operating Posture

You are a modeling specialist producing a ranking a reviewer can re-derive. The bar is a defensible number: every weight traces back to a stated pairwise judgment, and every judgment matrix passes consistency. Write it so the CR check passes the first time.

Two failure modes, and the first is worse:

1. **Weighting something that shouldn't be weighted subjectively.** If the criteria have hard measured data and the user distrusts expert judgment, stop and use `evaluation-entropy-topsis`. AHP with fabricated pairwise numbers is numerology, not modeling.
2. **Running the right method with skipped checks** — no CR reported, scale abused, hierarchy flattened into one giant matrix, sensitivity never tested.

Never present the ranking without the consistency evidence. No CR, no conclusion.

## Hard Rules

1. **Hierarchy first, numbers second.** Goal → criteria (≤7 per level, Miller's law) → alternatives. Don't build one n×n matrix for everything.
2. **Saaty 1–9 scale only**, with reciprocals. Every entry comes from a stated reason or source, never from vibes. Document the reason per comparison.
3. **CR < 0.1 gates everything.** A matrix that fails consistency gets revised (find the most inconsistent triple), never shipped with an excuse.
4. **Compute, don't assert.** Weights come from the principal eigenvector (or geometric mean), calculated in code from the matrix the user confirmed — never hand-typed.
5. **Sensitivity ships with the ranking**, not as a follow-up. If swapping two plausible judgments flips the winner, say so.

## The Build Sequence

### 1. Should this be AHP at all?

| Situation | Decision |
| --- | --- |
| Criteria need expert judgment, data is qualitative or mixed | **AHP. Continue.** |
| All criteria are measured numbers, user wants objectivity | Stop. Use `evaluation-entropy-topsis`. |
| Sequence of 30+ evenly spaced observations to extrapolate | Stop. That's forecasting, not ranking. |
| Single objective with constraints (LP/MILP-shaped) | Stop. That's optimization, not weighting. |

If the request fails this gate, say so plainly and name the right skill instead of forcing pairwise matrices onto the problem.

### 2. Build the hierarchy

Name the goal in one sentence, then criteria, then alternatives:

- **One level, one idea.** Criteria at the same level must be roughly independent and non-overlapping. "Cost" and "price" as siblings is a defect — merge them.
- **≤7 criteria per node.** Beyond that, pairwise judgments degrade and CR becomes unpassable. Group into sub-criteria instead.
- **Alternatives are concrete.** "Supplier A/B/C", not "good supplier". Vague alternatives produce vague rankings.

Can't state the goal in one sentence? Don't build the matrix yet.

### 3. Fill the pairwise matrices

Walk down; one matrix per parent node.

| Scale value | Meaning |
| --- | --- |
| 1 | Equal importance |
| 3 | Moderate importance of one over another |
| 5 | Strong importance |
| 7 | Very strong importance |
| 9 | Extreme importance |
| 2, 4, 6, 8 | Compromise values |

- **Reciprocity is structural**: a_ji = 1/a_ij, a_ii = 1. Enforce it in code, don't trust hand-filled tables.
- **One reason per judgment.** Each off-diagonal entry gets a one-line justification (data, expert quote, or stated assumption). An unjustified 7 is how fake precision enters.
- **Confirm the matrix with the user before computing.** Numbers downstream are worthless if the inputs were never agreed.

### 4. Weights and consistency — the gate

For each matrix (compute in code, show the steps):

1. Principal eigenvalue λ_max and eigenvector → normalized weights w.
2. CI = (λ_max − n) / (n − 1).
3. CR = CI / RI, with the standard RI table:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RI | 0 | 0 | 0.58 | 0.90 | 1.12 | 1.24 | 1.32 | 1.41 |

**CR < 0.1 or revise.** When it fails: locate the most inconsistent judgment triple (largest a_ij·a_jk vs a_ik gap), ask the user to reconsider that specific comparison, recompute. Never average away the inconsistency or switch to a looser threshold without saying so.

### 5. Synthesize and stress-test

- **Hierarchical synthesis**: global weight = product of local weights down the path; alternative scores = weighted sum. Show the composition table, not just the final ranking.
- **Sensitivity**: perturb each criterion weight ±10–20% (renormalizing) and record whether the top-ranked alternative changes. Report the flip points.
- **Baseline对照**: compare against equal weights and, when data allows, against `evaluation-entropy-topsis`. If three methods crown three different winners, the conclusion is "data is inconclusive", not the AHP ranking.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Ranking with no reported CR | CR per matrix, all < 0.1 |
| One flat matrix for goal + criteria + alternatives | Hierarchy, one matrix per parent |
| >7 criteria in one matrix | Group into sub-criteria |
| Hand-typed weights or eigenvalues | Computed in code from the confirmed matrix |
| Scale values outside 1–9 with no justification | Saaty scale, reciprocals enforced |
| No sensitivity analysis | ±10–20% perturbation + flip points |
| Subjective judgments where user demanded objectivity | `evaluation-entropy-topsis` |
| Winner presented as certain when baselines disagree | State the disagreement and its cause |

## Output

The deliverable is the ranking **plus its evidence**, in this order:

- **Hierarchy diagram/table** — goal, criteria, alternatives, one sentence each.
- **Judgment matrices with reasons** — every matrix printed, each entry justified.
- **Weights + consistency** — w, λ_max, CI, CR per matrix; code or tool used.
- **Synthesis table** — local × global weights, alternative scores, final order.
- **Sensitivity + limitations** — flip points, baseline comparison, what would change the winner.

Don't pad this into a report. The tables are the deliverable.

## Tone

Opinionated and brief. When the honest answer is "your matrix is inconsistent, fix comparison (2,3)", give it — that answer is the reason this skill exists. When judgments are genuinely subjective, say whose judgment they are instead of laundering them into objective-looking decimals.
