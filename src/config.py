"""
Centralized configuration for the Mutual Fund FAQ Assistant.
Loads environment variables and defines all constants used across modules.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# ──────────────────────────────────────────────
# Groq API Configuration
# ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_GENERATION_MODEL = os.getenv("GROQ_GENERATION_MODEL", "openai/gpt-oss-120b")
GROQ_GUARDRAIL_MODEL = os.getenv("GROQ_GUARDRAIL_MODEL", "qwen/qwen3.6-27b")

# ──────────────────────────────────────────────
# Embedding Configuration
# ──────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# ──────────────────────────────────────────────
# ChromaDB Configuration
# ──────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./vectorstore/chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "mutual_fund_faq")

# ──────────────────────────────────────────────
# Retrieval Configuration
# ──────────────────────────────────────────────
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))
RETRIEVAL_SEARCH_TYPE = os.getenv("RETRIEVAL_SEARCH_TYPE", "similarity")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))

# ──────────────────────────────────────────────
# LLM Generation Configuration
# ──────────────────────────────────────────────
LLM_TEMPERATURE = 0        # Deterministic for factual answers
LLM_MAX_TOKENS = 256       # Short responses only
MAX_QUERY_LENGTH = 500      # Truncate queries beyond this length

# ──────────────────────────────────────────────
# Target Schemes
# ──────────────────────────────────────────────
TARGET_SCHEMES = {
    "hdfc_midcap": {
        "name": "HDFC Mid-Cap Fund Direct Growth",
        "category": "Mid-Cap",
        "url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    },
    "hdfc_smallcap": {
        "name": "HDFC Small Cap Fund Direct Growth",
        "category": "Small-Cap",
        "url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
    },
    "hdfc_gold_fof": {
        "name": "HDFC Gold ETF Fund of Fund Direct Plan Growth",
        "category": "Gold / FoF",
        "url": "https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth",
    },
    "hdfc_largecap": {
        "name": "HDFC Large Cap Fund Direct Growth",
        "category": "Large-Cap",
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
    },
    "hdfc_elss": {
        "name": "HDFC ELSS Tax Saver Fund Direct Plan Growth",
        "category": "ELSS (Tax Saver)",
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    },
}

# ──────────────────────────────────────────────
# Refusal & Safety Configuration
# ──────────────────────────────────────────────
AMFI_EDUCATION_URL = "https://www.amfiindia.com/investor-corner/knowledge-center.html"
SEBI_INVESTOR_URL = "https://investor.sebi.gov.in/"

# ──────────────────────────────────────────────
# System Prompts
# ──────────────────────────────────────────────
GENERATION_SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant.

STRICT RULES:
1. Answer ONLY using the provided context. Do NOT use any outside knowledge.
2. Keep your response to a MAXIMUM of 3 sentences.
3. If the context does not contain the answer, respond exactly with:
   "I don't have this information in my current sources."
4. NEVER provide investment advice, opinions, or recommendations.
5. NEVER compare fund performance or calculate returns.
6. Do NOT include any source links or date footers in your answer.

CONTEXT:
{context}

USER QUESTION:
{question}"""

GUARDRAIL_SYSTEM_PROMPT = """Classify the following user query into exactly one category.
Respond with ONLY the category name, nothing else.

Categories:
- FACTUAL: Questions asking for specific facts about mutual fund schemes
  (expense ratio, exit load, SIP amount, benchmark, riskometer, lock-in, NAV, AUM, fund manager)
- ADVISORY: Questions seeking investment advice, opinions, recommendations,
  comparisons, or return predictions
- OUT_OF_SCOPE: Questions unrelated to HDFC mutual fund schemes

Query: "{query}"

Category:"""

# ──────────────────────────────────────────────
# Startup Validation
# ──────────────────────────────────────────────
def validate_config():
    """Validate that critical configuration values are present."""
    errors = []

    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY is not set. Add it to your .env file.")

    if not GROQ_API_KEY or GROQ_API_KEY == "gsk_your_groq_api_key_here":
        errors.append("GROQ_API_KEY is still the placeholder value. Replace it with your actual key.")

    if errors:
        raise ValueError(
            "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )


if __name__ == "__main__":
    # Quick validation check
    try:
        validate_config()
        print("✅ Configuration is valid.")
        print(f"   Groq Generation Model: {GROQ_GENERATION_MODEL}")
        print(f"   Groq Guardrail Model:  {GROQ_GUARDRAIL_MODEL}")
        print(f"   Embedding Model:       {EMBEDDING_MODEL}")
        print(f"   ChromaDB Dir:          {CHROMA_PERSIST_DIR}")
        print(f"   Collection:            {CHROMA_COLLECTION_NAME}")
        print(f"   Top-K:                 {RETRIEVAL_TOP_K}")
        print(f"   Similarity Threshold:  {SIMILARITY_THRESHOLD}")
    except ValueError as e:
        print(f"❌ {e}")
