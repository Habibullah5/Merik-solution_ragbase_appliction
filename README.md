# Merik Engineering Handbook RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant designed to index the Merik Engineering Handbook and answer user queries with verifiable, chunk-level citations.

---

## Indexing Command

To index the handbook corpus, parse structural Markdown, and build the vector search database, run the indexing command:

```bash
uv run python -m merik_rag.ingest