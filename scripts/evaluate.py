import json
from merik_rag.config import QUESTIONS_PATH, CHUNKS_PATH
from merik_rag.models import Chunk
from merik_rag.retrieval import RetrievalEngine
from merik_rag.generator import RAGGenerator

def run_evaluation():
    print("--- Starting Grader Evaluation Benchmark ---")
    
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
    chunks = [Chunk(**item) for item in chunks_data]

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        eval_questions = json.load(f)

    retriever = RetrievalEngine(chunks)
    generator = RAGGenerator()

    correct_retrievals = 0
    correct_refusals = 0
    total = len(eval_questions)

    for idx, q in enumerate(eval_questions):
        query = q["question"]
        expected_sections = q.get("expected_sections", [])
        should_refuse = q.get("should_refuse", False)

        retrieved = retriever.retrieve(query)
        response = generator.generate(query, retrieved)

        # Retrieval accuracy check
        retrieved_sections = [r[0].metadata.section for r in retrieved]
        hit = any(any(exp in sec for sec in retrieved_sections) for exp in expected_sections) if expected_sections else False

        if hit or (should_refuse and response.refused):
            correct_retrievals += 1

        status = "PASS" if (response.refused if should_refuse else hit) else "FAIL"
        print(f"[{status}] Q{idx+1}: {query[:60]}...")

    print(f"\nAccuracy Score: {(correct_retrievals / total) * 100:.2f}%")

if __name__ == "__main__":
    run_evaluation()