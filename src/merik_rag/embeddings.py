from sentence_transformers import SentenceTransformer
from merik_rag.config import EMBED_MODEL

class EmbeddingEngine:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)

    def embed_text(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()