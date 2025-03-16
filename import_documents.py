import os
import argparse
from modules.importer import process_pdf_document, process_document_folder
from modules.processor import load_json, save_json, segment_from_json
from config import (
    LAW_STRUCTURE_PATH,
    CHUNKS_PATH,
    RAW_DIR,
    PROCESSED_DIR,
    MAX_CHUNK_SIZE,
    OVERLAP_SIZE,
)


def main():
    """Script d'importation de documents pour enrichir la base de connaissances"""
    parser = argparse.ArgumentParser(
        description="Importe des documents PDF pour enrichir la base de connaissances"
    )
    parser.add_argument("--pdf", help="Chemin vers un fichier PDF à importer")
    parser.add_argument(
        "--folder", help="Chemin vers un dossier contenant des PDF à importer"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Réinitialiser la base de connaissances"
    )
    args = parser.parse_args()

    if not args.pdf and not args.folder:
        print(
            "Erreur : Vous devez spécifier un fichier PDF (--pdf) ou un dossier (--folder)"
        )
        return

    # Récupérer la structure existante si disponible et si on ne veut pas réinitialiser
    existing_structure = {}
    if os.path.exists(LAW_STRUCTURE_PATH) and not args.reset:
        print(f"Chargement de la structure existante depuis {LAW_STRUCTURE_PATH}")
        existing_structure = load_json(LAW_STRUCTURE_PATH)

    # Traiter les nouveaux documents
    new_structure = {}
    if args.pdf:
        # Traiter un seul fichier PDF
        new_structure = process_pdf_document(args.pdf)
    elif args.folder:
        # Traiter tous les PDF d'un dossier
        temp_output = os.path.join(PROCESSED_DIR, "temp_structure.json")
        new_structure = process_document_folder(args.folder, temp_output)

    # Fusionner avec la structure existante si nécessaire
    if existing_structure and not args.reset:
        from modules.importer import merge_legal_structures

        final_structure = merge_legal_structures([existing_structure, new_structure])
    else:
        final_structure = new_structure

    # Sauvegarder la structure finale
    save_json(final_structure, LAW_STRUCTURE_PATH)
    print(f"Structure finale sauvegardée dans {LAW_STRUCTURE_PATH}")

    # Générer les nouveaux chunks
    print("Segmentation de la structure en chunks...")
    chunks = segment_from_json(
        final_structure, max_chunk_size=MAX_CHUNK_SIZE, overlap=OVERLAP_SIZE
    )
    save_json(chunks, CHUNKS_PATH)
    print(f"Chunks sauvegardés dans {CHUNKS_PATH}")

    print(
        f"Importation terminée. Exécutez maintenant 'python indexer.py' pour mettre à jour l'index vectoriel."
    )


if __name__ == "__main__":
    main()
