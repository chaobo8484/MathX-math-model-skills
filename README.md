# MathX 数学建模技能

[English](./README.en.md)

面向建模者与研究者，帮你做出更好的数学模型、论文与图表。

选对方法很难——AHP 还是熵权 TOPSIS，ARIMA 还是灰色预测，柱状图还是热力图。这些技能帮你更快做出正确的决定。

它们来自多年的数学建模与竞赛经验（MCM/国赛）。每个技能列出 Agent 用该方法时最常犯的错误，以及修正办法。

## 安装

[![skills.sh](https://skills.sh/b/chaobo8484/MathX-math-model-skills)](https://skills.sh/chaobo8484/MathX-math-model-skills)

```bash
npx skills@latest add chaobo8484/MathX-math-model-skills
```

支持 Claude Code、Codex 与 OpenCode。Claude Code 还可以通过 marketplace（`.claude-plugin/marketplace.json`）安装为托管插件。

公共词汇在 [CONTEXT.md](./CONTEXT.md) 中——所有技能默认你已读过。每个项目先跑一次 `/setup-mathx`，再用其他技能。

## 为什么要用？

Agent 没有建模判断力。

它们跑 AHP 从不检验 CR，给 8 个数据点拟合 ARIMA，给时间序列画 3D 饼图，引用不存在的文献。这些小毛病叠加起来，决定了你的论文是令人信服，还是……经不起推敲。

这些技能把每个方法站得住脚的检查编码下来：一致性比率、平稳性诊断、样本量门禁、不做事项清单。一条通往“审稿人挑不出毛病”的捷径。

## 索引

触发方式：人触发 = 你键入调用；自动 = Agent 按任务自行调用。

| 入口 | 说明 | 触发 |
|---|---|---|
| [ask-mathx](./skills/ask-mathx/SKILL.md) | 不知道该用哪个技能时先走这里：帮你选 1–2 个并排好顺序 | 人触发 |
| [setup-mathx](./skills/setup-mathx/SKILL.md) | 每个项目先跑一次：绑定数据目录、模板版本和绘图后端 | 人触发 |

### 建模 Modeling

| 技能 | 说明 | 触发 |
|---|---|---|
| [ahp](./skills/ahp/SKILL.md) | 成对比较层次结构做主观排序，经判断矩阵算特征权重，CR < 0.1 | 自动 |
| [evaluation-entropy-topsis](./skills/evaluation-entropy-topsis/SKILL.md) | 客观熵权 + TOPSIS 贴近度做多指标排序，无需主观打分 | 自动 |
| [gray-prediction](./skills/gray-prediction/SKILL.md) | GM(1,1) 外推近指数趋势的极小样本（4–10 个点） | 自动 |
| [time-series-arima](./skills/time-series-arima/SKILL.md) | ARIMA/SARIMA 建模等间隔序列（约 30 点以上），平稳性诊断与滚动回测 | 自动 |
| [bp-neural-network](./skills/bp-neural-network/SKILL.md) | 反向传播前馈网络拟合非线性回归或分类，训练/验证划分与早停 | 自动 |
| [regression-family](./skills/regression-family/SKILL.md) | OLS、岭、Lasso、Logistic 的拟合选择与诊断，EDA/VIF + 交叉验证 | 自动 |
| [clustering-classification](./skills/clustering-classification/SKILL.md) | KMeans/DBSCAN 分群与随机森林分类，肘部/轮廓系数 + 分层交叉验证 | 自动 |
| [genetic-algorithm](./skills/genetic-algorithm/SKILL.md) | 选择交叉变异求解非凸组合优化（调度、选址、路径） | 自动 |
| [optimization-lp-milp](./skills/optimization-lp-milp/SKILL.md) | 线性目标约束与整数决策交给可复现求解器（HiGHS/CBC/SCIP） | 自动 |
| [monte-carlo-simulation](./skills/monte-carlo-simulation/SKILL.md) | 解析解困难时用随机抽样估计概率、期望与风险 | 自动 |
| [differential-equation](./skills/differential-equation/SKILL.md) | ODE 积分与有限差分描述连续演化（SIR、热传导、种群） | 自动 |
| [graph-network](./skills/graph-network/SKILL.md) | 最短路、最大流、中心性与社区分析 | 自动 |

### 写作 Writing

| 技能 | 说明 | 触发 |
|---|---|---|
| [literature-review](./skills/literature-review/SKILL.md) | 结构化检索、去重与主题归类，输出可追溯的研究缺口表 | 人触发 |
| [paper-outline](./skills/paper-outline/SKILL.md) | 为 MCM、国赛或期刊论文设计章节结构与 Claim-Evidence-Link 故事线 | 人触发 |
| [latex-typesetting](./skills/latex-typesetting/SKILL.md) | 分块填入官方 LaTeX 模板并编译出 PDF，按报错日志迭代修错 | 人触发 |
| [citation-bibliography](./skills/citation-bibliography/SKILL.md) | 清洗 BibTeX，核对文内引用与参考文献表双向一致 | 人触发 |
| [figure-table-generation](./skills/figure-table-generation/SKILL.md) | 把分析结果整理成带题注引用的投稿级图表与 booktabs 表格 | 人触发 |
| [polish-proofread](./skills/polish-proofread/SKILL.md) | 统一术语、时态、语态与图表标题的中英文学术润色 | 人触发 |
| [reproducibility-checklist](./skills/reproducibility-checklist/SKILL.md) | 交稿前自检：环境、随机种子、数据、代码、图表与审稿视角 | 人触发 |

### 研究 Research

| 技能 | 说明 | 触发 |
|---|---|---|
| [conjecture-formulation](./skills/conjecture-formulation/SKILL.md) | 从模式、类比与数值现象提炼可证伪的数学命题 | 自动 |
| [proof-assistant](./skills/proof-assistant/SKILL.md) | 拆引理、选证明策略，显式标记每个未验证缺口 | 自动 |
| [symbolic-computation](./skills/symbolic-computation/SKILL.md) | SymPy 化简、求导、积分、解方程并导出 LaTeX | 自动 |
| [numerical-verification](./skills/numerical-verification/SKILL.md) | 边界扫描与可复现实验评估猜想证据强度 | 自动 |
| [counterexample-search](./skills/counterexample-search/SKILL.md) | 暴力、剪枝与启发式寻找并验证最小反例 | 自动 |
| [arxiv-literature-synthesis](./skills/arxiv-literature-synthesis/SKILL.md) | 从引用图梳理领域演化、定理依赖与开放问题 | 自动 |

### 可视化 Visualization

| 技能 | 说明 | 触发 |
|---|---|---|
| [chart-decision](./skills/chart-decision/SKILL.md) | 按数据类型与表达目标选图型，排除误导性视觉编码 | 自动 |
| [scientific-plotting](./skills/scientific-plotting/SKILL.md) | Matplotlib/Seaborn 色盲安全静态矢量图 | 自动 |
| [statistical-plot](./skills/statistical-plot/SKILL.md) | 分布、相关、检验、残差、ROC 与 N、p 值、置信区间同图呈现 | 自动 |
| [plotly-interactive](./skills/plotly-interactive/SKILL.md) | 缩放、悬停、联动的 Plotly 探索图，超万点降采样 | 自动 |
| [publication-figure](./skills/publication-figure/SKILL.md) | 按单双栏尺寸、DPI、字体嵌入组装多子图投稿图 | 自动 |
| [diagram-schematic](./skills/diagram-schematic/SKILL.md) | Mermaid/Graphviz/NetworkX 可编辑矢量示意图、流程图与网络图 | 自动 |
