---
name: literature-review
description: "结构化检索、去重与主题归类，把文献变成可追溯的研究缺口表。"
disable-model-invocation: true
---
# 文献综述与研究缺口

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: turn a pile of papers into a traceable gap table the paper's introduction can cite. It does not map theorem dependencies (that's `arxiv-literature-synthesis`) and it does not write the paper (that's `paper-outline`).

## Operating Posture

You run this when the user types it, once per paper. The product is a gap table where every row traces to a verified identifier (DOI/arXiv ID). The bar is citability: a reviewer following any row lands on a real paper saying what the table claims. An uncited gap is an opinion with a table border.

Two failure modes, and the first is worse:

1. **Fabricated bibliography.** Plausible titles, wrong years, nonexistent papers. Verify every identifier against a real index before it enters the table — no identifier, no row.
2. **Summary pile with no gap.** Ten paper summaries ending in "more research is needed". A review that doesn't name the specific missing piece (method × scenario × evidence) produced reading notes, not a gap.

Never deliver the table without verified identifiers and a named gap. No gap, no review.

## Hard Rules

1. **Search strings recorded.** Database + query + date + hit count per string. "Searched widely" is not a method section.
2. **Inclusion/exclusion criteria before screening.** Years, venues, languages, method families — decided first, applied consistently, counts reported (retrieved → screened → kept).
3. **One row per paper, four columns minimum.** Method family, scenario/data, key result with numbers, limitation in the authors' or your tested terms. Rows without numbers are placeholders, labeled as such.
4. **Gap stated as method × scenario × evidence.** "No study applies [method] to [scenario] with [evidence level]" — three slots filled, each traceable to table rows. A gap none of the rows supports is invented.
5. **Theme, don't enumerate.** Group into 2–4 method families or schools; within-family comparison (what beats what, under which conditions) is the synthesis. Chronological listing without comparison is a catalog.

## The Production Sequence

### 1. Scope with the user first

- Research question in one sentence, venue type (MCM/国赛/journal), target gap use (introduction motivation vs method choice justification).
- **Gate**: can't state the question in one sentence → ask, don't retrieve. Retrieval without a question drifts by construction.

### 2. Retrieve, screen, keep

- Run the recorded strings; screen titles → abstracts → full text with counts at each funnel stage.
- Deduplicate (preprint/published = one row). Verify identifiers. Note the stop rule (saturation: new strings add no kept papers).

### 3. Tabulate and theme

- Fill the four-column rows; group into families; write the within-family verdicts (which method wins where, and where all fail — the failure zone is where the gap lives).

### 4. Name the gap — the gate

- **Gate**: gap sentence with all three slots traceable to rows. Then the paper's entry point: which section of `paper-outline` this gap feeds, in one line.

## Never Ship

| Never | Instead |
| --- | --- |
| Unverified references | Identifier checked per row |
| Unrecorded search | Strings + counts + dates |
| Post-hoc criteria | Criteria before screening |
| Numberless rows undisclosed | Labeled as placeholders |
| "More research needed" | method × scenario × evidence gap |
| Catalog without comparison | Family verdicts + failure zone |

## Output

- **Gap table** — rows with identifiers, grouped by family.
- **Funnel numbers** — retrieved → screened → kept.
- **Gap sentence** — traceable, feeding the outline.
- **Handoff** — which outline section it serves.

## Tone

Opinionated and brief. When the honest answer is "the gap you want is already filled by these two papers — here's the real adjacent gap", say so. When the funnel kept 3 papers, report 3 instead of padding with near-misses.
