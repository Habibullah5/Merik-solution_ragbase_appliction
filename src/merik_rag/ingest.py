import json
from merik_rag.config import HANDBOOK_PATH, CHUNKS_PATH, INDEX_DIR
from merik_rag.chunking import StructuralChunker
from merik_rag.embeddings import EmbeddingEngine
from merik_rag.vector_search import VectorSearch

def run_ingestion():
    print(f"Parsing and chunking {HANDBOOK_PATH}...")
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    chunker = StructuralChunker(HANDBOOK_PATH)
    chunks = chunker.split()

    # Save chunks locally
    serialized_chunks = [c.model_dump() for c in chunks]
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(serialized_chunks, f, indent=2)

    # Populate vector database
    print("Generating embeddings and building vector index...")
    embedder = EmbeddingEngine()
    vdb = VectorSearch(embedder)
    vdb.index_chunks(chunks)

    print(f"Indexing complete! Successfully chunked and stored {len(chunks)} structural sections.")

if __name__ == "__main__":
    run_ingestion()