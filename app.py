import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.models import ChatRequest, ChatResponse
from modules.vectorizer import Vectorizer
from modules.retriever import Retriever
from modules.generator import generate_response
from config import (
    INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL,
    TOP_K_RESULTS,
    GEMINI_API_KEY,
)

# Variables globales pour les services
vectorizer = None
retriever = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation: code exécuté au démarrage de l'application
    global vectorizer, retriever

    # Vérification de l'existence de l'index
    if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
        raise RuntimeError(
            "L'index FAISS n'a pas été trouvé. Veuillez exécuter le script d'indexation d'abord."
        )

    # Initialisation du vectorizer et du retriever
    vectorizer = Vectorizer(model_name=EMBEDDING_MODEL)
    retriever = Retriever()
    retriever.load_index(INDEX_PATH, METADATA_PATH)

    print("Services initialisés avec succès")

    yield  # Ceci est où l'application s'exécute

    # Nettoyage: code exécuté à l'arrêt de l'application
    print("Arrêt des services...")
    # Libérer les ressources si nécessaire
    # Par exemple: fermer les connexions, libérer la mémoire, etc.


# Initialisation de l'API FastAPI avec le gestionnaire de lifespan
app = FastAPI(
    title="Chatbot RAG API",
    description="API pour un chatbot sur la loi sénégalaise de protection des données personnelles",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint de base"""
    return {
        "message": "Bienvenue sur l'API du chatbot RAG pour la loi sur la protection des données personnelles"
    }


@app.get("/health")
async def health_check():
    """Vérification de l'état du service"""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal pour les requêtes de chat"""
    try:
        # Vectorisation de la requête
        query_embedding = vectorizer.vectorize_query(request.message)

        # Récupération des passages pertinents
        retrieved_chunks = retriever.retrieve_relevant_chunks(
            query_embedding, top_k=TOP_K_RESULTS
        )

        HORS_SUJET_RESPONSE = """
        Je suis un assistant spécialisé dans la loi sénégalaise sur la protection des données personnelles (Loi n° 2008-12 du 25 janvier 2008).

        Votre question ne semble pas porter sur ce sujet. Je peux vous aider avec des questions comme :
        - "Qu'est-ce que la CDP et quelles sont ses missions ?",
        - Quels sont les droits des personnes concernées par un traitement de données ?
        - Comment la Commission des Données Personnelles (CDP) est-elle organisée ?
        - Quelles sont les formalités préalables à un traitement de données ?
        - Quelles sont les obligations de sécurité pour un responsable de traitement ?
        - Comment les transferts internationaux de données sont-ils encadrés au Sénégal ?

        Je vous invite à poser question en lien avec cette législation.
        """

        # Message pour les questions pertinentes sans réponse
        PERTINENT_SANS_REPONSE = """
        Votre question sur la protection des données personnelles au Sénégal est pertinente, mais je ne dispose pas d'informations suffisantes dans ma base de connaissances pour y répondre avec précision.

        La loi n° 2008-12 du 25 janvier 2008 comporte de nombreuses dispositions, et il est possible que votre question concerne :
        - Des aspects spécifiques non couverts par ma base documentaire actuelle
        - Des détails d'application pratique de la loi
        - Des modifications législatives récentes
        - Des interprétations jurisprudentielles particulières

        Puis-je vous suggérer de :
        1. Reformuler votre question différemment
        2. Me demander des informations sur un sujet connexe
        3. Consulter directement le site de la Commission des Données Personnelles du Sénégal pour des informations plus spécifiques

        Je reste à votre disposition pour répondre à d'autres questions sur cette législation.
        """

        # Récupérer le meilleur score de similarité
        best_score = retrieved_chunks[0].get("similarity_score", 0)

        # Vérifier si les passages récupérés sont suffisamment pertinents
        # Si le meilleur score de similarité est inférieur à 0.5, considérer qu'aucun passage n'est pertinent
        if not retrieved_chunks or best_score < 0.5:
            return ChatResponse(
                response=HORS_SUJET_RESPONSE,
                sources=[],
            )
        # Si le meilleur score de similarité est inférieur à 0.6, considérer qu'aucun passage n'est pertinent
        if retrieved_chunks[0].get("similarity_score", 0) < 0.6:
            return ChatResponse(
                response=PERTINENT_SANS_REPONSE,
                sources=[],
            )

        # Génération de la réponse
        response_text = generate_response(
            query=request.message,
            retrieved_chunks=retrieved_chunks,
            api_key=GEMINI_API_KEY,
        )

        # Préparation des sources
        sources = []
        for chunk in retrieved_chunks:
            source = {
                "chapitre": chunk["metadata"].get("chapter", ""),
                "section": chunk["metadata"].get("section", ""),
                "article": chunk["metadata"].get("article", ""),
                "score": chunk.get("similarity_score", 0),
                # "relevance": chunk.get("relevance", 0),
            }
            sources.append(source)

        return ChatResponse(response=response_text, sources=sources)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du traitement de la requête: {str(e)}"
        )


# Point d'entrée pour uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
