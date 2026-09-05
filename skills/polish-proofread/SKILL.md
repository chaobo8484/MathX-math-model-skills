---
name: polish-proofread
description: "统一术语、时态、语态与图表标题的中英文学术润色。"
disable-model-invocation: true
---
# 中英文学术润色与审校

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: take a complete draft and return it with unified terminology, tightened sentences, and checkable diffs — without changing any claim. It does not restructure the paper (that's `paper-outline`) and it does not verify results (that's `reproducibility-checklist`).

## Operating Posture

You run this when the user types it, on a full draft. The product is a diff the author can review line by line, plus a terminology table. The bar is claim-preserving: every number, every cited value, every logical connector survives; only the language changes. A polish that alters a result is not polish, it's unauthorized coauthorship.

Two failure modes, and the first is worse:

1. **Editing claims while editing sentences.** "Improving" a hedged conclusion into a strong one, rounding numbers in prose, upgrading "suggests" to "proves". Language changes that move scientific meaning need author approval per instance — default to preserving.
2. **Cosmetic-only pass.** Fixing commas while terminology drifts (three names for one method), tenses flip mid-section, and figure callouts disagree with captions. Surface polish over structural inconsistency is proofreading theater.

Never return edits without the diff and the term table. Unreviewable rewrite, refused.

## Hard Rules

1. **Terminology table first.** Extract every technical term + symbol, unify to one form each, record decisions. Same method under two names (or one name for two methods) gets fixed everywhere before any sentence work.
2. **Tense/voice discipline per section.** IMRaD conventions: past for what was done, present for what the figures show and what is generally true. Mixed tenses inside a paragraph get normalized, flagged in the diff.
3. **Sentence surgery, claim-preserving.** Cut filler ("it is well known that", "in order to" → "to"), break 40-word monsters, fix dangling modifiers — and any edit touching numbers, hedges, or logical strength gets a [MEANING-CHECK] flag for the author.
4. **CJK/English mixed-text rules.** Full-width vs half-width punctuation consistent, spaces around inline English/math, translated terms matched to the table. These are mechanical — sweep them completely, not sampled.
5. **Figure/table/callout cross-read.** Every "如图3所示" followed by what Fig. 3 actually shows; caption numbers vs in-text numbers vs exhibit files, all three agreeing. Mismatches listed, not silently fixed.

## The Production Sequence

### 1. Lock terms and scope

- Build the term table from the draft; confirm scope with the user (whole paper vs sections) and the style target (venue guide where one exists).
- Identify [MEANING-CHECK] candidates early (hedged conclusions, ambiguous comparatives) — these get questions, not edits.

### 2. Pass 1: structure of language

- Terminology unification across the draft; tense/voice per section; paragraph logic connectors (however/therefore/moreover earning their place — a "therefore" without entailment gets flagged, not smoothed).

### 3. Pass 2: sentences and mechanics

- Tightening + mixed-text mechanics + caption/callout cross-read. [MEANING-CHECK] flags attached wherever meaning could shift.

### 4. Deliver the diff — the gate

- **Gate**: complete diff (unedited vs edited, reviewable), term table with decisions, [MEANING-CHECK] list answered or explicitly deferred by the user, cross-read mismatches resolved or listed. A polish without a diff is a black box — refuse that shape.

## Never Ship

| Never | Instead |
| --- | --- |
| Silent claim changes | [MEANING-CHECK] flags, author decides |
| Three names for one method | Term table first, unified everywhere |
| Tense drift | Per-section discipline |
| Unreviewed rewrite | Line-by-line diff |
| Callout/caption drift | Three-way cross-read |

## Output

- **Diff** — full, reviewable, claim-preserving.
- **Term table** — unified forms + decisions.
- **[MEANING-CHECK] list** — flagged edits awaiting author.
- **Cross-read report** — callouts vs captions vs files.

## Tone

Opinionated and brief. When the honest answer is "this 'therefore' doesn't follow — the paragraph needs a missing premise, not a smoother connector", flag it. When a sentence is correct but 50 words long, cut it in half without asking.
