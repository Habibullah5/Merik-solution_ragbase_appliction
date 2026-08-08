import chromadb
from typing import List, Tuple
from merik_rag.models import Chunk
from merik_rag.embeddings import EmbeddingEngine
from merik_rag.config import INDEX_DIR

class VectorSearch:
    """Dense vector search using ChromaDB."""
    
    def __init__(self, embedder: EmbeddingEngine):
        self.embedder = embedder
        self.client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
        self.collection = self.client.get_or_create_collection(name="merik_docs")

    def index_chunks(self, chunks: List[Chunk]):
        embeddings = self.embedder.embed_text([c.content for c in chunks])
        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            documents=[c.content for c in chunks],
            embeddings=embeddings,
            metadatas=[c.metadata.model_dump() for c in chunks]
        )

    def search(self, query: str, top_k: int, chunk_map: dict) -> List[Tuple[Chunk, float]]:
        query_emb = self.embedder.embed_text([query])
        results = self.collection.query(query_embeddings=query_emb, n_results=top_k)
        
        matches = []
        if results["ids"]:
            for chunk_id, dist in zip(results["ids"][0], results["distances"][0]):
                if chunk_id in chunk_map:
                    # Convert distance to similarity score
                    matches.append((chunk_map[chunk_id], float(1.0 / (1.0 + dist))))
        return matches