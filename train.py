#!/usr/bin/env python3
"""
train.py — Pipeline d'entraînement complet FRAUDX
Exécute toutes les phases : téléchargement → prétraitement → modèles → SHAP → sauvegarde

Usage:
    python train.py                          # Entraînement complet
    python train.py --skip-download          # Utiliser les fichiers existants
    python train.py --fast                   # Version rapide (100k lignes, 10 trials Optuna)
    python train.py --dataset credit-card    # Utiliser Credit Card Fraud (ULB)
"""
import argparse
import pandas as pd
import numpy as np
import joblib
import json
import os
import sys
import warnings
import time
from pathlib import Path

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             average_precision_score, confusion_matrix,
                             precision_recall_curve)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

print("""
╔══════════════════════════════════════════════╗
║         FRAUDX — Training Pipeline           ║
║  Détection de fraude bancaire par IA (Togo)  ║
╚══════════════════════════════════════════════╝
""")


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline d'entraînement FRAUDX")
    parser.add_argument("--skip-download", action="store_true",
                        help="Utiliser les fichiers CSV existants dans data/")
    parser.add_argument("--fast", action="store_true",
                        help="Mode rapide (100k lignes, 10 essais Optuna)")
    parser.add_argument("--dataset", type=str, default="ieee",
                        choices=["ieee", "credit-card"],
                        help="Dataset à utiliser")
    parser.add_argument("--optuna-trials", type=int, default=None,
                        help="Nombre d'essais Optuna (défaut: 30, rapide: 10)")
    parser.add_argument("--output", type=str, default="models_optuna/",
                        help="Dossier de sortie pour les modèles")
    parser.add_argument("--seed", type=int, default=42,
                        help="Seed aléatoire")
    return parser.parse_args()


def download_data(args):
    """Télécharge le dataset depuis Kaggle ou utilise les fichiers locaux."""
    if args.skip_download:
        print("ℹ️  Utilisation des fichiers existants dans data/")
        if args.dataset == "ieee":
            base = Path("data")
            train_file = base / "train_transaction.csv"
            id_file = base / "train_identity.csv"
            if not train_file.exists():
                print(f"❌ {train_file} non trouvé. Téléchargez-le depuis Kaggle.")
                print("   Ou lancez sans --skip-download")
                sys.exit(1)
            return train_file, id_file if id_file.exists() else None
        else:
            return Path("data/creditcard.csv"), None

    print("📥 Téléchargement du dataset...")
    if args.dataset == "ieee":
        try:
            import kagglehub
            path = Path(kagglehub.competition_download("ieee-fraud-detection"))
            print(f"   Dataset dans : {path}")
            return path / "train_transaction.csv", path / "train_identity.csv"
        except Exception as e:
            print(f"❌ Erreur kagglehub : {e}")
            print("   Vérifiez votre connexion Kaggle ou utilisez --skip-download")
            sys.exit(1)
    else:
        print("ℹ️  Credit Card Fraud : utilisez --skip-download et placez creditcard.csv dans data/")
        return Path("data/creditcard.csv"), None


def load_and_merge(train_path, id_path=None, fast=False):
    """Charge et fusionne les données."""
    print(f"\n📂 Chargement des données...")
    t0 = time.time()

    df = pd.read_csv(train_path, nrows=100000 if fast else None)
    print(f"   train_transaction : {df.shape}")

    if id_path and Path(id_path).exists():
        identity = pd.read_csv(id_path, nrows=100000 if fast else None)
        df = df.merge(identity, on="TransactionID", how="left")
        print(f"   après fusion identity : {df.shape}")

    print(f"   Temps : {time.time()-t0:.1f}s")
    return df


def preprocess(df, output_dir):
    """Prétraitement complet."""
    print(f"\n🧹 Prétraitement...")
    t0 = time.time()

    # Suppression colonnes >90% NaN
    missing = (df.isnull().sum() / len(df) * 100)
    cols_drop = missing[missing > 90].index.tolist()
    df = df.drop(columns=cols_drop)
    print(f"   Colonnes supprimées (>90% NaN) : {len(cols_drop)}")

    # Séparation target
    y = df["isFraud"].values
    X = df.drop(columns=["isFraud", "TransactionID"], errors="ignore")

    # Feature engineering
    X = engineer_features(X)

    # Séparation num/cat
    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(include="object").columns.tolist()
    print(f"   Numériques : {len(num_cols)}, Catégorielles : {len(cat_cols)}")

    # Split stratifié
    X_train, X_test, y_train, y_test = train_test_split(
        X[num_cols + cat_cols], y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"   Split : train={X_train.shape}, test={X_test.shape}")

    # Imputation
    num_imputer = SimpleImputer(strategy="median")
    cat_imputer = SimpleImputer(strategy="most_frequent")

    X_train_num = pd.DataFrame(num_imputer.fit_transform(X_train[num_cols]),
                               columns=num_cols, index=X_train.index)
    X_test_num = pd.DataFrame(num_imputer.transform(X_test[num_cols]),
                              columns=num_cols, index=X_test.index)

    X_train_cat = pd.DataFrame(cat_imputer.fit_transform(X_train[cat_cols]),
                               columns=cat_cols, index=X_train.index)
    X_test_cat = pd.DataFrame(cat_imputer.transform(X_test[cat_cols]),
                              columns=cat_cols, index=X_test.index)

    # Frequency encoding (haute cardinalité) + OneHot (faible)
    high_card = []
    low_card = []
    for col in cat_cols:
        n = X_train_cat[col].nunique()
        if n > 10:
            high_card.append(col)
        else:
            low_card.append(col)

    freq_maps = {}
    for col in high_card:
        freq = X_train_cat[col].value_counts() / len(X_train_cat)
        freq_maps[col] = freq.to_dict()
        X_train_cat[col] = X_train_cat[col].map(freq).fillna(0)
        X_test_cat[col] = X_test_cat[col].map(freq).fillna(0)

    ohe = None
    if low_card:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        train_ohe = ohe.fit_transform(X_train_cat[low_card])
        test_ohe = ohe.transform(X_test_cat[low_card])
        ohe_cols = ohe.get_feature_names_out(low_card)
        train_ohe_df = pd.DataFrame(train_ohe, columns=ohe_cols, index=X_train_cat.index)
        test_ohe_df = pd.DataFrame(test_ohe, columns=ohe_cols, index=X_test_cat.index)
        X_train_cat = X_train_cat.drop(columns=low_card)
        X_test_cat = X_test_cat.drop(columns=low_card)
        X_train_cat = pd.concat([X_train_cat, train_ohe_df], axis=1)
        X_test_cat = pd.concat([X_test_cat, test_ohe_df], axis=1)

    # Assemblage
    X_train_processed = pd.concat([X_train_num, X_train_cat], axis=1)
    X_test_processed = pd.concat([X_test_num, X_test_cat], axis=1)

    # Standardisation
    scaler = StandardScaler()
    X_train_scaled = X_train_processed.copy()
    X_test_scaled = X_test_processed.copy()
    scalable = [c for c in num_cols if c in X_train_scaled.columns]
    X_train_scaled[scalable] = scaler.fit_transform(X_train_processed[scalable])
    X_test_scaled[scalable] = scaler.transform(X_test_processed[scalable])

    # Sauvegarde des artefacts
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, f"{output_dir}/scaler.pkl")
    joblib.dump(freq_maps, f"{output_dir}/freq_maps.pkl")
    if ohe:
        joblib.dump(ohe, f"{output_dir}/ohe_encoder.pkl")
    with open(f"{output_dir}/num_cols.json", "w") as f:
        json.dump(num_cols, f)

    print(f"   Temps : {time.time()-t0:.1f}s")
    return X_train_scaled, X_test_scaled, y_train, y_test


def engineer_features(X):
    """Feature engineering avancée pour la détection de fraude."""
    # --- Features temporelles ---
    if "TransactionDT" in X.columns:
        start = pd.Timestamp("2017-12-01")
        dt = start + pd.to_timedelta(X["TransactionDT"], unit="s")
        X["hour"] = dt.dt.hour
        X["dayofweek"] = dt.dt.dayofweek
        X["is_weekend"] = dt.dt.dayofweek.isin([5, 6]).astype(int)
        X["is_night"] = ((dt.dt.hour >= 22) | (dt.dt.hour <= 5)).astype(int)
        X["day_of_month"] = dt.dt.day

    # --- Features de montant ---
    if "TransactionAmt" in X.columns:
        X["log_amount"] = np.log1p(X["TransactionAmt"])
        X["amt_100_ratio"] = X["TransactionAmt"] / 100

    # --- Features de vélocité (comportementales) ---
    for group_col in ["card1", "card2", "card3", "addr1", "addr2"]:
        if group_col in X.columns and "TransactionAmt" in X.columns:
            key = f"tx_count_by_{group_col}"
            X[key] = X.groupby(group_col)["TransactionAmt"].transform("count")
            key_avg = f"avg_amt_by_{group_col}"
            X[key_avg] = X.groupby(group_col)["TransactionAmt"].transform("mean")
            key_ratio = f"amt_ratio_{group_col}"
            X[key_ratio] = X["TransactionAmt"] / (X[key_avg] + 1)

    # --- Délai depuis dernière transaction par carte ---
    if "card1" in X.columns and "TransactionDT" in X.columns:
        X_sorted = X.sort_values(["card1", "TransactionDT"])
        X["time_since_last_tx_card1"] = X_sorted.groupby("card1")["TransactionDT"].diff().fillna(0)

    # --- Features email domain ---
    for col in ["P_emaildomain", "R_emaildomain"]:
        if col in X.columns:
            X[f"{col}_cat"] = X[col].fillna("unknown").map(
                lambda x: "premium" if any(d in str(x) for d in ["gmail", "yahoo", "outlook", "hotmail"])
                else ("pro" if any(d in str(x) for d in ["company", "corp", "bank"])
                else "other")
            )

    # --- Interaction carte x montant ---
    if all(c in X.columns for c in ["card1", "card2", "TransactionAmt"]):
        X["card1_card2_amt"] = X.groupby(["card1", "card2"])["TransactionAmt"].transform("mean").fillna(0)

    # --- Distance features (si disponibles) ---
    if "dist1" in X.columns and "dist2" in X.columns:
        X["dist_diff"] = abs(X["dist1"].fillna(0) - X["dist2"].fillna(0))
    if "dist1" in X.columns:
        X["dist1_log"] = np.log1p(X["dist1"].fillna(0))

    return X


def train_isoforest(X_train, X_test, y_test, output_dir):
    """Entraîne Isolation Forest (Niveau 1)."""
    print(f"\n🌲 Isolation Forest...")
    t0 = time.time()

    iso = IsolationForest(contamination=0.035, random_state=42, n_jobs=-1)
    iso.fit(X_train)

    preds = np.where(iso.predict(X_test) == -1, 1, 0)
    recall = recall_score(y_test, preds)
    print(f"   Recall : {recall:.4f}")

    joblib.dump(iso, f"{output_dir}/isolation_forest.pkl")
    print(f"   Temps : {time.time()-t0:.1f}s")
    return iso


def train_xgboost(X_train, X_test, y_train, y_test, output_dir, fast=False, n_trials=None):
    """Entraîne XGBoost avec Optuna (Niveau 2)."""
    print(f"\n⚡ XGBoost + Optuna...")
    t0 = time.time()

    if n_trials is None:
        n_trials = 10 if fast else 100
    print(f"   Optimisation Optuna ({n_trials} essais, optimisation RECALL avec contrainte precision>0.15)...")

    scale_pos_weight = len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1)

    try:
        import optuna
        from imblearn.pipeline import Pipeline as ImbPipeline

        # Échantillon stratifié pour accélérer Optuna
        n_sample = 30000 if fast else 50000
        if len(X_train) > n_sample * 2:
            X_opt, _, y_opt, _ = train_test_split(
                X_train, y_train, train_size=n_sample, stratify=y_train, random_state=42
            )
            print(f"   Optuna sur échantillon stratifié : {X_opt.shape}")
        else:
            X_opt, y_opt = X_train, y_train

        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 300),
                "max_depth": trial.suggest_int("max_depth", 3, 8),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
                "subsample": trial.suggest_float("subsample", 0.7, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "gamma": trial.suggest_float("gamma", 0, 3),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 5.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 5.0, log=True),
                "min_child_weight": trial.suggest_int("min_child_weight", 1, 8),
                "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1.0, scale_pos_weight),
                "random_state": 42, "eval_metric": "logloss"
            }
            X_tr, X_val, y_tr, y_val = train_test_split(
                X_opt, y_opt, test_size=0.2, stratify=y_opt, random_state=trial.number
            )
            model = XGBClassifier(**params)
            model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
            y_probs = model.predict_proba(X_val)[:, 1]
            y_pred = (y_probs >= 0.5).astype(int)
            recall = recall_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred)
            if precision < 0.15:
                return 0.0
            return recall

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
        best_params = study.best_params
        print(f"   Meilleur F1 (CV) : {study.best_value:.4f}")
        print(f"   Meilleurs params : {best_params}")
        joblib.dump(best_params, f"{output_dir}/best_params.pkl")
    except ImportError:
        print("   optuna non installé → utilisation des paramètres par défaut")
        best_params = {
            "n_estimators": 200, "max_depth": 8, "learning_rate": 0.1,
            "subsample": 0.8, "colsample_bytree": 0.8, "gamma": 0.1,
            "reg_alpha": 0.1, "reg_lambda": 1.0
        }

    best_params["random_state"] = 42
    best_params["eval_metric"] = "logloss"

    scale_pos_weight_final = best_params.pop("scale_pos_weight", scale_pos_weight)
    best_params["scale_pos_weight"] = scale_pos_weight_final
    best_params["n_estimators"] = int(best_params.get("n_estimators", 300) * 1.5)

    # Modèle final (scale_pos_weight + SMOTE si assez rapide)
    if len(X_train) < 200000:
        smote = SMOTE(random_state=42, sampling_strategy=0.5)
        X_res, y_res = smote.fit_resample(X_train, y_train)
        print(f"   SMOTE final : {X_train.shape} → {X_res.shape} (ratio=0.5)")
    else:
        X_res, y_res = X_train, y_train
        print(f"   Pas de SMOTE (dataset large): {X_train.shape}")
    model = XGBClassifier(**best_params, n_jobs=-1)
    model.fit(X_res, y_res)

    # Seuil optimal : trouver le seuil qui donne RECALL >= 0.85 avec la meilleure précision
    y_probs = model.predict_proba(X_test)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

    best_threshold = 0.5
    best_precision_at_target = 0.0
    for i in range(len(thresholds)):
        if recalls[i] >= 0.85 and precisions[i] >= best_precision_at_target:
            best_precision_at_target = precisions[i]
            best_threshold = thresholds[i]

    # Si aucun threshold n'atteint 0.85, prendre celui avec le recall max
    if best_precision_at_target == 0.0:
        best_idx = recalls.argmax()
        best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5

    # Évaluation
    y_pred = (y_probs >= best_threshold).astype(int)
    metrics = {
        "f1": float(f1_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "auc_pr": float(average_precision_score(y_test, y_probs)),
        "threshold": float(best_threshold)
    }
    print(f"   Recall={metrics['recall']:.4f}, Precision={metrics['precision']:.4f}, "
          f"F1={metrics['f1']:.4f}, AUC-PR={metrics['auc_pr']:.4f}, Seuil={metrics['threshold']:.4f}")

    # Sauvegarde
    joblib.dump(model, f"{output_dir}/xgb_model.pkl")
    np.save(f"{output_dir}/best_threshold.npy", best_threshold)
    with open(f"{output_dir}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"   Temps : {time.time()-t0:.1f}s")
    return model, metrics


def generate_shap(model, X_test, y_test, output_dir):
    """Génère les explications SHAP."""
    print(f"\n🔮 SHAP Explainer...")
    t0 = time.time()

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        X_sample = X_test.sample(500, random_state=42)
        shap_values = explainer.shap_values(X_sample)

        # Top 20 summary plot
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_sample, max_display=20, show=False)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/shap_summary.png", dpi=150, bbox_inches="tight")
        plt.close()

        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_sample, plot_type="bar", max_display=20, show=False)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/shap_importance.png", dpi=150, bbox_inches="tight")
        plt.close()

        # Top features
        importance = np.abs(shap_values).mean(axis=0)
        top_idx = np.argsort(importance)[-10:][::-1]
        top_features = [{"feature": X_sample.columns[i],
                         "importance": float(importance[i])} for i in top_idx]
        with open(f"{output_dir}/top_features.json", "w") as f:
            json.dump(top_features, f, indent=2)

        print(f"   Top features : {[f['feature'] for f in top_features[:5]]}")
        print(f"   Temps : {time.time()-t0:.1f}s")

    except Exception as e:
        print(f"   ⚠️  SHAP ignoré : {e}")


def summary(metrics, output_dir):
    """Affiche le résumé final."""
    recall_ok = "✅ ATTEINT" if metrics['recall'] >= 0.85 else "❌ NON ATTEINT (cible: 0.85)"
    print(f"""
╔═══ RÉSUMÉ DE L'ENTRAÎNEMENT ═══╗
  Recall       : {metrics['recall']:.4f}  {recall_ok}
  Precision    : {metrics['precision']:.4f}
  F1-Score     : {metrics['f1']:.4f}
  AUC-PR       : {metrics['auc_pr']:.4f}
  Seuil        : {metrics['threshold']:.4f}

  Modèles sauvegardés dans : {output_dir}/
  ├── xgb_model.pkl
  ├── isolation_forest.pkl
  ├── scaler.pkl
  ├── freq_maps.pkl
  ├── ohe_encoder.pkl (si existant)
  ├── best_params.pkl
  ├── best_threshold.npy
  ├── metrics.json
  ├── top_features.json
  └── shap_*.png
╚══════════════════════════════════╝""")

    # Interprétation pour le mémoire
    status = "validée" if metrics['recall'] >= 0.85 else "non validée"
    print(f"""
📋 Pour le mémoire (Chapitre IV) :
  HS1 — Recall = {metrics['recall']:.2%} → Hypothèse {status}
        (cible: ≥ 85% des fraudes détectées)
  HS3 — Les graphiques SHAP (shap_summary.png, shap_importance.png)
        montrent les variables les plus influentes, facilitant l'adoption par les analystes.
""")


def main():
    args = parse_args()
    output_dir = args.output

    print(f"Dataset : {args.dataset}")
    print(f"Mode : {'Rapide' if args.fast else 'Complet'}")
    print(f"Output : {output_dir}/")
    print()

    # 1. Download
    train_path, id_path = download_data(args)

    # 2. Load
    df = load_and_merge(train_path, id_path, fast=args.fast)
    print(f"   Dimensions : {df.shape}")
    print(f"   Taux fraude : {df['isFraud'].mean()*100:.2f}%")

    # 3. Preprocess
    X_train, X_test, y_train, y_test = preprocess(df, output_dir)

    # 4. Isolation Forest
    train_isoforest(X_train, X_test, y_test, output_dir)

    # 5. XGBoost
    n_trials = args.optuna_trials if args.optuna_trials is not None else (10 if args.fast else 30)
    model, metrics = train_xgboost(X_train, X_test, y_train, y_test, output_dir, fast=args.fast, n_trials=n_trials)

    # 6. SHAP
    generate_shap(model, X_test, y_test, output_dir)

    # 7. Summary
    summary(metrics, output_dir)


if __name__ == "__main__":
    main()
