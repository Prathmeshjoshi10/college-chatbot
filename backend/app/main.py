from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Import our services
from app.services.rag_service import RAGService

# Load environment variables
load_dotenv()

# Check if API key is available
if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY not found in environment variables")

# Initialize FastAPI app
app = FastAPI(
    title="College Chatbot API",
    description="API for a college chatbot using Google Gemini LLM and RAG",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = None

@app.on_event("startup")
async def startup_event():
    global rag_service
    try:
        rag_service = RAGService()
        print("RAG service initialized successfully")
    except Exception as e:
        print(f"Error initializing RAG service: {e}")

# Define request and response models
class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not initialized")
    
    try:
        response, sources = await rag_service.generate_response(
            request.message, request.chat_history
        )
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "rag_service": rag_service is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
