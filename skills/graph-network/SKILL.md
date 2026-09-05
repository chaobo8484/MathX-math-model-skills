---
name: graph-network
description: "最短路、最大流、中心性与社区分析。Use when 问题含路径流量关键节点时；画流程架构示意图用 diagram-schematic。"
---
# 图与网络分析

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: turn a path/flow/node/community question into computed answers on an explicitly declared graph. It does not do constrained optimization with side conditions (that's `optimization-lp-milp`), and it does not draw architecture diagrams (that's `diagram-schematic`).

## Operating Posture

You are a modeling specialist producing answers re-derivable from an edge list. The bar is declaration-first: directed or not, what weight means, which algorithm, all stated before any number. Write it so the weight-semantics line passes review the first time.

Two failure modes, and the first is worse:

1. **Computing on an undeclared graph.** Weight as cost vs capacity vs affinity silently decides whether shortest-path, max-flow, or community detection is even meaningful. An answer from ambiguous semantics is a random number with a famous algorithm's name.
2. **Metric shopping** — five centralities computed, the flattering one reported; communities without modularity; flows without capacities sourced. Unreported alternatives are hidden degrees of freedom.

Never present a network number without the graph declaration and a visual check. No declaration, no metric.

## Hard Rules

1. **Declare the graph in one block.** Directed/undirected, node meaning, edge meaning, weight meaning + units + source. "Weight = strength" vs "weight = distance" inverts every path result — state it.
2. **Match algorithm to semantics.** Costs/distances → shortest paths; capacities → max flow/min cut; influence/bridging → centrality (named variant); dense groups → community detection with modularity reported.
3. **Centrality variant named, never bare "centrality".** Degree / betweenness / closeness / eigenvector / PageRank (α stated) answer different questions — pick by the question, report the rest as appendix or not at all.
4. **Negative weights and disconnectedness checked first.** Negative edges → Bellman-Ford and no Dijkstra, stated; disconnected graph → per-component analysis, cross-component distances are undefined, not zero.
5. **Every computation gets a visual check.** Layout plot with the answer highlighted (path drawn, cut shown, top nodes labeled). A table of node IDs without the picture is unverifiable.

## The Build Sequence

### 1. Should this be network analysis at all?

| Situation | Decision |
| --- | --- |
| Paths, flows, key nodes, or communities on relational data | **Graph-network. Continue.** |
| Flows with side constraints (budgets, time windows, integrality) | Formulate in `optimization-lp-milp`; use this skill for the network substructure. |
| Just need a system/method diagram drawn | Stop. Use `diagram-schematic`. |
| "Network" as metaphor with no edge data | Stop. Say so; no edges, no analysis. |

### 2. Declare and build

- Node/edge/weight semantics block (rule 1), edge list source, n/m counts, density, directedness.
- Sanity: self-loops and multi-edges — kept, collapsed (how?), or rejected, stated. Weight distribution glanced at (a single 1e9 edge dominating paths is a data bug until proven otherwise).

### 3. Compute per question type

- **Paths**: algorithm named (Dijkstra/BFS/Bellman-Ford/A*), source-target or all-pairs stated; report path + cost, not cost alone.
- **Flows**: max-flow value + min-cut edges shown; capacities sourced per edge. Uncapacitated "flow" is connectivity — label it so.
- **Centrality**: one primary variant justified by the question ("bridges" → betweenness, "reach" → closeness, "prestige" → eigenvector/PageRank); full ranking table, top-k interpreted in domain terms.
- **Communities**: method named (Louvain/Leiden/label-prop), modularity reported; communities without a modularity number are asserted, not found.

### 4. Robustness

- Perturb: remove top-1/top-3 nodes (or ±10% weights) and re-run the headline computation. A "key node" whose removal changes nothing wasn't key; a ranking that scrambles under ±10% weights is noise — both reported, not buried.
- Compare against a null model where cheap (configuration model / random rewiring) for community and centrality claims.

### 5. Show it

- One layout figure per headline result, answer highlighted, N/M in caption (`scientific-plotting` conventions). Tables carry node labels, never bare integer IDs without a mapping.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Undeclared weight semantics | Meaning + units + source, one block |
| Bare "centrality" | Named variant, justified by the question |
| Dijkstra on negative weights | Bellman-Ford, stated |
| Cross-component distances as zero | Per-component analysis |
| Metric shopping | One primary metric + appendix, modularity shown |
| Node-ID tables without a picture | Layout figure per headline result |

## Output

The deliverable is the answer **plus the graph it came from**, in this order:

- **Declaration** — directedness, semantics, weight meaning/units/source, n/m.
- **Computation** — algorithm named, parameters, tool used.
- **Answer** — path/flow/ranking/communities with numbers.
- **Robustness** — perturbation + null-model verdict.
- **Figure + limits** — highlighted layout, scope, what breaks the answer.

Don't pad this into a report. The declaration block is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "your weights are affinities, so shortest-path is meaningless here — you want community detection", give it. When modularity is 0.12, report "no real communities" instead of coloring noise.
