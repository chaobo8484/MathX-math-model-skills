---
name: latex-typesetting
description: "把内容填入官方 LaTeX 模板并编译出 PDF，按报错日志迭代修错。"
disable-model-invocation: true
---
# LaTeX 排版与模板填充

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A production skill, human-invoked. It does ONE thing: fill an official template block by block and iterate on the compiler log until a clean PDF comes out. It does not design the paper's logic (that's `paper-outline`) and it does not draw figures (that's `publication-figure` / `figure-table-generation`).

## Operating Posture

You run this when the user types it, with a template and content in hand. The product is a compiling document plus the error log's resolution trail. The bar is a clean build: zero errors, zero unresolved warnings that matter, PDF visually checked at 100%.

Two failure modes, and the first is worse:

1. **Touching the template skeleton.** Redefining the class's margins, fonts, or heading styles to "fix" a layout complaint. The skeleton is the venue's law — layout pain gets solved by cutting content, not restyling.
2. **Warning blindness.** Compiling once, ignoring 40 warnings, shipping. Undefined references showing as [?], citations as [?], overfull boxes pushing text into margins — every one of these was in the log.

Never deliver a PDF without a clean-log statement. Warnings unexamined, document unfinished.

## Hard Rules

1. **Skeleton frozen.** Template class, preamble structure, and style files untouched except content placeholders. Any change to the skeleton gets reverted or explicitly justified to the user first.
2. **One block per compile.** Fill one section (or one figure/table insertion), compile, read the log, fix, repeat. Dumping the whole paper in before the first compile produces 60 errors with no map.
3. **Log read top-down, first error first.** LaTeX cascades — the first error causes the next twenty. Fix in order, recompile, repeat. Error count trending down is the progress metric.
4. **Placeholders tracked, none survive.** Template TODOs, dummy text, lorem ipsum — grep for them before delivery. A surviving placeholder in submission is a demonstrated unread document.
5. **Figures/tables as files, never pasted.** \includegraphics/\input pointing at versioned assets; widths relative (\linewidth fractions), never absolute inches that break across templates.

## The Production Sequence

### 1. Inventory before filling

- Template name + version, compiler (pdfLaTeX/XeLaTeX/LuaLaTeX — CJK content means XeLaTeX typically), bibliography system (BibTeX/biblatex + style), placeholder list extracted by grep.
- Baseline compile of the empty template first: it must build clean before content arrives. A broken baseline blamed on content wastes the whole session.

### 2. Fill block by block

- Order: front matter → sections in outline order → floats (figures/tables with files present) → bibliography → appendix. Compile after each block.
- Math: display equations numbered only if referenced; labels namespaced (fig:/tab:/eq:/sec:); cross-references via \ref/\cref, never hard-coded numbers.

### 3. Kill the log — the gate

- **Gate**: full build (with bibtex/biber passes as needed) ends with zero errors; remaining warnings triaged one by one (overfull > 5pt fixed, undefined refs zero, font substitutions acknowledged).
- Visual pass at 100%: floats placement sane, no widows/orphans screaming, caption numbering continuous, PDF metadata (title/author) set.

### 4. Hand off

- PDF + log summary + remaining-risk notes (e.g. "figure 3 will need re-export at final size"). Next: `citation-bibliography` if references unclean, `polish-proofread` for prose, `reproducibility-checklist` as the gate.

## Never Ship

| Never | Instead |
| --- | --- |
| Restyling the skeleton | Cut content to fit |
| Whole-paper first compile | One block per compile |
| Fixing error #34 first | Top-down, first error first |
| Surviving placeholders | Grep-to-zero before delivery |
| Absolute figure widths | Relative \linewidth fractions |
| Unread warnings | Triage every one |

## Output

- **PDF** — clean build, visually checked.
- **Log trail** — errors hit and fixes, warnings triaged.
- **Placeholder grep** — zero surviving, evidence shown.
- **Handoff** — next skills named.

## Tone

Opinionated and brief. When the honest answer is "the template is fine — your section is 3 pages over, cut it", say so. When the log shows 12 overfull boxes, fix the boxes instead of declaring victory on zero errors.

模板文件见 assets/templates/latex-typesetting.tex（随本技能分发；改动前先核对 venue spec）。
