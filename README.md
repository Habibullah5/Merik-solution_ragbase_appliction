# Merik Engineering Handbook RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant designed to index the Merik Engineering Handbook and answer user queries with verifiable, chunk-level citations.

---

## 1. How to Index the Handbook

To index the handbook (parse structural Markdown and build the vector search index), execute the **indexing command**:

```bash
uv run python -m merik_rag.ingest