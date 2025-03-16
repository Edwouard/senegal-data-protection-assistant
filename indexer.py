import os
import json
import argparse
from modules.processor import load_json, save_json, segment_from_json
from modules.vectorizer import Vectorizer
from modules.retriever import Retriever
from config import (
    LAW_STRUCTURE_PATH,
    CHUNKS_PATH,
    INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL,
    MAX_CHUNK_SIZE,
    OVERLAP_SIZE,
)


def main():
    """Script d'indexation des documents"""
    parser = argparse.ArgumentParser(
        description="Indexation des documents pour le chatbot RAG"
    )
    parser.add_argument(
        "--force-segmentation",
        action="store_true",
        help="Forcer la re-segmentation des documents",
    )
    args = parser.parse_args()

    print("Démarrage de l'indexation des documents...")

    # Vérification de l'existence du fichier de structure de la loi
    if not os.path.exists(LAW_STRUCTURE_PATH):
        print(
            f"Erreur: {LAW_STRUCTURE_PATH} n'existe pas. Veuillez importer des documents d'abord."
        )
        return

    # Chargement de la structure de la loi
    print(f"Chargement de la structure de la loi depuis {LAW_STRUCTURE_PATH}")
    law_structure = load_json(LAW_STRUCTURE_PATH)

    # Segmentation des documents
    if os.path.exists(CHUNKS_PATH) and not args.force_segmentation:
        print(f"Chargement des chunks depuis {CHUNKS_PATH}")
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        print("Segmentation de la structure de la loi...")
        chunks = segment_from_json(
            law_structure, max_chunk_size=MAX_CHUNK_SIZE, overlap=OVERLAP_SIZE
        )
        print(f"Sauvegarde des chunks dans {CHUNKS_PATH}")
        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Nombre de chunks: {len(chunks)}")

    # Vectorisation des chunks
    print("Vectorisation des chunks...")
    vectorizer = Vectorizer(model_name=EMBEDDING_MODEL)
    vectors = vectorizer.vectorize_chunks(chunks)

    # Construction et sauvegarde de l'index FAISS
    print("Construction de l'index FAISS...")
    retriever = Retriever()
    retriever.build_index(vectors)

    print(f"Sauvegarde de l'index dans {INDEX_PATH}")
    retriever.save_index(INDEX_PATH, METADATA_PATH)

    print("Indexation terminée avec succès!")


if __name__ == "__main__":
    main()
