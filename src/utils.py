import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


def load_and_merge_ieee(transaction_path, identity_path=None):
    df = pd.read_csv(transaction_path)
    if identity_path:
        identity = pd.read_csv(identity_path)
        df = df.merge(identity, on="TransactionID", how="left")
    return df


def basic_exploration(df):
    print(f"Dimensions : {df.shape}")
    print(f"Mémoire : {df.memory_usage(deep=True).sum() / 1024**2:.2f} Mo")
    print(f"Taux de fraude : {df['isFraud'].mean()*100:.2f}%")
    print(f"Colonnes numériques : {df.select_dtypes(include=np.number).shape[1]}")
    print(f"Colonnes catégorielles : {df.select_dtypes(include='object').shape[1]}")


def plot_fraud_distribution(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(1, 2, figsize=(10, 4))
    counts = df['isFraud'].value_counts()
    ax[0].bar(['Non fraude (0)', 'Fraude (1)'], counts.values, color=['steelblue', 'crimson'])
    ax[0].set_ylabel('Nombre de transactions')
    ax[0].set_title('Distribution des classes')
    for i, v in enumerate(counts.values):
        ax[0].text(i, v + 500, f'{v:,}', ha='center', fontsize=10)
    ax[1].pie(counts.values, labels=['Non fraude', 'Fraude'], autopct='%1.1f%%',
              colors=['steelblue', 'crimson'], startangle=90)
    ax[1].set_title('Proportion')
    plt.tight_layout()


def plot_missing_rate(df, threshold=90, ax=None):
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    high_missing = missing[missing > threshold]
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 4))
    ax.barh(range(len(high_missing)), high_missing.values, color='salmon')
    ax.set_yticks(range(len(high_missing)))
    ax.set_yticklabels(high_missing.index, fontsize=8)
    ax.axvline(threshold, color='red', linestyle='--', label=f'Seuil {threshold}%')
    ax.set_xlabel('Taux de valeurs manquantes (%)')
    ax.set_title(f'Colonnes avec plus de {threshold}% de NaN')
    ax.legend()
    plt.tight_layout()
    return high_missing


def drop_high_missing(df, threshold=90):
    missing = (df.isnull().sum() / len(df) * 100)
    cols_to_drop = missing[missing > threshold].index.tolist()
    df_clean = df.drop(columns=cols_to_drop)
    print(f"Supprimé : {len(cols_to_drop)} colonnes (> {threshold}% NaN)")
    return df_clean, cols_to_drop


def plot_amount_by_fraud(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(1, 2, figsize=(12, 4))
    df_pos = df[df['isFraud'] == 1]['TransactionAmt']
    df_neg = df[df['isFraud'] == 0]['TransactionAmt']
    ax[0].hist(np.log1p(df_neg), bins=80, alpha=0.6, label='Non fraude', color='steelblue')
    ax[0].hist(np.log1p(df_pos), bins=80, alpha=0.6, label='Fraude', color='crimson')
    ax[0].set_xlabel('log(TransactionAmt + 1)')
    ax[0].set_ylabel('Fréquence')
    ax[0].set_title('Distribution du montant (log)')
    ax[0].legend()
    ax[1].boxplot([df_neg, df_pos], labels=['Non fraude', 'Fraude'], widths=0.5)
    ax[1].set_ylabel('Montant')
    ax[1].set_title('Boxplot par classe')
    plt.tight_layout()


def split_and_scale(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    print(f"Train : {X_train.shape}, Test : {X_test.shape}")
    print(f"Fraude Train : {y_train.mean()*100:.2f}%, Fraude Test : {y_test.mean()*100:.2f}%")
    return X_train, X_test, y_train, y_test


def apply_smote(X_train, y_train, random_state=42):
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"Avant SMOTE : Fraude = {y_train.sum()}, Non fraude = {(y_train == 0).sum()}")
    print(f"Après SMOTE : Fraude = {y_res.sum()}, Non fraude = {(y_res == 0).sum()}")
    return X_res, y_res


def save_model(model, scaler, encoders, path="models_optuna/"):
    joblib.dump(model, f"{path}xgb_model.pkl")
    joblib.dump(scaler, f"{path}scaler.pkl")
    joblib.dump(encoders, f"{path}encoders.pkl")
    print(f"Modèle sauvegardé dans {path}")


def load_saved_model(path="models_optuna/"):
    model = joblib.load(f"{path}xgb_model.pkl")
    scaler = joblib.load(f"{path}scaler.pkl")
    encoders = joblib.load(f"{path}encoders.pkl")
    return model, scaler, encoders
