# Merik Engineering Handbook RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant designed to index the Merik Engineering Handbook and answer user queries with verifiable, chunk-level citations.

---

## Indexing Command

To index the handbook corpus, parse structural Markdown, and build the vector search database, run the indexing command:

```bash
uv run python -m merik_rag.ingest
```

---

## Question / Query Command

To query the handbook and ask a question with chunk-level citations, run the question/query command:

```bash
uv run merik-rag ask "What is the equipment budget for new engineers?"
```

*(Alternative execution command)*:
```bash
uv run python -m merik_rag.cli ask "What is the equipment budget for new engineers?"
```

---

## Evaluation Command

To run the automated benchmark evaluation suite against test questions:

```bash
uv run python scripts/evaluate.py
```

---

## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Habibullah5/Merik-solution_ragbase_appliction.git](https://github.com/Habibullah5/Merik-solution_ragbase_appliction.git)
   cd Merik-solution_ragbase_appliction
   ```

2. **Install Dependencies:**
   ```bash
   uv sync
   ```

3. **Configure Environment:**
   Create a `.env` file in the project root:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```