import re
import json
import nltk
from typing import Dict, Any
from nltk.tokenize import sent_tokenize

# Téléchargement des ressources NLTK
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def extract_legal_structure(text):
    """
    Fonction d'extraction du contenu du document et de la structure.
    Cette fonction est reprise depuis la base de connaissance fournie.
    """
    # Structure pour stocker les données
    law_structure = {}

    # Variables pour suivre la position dans la hiérarchie
    current_chapter = None
    current_section = None
    chapter_num = None
    section_num = None

    # Nettoyer le texte
    text = re.sub(r"► Page \d+ ◄", "", text)
    text = re.sub(r"Page \d+ ◄", "", text)

    # Diviser le texte en lignes
    lines = text.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Détecter un chapitre
        chapitre_match = re.match(
            r"(?:CHAPITRE|Chapitre)\s+([^\.]+)\.\s*-\s*([^\n]+)", line, re.IGNORECASE
        )
        if chapitre_match or re.match(
            r"CHAPITRE\s+([IVXLCDM]+)\s*[:\.]", line, re.IGNORECASE
        ):
            if not chapitre_match:
                # Gérer le cas où le format est différent (ex: "CHAPITRE II : titre")
                alt_match = re.match(
                    r"(?:CHAPITRE|Chapitre)\s+([IVXLCDM]+)\s*[:\.](?:\s+)?([^\n]*)",
                    line,
                    re.IGNORECASE,
                )
                if alt_match:
                    chapter_num = alt_match.group(1)
                    chapter_title = alt_match.group(2).strip()
                    if not chapter_title and i + 1 < len(lines):
                        chapter_title = lines[i + 1].strip()
                        i += 1
            else:
                chapter_num = chapitre_match.group(1)
                chapter_title = chapitre_match.group(2)

            # Normaliser le format du chapitre
            current_chapter = f"Chapitre {chapter_num}: {chapter_title}"
            law_structure[current_chapter] = {}
            i += 1
            continue

        # Détecter une section
        section_match = re.match(
            r"Section\s+([^\.]+)\.\s*-\s*([^\n]+)", line, re.IGNORECASE
        )
        if section_match or re.match(
            r"Section\s+([IVXLCDM]+|première|[0-9]+)\s*[:\.]", line, re.IGNORECASE
        ):
            if not section_match:
                # Gérer le cas où le format est différent
                alt_match = re.match(
                    r"Section\s+([IVXLCDM]+|première|[0-9]+)\s*[:\.](?:\s+)?([^\n]*)",
                    line,
                    re.IGNORECASE,
                )
                if alt_match:
                    section_num = alt_match.group(1)
                    section_title = alt_match.group(2).strip()
                    if not section_title and i + 1 < len(lines):
                        section_title = lines[i + 1].strip()
                        i += 1
            else:
                section_num = section_match.group(1)
                section_title = section_match.group(2)

            # Vérifier que nous avons déjà un chapitre
            if current_chapter is None:
                # Identifier si le texte précédent contient des indications sur le chapitre
                for j in range(i - 1, max(0, i - 10), -1):
                    if re.match(r"CHAPITRE|Chapitre", lines[j].strip(), re.IGNORECASE):
                        # Essayer de reconstruire le chapitre à partir des lignes précédentes
                        chapitre_text = " ".join(lines[j:i]).strip()
                        chapitre_match = re.search(
                            r"(?:CHAPITRE|Chapitre)\s+([^\.]+)[\.:\s]+([^\n]+)",
                            chapitre_text,
                            re.IGNORECASE,
                        )
                        if chapitre_match:
                            current_chapter = f"Chapitre {chapitre_match.group(1)}: {chapitre_match.group(2)}"
                            law_structure[current_chapter] = {}
                            break

                if current_chapter is None:
                    current_chapter = "Chapitre non spécifié"
                    law_structure[current_chapter] = {}

            # Normaliser le format de la section
            current_section = f"Section {section_num}: {section_title}"
            law_structure[current_chapter][current_section] = {}
            i += 1
            continue

        # Détecter un article
        article_match = re.match(r"Article\s+([^\.:]+)[\.:]", line)
        if article_match:
            article_num = article_match.group(1)
            article_key = f"Article {article_num}"

            # Vérifier et créer la structure si nécessaire
            if current_chapter is None:
                current_chapter = "Chapitre non spécifié"
                law_structure[current_chapter] = {}

            if current_section is None:
                # Essayer d'identifier la section à partir des lignes précédentes
                for j in range(i - 1, max(0, i - 10), -1):
                    if re.match(r"Section", lines[j].strip(), re.IGNORECASE):
                        # Reconstruire la section
                        section_text = " ".join(lines[j:i]).strip()
                        section_match = re.search(
                            r"Section\s+([^\.]+)[\.:\s]+([^\n]+)",
                            section_text,
                            re.IGNORECASE,
                        )
                        if section_match:
                            current_section = f"Section {section_match.group(1)}: {section_match.group(2)}"
                            break

                if current_section is None:
                    current_section = "Section non spécifiée"

            # S'assurer que la section existe dans le chapitre actuel
            if current_section not in law_structure[current_chapter]:
                law_structure[current_chapter][current_section] = {}

            # Extraire le contenu de l'article
            article_content = []
            article_line = line  # Garder la ligne avec le numéro d'article
            j = i + 1
            while j < len(lines) and not (
                re.match(r"Article\s+([^\.:]+)[\.:]", lines[j].strip())
                or re.match(
                    r"Section\s+([^\.]+)\.\s*-", lines[j].strip(), re.IGNORECASE
                )
                or re.match(
                    r"CHAPITRE\s+([^\.]+)\.\s*-", lines[j].strip(), re.IGNORECASE
                )
            ):
                article_content.append(lines[j].strip())
                j += 1

            # Joindre le contenu de l'article avec son numéro
            full_article_content = (
                article_line + " " + " ".join(article_content).strip()
            )
            law_structure[current_chapter][current_section][
                article_key
            ] = full_article_content
            i = j
            continue

        i += 1

    return law_structure


def segment_from_json(law_structure, max_chunk_size=1200, overlap=250):
    """
    Fonction de segmentation reprise depuis la base de connaissance fournie.
    Segmente la structure de la loi en chunks.
    """
    chunks = []

    for chapter_key, chapter_content in law_structure.items():
        for section_key, section_content in chapter_content.items():
            # Optionnel: créer un chunk de contexte pour la section
            # section_context = f"{chapter_key}\n{section_key}\n\nRésumé: Cette section traite de {section_key.split(':', 1)[1] if ':' in section_key else section_key}"

            for article_key, article_text in section_content.items():
                # Créer l'en-tête avec métadonnées
                header = f"{chapter_key} | {section_key} | {article_key}"

                # Extraire le numéro d'article si possible
                article_number = None
                article_match = re.search(r"Article\s+([^\s\.]+)", article_key)
                if article_match:
                    article_number = article_match.group(1)

                # Traiter l'article selon sa longueur
                if len(article_text) + len(header) <= max_chunk_size:
                    chunks.append(
                        {
                            "text": f"{header}\n\n{article_text}",
                            "metadata": {
                                "chapter": chapter_key,
                                "section": section_key,
                                "article": article_key,
                                "article_number": article_number,
                            },
                        }
                    )
                else:
                    # Diviser l'article en préservant le contexte
                    sentences = sent_tokenize(article_text)
                    current_chunk = header + "\n\n"

                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) <= max_chunk_size:
                            current_chunk += sentence + " "
                        else:
                            chunks.append(
                                {
                                    "text": current_chunk,
                                    "metadata": {
                                        "chapter": chapter_key,
                                        "section": section_key,
                                        "article": article_key,
                                        "article_number": article_number,
                                        "is_partial": True,
                                    },
                                }
                            )

                            # Créer un nouveau chunk avec chevauchement
                            overlap_text = " ".join(
                                current_chunk.split()[-overlap // 10 :]
                            )
                            current_chunk = (
                                f"{header} [SUITE]\n\n{overlap_text} {sentence} "
                            )

                    # Ajouter le dernier chunk
                    if current_chunk and current_chunk != header + "\n\n":
                        chunks.append(
                            {
                                "text": current_chunk,
                                "metadata": {
                                    "chapter": chapter_key,
                                    "section": section_key,
                                    "article": article_key,
                                    "article_number": article_number,
                                    "is_partial": True,
                                },
                            }
                        )

    return chunks


def load_json(filepath: str) -> Dict:
    """Charge un fichier JSON"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, filepath: str) -> None:
    """Sauvegarde des données au format JSON"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
