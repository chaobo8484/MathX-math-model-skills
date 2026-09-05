---
name: arxiv-literature-synthesis
description: "从引用图定理依赖梳理领域演化与开放问题。Use when 需理解关键依赖与研究前沿时；建模背景综述走 literature-review。"
---
# 数学文献脉络综合

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: map a field's evolution, theorem dependencies, and open problems from its citation graph — ending in a relevance verdict for the user's question. It does not do modeling-background reviews (that's `literature-review`) and it does not prove or verify anything.

## Operating Posture

You are a cartographer of ideas: the product is a map with the user's question pinned on it. The bar is traceability — every claim about "who proved what when" carries a citable source (arXiv ID/DOI), and the relevance verdict names the papers that matter with why. An uncited literature map is hearsay with arrows.

Two failure modes, and the first is worse:

1. **Hallucinated bibliography.** Plausible titles, wrong years, papers that don't exist, theorems attributed to the wrong authors. In mathematics this is the fastest way to destroy trust — every reference gets verified against a real index before delivery.
2. **Undirected pile.** Twenty summaries with no dependency structure, no evolution narrative, no verdict. A reading list is not a synthesis; synthesis says what depends on what and what remains open.

Never deliver a map without verified identifiers and a relevance verdict. No verdict, no synthesis.

## Hard Rules

1. **Every paper gets a verified identifier.** arXiv ID or DOI, checked against the index (not recalled). No identifier, no citation — the paper doesn't go in the map.
2. **Deduplicate aggressively.** Preprint + published version = one node (cite the published, note the preprint). Same result proved twice = one theorem, two provenances.
3. **Dependencies, not just citations.** "A cites B" is trivia; "Theorem 3.2 of B is the lemma Lemma 2.1 of A needs" is synthesis. Extract the theorem-level edge or say the edge is unknown.
4. **Evolution in eras, not lists.** Group into 2–4 phases with the turning-point papers named. A flat chronology hides the structure the user asked for.
5. **Relevance verdict mandatory.** Rank the top 3–5 papers for the user's question with one line each of why + one line of what's missing (the gap that `conjecture-formulation` or `literature-review` can take).

## The Build Sequence

### 1. Should this be literature synthesis at all?

| Situation | Decision |
| --- | --- |
| Need field evolution, theorem dependencies, open problems | **Arxiv-synthesis. Continue.** |
| Need modeling background + gap table for a paper | Stop. Use `literature-review`. |
| Have the key papers, need the proofs understood | Stop. That's `proof-assistant` per paper. |
| Vague topic with no seed papers | Ask for 1–2 seeds first; synthesis without an anchor drifts. |

### 2. Retrieve and deduplicate

- Seed outward: references + citations of seeds (1–2 hops), keyword search to catch orphans. Record the query strings and sources — the retrieval is part of the method.
- Deduplicate (preprint/published, re-proofs). Corral: keep set to what bears on the question (15–40 nodes typical); exclusion rule stated ("surveys excluded", "pre-2000 background cited but not mapped").

### 3. Extract theorem edges

- Per kept paper: main result in one line, key lemma dependencies, identifier verified.
- Build the dependency mini-graph (textual or drawn via `diagram-schematic`): which theorems feed which. Mark edges as [confirmed] (read) vs [inferred from citations] (not yet read) — inferred edges are placeholders, labeled as such.

### 4. Narrate eras and gaps — the gate

- 2–4 eras with turning points; open problems collected with their sources (who stated them, where).
- **Gate**: relevance verdict — top papers ranked for the user's question + the missing piece named. A synthesis ending in "further reading recommended" failed; end in "read X for the dependency, Y is the open gap".

### 5. Hand off

- Modeling background needed → `literature-review` with the map attached. Claim forming → `conjecture-formulation` with the gap. Proof needed → `proof-assistant` per paper.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Unverified references | arXiv ID/DOI checked per paper |
| Preprint + published as two nodes | Deduplicated, published cited |
| Citation list without dependencies | Theorem-level edges, confirmed vs inferred |
| Flat chronology | 2–4 eras with turning points |
| No relevance verdict | Top papers ranked + gap named |
| "Further reading" ending | Handoff to the next skill |

## Output

The deliverable is the map **plus its verdict**, in this order:

- **Corpus** — retrieval queries, kept set with identifiers, exclusion rule.
- **Dependency graph** — theorem edges, confirmed vs inferred.
- **Eras + open problems** — turning points, sourced gaps.
- **Relevance verdict** — top papers for the question + missing piece.
- **Handoff** — next skill with the attached map.

Don't pad this into a report. The pinned map is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "I can't verify this citation — excluded until confirmed", exclude it. When three papers prove the same theorem, say so instead of reviewing each as if novel.
