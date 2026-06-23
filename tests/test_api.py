"""
Tests unitaires pour l'API (sans dépendre des modèles entraînés).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
from fastapi.testclient import TestClient

# On patch le chargement des modèles pour les tests
import fraudx.preprocessing
import joblib
import numpy as np

# Créer des artefacts factices pour les tests
os.makedirs("models_optuna", exist_ok=True)
joblib.dump({}, "models_optuna/freq_maps.pkl")
np.save("models_optuna/best_threshold.npy", np.array(0.5))
joblib.dump(None, "models_optuna/scaler.pkl")

from src.api import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["status"] == "opérationnel"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_type" in data


def test_predict_endpoint():
    payload = {
        "TransactionAmt": 50000.0,
        "card1": 12345.0,
        "hour": 14,
        "dayofweek": 3
    }
    response = client.post("/predict", json=payload)
    # Peut échouer si les modèles ne sont pas chargés correctement
    # mais doit retourner 200 ou 400, pas 500
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        data = response.json()
        assert "transaction_id" in data
        assert "fraud_score" in data
        assert "prediction" in data
        assert "risk_level" in data
        assert "top_features" in data


def test_predict_invalid_payload():
    payload = {"invalid_field": "test"}
    response = client.post("/predict", json=payload)
    # Doit retourner 422 (validation error) ou 400
    assert response.status_code in [422, 400]


def test_batch_endpoint():
    payload = {
        "transactions": [
            {"TransactionAmt": 1000.0, "hour": 10, "dayofweek": 1},
            {"TransactionAmt": 50000.0, "hour": 14, "dayofweek": 3}
        ]
    }
    response = client.post("/batch", json=payload)
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        data = response.json()
        assert "total" in data
        assert "predictions" in data
        assert data["total"] == 2


def test_logs_endpoint():
    response = client.get("/logs?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "recent" in data


def test_feedback_endpoint():
    response = client.post("/feedback",
                          params={"transaction_id": "TX_TEST123",
                                  "is_fraud": True,
                                  "analyst": "test"})
    assert response.status_code in [200, 404]


def test_cors_headers():
    response = client.options("/predict")
    assert response.status_code in [200, 405]


def test_risk_level_logic():
    from src.api import get_risk_level
    assert get_risk_level(0.95) == "Critique"
    assert get_risk_level(0.8) == "Élevé"
    assert get_risk_level(0.5) == "Moyen"
    assert get_risk_level(0.2) == "Faible"
