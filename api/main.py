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

from fastapi import BackgroundTasks, UploadFile, File

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

@app.get("/api/ingest")
def ingest_data(background_tasks: BackgroundTasks):
    """
    Temporary endpoint to trigger data ingestion on the cloud server.
    Uses BackgroundTasks to prevent timeouts.
    """
    try:
        from scripts.chunk_and_embed import main as ingest_main
        background_tasks.add_task(ingest_main)
        return {"status": "success", "message": "Data ingestion started in the background!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/ingest")
async def upload_and_ingest(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a document and trigger ingestion in the background.
    """
    try:
        import os
        
        # Ensure processed directory exists
        proc_dir = os.path.join("data", "processed")
        os.makedirs(proc_dir, exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join(proc_dir, file.filename)
        with open(file_path, "wb") as buffer:
            import shutil
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger background ingestion
        from scripts.chunk_and_embed import main as ingest_main
        background_tasks.add_task(ingest_main)
        
        return {"status": "success", "message": f"File '{file.filename}' uploaded and ingestion started in the background!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
