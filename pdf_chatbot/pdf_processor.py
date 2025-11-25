"""
PDF Processing Module
Handles PDF text extraction, chunking, and embedding generation
"""
import PyPDF2
import io
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np


class PDFProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize PDF processor with embedding model
        Uses a lightweight model that runs offline
        """
        print(f"Loading embedding model: {model_name}...")
        self.embedding_model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully!")
    
    def extract_text_from_pdf(self, pdf_file: bytes) -> str:
        """
        Extract text from PDF file
        """
        try:
            pdf_file_obj = io.BytesIO(pdf_file)
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """
        Split text into chunks with overlap
        Returns list of dictionaries with text and metadata
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "chunk_id": len(chunks),
                "start_word": i,
                "end_word": min(i + chunk_size, len(words))
            })
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        """
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def process_pdf(self, pdf_file: bytes) -> tuple:
        """
        Complete PDF processing pipeline
        Returns: (chunks, embeddings)
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_file)
        
        if not text:
            raise Exception("No text extracted from PDF")
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        # Generate embeddings
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = self.generate_embeddings(chunk_texts)
        
        return chunks, embeddings

