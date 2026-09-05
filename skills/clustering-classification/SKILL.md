---
name: clustering-classification
description: "KMeans/DBSCAN 分群与随机森林分类。Use when 为样本发现群组或打标签时；解释变量关系用 regression-family。"
---
# 聚类与分类

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: find groups in unlabeled data or label new samples, with the cluster count and the error both earned. It does not do explanatory modeling (that's `regression-family`), nonlinear black-box fitting (that's `bp-neural-network`), or plotting for its own sake (that's `statistical-plot`).

## Operating Posture

You are a modeling specialist producing groups a skeptic can re-derive and labels with a measured error. The bar is two-sided: unsupervised side needs a justified K and stability; supervised side needs stratified-CV error with a confusion matrix. Write it so both checks pass the first time.

Two failure modes, and the first is worse:

1. **Clustering noise and naming it.** K picked by wish, unscaled features letting one variable dictate distance, DBSCAN eps unexamined. A KMeans partition always exists — that doesn't mean groups exist.
2. **Classification accuracy without context** — no stratification on imbalance, test leakage via preprocessing, single split, confusion matrix missing. Accuracy on a 90/10 split is a majority-class celebration.

Never present groups without stability evidence, or labels without a confusion matrix. No evidence, no claim.

## Hard Rules

1. **Standardize before any distance.** Z-score (or robust scaling with outliers) from training data. Euclidean distance on raw mixed units is dominated by the largest scale — that choice must never be accidental.
2. **K is chosen by elbow + silhouette, both shown.** One of them alone is weak; a K with silhouette < ~0.25 is a warning to report, not a result to decorate.
3. **DBSCAN eps from the k-distance plot, minPts stated.** eps hand-picked with no plot is guessing; report the noise fraction as a finding.
4. **Supervised side: stratified k-fold CV + confusion matrix, always.** Imbalance stated up front; accuracy never the lone headline on skewed classes.
5. **No leakage through preprocessing.** Scaling, encoding, feature selection fit on train folds only. Leakage check is part of the deliverable, stated in one line.

## The Build Sequence

### 1. Which side — and should this skill fire at all?

| Situation | Decision |
| --- | --- |
| No labels, looking for groups (tens to tens of thousands of samples) | **Clustering side. Continue.** |
| Labels exist, need to tag new samples | **Classification side. Continue.** |
| Need to explain drivers or select variables | Stop. Use `regression-family`. |
| Complex nonlinearity, prediction only | Stop. Use `bp-neural-network` if it beats a forest baseline. |

If both sides apply (cluster then classify), run them as two stages with separate checks — never let the clustering's K leak into the classifier's CV unexamined.

### 2. Preprocess once, loudly

- Missing values, categoricals, obvious outliers: handling named per column.
- Scale: z-score default; robust (median/IQR) with heavy tails. State which and why.
- Dimensionality: if p is large relative to n, PCA/t-SNE/UMAP for visualization only — cluster in a stated space, and say which.

### 3a. Clustering: earn the K

- KMeans over a K range: elbow plot (inertia) + silhouette per K, both shown. DBSCAN alternative: k-distance plot for eps, minPts ≈ dimensionality-aware default, stated.
- **Gate**: chosen K has both elbow support and the best-or-tied silhouette; silhouette < ~0.25 → report "weak structure" instead of naming personas for the clusters.
- Stability: bootstrap/jitter reruns, adjusted Rand index across runs. Unstable partitions get reported as unstable, not averaged into false confidence.
- Profile each cluster (centroids, sizes, distinguishing features) — a cluster you can't describe in one sentence is a shard, not a segment.

### 3b. Classification: earn the error

- Model: random forest default (stated n_estimators, max_depth); compare against Logistic baseline from `regression-family`.
- Stratified k-fold CV (k = 5 typical), seed reported. Metrics per fold: accuracy + F1 (macro) + AUC where binary; confusion matrix aggregated.
- Imbalance: class weights or resampling stated; headline is F1/AUC, never bare accuracy on skew.
- **Gate**: CV error beats both majority-class and Logistic baselines, or the deliverable is "forest adds nothing" with numbers.

### 4. Visualize the verdict (not the decoration)

- 2-D embedding (PCA/UMAP) colored by cluster/label for the report — via `statistical-plot` conventions (N in caption).
- Confusion matrix heatmap for classification. These two figures are required; additional plots only if they change a decision.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Distance on unscaled mixed units | Standardized, method stated |
| K by wish or single metric | Elbow + silhouette, both shown |
| Silhouette < ~0.25 presented as segments | Weak-structure verdict |
| Bare accuracy on skewed classes | F1/AUC + confusion matrix |
| Preprocessing fit on full data | Train-fold-only, leakage line stated |
| Cluster names without profiles | One-sentence per-cluster description |
| Unstable partition averaged quiet | ARI stability reported |

## Output

The deliverable is the grouping or the classifier **plus its evidence**, in this order:

- **Data + preprocess** — n, p, handling, scaling, seed.
- **Clustering**: K-range plots, chosen K with both metrics, stability ARI, cluster profiles. **Classification**: CV scheme, per-fold metrics, confusion matrix, baseline gaps.
- **Figures** — embedding plot + confusion heatmap with N.
- **Limits** — weak structure or unstable signs, valid scope, what would change the grouping.

Don't pad this into a report. The evidence is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "silhouette 0.18 — there are no real groups here, only partitions", give it. When the forest ties Logistic, ship Logistic and say the forest earned nothing.
