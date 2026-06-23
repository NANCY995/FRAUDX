"""
Runner local pour FRAUDX_Pipeline_Complet.py
Adapte le pipeline Colab à un environnement Windows local.
"""
import os, sys, time, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'outputs')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(OUTPUT_DIR)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

print("="*60)
print("FRAUDX — Pipeline de Détection de Fraude (Local)")
print("="*60)
print(f"\n📂 Répertoire de travail : {os.getcwd()}")
print(f"📂 Données : {DATA_DIR}")

# ────────────────────────────────────
# 1 — CHARGEMENT
# ────────────────────────────────────
print("\n📂 Chargement des fichiers...")
t0 = time.time()
train_trans = pd.read_csv(os.path.join(DATA_DIR, 'train_transaction.csv'))
train_identity = pd.read_csv(os.path.join(DATA_DIR, 'train_identity.csv'))
print(f"   train_transaction   : {train_trans.shape}")
print(f"   train_identity      : {train_identity.shape}")

train = train_trans.merge(train_identity, on='TransactionID', how='left')
print(f"   train (fusionné)    : {train.shape}  ({time.time()-t0:.2f}s)")

# ────────────────────────────────────
# 2 — EDA
# ────────────────────────────────────
print("\n" + "="*60)
print("📊 ANALYSE EXPLORATOIRE (EDA)")
print("="*60)

fraud_rate = train['isFraud'].mean()
print(f"\n🔹 Taux de fraude : {fraud_rate:.4f} ({fraud_rate*100:.2f}%)")
print(f"   Transactions légitimes :  {(train['isFraud']==0).sum():,}")
print(f"   Transactions frauduleuses : {(train['isFraud']==1).sum():,}")

# ────────────────────────────────────
# 3 — PRÉTRAITEMENT
# ────────────────────────────────────
print("\n" + "="*60)
print("🧹 PRÉTRAITEMENT")
print("="*60)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

X = train.drop(['TransactionID', 'isFraud'], axis=1, errors='ignore')
y = train['isFraud']

cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
print(f"\n   Variables numériques : {len(num_cols)}")
print(f"   Variables catégorielles : {len(cat_cols)}")

high_missing = [c for c in X.columns if X[c].isnull().mean() > 0.90]
X = X.drop(columns=high_missing, errors='ignore')
print(f"   Colonnes supprimées (>90% manquantes) : {len(high_missing)}")

# Split AVANT encodage
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"\n   Train : {X_train.shape}, Test : {X_test.shape}")

cat_cols_updated = [c for c in cat_cols if c in X.columns]
for col in cat_cols_updated:
    if X_train[col].nunique() < 20:
        train_dummies = pd.get_dummies(X_train[col], prefix=col, drop_first=True)
        test_dummies = pd.get_dummies(X_test[col], prefix=col, drop_first=True)
        test_dummies = test_dummies.reindex(columns=train_dummies.columns, fill_value=0)
        X_train = pd.concat([X_train.drop(col, axis=1), train_dummies], axis=1)
        X_test = pd.concat([X_test.drop(col, axis=1), test_dummies], axis=1)
    else:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col].astype(str))
        X_test[col] = X_test[col].astype(str).map(
            lambda x: le.transform([x])[0] if x in le.classes_ else -1
        )
print(f"   Encodage OK. Train : {X_train.shape}, Test : {X_test.shape}")

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
num_cols_train = X_train.select_dtypes(include=[np.number]).columns
X_train[num_cols_train] = scaler.fit_transform(X_train[num_cols_train])
X_test[num_cols_train] = scaler.transform(X_test[num_cols_train])
print("   ✅ Normalisation OK.")

# Imputation des NaNs (SMOTE ne les accepte pas)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_test = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns, index=X_test.index)
print("   ✅ Imputation (median) OK.")

from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy=0.5, k_neighbors=5, random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(f"   SMOTE OK. Train : {X_train_res.shape}, Fraude : {y_train_res.mean():.2%}")

# ────────────────────────────────────
# 4 — ISOLATION FOREST
# ────────────────────────────────────
print("\n" + "="*60)
print("🌲 NIVEAU 1 — Isolation Forest")
print("="*60)

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             average_precision_score, confusion_matrix)
import xgboost as xgb

t0 = time.time()
iso = IsolationForest(n_estimators=100, contamination=0.05, random_state=42, n_jobs=-1)
iso.fit(X_train_res)
t_train_iso = time.time() - t0

t0 = time.time()
y_pred_iso = iso.predict(X_test)
y_pred_iso = np.where(y_pred_iso == -1, 1, 0)
t_pred_iso = time.time() - t0
latency_iso = (t_pred_iso / len(X_test)) * 1000

f1_iso = f1_score(y_test, y_pred_iso)
recall_iso = recall_score(y_test, y_pred_iso)
prec_iso = precision_score(y_test, y_pred_iso)
pr_auc_iso = average_precision_score(y_test, y_pred_iso)
cm_iso = confusion_matrix(y_test, y_pred_iso)

print(f"   F1-Score  : {f1_iso:.4f}")
print(f"   Recall    : {recall_iso:.4f}")
print(f"   Précision : {prec_iso:.4f}")
print(f"   AUC-PR    : {pr_auc_iso:.4f}")
print(f"   Train     : {t_train_iso:.2f}s | Latence : {latency_iso:.3f} ms/tx")

# ────────────────────────────────────
# 5 — RANDOM FOREST
# ────────────────────────────────────
print("\n" + "="*60)
print("🌳 NIVEAU 2A — Random Forest")
print("="*60)

from sklearn.ensemble import RandomForestClassifier

t0 = time.time()
rf = RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_leaf=5,
                            class_weight='balanced', random_state=42, n_jobs=-1)
rf.fit(X_train_res, y_train_res)
t_train_rf = time.time() - t0

t0 = time.time()
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
t_pred_rf = time.time() - t0
latency_rf = (t_pred_rf / len(X_test)) * 1000

f1_rf = f1_score(y_test, y_pred_rf)
recall_rf = recall_score(y_test, y_pred_rf)
prec_rf = precision_score(y_test, y_pred_rf)
pr_auc_rf = average_precision_score(y_test, y_prob_rf)
cm_rf = confusion_matrix(y_test, y_pred_rf)

print(f"   F1-Score  : {f1_rf:.4f}")
print(f"   Recall    : {recall_rf:.4f}")
print(f"   Précision : {prec_rf:.4f}")
print(f"   AUC-PR    : {pr_auc_rf:.4f}")
print(f"   Train     : {t_train_rf:.2f}s | Latence : {latency_rf:.3f} ms/tx")

# ────────────────────────────────────
# 6 — XGBoost
# ────────────────────────────────────
print("\n" + "="*60)
print("⚡ NIVEAU 2B — XGBoost")
print("="*60)

scale_pos_weight = (y_train_res == 0).sum() / (y_train_res == 1).sum()

t0 = time.time()
xgb_model = xgb.XGBClassifier(
    n_estimators=200, max_depth=6, learning_rate=0.05,
    subsample=0.8, colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    eval_metric='aucpr', random_state=42, n_jobs=-1
)
xgb_model.fit(X_train_res, y_train_res)
t_train_xgb = time.time() - t0

t0 = time.time()
y_pred_xgb = xgb_model.predict(X_test)
y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]
t_pred_xgb = time.time() - t0
latency_xgb = (t_pred_xgb / len(X_test)) * 1000

f1_xgb = f1_score(y_test, y_pred_xgb)
recall_xgb = recall_score(y_test, y_pred_xgb)
prec_xgb = precision_score(y_test, y_pred_xgb)
pr_auc_xgb = average_precision_score(y_test, y_prob_xgb)
cm_xgb = confusion_matrix(y_test, y_pred_xgb)

print(f"   F1-Score  : {f1_xgb:.4f}")
print(f"   Recall    : {recall_xgb:.4f}")
print(f"   Précision : {prec_xgb:.4f}")
print(f"   AUC-PR    : {pr_auc_xgb:.4f}")
print(f"   Train     : {t_train_xgb:.2f}s | Latence : {latency_xgb:.3f} ms/tx")

# ────────────────────────────────────
# 7 — TABLEAU COMPARATIF
# ────────────────────────────────────
print("\n" + "="*60)
print("📊 BENCHMARK COMPARATIF")
print("="*60)

results = pd.DataFrame({
    'Modèle': ['Isolation Forest', 'Random Forest', 'XGBoost'],
    'F1-Score': [f1_iso, f1_rf, f1_xgb],
    'Recall': [recall_iso, recall_rf, recall_xgb],
    'Précision': [prec_iso, prec_rf, prec_xgb],
    'AUC-PR': [pr_auc_iso, pr_auc_rf, pr_auc_xgb],
    'Train (s)': [round(t_train_iso,1), round(t_train_rf,1), round(t_train_xgb,1)],
    'Latence (ms/tx)': [round(latency_iso,3), round(latency_rf,3), round(latency_xgb,3)]
})
print("\n" + results.to_string(index=False))
results.to_csv('benchmark_resultats.csv', index=False)
print("\n✅ Résultats sauvegardés dans benchmark_resultats.csv")

latex = results.to_latex(index=False, caption="Performances comparatives des modèles",
                         label="tab:benchmark", float_format="%.4f")
with open('benchmark_table.tex', 'w') as f:
    f.write(latex)
print("✅ Tableau LaTeX sauvegardé dans benchmark_table.tex")

TN, FP, FN, TP = cm_xgb.ravel()
print(f"\n   Matrice de confusion — XGBoost :")
print(f"   VN:{TN:,}  FP:{FP:,}  FN:{FN:,}  VP:{TP:,}")
print(f"   Taux FP : {FP/(TN+FP)*100:.2f}% | Taux FN : {FN/(TP+FN)*100:.2f}%")

# ────────────────────────────────────
# 8 — SHAP (échantillon réduit)
# ────────────────────────────────────
print("\n" + "="*60)
print("🔍 SHAP — Explicabilité XGBoost")
print("="*60)

import shap

X_test_sample = X_test.sample(min(300, len(X_test)), random_state=42)
y_test_sample = y_test.loc[X_test_sample.index]

t0 = time.time()
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test_sample)
print(f"   Calcul SHAP : {time.time()-t0:.2f}s")

shap_importance = np.abs(shap_values).mean(axis=0)
top10_idx = np.argsort(shap_importance)[-10:][::-1]
top10_features = X_test_sample.columns[top10_idx]

shap_table = pd.DataFrame({
    'Variable': top10_features,
    'Valeur SHAP moyenne': shap_importance[top10_idx]
})
print("\n🔹 Top 10 variables importantes (SHAP) :")
print(shap_table.to_string(index=False))
shap_table.to_csv('shap_top10_variables.csv', index=False)

# ────────────────────────────────────
# 9 — RÉSUMÉ FINAL
# ────────────────────────────────────
print("\n" + "="*60)
print("✅ PIPELINE TERMINÉ")
print("="*60)
print(f"\n📁 Tous les fichiers de sortie dans : {OUTPUT_DIR}")
print(f"   - benchmark_resultats.csv")
print(f"   - benchmark_table.tex")
print(f"   - shap_top10_variables.csv")
print(f"\n{'='*60}")
print("RÉSULTATS À REPORTER DANS LE MÉMOIRE")
print('='*60)

print(f"""
┌──────────────────────┬────────────┬────────────┬────────────┐
│ Métrique             │  IF        │  RF        │  XGB       │
├──────────────────────┼────────────┼────────────┼────────────┤
│ F1-Score             │ {f1_iso:.4f}      │ {f1_rf:.4f}      │ {f1_xgb:.4f}      │
│ Recall               │ {recall_iso:.4f}      │ {recall_rf:.4f}      │ {recall_xgb:.4f}      │
│ Précision            │ {prec_iso:.4f}      │ {prec_rf:.4f}      │ {prec_xgb:.4f}      │
│ AUC-PR               │ {pr_auc_iso:.4f}      │ {pr_auc_rf:.4f}      │ {pr_auc_xgb:.4f}      │
│ Temps entraînement   │ {t_train_iso:.1f}s      │ {t_train_rf:.1f}s      │ {t_train_xgb:.1f}s      │
│ Latence (ms/tx)      │ {latency_iso:.3f}      │ {latency_rf:.3f}      │ {latency_xgb:.3f}      │
└──────────────────────┴────────────┴────────────┴────────────┘
""")
