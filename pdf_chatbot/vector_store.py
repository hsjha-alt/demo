"""
Vector Store Module
Handles document storage and similarity search using FAISS
"""
import faiss
import numpy as np
from typing import List, Dict, Tuple


class VectorStore:
    def __init__(self, dimension: int = 384):
        """
        Initialize FAISS vector store
        dimension: embedding dimension (384 for all-MiniLM-L6-v2)
        """
        self.dimension = dimension
        self.index = None
        self.chunks = []
        self.is_initialized = False
    
    def build_index(self, embeddings: np.ndarray, chunks: List[Dict]):
        """
        Build FAISS index from embeddings and store chunks
        """
        if len(embeddings) == 0:
            raise Exception("No embeddings provided")
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        self.index.add(embeddings)
        
        # Store chunks
        self.chunks = chunks
        self.is_initialized = True
        
        print(f"Vector store initialized with {len(chunks)} chunks")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        """
        Search for similar chunks
        Returns top_k most similar chunks with their metadata
        """
        if not self.is_initialized:
            raise Exception("Vector store not initialized. Please upload a PDF first.")
        
        # Normalize query embedding
        query_embedding = query_embedding.astype('float32')
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Retrieve chunks
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "score": float(distances[0][i]),
                    "rank": i + 1
                })
        
        return results
    
    def clear(self):
        """
        Clear the vector store
        """
        self.index = None
        self.chunks = []
        self.is_initialized = False
        print("Vector store cleared")

