import os
import anthropic
from dotenv import load_dotenv
from typing import List, Tuple
from merik_rag.models import Chunk, QueryResponse
from merik_rag.prompts import SYSTEM_PROMPT, format_user_prompt
from merik_rag.citations import CitationValidator
from merik_rag.config import MIN_RELEVANCE_SCORE

load_dotenv()

class RAGGenerator:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment or .env file.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.candidate_models = [
            "claude-haiku-4-5-20251001",
            "claude-sonnet-4-5-20250929",
            "claude-sonnet-5"
        ]

    def generate(self, query: str, retrieved_results: List[Tuple[Chunk, float]]) -> QueryResponse:
        if not retrieved_results or retrieved_results[0][1] < MIN_RELEVANCE_SCORE:
            return QueryResponse(
                query=query,
                answer="I am unable to answer this question as the provided handbook sections do not contain relevant information.",
                citations=[],
                refused=True
            )

        chunks = [item[0] for item in retrieved_results]
        user_prompt = format_user_prompt(query, chunks)

        message = None
        last_err = None
        for model_id in self.candidate_models:
            try:
                message = self.client.messages.create(
                    model=model_id,
                    max_tokens=1000,
                    temperature=0.0,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                break
            except anthropic.NotFoundError as e:
                last_err = e
                continue

        if message is None:
            raise last_err

        answer = message.content[0].text
        found_citations = CitationValidator.extract_citations(answer)
        refused = "unable to answer" in answer.lower()

        return QueryResponse(
            query=query,
            answer=answer,
            citations=found_citations if not refused else [],
            refused=refused
        )
