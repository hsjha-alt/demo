"""
FastAPI Backend
Provides REST API endpoints for PDF processing and chat
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from chat_engine import ChatEngine
import numpy as np

app = FastAPI(title="PDF Chatbot API")

# Enable CORS for Gradio integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_processor = PDFProcessor()
vector_store = VectorStore()
chat_engine = ChatEngine()

# Global state
current_pdf_name = None


class ChatRequest(BaseModel):
    query: str
    top_k: int = 3


class ChatResponse(BaseModel):
    response: str
    context_used: int


@app.get("/")
async def root():
    return {"message": "PDF Chatbot API is running"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process PDF file
    """
    global current_pdf_name
    
    try:
        # Read PDF file
        pdf_bytes = await file.read()
        
        # Process PDF
        chunks, embeddings = pdf_processor.process_pdf(pdf_bytes)
        
        # Build vector store
        vector_store.build_index(embeddings, chunks)
        
        current_pdf_name = file.filename
        
        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "chunks": len(chunks),
            "status": "ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the PDF
    """
    try:
        # Generate query embedding
        query_embedding = pdf_processor.generate_embeddings([request.query])[0]
        
        # Search for relevant chunks
        context_chunks = vector_store.search(query_embedding, top_k=request.top_k)
        
        # Generate response
        result = chat_engine.chat(request.query, context_chunks)
        
        return ChatResponse(
            response=result["response"],
            context_used=len(context_chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def status():
    """
    Get current status
    """
    return {
        "pdf_loaded": vector_store.is_initialized,
        "current_pdf": current_pdf_name,
        "chunks_count": len(vector_store.chunks) if vector_store.is_initialized else 0,
        "ollama_connected": chat_engine.check_ollama_connection()
    }


@app.post("/clear")
async def clear():
    """
    Clear current PDF and conversation history
    """
    vector_store.clear()
    chat_engine.clear_history()
    global current_pdf_name
    current_pdf_name = None
    
    return {"message": "Cleared successfully"}


if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("Make sure Ollama is running: ollama serve")
    uvicorn.run(app, host="0.0.0.0", port=8000)

