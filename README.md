# Merik Engineering Handbook RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant designed to index the Merik Engineering Handbook and answer user queries with verifiable, chunk-level citations.

---

## Indexing

To parse the structural Markdown handbook and build the vector search index, run the indexing command:

```bash
uv run python -m merik_rag.ingest
## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Habibullah5/Merik-solution_ragbase_appliction.git](https://github.com/Habibullah5/Merik-solution_ragbase_appliction.git)
   cd Merik-solution_ragbase_appliction