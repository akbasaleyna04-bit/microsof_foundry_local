# Local RAG Assistant (Microsoft Foundry Local)

An enterprise-grade, offline-first Retrieval-Augmented Generation (RAG) assistant. Built entirely on the Microsoft Foundry Local SDK, this project ensures zero data leakage by running Large Language Models (LLMs) and vector embeddings strictly on your local hardware—eliminating the need for internet connectivity or Azure cloud services.

---

## 🚀 Architecture & Key Features

* **100% Local Execution (Edge AI):** Completely decoupled from cloud APIs. Ensures absolute data privacy and lower latency for local operations.
* **Intelligent Document Ingestion:** Implements semantic text chunking with configurable limits (`CHUNK_MAX_CHARS` and `CHUNK_OVERLAP_CHARS`) to preserve contextual integrity across documents.
* **Custom Vector Search Engine:** Utilizes the `qwen3-embedding-0.6b` model to generate high-dimensional vectors, stored efficiently in a lightweight SQLite database (`data/rag.db`). Search is driven by optimized cosine similarity calculations.
* **Zero-Hallucination Guardrails:** Powered by `phi-3.5-mini` and strictly engineered system prompts. If the context does not contain the answer, the pipeline deterministically falls back to a safe default: *"Bu bilgi belgelerimde bulunmuyor."*
* **Fault-Tolerant Pipeline:** Engineered with robust exception handling. Gracefully catches local hardware timeouts and `Operation was cancelled` events (via `FoundryLocalException`), preventing system crashes during intensive CPU/GPU loads.
* **Interactive Web UI:** Wrapped in a clean, responsive Gradio interface for seamless user interaction.

---

## 🛠️ Technology Stack

* **Core Language:** Python 3.12
* **AI SDK:** Microsoft Foundry Local SDK
* **LLM (Chat):** `phi-3.5-mini`
* **Embedding Model:** `qwen3-embedding-0.6b`
* **Database:** SQLite
* **Frontend:** Gradio

---

## 📂 Repository Structure

```text
microsoft_proje/
│
├── data/
│   ├── docs/          # Source directory for knowledge base (.md, .txt)
│   └── rag.db         # Generated SQLite vector database
│
├── rag/
│   ├── __init__.py
│   ├── chunker.py     # Semantic chunking algorithms
│   ├── config.py      # Environment and model configurations
│   ├── db.py          # SQLite schema and transaction management
│   ├── foundry.py     # Microsoft Foundry Local SDK wrappers
│   ├── pipeline.py    # Core RAG orchestration (retrieve -> generate)
│   └── retrieve.py    # Vector math and cosine similarity search
│
├── app.py             # Gradio application entry point
├── ingest.py          # Data pipeline for document embedding
├── evaluate.py        # Automated testing and validation suite
├── selfcheck.py       # Environment and dependency verification
└── requirements.txt   # Python dependencies

---

##⚙️ Quick Start Guide

* **1. Clone & Setup Environment**
```bash
git clone https://github.com/akbasaleyna04-bit/microsof_foundry_local.git
cd microsof_foundry_local
python -m venv .venv

* **2. Install Dependencies**
```bash
pip install -r requirements.txt

* **3. Ingest Knowledge Base**
*Process your local documents and build the vector database:
```bash
python ingest.py

* **4. Launch the Assistant**
```bash
python app.py