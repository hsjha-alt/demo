"""
Chat Engine Module
Handles conversation with PDF using Ollama and RAG
"""
import ollama
from typing import List, Dict
import numpy as np


class ChatEngine:
    def __init__(self, model_name: str = "phi"):
        """
        Initialize chat engine with Ollama
        Make sure Ollama is running and the model is downloaded
        """
        self.model_name = model_name
        self.conversation_history = []
    
    def check_ollama_connection(self) -> bool:
        """
        Check if Ollama is running and model is available
        """
        try:
            # Try to list models
            models = ollama.list()
            available_models = [model['name'] for model in models.get('models', [])]
            
            # Check if our model is available
            if self.model_name not in available_models:
                print(f"Warning: Model '{self.model_name}' not found. Available models: {available_models}")
                print(f"Please run: ollama pull {self.model_name}")
                return False
            
            return True
        except Exception as e:
            print(f"Error connecting to Ollama: {str(e)}")
            print("Make sure Ollama is running. Start it with: ollama serve")
            return False
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generate response using RAG (Retrieval Augmented Generation)
        """
        # Build context from retrieved chunks
        context = "\n\n".join([
            f"Document excerpt {i+1}:\n{chunk['chunk']['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        # Create prompt with context
        prompt = f"""You are a helpful assistant that answers questions based on the provided document context.

Document Context:
{context}

Question: {query}

Please provide a detailed answer based on the document context above. If the context doesn't contain enough information to answer the question, please say so."""

        try:
            # Generate response using Ollama
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                stream=False
            )
            
            return response['response']
        except Exception as e:
            return f"Error generating response: {str(e)}. Make sure Ollama is running and the model is available."
    
    def chat(self, query: str, context_chunks: List[Dict]) -> Dict:
        """
        Complete chat function that generates response and updates history
        """
        response = self.generate_response(query, context_chunks)
        
        # Update conversation history
        self.conversation_history.append({
            "query": query,
            "response": response,
            "context_used": len(context_chunks)
        })
        
        return {
            "response": response,
            "context_chunks": context_chunks
        }
    
    def clear_history(self):
        """
        Clear conversation history
        """
        self.conversation_history = []

