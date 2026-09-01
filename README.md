# HDFC Mutual Fund FAQ Assistant

## Overview
A facts-only AI assistant tailored for HDFC mutual fund schemes, built using Retrieval-Augmented Generation (RAG). The system answers objective, verifiable queries by retrieving information exclusively from official, reliable sources. It features a robust multi-model setup to enforce strict guardrails, ensuring that the assistant provides **facts only** and never provides investment advice.

> **⚠️ Facts-only. No investment advice.**

## Key Features
- ✅ **Strict Guardrails**: Uses a lightweight classification model to aggressively block advisory, subjective, or PII (Personally Identifiable Information) queries before they even reach the main generation model.
- ✅ **Source-Grounded Generation**: Answers are explicitly constrained to the provided context retrieved from the vector database. Hallucinations are actively minimized.
- ✅ **Lightning-Fast Inference**: Uses Groq LPUs to power LLM generation, delivering near-instant responses.
- ✅ **Automated Data Pipeline**: GitHub Actions periodically run data ingestion scripts to scrape, clean, chunk, and embed the latest mutual fund data.
- ✅ **Modern UI**: A responsive, premium Next.js interface styled with Tailwind CSS, providing a delightful and seamless user experience.

## Tech Stack

| Component | Technology |
|---|---|
| **Primary LLM** | Groq (`llama-3.3-70b-versatile`) |
| **Guardrail LLM** | Groq (`llama-3.1-8b-instant` / `qwen-2.5`) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (Local execution) |
| **Vector Database** | ChromaDB (SQLite-backed) |
| **Frontend** | Next.js (React), Tailwind CSS, Lucide Icons |
| **Backend** | FastAPI, Python, LangChain |
| **Hosting** | Vercel (Frontend) & Railway (Backend) |

## Supported Schemes
Currently, the knowledge base holds context for the following diverse HDFC schemes:

| # | Scheme | Category |
|---|---|---|
| 1 | HDFC Mid-Cap Fund Direct Growth | Mid-Cap |
| 2 | HDFC Small Cap Fund Direct Growth | Small-Cap |
| 3 | HDFC Gold ETF Fund of Fund Direct Plan Growth | Gold / FoF |
| 4 | HDFC Large Cap Fund Direct Growth | Large-Cap |
| 5 | HDFC ELSS Tax Saver Fund Direct Plan Growth | ELSS (Tax Saver) |

---

## Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mraodeo/RAG-Project-Grow.git
cd RAG-Project-Grow
```

### 2. Backend Setup (FastAPI + ChromaDB)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright (used for scraping)
playwright install chromium

# Configure Environment Variables
copy .env.example .env
# Open .env and add your GROQ_API_KEY
```

### 3. Run the Data Pipeline
Before you can chat, you must populate the local Chroma vector database:
```bash
python scripts/scrape.py
python scripts/clean.py
python scripts/chunk_and_embed.py
```

### 4. Launch the Application
You need to run both the backend and frontend simultaneously in separate terminals.

**Terminal 1 (Backend):**
```bash
uvicorn api.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm run dev
```
The application will now be available at `http://localhost:3000`.

---

## Deployment

This repository is configured for modern serverless deployment.

### Backend (Railway)
1. Connect your GitHub repository to [Railway](https://railway.app/).
2. Railway will automatically detect the `Procfile` (`web: uvicorn api.main:app --host 0.0.0.0 --port $PORT`) and `requirements.txt`.
3. Add your `GROQ_API_KEY` to the Railway Environment Variables.
4. *Note:* A failsafe is built into `config.py` that automatically copies the local ChromaDB SQLite files to `/tmp` in ephemeral environments like Railway, circumventing read-only filesystem restrictions.

### Frontend (Vercel)
1. Import the project into [Vercel](https://vercel.com/).
2. **Crucial:** Set the **Root Directory** to `frontend`.
3. The `next.config.ts` handles API routing by rewriting `/api/:path*` to your live Railway backend URL.

---

## Project Structure
```text
RAG-Project/
├── .github/workflows/      # GitHub Actions for automated cron jobs
├── api/                    # FastAPI entry points & route handlers
├── docs/                   # Markdown documentation & architectural diagrams
├── data/                   # Raw HTML and cleaned text documents
├── scripts/                # ETL pipeline scripts (scrape, clean, embed)
├── src/                    # Core RAG logic (retriever, guardrails, LLM pipeline)
├── vectorstore/            # Local ChromaDB persistent storage (SQLite)
├── frontend/               # Next.js React frontend
├── tests/                  # Unit and integration tests
├── eval/                   # Benchmarks, datasets, and evaluation scripts
├── .env.example            # Environment variable template
├── requirements.txt        # Python backend dependencies
└── README.md               # Project documentation
```

## Known Limitations
- **Data Freshness**: The corpus is updated daily via automated GitHub Actions; intraday NAV fluctuations or highly real-time market data is not tracked.
- **Scope**: Designed specifically for 5 targeted HDFC schemes.
- **Conversation State**: The system handles single-turn queries. Contextual multi-turn conversation memory is intentionally omitted to prevent hallucination drift.

## Disclaimer
> **Facts-only. No investment advice.**
>
> This AI assistant provides factual information strictly sourced from public mutual fund documents. It does not offer investment advice, opinions, predictions, or recommendations. For financial guidance, please consult a SEBI-registered advisor.

## License
This project is for educational and demonstrative purposes only.
