import sys
import os

# Add project root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, BackgroundTasks
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
    response_text = process_query(request.query)
    return ChatResponse(response=response_text)

@app.get("/api/ingest")
def ingest_data():
    """
    Trigger data ingestion synchronously so we can see errors.
    """
    try:
        from scripts.chunk_and_embed import main as ingest_main
        ingest_main()
        
        # After ingestion, reload the retriever's vectorstore
        from src import retriever, config
        from langchain_community.vectorstores import Chroma
        retriever.vectorstore = Chroma(
            persist_directory=config.CHROMA_PERSIST_DIR,
            embedding_function=retriever.embeddings,
            collection_name=config.CHROMA_COLLECTION_NAME
        )
        count = retriever.vectorstore._collection.count()
        return {"status": "success", "message": f"Ingestion complete! ChromaDB now has {count} chunks."}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

@app.get("/api/debug")
def debug_info():
    """
    Debug endpoint to check ChromaDB and config state.
    """
    try:
        from src import config, retriever
        count = retriever.vectorstore._collection.count()
        return {
            "chroma_persist_dir": config.CHROMA_PERSIST_DIR,
            "collection_name": config.CHROMA_COLLECTION_NAME,
            "chunk_count": count,
            "groq_api_key_set": bool(config.GROQ_API_KEY),
            "generation_model": config.GROQ_GENERATION_MODEL,
            "data_dir_exists": os.path.exists("data/processed"),
            "data_files": os.listdir("data/processed") if os.path.exists("data/processed") else [],
        }
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

