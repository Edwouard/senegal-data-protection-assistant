import fitz  # PyMuPDF
import os
from typing import Dict, Any, List
from modules.processor import extract_legal_structure, save_json


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrait le texte d'un document PDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def process_pdf_document(
    pdf_path: str, output_path: str = None, copy_to_raw: bool = True
) -> Dict[str, Any]:
    """
    Traite un document PDF : extraction du texte et de la structure légale

    Args:
        pdf_path: Chemin vers le fichier PDF
        output_path: Chemin pour sauvegarder la structure extraite (optionnel)
        copy_to_raw: Indique si le fichier doit être copié dans le dossier raw

    Returns:
        Dict: Structure légale extraite
    """
    print(f"Traitement du document PDF : {pdf_path}")

    # Copier le fichier PDF dans le dossier raw si demandé
    if copy_to_raw:
        import shutil
        from config import RAW_DIR

        filename = os.path.basename(pdf_path)
        destination = os.path.join(RAW_DIR, filename)

        if os.path.exists(destination) and os.path.samefile(pdf_path, destination):
            # Le fichier est déjà dans le bon dossier
            pass
        else:
            shutil.copy2(pdf_path, destination)
            print(f"Fichier copié dans {destination}")

    # Extraction du texte
    document_text = extract_text_from_pdf(pdf_path)

    # Extraction de la structure légale
    legal_structure = extract_legal_structure(document_text)

    # Sauvegarde de la structure si un chemin est fourni
    if output_path:
        save_json(legal_structure, output_path)
        print(f"Structure légale sauvegardée dans : {output_path}")

    return legal_structure


def merge_legal_structures(structures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Fusionne plusieurs structures légales en une seule

    Args:
        structures: Liste des structures légales à fusionner

    Returns:
        Dict: Structure fusionnée
    """
    merged_structure = {}

    for structure in structures:
        for chapter_key, chapter_content in structure.items():
            # Si le chapitre n'existe pas encore, l'ajouter
            if chapter_key not in merged_structure:
                merged_structure[chapter_key] = {}

            # Parcourir les sections du chapitre
            for section_key, section_content in chapter_content.items():
                # Si la section n'existe pas encore dans ce chapitre, l'ajouter
                if section_key not in merged_structure[chapter_key]:
                    merged_structure[chapter_key][section_key] = {}

                # Ajouter les articles
                for article_key, article_content in section_content.items():
                    # Si un article avec le même nom existe déjà, ajouter un suffixe
                    if article_key in merged_structure[chapter_key][section_key]:
                        # On peut choisir de fusionner ou de renommer
                        # Ici, on choisit de remplacer avec avertissement
                        print(
                            f"Attention : L'article {article_key} existe déjà et sera remplacé"
                        )

                    merged_structure[chapter_key][section_key][
                        article_key
                    ] = article_content

    return merged_structure


def process_document_folder(folder_path: str, output_path: str) -> Dict[str, Any]:
    """
    Traite tous les documents PDF d'un dossier et fusionne leurs structures

    Args:
        folder_path: Chemin vers le dossier contenant les PDF
        output_path: Chemin pour sauvegarder la structure fusionnée

    Returns:
        Dict: Structure légale fusionnée
    """
    structures = []

    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            # Extraire la structure du document
            structure = process_pdf_document(pdf_path)
            structures.append(structure)

    # Fusionner toutes les structures
    merged_structure = merge_legal_structures(structures)

    # Sauvegarder la structure fusionnée
    save_json(merged_structure, output_path)
    print(f"Structure fusionnée sauvegardée dans : {output_path}")

    return merged_structure
