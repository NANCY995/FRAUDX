import os
import pandas as pd
import numpy as np
import joblib
import shap
import uuid
import datetime
import logging
import time
import hashlib
import hmac
import base64
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import asyncio

from fraudx.preprocessing import FraudPreprocessor, FeatureEngineer
from fraudx.config import config as fraudx_config
from fraudx.security import (
    sanitize_html, validate_transaction_amount,
    hash_tx_value, RateLimiter, validate_string_length
)

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("fraudx")

security = HTTPBearer(auto_error=False)
rate_limiter = RateLimiter(max_requests=int(os.getenv("API_RATE_LIMIT", "100")), window_seconds=60)

preprocessor = FraudPreprocessor(models_path=fraudx_config.MODELS_PATH)
preprocessor.load_artifacts()

model_path = Path(fraudx_config.MODELS_PATH) / fraudx_config.MODEL_NAME
model = joblib.load(model_path)
logger.info(f"Modele charge : {model_path}")
explainer = shap.TreeExplainer(model)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "https://fraudx-memoirel3.streamlit.app,http://localhost:8501,http://localhost:8000"
).split(",")

JWT_SECRET = os.getenv("JWT_SECRET", "fraudx-dev-secret-change-in-prod")
JWT_ALGO = "HS256"
JWT_EXPIRY_HOURS = 24

ROLES = ["analyste", "superviseur", "administrateur"]

USERS = {
    "analyste1": {"password": "fraudx2025", "role": "analyste", "nom": "Analyste Test"},
    "superviseur1": {"password": "fraudx2025", "role": "superviseur", "nom": "Superviseur Test"},
    "admin1": {"password": "fraudx2025", "role": "administrateur", "nom": "Admin Test"},
}

ENDPOINT_ROLES = {
    "/predict": ["analyste", "superviseur", "administrateur"],
    "/predict/togo": ["analyste", "superviseur", "administrateur"],
    "/batch": ["analyste", "superviseur", "administrateur"],
    "/explain": ["analyste", "superviseur", "administrateur"],
    "/feedback": ["analyste", "superviseur", "administrateur"],
    "/logs": ["superviseur", "administrateur"],
    "/users": ["administrateur"],
    "/health": ["analyste", "superviseur", "administrateur"],
}


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def create_jwt(username: str, role: str) -> str:
    header = _b64url(json.dumps({"alg": JWT_ALGO, "typ": "JWT"}).encode())
    now = int(time.time())
    payload = _b64url(json.dumps({
        "sub": username, "role": role, "iat": now, "exp": now + JWT_EXPIRY_HOURS * 3600
    }).encode())
    sig = _b64url(hmac.new(JWT_SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"


def decode_jwt(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Bad token format")
        expected_sig = _b64url(hmac.new(JWT_SECRET.encode(), f"{parts[0]}.{parts[1]}".encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(parts[2], expected_sig):
            raise ValueError("Invalid signature")
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
        if payload.get("exp", 0) < time.time():
            raise ValueError("Token expired")
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token invalide: {str(e)}")


app = FastAPI(
    title="FRAUDX - Detection de fraude bancaire",
    description="API temps reel avec explicabilite SHAP et RBAC",
    version="3.0.0",
    contact={"name": "Johnson Nancy", "organization": "Elna Comply"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.post("/auth/login", tags=["Authentication"])
def login(username: str, password: str):
    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_jwt(username, user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRY_HOURS * 3600,
        "username": username,
        "role": user["role"],
        "nom": user["nom"]
    }


def verify_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    if not credentials:
        raise HTTPException(status_code=401, detail="Token requis")
    payload = decode_jwt(credentials.credentials)
    return payload


def require_role(required_roles: List[str]):
    def role_checker(payload: dict = Depends(verify_auth)):
        if payload.get("role") not in required_roles:
            raise HTTPException(status_code=403, detail="Role insuffisant")
        return payload
    return role_checker


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = rate_limiter.is_allowed(client_ip)
    if not allowed:
        return Response(status_code=429, headers={"Retry-After": str(retry_after)})
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    if response.status_code < 500:
        logger.info(f"{request.method} {request.url.path} | {response.status_code} | {duration:.0f}ms")
    return response


class Transaction(BaseModel):
    TransactionAmt: float = Field(..., gt=0, le=1_000_000_000)
    TransactionDT: Optional[float] = Field(None, ge=0)
    card1: Optional[float] = None
    card2: Optional[float] = None
    card3: Optional[float] = None
    card4: Optional[str] = None
    card5: Optional[float] = None
    card6: Optional[str] = None
    addr1: Optional[float] = None
    addr2: Optional[float] = None
    dist1: Optional[float] = None
    dist2: Optional[float] = None
    ProductCD: Optional[str] = None
    P_emaildomain: Optional[str] = None
    R_emaildomain: Optional[str] = None
    hour: Optional[int] = Field(None, ge=0, le=23)
    dayofweek: Optional[int] = Field(None, ge=0, le=6)
    canal: Optional[str] = None
    operateur: Optional[str] = None
    ville: Optional[str] = None
    type_operation: Optional[str] = None
    device_change_days: Optional[float] = None
    tx_last_30min: Optional[float] = None


class BatchRequest(BaseModel):
    transactions: List[Transaction]


class BatchResponse(BaseModel):
    predictions: List[dict]
    total: int
    fraud_count: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_type: str
    version: str


prediction_log: List[dict] = []


def get_risk_level(score: float) -> str:
    if score >= 0.9: return "Critique"
    elif score >= 0.7: return "Eleve"
    elif score >= 0.4: return "Moyen"
    return "Faible"


def process_transaction(tx: dict) -> dict:
    df = FeatureEngineer.add_temporal_features(pd.DataFrame([tx]))
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)
    df = FeatureEngineer.add_velocity_features(df)
    df = FeatureEngineer.add_email_features(df)
    df = FeatureEngineer.add_ussd_features(df)

    for col in df.select_dtypes(include=["object"]).columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    X = preprocessor.transform(df)
    expected = model.get_booster().feature_names
    for col in expected:
        if col not in X.columns:
            X[col] = 0.0
    X = X[expected]

    proba = float(model.predict_proba(X)[0, 1])
    threshold = preprocessor.best_threshold
    prediction = "FRAUDE" if proba >= threshold else "NORMALE"

    shap_values = explainer.shap_values(X)
    importance = np.abs(shap_values[0])
    top_idx = np.argsort(importance)[-5:][::-1]

    top_features = []
    for i in top_idx:
        col = X.columns[i]
        top_features.append({
            "feature": col,
            "value": float(X.iloc[0, i]) if not isinstance(X.iloc[0, i], (str, bytes)) else str(X.iloc[0, i]),
            "shap_value": float(shap_values[0, i]),
            "impact": "positif (fraude)" if shap_values[0, i] > 0 else "negatif (normale)"
        })

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


@app.get("/", tags=["Status"])
def root():
    return {"service": "FRAUDX", "version": "3.0.0", "docs": "/docs", "status": "operationnel"}


@app.get("/health", tags=["Status"])
def health():
    return HealthResponse(status="healthy", model_loaded=True, model_type=type(model).__name__, version="3.0.0")


@app.post("/predict", tags=["Prediction"])
def predict(transaction: Transaction, payload: dict = Depends(require_role(["analyste", "superviseur", "administrateur"]))):
    try:
        result = process_transaction(transaction.dict())
        result["analyse_par"] = payload.get("sub", "unknown")
        result["role"] = payload.get("role", "unknown")
        prediction_log.append(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prediction : {str(e)}")


@app.post("/batch", response_model=BatchResponse, tags=["Prediction"])
def batch_predict(batch: BatchRequest, payload: dict = Depends(require_role(["analyste", "superviseur", "administrateur"]))):
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
    return BatchResponse(predictions=results, total=len(results), fraud_count=fraud_count)


@app.post("/explain", tags=["Explicabilite"])
def explain(transaction: Transaction, payload: dict = Depends(require_role(["analyste", "superviseur", "administrateur"]))):
    try:
        df = FeatureEngineer.add_temporal_features(pd.DataFrame([transaction.dict()]))
        df = FeatureEngineer.add_amount_features(df)
        df = FeatureEngineer.add_behavioral_features(df)
        df = FeatureEngineer.add_velocity_features(df)
        df = FeatureEngineer.add_email_features(df)
        df = FeatureEngineer.add_ussd_features(df)

        for col in df.select_dtypes(include=["object"]).columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="ignore")
            except Exception:
                pass

        X = preprocessor.transform(df)
        expected = model.get_booster().feature_names
        for col in expected:
            if col not in X.columns:
                X[col] = 0.0
        X = X[expected]

        shap_values = explainer.shap_values(X)
        importance = np.abs(shap_values[0])
        all_idx = np.argsort(importance)[::-1]

        all_features = []
        for i in all_idx:
            col = X.columns[i]
            all_features.append({
                "feature": col,
                "value": float(X.iloc[0, i]) if not isinstance(X.iloc[0, i], (str, bytes)) else str(X.iloc[0, i]),
                "shap_value": float(shap_values[0, i]),
                "abs_importance": float(importance[i]),
                "impact": "positif (fraude)" if shap_values[0, i] > 0 else "negatif (normale)"
            })

        proba = float(model.predict_proba(X)[0, 1])
        threshold = preprocessor.best_threshold
        prediction = "FRAUDE" if proba >= threshold else "NORMALE"

        return {
            "prediction": prediction,
            "fraud_score": proba,
            "threshold": float(threshold),
            "top_5": all_features[:5],
            "all_features_sorted": all_features,
            "total_features": len(all_features),
            "analyse_par": payload.get("sub", "unknown"),
            "role": payload.get("role", "unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur d'explicabilite : {str(e)}")


@app.get("/logs", tags=["Monitoring"])
def get_logs(limit: int = 50, payload: dict = Depends(require_role(["superviseur", "administrateur"]))):
    safe_limit = min(max(limit, 1), 1000)
    return {"total": len(prediction_log), "recent": prediction_log[-safe_limit:]}


@app.post("/feedback", tags=["Monitoring"])
def submit_feedback(transaction_id: str, is_fraud: bool, analyst: str = "anonymous",
                    payload: dict = Depends(require_role(["analyste", "superviseur", "administrateur"]))):
    safe_analyst = validate_string_length(analyst, 100)
    for entry in reversed(prediction_log):
        if entry.get("transaction_id") == transaction_id:
            entry["feedback"] = {
                "is_fraud": is_fraud,
                "analyst": safe_analyst,
                "timestamp": datetime.datetime.now().isoformat()
            }
            return {"status": "ok", "message": "Feedback enregistre"}
    raise HTTPException(status_code=404, detail="Transaction non trouvee")


@app.get("/users", tags=["Administration"])
def list_users(payload: dict = Depends(require_role(["administrateur"]))):
    return {
        "users": [
            {"username": k, "role": v["role"], "nom": v["nom"]}
            for k, v in USERS.items()
        ]
    }


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    allowed, _ = rate_limiter.is_allowed(websocket.client.host if websocket.client else "ws_unknown")
    if not allowed:
        await websocket.close(code=1008)
        return
    await websocket.send_json({"status": "connected", "message": "FRAUDX streaming actif"})
    try:
        while True:
            data = await websocket.receive_json()
            if "TransactionAmt" not in data:
                await websocket.send_json({"error": "Champ TransactionAmt requis"})
                continue
            result = process_transaction(data)
            prediction_log.append(result)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


class TogoTransaction(BaseModel):
    montant_cfa: float = Field(..., gt=0, le=10_000_000)
    canal: str = Field(..., pattern=r"^(USSD|APP|AGENT|WEB)$")
    operateur: str = Field(..., pattern=r"^(TogoCom Cash|Moov Money|Flooz)$")
    ville: str = Field(..., max_length=100)
    type_operation: str = Field(..., pattern=r"^(RECHARGE|TRANSFERT|PAIEMENT|RETRAIT)$")
    device_change_days: float = Field(0, ge=0)
    tx_last_30min: float = Field(0, ge=0)
    hour: Optional[int] = Field(None, ge=0, le=23)
    dayofweek: Optional[int] = Field(None, ge=0, le=6)


CANAL_TO_PRODUCTCD = {"USSD": "W", "APP": "H", "AGENT": "C", "WEB": "S"}
OPERATEUR_TO_CARD4 = {"TogoCom Cash": "visa", "Moov Money": "mastercard", "Flooz": "discover"}


@app.post("/predict/togo", tags=["Togo Mobile Money"])
def predict_togo(tx: TogoTransaction, payload: dict = Depends(require_role(["analyste", "superviseur", "administrateur"]))):
    mapped = {
        "TransactionAmt": tx.montant_cfa,
        "TransactionDT": None,
        "card1": hash_tx_value(f"{tx.operateur}{tx.ville}"),
        "card4": OPERATEUR_TO_CARD4.get(tx.operateur, "visa"),
        "ProductCD": CANAL_TO_PRODUCTCD.get(tx.canal, "W"),
        "addr1": hash_tx_value(tx.ville),
        "D1": tx.device_change_days,
        "C1": tx.tx_last_30min,
        "hour": tx.hour if tx.hour is not None else 12,
        "dayofweek": tx.dayofweek if tx.dayofweek is not None else 3,
        "canal": tx.canal,
        "operateur": tx.operateur,
        "ville": tx.ville,
        "type_operation": tx.type_operation,
        "device_change_days": tx.device_change_days,
        "tx_last_30min": tx.tx_last_30min
    }
    transaction = Transaction(**mapped)
    result = predict(transaction)

    ussd_risk = []
    if tx.canal == "USSD" and tx.device_change_days <= 1 and tx.montant_cfa > 30000:
        ussd_risk.append("SIM SWAP suspect (canal USSD + changement appareil recent + montant eleve)")
    if tx.tx_last_30min >= 3:
        ussd_risk.append("CASCADE de transferts (3+ transactions en 30 min)")
    if tx.canal == "AGENT" and tx.montant_cfa % 10000 == 0 and tx.montant_cfa > 100000:
        ussd_risk.append("AGENT frauduleux suspect (montant ronde eleve)")
    if tx.canal == "USSD" and tx.hour and tx.hour >= 0 and tx.hour <= 5 and tx.montant_cfa > 50000:
        ussd_risk.append("TRANSACTION INHABITUELLE (heure creuse + montant eleve)")

    if ussd_risk:
        result["ussd_risk_factors"] = ussd_risk
    result["canal"] = tx.canal
    result["operateur"] = tx.operateur
    result["montant_fcfa"] = tx.montant_cfa
    return result


def main():
    port = int(os.environ.get("API_PORT", 8000))
    host = os.environ.get("API_HOST", "0.0.0.0")
    log_level = os.environ.get("LOG_LEVEL", "info").lower()
    logger.info(f"FRAUDX API demarree sur {host}:{port}")
    uvicorn.run("src.api:app", host=host, port=port, reload=False, log_level=log_level)


if __name__ == "__main__":
    main()
