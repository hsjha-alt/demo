"""
Gradio UI Application
Provides user-friendly interface for PDF upload and chat
"""
import gradio as gr
import requests
import os
from typing import Tuple, List


# API endpoint
API_URL = "http://localhost:8000"


def upload_pdf(file) -> Tuple[str, str]:
    """
    Upload PDF to the backend
    """
    if file is None:
        return "Please select a PDF file", ""
    
    try:
        with open(file.name, "rb") as f:
            files = {"file": (os.path.basename(file.name), f, "application/pdf")}
            response = requests.post(f"{API_URL}/upload-pdf", files=files)
        
        if response.status_code == 200:
            data = response.json()
            return f"✅ PDF uploaded successfully!\n\nFilename: {data['filename']}\nChunks: {data['chunks']}", ""
        else:
            return f"❌ Error: {response.json().get('detail', 'Unknown error')}", ""
    except requests.exceptions.ConnectionError:
        return "❌ Error: Cannot connect to API. Make sure FastAPI server is running.", ""
    except Exception as e:
        return f"❌ Error: {str(e)}", ""


def chat(message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
    """
    Chat with the PDF
    """
    if not message.strip():
        return "", history
    
    try:
        # Check status first
        status_response = requests.get(f"{API_URL}/status")
        if status_response.status_code == 200:
            status = status_response.json()
            if not status["pdf_loaded"]:
                return "Please upload a PDF first!", history
            
            if not status["ollama_connected"]:
                return "Ollama is not connected. Please make sure Ollama is running and the model is available.", history
        
        # Send chat request
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": message, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data["response"]
            
            # Update history
            history.append([message, bot_response])
            return "", history
        else:
            error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
            history.append([message, error_msg])
            return "", history
    except requests.exceptions.ConnectionError:
        error_msg = "Cannot connect to API. Make sure FastAPI server is running."
        history.append([message, error_msg])
        return "", history
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append([message, error_msg])
        return "", history


def check_status() -> str:
    """
    Check system status
    """
    try:
        response = requests.get(f"{API_URL}/status")
        if response.status_code == 200:
            status = response.json()
            pdf_status = "✅ Loaded" if status["pdf_loaded"] else "❌ No PDF loaded"
            ollama_status = "✅ Connected" if status["ollama_connected"] else "❌ Not connected"
            
            return f"""
**System Status:**
- PDF: {pdf_status} ({status.get('current_pdf', 'N/A')})
- Chunks: {status.get('chunks_count', 0)}
- Ollama: {ollama_status}
"""
        else:
            return "❌ Cannot check status"
    except:
        return "❌ Cannot connect to API"


# Create Gradio interface
with gr.Blocks(title="PDF Chatbot") as demo:
    gr.Markdown(
        """
        # 📚 PDF Chatbot
        
        Upload a PDF document and chat with it using AI! This application runs completely offline.
        
        **Setup Instructions:**
        1. Make sure Ollama is installed and running: `ollama serve`
        2. Download a model: `ollama pull llama2` (or any other model)
        3. Start the FastAPI server: `python api.py`
        4. Then run this Gradio app: `python gradio_app.py`
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📄 Upload PDF")
            pdf_upload = gr.File(
                label="Select PDF File",
                file_types=[".pdf"],
                type="filepath"
            )
            upload_btn = gr.Button("Upload PDF", variant="primary")
            upload_status = gr.Textbox(
                label="Upload Status",
                lines=4,
                interactive=False
            )
            
            gr.Markdown("### ℹ️ System Status")
            status_btn = gr.Button("Check Status")
            status_display = gr.Markdown()
        
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat with PDF")
            chatbot = gr.Chatbot(
                label="Conversation",
                height=500
            )
            msg_input = gr.Textbox(
                label="Your Question",
                placeholder="Ask a question about the PDF...",
                lines=2
            )
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear Chat")
    
    # Event handlers
    upload_btn.click(
        fn=upload_pdf,
        inputs=[pdf_upload],
        outputs=[upload_status, msg_input]
    )
    
    status_btn.click(
        fn=check_status,
        outputs=status_display
    )
    
    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot]
    )
    
    send_btn.click(
        fn=chat,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot]
    )
    
    clear_btn.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, msg_input]
    )


if __name__ == "__main__":
    print("Starting Gradio app...")
    print("Make sure FastAPI server is running on http://localhost:8000")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, theme=gr.themes.Soft())

