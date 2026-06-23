#!/usr/bin/env python3
"""
benchmark.py — Benchmark complet des modèles FRAUDX
Compare Isolation Forest, Random Forest, XGBoost côte-à-côte.

Usage:
    python benchmark.py                          # Benchmark complet
    python benchmark.py --fast                   # Version rapide (100k lignes)
    python benchmark.py --models if rf xgb       # Modèles spécifiques

Sortie :
    reports/benchmark_<date>/
    ├── metrics_comparison.csv       # Tableau comparatif
    ├── metrics_comparison_latex.txt # Tableau LaTeX pour le mémoire
    ├── precision_recall_curve.png   # Courbes PR
    ├── roc_curve.png                # Courbes ROC
    ├── barplot_comparison.png       # Barplot F1/Recall/Precision
    ├── confusion_matrices.png       # Matrices de confusion
    └── summary.json                 # Résumé structuré
"""
import argparse
import json
import time
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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (confusion_matrix, f1_score, recall_score,
                             precision_score, average_precision_score,
                             roc_auc_score, precision_recall_curve, roc_curve)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 150


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark FRAUDX")
    parser.add_argument("--fast", action="store_true", help="Mode rapide")
    parser.add_argument("--models", nargs="+", default=["if", "rf", "xgb"],
                        choices=["if", "rf", "xgb"],
                        help="Modèles à comparer")
    parser.add_argument("--output", type=str, default="reports",
                        help="Dossier de sortie")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def load_data(fast=False):
    """Charge les données prétraitées ou les génère."""
    data_path = Path("data")

    # Essayer de charger les données existantes
    train_file = data_path / "train_transaction.csv"
    if train_file.exists():
        print(f"📂 Chargement de {train_file}...")
        nrows = 100000 if fast else None
        df = pd.read_csv(train_file, nrows=nrows)
        print(f"   Dimensions : {df.shape}, Fraude: {df['isFraud'].mean()*100:.2f}%")
        return df

    # Fallback : générer des données synthétiques
    print("⚠️  Dataset IEEE-CIS non trouvé. Génération de données synthétiques...")
    from fraudx.synthetic_data import generate_togo_dataset
    df = generate_togo_dataset(n_transactions=20000 if fast else 50000)
    df = df.rename(columns={"montant_cfa": "TransactionAmt",
                            "canal": "ProductCD",
                            "operateur": "card4"})
    # Créer des colonnes numériques factices pour le test
    np.random.seed(42)
    for prefix in ["V", "C", "D"]:
        for i in range(5):
            df[f"{prefix}{i}"] = np.random.randn(len(df))
    return df


def preprocess_benchmark(df, random_state=42):
    """Prétraitement simplifié pour le benchmark."""
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.impute import SimpleImputer

    y = df["isFraud"].values

    # Feature engineering
    if "TransactionDT" in df.columns:
        import datetime
        start = datetime.datetime(2017, 12, 1)
        dt = df["TransactionDT"].apply(lambda x: start + datetime.timedelta(seconds=int(x)))
        df["hour"] = dt.dt.hour
        df["dayofweek"] = dt.dt.dayofweek
    if "TransactionAmt" in df.columns:
        df["log_amount"] = np.log1p(df["TransactionAmt"])

    # Garder les colonnes numériques
    drop_cols = ["isFraud", "TransactionID", "TransactionDT", "TransactionDT_dt",
                 "timestamp", "transaction_id", "user_id", "agent_id",
                 "fraud_type", "type_operation"]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(include="object").columns.tolist()

    # Imputation
    X_num = pd.DataFrame(SimpleImputer(strategy="median").fit_transform(X[num_cols]),
                         columns=num_cols, index=X.index)

    # Encodage simple des catégorielles
    X_cat = pd.DataFrame()
    for col in cat_cols:
        X_cat[col] = SimpleImputer(strategy="most_frequent").fit_transform(X[[col]]).ravel()
        X_cat[col] = X_cat[col].astype("category").cat.codes

    X_processed = pd.concat([X_num, X_cat], axis=1)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, stratify=y, random_state=random_state
    )

    # Scaling
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train),
                                  columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test),
                                 columns=X_test.columns, index=X_test.index)

    # SMOTE pour XGBoost et RF
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X_train_scaled, y_train)

    return (X_train_scaled, X_test_scaled, y_train, y_test,
            X_res, y_res, scaler)


def train_and_evaluate(model, model_name, X_train, y_train, X_test, y_test):
    """Entraîne et évalue un modèle, retourne les métriques."""
    t0 = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - t0

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    if y_proba is None:
        # Isolation Forest
        y_score = -model.score_samples(X_test)
        y_proba = (y_score - y_score.min()) / (y_score.max() - y_score.min() + 1e-10)
        y_pred_bin = np.where(y_pred == -1, 1, 0)
    else:
        y_pred_bin = y_pred

    cm = confusion_matrix(y_test, y_pred_bin)
    metrics = {
        "model": model_name,
        "f1_score": float(f1_score(y_test, y_pred_bin)),
        "recall": float(recall_score(y_test, y_pred_bin)),
        "precision": float(precision_score(y_test, y_pred_bin)),
        "auc_pr": float(average_precision_score(y_test, y_proba)),
        "auc_roc": float(roc_auc_score(y_test, y_proba)),
        "train_time_s": round(train_time, 2),
        "tn": int(cm[0, 0]), "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]), "tp": int(cm[1, 1]),
    }
    return metrics, y_proba, y_pred_bin


def plot_pr_curves(results, output_dir, y_test):
    """Courbes Precision-Recall comparatives."""
    plt.figure(figsize=(8, 6))
    for model_name, y_proba in results["probas"].items():
        precisions, recalls, _ = precision_recall_curve(y_test, y_proba)
        auc_pr = average_precision_score(y_test, y_proba)
        plt.plot(recalls, precisions, label=f"{model_name} (AUC-PR={auc_pr:.3f})", linewidth=2)

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Courbes Precision-Recall — Comparaison des modèles")
    plt.legend(loc="lower left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/precision_recall_curve.png", dpi=150)
    plt.close()
    print(f"   ✓ precision_recall_curve.png")


def plot_roc_curves(results, output_dir, y_test):
    """Courbes ROC comparatives."""
    plt.figure(figsize=(8, 6))
    for model_name, y_proba in results["probas"].items():
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        plt.plot(fpr, tpr, label=f"{model_name} (AUC={auc:.3f})", linewidth=2)

    plt.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Aléatoire")
    plt.xlabel("Taux de faux positifs (FPR)")
    plt.ylabel("Taux de vrais positifs (TPR)")
    plt.title("Courbes ROC — Comparaison des modèles")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/roc_curve.png", dpi=150)
    plt.close()
    print(f"   ✓ roc_curve.png")


def plot_barplot(metrics_df, output_dir):
    """Barplot comparatif F1/Recall/Precision."""
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(metrics_df))
    width = 0.25

    bars1 = ax.bar(x - width, metrics_df["f1_score"], width, label="F1-Score", color="#2E86AB")
    bars2 = ax.bar(x, metrics_df["recall"], width, label="Recall", color="#A23B72")
    bars3 = ax.bar(x + width, metrics_df["precision"], width, label="Precision", color="#F18F01")

    ax.set_xlabel("Modèle")
    ax.set_ylabel("Score")
    ax.set_title("Comparaison des performances par modèle")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_df["model"])
    ax.legend()
    ax.set_ylim(0, 1.05)

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.01,
                    f"{height:.3f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/barplot_comparison.png", dpi=150)
    plt.close()
    print(f"   ✓ barplot_comparison.png")


def plot_confusion_matrices(results, output_dir, y_test):
    """Matrices de confusion pour chaque modèle."""
    n_models = len(results["predictions"])
    fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4))
    if n_models == 1:
        axes = [axes]

    for ax, (model_name, y_pred) in zip(axes, results["predictions"].items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=["Normal", "Fraude"],
                    yticklabels=["Normal", "Fraude"])
        ax.set_title(f"{model_name}")
        ax.set_xlabel("Prédiction")
        ax.set_ylabel("Réel")

    plt.suptitle("Matrices de confusion", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrices.png", dpi=150)
    plt.close()
    print(f"   ✓ confusion_matrices.png")


def generate_latex_table(metrics_df):
    """Génère un tableau LaTeX pour le mémoire."""
    latex = []
    latex.append(r"\begin{table}[h]")
    latex.append(r"\centering")
    latex.append(r"\caption{Comparaison des performances des modèles}")
    latex.append(r"\label{tab:model_comparison}")
    latex.append(r"\begin{tabular}{lccccccc}")
    latex.append(r"\toprule")
    latex.append(r"Modèle & F1-Score & Recall & Precision & AUC-PR & AUC-ROC & FP & FN \\")
    latex.append(r"\midrule")

    for _, row in metrics_df.iterrows():
        latex.append(
            f"  {row['model']} & {row['f1_score']:.4f} & {row['recall']:.4f} & "
            f"{row['precision']:.4f} & {row['auc_pr']:.4f} & {row['auc_roc']:.4f} & "
            f"{int(row['fp'])} & {int(row['fn'])} \\\\"
        )

    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    return "\n".join(latex)


def main():
    args = parse_args()
    output_dir = Path(args.output) / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("""
╔══════════════════════════════════════════╗
║     FRAUDX — Benchmark des modèles       ║
╚══════════════════════════════════════════╝
    """)
    print(f"Modèles : {args.models}")
    print(f"Mode : {'Rapide' if args.fast else 'Complet'}")
    print(f"Sortie : {output_dir}/\n")

    # 1. Chargement
    df = load_data(fast=args.fast)

    # 2. Prétraitement
    print("\n⚙️  Prétraitement...")
    X_train, X_test, y_train, y_test, X_res, y_res, scaler = preprocess_benchmark(df)

    n_models = len(args.models)
    n_features = X_train.shape[1]
    fraud_rate = y_train.mean()
    print(f"   Train : {X_train.shape}, Test : {X_test.shape}")
    print(f"   SMOTE : {X_res.shape}")
    print(f"   Features : {n_features}, Fraude train : {fraud_rate*100:.2f}%")

    # 3. Benchmark
    results = {"metrics": [], "probas": {}, "predictions": {}}

    if "if" in args.models:
        print("\n🌲 Isolation Forest...")
        iso = IsolationForest(contamination=fraud_rate, random_state=args.seed, n_jobs=-1)
        metrics, y_proba, y_pred = train_and_evaluate(
            iso, "Isolation Forest", X_train, None, X_test, y_test
        )
        results["metrics"].append(metrics)
        results["probas"]["Isolation Forest"] = y_proba
        results["predictions"]["Isolation Forest"] = y_pred

    if "rf" in args.models:
        print("🌳 Random Forest...")
        rf = RandomForestClassifier(n_estimators=100, max_depth=10,
                                    random_state=args.seed, n_jobs=-1, class_weight="balanced")
        metrics, y_proba, y_pred = train_and_evaluate(
            rf, "Random Forest", X_res, y_res, X_test, y_test
        )
        results["metrics"].append(metrics)
        results["probas"]["Random Forest"] = y_proba
        results["predictions"]["Random Forest"] = y_pred

    if "xgb" in args.models:
        print("⚡ XGBoost...")
        xgb = XGBClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.1,
            subsample=0.8, colsample_bytree=0.8, gamma=0.1,
            reg_alpha=0.1, reg_lambda=1.0,
            random_state=args.seed, use_label_encoder=False, eval_metric="logloss"
        )
        metrics, y_proba, y_pred = train_and_evaluate(
            xgb, "XGBoost", X_res, y_res, X_test, y_test
        )
        results["metrics"].append(metrics)
        results["probas"]["XGBoost"] = y_proba
        results["predictions"]["XGBoost"] = y_pred

    # 4. Fusion des métriques
    metrics_df = pd.DataFrame(results["metrics"])

    print("\n" + "=" * 60)
    print("📊 TABLEAU COMPARATIF")
    print("=" * 60)
    print(metrics_df.to_string(index=False))
    print("=" * 60)

    # 5. Sauvegarde CSV
    metrics_df.to_csv(f"{output_dir}/metrics_comparison.csv", index=False)
    print(f"\n✅ metrics_comparison.csv")

    # 6. Tableau LaTeX
    latex = generate_latex_table(metrics_df)
    with open(f"{output_dir}/metrics_comparison_latex.txt", "w", encoding="utf-8") as f:
        f.write(latex)
    print(f"✅ metrics_comparison_latex.txt (prêt pour le mémoire)")

    # 7. Figures
    print("\n📈 Génération des figures...")
    plot_pr_curves(results, output_dir, y_test)
    plot_roc_curves(results, output_dir, y_test)
    plot_barplot(metrics_df, output_dir)
    plot_confusion_matrices(results, output_dir, y_test)

    # 8. Rapport JSON
    summary = {
        "date": datetime.now().isoformat(),
        "n_transactions": len(df),
        "n_features": n_features,
        "fraud_rate": float(fraud_rate),
        "models_tested": args.models,
        "metrics": results["metrics"],
        "best_model": metrics_df.loc[metrics_df["f1_score"].idxmax(), "model"],
        "best_f1": float(metrics_df["f1_score"].max()),
    }
    with open(f"{output_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✅ summary.json")

    print(f"\n📁 Rapport complet : {output_dir}/")
    print(f"\n🏆 Meilleur modèle : {summary['best_model']} (F1={summary['best_f1']:.4f})")


if __name__ == "__main__":
    main()
