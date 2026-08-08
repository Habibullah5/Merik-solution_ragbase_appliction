import sys
import json
from merik_rag.config import CHUNKS_PATH, HANDBOOK_PATH
from merik_rag.models import Chunk
from merik_rag.ingest import run_ingestion
from merik_rag.retrieval import RetrievalEngine
from merik_rag.generator import RAGGenerator

def load_indexed_chunks() -> list[Chunk]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"Missing index file at {CHUNKS_PATH}. Run 'uv run python -m merik_rag.ingest' first.")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Chunk(**item) for item in data]

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  uv run merik-rag index")
        print("  uv run merik-rag ask \"<question>\"")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "index":
        run_ingestion()
        
    elif command == "ask":
        if len(sys.argv) < 3:
            print("Please provide a question string.")
            sys.exit(1)
        
        query = sys.argv[2]
        chunks = load_indexed_chunks()
        retriever = RetrievalEngine(chunks)
        results = retriever.retrieve(query)
        
        generator = RAGGenerator()
        response = generator.generate(query, results)

        print("\n=== ANSWER ===")
        print(response.answer)
        print("\n=== CITATIONS ===")
        print(response.citations)
        print(f"\nRefused: {response.refused}")

if __name__ == "__main__":
    main()