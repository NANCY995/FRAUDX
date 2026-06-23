import os
import pandas as pd
import numpy as np
import joblib
import shap
import uuid
import datetime
import logging
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import asyncio

from fraudx.preprocessing import FraudPreprocessor, FeatureEngineer
from fraudx.config import config as fraudx_config

# === Logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("fraudx")

# === Initialisation ===
security = HTTPBearer()
preprocessor = FraudPreprocessor(models_path=fraudx_config.MODELS_PATH)
preprocessor.load_artifacts()

model_path = Path(fraudx_config.MODELS_PATH) / fraudx_config.MODEL_NAME
model = joblib.load(model_path)
logger.info(f"Modèle chargé : {model_path}")
explainer = shap.TreeExplainer(model)

# === Application ===
app = FastAPI(
    title="FRAUDX - Détection de fraude bancaire",
    description="API temps réel avec explicabilité SHAP — Contexte Togo (mobile money + transactions bancaires)",
    version="2.0.0",
    contact={"name": "Johnson Nancy", "organization": "Elna Comply"}
)

# === Middleware ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} | {response.status_code} | {duration:.0f}ms")
    return response


# === Schémas ===
class Transaction(BaseModel):
    TransactionAmt: float = Field(..., description="Montant de la transaction")
    TransactionDT: Optional[float] = Field(None, description="Timestamp (secondes depuis 2017-12-01)")
    card1: Optional[float] = Field(None, description="Identifiant carte/device")
    card2: Optional[float] = None
    card3: Optional[float] = None
    card4: Optional[str] = Field(None, description="Type de carte ou opérateur mobile money")
    card5: Optional[float] = None
    card6: Optional[str] = None
    addr1: Optional[float] = Field(None, description="Ville/localisation (Togo)")
    addr2: Optional[float] = None
    dist1: Optional[float] = None
    dist2: Optional[float] = None
    ProductCD: Optional[str] = Field(None, description="Type de produit/canal (W, H, C, USSD, APP, AGENT)")
    P_emaildomain: Optional[str] = None
    R_emaildomain: Optional[str] = None
    hour: Optional[int] = Field(None, ge=0, le=23)
    dayofweek: Optional[int] = Field(None, ge=0, le=6)
    # Champs mobile money Togo
    canal: Optional[str] = Field(None, description="Canal mobile money (USSD, APP, AGENT, WEB)")
    operateur: Optional[str] = Field(None, description="Opérateur (TogoCom Cash, Moov Money, Flooz)")
    ville: Optional[str] = Field(None, description="Ville de la transaction au Togo")
    type_operation: Optional[str] = Field(None, description="Type (RECHARGE, TRANSFERT, PAIEMENT, RETRAIT)")
    device_change_days: Optional[float] = Field(None, description="Jours depuis dernier changement de SIM/appareil")
    tx_last_30min: Optional[float] = Field(None, description="Nombre de transactions dans les 30 dernières minutes")


class BatchRequest(BaseModel):
    transactions: List[Transaction]


class FeatureImpact(BaseModel):
    feature: str
    value: float
    shap_value: float
    impact: str


class PredictionResponse(BaseModel):
    transaction_id: str
    timestamp: str
    fraud_score: float
    prediction: str
    risk_level: str
    top_features: List[FeatureImpact]


class BatchResponse(BaseModel):
    predictions: List[PredictionResponse]
    total: int
    fraud_count: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_type: str
    version: str


# === Logs en mémoire (sera remplacé par SQLite) ===
prediction_log: List[dict] = []


# === Fonctions internes ===
def get_risk_level(score: float) -> str:
    if score >= 0.9: return "Critique"
    elif score >= 0.7: return "Élevé"
    elif score >= 0.4: return "Moyen"
    return "Faible"


def process_transaction(tx: dict) -> dict:
    # Feature engineering
    df = FeatureEngineer.add_temporal_features(pd.DataFrame([tx]))
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)
    df = FeatureEngineer.add_velocity_features(df)
    df = FeatureEngineer.add_email_features(df)

    # Convertir les types numériques pour éviter les erreres numpy
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    # Prétraitement
    X = preprocessor.transform(df)

    # Aligner les colonnes avec celles attendues par le modèle
    expected = model.get_booster().feature_names
    for col in expected:
        if col not in X.columns:
            X[col] = 0.0
    X = X[expected]

    # Prédiction
    proba = float(model.predict_proba(X)[0, 1])
    threshold = preprocessor.best_threshold
    prediction = "FRAUDE" if proba >= threshold else "NORMALE"

    # SHAP
    shap_values = explainer.shap_values(X)
    importance = np.abs(shap_values[0])
    top_idx = np.argsort(importance)[-3:][::-1]

    top_features = []
    for i in top_idx:
        col = X.columns[i]
        top_features.append(FeatureImpact(
            feature=col,
            value=float(X.iloc[0, i]) if not isinstance(X.iloc[0, i], (str, bytes)) else str(X.iloc[0, i]),
            shap_value=float(shap_values[0, i]),
            impact="positif (fraude)" if shap_values[0, i] > 0 else "négatif (normale)"
        ))

    tx_id = f"TX_{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now().isoformat()

    return {
        "transaction_id": tx_id,
        "timestamp": ts,
        "fraud_score": proba,
        "prediction": prediction,
        "risk_level": get_risk_level(proba),
        "top_features": top_features
    }


# === Endpoints ===
@app.get("/", tags=["Status"])
def root():
    return {
        "service": "FRAUDX",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "opérationnel"
    }


@app.get("/health", response_model=HealthResponse, tags=["Status"])
def health():
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_type=type(model).__name__,
        version="2.0.0"
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prédiction"])
def predict(transaction: Transaction):
    try:
        result = process_transaction(transaction.dict())
        prediction_log.append(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction : {str(e)}")


@app.post("/batch", response_model=BatchResponse, tags=["Prédiction"])
def batch_predict(batch: BatchRequest):
    results = []
    for tx in batch.transactions:
        try:
            result = process_transaction(tx.dict())
            results.append(result)
            prediction_log.append(result)
        except Exception as e:
            results.append({
                "transaction_id": "ERROR",
                "timestamp": datetime.datetime.now().isoformat(),
                "fraud_score": 0.0,
                "prediction": "ERREUR",
                "risk_level": "Inconnu",
                "top_features": [],
                "error": str(e)
            })
    fraud_count = sum(1 for r in results if r["prediction"] == "FRAUDE")
    return BatchResponse(
        predictions=results,
        total=len(results),
        fraud_count=fraud_count
    )


@app.get("/logs", tags=["Monitoring"])
def get_logs(limit: int = 50):
    return {"total": len(prediction_log), "recent": prediction_log[-limit:]}


@app.post("/feedback", tags=["Monitoring"])
def submit_feedback(transaction_id: str, is_fraud: bool, analyst: str = "anonymous"):
    for entry in reversed(prediction_log):
        if entry.get("transaction_id") == transaction_id:
            entry["feedback"] = {
                "is_fraud": is_fraud,
                "analyst": analyst,
                "timestamp": datetime.datetime.now().isoformat()
            }
            return {"status": "ok", "message": "Feedback enregistré"}
    raise HTTPException(status_code=404, detail="Transaction non trouvée")


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"status": "connected", "message": "FRAUDX streaming actif"})

    try:
        while True:
            data = await websocket.receive_json()
            result = process_transaction(data)
            prediction_log.append(result)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


class StreamConfig(BaseModel):
    continuous: bool = Field(False, description="Mode flux continu")
    delay_ms: int = Field(500, ge=100, le=10000, description="Délai entre chaque analyse en mode continu")


class TogoTransaction(BaseModel):
    montant_cfa: float = Field(..., description="Montant en FCFA")
    canal: str = Field(..., description="Canal (USSD, APP, AGENT, WEB)")
    operateur: str = Field(..., description="Opérateur (TogoCom Cash, Moov Money, Flooz)")
    ville: str = Field(..., description="Ville au Togo")
    type_operation: str = Field(..., description="Type (RECHARGE, TRANSFERT, PAIEMENT, RETRAIT)")
    device_change_days: float = Field(0, description="Jours depuis dernier changement SIM")
    tx_last_30min: float = Field(0, description="Transactions dans les 30 dernières minutes")
    hour: Optional[int] = Field(None, ge=0, le=23)
    dayofweek: Optional[int] = Field(None, ge=0, le=6)

    class Config:
        json_schema_extra = {
            "example": {
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
        }


CANAL_TO_PRODUCTCD = {"USSD": "W", "APP": "H", "AGENT": "C", "WEB": "S"}
OPERATEUR_TO_CARD4 = {"TogoCom Cash": "visa", "Moov Money": "mastercard", "Flooz": "discover"}


@app.post("/predict/togo", response_model=PredictionResponse, tags=["Togo Mobile Money"])
def predict_togo(tx: TogoTransaction):
    """
    Endpoint spécialisé pour les transactions mobile money au Togo.
    Mappe automatiquement les champs togolais vers le format du modèle.
    """
    mapped = {
        "TransactionAmt": tx.montant_cfa,
        "TransactionDT": None,
        "card1": abs(hash(tx.operateur + tx.ville)) % 10000,
        "card4": OPERATEUR_TO_CARD4.get(tx.operateur, "visa"),
        "ProductCD": CANAL_TO_PRODUCTCD.get(tx.canal, "W"),
        "addr1": abs(hash(tx.ville)) % 1000,
        "D1": tx.device_change_days,
        "C1": tx.tx_last_30min,
        "hour": tx.hour if tx.hour is not None else 12,
        "dayofweek": tx.dayofweek if tx.dayofweek is not None else 3
    }

    transaction = Transaction(**mapped)
    return predict(transaction)


@app.post("/predict/stream", tags=["Prédiction"])
def predict_stream(transaction: Transaction, config: StreamConfig = StreamConfig()):
    """
    Endpoint pour analyse unique avec configuration du mode streaming.
    Utilisé par le dashboard pour afficher les résultats en temps réel.
    """
    return predict(transaction)


def main():
    """Point d'entrée pour la CLI (setup.py console_scripts)."""
    port = int(os.environ.get("API_PORT", 8000))
    host = os.environ.get("API_HOST", "0.0.0.0")
    logger.info(f"🚀 FRAUDX API démarrée sur {host}:{port}")
    uvicorn.run("src.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
