import faiss
import numpy as np
import pickle
from typing import List, Dict, Any


class Retriever:
    def __init__(self):
        """Initialisation du service de récupération"""
        self.index = None
        self.metadata = []

    def build_index(self, vectors: List[Dict[str, Any]]):
        """Construction de l'index FAISS à partir des vecteurs"""
        # Extraire les embeddings et les métadonnées
        embeddings = np.array([vec["embedding"] for vec in vectors]).astype("float32")
        metadata = vectors

        # Créer l'index FAISS
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.metadata = metadata

    def save_index(self, index_path: str, metadata_path: str):
        """Sauvegarde de l'index et des métadonnées"""
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load_index(self, index_path: str, metadata_path: str):
        """Chargement de l'index et des métadonnées"""
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def retrieve_relevant_chunks(
        self, query_embedding, top_k=5, min_similarity_score=0.5
    ):
        """
        Fonction de récupération des chunks pertinents reprise depuis la base de connaissance.
        """
        try:
            """
            # Reshape pour s'assurer que l'embedding est au bon format
            query_embedding = query_embedding.reshape(1, -1)

            # Recherche des chunks les plus similaires
            distances, indices = self.index.search(query_embedding, top_k)

            # Récupération des chunks et de leurs métadonnées
            results = []
            for i, idx in enumerate(indices[0]):
                # Si un seuil de distance est défini, vérifier si le résultat est pertinent
                if max_distance is not None and distances[0][i] > max_distance:
                    continue

                # Convertir la distance en score de similarité
                similarity_score = 1.0 / (1.0 + float(distances[0][i]))

                # Convertir le score de similarité en pourcentage de pertinence
                relevance = similarity_score * 100

                chunk = self.metadata[idx]
                results.append(
                    {
                        "text": chunk["text"],
                        "metadata": chunk["metadata"],
                        "distance": float(distances[0][i]),
                        "similarity_score": similarity_score,
                        "relevance": relevance,
                    }
                )
            """

            # Normaliser les embeddings pour le calcul de similarité cosinus
            # query_embedding_normalized = query_embedding / np.linalg.norm(                query_embedding            )

            # Calculer la similarité cosinus avec tous les embeddings de l'index
            # Note: cela nécessite de modifier la structure de l'index FAISS
            # pour utiliser IndexFlatIP (Inner Product) au lieu de IndexFlatL2
            similarities, indices = self.index.search(
                query_embedding.reshape(1, -1), top_k
            )

            results = []
            for i, idx in enumerate(indices[0]):
                # La similarité cosinus est déjà entre -1 et 1, nous pouvons l'ajuster à [0,1] si nécessaire
                similarity_score = (
                    similarities[0][i] + 1
                ) / 2  # Optionnel: convertir de [-1,1] à [0,1]

                if similarity_score >= min_similarity_score:
                    chunk = self.metadata[idx]
                    results.append(
                        {
                            "text": chunk["text"],
                            "metadata": chunk["metadata"],
                            "similarity_score": similarity_score,
                        }
                    )
            return results
        except Exception as e:
            print(f"Erreur lors de la récupération des chunks: {str(e)}")
            return []
