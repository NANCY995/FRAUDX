#!/usr/bin/env python3
"""
retrain.py — Réentraînement automatique du modèle XGBoost
À exécuter périodiquement (cron, scheduler) ou après N nouveaux feedbacks.

Usage:
    python retrain.py --min-samples 1000
"""
import argparse
import pandas as pd
import numpy as np
import joblib
import json
import warnings
import sys
from pathlib import Path
from datetime import datetime

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, recall_score, precision_score, average_precision_score
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

from fraudx.db import get_labeled_data, save_model_metrics
from fraudx.config import config as fraudx_config


def parse_args():
    parser = argparse.ArgumentParser(description="Réentraînement du modèle XGBoost")
    parser.add_argument("--min-samples", type=int, default=500,
                        help="Nombre minimum d'échantillons labellisés pour lancer le retrain")
    parser.add_argument("--output", type=str,
                        default=f"{fraudx_config.MODELS_PATH}{fraudx_config.MODEL_NAME}",
                        help="Chemin de sortie du modèle")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simule sans sauvegarder")
    return parser.parse_args()


def retrain(min_samples: int = 500, output_path: str = None,
            dry_run: bool = False) -> dict:
    if output_path is None:
        output_path = f"{fraudx_config.MODELS_PATH}{fraudx_config.MODEL_NAME}"
    models_dir = str(Path(output_path).parent)
    print(f"[{datetime.now().isoformat()}] === RETRAIN XGBoost ===")

    # 1. Charger les données labellisées
    df = get_labeled_data()
    if df is None or len(df) < min_samples:
        print(f"❌ Pas assez de données : {len(df) if df is not None else 0} < {min_samples}")
        return {"status": "skipped", "reason": f"insufficient data ({len(df) if df is not None else 0})"}

    print(f"✅ Données chargées : {len(df)} transactions labellisées")
    print(f"   Taux de fraude : {df['label'].mean() * 100:.2f}%")

    # 2. Préparer X, y
    from fraudx.preprocessing import FraudPreprocessor, FeatureEngineer
    preprocessor = FraudPreprocessor()
    preprocessor.load_artifacts()

    # Feature engineering
    X = df.drop(columns=["id", "transaction_id", "timestamp", "raw_input",
                         "created_at", "label", "feedback_fraud", "analyst",
                         "prediction", "risk_level", "fraud_score"], errors="ignore")
    X = FeatureEngineer.add_temporal_features(X)
    X = FeatureEngineer.add_amount_features(X)
    X = FeatureEngineer.add_behavioral_features(X)
    X = FeatureEngineer.add_velocity_features(X)
    X = FeatureEngineer.add_email_features(X)
    y = df["label"].values

    # Prétraitement
    X_processed = preprocessor.transform(X)

    # 3. Split + SMOTE
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, stratify=y, random_state=42
    )

    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"✅ SMOTE appliqué : {len(X_res)} échantillons")

    # 4. Entraînement avec les meilleurs paramètres connus
    best_params_file = Path(models_dir) / "best_params.pkl"
    best_params = joblib.load(best_params_file) if best_params_file.exists() else {
        "n_estimators": 300, "max_depth": 8, "learning_rate": 0.05,
        "subsample": 0.8, "colsample_bytree": 0.8, "gamma": 0.1,
        "reg_alpha": 0.1, "reg_lambda": 1.0, "scale_pos_weight": 10,
        "random_state": 42, "eval_metric": "logloss"
    }

    model = XGBClassifier(**best_params)
    model.fit(X_res, y_res)

    # 5. Évaluation
    y_pred = model.predict(X_test)
    y_probs = model.predict_proba(X_test)[:, 1]

    metrics = {
        "f1": float(f1_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "auc_pr": float(average_precision_score(y_test, y_probs))
    }

    print(f"📊 Métriques : F1={metrics['f1']:.4f}, Recall={metrics['recall']:.4f}, "
          f"Precision={metrics['precision']:.4f}, AUC-PR={metrics['auc_pr']:.4f}")

    # 6. Comparer avec le meilleur modèle existant
    best_existing = None
    try:
        best_existing = joblib.load(output_path) if Path(output_path).exists() else None
        if best_existing:
            old_probs = best_existing.predict_proba(X_test)[:, 1]
            old_recall = recall_score(y_test, best_existing.predict(X_test))
            old_f1 = f1_score(y_test, best_existing.predict(X_test))
            print(f"   Ancien Recall : {old_recall:.4f} → Nouveau Recall : {metrics['recall']:.4f}")
        else:
            old_f1 = 0.0
    except Exception:
        old_f1 = 0.0

    if metrics["recall"] > old_recall or old_f1 == 0.0:
        if not dry_run:
            # Sauvegarder
            Path(models_dir).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, output_path)
            with open(Path(models_dir) / "best_params.pkl", "wb") as f:
                joblib.dump(best_params, f)

            # Ajuster le seuil optimal (target recall >= 0.85)
            from sklearn.metrics import precision_recall_curve
            precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
            best_threshold = 0.5
            best_precision_at_target = 0.0
            for i in range(len(thresholds)):
                if recalls[i] >= 0.85 and precisions[i] >= best_precision_at_target:
                    best_precision_at_target = precisions[i]
                    best_threshold = thresholds[i]
            if best_precision_at_target == 0.0:
                best_idx = recalls.argmax()
                best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
            np.save(Path(models_dir) / "best_threshold.npy", best_threshold)

            # Enregistrer dans la DB
            save_model_metrics(
                model_name=f"xgb_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                model_path=output_path,
                f1=metrics["f1"], recall=metrics["recall"],
                precision=metrics["precision"], auc_pr=metrics["auc_pr"],
                params=best_params
            )
            print(f"✅ Modèle sauvegardé : {output_path} (seuil={best_threshold:.4f})")
        else:
            print("🔍 Dry-run : modèle NON sauvegardé")

        return {"status": "trained", "metrics": metrics}
    else:
        print(f"ℹ️  Aucune amélioration : ancien Recall={old_recall:.4f} >= nouveau={metrics['recall']:.4f}")
        return {"status": "skipped", "reason": "no improvement"}


if __name__ == "__main__":
    args = parse_args()
    result = retrain(min_samples=args.min_samples, output_path=args.output, dry_run=args.dry_run)
    print(f"\nRésultat : {json.dumps(result, indent=2)}")
