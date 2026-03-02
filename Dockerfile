# ──────────────────────────────────────────────────────────────────────────────
# Stripe RAG Agent – Backend Dockerfile
# Base: python:3.11-slim
# ──────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# ---------------------------------------------------------------------------
# System dependencies
#   pandoc  – required by pypandoc (RST/MD parsing during ingestion)
#   gcc/g++ – required to compile some Python C-extension packages
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------------------------------------------------------------------------
# Python dependencies
# Step 1: install CPU-only PyTorch FIRST (~700 MB vs ~2 GB for the default
#         CUDA build that sentence-transformers would otherwise pull in).
# Step 2: install the rest of requirements.txt (sentence-transformers will
#         detect torch is already present and skip re-downloading it).
# ---------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir \
        torch==2.5.1+cpu \
        --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Pre-download the HuggingFace embedding model at build time so the
# container starts instantly without needing an internet connection.
# Model: BAAI/bge-small-en-v1.5  (~130 MB)
# ---------------------------------------------------------------------------
RUN python -c "\
from langchain_huggingface import HuggingFaceEmbeddings; \
HuggingFaceEmbeddings( \
    model_name='BAAI/bge-small-en-v1.5', \
    model_kwargs={'device': 'cpu'}, \
    encode_kwargs={'normalize_embeddings': True} \
)"

# ---------------------------------------------------------------------------
# Application source + configuration
# ---------------------------------------------------------------------------
COPY src/       ./src/
COPY config.yaml .

# ---------------------------------------------------------------------------
# Pre-built ChromaDB vector store (populated locally – do NOT re-ingest)
# Raw docs are also included in case re-ingestion is ever triggered.
# ---------------------------------------------------------------------------
COPY data/chroma_db/  ./data/chroma_db/
COPY data/raw/        ./data/raw/
# Optional JSON exports (small, harmless to include)
COPY data/db_dump.json      ./data/db_dump.json
COPY data/enriched_db.json  ./data/enriched_db.json

# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
