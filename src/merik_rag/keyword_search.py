from typing import List, Tuple
from rank_bm25 import BM25Okapi
from merik_rag.models import Chunk

class BM25Search:
    """Keyword search for error codes, exact configs, and variable names."""
    
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.corpus = [c.content.lower().split(" ") for c in chunks]
        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query: str, top_k: int) -> List[Tuple[Chunk, float]]:
        tokenized_query = query.lower().split(" ")
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [(self.chunks[i], float(scores[i])) for i in top_indices]