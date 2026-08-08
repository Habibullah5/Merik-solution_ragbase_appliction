import re
from typing import List

class CitationValidator:
    """Verifies that all inline citations in the LLM answer match retrieved context chunks."""

    @staticmethod
    def extract_citations(text: str) -> List[str]:
        return list(set(re.findall(r'\[(merik_[a-f0-9]+_\d+)\]', text)))

    @staticmethod
    def validate(citations: List[str], valid_chunk_ids: List[str]) -> bool:
        return all(cid in valid_chunk_ids for cid in citations)