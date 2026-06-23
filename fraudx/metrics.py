"""
Métriques d'évaluation personnalisées pour le mémoire FRAUDX.
Au-delà du F1 standard, ces métriques sont conçues pour :
- HS1 : mesurer la réduction des faux négatifs
- HS3 : quantifier l'utilité de l'explicabilité
- Contextualisation Togo : performance par canal mobile money
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (confusion_matrix, f1_score, recall_score,
                             precision_score, average_precision_score,
                             precision_recall_curve, roc_auc_score)
from typing import Dict, List, Optional, Tuple


class FraudMetrics:
    """
    Calculateur de métriques étendu pour la détection de fraude.
    Inclut des métriques spécifiques au contexte bancaire et mobile money.
    """

    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray,
                 y_proba: Optional[np.ndarray] = None):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.y_proba = np.array(y_proba) if y_proba is not None else None
        self._cm = None

    @property
    def cm(self) -> np.ndarray:
        if self._cm is None:
            self._cm = confusion_matrix(self.y_true, self.y_pred)
        return self._cm

    @property
    def tn(self) -> int:
        return int(self.cm[0, 0])

    @property
    def fp(self) -> int:
        return int(self.cm[0, 1])

    @property
    def fn(self) -> int:
        return int(self.cm[1, 0])

    @property
    def tp(self) -> int:
        return int(self.cm[1, 1])

    def standard(self) -> Dict[str, float]:
        """Métriques standards du mémoire."""
        return {
            "f1_score": float(f1_score(self.y_true, self.y_pred)),
            "recall": float(recall_score(self.y_true, self.y_pred)),
            "precision": float(precision_score(self.y_true, self.y_pred)),
            "auc_pr": float(average_precision_score(self.y_true, self.y_proba))
            if self.y_proba is not None else None,
            "auc_roc": float(roc_auc_score(self.y_true, self.y_proba))
            if self.y_proba is not None else None,
            "tn": self.tn,
            "fp": self.fp,
            "fn": self.fn,
            "tp": self.tp,
        }

    def hs1_metrics(self) -> Dict[str, float]:
        """
        Métriques spécifiques à HS1 (réduction des faux négatifs).
        - Taux de faux négatifs : FN / (TP + FN) = 1 - Recall
        - Taux de détection des fraudes : Recall
        - Coût estimé des FN (si montant moyen fourni)
        """
        total_fraudes = self.tp + self.fn
        fn_rate = self.fn / total_fraudes if total_fraudes > 0 else 0.0
        return {
            "hs1_false_negative_rate": float(fn_rate),
            "hs1_detection_rate": float(recall_score(self.y_true, self.y_pred)),
            "hs1_fn_count": self.fn,
            "hs1_tp_count": self.tp,
        }

    def hs3_interpretability_metrics(self, shap_importance: np.ndarray,
                                     top_k: int = 5) -> Dict:
        """
        Métriques pour HS3 : mesure l'utilité de l'explicabilité.
        - Concentration SHAP : quelle part de l'explication est portée par les top-k variables ?
        - Stabilité SHAP : variance des top features entre échantillons
        """
        if shap_importance is None or len(shap_importance) == 0:
            return {"hs3_shap_concentration": None, "hs3_top_features": []}

        # Concentration : proportion de l'importance totale portée par les top-k
        sorted_imp = np.sort(shap_importance)[::-1]
        top_k_sum = sorted_imp[:top_k].sum()
        total_sum = sorted_imp.sum()
        concentration = float(top_k_sum / total_sum) if total_sum > 0 else 0.0

        return {
            "hs3_shap_concentration": concentration,
            "hs3_top_k": top_k,
            "hs3_total_features": len(shap_importance),
        }

    def cost_analysis(self, amounts: np.ndarray,
                      cost_per_fp: float = 5000,
                      cost_per_fn: float = 50000) -> Dict[str, float]:
        """
        Analyse de coût simplifiée pour le mémoire (section 4.6.2).
        - Coût des faux positifs : temps analyste perdu
        - Coût des faux négatifs : pertes financières non détectées
        """
        fn_amounts = amounts[self.y_true == 1][self.y_pred[self.y_true == 1] == 0] if len(amounts) == len(self.y_true) else np.array([0])
        fp_cost = self.fp * cost_per_fp
        fn_cost = self.fn * cost_per_fn
        total_fraud_amount = float(amounts[self.y_true == 1].sum()) if len(amounts) == len(self.y_true) else 0.0

        return {
            "fp_cost_fcfa": float(fp_cost),
            "fn_cost_fcfa": float(fn_cost),
            "total_operational_cost": float(fp_cost + fn_cost),
            "total_fraud_amount_fcfa": total_fraud_amount,
            "saved_amount_estimate": float(total_fraud_amount * recall_score(self.y_true, self.y_pred)),
        }

    def segment_performance(self, df: pd.DataFrame,
                            segment_col: str) -> pd.DataFrame:
        """
        Performance segmentée par une variable (canal, tranche de montant, heure...).
        Utilisé dans le Chapitre IV pour l'analyse par canal mobile money.
        """
        results = []
        for segment in df[segment_col].unique():
            mask = df[segment_col] == segment
            y_true_s = self.y_true[mask.values] if hasattr(mask, 'values') else self.y_true[mask]
            y_pred_s = self.y_pred[mask.values] if hasattr(mask, 'values') else self.y_pred[mask]
            if len(y_true_s) == 0:
                continue
            results.append({
                "segment": segment,
                "count": int(len(y_true_s)),
                "fraud_count": int(y_true_s.sum()),
                "f1": float(f1_score(y_true_s, y_pred_s)),
                "recall": float(recall_score(y_true_s, y_pred_s)),
                "precision": float(precision_score(y_true_s, y_pred_s)),
            })
        return pd.DataFrame(results).sort_values("count", ascending=False)

    def threshold_analysis(self) -> Dict:
        """
        Analyse de l'impact du seuil de décision sur les métriques.
        Utile pour justifier le choix du seuil dans le mémoire.
        """
        if self.y_proba is None:
            return {}
        precisions, recalls, thresholds = precision_recall_curve(self.y_true, self.y_proba)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        best_idx = f1_scores.argmax()

        return {
            "optimal_threshold": float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5,
            "f1_at_optimal": float(f1_scores[best_idx]),
            "recall_at_optimal": float(recalls[best_idx]),
            "precision_at_optimal": float(precisions[best_idx]),
        }

    def summary(self, amounts: Optional[np.ndarray] = None) -> Dict:
        """Rapport complet pour le mémoire."""
        metrics = {}
        metrics.update(self.standard())
        metrics.update(self.hs1_metrics())
        metrics.update({"threshold_analysis": self.threshold_analysis()})
        if amounts is not None:
            metrics.update(self.cost_analysis(amounts))
        return metrics
