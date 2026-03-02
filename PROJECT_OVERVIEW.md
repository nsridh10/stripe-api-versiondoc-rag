# Stripe API Documentation RAG Agent — Project Overview

**Live Demo**: [http://18.116.13.255](http://18.116.13.255) (AWS EC2)

**GitHub Repositories**:

- Backend: [https://github.com/nsridh10/stripe-api-versiondoc-rag](https://github.com/nsridh10/stripe-api-versiondoc-rag)
- Frontend: [https://github.com/nsridh10/stripe-rag-frontend](https://github.com/nsridh10/stripe-rag-frontend)

---

## Executive Summary

This is a production-ready RAG (Retrieval-Augmented Generation) system that enables natural language queries against Stripe's API documentation across multiple versions. The system features:

- **8-node LangGraph agent pipeline** with intelligent routing, budget management, and retry logic
- **Multi-version documentation support** (basil and clover versions with version-aware retrieval)
- **Context-aware multi-turn conversations** with intent detection and session management
- **Comprehensive evaluation framework** using RAGAS v1.0+ with detailed metrics and reports
- **Full-stack implementation** with FastAPI backend and React TypeScript frontend
- **Production deployment** on AWS EC2 with Docker Compose

---

## System Architecture

```
┌───────────────────┐       POST /query       ┌──────────────────────────┐      similarity_search     ┌────────────┐
│  React + TS + Vite│ ──────────────────────▶  │  FastAPI + LangGraph     │ ──────────────────────────▶│  ChromaDB  │
│  (Chat UI)        │ ◀──────────────────────  │  (8-Node Agent Graph)    │ ◀──────────────────────────│  (Vectors) │
└───────────────────┘   answer + sources +     └──────────────────────────┘   chunks + similarity      └────────────┘
                        execution_trace                                        scores
```

### Technology Stack

**Backend**:

- FastAPI (Python 3.11)
- LangGraph for stateful agent orchestration
- ChromaDB for vector storage
- BAAI/bge-small-en-v1.5 embeddings (HuggingFace, CPU-only)
- Multi-provider LLM support (Groq, Grok/xAI, Google Gemini, OpenAI)

**Frontend**:

- React 18 + TypeScript
- Vite build system
- Custom CSS styling
- Real-time source document and execution trace visualization

**Deployment**:

- Docker Compose (2 containers)
- AWS EC2 t3.small instance
- nginx reverse proxy
- Persistent ChromaDB storage

---

## Assignment Requirements — Completion Checklist

### ✅ 1. Data Preparation

**Requirement**: Prepare a small dataset of text documents

**Implementation**:

- **16 Stripe API documentation files** covering 8 API classes (Accounts, Customers, Payment Intents, Subscriptions, Refunds, Products, Prices, Transfers)
- **2 versions per API class**: `basil` (older, reStructuredText format) and `clover` (latest, Markdown format)
- Data located in: `data/raw/` directory
- Total corpus size: ~500KB of technical documentation

**Innovation**: Dual-format parsing with ParserFactory pattern — dynamically selects RSTParser or MarkdownParser based on file extension, enabling version-agnostic ingestion pipeline.

### ✅ 2. Backend Development

**Requirement**: FastAPI backend with RAG system using LLM and vector database

**Implementation**:

- **FastAPI REST API** with 8 endpoints (`/query`, `/sessions`, `/ingest`, etc.)
- **LangGraph 8-node agent pipeline** with conditional routing:
  - Frontier (validation guard)
  - Planner (query decomposition)
  - Budget Checker (resource governor)
  - Executor (tool caller)
  - Tools (vector DB search)
  - Query Expander (retry logic)
  - Restructurer (coverage analysis)
  - Synthesizer (final answer generation)
- **ChromaDB vector store** with metadata-filtered retrieval (`api_class`, `version`, `source_file`)
- **Multi-provider LLM support** — users bring their own API keys, configured per-request
- **Context-aware retrieval** — combines documents with conversation history and operation logs

**Innovation**: The agent uses a **budget-aware planning system** that prevents token/cost overruns by enforcing a configurable tool call limit (default: 6 per request), asks users to narrow queries when budgets are exceeded, and provides transparent execution traces showing which paths were taken and why.

### ✅ 3. Evaluation

**Requirement**: Simple evaluation framework to measure quality of generated responses

**Implementation**:

- **RAGAS (Retrieval-Augmented Generation Assessment) v1.0+**
- **5 comprehensive test cases**:
  1. Basic query (create a customer)
  2. Version comparison (basil vs clover differences)
  3. Junk rejection (weather query — tests guard node)
  4. Multi-API budget overflow (tests resource limits)
  5. Version-specific query (basil refund creation)
- **Metrics collected**:
  - **Performance**: Latency (seconds), token usage, tool calls
  - **Quality** (LLM-as-judge using Groq llama-3.3-70b):
    - **Faithfulness** — Is the answer grounded in retrieved context?
    - **Answer Relevancy** — Does the answer address the question?
    - **Answer Correctness** — How complete vs. ground truth?
- **CSV report generation** — timestamped detailed and summary reports saved to `data/eval/`

**Results** (from latest run):
| Metric | Value |
|--------|-------|
| Avg latency | 3.2s |
| Avg tokens | 2,675 |
| Avg tool calls | 0.8 |
| Faithfulness (RAG queries) | 0.8–1.0 |
| Answer Relevancy (RAG queries) | 0.98–1.0 |

The evaluation correctly validates edge cases:

- **Junk queries** are rejected at the Frontier node (0 tokens, 0 tool calls)
- **Budget overflow** is detected by Budget Checker before expensive retrieval
- **Actual RAG queries** score high on faithfulness and relevancy

**Code**: `src/eval/eval_llm.py` (603 lines), `src/eval/test_cases.py`

### ✅ 4. Frontend (Optional — Big Plus)

**Requirement**: User-friendly React interface for queries and responses

**Implementation**:

- **React 18 + TypeScript + Vite** SPA
- **Three-panel layout**:
  - **Left sidebar**: Session management, LLM configuration (provider/model/API key), new chat button
  - **Center chat area**: Message bubbles with Markdown rendering, text input
  - **Right panel**: Toggleable Source Documents or Execution Trace viewer
- **LLM configuration UI**:
  - Dropdown for providers (Groq, Grok, Gemini, OpenAI)
  - Model field (context-aware examples)
  - Secure API key input (never stored on backend)
- **Source Documents panel**:
  - Shows retrieved chunks per tool call
  - Displays similarity scores, section paths, and expandable content previews
- **Execution Trace panel**:
  - Node executions with duration bars and input/output JSON
  - Routing decisions showing graph path and reasons
  - Original retrieval plan visualization
- **Session cache**: In-memory message cache for instant session switching without re-fetching

**Innovation**: Full transparency into the agent's reasoning — every response includes both the retrieved source chunks and a complete execution trace showing which nodes ran, why routing decisions were made, and how long each step took.

---

## Key Innovations Beyond Requirements

### 1. Multi-Turn Context Management

The system maintains conversation context across turns with automatic intent detection:

- **Follow-up queries** inherit prior context (operation logs, active API scope)
- **New intent detection** triggers context boundary reset to prevent pollution
- **Context start marker** limits the conversation window fed to the agent while keeping full history visible in UI

### 2. Structure-Aware Chunking

Two modes tested:

- **Granular mode** (chunk_size=1000) — initially used but **over-fragmented** parameter tables
- **Large mode** (chunk_size=4000, current) — keeps endpoint blocks and tables intact, significantly improved retrieval quality for field/parameter queries

Decision documented in README with rationale.

### 3. Metadata-Enriched Retrieval

ChromaDB chunks include:

- `api_class` — enables filtered retrieval (search only CUSTOMERS docs)
- `version` — enables version-specific or cross-version queries
- `source_file` — enables source traceability in UI

This reduces search space by ~8x for single-API queries.

### 4. CPU-Only Deployment Optimization

- Installs CPU-only PyTorch before `sentence-transformers` (saves ~1.3GB)
- Pre-downloads HuggingFace model at Docker build time (instant startup, no internet required in prod)
- Singleton embedding function with caching (initialized once per container)

### 5. Comprehensive Documentation

- **Backend README** (472 lines) — covers ingestion, agent pipeline, evaluation, API routes, deployment
- **Frontend README** (155 lines) — covers UI features with 5 screenshots
- **This overview** — unified project documentation
- **docs/DEPLOY.md** — step-by-step AWS EC2 guide
- **docs/CONVERSATION_MEMORY.md** — memory system design
- **src/eval/README.md** — evaluation pipeline details

---

## Quick Start

### Try the Live Demo

Visit [http://18.116.13.255](http://18.116.13.255) and:

1. Select a provider (Groq recommended)
2. Enter your API key (e.g., Groq: `gsk_...`)
3. Choose a model (e.g., `llama-3.3-70b-versatile`)
4. Try queries like:
   - "How do I create a customer in Stripe?"
   - "What are the differences between the Customer API in basil and clover?"
   - "What fields can I update on a subscription?"

### Run Locally (Backend)

```bash
git clone https://github.com/nsridh10/stripe-api-versiondoc-rag.git
cd stripe-api-versiondoc-rag
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python "src/test files/reingest_enriched.py"  # Ingest docs with pre-enriched metadata
uvicorn src.main:app --reload --port 8000
```

### Run Locally (Frontend)

```bash
git clone https://github.com/nsridh10/stripe-rag-frontend.git
cd stripe-rag-frontend
npm install
npm run dev
```

### Run Evaluation

```bash
cd stripe-api-versiondoc-rag
pip install -r requirements-eval.txt
export GROQ_API_KEY="your-key"
python -m src.eval.eval_llm
```

---

## Project Statistics

| Metric                  | Value                                             |
| ----------------------- | ------------------------------------------------- |
| Backend code            | ~5,000 lines (Python)                             |
| Frontend code           | ~2,000 lines (TypeScript/React)                   |
| Documentation           | ~1,200 lines (3 READMEs + deployment guide)       |
| Evaluation test cases   | 5 (covering RAG, edge cases, budget limits)       |
| Vector DB chunks        | ~150 (16 docs × ~2-3 chunks each with large mode) |
| API endpoints           | 8 (query, sessions CRUD, ingestion, health)       |
| LangGraph nodes         | 8 (frontier → synthesizer)                        |
| Supported LLM providers | 4 (Groq, Grok, Gemini, OpenAI)                    |
| Deployment containers   | 2 (FastAPI + nginx)                               |

---

## Evaluation Results Summary

Full results available in `data/eval/eval_report_20260302_094840.csv`.

**Summary Statistics**:

- Total test cases: 5
- Avg latency: 3.2s
- Avg tokens: 2,675
- Avg tool calls: 0.8

**Quality Metrics** (for RAG-processed queries):

- Faithfulness: 0.8–1.0 (answers grounded in retrieved docs)
- Answer Relevancy: 0.98–1.0 (addresses the question asked)
- Answer Correctness: 0.51–0.88 (compared to reference ground truth)

**Edge Case Validation**:

- Junk query ("What's the weather?") → correctly rejected at Frontier (0 tokens, 0 tools)
- Budget overflow query (8 lookups) → correctly caught by Budget Checker, user prompted to narrow query

---

## Technical Decisions & Trade-offs

### Why LangGraph over LangChain LCEL?

LangGraph enables **stateful, conditional routing** with retry logic and complex decision trees. The agent can:

- Route back to Query Expander on retrieval failures
- Skip synthesizer if budget is exhausted
- Dynamically adjust plans based on prior results

This level of control is difficult to express in LCEL's linear chain model.

### Why ChromaDB over Pinecone/Weaviate?

- **Local-first**: No external API dependencies or quotas
- **Embeddable**: Runs in-process with Python, simplifies deployment
- **Metadata filtering**: Native support for `where` clause filtering on `api_class` and `version`
- **Persistent storage**: File-based, no server management required

### Why CPU-only embeddings?

- **Cost**: AWS EC2 GPU instances are 3-5× more expensive
- **Latency**: bge-small-en-v1.5 embeds ~150 chunks in <1s on CPU
- **Assignment scope**: 16 documents don't require GPU acceleration

In production with thousands of documents, I'd use a dedicated embedding service (e.g., HuggingFace Inference API) or GPU-accelerated inference.

### Why RAGAS over custom metrics?

RAGAS provides **standardized, LLM-as-judge evaluation** with:

- Research-backed metrics (Faithfulness, Answer Relevancy from academic papers)
- HuggingFace Dataset integration
- Automated claim extraction and verification

Building equivalent custom metrics would require significant ML expertise and validation.

---

## Repository Structure

**Backend**: [stripe-api-versiondoc-rag](https://github.com/nsridh10/stripe-api-versiondoc-rag)

```
├── src/
│   ├── main.py              # FastAPI app
│   ├── graph/               # 8-node LangGraph pipeline
│   ├── prompts/             # System prompts for each node
│   ├── tools/               # search_stripe_api_docs tool
│   ├── routes/              # API endpoints
│   ├── eval/                # RAGAS evaluation framework
│   ├── ingestion.py         # Document parsing & embedding
│   ├── memory.py            # Session management
│   └── trace.py             # Execution trace collector
├── data/
│   ├── raw/                 # 16 Stripe API docs
│   ├── chroma_db/           # Vector store (gitignored)
│   └── eval/                # CSV evaluation reports
├── docs/
│   ├── DEPLOY.md            # AWS EC2 deployment guide
│   └── CONVERSATION_MEMORY.md
├── README.md                # Backend documentation
└── PROJECT_OVERVIEW.md      # This file
```

**Frontend**: [stripe-rag-frontend](https://github.com/nsridh10/stripe-rag-frontend)

```
├── src/
│   ├── App.tsx              # Main layout
│   ├── api.ts               # Backend API calls
│   ├── types.ts             # TypeScript interfaces
│   └── components/
│       ├── Sidebar.tsx      # Sessions + LLM config
│       ├── ChatArea.tsx     # Message bubbles
│       ├── SourcePanel.tsx  # Retrieved chunks
│       └── TracePanel.tsx   # Graph execution trace
├── screenshots/             # UI screenshots for README
└── README.md                # Frontend documentation
```

---

## Contact

**Developer**: Navein Sridhar  
**GitHub**: [nsridh10](https://github.com/nsridh10)  
**Repositories**:

- Backend: [stripe-api-versiondoc-rag](https://github.com/nsridh10/stripe-api-versiondoc-rag)
- Frontend: [stripe-rag-frontend](https://github.com/nsridh10/stripe-rag-frontend)

**Live Demo**: [http://18.116.13.255](http://18.116.13.255)

---

## License

MIT License — feel free to use this code for learning and portfolio purposes.
