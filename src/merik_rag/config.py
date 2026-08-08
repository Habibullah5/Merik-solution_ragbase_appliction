from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "index"
HANDBOOK_PATH = DATA_DIR / "handbook.md"
QUESTIONS_PATH = DATA_DIR / "questions.json"
CHUNKS_PATH = INDEX_DIR / "chunks.json"

# Search Parameters
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K_RETRIEVAL = 4
RRF_K = 60
MIN_RELEVANCE_SCORE = 0.012  # Threshold below which assistant refuses to answer