import gradio as gr
import requests
import json
import os
import tempfile
from datetime import datetime
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration de l'API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Vérification de la version de Gradio
print(f"Gradio version: {gr.__version__}")


def format_sources(sources):
    """Formate les sources pour l'affichage"""
    if not sources:
        return ""

    formatted = "**Sources utilisées:**\n\n"
    for i, source in enumerate(sources):
        # Formatage des informations de source avec Markdown
        chapitre = source.get("chapitre", "").replace("Chapitre", "**Chapitre")
        if ":" in chapitre:
            chapitre = chapitre.replace(":", ":**", 1)
        else:
            chapitre += "**"

        section = source.get("section", "").replace("Section", "_Section")
        if ":" in section:
            section = section.replace(":", ":_", 1)
        else:
            section += "_"

        article = source.get("article", "")
        score = source.get("score", 0)
        score_percent = f"{score*100:.1f}%" if score else ""

        formatted += f"{i+1}. {chapitre} | {section} | {article} ({score_percent})\n"

    return formatted


def convert_to_messages_format(history):
    """Convertit l'historique du format tuples au format messages"""
    messages = []
    for item in history:
        if isinstance(item, dict):
            messages.append(item)
        else:
            user_msg, assistant_msg = item
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
    return messages


def query_chatbot(message, history, progress=gr.Progress()):
    """Fonction qui communique avec l'API du chatbot et met à jour l'historique"""
    try:
        # Afficher le progrès
        progress(0, desc="Envoi de la requête...")

        # Requête à l'API
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"},
        )

        progress(0.5, desc="Traitement de la réponse...")

        # Vérification de la réponse
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "")
            sources = data.get("sources", [])

            # Ajouter les sources formatées à la réponse
            if sources:
                response_text += "\n\n" + format_sources(sources)

            progress(1.0, desc="Terminé!")

            # Convertir l'historique existant au format "messages" si nécessaire
            messages_history = convert_to_messages_format(history)

            # Ajouter le nouveau message et la réponse
            messages_history.append({"role": "user", "content": message})
            messages_history.append({"role": "assistant", "content": response_text})

            return messages_history

        else:
            progress(1.0, desc="Erreur!")
            if response.status_code == 404:
                error_msg = f"⚠️ Erreur: API non disponible. Vérifiez que le serveur est en cours d'exécution."
            elif response.status_code == 500:
                error_msg = f"⚠️ Erreur: Le serveur a rencontré une erreur interne. Veuillez réessayer plus tard."
            else:
                error_msg = f"⚠️ Erreur: Impossible de communiquer avec l'API (Statut: {response.status_code})"

            # Convertir l'historique et ajouter le message d'erreur
            messages_history = convert_to_messages_format(history)
            messages_history.append({"role": "user", "content": message})
            messages_history.append({"role": "assistant", "content": error_msg})

            return messages_history

    except requests.exceptions.ConnectionError:
        progress(1.0, desc="Erreur de connexion!")
        error_msg = f"⚠️ Erreur de connexion: Impossible d'atteindre l'API. Vérifiez l'URL ({API_URL}) et que le serveur est en cours d'exécution."

        # Convertir l'historique et ajouter le message d'erreur
        messages_history = convert_to_messages_format(history)
        messages_history.append({"role": "user", "content": message})
        messages_history.append({"role": "assistant", "content": error_msg})

        return messages_history

    except Exception as e:
        progress(1.0, desc="Erreur!")
        error_msg = f"⚠️ Erreur: {str(e)}"

        # Convertir l'historique et ajouter le message d'erreur
        messages_history = convert_to_messages_format(history)
        messages_history.append({"role": "user", "content": message})
        messages_history.append({"role": "assistant", "content": error_msg})

        return messages_history


def reset_conversation():
    """Réinitialise la conversation"""
    return []


def save_conversation(history, format="md"):
    """
    Enregistre la conversation au format texte et renvoie un fichier téléchargeable

    Args:
        history: Historique de la conversation
        format: Format de sortie (md par défaut)

    Returns:
        Chemin vers le fichier généré
    """
    if not history:
        return None

    # Formatter le contenu selon le format choisi
    if format == "md":
        content = format_conversation_markdown(history)
        extension = "md"
    elif format == "txt":
        content = format_conversation_text(history)
        extension = "txt"
    else:
        # Format par défaut
        content = format_conversation_markdown(history)
        extension = "md"

    # Créer un fichier temporaire avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"conversation_{timestamp}.{extension}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def format_conversation_markdown(history):
    """Formate la conversation au format Markdown"""
    conversation_text = "# Conversation avec l'Assistant Juridique\n\n"
    conversation_text += (
        f"_Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}_\n\n"
    )

    question_count = 0

    for i, message in enumerate(history):
        if isinstance(message, dict):
            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":
                question_count += 1
                conversation_text += f"## Question {question_count}\n\n"
                conversation_text += f"**Utilisateur**: {content}\n\n"
            elif role == "assistant":
                conversation_text += f"**Assistant**: {content}\n\n"
                conversation_text += "---\n\n"
        else:
            # Ancien format (tuples), au cas où
            user_msg, assistant_msg = message
            question_count += 1
            conversation_text += f"## Question {question_count}\n\n"
            conversation_text += f"**Utilisateur**: {user_msg}\n\n"
            conversation_text += f"**Assistant**: {assistant_msg}\n\n"
            conversation_text += "---\n\n"

    # Ajouter des statistiques
    conversation_text += f"\n\n## Statistiques\n\n"
    conversation_text += f"- Nombre total de questions: {question_count}\n"
    conversation_text += f"- Date d'export: {datetime.now().strftime('%d/%m/%Y')}\n"

    return conversation_text


def format_conversation_text(history):
    """Formate la conversation au format texte simple"""
    conversation_text = "CONVERSATION AVEC L'ASSISTANT JURIDIQUE\n"
    conversation_text += (
        f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n"
    )

    question_count = 0

    for i, message in enumerate(history):
        if isinstance(message, dict):
            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":
                question_count += 1
                conversation_text += f"QUESTION {question_count}\n"
                conversation_text += f"Utilisateur: {content}\n\n"
            elif role == "assistant":
                conversation_text += f"Assistant: {content}\n\n"
                conversation_text += "----------------------------------------\n\n"
        else:
            # Ancien format (tuples), au cas où
            user_msg, assistant_msg = message
            question_count += 1
            conversation_text += f"QUESTION {question_count}\n"
            conversation_text += f"Utilisateur: {user_msg}\n\n"
            conversation_text += f"Assistant: {assistant_msg}\n\n"
            conversation_text += "----------------------------------------\n\n"

    return conversation_text


# Configuration de l'interface Gradio avec le thème par défaut
theme = gr.themes.Soft(primary_hue="blue")

with gr.Blocks(theme=theme) as demo:
    # En-tête
    gr.Markdown(
        """
    # Assistant Juridique - Loi sur la Protection des Données Personnelles au Sénégal
    
    Posez vos questions sur la loi sénégalaise n° 2008-12 du 25 janvier 2008 portant sur la Protection des données à caractère personnel.
    """
    )

    # Chatbot avec le nouveau format "messages"
    chatbot = gr.Chatbot(
        value=[],
        show_copy_button=True,
        height=500,
        type="messages",
        avatar_images=(None, "🤖"),
    )

    # Contrôles
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Quels sont les droits des personnes concernées par la collecte de données personnelles ?",
            container=False,
            scale=8,
        )
        submit_button = gr.Button("Envoyer", variant="primary", scale=1)
        reset_button = gr.Button("🔄 Nouvelle conversation", scale=1)

    # Statut
    with gr.Row():
        status = gr.Textbox(
            value="Prêt à répondre à vos questions.", label="Statut", interactive=False
        )

    # Options de téléchargement
    with gr.Accordion("Options d'export", open=False):
        with gr.Row():
            format_radio = gr.Radio(
                ["Markdown (.md)", "Texte (.txt)"],
                label="Format d'export",
                value="Markdown (.md)",
            )
            download_button = gr.Button("📥 Télécharger la conversation")

        download_file = gr.File(
            label="Fichier de conversation", interactive=False, visible=False
        )

    # À propos
    with gr.Accordion("À propos de cet assistant", open=False):
        gr.Markdown(
            """
        ## Assistant Juridique IA pour la Loi sur la Protection des Données Personnelles

        Cet assistant juridique est spécialisé dans la loi sénégalaise sur la protection des données personnelles : loi n° 2008-12 du 25 janvier 2008.
        Il utilise une approche de Retrieval-Augmented Generation (RAG) pour fournir des réponses précises basées sur le texte de loi original.
        
        ### Fonctionnement
        
        1. Votre question est analysée pour identifier les concepts juridiques pertinents
        2. L'assistant recherche les articles de loi les plus pertinents
        3. Une réponse est générée en se basant uniquement sur ces articles
        4. Les sources utilisées sont citées pour plus de transparence
        
        ### Limites
        
        - Cet assistant ne remplace pas un avis juridique professionnel
        - Il se limite aux informations contenues dans la loi sur la protection des données personnelles
        - En cas de doute, consultez un avocat ou la Commission des Données Personnelles
        
        ### Utilisation du mode clair/sombre
        
        Vous pouvez changer entre le mode clair et sombre en utilisant le bouton settings situé en bas à droite de la page.
        """
        )

    # Exemples de questions
    gr.Examples(
        examples=[
            "Qu'est-ce que la Commission des Données Personnelles (CDP) et quelles sont ses missions ?",
            "Quels sont les droits des personnes concernées par un traitement de données personnelles ?",
            "Dans quels cas peut-on transférer des données personnelles vers un pays tiers ?",
            "Comment sont sanctionnés les manquements à la loi sur la protection des données ?",
            "Quelles sont les formalités préalables à la mise en œuvre d'un traitement de données ?",
            "Comment est définie une donnée à caractère personnel ?",
        ],
        inputs=msg,
        label="Exemples",
    )

    # Gestion des interactions avec l'API de progression intégrée

    # Soumission par Enter
    msg.submit(
        query_chatbot,
        [msg, chatbot],
        [chatbot],
    ).then(
        lambda: "", None, [msg]
    ).then(lambda: "✅ Prêt à répondre à vos questions.", None, [status])

    # Soumission par bouton
    submit_button.click(
        query_chatbot,
        [msg, chatbot],
        [chatbot],
    ).then(
        lambda: "", None, [msg]
    ).then(lambda: "✅ Prêt à répondre à vos questions.", None, [status])

    # Réinitialisation de la conversation
    reset_button.click(reset_conversation, None, chatbot).then(
        lambda: "Conversation réinitialisée.", None, [status]
    )

    # Fonction pour traiter le format sélectionné
    def get_format_extension(format_choice):
        return "md" if format_choice == "Markdown (.md)" else "txt"

    # Téléchargement de la conversation
    download_button.click(
        lambda fmt, hist: save_conversation(hist, get_format_extension(fmt)),
        [format_radio, chatbot],
        [download_file],
    ).then(lambda: gr.update(visible=True), None, [download_file]).then(
        lambda: "Conversation prête à être téléchargée.", None, [status]
    )

# Lancement de l'interface
if __name__ == "__main__":
    # Détermine si on doit partager l'application publiquement
    share_env = os.getenv("GRADIO_SHARE", "False").lower() in ("true", "1", "t")

    # Port du serveur Gradio
    port = int(os.getenv("GRADIO_SERVER_PORT", 7860))

    # Lancement de l'application
    demo.launch(
        server_name="0.0.0.0",  # Permet d'accéder à l'application depuis d'autres machines
        server_port=port,
        share=share_env,
        debug=True,  # Activer le mode debug pour voir les erreurs détaillées
    )
