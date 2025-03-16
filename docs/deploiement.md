# Guide de Déploiement

<div align="center">
  
![Chatbot-RAG](https://img.shields.io/badge/Chatbot-RAG-blue?style=for-the-badge&logo=docker&logoColor=white)

**Guide de Déploiement et d'Administration**

*Déployer, maintenir et superviser l'assistant juridique dans différents environnements*

</div>

## Table des Matières

1. [Prérequis](#prérequis)
2. [Déploiement Local](#déploiement-local)
3. [Déploiement avec Docker](#déploiement-avec-docker)


## Prérequis

### Matériel Recommandé

- **CPU** : 4 cœurs minimum, 8 cœurs recommandés
- **RAM** : 8 Go minimum, 16 Go recommandés
- **Stockage** : 1 Go pour l'application, plus selon la taille du corpus juridique
- **GPU** : Optionnel mais recommandé pour les grands corpus (améliore les performances de FAISS)

### Logiciels Requis

- **Python** : Version 3.8 ou supérieure
- **pip** : Gestionnaire de paquets Python à jour
- **Docker** (optionnel) : Version 20.10 ou supérieure si déploiement conteneurisé
- **Git** : Pour récupérer le code source (optionnel)
- **Clé API Gemini** : Nécessaire pour le service de génération de texte

## Déploiement Local

### Installation des Dépendances

1. Clonez le dépôt (ou téléchargez l'archive) :
   ```bash
   git clone https://github.com/votre-nom/chatbot-rag.git
   cd chatbot-rag
   ```

2. Créez un environnement virtuel Python (recommandé) :
   ```bash
   python -m venv venv
   
   # Activation sur Windows
   venv\Scripts\activate
   
   # Activation sur Linux/MacOS
   source venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration Initiale

1. Créez un fichier `.env` à la racine du projet avec votre clé API :
   ```
   GEMINI_API_KEY=votre_clé_api_gemini
   ```

2. Vérifiez les paramètres dans `config.py` et ajustez-les si nécessaire.

### Importation et Indexation des Documents

1. Placez vos documents PDF dans le dossier `data/raw/` ou importez-les directement :
   ```bash
   python import_documents.py --pdf chemin/vers/votre/document.pdf
   ```

2. Créez l'index vectoriel :
   ```bash
   python indexer.py
   ```

### Lancement de l'Application

1. Démarrez l'application complète (API + Interface) :
   ```bash
   python run.py
   ```

2. Accédez à l'application :
   - Interface utilisateur : http://localhost:7860
   - API : http://localhost:8000
   - Documentation API : http://localhost:8000/docs

## Déploiement avec Docker

### Construction de l'Image

1. Construisez l'image Docker :
   ```bash
   docker build -t votre_nom_utilisateur/chatbot-rag .
   ```

### Exécution du Conteneur

1. Exécutez le conteneur avec les paramètres appropriés :
   ```bash
   docker run -d --name chatbot-rag \
     -p 8000:8000 \
     -p 7860:7860 \
     -e GEMINI_API_KEY=votre_clé_api \
     -v $(pwd)/data:/app/data \
     votre_nom_utilisateur/chatbot-rag
   ```

2. Vérifiez que le conteneur fonctionne correctement :
   ```bash
   docker logs chatbot-rag
   ```

### Utilisation avec Docker Compose

1. Créez un fichier `docker-compose.yml` :
   ```yaml
   version: '3'
   
   services:
     chatbot-rag:
       build: .
       ports:
         - "8000:8000"
         - "7860:7860"
       environment:
         - GEMINI_API_KEY=votre_clé_api
       volumes:
         - ./data:/app/data
       restart: unless-stopped
   ```

2. Lancez avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

