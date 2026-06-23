#!/usr/bin/env python3
"""
FRAUDX CLI — Point d'entrée unique pour toutes les commandes.

Usage:
    fraudx train [--fast]
    fraudx api [--port 8000]
    fraudx dashboard [--port 8501]
    fraudx simulate [--transactions 50]
    fraudx retrain [--min-samples 500]
    fraudx test
"""
import argparse
import sys
import subprocess
import os


def cmd_train(args):
    from train import main as train_main
    sys.argv = ["train.py"]
    if args.fast:
        sys.argv.append("--fast")
    if args.dataset:
        sys.argv.extend(["--dataset", args.dataset])
    train_main()


def cmd_api(args):
    host = args.host or os.environ.get("API_HOST", "0.0.0.0")
    port = args.port or int(os.environ.get("API_PORT", "8000"))
    print(f"🚀 Lancement de l'API sur {host}:{port}")
    os.execvp("uvicorn", ["uvicorn", "src.api:app", "--host", host, "--port", str(port), "--reload"])


def cmd_dashboard(args):
    port = args.port or int(os.environ.get("DASHBOARD_PORT", "8501"))
    print(f"📊 Lancement du dashboard sur :{port}")
    os.execvp("streamlit", ["streamlit", "run", "app.py", "--server.port", str(port)])


def cmd_simulate(args):
    from simulate_stream import main as sim_main
    sys.argv = ["simulate_stream.py"]
    sys.argv.extend(["--transactions", str(args.transactions)])
    sys.argv.extend(["--delay", str(args.delay)])
    sys.argv.extend(["--api", args.api])
    sim_main()


def cmd_retrain(args):
    from retrain import retrain
    result = retrain(min_samples=args.min_samples, dry_run=args.dry_run)
    print(result)


def cmd_test(args):
    import pytest
    test_args = ["tests/", "-v", "--tb=short"]
    if args.e2e:
        test_args = ["-m", ""]
        subprocess.run([sys.executable, "-m", "tests.test_e2e"], check=True)
    else:
        sys.exit(pytest.main(test_args))


def main():
    parser = argparse.ArgumentParser(
        description="FRAUDX — Détection de fraude bancaire par IA (Togo)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  fraudx train --fast
  fraudx api
  fraudx dashboard
  fraudx simulate --transactions 100
  fraudx test
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # train
    p_train = subparsers.add_parser("train", help="Entraîner les modèles")
    p_train.add_argument("--fast", action="store_true", help="Mode rapide")
    p_train.add_argument("--dataset", choices=["ieee", "credit-card"], default="ieee")
    p_train.set_defaults(func=cmd_train)

    # api
    p_api = subparsers.add_parser("api", help="Lancer l'API")
    p_api.add_argument("--host", default=None, help="Hôte (défaut: 0.0.0.0)")
    p_api.add_argument("--port", type=int, default=None, help="Port (défaut: 8000)")
    p_api.set_defaults(func=cmd_api)

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Lancer le dashboard Streamlit")
    p_dash.add_argument("--port", type=int, default=None, help="Port (défaut: 8501)")
    p_dash.set_defaults(func=cmd_dashboard)

    # simulate
    p_sim = subparsers.add_parser("simulate", help="Simuler un flux de transactions")
    p_sim.add_argument("--transactions", type=int, default=50, help="Nombre de transactions")
    p_sim.add_argument("--delay", type=float, default=0.5, help="Délai entre envois (s)")
    p_sim.add_argument("--api", default="http://localhost:8000", help="URL de l'API")
    p_sim.set_defaults(func=cmd_simulate)

    # retrain
    p_ret = subparsers.add_parser("retrain", help="Réentraîner le modèle")
    p_ret.add_argument("--min-samples", type=int, default=500, help="Échantillons minimum")
    p_ret.add_argument("--dry-run", action="store_true", help="Simulation")
    p_ret.set_defaults(func=cmd_retrain)

    # test
    p_test = subparsers.add_parser("test", help="Lancer les tests")
    p_test.add_argument("--e2e", action="store_true", help="Tests de bout en bout")
    p_test.set_defaults(func=cmd_test)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
