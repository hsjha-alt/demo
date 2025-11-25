"""
Main Application
Runs both FastAPI and Gradio together
"""
import subprocess
import threading
import time
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import app as fastapi_app
import gradio as gr
from gradio_app import demo as gradio_demo


def run_fastapi():
    """Run FastAPI server in a separate thread"""
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info")


def run_gradio():
    """Run Gradio app in a separate thread"""
    time.sleep(2)  # Wait for FastAPI to start
    gradio_demo.launch(server_name="0.0.0.0", server_port=7860, share=False, theme=gr.themes.Soft())


if __name__ == "__main__":
    print("=" * 60)
    print("PDF Chatbot - Starting Application")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Make sure Ollama is running!")
    print("   Start Ollama with: ollama serve")
    print("   Download a model: ollama pull phi (or llama2, mistral)")
    print("\n" + "=" * 60)
    print("Starting FastAPI server on http://localhost:8000")
    print("Starting Gradio app on http://localhost:7860")
    print("=" * 60 + "\n")
    
    # Start FastAPI in a thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Start Gradio (blocking)
    run_gradio()

