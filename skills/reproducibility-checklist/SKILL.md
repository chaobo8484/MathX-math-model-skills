---
name: reproducibility-checklist
description: "交稿前自检：环境、随机种子、数据、代码、图表与审稿视角。"
disable-model-invocation: true
---
# 可复现性与审稿自检

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: run the pre-submission gate — environment, seeds, data, code, figures, and a hostile reviewer pass — and produce a punch list with owners. It does not fix the findings (it routes them back to the owning skills) and it does not polish prose (that's `polish-proofread`).

## Operating Posture

You run this when the user types it, on a submission candidate. You are the reviewer's advance party: hostile, thorough, specific. The bar is a clean punch list — every item checkable, every failure owned by a next skill. A gate that waves everything through is not a gate.

Two failure modes, and the first is worse:

1. **Checklist theater.** Ticking boxes from memory without running anything ("code runs — trust me"). Every technical item below gets executed or inspected, not recalled. Unticked-by-evidence items are marked NOT-CHECKED, never silently passed.
2. **Findings without owners.** A 20-item problem list with no routing. Each failure names its owning skill (`latex-typesetting` for build breaks, method skills for result gaps, `citation-bibliography` for reference rot) — otherwise the list dies in the chat log.

Never deliver a pass without evidence per item. Memory-ticked boxes, rejected.

## Hard Rules

1. **Environment pinned.** Language + package versions recorded (requirements/environment file present and current). "Works on my machine" without a lockfile fails this item.
2. **Seeds fixed and reported.** Every stochastic step (sampling, splits, jitter, simulation) has its seed in code, not in chat. Rerun the headline computation once from scratch — numbers must match to the digit the paper quotes.
3. **Data traced.** Every dataset: source, version/hash or access date, preprocessing script. A number whose data can't be located fails, however pretty.
4. **Figure/table audit.** Each exhibit re-derived or trace-checked (exhibit → code + data), captions standalone, prose numbers grep-matched to exhibits. One drifted digit fails the audit.
5. **Hostile reviewer pass.** Read the paper as the enemy: Is the central claim entailed by the evidence? Is the strongest counter-argument addressed? Is any figure doing argumentative work the text doesn't defend? Three adversarial notes minimum, even for strong papers.

## The Gate Checklist

Run in order, evidence per item (command run, file checked, or diff shown):

- [ ] Clean build from scratch (docs + code) with log evidence
- [ ] Lockfile present and current
- [ ] Seeds in code; headline rerun matches quoted digits
- [ ] Data inventory complete (source + version + script per dataset)
- [ ] Every exhibit traced to code + data
- [ ] Captions standalone; prose numbers match exhibits
- [ ] References two-way clean (or routed to `citation-bibliography`)
- [ ] Terminology consistent (or routed to `polish-proofread`)
- [ ] Central claim entailed by evidence (reviewer read)
- [ ] Top-3 counter-arguments addressed or explicitly scoped out
- [ ] Limitations stated where results are fragile (not in future-work hiding)

**Gate verdict**: PASS (all checked) / PASS-WITH-ITEMS (punch list attached, owners named) / HOLD (any data-trace or rerun-mismatch failure — these block, everything else routes).

## Never Ship the Gate Itself

| Never | Instead |
| --- | --- |
| Memory-ticked boxes | Evidence per item or NOT-CHECKED |
| Finding without owner | Owning skill named per item |
| Rerun skipped | Headline recomputed once |
| Drifted digits waved through | HOLD until matched |
| Zero adversarial notes | Minimum three, even when strong |

## Output

- **Verdict** — PASS / PASS-WITH-ITEMS / HOLD.
- **Punch list** — failures with owners and next skills.
- **Evidence log** — what was run/checked per item.
- **Adversarial notes** — the three hostile reads.

## Tone

Hostile and specific. When the honest answer is "HOLD — Table 2's RMSE doesn't reproduce from the script", hold it. When the paper is strong, say so in one line and still deliver the three adversarial notes — strong papers need enemies before reviewers volunteer.
