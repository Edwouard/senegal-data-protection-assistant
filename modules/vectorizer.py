from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any


class Vectorizer:
    def __init__(self, model_name="dangvantuan/sentence-camembert-base"):
        """Initialisation du modèle de vectorisation"""
        self.model = SentenceTransformer(model_name)

    def vectorize_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Vectorisation des chunks reprise depuis la base de connaissance fournie.
        """
        vectors = []
        for chunk in chunks:
            text = chunk["text"]
            embedding = self.model.encode(text)
            embedding = embedding / np.linalg.norm(embedding)
            chunk["embedding"] = embedding
            vectors.append(chunk)
        return vectors

    def vectorize_query(self, query: str) -> np.ndarray:
        """Vectorisation d'une requête utilisateur"""
        embedding = self.model.encode(query).astype("float32")
        return embedding / np.linalg.norm(embedding)
