# FRAUDX — Makefile
# Commandes courantes pour le développement et la production

.PHONY: help install train api dashboard simulate test lint clean docker-build docker-up

help:
	@echo "╔══════════════════════════════════════════╗"
	@echo "║         FRAUDX — Commandes               ║"
	@echo "╠══════════════════════════════════════════╣"
	@echo "║ make install     → Installer les dépendances  ║"
	@echo "║ make train       → Entraîner les modèles       ║"
	@echo "║ make train-fast  → Entraînement rapide         ║"
	@echo "║ make api         → Lancer l'API                ║"
	@echo "║ make dashboard   → Lancer le dashboard         ║"
	@echo "║ make simulate    → Simuler un flux             ║"
	@echo "║ make test        → Lancer les tests            ║"
	@echo "║ make test-e2e    → Tests de bout en bout       ║"
	@echo "║ make lint        → Vérifier le code            ║"
	@echo "║ make clean       → Nettoyer fichiers temporaires ║"
	@echo "║ make docker-build → Builder l'image Docker     ║"
	@echo "║ make docker-up   → Lancer avec Docker          ║"
	@echo "╚══════════════════════════════════════════╝"

install:
	pip install -e .
	pip install -r config/requirements.txt

train:
	python train.py

train-fast:
	python train.py --fast

api:
	uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

dashboard:
	streamlit run app_streamlit.py --server.port 8501

simulate:
	python simulate_stream.py --transactions 50 --delay 0.5

test:
	pytest tests/ -v --tb=short

test-e2e:
	python -m tests.test_e2e

lint:
	@echo "Vérification du code..."
	@python -c "import py_compile; import sys; files=__import__('glob').glob('**/*.py', recursive=True); [print(f'  OK {f}') or py_compile.compile(f, doraise=True) for f in files]"
	@echo "✅ Syntaxe OK"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	@echo "✅ Nettoyé"

docker-build:
	docker-compose build

docker-up:
	docker-compose up api dashboard
