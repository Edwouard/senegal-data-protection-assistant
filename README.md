# Chatbot-RAG : Assistant juridique pour la loi sénégalaise sur la protection des données personnelles

<div align="center">
  
![Logo du Chatbot-RAG](https://img.shields.io/badge/Chatbot-RAG-blue?style=for-the-badge&logo=robot&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-3.35.0-orange.svg)](https://gradio.app/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Licence](https://img.shields.io/badge/Licence-MIT-green.svg)](LICENSE)

</div>

## 📝 Présentation

Le **Chatbot-RAG** est un assistant conversationnel spécialisé dans la législation sénégalaise sur la protection des données personnelles (Loi n° 2008-12 du 25 janvier 2008). Reposant sur l'approche Retrieval-Augmented Generation (RAG), ce chatbot combine recherche sémantique et intelligence artificielle générative pour fournir des réponses précises et contextuelles aux questions juridiques.

### ✨ Caractéristiques principales

- **Recherche sémantique avancée** pour identifier les passages pertinents de la loi
- **Réponses intelligentes** générées par le modèle Gemini d'IA
- **Interface utilisateur intuitive** développée avec Gradio
- **Références des sources** utilisées pour générer les réponses
- **API RESTful** pour une intégration facile dans d'autres applications
- **Architecture modulaire** facilitant l'extension à d'autres domaines juridiques

## 🖼️ Captures d'écran

<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Interface+du+Chatbot-RAG" alt="Interface du Chatbot-RAG" width="800"/>
</div>

## 🚀 Installation et démarrage rapide

### Prérequis

- Python 3.8 ou supérieur
- Clé API Gemini

### Installation avec pip

```bash
# Cloner le dépôt
git clone https://github.com/votre-nom/chatbot-rag.git
cd chatbot-rag

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API Gemini (créez un fichier .env avec votre clé)
echo "GEMINI_API_KEY=votre_clé_api" > .env

# Importer et indexer les documents
python import_documents.py --pdf data/raw/cdp_Loi_2008-12_Protection_des_données_personnelles.pdf
python indexer.py

# Lancer l'application
python run.py
```

L'application sera accessible à l'adresse : 
- Interface utilisateur : http://localhost:7860
- API : http://localhost:8000

### Installation avec Docker

```bash
# Construire l'image Docker
docker build -t votre_nom_utilisateur/chatbot-rag .

# Exécuter le conteneur
docker run -p 8000:8000 -p 7860:7860 -e GEMINI_API_KEY=votre_clé_api votre_nom_utilisateur/chatbot-rag
```

## 💡 Utilisation

1. **Accédez à l'interface** via votre navigateur à l'adresse http://localhost:7860
2. **Posez votre question** sur la loi de protection des données personnelles
3. **Obtenez une réponse précise** avec les références aux articles pertinents

### Exemples de questions

- "Qu'est-ce que la Commission des Données Personnelles (CDP) et quelles sont ses missions ?"
- "Quels sont les droits des personnes concernées par un traitement de données personnelles ?"
- "Dans quels cas peut-on transférer des données personnelles vers un pays tiers ?"
- "Comment sont sanctionnés les manquements à la loi sur la protection des données ?"

## 🔌 API

Le chatbot expose une API RESTful avec les endpoints suivants :

- **GET /** - Page d'accueil de l'API
- **GET /health** - Vérification de l'état du service
- **POST /chat** - Endpoint principal pour les requêtes de chat
  ```json
  // Requête
  {
    "message": "Qu'est-ce que la CDP ?"
  }
  
  // Réponse
  {
    "response": "La Commission des Données Personnelles (CDP) est une autorité administrative indépendante...",
    "sources": [
      {
        "chapitre": "Chapitre II: Commission de protection aux Données à caractère personnelles.",
        "section": "Section première: Statut, composition et organisation.",
        "article": "Article 5",
        "score": 0.92
      }
    ]
  }
  ```

Une documentation interactive de l'API est disponible à l'adresse http://localhost:8000/docs.

## 🧩 Architecture

Le projet est structuré de manière modulaire pour faciliter la maintenance et l'extension :

```
chatbot-rag/
├── app.py                # Point d'entrée principal de l'API FastAPI
├── interface.py          # Interface utilisateur Gradio
├── run.py                # Script pour exécuter l'API et l'interface ensemble
├── config.py             # Configuration et variables d'environnement partagées
├── indexer.py            # Script pour l'indexation des documents
├── import_documents.py   # Script pour l'importation de nouveaux documents PDF
├── modules/              # Modules partagés entre l'API et l'interface
└── data/                 # Données du projet
    ├── raw/              # Documents PDF bruts
    ├── processed/        # Structures extraites et chunks prétraités
    └── index/            # Index vectoriel FAISS
```

### Flux de fonctionnement

1. **Prétraitement** : Les documents juridiques sont importés, traités et segmentés.
2. **Indexation** : Chaque segment est vectorisé et indexé avec FAISS.
3. **Requête** : L'utilisateur pose une question via l'interface.
4. **Récupération** : Les segments les plus pertinents sont identifiés.
5. **Génération** : Une réponse cohérente est générée à partir de ces segments.

## 🛠️ Personnalisation

### Adapter à d'autres domaines juridiques

1. **Importez vos documents** :
   ```bash
   python import_documents.py --pdf votre_document.pdf
   ```

2. **Réindexez la base de connaissances** :
   ```bash
   python indexer.py --force-segmentation
   ```

3. **Ajustez les paramètres de recherche** dans `config.py` :
   ```python
   TOP_K_RESULTS = 5  # Nombre de passages à récupérer
   MAX_CHUNK_SIZE = 1200  # Taille maximale des segments
   ```

### Modifier le modèle d'embeddings

Changez le modèle dans `config.py` :
```python
EMBEDDING_MODEL = "votre_modele_preferé"
```

## 📊 Performance

Le système a été optimisé pour :
- **Précision** : Les réponses sont basées uniquement sur le texte de loi
- **Rapidité** : Le temps de réponse moyen est inférieur à 2 secondes
- **Pertinence** : Les résultats sont classés par score de similarité

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📱 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à contacter l'équipe de développement.

---

<div align="center">
  <p>Développé avec ❤️ pour simplifier l'accès au droit sénégalais</p>
</div>