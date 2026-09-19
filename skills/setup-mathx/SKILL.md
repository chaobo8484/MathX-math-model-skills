---
name: setup-mathx
description: "第一次用先跑我：绑定数据目录、模板版本、绘图后端和证据后端，写进 docs/agents/ 供其余技能读取。"
disable-model-invocation: true
---

# Setup-MathX：一次绑定，处处复用

用户键入时运行，每个项目一次。先整编工作区（步骤 0），再问四个问题，答案写进 `docs/agents/mathx-config.md`，停。其他技能有这个文件就读它，不再重问。

## 0. 工作区整编——gate

用户刚拿到赛题时，工作区一般是散件：原题 PDF（约两页，说明全部题目）+ 附件（XLSX/CSV 等，或装在附件目录里）。先整编，后绑定。

- 调 `assets/scripts/intake-organize.py --workdir <用户工作区> --out report.json`（默认 dry-run，只出方案不搬）。
- 按题目分文件夹归位：`<workdir>/A题/` 内放原题 PDF + 附件原样（按问细分由 `scaffold-questions.py` 接手，不在这里建工作目录）。只动顶层散件；已存在的题目文件夹、`docs/`、`.git` 一律不动。支持 A–E 全套：附件名带字号（附件A/A题附件/A_data）自动归位该题；多题共用的总题 PDF 留根目录不动。
- **gate**：报告 verdict 为 HOLD（附件归属不明、题数不明、目标已存在）时先问用户，问清后用 `--problems` 指定题号重跑；OPEN 时给用户看搬移方案，确认后 `--apply` 执行；PASS 直接往下走。
- 整编结果记入 config 的 `problem_dirs` 行（无题目时填 none），下游 `ingest-inputs` 吃附件、`latex-typesetting` 出稿只认整编后的位置。
- 每个题目文件夹下再按问脚手架：调 `assets/scripts/scaffold-questions.py --problem-dir <A题目录> --out report.json`，问数从原题 PDF 文本自动探测（问题一/二/三、第X问、Q1/Q2…），探不到 HOLD 问用户，`--questions` 可直接指定。确认后 `--apply` 建目录，约定统一为 `qN/charts_qN/ + data_qN/（raw） + script_qN/ + cleaned_data/（processed）`——脚本只认这个位置：清洗分析代码进 `script_qN/`，原始数据进 `data_qN/`，`ingest-inputs` 洗后数据进 `cleaned_data/`，图表输出进 `charts_qN/`。同时在题目根目录生成 `main.py` 总入口（论文附录提交版，不直接运行）：浓缩各问核心调用索引，函数名留 TODO 由 Agent 按实际脚本填实；已存在永不覆盖。

## The four questions

四个问题一轮问完，各带推荐默认。等回答再落盘。

```
❓ **Q1** — **数据目录**: 分析数据放在哪里？(推荐: ./data, 原始与处理后分 raw/ + processed/)

❓ **Q2** — **模板与输出格式**: 目标 venue 与模板？(推荐: 按 paper-outline 的 venue 判断: MCM 用官方 mcmthesis, 国赛用官方 cumcmthesis 模板（文献著录按 GB/T 7714）, 期刊用 venue 模板; 无论文需求填 none；中文内容默认 `XeLaTeX`，否则 `pdfLaTeX` 见 `CONTEXT.md:21`；终稿 PDF 用 TEX，协作草稿用 DOCX 见 `latex-typesetting`)

❓ **Q3** — **绘图后端**: 静态图风格与交互需求？(推荐: Matplotlib + Okabe-Ito 静态为主, 探索期加 Plotly)

❓ **Q4** — **证据后端**: 外部取证走哪档？(推荐: none; 自给链接选 manual; 通用搜索选 generic; Firecrawl 是高级选项，仅深爬用，需自备 key 存环境变量，仓内只记名不存值)
```

## Write the config

在项目里建 `docs/agents/mathx-config.md`，内容如下（一字不差）：

```markdown
# mathx-config (written by setup-mathx, <date>)

- data_dir: <answer 1> (raw/ + processed/ convention)
- venue_template: <answer 2> (name + version, or none)
- latex_compiler: <XeLaTeX|pdfLaTeX> (中文内容 XeLaTeX，否则 pdfLaTeX)
- output_format: <TEX|DOCX> (终稿 PDF 用 TEX，协作草稿用 DOCX)
- plot_backend: <answer 3> (static style block location + interactive yes/no)
- evidence_backend: <answer 4> (none | manual | generic | firecrawl-advanced)
- problem_dirs: <步骤 0 整编结果，如 A题/（无题目时填 none），下游技能只认这里>
- evidence_key_source: env:FIRECRAWL_API_KEY (name only, never the value)
- glossary: project terms differing from CONTEXT.md (empty at setup, grows via use)
```

然后三行告诉用户：记了什么、其他技能会读它、答案变了重跑 `/setup-mathx`。停——不要顺手开始建模、搭大纲、画图。

## Tone

快而行政。本技能是额外开销；压到最小。先整编，后四问，一个文件，完事。
