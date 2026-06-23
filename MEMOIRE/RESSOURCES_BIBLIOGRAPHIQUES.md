# RESSOURCES — FRAUDX (Détection de fraude bancaire par IA au Togo)

> Inventaire des datasets, papiers académiques, outils et organismes de référence.

---

## 1. DATASETS (Kaggle) — 100% Réels

### Dataset Principal : IEEE-CIS Fraud Detection
- **Lien :** https://www.kaggle.com/c/ieee-cis-fraud-detection/data
- **Taille :** ~590 000 transactions
- **Taux fraude :** 3,5%
- **Date :** 2019
- **Statut :** 100% VÉRIFIÉ

### Dataset Alternatif : Credit Card Fraud (ULB)
- **Lien :** https://www.kaggle.com/datasets/uciml/credit-card-fraud-detection
- **Taille :** ~284 807 transactions
- **Taux fraude :** 0,17%
- **Date :** 2017
- **Statut :** 100% VÉRIFIÉ

### Kaggle API Key (téléchargement automatique)
- **Lien :** https://www.kaggle.com/settings
- → Cliquer sur "Create New API Key" → génère `kaggle.json`

---

## 2. RESSOURCES TECHNIQUES IA/ML

| Outil | Documentation | Paper original |
|---|---|---|
| **XGBoost** | https://xgboost.readthedocs.io/ | https://doi.org/10.1145/2939672.2939785 |
| **SHAP** | https://shap.readthedocs.io/ | arXiv:1703.07191 |
| **Scikit-learn** | https://scikit-learn.org/stable/ | https://jmlr.org/papers/v12/pedregosa11a.html |
| **Isolation Forest** | https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html | https://doi.org/10.1109/ICDM.2008.17 |
| **Optuna** | https://optuna.org/ | — |
| **Imbalanced-learn (SMOTE)** | https://imbalanced-learn.org/stable/ | — |
| **TensorFlow/Keras** | https://www.tensorflow.org/ | — |
| **NumPy** | https://numpy.org/ | — |
| **Pandas** | https://pandas.pydata.org/ | — |
| **Matplotlib** | https://matplotlib.org/ | — |
| **Seaborn** | https://seaborn.pydata.org/ | — |
| **Missingno** | https://github.com/ResidentMario/missingno | — |
| **Category Encoders** | https://contrib.scikit-learn.org/category_encoders/ | — |
| **Joblib** | https://joblib.readthedocs.io/ | — |
| **FastAPI** | https://fastapi.tiangolo.com/ | — |
| **Ngrok** | https://ngrok.com/ | — |

---

## 3. ORGANISMES RÉGLEMENTAIRES (Références mémoire)

### BCEAO (Banque Centrale des États de l'Afrique de l'Ouest)
- **Site officiel :** https://www.bceao.int/
- **Directive AML/CFT :** https://www.bceao.int/fr/reglementation
- **Rapport UEMOA 2023 :** https://www.bceao.int/fr/publications

### UEMOA (Union Économique et Monétaire Ouest Africaine)
- **Site officiel :** https://www.uemoa.int/
- **Règlementation bancaire :** https://www.uemoa.int/fr/reglementation-bancaire

### GIABA (Groupe d'Action contre le Blanchiment en Afrique de l'Ouest)
- **Site officiel :** https://www.giaba.org/
- **Rapport AML/CFT 2023 :** https://www.giaba.org/publications

### CENTIF Côte d'Ivoire (Typologies fraude)
- **Site :** https://www.centif.ci/
- **Rapport typologies :** https://www.centif.ci/documents/

### GSMA (Mobile Money Africa)
- **Site :** https://www.gsma.com/mobilefordevelopment/
- **Togo Report 2023 :** https://www.gsma.com/mobilefordevelopment/resources/

### Findev Gateway (UEMOA)
- **Site :** https://www.findevgateway.org/
- **Blog UEMOA 2024 :** https://www.findevgateway.org/fr/blog/2024/06

### OECD — Consumer Protection in Digital Finance
- **Lien :** https://www.oecd.org/finance/consumer-protection-digital-finance/

### FATF (GAFI) — Digital Identity & Financial Inclusion
- **Lien :** https://www.fatf-gafi.org/publications/identity/

---

## 4. RÉFÉRENCES BIBLIOGRAPHIQUES (Liens directs)

| Référence | DOI / Lien |
|---|---|
| XGBoost — Chen & Guestrin (2016) | https://doi.org/10.1145/2939672.2939785 |
| SHAP — Lundberg & Lee (2017) | arXiv:1703.07191 |
| SHAP Nature MI — Lundberg et al. (2020) | https://doi.org/10.1038/s42256-019-0105-2 |
| Scikit-learn — Pedregosa et al. (2011) | https://jmlr.org/papers/v12/pedregosa11a.html |
| Deep Learning Book — Goodfellow et al. | https://www.deeplearningbook.org/ |
| Isolation Forest — Liu et al. (2008) | https://doi.org/10.1109/ICDM.2008.17 |
| LIME — Ribeiro et al. (2016) | https://doi.org/10.1371/journal.pone.0130140 |
| SMOTE — Chawla et al. (2002) | https://doi.org/10.1613/jair.953 |
| Random Forest — Breiman (2001) | https://doi.org/10.1023/A:1010933404324 |
| Botchey et al. — Ghana (IJERT 2022) | https://doi.org/10.17577/IJERTV11IS010191 |
| Lokanan — Ouganda (Wiley 2024) | https://doi.org/10.1002/aia2.67 |
| Adewumi & Akinyelu — Nigeria (IEEE 2020) | https://doi.org/10.1109/ACCESS.2020.3018846 |
| Adepoju et al. — Mobile Money Afrique (2023) | https://doi.org/10.1016/j.techfore.2023.122716 |

---

## 5. OUTILS TECHNIQUES (Développement PoC)

| Outil | Usage | Lien |
|---|---|---|
| **Google Colab** | Notebooks exécutables (GPU gratuit) | https://colab.research.google.com/ |
| **GitHub** | Versionnement privé | https://github.com/ |
| **Google Drive** | Stockage datasets / modèles | https://drive.google.com/ |
| **Draw.io** | Schémas d'architecture | https://draw.io/ |
| **LucidChart** | Schémas (alternative) | https://lucidchart.com/ |
| **Figma** | Mockups dashboard | https://www.figma.com/ |
| **Canva** | Mockups (alternative) | https://www.canva.com/ |
| **Overleaf** | Rédaction LaTeX (mémoire) | https://www.overleaf.com/ |
| **Zotero** | Gestion des références APA | https://www.zotero.org/ |
| **Mendeley** | Gestion des références (alternative) | https://www.mendeley.com/ |

---

## 6. COMMANDES UTILES (Rappel rapide)

### Kaggle — Téléchargement automatique via Python

```python
import kagglehub
path = kagglehub.dataset_download("ieee-fraud-detection")
```

### Installation des dépendances

```python
!pip install pandas numpy matplotlib seaborn scikit-learn xgboost imbalanced-learn shap kagglehub optuna category_encoders
```

### Split stratifié + SMOTE (ordre correct)

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    stratify=y, random_state=42)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
```

### SHAP — Explicabilité

```python
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, max_display=20)
```
