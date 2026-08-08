import hashlib
from pathlib import Path
from typing import List
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from merik_rag.models import Chunk, ChunkMetadata

class StructuralChunker:
    """Splits Markdown documents strictly along structural section headers."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.headers = [
            ("#", "header_1"),
            ("##", "header_2"),
            ("###", "header_3"),
        ]

    def split(self) -> List[Chunk]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers, strip_headers=False
        )
        header_docs = md_splitter.split_text(raw_text)

        # Fallback splitter for sections that exceed token boundaries while preserving syntax
        char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=120,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = []
        for doc in header_docs:
            sub_docs = char_splitter.split_documents([doc])
            for idx, sub_doc in enumerate(sub_docs):
                section_path = " > ".join([
                    v for k, v in sub_doc.metadata.items() if k.startswith("header_")
                ]) or "Root"

                content_hash = hashlib.md5(sub_doc.page_content.encode()).hexdigest()[:8]
                chunk_id = f"merik_{content_hash}_{idx}"

                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    content=sub_doc.page_content,
                    metadata=ChunkMetadata(
                        source=self.file_path.name,
                        section=section_path,
                        chunk_id=chunk_id
                    )
                ))
        return chunks