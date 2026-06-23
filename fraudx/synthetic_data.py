"""
Générateur de données synthétiques de transactions mobile money Togo.
Permet de tester le modèle sur des données plus proches du contexte togolais.

Usage:
    from fraudx.synthetic_data import generate_togo_dataset
    df = generate_togo_dataset(n_transactions=5000)
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional


# Canaux mobile money au Togo
CANAUX = ["USSD", "APP", "AGENT", "WEB"]

# Opérateurs mobile money Togo
OPERATEURS_MM = ["TogoCom Cash", "Moov Money", "Flooz"]

# Types d'opérations mobile money
TYPES_OPERATION = ["RECHARGE", "TRANSFERT", "PAIEMENT", "RETRAIT", "WITHDRAWAL"]

# Banques togolaises
BANQUES = ["BTCI", "Orabank", "UTB", "Ecobank", "SGBT", "BSIC"]

# Villes togolaises
VILLES = ["Lomé", "Sokodé", "Kara", "Kpalimé", "Atakpamé", "Dapaong", "Tsévié"]

# Plages horaires typiques mobile money (pics 8h-10h et 17h-19h)
HEURES_PICS = list(range(8, 11)) + list(range(17, 20))
HEURES_CREUSES = list(range(0, 6))
HEURES_NORMALES = [h for h in range(24) if h not in HEURES_PICS and h not in HEURES_CREUSES]


def _random_hour(pic_prob: float = 0.4) -> int:
    """Heure aléatoire avec pics aux heures d'affluence."""
    r = np.random.random()
    if r < pic_prob:
        return int(np.random.choice(HEURES_PICS))
    elif r < pic_prob + 0.1:
        return int(np.random.choice(HEURES_CREUSES))
    else:
        return int(np.random.choice(HEURES_NORMALES))


def _random_montant(canal: str, operation: str) -> float:
    """Montant réaliste selon le canal et le type d'opération."""
    if operation == "RECHARGE":
        return round(np.random.lognormal(mean=7.5, sigma=0.8), 0)  # ~1800 FCFA médian
    elif operation == "TRANSFERT":
        return round(np.random.lognormal(mean=9.0, sigma=1.0), 0)  # ~8000 FCFA médian
    elif operation == "PAIEMENT":
        return round(np.random.lognormal(mean=8.5, sigma=1.2), 0)  # ~5000 FCFA médian
    elif operation == "RETRAIT":
        return round(np.random.lognormal(mean=9.5, sigma=0.9), 0)  # ~13000 FCFA médian
    else:
        return round(np.random.lognormal(mean=8.0, sigma=1.5), 0)


def _generate_fraud_rules(row: dict, fraud_patterns: list) -> bool:
    """Applique des règles de fraude réalistes pour le Togo."""
    # SIM swap : changement d'appareil récent + montant élevé
    if "SIM swap" in fraud_patterns:
        if (row.get("device_change_days", 999) <= 1 and
            row.get("montant_cfa", 0) > 30000 and
            row.get("canal") in ["USSD", "APP"]):
            return True

    # Transaction inhabituelle : heure creuse + montant élevé + nouveau bénéficiaire
    if "transaction_inhabituelle" in fraud_patterns:
        if (row.get("hour", 12) in HEURES_CREUSES and
            row.get("montant_cfa", 0) > 50000):
            return True

    # Cascade de transferts : 3+ transactions en <30 min
    if "cascade" in fraud_patterns:
        if (row.get("tx_last_30min", 0) >= 3 and
            row.get("montant_cfa", 0) > 20000):
            return True

    # Agent frauduleux : montant ronde + même agent pour plusieurs comptes
    if "agent_frauduleux" in fraud_patterns:
        if (row.get("canal") == "AGENT" and
            row.get("montant_cfa", 0) % 10000 == 0 and
            row.get("montant_cfa", 0) > 100000):
            return True

    # Usurpation : tentative de connexion depuis un nouvel appareil
    if "usurpation" in fraud_patterns:
        if (row.get("device_change_days", 999) == 0 and
            row.get("montant_cfa", 0) > 100000):
            return True

    return False


def generate_togo_dataset(n_transactions: int = 5000,
                          fraud_rate: float = 0.035,
                          seed: int = 42) -> pd.DataFrame:
    """
    Génère un dataset synthétique de transactions mobile money Togo.

    Paramètres
    ----------
    n_transactions : int
        Nombre de transactions à générer (défaut: 5000)
    fraud_rate : float
        Taux de fraude cible (défaut: 0.035 soit 3.5%)
    seed : int
        Seed aléatoire pour reproductibilité

    Retour
    ------
    pd.DataFrame avec les colonnes correspondant au contexte togolais
    """
    np.random.seed(seed)
    rng = np.random.default_rng(seed)

    print(f"🇹🇬 Génération de {n_transactions} transactions mobile money Togo...")
    print(f"   Taux de fraude cible : {fraud_rate*100:.1f}%")

    # Profils utilisateurs (SIMs)
    n_users = n_transactions // 10
    users = {
        f"SIM_{i:06d}": {
            "ville": rng.choice(VILLES),
            "operateur": rng.choice(OPERATEURS_MM),
            "age_compte_jours": int(rng.exponential(365)),
            "tx_moyen": round(rng.lognormal(mean=8.5, sigma=0.8), 0)
        }
        for i in range(n_users)
    }

    params = {
        "ville": rng.choice(VILLES),
        "operateur": rng.choice(OPERATEURS_MM),
        "age_compte_jours": int(rng.exponential(365)),
        "tx_moyen": round(rng.lognormal(mean=8.5, sigma=0.8), 0)
    }

    transactions = []
    fraud_count = 0

    for i in range(n_transactions):
        user_id = f"SIM_{rng.integers(0, n_users):06d}"
        canal = rng.choice(CANAUX, p=[0.35, 0.30, 0.25, 0.10])
        operation = rng.choice(TYPES_OPERATION)
        montant = _random_montant(canal, operation)
        hour = _random_hour()
        dayofweek = rng.integers(0, 7)
        device_change = max(0, int(rng.exponential(90)))

        tx = {
            "transaction_id": f"TG_{i:06d}",
            "user_id": user_id,
            "montant_cfa": montant,
            "canal": canal,
            "type_operation": operation,
            "operateur": rng.choice(OPERATEURS_MM),
            "ville": rng.choice(VILLES),
            "agent_id": f"AGT_{rng.integers(0, 500):04d}" if canal == "AGENT" else None,
            "hour": hour,
            "dayofweek": dayofweek,
            "device_change_days": device_change,
            "tx_last_30min": int(rng.poisson(0.5)),
            "age_compte_jours": rng.integers(1, 2000),
            "timestamp": datetime(2024, 1, 1) + timedelta(
                days=int(rng.integers(0, 365)),
                hours=int(hour),
                minutes=int(rng.integers(0, 59))
            )
        }

        # Générer les transactions frauduleuses
        if rng.random() < fraud_rate:
            fraud_patterns = rng.choice(
                ["SIM swap", "transaction_inhabituelle", "cascade",
                 "agent_frauduleux", "usurpation"],
                size=rng.integers(1, 3), replace=False
            )
            tx["isFraud"] = int(_generate_fraud_rules(tx, fraud_patterns))
            tx["fraud_type"] = ", ".join(fraud_patterns) if tx["isFraud"] else None
        else:
            tx["isFraud"] = 0
            tx["fraud_type"] = None

        fraud_count += tx["isFraud"]
        transactions.append(tx)

    df = pd.DataFrame(transactions)

    # Recalculer le taux de fraude effectif
    actual_fraud_rate = df["isFraud"].mean()
    print(f"   Transactions générées : {len(df)}")
    print(f"   Taux de fraude effectif : {actual_fraud_rate*100:.2f}%")
    print(f"   Fraudes SIM swap : {((df['fraud_type'] if df['fraud_type'] is not None else '').str.contains('SIM swap')).sum()}")
    print(f"   Cannaux : {df['canal'].value_counts().to_dict()}")
    print(f"   Opérateurs : {df['operateur'].value_counts().to_dict()}")

    return df


def generate_togo_dataset_ieee_compatible(n_transactions: int = 5000,
                                           fraud_rate: float = 0.035,
                                           seed: int = 42) -> pd.DataFrame:
    """
    Génère un dataset synthétique Togo avec des noms de colonnes compatibles IEEE-CIS
    pour tester directement le modèle pré-entraîné.
    """
    df_mm = generate_togo_dataset(n_transactions, fraud_rate, seed)

    # Mapping des colonnes mobile money → IEEE-CIS
    mapping = {
        "montant_cfa": "TransactionAmt",
        "ville": "addr1",
        "operateur": "card4",
        "canal": "ProductCD",
        "device_change_days": "D1",
        "tx_last_30min": "C1",
        "age_compte_jours": "D2",
        "hour": "hour",
        "dayofweek": "dayofweek"
    }

    df_ieee = df_mm.rename(columns=mapping)
    df_ieee["TransactionDT"] = df_ieee["timestamp"].apply(
        lambda x: int((x - datetime(2017, 12, 1)).total_seconds())
    )

    # Garder les colonnes pertinentes pour le modèle
    keep_cols = list(mapping.values()) + ["TransactionDT", "isFraud"]
    df_ieee = df_ieee[[c for c in keep_cols if c in df_ieee.columns]]

    print(f"✅ Dataset compatible IEEE-CIS : {df_ieee.shape}")
    return df_ieee


if __name__ == "__main__":
    df = generate_togo_dataset(1000)
    print(f"\nAperçu :")
    print(df.head())
    print(f"\nColonnes : {df.columns.tolist()}")
