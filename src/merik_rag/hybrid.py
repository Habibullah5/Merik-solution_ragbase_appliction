from typing import List, Tuple
from merik_rag.models import Chunk
from merik_rag.config import RRF_K

class HybridSearch:
    """Fuses Sparse (BM25) and Dense (Vector) search using Reciprocal Rank Fusion (RRF)."""

    @staticmethod
    def fuse_rrf(
        dense_results: List[Tuple[Chunk, float]], 
        sparse_results: List[Tuple[Chunk, float]], 
        top_k: int
    ) -> List[Tuple[Chunk, float]]:
        
        rrf_scores = {}
        chunk_lookup = {}

        for rank, (chunk, _) in enumerate(dense_results):
            rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0.0) + (1.0 / (RRF_K + rank + 1))
            chunk_lookup[chunk.chunk_id] = chunk

        for rank, (chunk, _) in enumerate(sparse_results):
            rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0.0) + (1.0 / (RRF_K + rank + 1))
            chunk_lookup[chunk.chunk_id] = chunk

        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(chunk_lookup[cid], score) for cid, score in sorted_chunks]