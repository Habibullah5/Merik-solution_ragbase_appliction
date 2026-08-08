from typing import List, Tuple
from merik_rag.models import Chunk
from merik_rag.keyword_search import BM25Search
from merik_rag.vector_search import VectorSearch
from merik_rag.embeddings import EmbeddingEngine
from merik_rag.hybrid import HybridSearch
from merik_rag.config import TOP_K_RETRIEVAL

class RetrievalEngine:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.chunk_map = {c.chunk_id: c for c in chunks}
        self.bm25 = BM25Search(chunks)
        self.embedder = EmbeddingEngine()
        self.vector_db = VectorSearch(self.embedder)

    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> List[Tuple[Chunk, float]]:
        sparse_res = self.bm25.search(query, top_k=top_k * 2)
        dense_res = self.vector_db.search(query, top_k=top_k * 2, chunk_map=self.chunk_map)
        return HybridSearch.fuse_rrf(dense_res, sparse_res, top_k=top_k)