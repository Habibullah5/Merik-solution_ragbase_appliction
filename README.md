# Merik Engineering Handbook RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant built to index the Merik Engineering Handbook and provide accurate answers backed by explicit chunk-level citations.

---

## Key Features

* **Structural Splitting:** Splits documents by Markdown section headers rather than fixed character counts to preserve semantic context.
* **Metadata Persistence:** Stores document IDs, sections, and chunk IDs on every chunk (`merik_fd866974_0`).
* **Hybrid Retrieval:** Combines BM25 keyword matching with vector similarity search for accurate recall across exact terms and semantic queries.
* **Strict Citation Verification:** Parses model output to ensure every claim carries valid contextual chunk citations.
* **Guardrail Refusal:** Automatically refuses to answer queries when context relevance falls below the threshold or the topic is out-of-bounds.

---

## Prerequisites & Installation

### 1. Requirements
* Python 3.10+
* [`uv`](https://github.com/astral-sh/uv) package manager

### 2. Environment Setup
Clone the repository and install dependencies:

```bash
git clone [https://github.com/your-username/merik-rag.git](https://github.com/your-username/merik-rag.git)
cd merik-rag
uv sync