FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Création des dossiers nécessaires
RUN mkdir -p data models docs/mockups

# Exposition du port API
EXPOSE 8000
EXPOSE 8501

# Commande par défaut : API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
