# Mutual Fund FAQ Assistant

## Overview
A facts-only FAQ assistant for HDFC mutual fund schemes, built using Retrieval-Augmented Generation (RAG). The system answers objective, verifiable queries by retrieving information exclusively from official public sources (AMC, AMFI, SEBI).

> **⚠️ Facts-only. No investment advice.**

## Features
- ✅ Facts-only answers with source citations
- ✅ Guardrail: refuses advisory and PII queries
- ✅ Covers 5 HDFC schemes across diverse categories
- ✅ Ultra-fast inference via Groq LPU

## Tech Stack

| Component | Technology |
|---|---|
| **LLM** | Groq (`llama-3.3-70b-versatile`) |
| **Guardrail LLM** | Groq (`llama-3.1-8b-instant`) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (local) |
| **Vector Store** | ChromaDB |
| **Frontend** | Next.js (React) on Vercel |
| **Backend** | FastAPI (Python) on Railway |
| **Framework** | LangChain |
| **Language** | Python 3.10+ / TypeScript |

## Supported Schemes

| # | Scheme | Category |
|---|---|---|
| 1 | HDFC Mid-Cap Fund Direct Growth | Mid-Cap |
| 2 | HDFC Small Cap Fund Direct Growth | Small-Cap |
| 3 | HDFC Gold ETF Fund of Fund Direct Plan Growth | Gold / FoF |
| 4 | HDFC Large Cap Fund Direct Growth | Large-Cap |
| 5 | HDFC ELSS Tax Saver Fund Direct Plan Growth | ELSS (Tax Saver) |

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd RAG-Project
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser
```bash
playwright install chromium
```

### 5. Configure Environment
```bash
copy .env.example .env
# Edit .env and add your Groq API key
```

### 6. Verify Groq API Connection
```bash
python scripts/verify_groq.py
```

### 7. Run Data Ingestion Pipeline
```bash
python scripts/scrape.py
python scripts/clean.py
python scripts/chunk_and_embed.py
```

### 8. Launch the Backend (FastAPI)
```bash
uvicorn api.main:app --reload
```

### 9. Launch the Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
The application will be available at `http://localhost:3000`.

## Project Structure
```
RAG-Project/
├── .github/workflows/      # GitHub Actions for daily data ingestion
├── api/                    # FastAPI backend endpoints
├── docs/                   # Documentation
├── data/                   # Raw and processed data
├── scripts/                # Data pipeline scripts
├── src/                    # Core application code
├── vectorstore/            # ChromaDB persistent storage
├── frontend/               # Next.js React frontend
├── tests/                  # Test suite
├── eval/                   # Evaluation datasets & results
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Architecture
See [docs/Architecture.md](docs/Architecture.md) for the detailed system design.

## Known Limitations
- Data corpus is automatically updated daily via GitHub Actions, but real-time intraday data is not available.
- HDFC schemes only — not multi-AMC
- No multi-turn conversation — each query is independent
- Depends on Groq API availability

## Disclaimer
> **Facts-only. No investment advice.**
>
> This assistant provides factual information only. It does not offer investment advice, opinions, or recommendations. For investment guidance, please consult a SEBI-registered advisor.

## License
This project is for educational purposes only.
