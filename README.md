# FRAUDX — Détection de la fraude bancaire et mobile money par IA au Togo

**Mémoire de Master — Collège de Paris Supérieur**
**Étudiant-chercheur :** Johnson Nancy
**Co-écrit avec :** Elna Comply (conformité réglementaire)

---

## Résultats clés

| Métrique | Valeur | Modèle |
|----------|--------|--------|
| Recall | **85.02%** | XGBoost (Optuna) |
| Precision | 13.54% | XGBoost (seuil optimal) |
| AUC-PR | 0.5735 | XGBoost |
| F1-Score | **0.607** | XGBoost (benchmark) |
| F1-Score RF | 0.370 | Random Forest |
| F1-Score IF | 0.161 | Isolation Forest |
| Seuil optimal | ~0.325 | Optimisé recall ≥ 85% |

> L'hypothèse H1 (recall ≥ 85%) est **validée** : le modèle détecte 85% des fraudes avec une precision de 13.5% (meilleur compromis après optimisation du seuil).

## Structure du projet

```
FRAUDX/
├── app.py                       # Application Streamlit unifiée (6 pages)
├── train.py                     # Pipeline d'entraînement CLI + Optuna
├── simulate_stream.py           # Simulation flux temps réel
├── benchmark.py                 # Benchmark IF vs RF vs XGBoost
├── generate_figures.py          # Figures pour le mémoire (Ch. III)
├── retrain.py                   # Script de réentraînement
├── fraudx/                      # Package Python
│   ├── preprocessing.py         # Transformation des données
│   ├── synthetic_data.py        # Génération données synthétiques Togo
│   ├── cli.py                   # Interface CLI
│   ├── config.py                # Configuration
│   ├── db.py                    # Base SQLite (logs, feedback)
│   └── metrics.py               # Métriques personnalisées
├── src/
│   └── api.py                   # API FastAPI (5 endpoints)
├── models_optuna/               # Modèle final XGBoost + artefacts
│   ├── xgb_model.pkl            # Modèle entraîné (483 features)
│   ├── best_threshold.npy       # Seuil optimal
│   ├── scaler.pkl               # StandardScaler
│   ├── ohe_encoder.pkl          # OneHotEncoder
│   └── metrics.json             # Métriques de performance
├── notebooks/                   # Notebooks Google Colab (Phases 1-7)
├── reports/                     # Benchmark + figures mémoire
├── tests/                       # Tests pytest (29 tests)
├── .github/workflows/           # CI GitHub Actions
├── requirements.txt             # Dépendances
└── pyproject.toml               # Configuration Python
```

## Pipeline technique

```
Données (IEEE-CIS 590k lignes)
  → EDA (distribution, NaN, montant, temporel)
  → Prétraitement (imputation, OHE, scaling, 483 features)
  → XGBoost + Optuna (30 essais, échantillonnage 50k)
  → Optimisation du seuil (recall ≥ 85%)
  → SHAP (interprétabilité top 15 features)
  → API FastAPI (5 endpoints)
  → Application Streamlit (6 pages interactives)
  → Benchmark (XGBoost > RF > Isolation Forest)
  → Déploiement Streamlit Cloud
```

## Architecture applicative

- **Frontend :** [Streamlit](https://fraudx-memoirel3.streamlit.app/) — 6 pages : Dataset, Prétraitement, Entraînement, Résultats, Benchmark, Prédiction
- **API REST :** FastAPI — health, predict, predict/togo, batch, logs, feedback
- **Stockage :** SQLite (predictions, feedback, logs)
- **CI/CD :** GitHub Actions (tests automatiques + retrain sur demande)

## Stack technique

- **Environnement :** Google Colab (notebooks), Streamlit Cloud (production)
- **Langage :** Python 3.10+
- **ML/DL :** Scikit-learn, XGBoost, Imbalanced-learn (SMOTE)
- **Optimisation :** Optuna
- **Explicabilité :** SHAP (TreeExplainer)
- **API :** FastAPI + Uvicorn
- **Dashboard :** Streamlit + Plotly
- **Déploiement :** Streamlit Cloud (gratuit)

## Déploiement

L'application est disponible en ligne :
- **Streamlit Cloud :** [fraudx-memoirel3.streamlit.app](https://fraudx-memoirel3.streamlit.app/)
- **Repository GitHub :** [github.com/NANCY995/FRAUDX](https://github.com/NANCY995/FRAUDX)

### Lancement local

```bash
git clone https://github.com/NANCY995/FRAUDX.git
cd FRAUDX
pip install -r requirements.txt
streamlit run app.py          # Application complète
uvicorn src.api:app --reload  # API seule (port 8000)
```

## Tests

```bash
pytest tests/ -v --tb=short   # 29 tests (API, E2E, preprocessing, intégration)
```

Les tests couvrent : prédiction IEEE-CIS, batch, Mobile Money Togo, scénarios fraude, preprocessing, et endpoints santé.

## Datasets

- **Principal :** IEEE-CIS Fraud Detection (Kaggle, ~590k transactions, 3.5% fraude) — auto-téléchargé via kagglehub si absent
- **Alternatif :** Credit Card Fraud (ULB, ~285k transactions, 0.17% fraude) — auto-téléchargé si absent
- **Synthétique Togo :** Généré localement via `fraudx/synthetic_data.py`

## Limites et prochaines étapes

- **Données réelles Togo :** Les tests Mobile Money utilisent des données synthétiques faute de données réelles disponibles. Une collaboration avec un opérateur (TogoCom, Moov, Flooz) permettrait de valider le modèle en conditions réelles.
- **Généralisation :** Le modèle est entraîné sur IEEE-CIS (USA). L'adaptation au contexte ouest-africain nécessite un réentraînement sur des données locales.
- **Production :** L'API et le dashboard sont fonctionnels, mais une mise en production nécessiterait une infrastructure cloud scalable (authentification, monitoring, HA).
- **Réentraînement continu :** Un workflow GitHub Actions permet le réentraînement planifié, mais l'intégration avec des données fraîches n'est pas encore automatisée.
- **Scalabilité :** L'API FastAPI n'est pas déployée sur le cloud (seul le dashboard Streamlit est en ligne). Le déploiement complet API + BDD nécessite Render/Supabase.

## Licence

MIT
