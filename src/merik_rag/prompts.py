SYSTEM_PROMPT = """You are an accurate technical assistant for the Merik Engineering Handbook.

RULES:
1. Answer questions strictly using facts directly mentioned in the provided Context Chunks.
2. Every claim or statement in your response MUST be cited directly using inline chunk ID brackets: [merik_xxxx_x].
3. If the context chunks DO NOT contain sufficient evidence to answer the question, output ONLY:
   "I am unable to answer this question as the provided handbook sections do not contain relevant information."
"""

def format_user_prompt(query: str, context_chunks: list) -> str:
    formatted_context = ""
    for chunk in context_chunks:
        formatted_context += (
            f"--- CHUNK ID: {chunk.chunk_id} ---\n"
            f"Source: {chunk.metadata.source} | Section: {chunk.metadata.section}\n"
            f"Content:\n{chunk.content}\n\n"
        )
    return f"Context Chunks:\n{formatted_context}\nQuestion: {query}"