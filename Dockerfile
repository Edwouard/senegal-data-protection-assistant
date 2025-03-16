# Image de base : Python 3.9 pour une bonne compatibilité avec les bibliothèques
FROM python:3.9-slim

# Définition des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    LANG=fr_FR.UTF-8 \
    LANGUAGE=fr_FR.UTF-8 \
    LC_ALL=fr_FR.UTF-8

# Mise à jour du système et installation des dépendances nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    locales \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création des répertoires de données s'ils n'existent pas
RUN mkdir -p data/raw data/processed data/index

# Exposition des ports pour l'API FastAPI et l'interface Gradio
EXPOSE 8000 7860

# Vérification de l'existence d'un modèle indexé au démarrage
# Si aucun index n'existe, il faudra exécuter les scripts d'importation et d'indexation manuellement
RUN if [ ! -f "data/index/faiss_index.bin" ]; then \
    echo "Aucun index trouvé. Vous devrez exécuter les scripts d'importation et d'indexation."; \
    fi

# Script de démarrage
CMD ["python", "run.py"]