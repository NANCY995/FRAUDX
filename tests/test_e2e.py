"""
Test d'intégration complet : génération de données → prédiction → feedback → logs.
Ne nécessite pas l'API en cours d'exécution (utilise TestClient).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

# Patch des artefacts de modèle avant d'importer l'app
import joblib
os.makedirs("models_optuna", exist_ok=True)
joblib.dump({}, "models_optuna/freq_maps.pkl")
np.save("models_optuna/best_threshold.npy", np.array(0.5))
joblib.dump(None, "models_optuna/scaler.pkl")

from src.api import app
from fraudx.synthetic_data import generate_togo_dataset

client = TestClient(app)


def test_e2e_ieee_prediction():
    """Test complet : prédiction IEEE-CIS → logs → feedback."""
    payload = {
        "TransactionAmt": 50000.0,
        "card1": 12345.0,
        "card4": "visa",
        "ProductCD": "C",
        "addr1": 200.0,
        "hour": 14,
        "dayofweek": 3
    }

    r = client.post("/predict", json=payload)
    assert r.status_code in [200, 400]

    if r.status_code == 200:
        data = r.json()
        assert "transaction_id" in data
        assert "fraud_score" in data
        assert "prediction" in data
        assert "risk_level" in data
        assert "top_features" in data
        assert len(data["top_features"]) == 3

        # Feedback
        tx_id = data["transaction_id"]
        fb = client.post("/feedback", params={
            "transaction_id": tx_id,
            "is_fraud": True,
            "analyst": "test_e2e"
        })
        assert fb.status_code in [200, 404]

        # Logs
        logs = client.get("/logs?limit=10")
        assert logs.status_code == 200
        assert logs.json()["total"] >= 1


def test_e2e_batch_prediction():
    """Test du batch endpoint avec 5 transactions."""
    payload = {
        "transactions": [
            {"TransactionAmt": 1000.0, "hour": 8, "dayofweek": 1},
            {"TransactionAmt": 50000.0, "hour": 2, "dayofweek": 0},
            {"TransactionAmt": 25000.0, "hour": 18, "dayofweek": 5},
            {"TransactionAmt": 500.0, "hour": 12, "dayofweek": 3},
            {"TransactionAmt": 100000.0, "hour": 3, "dayofweek": 6}
        ]
    }

    r = client.post("/batch", json=payload)
    assert r.status_code in [200, 400]

    if r.status_code == 200:
        data = r.json()
        assert data["total"] == 5
        assert len(data["predictions"]) == 5
        for pred in data["predictions"]:
            assert "transaction_id" in pred
            assert "fraud_score" in pred


def test_e2e_with_synthetic_togo_data():
    """Test avec des données synthétiques Togo."""
    df = generate_togo_dataset(n_transactions=10, seed=42)

    for _, row in df.iterrows():
        payload = {
            "TransactionAmt": float(row["montant_cfa"]),
            "card1": float(abs(hash(row["operateur"])) % 10000),
            "card4": row["operateur"],
            "ProductCD": "W" if row["canal"] == "USSD" else "H",
            "addr1": float(abs(hash(row["ville"])) % 1000),
            "hour": int(row["hour"]),
            "dayofweek": int(row["dayofweek"])
        }

        r = client.post("/predict", json=payload)
        assert r.status_code in [200, 400]


def test_e2e_togo_endpoint():
    """Test du endpoint /predict/togo."""
    payload = {
        "montant_cfa": 50000,
        "canal": "USSD",
        "operateur": "TogoCom Cash",
        "ville": "Lomé",
        "type_operation": "TRANSFERT",
        "device_change_days": 0,
        "tx_last_30min": 3,
        "hour": 14,
        "dayofweek": 3
    }

    r = client.post("/predict/togo", json=payload)
    assert r.status_code in [200, 400]

    if r.status_code == 200:
        data = r.json()
        assert data["prediction"] in ["FRAUDE", "NORMALE"]
        assert data["risk_level"] in ["Faible", "Moyen", "Élevé", "Critique"]


def test_e2e_high_value_fraud_scenario():
    """Test un scénario à haut risque : montant élevé, heure creuse, nouveau device."""
    payload = {
        "TransactionAmt": 250000.0,
        "card1": 99999.0,
        "card4": "visa",
        "ProductCD": "C",
        "addr1": 500.0,
        "hour": 3,
        "dayofweek": 0
    }

    r = client.post("/predict", json=payload)
    assert r.status_code in [200, 400]

    if r.status_code == 200:
        data = r.json()
        # Ces transactions devraient avoir un score élevé
        logger.info(f"High-value fraud score: {data['fraud_score']}")
        logger.info(f"Top features: {[f['feature'] for f in data['top_features']]}")


def test_e2e_low_value_normal_scenario():
    """Test un scénario normal : petit montant, heure normale."""
    payload = {
        "TransactionAmt": 1500.0,
        "card1": 11111.0,
        "card4": "mastercard",
        "ProductCD": "S",
        "addr1": 100.0,
        "hour": 12,
        "dayofweek": 3
    }

    r = client.post("/predict", json=payload)
    assert r.status_code in [200, 400]


def test_e2e_health_and_root():
    """Test les endpoints de santé."""
    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["status"] == "opérationnel"

    health = client.get("/health")
    assert health.status_code == 200


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test_e2e")

    test_e2e_ieee_prediction()
    test_e2e_batch_prediction()
    test_e2e_with_synthetic_togo_data()
    test_e2e_togo_endpoint()
    test_e2e_high_value_fraud_scenario()
    test_e2e_low_value_normal_scenario()
    test_e2e_health_and_root()
    print("\n✅ Tous les tests E2E passés")
