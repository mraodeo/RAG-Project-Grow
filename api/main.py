import sys
import os

# Add project root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import process_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Mutual Fund API")

# Allow CORS for local development (Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mutual Fund RAG API is running"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Process a chat query using the RAG pipeline.
    """
    # The pipeline is fully synchronous right now
    # If the user hits a rate limit, the pipeline will return an error string
    response_text = process_query(request.query)
    return ChatResponse(response=response_text)
