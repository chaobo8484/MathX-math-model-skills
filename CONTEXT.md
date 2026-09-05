# CONTEXT.md — MathX shared language

Read this file before running any skill in this repo. It holds the vocabulary every skill assumes: symbols, units, venues, and tool defaults. Terms defined here are used verbatim in code, figures, and prose.

## Symbols and units

- Time variables: `t` in days unless stated; rates per day. State any deviation in the deliverable.
- Matrices: uppercase (`X` data, `W` weights); vectors lowercase; estimates wear hats (`x̂`).
- Random seeds: integer, recorded in code. "Seed 42" with no code location is not a seed.
- Language policy（结构英文 + 表述中文 + 句内不混写）:
  1. 结构词固定英文：Operating Posture / Hard Rules / Build Sequence / Never Ship / Output / Tone，以及 gate / probe / baseline / verdict 等执行关键词，不许自创新词或翻成中文。
  2. 解释、例子、表格内容用中文；方法名、工具名、阈值符号保持英文原文。
  3. 一句话一种语言；代码与反引号内术语算英文，不计入混写。
  4. description 纯中文 + 英文方法关键词，不出现 Use when / Trigger phrases 等英文残留。
  5. 禁止中英同义复读：同一意思只讲一遍，以中文为准。
- Paper prose follows the venue; code comments in English.

## Venues and templates

- MCM / 国赛 / journal — the three venue types. Every writing skill asks which one before starting.
- LaTeX compiler default: XeLaTeX for CJK content, pdfLaTeX otherwise. Bibliography per venue (GB/T 7714 for 国赛, venue .bst/biblatex for journals).
- Figure sizes: single column ≈ 89mm, double ≈ 183mm (verify per venue in `publication-figure`).

## Method vocabulary (use these words, not synonyms)

- Ranking with expert judgment → `ahp`; with measured data only → `evaluation-entropy-topsis`. Never "AHP weighting" for entropy weights.
- Tiny samples (4–10 pts) → `gray-prediction`; 30+ evenly spaced → `time-series-arima`.
- Evidence grades: SUPPORTED / OPEN / REFUTED (`numerical-verification`); gap tags: [PROVEN] / [SKETCH] / [GAP] / [AXIOM-OR-CITED] (`proof-assistant`).
- Statistical figures always carry N, test, p, effect, CI — the five-piece set (`statistical-plot`).
- Palette: Okabe-Ito categories, viridis continuous. No rainbow, no red-green critical encoding.

## Tool defaults

- Compute in Python (NumPy/SciPy/SymPy/NetworkX/PuLP), plot in Matplotlib/Seaborn (static) or Plotly (interactive).
- Solver default order: HiGHS → SCIP → CBC; record name + version actually used.
- Input normalization via `ingest-inputs`: CSV/XLSX with pandas (encoding sniff UTF-8/GBK) + openpyxl, MP4 frame extraction at declared fps, JPG classified first (data-chart digitize / example-image describe).
- practicedecisions live with the project using the skills (data dir, template version, backend), recorded by `setup-mathx` under `docs/agents/` — read that file too when it exists.
