from pydantic import BaseModel
from typing import List, Dict, Optional

class ChunkMetadata(BaseModel):
    source: str
    section: str
    chunk_id: str

class Chunk(BaseModel):
    chunk_id: str
    content: str
    metadata: ChunkMetadata

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[str]
    refused: bool