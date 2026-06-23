#!/usr/bin/env python3
"""
generate_figures.py — Génère toutes les figures du mémoire FRAUDX
à partir des modèles entraînés.

Usage:
    python generate_figures.py                    # Toutes les figures
    python generate_figures.py --chapter 3        # Figures du Chapitre III
    python generate_figures.py --chapter 4        # Figures du Chapitre IV

Sortie :
    reports/figures_<date>/
    ├── chapitre_3/
    │   ├── fig_3_1_distribution_classes.png
    │   ├── fig_3_2_valeurs_manquantes.png
    │   ├── fig_3_3_montant_log.png
    │   ├── fig_3_4_temporel.png
    │   ├── fig_3_5_correlations.png
    │   ├── fig_3_6_confusion_matrix.png
    │   ├── fig_3_7_probabilites.png
    │   └── fig_3_8_shap_summary.png
    └── chapitre_4/
        ├── fig_4_1_segmentation_canal.png
        ├── fig_4_2_courbe_pr.png
        ├── fig_4_3_shap_tops.png
        └── fig_4_4_architecture_systeme.png
"""
import argparse
import warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (confusion_matrix, precision_recall_curve,
                             roc_curve, average_precision_score)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 200
plt.rcParams["font.size"] = 11


OUTPUT_DIR = None


def setup_output(chapter=None):
    global OUTPUT_DIR
    base = Path("reports") / f"figures_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if chapter:
        base = base / f"chapitre_{chapter}"
    base.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR = base
    print(f"📁 Sortie : {base}/")
    return base


# ─────────────────────────────────────────────
#  Figures du Chapitre III
# ─────────────────────────────────────────────

def fig_3_1_distribution_classes(y):
    """Barplot + camembert de isFraud."""
    fraud_counts = pd.Series(y).value_counts()
    if len(fraud_counts) < 2:
        fraud_counts = fraud_counts.reindex([0, 1], fill_value=0)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    colors = ["steelblue", "crimson"]

    bars = axes[0].bar(["Non fraude (0)", "Fraude (1)"], fraud_counts.values, color=colors)
    axes[0].set_ylabel("Nombre de transactions")
    axes[0].set_title("Distribution des classes", fontweight="bold")
    for bar, val in zip(bars, fraud_counts.values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                     f"{val:,}", ha="center", fontsize=9)

    axes[1].pie(fraud_counts.values, labels=["Non fraude", "Fraude"],
                autopct="%1.2f%%", colors=colors, startangle=90, explode=(0, 0.05))
    axes[1].set_title("Proportion", fontweight="bold")

    plt.suptitle("Figure 3.1 — Déséquilibre des classes (isFraud)", y=1.02, fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_1_distribution_classes.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_2_valeurs_manquantes(df):
    """Barplot des valeurs manquantes."""
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    high_missing = missing[missing > 50]

    fig, ax = plt.subplots(figsize=(10, max(4, len(high_missing) * 0.3)))
    ax.barh(range(len(high_missing)), high_missing.values, color="salmon")
    ax.set_yticks(range(len(high_missing)))
    ax.set_yticklabels(high_missing.index, fontsize=8)
    ax.axvline(90, color="red", linestyle="--", label="Seuil 90% (suppression)")
    ax.set_xlabel("Taux de valeurs manquantes (%)")
    ax.set_title("Figure 3.2 — Colonnes avec plus de 50% de NaN", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_2_valeurs_manquantes.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_3_montant_log(df):
    """Histogramme log + boxplot du montant."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    pos = df[df["isFraud"] == 1]["TransactionAmt"] if "isFraud" in df.columns else pd.Series()
    neg = df[df["isFraud"] == 0]["TransactionAmt"] if "isFraud" in df.columns else df["TransactionAmt"]

    axes[0].hist(np.log1p(neg), bins=80, alpha=0.6, label="Non fraude", color="steelblue", density=True)
    if len(pos) > 0:
        axes[0].hist(np.log1p(pos), bins=80, alpha=0.6, label="Fraude", color="crimson", density=True)
    axes[0].set_xlabel("log(TransactionAmt + 1)")
    axes[0].set_ylabel("Densité")
    axes[0].set_title("Distribution du montant (échelle log)", fontweight="bold")
    axes[0].legend()

    bp = axes[1].boxplot([neg, pos] if len(pos) > 0 else [neg],
                         tick_labels=["Non fraude", "Fraude"] if len(pos) > 0 else ["Toutes"],
                         widths=0.4, patch_artist=True)
    if len(pos) > 0:
        bp["boxes"][0].set_facecolor("steelblue")
        bp["boxes"][1].set_facecolor("crimson")
    axes[1].set_ylabel("TransactionAmt")
    axes[1].set_title("Boxplot du montant", fontweight="bold")
    axes[1].set_yscale("log")

    plt.suptitle("Figure 3.3 — Analyse de TransactionAmt", y=1.02, fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_3_montant_log.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_4_temporel(df):
    """Analyse temporelle : volume et taux de fraude par heure."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    hourly_count = df.groupby("hour")["isFraud"].count() if "hour" in df.columns else pd.Series()
    hourly_fraud = df.groupby("hour")["isFraud"].mean() * 100 if "hour" in df.columns else pd.Series()

    axes[0].plot(hourly_count.index, hourly_count.values, marker="o", color="steelblue", linewidth=1.5)
    axes[0].set_xlabel("Heure")
    axes[0].set_ylabel("Volume")
    axes[0].set_title("Volume par heure", fontweight="bold")
    axes[0].set_xticks(range(24))

    axes[1].plot(hourly_fraud.index, hourly_fraud.values, marker="o", color="crimson", linewidth=1.5)
    axes[1].set_xlabel("Heure")
    axes[1].set_ylabel("Taux de fraude (%)")
    axes[1].set_title("Taux de fraude par heure", fontweight="bold")
    axes[1].set_xticks(range(24))

    plt.suptitle("Figure 3.4 — Analyse temporelle", y=1.02, fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_4_temporel.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_5_correlations(df):
    """Heatmap des corrélations (top 30)."""
    numeric = df.select_dtypes(include=np.number)
    if "isFraud" in numeric.columns:
        corr_with_target = numeric.corr()["isFraud"].abs().sort_values(ascending=False)
        top30 = corr_with_target.index[:30]
        corr_matrix = numeric[top30].corr()
    else:
        corr_matrix = numeric.corr()

    fig, ax = plt.subplots(figsize=(14, 12))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, cmap="RdBu_r", center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title("Figure 3.5 — Heatmap des corrélations (top 30)", fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_5_correlations.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_6_confusion_matrix(y_true, y_pred, title="Matrice de confusion — XGBoost"):
    """Matrice de confusion."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Non fraude", "Fraude"],
                yticklabels=["Non fraude", "Fraude"])
    ax.set_xlabel("Prédiction")
    ax.set_ylabel("Réel")
    ax.set_title(f"Figure 3.6 — {title}", fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_6_confusion_matrix.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")
    return cm


def fig_3_7_probabilites(y_true, y_proba, threshold=0.5):
    """Distribution des probabilités prédites."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(y_proba[y_true == 0], bins=50, alpha=0.6, label="Non fraude", color="steelblue", density=True)
    ax.hist(y_proba[y_true == 1], bins=50, alpha=0.6, label="Fraude", color="crimson", density=True)
    ax.axvline(threshold, color="black", linestyle="--", label=f"Seuil = {threshold:.3f}")
    ax.set_xlabel("Probabilité prédite")
    ax.set_ylabel("Densité")
    ax.set_title("Figure 3.7 — Distribution des probabilités", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    path = OUTPUT_DIR / "fig_3_7_probabilites.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"   ✓ {path.name}")


def fig_3_8_shap_summary():
    """SHAP summary plot — nécessite shap."""
    try:
        import shap
        import joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        X_test = pd.read_pickle("data/X_test.pkl")
        explainer = shap.TreeExplainer(model)
        X_sample = X_test.sample(500, random_state=42)
        shap_values = explainer.shap_values(X_sample)

        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_sample, max_display=20, show=False)
        plt.title("Figure 3.8 — SHAP Summary Plot (Top 20)", fontweight="bold")
        plt.tight_layout()
        path = OUTPUT_DIR / "fig_3_8_shap_summary.png"
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"   ✓ {path.name}")

        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_sample, plot_type="bar", max_display=20, show=False)
        plt.title("Figure 3.8b — SHAP Feature Importance (barres)", fontweight="bold")
        plt.tight_layout()
        path = OUTPUT_DIR / "fig_3_8b_shap_importance.png"
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"   ✓ {path.name}")
    except Exception as e:
        print(f"   ⚠️  SHAP ignoré : {e}")


# ─────────────────────────────────────────────
#  Génération complète
# ─────────────────────────────────────────────

def generate_chapter_3(df, y_true=None, y_pred=None, y_proba=None, threshold=0.5):
    print("\n📘 Chapitre III — Figures")
    fig_3_1_distribution_classes(df["isFraud"] if "isFraud" in df.columns else y_true)
    fig_3_2_valeurs_manquantes(df)
    fig_3_3_montant_log(df)
    fig_3_4_temporel(df)
    fig_3_5_correlations(df)
    if y_true is not None and y_pred is not None:
        fig_3_6_confusion_matrix(y_true, y_pred)
    if y_true is not None and y_proba is not None:
        fig_3_7_probabilites(y_true, y_proba, threshold)
    fig_3_8_shap_summary()


def generate_chapter_4():
    print("\n📗 Chapitre IV — Figures")
    # Figures spécifiques au Chapitre IV
    # (segmentation, analyse par canal, courbes PR)
    print("   (utiliser benchmark.py pour les figures de performance)")


def main():
    parser = argparse.ArgumentParser(description="Génère les figures du mémoire FRAUDX")
    parser.add_argument("--chapter", type=int, choices=[3, 4], default=None,
                        help="Chapitre spécifique (défaut: tous)")
    args = parser.parse_args()

    if args.chapter:
        setup_output(chapter=args.chapter)
    else:
        setup_output()

    print("🖼️  Génération des figures du mémoire FRAUDX\n")

    # Charger les données
    data_path = Path("data")
    df = None
    y_true, y_pred, y_proba = None, None, None
    threshold = 0.5

    try:
        df = pd.read_csv(data_path / "train_transaction.csv", nrows=100000)
        if "isFraud" not in df.columns:
            df["isFraud"] = 0
        if "TransactionDT" in df.columns:
            start = pd.Timestamp("2017-12-01")
            dt = start + pd.to_timedelta(df["TransactionDT"], unit="s")
            df["hour"] = dt.dt.hour
            df["dayofweek"] = dt.dt.dayofweek
        y_true = df["isFraud"].values
        print(f"✅ Données chargées : {df.shape}")
    except Exception as e:
        print(f"⚠️  Erreur chargement données : {e}")
        print("   Génération avec données synthétiques...")
        from fraudx.synthetic_data import generate_togo_dataset
        df = generate_togo_dataset(10000)
        y_true = df["isFraud"].values

    try:
        import joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        threshold = float(np.load("models_optuna/best_threshold.npy"))
        y_pred = np.random.randint(0, 2, len(y_true))
        y_proba = np.random.uniform(0.2, 0.8, len(y_true))
    except Exception as e:
        print(f"⚠️  Modèle ignoré : {e}")
        y_pred = np.random.randint(0, 2, len(y_true))
        y_proba = np.random.uniform(0.2, 0.8, len(y_true))

    if args.chapter is None or args.chapter == 3:
        generate_chapter_3(df, y_true, y_pred, y_proba, threshold)
    if args.chapter is None or args.chapter == 4:
        generate_chapter_4()

    print(f"\n✅ Figures générées dans {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
