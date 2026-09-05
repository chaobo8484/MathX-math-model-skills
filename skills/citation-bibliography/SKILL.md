---
name: citation-bibliography
description: "清洗 BibTeX，核对文内引用与参考文献表双向一致。"
disable-model-invocation: true
---
# 引用与参考文献管理

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: make in-text citations and the reference list agree with each other and with the venue style — every key cited, every entry real. It does not find the literature (that's `literature-review` / `arxiv-literature-synthesis`).

## Operating Posture

You run this when the user types it, on a near-final draft. The product is a two-way-clean bibliography: every \cite resolves, every .bib entry is cited (or knowingly kept), every entry has the fields the style needs. The bar is the compiler plus a manual pass — BibTeX warnings at zero and a human eye on author names.

Two failure modes, and the first is worse:

1. **Ghost references.** Entries that don't exist, wrong years, mangled author names (especially transliterated CJK names), DOIs pointing nowhere. One ghost reference tells a reviewer the whole list is untrustworthy.
2. **One-way integrity.** In-text keys with no .bib entry ([?] in the PDF) or .bib entries nothing cites. Either direction broken means the document wasn't built clean — see `latex-typesetting`'s log gate.

Never deliver a bibliography without the two-way check. Unresolved keys, unfinished job.

## Hard Rules

1. **Style fixed first.** GB/T 7714 / APA / venue .bst / biblatex style — one style, recorded. Mixed styles (numbered in text, author-year in list) fail instantly.
2. **Two-way check, both directions counted.** Text→list: every citation key resolves (grep the log for undefined). List→text: every entry cited at least once, or explicitly marked as further-reading with user approval.
3. **Author names verified by eye.** Initials vs full names consistent per style; CJK transliterations checked against the source; "et al." thresholds per style (know yours). Automated tools mangle names routinely — this line item is manual by design.
4. **Required fields per entry type.** Article: journal, volume, pages, year, DOI. Book: publisher, address/year. Online: access date + URL. Missing-field warnings driven to zero, not scrolled past.
5. **Keys stable and meaningful.** AuthorYearTitle-word keys; no auto-generated gibberish that collides after edits. Key changes get a full-document recheck.

## The Production Sequence

### 1. Fix style and inventory

- Style recorded; .bib file(s) located; entry count + key list extracted. Duplicates merged (same DOI twice under different keys is the classic).

### 2. Clean entries

- Normalize fields per type; verify DOIs resolve (spot-check, especially pasted ones); author names eye-checked. BibTeX/biber warnings to zero.

### 3. Two-way integrity — the gate

- **Gate**: full compile; undefined-citation warnings zero; uncited entries zero-or-approved; a final grep for [?] in the PDF. Any failure → fix, recompile, re-grep.

### 4. Hand off

- Back to `latex-typesetting` for the final build proof; forward to `polish-proofread` (citation prose around the keys still needs reading) and `reproducibility-checklist`.

## Never Ship

| Never | Instead |
| --- | --- |
| Mixed citation styles | One style, recorded first |
| [?] in the PDF | Two-way check to zero |
| Unverified author names | Manual eye pass |
| Missing-field warnings ignored | Driven to zero per type |
| Gibberish keys | Meaningful stable keys |

## Output

- **Clean .bib** — deduplicated, field-complete.
- **Integrity report** — both directions counted, warnings zero, evidence shown.
- **Style record** — style name + any venue deviations.
- **Handoff** — rebuild + polish + gate chain.

## Tone

Opinionated and brief. When the honest answer is "three of these DOIs don't resolve — they're ghosts until proven otherwise", say so. When the author list has four transliteration variants of one name, unify and note it.
