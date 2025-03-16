import os
from typing import List, Dict, Any
import google.generativeai as genai


def generate_response(
    query: str, retrieved_chunks: List[Dict[Any, Any]], api_key: str = None
) -> str:
    """
    Génère une réponse à la requête de l'utilisateur en utilisant les chunks récupérés comme contexte.
    Fonction adaptée depuis la base de connaissance fournie.

    Args:
        query: La question posée par l'utilisateur
        retrieved_chunks: Liste des chunks pertinents récupérés par le retriever
        api_key: Clé API pour Gemini (peut être définie comme variable d'environnement)

    Returns:
        str: Réponse générée
    """
    try:
        # Configuration de l'API Gemini
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Aucune clé API Gemini fournie. Utilisez le paramètre api_key ou définissez la variable d'environnement GEMINI_API_KEY."
            )

        genai.configure(api_key=api_key)

        # Sélection du modèle
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={
                "temperature": 0.2,  # Valeur basse pour favoriser la précision et la cohérence
                "top_p": 0.95,  # Contrôle la diversité de manière plus fine que la température
                "top_k": 40,  # Limite le nombre de tokens considérés à chaque étape
                "max_output_tokens": 2048,  # Longueur maximale de la réponse générée
                "presence_penalty": 0.2,  # Pénalise légèrement la répétition de contenu
            },
        )

        # Construction du contexte à partir des chunks récupérés
        context = ""
        for i, chunk in enumerate(retrieved_chunks):
            # Extraction des métadonnées pertinentes
            chapter = chunk["metadata"].get("chapter", "Chapitre non spécifié")
            section = chunk["metadata"].get("section", "Section non spécifiée")
            article = chunk["metadata"].get("article", "Article non spécifié")

            # Ajouter le chunk au contexte avec ses références
            context += f"Référence {i+1}: {chapter} | {section} | {article}\n"
            context += f"{chunk['text']}\n\n"

        # Construction du prompt pour le modèle
        prompt = f"""
        # Contexte
        Vous êtes en train d'assister un utilisateur qui recherche des informations sur la loi sénégalaise sur la protection des données personnelles. L'utilisateur a posé la question suivante: "{query}"
        
        Voici les extraits pertinents de la loi:
        {context}
        
        # Rôle
        Vous êtes un expert juridique spécialisé dans le droit numérique sénégalais et particulièrement dans l'application de la loi sur la protection des données personnelles. Votre mission est de fournir des réponses précises et fondées sur les textes légaux.
        
        # Instruction
        Analysez les extraits fournis et formulez une réponse complète qui:
        1. Répond directement à la question posée
        2. Cite explicitement les articles pertinents (numéro et contenu)
        3. Explique les implications pratiques pour les personnes concernées
        4. Structure l'information de manière claire avec des sous-titres si nécessaire
        
        # Spécificité
        Utilisez uniquement les informations présentes dans les extraits fournis. Si la question nécessite des informations non présentes dans les extraits, indiquez clairement les limites de votre réponse et suggérez d'autres articles qui pourraient être consultés.
        
        # Personnalité
        Adoptez un ton professionnel mais accessible, évitez le jargon juridique excessif et expliquez les termes techniques. Soyez précis et factuel.
        
        # Évaluation
        Une bonne réponse sera évaluée sur sa précision juridique, sa clarté d'explication et sa pertinence par rapport à la question posée.
        
        ## Réponse:
        """

        # Génération de la réponse
        response = model.generate_content(prompt)

        # Nettoyage et formatage de la réponse
        answer = response.text.strip()

        return answer

    except Exception as e:
        # Gestion des erreurs
        error_message = (
            f"Une erreur s'est produite lors de la génération de la réponse: {str(e)}"
        )
        print(error_message)
        return "Je suis désolé, je ne peux pas générer une réponse en ce moment en raison d'une erreur technique."
