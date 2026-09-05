---
name: bp-neural-network
description: "反向传播前馈网络拟合非线性回归或分类。Use when 几十到几千样本、特征与目标复杂非线性时；需可解释系数用 regression-family。"
---
# BP 神经网络

> 先读仓库根目录的 CONTEXT.md（术语/单位/venue 默认），全文用它的词。

A construction skill. It does ONE thing: fit a nonlinear regression or classification with a backprop feedforward net that beats a linear baseline out of sample. It does not do interpretable coefficient modeling (that's `regression-family`), label discovery (that's `clustering-classification`), or deep learning at scale.

## Operating Posture

You are a modeling specialist spending parameters only where the nonlinearity earns them. The bar is a held-out number: validation or cross-validated error better than linear/regularized regression, with the gap reported — not training loss going down. Write it so the baseline comparison passes the first time.

Two failure modes, and the first is worse:

1. **Using a network where a line would do.** Dozens of samples with a roughly linear relation don't need hidden layers; they need `regression-family`. A network that ties linear regression is complexity with no return.
2. **Reporting training fit as performance** — no held-out split, no scaling, no early stopping, seed unreported, single lucky run. Training RMSE from an overfit net is a memorization score.

Never present a network without its held-out error and the baseline it beat. No baseline, no network.

## Hard Rules

1. **Split before touching the model.** Train/validation/test (or k-fold CV when n is small), split once, seed fixed and reported. Test set opens exactly once, at the end.
2. **Standardize features from training statistics only.** Mean/std computed on train, applied to validation/test. Scaling on the full data leaks.
3. **Start small.** One hidden layer, few units; grow only while validation improves. Parameter count ≪ n. A 200-unit layer on 80 samples is not modeling.
4. **Early stopping with patience, always.** Monitor validation loss; stop when it stalls (patience stated, e.g. 10–50 epochs depending on scale). No fixed-epoch training without a learning curve to justify it.
5. **Report CV error + seed variance.** Mean ± std over folds or seeds. A single run's number is anecdote; the spread is the result.

## The Build Sequence

### 1. Should this be a BP network at all?

| Situation | Decision |
| --- | --- |
| Dozens to thousands of samples, clearly nonlinear, baseline linear fails | **BP network. Continue.** |
| Need interpretable coefficients or variable selection | Stop. Use `regression-family`. |
| No labels, looking for groups | Stop. Use `clustering-classification`. |
| Images, sequences, or millions of samples | Stop. That's deep learning beyond this skill's scope — say so. |

Fit linear/ridge regression first, always. If the network can't beat it out of sample, ship the linear model and say why.

### 2. Data, split, scale

- EDA: n, p, missing values, target distribution, obvious outliers. Name the handling.
- Split (seed reported): e.g. 70/15/15 train/val/test, or 5-fold CV for n < ~500.
- Standardize features (train stats only); encode categoricals; normalize/image-scale targets for regression if it stabilizes training — and invert back before reporting error in original units.

### 3. Architecture and training

- Start: 1 hidden layer, units ≈ √(p·out) to 2p, tanh/ReLU hidden, linear/sigmoid/softmax output per task. Grow only on validation signal.
- Loss matches the task: MSE/MAE for regression, cross-entropy for classification. State it.
- Optimizer + learning rate stated (e.g. Adam 1e-3); learning curves (train vs val loss) plotted and kept. Divergence or wild oscillation → lower lr, don't just add epochs.
- Early stopping on validation loss with stated patience; restore best weights.

### 4. Evaluate honestly

- Test-once error in original units: RMSE/MAE (regression) or accuracy/F1/AUC + confusion matrix (classification), with the baseline's number beside it.
- **Gate**: network beats baseline out of sample, or the deliverable is "network adds nothing" with the numbers shown. Never tune on test; if test disappoints after val looked good, report both and diagnose (distribution shift? too small n?) instead of re-splitting quietly.
- Seed/fold spread: mean ± std. Wide spread on tiny n is itself a finding — report it.

### 5. Interpret within limits

- Sensitivity: which inputs move the output most (permutation importance or partial dependence on 1–2 key features). No claims about "learned physics" beyond what the checks support.
- Limits: data range of validity. Networks extrapolate badly — state the input domain the model is valid on.

## Never Ship

Self-check before you finish. Each is an automatic block:

| Never | Instead |
| --- | --- |
| Training error as the headline | Held-out / CV error, mean ± std |
| No baseline comparison | Linear-regularized baseline, same split |
| Scaling on full data | Train stats only, seed reported |
| Fixed epochs, no learning curve | Early stopping + curves kept |
| Test set opened twice | Once, at the end; disappointment reported honestly |
| Giant net on tiny n | Params ≪ n, grow on validation signal only |
| Extrapolation claims | Valid input domain stated |

## Output

The deliverable is the model **plus its honest scorecard**, in this order:

- **Data + split** — n, p, handling, split ratio, seed.
- **Architecture + training** — layers, units, activations, loss, optimizer/lr, patience, curves.
- **Scorecard** — CV/test error (mean ± std) vs baseline, confusion matrix or residual plot.
- **Interpretation + limits** — key drivers, valid domain, what would break it.

Don't pad this into a report. The scorecard is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "ridge regression ties your network — ship ridge", give it. When n is too small for any network, refuse instead of shrinking the validation set into existence.
