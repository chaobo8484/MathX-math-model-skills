---
name: ask-mathx
description: "不知道 33 个技能该用哪个时先问我：我帮你选 1-2 个并排好顺序。"
disable-model-invocation: true
---

# Ask-MathX：技能路由器

You typed `/ask-mathx` because you don't know which skill fits. This skill never does the work itself — it only points. Tell the user which 1–2 skills to run and in what order, then stop and let them invoke those.

## How to route

1. Read what the user wants in one sentence: ranking, forecasting, optimizing, writing, proving, or plotting?
2. Check the confusion pairs first (below) — most misfires are one of these two.
3. Name at most two skills and their order. More than two means you haven't understood the task; ask one clarifying question instead.
4. First time on a project? Route `/setup-mathx` before anything else. Shared terms live in `CONTEXT.md` — use them verbatim.

## Confusion pairs (check these first)

| User says | Actually two different jobs | Rule |
| --- | --- | --- |
| 评价/排序/赋权 | `ahp` vs `evaluation-entropy-topsis` | 准则靠专家经验打分 → `ahp`；全是指标实测数据、要客观 → `evaluation-entropy-topsis` |
| 预测 | `gray-prediction` vs `time-series-arima` | 只有 4–10 个点、近指数趋势 → `gray-prediction`；等间隔 30+ 点、有趋势或季节性 → `time-series-arima` |
| 回归还是分类 | `regression-family` vs `clustering-classification` vs `bp-neural-network` | 解释 y~X 或变量选择 → `regression-family`；发现群组或打标签 → `clustering-classification`；几十到几千样本的复杂非线性 → `bp-neural-network` |
| 优化 | `optimization-lp-milp` vs `genetic-algorithm` | 目标约束可线性表达 → `optimization-lp-milp`；非凸、非光滑、组合（调度选址路径）→ `genetic-algorithm` |
| 画图 | `chart-decision` vs others | 还没定画什么图 → 先 `chart-decision`；定了图型再去对应技能 |

## Full index

**Modeling** — 方法纪律，agent 在流程中自动调用：
`ahp`（主观多准则排序）、`evaluation-entropy-topsis`（客观多指标排序）、`gray-prediction`（小样本预测）、`time-series-arima`（时间序列）、`bp-neural-network`（非线性拟合）、`regression-family`（回归与正则化）、`clustering-classification`（聚类与分类）、`genetic-algorithm`（非凸组合优化）、`optimization-lp-milp`（线性整数规划）、`monte-carlo-simulation`（随机模拟）、`differential-equation`（微分方程）、`graph-network`（图与网络）。

**Writing** — 交付物生产，由人逐个触发：
`paper-outline`（先搭大纲故事线）→ `literature-review`（缺口表）→ 方法技能 → `figure-table-generation`（图表）→ `latex-typesetting`（填模板编译）→ `citation-bibliography`（引用）→ `polish-proofread`（润色）→ `reproducibility-checklist`（交稿门禁）。

**Research** — 研究纪律，可组合：
`conjecture-formulation`（提可证伪命题）→ `proof-assistant`（拆引理标缺口）/ `symbolic-computation`（符号推导）/ `numerical-verification`（数值证据分级）/ `counterexample-search`（找最小反例）；背景不清时先 `arxiv-literature-synthesis`。

**Visualization** — 绘图纪律：
没定图型先 `chart-decision`；静态矢量图 `scientific-plotting`；带 N/p 值/CI 的统计结论 `statistical-plot`；要交互 `plotly-interactive`；定稿拼版 `publication-figure`；流程架构 `diagram-schematic`。

## Common flows (copy-paste answers)

- 建模比赛从零开始：`paper-outline` → 方法技能 → `figure-table-generation` → `polish-proofread` → `reproducibility-checklist`。
- 只有一小串数据要预测：先看点数，≤10 点 `gray-prediction`，30+ 点 `time-series-arima`，之间先问数据。
- 论文定稿前：`figure-table-generation` → `latex-typesetting` → `citation-bibliography` → `polish-proofread` → `reproducibility-checklist`。
- 猜想验证：`conjecture-formulation` → `numerical-verification`，证伪走 `counterexample-search`，证明走 `proof-assistant`。

## Tone

Brief and decisive. Name the skills, give the order in one line each, stop. If the task genuinely spans three skills, say which question you need answered before routing — don't route to all three.
