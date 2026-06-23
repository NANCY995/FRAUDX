#!/usr/bin/env python3
"""
simulate_stream.py — Simule un flux temps réel de transactions vers l'API FRAUDX.

Usage:
    python simulate_stream.py --transactions 100 --delay 0.5 --api http://localhost:8000
"""
import argparse
import numpy as np
import pandas as pd
import requests
import json
import time
import random
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Simule un flux temps réel de transactions")
    parser.add_argument("--transactions", type=int, default=50,
                        help="Nombre de transactions à envoyer")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Délai entre chaque envoi (secondes)")
    parser.add_argument("--api", type=str, default="http://localhost:8000",
                        help="URL de l'API FRAUDX")
    parser.add_argument("--data", type=str, default="data/X_test.csv",
                        help="Fichier CSV contenant les transactions de test")
    return parser.parse_args()


def main():
    args = parse_args()

    # Charger les données de test
    data_path = Path(args.data)
    if data_path.exists():
        df = pd.read_csv(data_path)
        print(f"✅ Données chargées : {len(df)} transactions depuis {args.data}")
    else:
        # Générer des données synthétiques si le fichier n'existe pas
        print(f"⚠️  Fichier {args.data} non trouvé. Génération de données synthétiques...")
        np.random.seed(42)
        n = args.transactions
        df = pd.DataFrame({
            "TransactionAmt": np.random.exponential(1000, n),
            "card1": np.random.randint(1000, 9999, n),
            "card2": np.random.randint(1, 500, n),
            "addr1": np.random.randint(1, 1000, n),
            "addr2": np.random.randint(1, 200, n),
            "hour": np.random.randint(0, 23, n),
            "dayofweek": np.random.randint(0, 6, n),
        })

    # Tester la connexion à l'API
    try:
        r = requests.get(f"{args.api}/health", timeout=3)
        print(f"✅ API connectée : {r.json()}")
    except requests.exceptions.ConnectionError:
        print(f"❌ API inaccessible sur {args.api}")
        print(f"   Lance d'abord : uvicorn src.api:app --reload")
        return

    # Envoyer les transactions
    print(f"\n🚀 Simulation de {min(args.transactions, len(df))} transactions...\n")

    stats = {"total": 0, "fraude": 0, "erreur": 0}

    for i in range(min(args.transactions, len(df))):
        tx = df.iloc[i].dropna().to_dict()
        tx = {k: float(v) if isinstance(v, (int, float)) else v for k, v in tx.items()}

        try:
            r = requests.post(f"{args.api}/predict", json=tx, timeout=5)
            stats["total"] += 1

            if r.status_code == 200:
                result = r.json()
                is_fraud = result["prediction"] == "FRAUDE"
                risk = result["risk_level"]

                if is_fraud:
                    stats["fraude"] += 1
                    print(f"⚠️  #{i+1} FRAUDE  | score={result['fraud_score']:.3f} | risque={risk:8s} | "
                          f"top1={result['top_features'][0]['feature']}")
                else:
                    print(f"✓ #{i+1} NORMALE | score={result['fraud_score']:.3f} | risque={risk:8s}")
            else:
                stats["erreur"] += 1
                print(f"✗ #{i+1} ERREUR {r.status_code} : {r.text[:80]}")

        except requests.exceptions.RequestException as e:
            stats["erreur"] += 1
            print(f"✗ #{i+1} ERREUR CONNEXION : {e}")

        # Délai aléatoire pour simuler un flux réel
        time.sleep(args.delay * random.uniform(0.5, 1.5))

    # Résumé
    print(f"\n{'='*50}")
    print(f"📊 RÉSULTATS DE LA SIMULATION")
    print(f"{'='*50}")
    print(f"Total envoyé  : {stats['total']}")
    print(f"Fraudes       : {stats['fraude']} ({stats['fraude']/max(stats['total'],1)*100:.1f}%)")
    print(f"Erreurs       : {stats['erreur']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
