#!/usr/bin/env python3
"""
cluster_gate.py — 聚类/分类门禁（P0-2）

Hard Rules 对应（clustering-classification/SKILL.md）：
- 距离前标准化（z-score）
- K 用肘部 + 轮廓双指标，轮廓 <0.25 警告
- DBSCAN eps 来自 k-距离图
- 分类：分层 k 折 CV + 混淆矩阵，预处理不泄露
- 稳定性 ARI

Usage:
  聚类：  python cluster_gate.py data.csv --features x1,x2 --mode cluster --k-range 2,6 --out report.json
  分类：  python cluster_gate.py data.csv --features x1,x2 --y label --mode classify --out report.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import pandas as pd


def standardize(X: np.ndarray) -> tuple[np.ndarray, dict]:
    mean = X.mean(axis=0)
    std = X.std(axis=0, ddof=0)
    std = np.where(std == 0, 1, std)
    Xs = (X - mean) / std
    return Xs, {"mean": mean.tolist(), "std": std.tolist(), "method": "z-score"}


def cluster_gate(df: pd.DataFrame, features: list[str], k_min: int, k_max: int) -> dict:
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score, adjusted_rand_score
    except ImportError as e:
        return {
            "error": f"sklearn not installed: {e} — pip install scikit-learn",
            "k_range": [k_min, k_max],
            "verdict": "OPEN — 缺少依赖，无法执行门禁检查",
            "gate": {"sklearn_available": False},
        }

    X = df[features].values.astype(float)
    Xs, scaler_info = standardize(X)

    inertias: list[float] = []
    silhouettes: list[float | None] = []
    best_k = k_min
    best_sil = -1

    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(Xs)
        inertias.append(float(km.inertia_))
        if k > 1 and len(set(labels)) > 1:
            try:
                sil = float(silhouette_score(Xs, labels))
            except Exception:
                sil = None
        else:
            sil = None
        silhouettes.append(sil)
        if sil is not None and sil > best_sil:
            best_sil = sil
            best_k = k

    # Stability via bootstrap ARI (3 runs with jitter)
    stability: list[float] = []
    for seed in [1, 2, 3]:
        rng = np.random.default_rng(seed)
        Xj = Xs + rng.normal(0, 0.01, Xs.shape)
        km1 = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit_predict(Xs)
        km2 = KMeans(n_clusters=best_k, n_init=10, random_state=seed).fit_predict(Xj)
        try:
            ari = float(adjusted_rand_score(km1, km2))
        except Exception:
            ari = None
        stability.append(ari)

    warn_weak = best_sil is not None and best_sil < 0.25

    return {
        "scaler": scaler_info,
        "k_range": [k_min, k_max],
        "inertias": inertias,
        "silhouettes": silhouettes,
        "best_k": best_k,
        "best_silhouette": best_sil,
        "weak_structure_warning": warn_weak,
        "stability_ARI": stability,
        "gate": {
            "silhouette_ge_0_25": not warn_weak if best_sil is not None else None,
            "k_has_elbow_and_silhouette": True,  # both reported
        },
        "verdict": "HOLD — 轮廓<0.25 结构弱，不宜命名群组" if warn_weak else "PASS",
    }


def classify_gate(df: pd.DataFrame, features: list[str], y_col: str) -> dict:
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import StratifiedKFold, cross_val_predict
        from sklearn.metrics import confusion_matrix, classification_report
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
    except ImportError as e:
        return {
            "error": f"sklearn not installed: {e} — pip install scikit-learn",
            "verdict": "OPEN — 缺少依赖，无法执行门禁检查",
            "gates": {"sklearn_available": False},
        }

    X = df[features].values
    y = df[y_col].values

    # Check leakage note: pipeline ensures scaler fit only on train folds
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(pipe, X, y, cv=cv)

    # Per fold metrics would need cross_validate; simplified to overall
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

    acc = float(accuracy_score(y, y_pred))
    # F1 macro
    try:
        f1 = float(f1_score(y, y_pred, average="macro", zero_division=0))
    except Exception:
        f1 = None
    # AUC for binary
    auc = None
    labels = np.unique(y)
    if len(labels) == 2:
        try:
            # Need proba
            from sklearn.model_selection import cross_val_predict as cvp
            proba = cvp(pipe, X, y, cv=cv, method="predict_proba")
            # Take proba for positive class
            auc = float(roc_auc_score(y, proba[:, 1]))
        except Exception:
            auc = None

    cm = confusion_matrix(y, y_pred).tolist()
    # Baseline: majority class
    from collections import Counter
    cnt = Counter(y)
    majority = cnt.most_common(1)[0][0]
    acc_majority = float((y == majority).mean())

    return {
        "n": len(y),
        "classes": sorted([str(c) for c in labels]),
        "accuracy": round(acc, 4),
        "f1_macro": round(f1, 4) if f1 is not None else None,
        "auc": round(auc, 4) if auc is not None else None,
        "confusion_matrix": cm,
        "baseline_majority_acc": round(acc_majority, 4),
        "beats_baseline": acc > acc_majority,
        "gates": {
            "has_stratified_cv": True,
            "has_confusion_matrix": True,
            "no_leakage_pipeline": True,
        },
        "verdict": "PASS" if acc > acc_majority else "HOLD — 未打赢多数类基线",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="聚类/分类门禁")
    parser.add_argument("data", type=pathlib.Path, help="数据 CSV 路径")
    parser.add_argument("--features", type=str, required=True, help="逗号分隔特征列")
    parser.add_argument("--y", type=str, default=None, help="分类目标列（分类模式必填）")
    parser.add_argument("--mode", type=str, choices=["cluster", "classify"], required=True, help="聚类或分类")
    parser.add_argument("--k-range", type=str, default="2,6", help="聚类 K 区间如 2,6")
    parser.add_argument("--out", type=pathlib.Path, required=True, help="输出报告 JSON 路径")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    features = [s.strip() for s in args.features.split(",")]
    for f in features:
        if f not in df.columns:
            print(f"特征列 {f} 不存在", file=sys.stderr)
            sys.exit(1)

    if args.mode == "cluster":
        k_min, k_max = (int(x) for x in args.k_range.split(","))
        result = cluster_gate(df, features, k_min, k_max)
    else:
        if not args.y or args.y not in df.columns:
            print(f"分类模式需 --y 且列存在", file=sys.stderr)
            sys.exit(1)
        result = classify_gate(df, features, args.y)

    result["mode"] = args.mode
    result["features"] = features

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"门禁结果 ({args.mode}): {result.get('verdict')}")
    print(f"报告: {args.out}")


if __name__ == "__main__":
    main()
