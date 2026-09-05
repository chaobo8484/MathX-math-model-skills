# CONTEXT.md — MathX shared language

Read this file before running any skill in this repo. It holds the vocabulary every skill assumes: symbols, units, venues, and tool defaults. Terms defined here are used verbatim in code, figures, and prose.

## Symbols and units

- Time variables: `t` in days unless stated; rates per day. State any deviation in the deliverable.
- Matrices: uppercase (`X` data, `W` weights); vectors lowercase; estimates wear hats (`x̂`).
- Random seeds: integer, recorded in code. "Seed 42" with no code location is not a seed.
- Language: skill bodies are bilingual (English structure, Chinese detail). Paper prose follows the venue; code comments in English.

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
- practicedecisions live with the project using the skills (data dir, template version, backend), recorded by `setup-mathx` under `docs/agents/` — read that file too when it exists.
