# FRAUDX — Détection de la fraude bancaire et mobile money par IA au Togo

**Mémoire de Master — Collège de Paris Supérieur**
**Étudiant-chercheur :** Johnson Nancy
**Co-écrit avec :** Elna Comply (conformité réglementaire)

---

## Structure du projet

```
FRAUDX/
├── notebooks/                  # Notebooks Google Colab (Phases 1-7)
│   ├── 01_EDA.ipynb           # Analyse exploratoire (Jours 3-7)
│   ├── 02_Pretraitement.ipynb # Prétraitement & Feature Engineering (Jours 8-12)
│   ├── 03_IsolationForest.ipynb # Isolation Forest (Jours 13-14)
│   ├── 04_XGBoost.ipynb       # XGBoost + Optuna (Jours 15-24)
│   ├── 05_SHAP.ipynb          # Explicabilité SHAP (Jours 25-28)
│   └── 06_API_PoC.ipynb       # API FastAPI (Jours 39-42)
├── src/                       # Scripts Python
│   ├── utils.py              # Fonctions utilitaires
│   └── api.py                # API FastAPI (PoC)
├── config/
│   └── requirements.txt      # Dépendances Python
├── data/                     # Datasets (Kaggle → Google Drive)
├── models/                   # Modèles entraînés (joblib)
├── docs/
│   └── mockups/              # Maquettes d'interface
├── entretiens/               # Outils pour la phase qualitative
│   ├── MODELE_EMAIL_CONTACT.md    # Modèle d'email pour entretiens
│   └── GRILLE_ENTRETIEN_ANNEXE_A.md  # Grille d'entretien semi-directif
├── PLAN_MEMOIRE_FRAUDX.md    # Plan complet du mémoire
└── RESSOURCES_BIBLIOGRAPHIQUES.md  # Datasets, papiers, organismes, outils
```

## Pipeline technique

```
Données (IEEE-CIS) → EDA → Prétraitement/SMOTE → Modèles (Isolation Forest + XGBoost) 
→ SHAP → PoC (architecture + API) → Validation qualitative (entretiens)
→ Rédaction continue du mémoire
```

## Chronologie

| Semaine | Phase(s) | Focus |
|---------|----------|-------|
| 1 | 0-1 | Setup + EDA + lancement entretiens |
| 2 | 1-2 | Fin EDA + prétraitement |
| 3 | 2 | Feature engineering |
| 4 | 3-4 | Isolation Forest + premier XGBoost |
| 5 | 4 | Optimisation Optuna |
| 6 | 5 | SHAP |
| 7 | 6 | Contextualisation Togo + entretiens |
| 8 | 7 | PoC : architecture, mockups, API |
| 9-12 | 8 | Rédaction finale, relecture |

## Stack technique

- **Environnement :** Google Colab + Google Drive
- **Langage :** Python 3.10+
- **ML/DL :** Scikit-learn, XGBoost, Imbalanced-learn (SMOTE)
- **Optimisation :** Optuna
- **Explicabilité :** SHAP
- **API :** FastAPI + Uvicorn

## Comment démarrer

1. `01_EDA.ipynb` → Analyse exploratoire complète
2. `02_Pretraitement.ipynb` → Nettoyage, encodage, scaling
3. `03_IsolationForest.ipynb` → Détection d'anomalies (Niveau 1)
4. `04_XGBoost.ipynb` → Modèle principal + optimisation (Niveau 2)
5. `05_SHAP.ipynb` → Interprétabilité globale et locale
6. `06_API_PoC.ipynb` → API de prédiction
7. `entretiens/` → Préparer et mener les entretiens qualitatifs

## Dataset

- **Principal :** IEEE-CIS Fraud Detection (Kaggle, ~590k transactions, 3.5% fraude)
- **Alternatif :** Credit Card Fraud (ULB, ~285k transactions, 0.17% fraude)
