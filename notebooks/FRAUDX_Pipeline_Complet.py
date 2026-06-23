"""
FRAUDX — Pipeline Complet de Détection de Fraude
=================================================
À exécuter dans Google Colab (Runtime → Run all)
Durée estimée : ~45-60 min sur GPU (T4 gratuit)

Étapes :
  0. Setup Kaggle + Installation
  1. Téléchargement et chargement IEEE-CIS
  2. Analyse Exploratoire (EDA)
  3. Prétraitement + SMOTE
  4. Entraînement : Isolation Forest / Random Forest / XGBoost
  5. Évaluation comparative (F1, Recall, AUC-PR, Matrice de confusion)
  6. SHAP Explainability
  7. Benchmark export (CSV/LaTeX)
"""

# ─────────────────────────────────────────────────────
# CELLULE 0 — Setup Kaggle + Installation
# ─────────────────────────────────────────────────────
# IMPORTANT : Télécharge d'abord ton kaggle.json depuis
# https://www.kaggle.com/settings → API → Create New Token
# puis exécute cette cellule pour l'uploader.

from google.colab import files
import os, zipfile, json, time, warnings, sys, io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             average_precision_score,
                             confusion_matrix, classification_report,
                             precision_recall_curve)
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import shap

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
pd.set_option('display.max_columns', 50)

print("📦 Bibliothèques chargées.")
print(f"   Python {sys.version}")
print(f"   Pandas {pd.__version__}")

# Upload kaggle.json
if not os.path.exists('/root/.kaggle/kaggle.json'):
    print("\n🔑 Upload de kaggle.json nécessaire.")
    print("   Va sur https://www.kaggle.com/settings → API → Create New Token")
    uploaded = files.upload()
    for fn in uploaded.keys():
        with open('/root/.kaggle/kaggle.json', 'wb') as f:
            f.write(uploaded[fn])
    os.chmod('/root/.kaggle/kaggle.json', 0o600)
    print("✅ kaggle.json installé.")
else:
    print("✅ kaggle.json déjà présent.")

# ─────────────────────────────────────────────────────
# CELLULE 1 — Téléchargement du dataset IEEE-CIS
# ─────────────────────────────────────────────────────

print("\n📥 Téléchargement de IEEE-CIS Fraud Detection...")
os.system('kaggle competitions download -c ieee-fraud-detection -p /tmp/ieee/')

# Extraction
with zipfile.ZipFile('/tmp/ieee/ieee-fraud-detection.zip', 'r') as z:
    z.extractall('/tmp/ieee/')
print("✅ Extraction terminée.")

# ─────────────────────────────────────────────────────
# CELLULE 2 — Chargement des données
# ─────────────────────────────────────────────────────

print("\n📂 Chargement des fichiers...")
train_trans = pd.read_csv('/tmp/ieee/train_transaction.csv')
train_identity = pd.read_csv('/tmp/ieee/train_identity.csv')
test_trans = pd.read_csv('/tmp/ieee/test_transaction.csv')
test_identity = pd.read_csv('/tmp/ieee/test_identity.csv')

print(f"   train_transaction   : {train_trans.shape}")
print(f"   train_identity      : {train_identity.shape}")
print(f"   test_transaction    : {test_trans.shape}")
print(f"   test_identity       : {test_identity.shape}")

# Fusion
train = train_trans.merge(train_identity, on='TransactionID', how='left')
print(f"\n   train (fusionné)    : {train.shape}")

# ─────────────────────────────────────────────────────
# CELLULE 3 — Analyse Exploratoire (EDA)
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("📊 ANALYSE EXPLORATOIRE (EDA)")
print("="*60)

# 3.1 Distribution de la variable cible
fraud_rate = train['isFraud'].mean()
print(f"\n🔹 Taux de fraude : {fraud_rate:.4f} ({fraud_rate*100:.2f}%)")
print(f"   Transactions légitimes :  {(train['isFraud']==0).sum():,}")
print(f"   Transactions frauduleuses : {(train['isFraud']==1).sum():,}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
train['isFraud'].value_counts().plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'])
axes[0].set_title('Distribution isFraud', fontsize=14)
axes[0].set_xticklabels(['Non fraude (0)', 'Fraude (1)'])
axes[0].set_ylabel('Nombre de transactions')

train['isFraud'].value_counts(normalize=True).plot(kind='pie', ax=axes[1],
    labels=['Non fraude','Fraude'], autopct='%1.2f%%',
    colors=['#2ecc71','#e74c3c'], explode=[0, 0.05])
axes[1].set_title('Proportion isFraud', fontsize=14)
plt.tight_layout()
plt.savefig('eda_distribution_target.png', dpi=150)
plt.show()
print("   ✅ Graphique sauvegardé : eda_distribution_target.png")

# 3.2 Analyse du montant
print("\n🔹 Analyse de TransactionAmt :")
print(f"   Moyenne : {train['TransactionAmt'].mean():.2f}")
print(f"   Médiane : {train['TransactionAmt'].median():.2f}")
print(f"   Min     : {train['TransactionAmt'].min():.2f}")
print(f"   Max     : {train['TransactionAmt'].max():.2f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(train['TransactionAmt'], bins=100, color='#3498db', alpha=0.7)
axes[0].set_title('Distribution des montants (toutes transactions)', fontsize=13)
axes[0].set_xlabel('Montant')
axes[0].set_ylabel('Fréquence')
axes[0].set_xlim(0, train['TransactionAmt'].quantile(0.99))

# Montant par classe
train_box = train.copy()
train_box['isFraud'] = train_box['isFraud'].map({0:'Non fraude', 1:'Fraude'})
train_box.boxplot(column='TransactionAmt', by='isFraud', ax=axes[1])
axes[1].set_title('Montant par classe', fontsize=13)
axes[1].set_ylabel('Montant')
axes[1].set_ylim(0, train['TransactionAmt'].quantile(0.95))
plt.suptitle('')
plt.tight_layout()
plt.savefig('eda_montant.png', dpi=150)
plt.show()
print("   ✅ Graphique sauvegardé : eda_montant.png")

# 3.3 Analyse temporelle
print("\n🔹 Analyse temporelle (TransactionDT) :")
# Convertir Timestamp en jours (référence dataset)
train['DT_day'] = train['TransactionDT'] // (24*3600)
day_fraud = train.groupby('DT_day')['isFraud'].agg(['count','mean'])
day_fraud.columns = ['nb_transactions', 'fraud_rate']

fig, ax1 = plt.subplots(figsize=(14, 5))
color1 = '#3498db'
color2 = '#e74c3c'
ax1.bar(day_fraud.index, day_fraud['nb_transactions'], color=color1, alpha=0.6, label='Transactions')
ax1.set_xlabel('Jour (référence dataset)')
ax1.set_ylabel('Nombre de transactions', color=color1)
ax2 = ax1.twinx()
ax2.plot(day_fraud.index, day_fraud['fraud_rate'], color=color2, marker='o', linewidth=2, label='Taux de fraude')
ax2.set_ylabel('Taux de fraude', color=color2)
plt.title('Évolution temporelle : volume et taux de fraude', fontsize=14)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
plt.savefig('eda_temporel.png', dpi=150)
plt.show()
print("   ✅ Graphique sauvegardé : eda_temporel.png")

# 3.4 Corrélations (top variables)
print("\n🔹 Top 15 corrélations avec isFraud :")
numeric_cols = train.select_dtypes(include=[np.number]).columns
corr = train[numeric_cols].corr()['isFraud'].abs().sort_values(ascending=False)
top15_corr = corr[1:16]
print(top15_corr.to_string())

plt.figure(figsize=(10, 6))
top15_corr.plot(kind='barh', color='#e67e22')
plt.title('Top 15 des corrélations absolues avec isFraud', fontsize=14)
plt.xlabel('|Corrélation|')
plt.tight_layout()
plt.savefig('eda_correlations.png', dpi=150)
plt.show()
print("   ✅ Graphique sauvegardé : eda_correlations.png")

# 3.5 Valeurs manquantes
missing = train.isnull().sum()
missing_pct = (missing / len(train) * 100).sort_values(ascending=False)
missing_top = missing_pct[missing_pct > 0].head(20)
print(f"\n🔹 Top 20 des variables avec valeurs manquantes :")
print(missing_top.to_string())

# ─────────────────────────────────────────────────────
# CELLULE 4 — Prétraitement
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("🧹 PRÉTRAITEMENT")
print("="*60)

# 4.1 Séparation features / target
X = train.drop(['TransactionID', 'isFraud'], axis=1, errors='ignore')
y = train['isFraud']

# 4.2 Identification des types de colonnes
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
print(f"\n   Variables numériques : {len(num_cols)}")
print(f"   Variables catégorielles : {len(cat_cols)}")

# 4.3 Suppression des colonnes avec >90% de valeurs manquantes
high_missing = [c for c in X.columns if X[c].isnull().mean() > 0.90]
X = X.drop(columns=high_missing, errors='ignore')
print(f"   Colonnes supprimées (>90% manquantes) : {len(high_missing)}")
print(f"   Restantes : {X.shape[1]}")

# 4.5 Split Train / Test stratifié (AVANT encodage — anti-leakage)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"\n   Train : {X_train.shape}, Test : {X_test.shape}")

# 4.4 Encodage des variables catégorielles (fit sur train, transform sur test)
cat_cols_updated = [c for c in cat_cols if c in X.columns]
for col in cat_cols_updated:
    if X_train[col].nunique() < 20:
        # One-Hot: fit+transform séparés, alignement des colonnes
        train_dummies = pd.get_dummies(X_train[col], prefix=col, drop_first=True)
        test_dummies = pd.get_dummies(X_test[col], prefix=col, drop_first=True)
        test_dummies = test_dummies.reindex(columns=train_dummies.columns, fill_value=0)
        X_train = pd.concat([X_train.drop(col, axis=1), train_dummies], axis=1)
        X_test = pd.concat([X_test.drop(col, axis=1), test_dummies], axis=1)
    else:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col].astype(str))
        # Catégories inconnues dans le test → -1
        X_test[col] = X_test[col].astype(str).map(
            lambda x: le.transform([x])[0] if x in le.classes_ else -1
        )
print(f"   Encodage terminé. Train : {X_train.shape}, Test : {X_test.shape}")
print(f"\n   Train : {X_train.shape}, Test : {X_test.shape}")
print(f"   Train fraud rate : {y_train.mean():.4f}")
print(f"   Test fraud rate  : {y_test.mean():.4f}")

# 4.6 Normalisation
scaler = StandardScaler()
num_cols_train = X_train.select_dtypes(include=[np.number]).columns
X_train[num_cols_train] = scaler.fit_transform(X_train[num_cols_train])
X_test[num_cols_train] = scaler.transform(X_test[num_cols_train])
print("   ✅ Normalisation (StandardScaler) effectuée.")

# 4.7 SMOTE
print("\n🔹 Application de SMOTE...")
smote = SMOTE(sampling_strategy=0.5, k_neighbors=5, random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(f"   Après SMOTE — Train : {X_train_res.shape}")
print(f"   Non fraude : {(y_train_res==0).sum():,}, Fraude : {(y_train_res==1).sum():,}")
print(f"   Ratio : {y_train_res.mean():.2%} de fraudes")

# ─────────────────────────────────────────────────────
# CELLULE 5 — Entraînement Isolation Forest (Niveau 1)
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("🌲 NIVEAU 1 — Isolation Forest")
print("="*60)

t0 = time.time()
iso = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)
iso.fit(X_train_res)
t_train_iso = time.time() - t0
print(f"   Entraînement : {t_train_iso:.2f}s")

# Prédiction
t0 = time.time()
y_pred_iso = iso.predict(X_test)
y_pred_iso = np.where(y_pred_iso == -1, 1, 0)
t_pred_iso = time.time() - t0
latency_iso = (t_pred_iso / len(X_test)) * 1000

f1_iso = f1_score(y_test, y_pred_iso)
recall_iso = recall_score(y_test, y_pred_iso)
prec_iso = precision_score(y_test, y_pred_iso)
pr_auc_iso = average_precision_score(y_test, y_pred_iso)

print(f"   F1-Score  : {f1_iso:.4f}")
print(f"   Recall    : {recall_iso:.4f}")
print(f"   Précision : {prec_iso:.4f}")
print(f"   AUC-PR    : {pr_auc_iso:.4f}")
print(f"   Latence   : {latency_iso:.3f} ms/transaction")

cm_iso = confusion_matrix(y_test, y_pred_iso)

# ─────────────────────────────────────────────────────
# CELLULE 6 — Entraînement Random Forest (Niveau 2a)
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("🌳 NIVEAU 2A — Random Forest")
print("="*60)

t0 = time.time()
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=12,
    min_samples_leaf=5,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_res, y_train_res)
t_train_rf = time.time() - t0
print(f"   Entraînement : {t_train_rf:.2f}s")

t0 = time.time()
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
t_pred_rf = time.time() - t0
latency_rf = (t_pred_rf / len(X_test)) * 1000

f1_rf = f1_score(y_test, y_pred_rf)
recall_rf = recall_score(y_test, y_pred_rf)
prec_rf = precision_score(y_test, y_pred_rf)
pr_auc_rf = average_precision_score(y_test, y_prob_rf)

print(f"   F1-Score  : {f1_rf:.4f}")
print(f"   Recall    : {recall_rf:.4f}")
print(f"   Précision : {prec_rf:.4f}")
print(f"   AUC-PR    : {pr_auc_rf:.4f}")
print(f"   Latence   : {latency_rf:.3f} ms/transaction")

cm_rf = confusion_matrix(y_test, y_pred_rf)

# ─────────────────────────────────────────────────────
# CELLULE 7 — Entraînement XGBoost (Niveau 2b)
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("⚡ NIVEAU 2B — XGBoost")
print("="*60)

# Calcul du scale_pos_weight
scale_pos_weight = (y_train_res == 0).sum() / (y_train_res == 1).sum()
print(f"   scale_pos_weight = {scale_pos_weight:.2f}")

t0 = time.time()
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    eval_metric='aucpr',
    use_label_encoder=False,
    enable_categorical=False,
    random_state=42,
    n_jobs=-1
)
xgb_model.fit(
    X_train_res, y_train_res,
    eval_set=[(X_test, y_test)],
    verbose=False
)
t_train_xgb = time.time() - t0
print(f"   Entraînement : {t_train_xgb:.2f}s")

t0 = time.time()
y_pred_xgb = xgb_model.predict(X_test)
y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]
t_pred_xgb = time.time() - t0
latency_xgb = (t_pred_xgb / len(X_test)) * 1000

f1_xgb = f1_score(y_test, y_pred_xgb)
recall_xgb = recall_score(y_test, y_pred_xgb)
prec_xgb = precision_score(y_test, y_pred_xgb)
pr_auc_xgb = average_precision_score(y_test, y_prob_xgb)

print(f"   F1-Score  : {f1_xgb:.4f}")
print(f"   Recall    : {recall_xgb:.4f}")
print(f"   Précision : {prec_xgb:.4f}")
print(f"   AUC-PR    : {pr_auc_xgb:.4f}")
print(f"   Latence   : {latency_xgb:.3f} ms/transaction")

cm_xgb = confusion_matrix(y_test, y_pred_xgb)

# ─────────────────────────────────────────────────────
# CELLULE 8 — Tableau comparatif + Graphiques
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("📊 BENCHMARK COMPARATIF")
print("="*60)

results = pd.DataFrame({
    'Modèle': ['Isolation Forest', 'Random Forest', 'XGBoost'],
    'F1-Score': [f1_iso, f1_rf, f1_xgb],
    'Recall': [recall_iso, recall_rf, recall_xgb],
    'Précision': [prec_iso, prec_rf, prec_xgb],
    'AUC-PR': [pr_auc_iso, pr_auc_rf, pr_auc_xgb],
    'Train (s)': [t_train_iso, t_train_rf, t_train_xgb],
    'Latence (ms/tx)': [latency_iso, latency_rf, latency_xgb]
})
results = results.round(4)
print("\n" + results.to_string(index=False))

# Export CSV
results.to_csv('benchmark_resultats.csv', index=False)
print("\n✅ benchmark_resultats.csv exporté.")

# Export LaTeX
latex = results.to_latex(index=False, caption="Performances comparatives des modèles",
                         label="tab:benchmark", float_format="%.4f")
with open('benchmark_table.tex', 'w') as f:
    f.write(latex)
print("✅ benchmark_table.tex exporté.")

# ─────────────────────────────────────────────────────
# CELLULE 9 — Graphiques de performance
# ─────────────────────────────────────────────────────

# 9.1 Barres comparatives
metrics = ['F1-Score', 'Recall', 'Précision', 'AUC-PR']
x_pos = np.arange(len(metrics))
width = 0.25

fig, ax = plt.subplots(figsize=(14, 6))
ax.bar(x_pos - width, [f1_iso, recall_iso, prec_iso, pr_auc_iso], width,
       label='Isolation Forest', color='#e74c3c', alpha=0.8)
ax.bar(x_pos, [f1_rf, recall_rf, prec_rf, pr_auc_rf], width,
       label='Random Forest', color='#3498db', alpha=0.8)
ax.bar(x_pos + width, [f1_xgb, recall_xgb, prec_xgb, pr_auc_xgb], width,
       label='XGBoost', color='#2ecc71', alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(metrics, fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Comparaison des performances par modèle', fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.set_ylim(0, 1.05)
for i, v in enumerate([f1_iso, recall_iso, prec_iso, pr_auc_iso]):
    ax.text(i - width, v + 0.01, f'{v:.3f}', ha='center', fontsize=9)
for i, v in enumerate([f1_rf, recall_rf, prec_rf, pr_auc_rf]):
    ax.text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=9)
for i, v in enumerate([f1_xgb, recall_xgb, prec_xgb, pr_auc_xgb]):
    ax.text(i + width, v + 0.01, f'{v:.3f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('benchmark_comparatif.png', dpi=150)
plt.show()
print("✅ benchmark_comparatif.png sauvegardé.")

# 9.2 Matrices de confusion
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
models_cm = [('Isolation Forest', cm_iso), ('Random Forest', cm_rf), ('XGBoost', cm_xgb)]
for ax, (name, cm) in zip(axes, models_cm):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, cbar=False,
                xticklabels=['Non fraude', 'Fraude'],
                yticklabels=['Non fraude', 'Fraude'])
    ax.set_title(f'{name}', fontsize=13, fontweight='bold')
    ax.set_xlabel('Prédiction')
    ax.set_ylabel('Réel')
plt.tight_layout()
plt.savefig('matrices_confusion.png', dpi=150)
plt.show()
print("✅ matrices_confusion.png sauvegardé.")

# 9.3 Courbe Precision-Recall
fig, ax = plt.subplots(figsize=(10, 6))
for name, y_prob in [('Random Forest', y_prob_rf), ('XGBoost', y_prob_xgb)]:
    prec_curve, rec_curve, _ = precision_recall_curve(y_test, y_prob)
    auc = average_precision_score(y_test, y_prob)
    ax.plot(rec_curve, prec_curve, label=f'{name} (AUC-PR={auc:.4f})', linewidth=2)
ax.axhline(y=prec_iso, color='#e74c3c', linestyle='--', alpha=0.7,
           label=f'Isolation Forest (AUC-PR={pr_auc_iso:.4f})')
ax.set_xlabel('Recall', fontsize=12)
ax.set_ylabel('Precision', fontsize=12)
ax.set_title('Courbes Precision-Recall', fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.tight_layout()
plt.savefig('courbe_precision_recall.png', dpi=150)
plt.show()
print("✅ courbe_precision_recall.png sauvegardé.")

# ─────────────────────────────────────────────────────
# CELLULE 10 — SHAP Explainability
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("🔍 EXPLICABILITÉ SHAP — Modèle XGBoost")
print("="*60)

# Échantillon pour SHAP (300 lignes — compromis temps/précision)
X_test_sample = X_test.sample(min(300, len(X_test)), random_state=42)
print(f"   Échantillon SHAP : {len(X_test_sample)} transactions")

# SHAP TreeExplainer
t0 = time.time()
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test_sample)
t_shap = time.time() - t0
print(f"   Calcul SHAP : {t_shap:.2f}s")

# 10.1 Importance globale (bar plot)
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test_sample, plot_type="bar", max_display=20, show=False)
plt.title('Importance globale des variables (SHAP — XGBoost)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_importance_globale.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ shap_importance_globale.png sauvegardé.")

# 10.2 Summary plot (beeswarm)
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test_sample, max_display=20, show=False)
plt.title('SHAP Summary — Impact des variables (XGBoost)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_summary.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ shap_summary.png sauvegardé.")

# 10.3 Top 10 variables (export tableau)
shap_importance = np.abs(shap_values).mean(axis=0)
top10_idx = np.argsort(shap_importance)[-10:][::-1]
top10_features = X_test_sample.columns[top10_idx]
top10_values = shap_importance[top10_idx]

shap_table = pd.DataFrame({
    'Variable': top10_features,
    'Valeur SHAP moyenne': top10_values
})
print("\n🔹 Top 10 des variables les plus importantes (SHAP) :")
print(shap_table.to_string(index=False))
shap_table.to_csv('shap_top10_variables.csv', index=False)
print("✅ shap_top10_variables.csv exporté.")

# 10.4 Exemple individuel (force plot)
print("\n🔹 Exemple d'explication individuelle (première transaction frauduleuse test) :")
y_test_sample = y_test.loc[X_test_sample.index]
fraud_idx = np.where(y_test_sample == 1)[0]
if len(fraud_idx) > 0:
    idx = fraud_idx[0]
    shap.force_plot(explainer.expected_value, shap_values[idx, :],
                    X_test_sample.iloc[idx, :], matplotlib=True)
    plt.savefig('shap_force_plot_individuel.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ shap_force_plot_individuel.png sauvegardé.")

# 10.5 Waterfall plot
if len(fraud_idx) > 0:
    idx = fraud_idx[0]
    shap.plots.waterfall(shap.Explanation(values=shap_values[idx],
        base_values=explainer.expected_value,
        data=X_test_sample.iloc[idx].values,
        feature_names=X_test_sample.columns.tolist()), max_display=15)
    plt.tight_layout()
    plt.savefig('shap_waterfall.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ shap_waterfall.png sauvegardé.")

# ─────────────────────────────────────────────────────
# CELLULE 11 — Résumé final
# ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("📋 RÉSUMÉ FINAL — Résultats à reporter dans le mémoire")
print("="*60)

print(f"""
┌─────────────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Métrique                    │ Isolation Forest     │ Random Forest        │ XGBoost              │
├─────────────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ F1-Score                    │ {f1_iso:.4f}               │ {f1_rf:.4f}               │ {f1_xgb:.4f}               │
│ Recall                      │ {recall_iso:.4f}               │ {recall_rf:.4f}               │ {recall_xgb:.4f}               │
│ Précision                   │ {prec_iso:.4f}               │ {prec_rf:.4f}               │ {prec_xgb:.4f}               │
│ AUC-PR                      │ {pr_auc_iso:.4f}               │ {pr_auc_rf:.4f}               │ {pr_auc_xgb:.4f}               │
│ Temps entraînement          │ {t_train_iso:.2f}s             │ {t_train_rf:.2f}s             │ {t_train_xgb:.2f}s             │
│ Latence (ms/transaction)    │ {latency_iso:.3f}              │ {latency_rf:.3f}              │ {latency_xgb:.3f}              │
└─────────────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
""")

# Matrice de confusion XGBoost (format tableau pour le mémoire)
TN, FP, FN, TP = cm_xgb.ravel()
print(f"Matrice de confusion — XGBoost (seuil=0.5) :")
print(f"   Vrais Négatifs (VN)  : {TN:,} ({TN/(TN+FP)*100:.2f}%)")
print(f"   Faux Positifs (FP)   : {FP:,} ({FP/(TN+FP)*100:.2f}%)")
print(f"   Faux Négatifs (FN)   : {FN:,} ({FN/(TP+FN)*100:.2f}%)")
print(f"   Vrais Positifs (VP)  : {TP:,} ({TP/(TP+FN)*100:.2f}%)")

# ─────────────────────────────────────────────────────
# CELLULE 12 — Sauvegarde des résultats dans Colab
# ─────────────────────────────────────────────────────

print("\n💾 Sauvegarde des résultats...")
import zipfile as zf
files_to_zip = [
    'benchmark_resultats.csv', 'benchmark_table.tex',
    'eda_distribution_target.png', 'eda_montant.png', 'eda_temporel.png', 'eda_correlations.png',
    'benchmark_comparatif.png', 'matrices_confusion.png', 'courbe_precision_recall.png',
    'shap_importance_globale.png', 'shap_summary.png', 'shap_top10_variables.csv',
    'shap_force_plot_individuel.png', 'shap_waterfall.png'
]
existing_files = [f for f in files_to_zip if os.path.exists(f)]
with zf.ZipFile('FRAUDX_resultats.zip', 'w') as z:
    for f in existing_files:
        z.write(f)
print(f"✅ FRAUDX_resultats.zip créé ({len(existing_files)} fichiers).")

# Téléchargement (décommente pour télécharger automatiquement)
# from google.colab import files
# files.download('FRAUDX_resultats.zip')

print("\n🎯 Pipeline terminé avec succès !")
print("   Télécharge FRAUDX_resultats.zip depuis l'explorateur de fichiers Colab.")
