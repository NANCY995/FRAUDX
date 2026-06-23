# FRAUDX — Système complet de détection de fraude bancaire

> **Contexte :** Togo — transactions bancaires classiques + mobile money (TogoCom Cash, Moov Money/Flooz)
> **Architecture :** API REST + Dashboard Streamlit + Réentraînement automatique

---

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌────────────────┐
│  Client       │────>│  API FastAPI     │────>│  Préprocesseur │
│  (curl, app)  │     │  /predict        │     │  (fraudx/)     │
└──────────────┘     └──────┬───────────┘     └───────┬────────┘
                            │                         │
                    ┌───────▼───────────┐    ┌────────▼────────┐
                    │  SHAP Explainer   │    │  Modèle XGBoost │
                    └───────┬───────────┘    └────────┬────────┘
                            │                         │
                    ┌───────▼─────────────────────────▼────────┐
                    │           Réponse JSON                   │
                    │  fraud_score + top_features (SHAP)       │
                    └────────────────┬─────────────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │        Base SQLite              │
                    │  predictions + feedback + models │
                    └────────────────┬─────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │     Dashboard Streamlit          │
                    │  Alertes + SHAP + Monitoring     │
                    └────────────────┬─────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │        retrain.py                │
                    │  Réentraînement automatique      │
                    └──────────────────────────────────┘
```

---

## Installation

### Prérequis
- Python 3.10+
- Pip

### 1. Cloner et installer

```bash
git clone <repo-url> fraudx
cd fraudx
pip install -r config/requirements.txt
```

### 2. Entraîner les modèles (depuis Colab)

Exécuter dans l'ordre :
1. `01_EDA.ipynb` — Analyse exploratoire
2. `02_Pretraitement.ipynb` — Prétraitement (génère `models/`)
3. `04_XGBoost.ipynb` — Entraînement XGBoost (génère `xgb_model.pkl`)

### 3. Lancer l'API

```bash
uvicorn src.api:app --reload
```

Swagger UI : http://localhost:8000/docs

### 4. Lancer le dashboard

```bash
streamlit run app_streamlit.py
```

Dashboard : http://localhost:8501

### 5. Simuler un flux

```bash
python simulate_stream.py --transactions 100 --delay 0.3
```

---

## Docker

```bash
# Lancer API + Dashboard
docker-compose up api dashboard

# Lancer le réentraînement (une fois)
docker-compose run retrain
```

---

## Endpoints API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Statut du service |
| `GET` | `/health` | Santé du service |
| `POST` | `/predict` | Analyser une transaction |
| `POST` | `/batch` | Analyser plusieurs transactions |
| `GET` | `/logs` | Historique des prédictions |
| `POST` | `/feedback` | Envoyer un feedback analyste |

### Exemple `/predict`

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"TransactionAmt": 50000, "card1": 12345, "hour": 14, "dayofweek": 3}'
```

Réponse :
```json
{
  "transaction_id": "TX_ABC12345",
  "fraud_score": 0.873,
  "prediction": "FRAUDE",
  "risk_level": "Élevé",
  "top_features": [
    {"feature": "TransactionAmt", "shap_value": 0.45, "impact": "positif (fraude)"},
    {"feature": "V287", "shap_value": 0.32, "impact": "positif (fraude)"},
    {"feature": "D10", "shap_value": -0.21, "impact": "négatif (normale)"}
  ]
}
```

---

## Réentraînement automatique

```bash
# Réentraînement manuel
python retrain.py --min-samples 500

# Dry-run (test sans sauvegarder)
python retrain.py --dry-run
```

Le réentraînement est automatiquement déclenché quand :
- N nouveaux échantillons labellisés sont disponibles (feedback des analystes)
- Les performances du nouveau modèle dépassent l'ancien

---

## Structure du package

```
fraudx/
├── __init__.py          # Package
├── preprocessing.py     # Preprocessor réutilisable + FeatureEngineer
└── db.py                # Base de données SQLite

src/
├── api.py               # API FastAPI complète

app_streamlit.py         # Dashboard Streamlit
retrain.py               # Réentraînement automatique
simulate_stream.py       # Simulateur de flux temps réel
Dockerfile               # Conteneurisation
docker-compose.yml       # Orchestration
```

---

## Métriques cibles

| Métrique | Cible |
|----------|-------|
| F1-Score | ≥ 0.85 |
| Recall | ≥ 0.90 (HS1) |
| Precision | ≥ 0.80 |
| AUC-PR | ≥ 0.90 |
| Temps de réponse | < 100 ms |
| Faux positifs | < 2% |
