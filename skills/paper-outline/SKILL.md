---
name: paper-outline
description: "为 MCM、国赛或期刊论文设计章节结构和 Claim-Evidence-Link 故事线。"
disable-model-invocation: true
---
# 论文大纲与故事线

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: turn a modeling result (or a blank page) into a section-by-section outline where every section has a claim, its evidence, and its link sentence. It does not fill LaTeX templates (that's `latex-typesetting`) and it does not polish prose (that's `polish-proofread`).

## Operating Posture

You run this when the user types it, at the start of a paper or when a draft's logic collapses. The product is an outline a coauthor can write against without asking questions. The bar is Claim-Evidence-Link per section: strip any section's claim and the outline must visibly break — decorative sections get cut here, not by reviewers later.

Two failure modes, and the first is worse:

1. **Headings without claims.** "3.2 Model solution" with no stated assertion, no evidence pointer, no word budget. A headings-only outline outsources all thinking to drafting time, where it arrives too late.
2. **Storyline told backwards.** Methods before the question they answer, conclusions the evidence can't reach, limitations hidden in future work. The outline is where the logic gets stress-tested, not where it gets decorated.

Never deliver headings without claims. No claim, no section.

## Hard Rules

1. **Venue and type first.** MCM / 国赛 / journal — structure, length, and evidence bar follow the venue. An outline that fits every venue fits none.
2. **One claim per section, written as a sentence.** Not a topic ("ARIMA results") but an assertion ("SARIMA(1,1,1)(1,1,1)₁₂ beats seasonal-naive by 18% RMSE out of sample"). Unwritable claims reveal missing results — send those back to the method skills.
3. **Evidence pointer per claim.** Figure/table number or computation to be run, named. A claim with "evidence TBD" is a flagged hole, counted and listed — never silent.
4. **Link sentences between sections.** One line each: how this section's conclusion feeds the next section's premise. Broken links are where reviewers write "disconnected".
5. **Word budget per section.** Total capped by venue; allocation follows argument weight (results and method earn the most). A 40%-background outline is a literature review wearing a paper costume.

## The Production Sequence

### 1. Fix venue, type, and question

- Venue, page/word limit, central question in one sentence. Existing draft or blank page — if a draft exists, diagnose its logic failure first (which claim lacks evidence? which link breaks?).

### 2. Draft the storyline in 3 lines

- Setup (gap + question) → Build (method + evidence) → Payoff (answer + limits). If the payoff can't be stated yet, the results aren't ready — say which method skill must run first.

### 3. Expand to sections — the gate

- Per section: claim sentence, evidence pointer, link sentence, word budget. Use the template below.
- **Gate**: read claims top-to-bottom — do they entail the payoff? Read evidence column — any TBD is a listed hole with an owner skill. Holes are fine; hidden holes are not.

<outline-template>

## Section: [number + title]

**Claim:** [one assertive sentence]

**Evidence:** [figure/table/computation reference, or TBD → owning skill]

**Link:** [how this conclusion feeds the next section]

**Budget:** [words]

</outline-template>

### 4. Hand off

- Name the next skills in order (method runs → `figure-table-generation` → `latex-typesetting` → `citation-bibliography` → `polish-proofread` → `reproducibility-checklist`). The outline is done when someone else could execute that chain from it alone.

## Never Ship

| Never | Instead |
| --- | --- |
| Topic headings | Claim sentences |
| Evidence TBD, unlisted | Holed, counted, owned |
| Missing link sentences | Link per section |
| No word budget | Venue-capped allocation |
| Payoff exceeding evidence | Stress-test entailment top-to-bottom |

## Output

- **Outline** — sections in the template above.
- **Hole list** — TBD evidence with owning skills.
- **Handoff chain** — next skills in order.

## Tone

Opinionated and brief. When the honest answer is "section 4's claim needs a result you don't have — run the model first", send it back. When the draft's logic breaks between sections 2 and 3, name the break instead of renumbering around it.
