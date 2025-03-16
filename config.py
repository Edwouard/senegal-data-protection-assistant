import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Chemins des répertoires
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
INDEX_DIR = os.path.join(DATA_DIR, "index")

# Fichiers
LAW_STRUCTURE_PATH = os.path.join(PROCESSED_DIR, "law_structure.json")
CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")
INDEX_PATH = os.path.join(INDEX_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(INDEX_DIR, "metadata.pkl")

# Configuration du modèle
EMBEDDING_MODEL = "dangvantuan/sentence-camembert-base"
TOP_K_RESULTS = 5
MAX_CHUNK_SIZE = 1200
OVERLAP_SIZE = 250

# Clé API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Création des répertoires nécessaires
for directory in [DATA_DIR, RAW_DIR, PROCESSED_DIR, INDEX_DIR]:
    os.makedirs(directory, exist_ok=True)
