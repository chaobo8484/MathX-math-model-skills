---
name: setup-mathx
description: "第一次用先跑我：绑定数据目录、模板版本和绘图后端，写进 docs/agents/ 供其余技能读取。"
disable-model-invocation: true
---

# Setup-MathX：一次绑定，处处复用

用户键入时运行，每个项目一次。问三个问题，答案写进 `docs/agents/mathx-config.md`，停。其他技能有这个文件就读它，不再重问。

## The three questions

三个问题一轮问完，各带推荐默认。等回答再落盘。

```
❓ **Q1** — **数据目录**: 分析数据放在哪里？(推荐: ./data, 原始与处理后分 raw/ + processed/)

❓ **Q2** — **LaTeX 模板**: 目标 venue 与模板？(推荐: 按 paper-outline 的 venue 判断: MCM 用官方 mcmthesis, 国赛用 GB/T 7714 模板, 期刊用 venue 模板; 无论文需求填 none)

❓ **Q3** — **绘图后端**: 静态图风格与交互需求？(推荐: Matplotlib + Okabe-Ito 静态为主, 探索期加 Plotly)
```

## Write the config

在项目里建 `docs/agents/mathx-config.md`，内容如下（一字不差）：

```markdown
# mathx-config (written by setup-mathx, <date>)

- data_dir: <answer 1> (raw/ + processed/ convention)
- venue_template: <answer 2> (name + version, or none)
- plot_backend: <answer 3> (static style block location + interactive yes/no)
- glossary: project terms differing from CONTEXT.md (empty at setup, grows via use)
```

然后三行告诉用户：记了什么、其他技能会读它、答案变了重跑 `/setup-mathx`。停——不要顺手开始建模、搭大纲、画图。

## Tone

快而行政。本技能是额外开销；压到最小。三个问题，一个文件，完事。
