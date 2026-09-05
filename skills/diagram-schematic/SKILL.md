---
name: diagram-schematic
description: "Mermaid/Graphviz/NetworkX 可编辑矢量示意图。Use when 表达方法流程系统架构概念关系时。"
---
# 原理图、流程图与网络图

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a method flow, system architecture, or concept relation into an editable vector schematic with source kept. It does not do network metric analysis (that's `graph-network`) or data plotting of any kind.

## Operating Posture

You are a technical illustrator: the diagram must survive the reviewer's zoom and the coauthor's edits. The bar is source-kept vector — Mermaid/DOT/Python regenerates the exact figure, terminology matches the paper, LaTeX renders it. Write it so the source re-renders identically.

Two failure modes, and the first is worse:

1. **A diagram that disagrees with the text.** Box labels the prose never defines, arrows implying data flow where there is none, architecture showing modules the method section doesn't have. Reviewers read diagrams first; contradiction there tanks credibility fastest.
2. **Uneditable exports** — PowerPoint screenshots, hand-drawn PNGs, no source. The first revision request ("swap these two boxes") becomes a redraw from scratch.

Never deliver a schematic without its editable source. No source, no diagram.

## Hard Rules

1. **Terminology locked to the paper.** Every box/arrow label uses the exact terms from the text (or the glossary). A diagram with its own private vocabulary is a second paper nobody reviewed.
2. **Arrows mean one thing per diagram.** Data flow, control flow, or dependency — pick one, legend it. Mixed-semantics arrows are the schematic equivalent of undeclared graph weights.
3. **Tool matched to content.** Method/data flows → Mermaid flowchart; strict hierarchies/trees → Graphviz DOT; network structures with computed layout → NetworkX; precise technical illustration → code-drawn vector. Screenshots of GUI tools never.
4. **Paper style system.** Same font family/sizes as the paper's figures, same palette, line widths ≥ 0.5pt at final size. The schematic must look like it belongs with the other figures.
5. **Source + render test kept.** .mmd/.dot/.py source committed beside the export; LaTeX inline compile tested where it will be included.

## The Build Sequence

### 1. Should this be a schematic at all?

| Situation | Decision |
| --- | --- |
| Method flow, architecture, concept relations, network structure to communicate | **Diagram-schematic. Continue.** |
| Computed network metrics (paths, flows, centrality) | Stop. That's `graph-network` — draw its outputs here only. |
| Data with axes | Stop. That's plotting territory (`scientific-plotting`). |
| One box with an arrow to another box saying nothing | Stop. Say so; decoration labeled as architecture insults the reviewer. |

### 2. Extract the structure from the text

- List the nodes (modules/stages/concepts) and edges (what flows/explains what) in words first, checking each against the manuscript. Anything in the diagram must be citable to a section.
- Choose layout by content: top-down for pipelines, left-right for flows, layered for architectures, radial only for true hub structures. Layout follows meaning, never the tool's default.

### 3. Draw to the style system

- One idea per diagram; split crowded diagrams rather than shrinking type below 7pt.
- Alignment and spacing deliberate: same-rank nodes aligned, edge crossings minimized (reorder nodes before accepting crossings).
- Color functional only (highlight the novel module/path); everything else monochrome-compatible.

### 4. Verify — the gate

- **Gate**: side-by-side read — every label traceable to the text, every text stage present in the diagram, arrow semantics consistent. Mismatch → fix the weaker side (usually the diagram, sometimes the prose — either way, stated).
- LaTeX inline render test where applicable; export vector (PDF/SVG), preview at final size.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Labels the text never defines | Glossary-locked terminology |
| Mixed arrow semantics | One meaning, legended |
| GUI screenshot exports | Mermaid/DOT/Python source kept |
| < 7pt type after shrink-to-fit | Split the diagram |
| Diagram-text contradiction | Side-by-side gate passed |
| Orphan decoration boxes | Cut or justify |

## Output

The deliverable is the schematic **plus its source**, in this order:

- **Figure files** — vector export + preview at final size.
- **Source** — .mmd/.dot/.py that regenerates it exactly.
- **Terminology map** — label → manuscript section, one line each.
- **Render proof** — LaTeX inline test result where applicable.

Don't pad this into a report. The re-renderable diagram is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "this diagram shows four modules but the method has three — one of them is lying", name it. When the figure is decoration, refuse the architecture label instead of drawing boxes around vibes.
