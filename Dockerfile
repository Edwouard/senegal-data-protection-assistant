FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances de compilation pour FAISS et SentenceTransformers
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source avec la nouvelle structure
COPY app.py config.py interface.py run.py ./
COPY modules/ ./modules/
COPY tools/ ./tools/
COPY static/ ./static/

# Création des répertoires nécessaires
RUN mkdir -p data/raw data/processed data/index

# Variables d'environnement
ENV API_URL=http://localhost:8000
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Commande par défaut pour lancer l'application complète
CMD ["python", "run.py", "--api-port", "8000", "--ui-port", "7860", "--no-open"]

# Exposition des ports pour l'API et l'interface
EXPOSE 8000 7860