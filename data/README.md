# FRAUDX — Datasets

Ce dossier contient les données utilisées pour l'entraînement et les tests.

---

## Dataset principal : IEEE-CIS Fraud Detection

- **Source :** https://www.kaggle.com/c/ieee-cis-fraud-detection/data
- **Taille :** ~590 000 transactions, ~400 variables
- **Taux de fraude :** 3,5%
- **Fichiers attendus :**
  - `train_transaction.csv`
  - `train_identity.csv` (optionnel, fusion sur TransactionID)

### Téléchargement

```python
import kagglehub
path = kagglehub.dataset_download("ieee-fraud-detection")
```

Ou via le script d'entraînement :
```bash
python train.py
```

---

## Dataset alternatif : Credit Card Fraud (ULB)

- **Source :** https://www.kaggle.com/datasets/uciml/credit-card-fraud-detection
- **Taille :** ~284 807 transactions, 30 variables
- **Taux de fraude :** 0,17%

### Utilisation

```bash
python train.py --dataset credit-card --skip-download
```

Placez `creditcard.csv` dans ce dossier.

---

## Données générées par le pipeline

| Fichier | Description | Généré par |
|---------|-------------|------------|
| `X_train.pkl` | Features d'entraînement (scaled) | `02_Pretraitement.ipynb` ou `train.py` |
| `X_test.pkl` | Features de test (scaled) | `02_Pretraitement.ipynb` ou `train.py` |
| `y_train.pkl` | Labels d'entraînement | `02_Pretraitement.ipynb` ou `train.py` |
| `y_test.pkl` | Labels de test | `02_Pretraitement.ipynb` ou `train.py` |
| `X_featured.pkl` | Features avec engineering | `02_Pretraitement.ipynb` |
| `fraudx.db` | Base SQLite (prédictions + feedback) | API / retrain |

> ⚠️ Les fichiers `.pkl` et `.db` sont générés par le pipeline et ne sont pas versionnés (ignorés par `.gitignore`).
