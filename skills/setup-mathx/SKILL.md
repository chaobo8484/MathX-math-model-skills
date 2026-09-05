---
name: setup-mathx
description: "第一次用先跑我：绑定数据目录、模板版本和绘图后端，写进 docs/agents/ 供其余技能读取。"
disable-model-invocation: true
---

# Setup-MathX：一次绑定，处处复用

You run this when the user types it, once per project. It asks three questions, writes the answers to `docs/agents/mathx-config.md`, and stops. Every other skill reads that file when it exists instead of re-asking.

## The three questions

Ask all three in one round, each with a recommended default. Wait for answers before writing.

```
❓ **Q1** — **数据目录**: 分析数据放在哪里？(推荐: ./data, 原始与处理后分 raw/ + processed/)

❓ **Q2** — **LaTeX 模板**: 目标 venue 与模板？(推荐: 按 paper-outline 的 venue 判断: MCM 用官方 mcmthesis, 国赛用 GB/T 7714 模板, 期刊用 venue 模板; 无论文需求填 none)

❓ **Q3** — **绘图后端**: 静态图风格与交互需求？(推荐: Matplotlib + Okabe-Ito 静态为主, 探索期加 Plotly)
```

## Write the config

Create `docs/agents/mathx-config.md` in the project with exactly:

```markdown
# mathx-config (written by setup-mathx, <date>)

- data_dir: <answer 1> (raw/ + processed/ convention)
- venue_template: <answer 2> (name + version, or none)
- plot_backend: <answer 3> (static style block location + interactive yes/no)
- glossary: project terms differing from CONTEXT.md (empty at setup, grows via use)
```

Then tell the user, in three lines: what was recorded, that other skills will read it, and to re-run `/setup-mathx` when any answer changes. Stop — do not start modeling, outlining, or plotting.

## Tone

Fast and administrative. This skill is overhead; minimize it. Three questions, one file, done.
