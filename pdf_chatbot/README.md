# PDF Chatbot

A complete offline PDF chatbot application that allows you to upload PDF documents and chat with them using AI. The application uses Ollama for local LLM inference, FastAPI for the backend, and Gradio for the user interface.

## Features

- 📄 **PDF Upload**: Upload and process PDF documents
- 💬 **Chat Interface**: Ask questions about your PDF documents
- 🤖 **Local AI**: Uses Ollama for completely offline AI inference
- 🔍 **RAG (Retrieval Augmented Generation)**: Retrieves relevant context from PDF before answering
- 🌐 **Web Interface**: Beautiful Gradio UI for easy interaction
- ⚡ **FastAPI Backend**: RESTful API for PDF processing and chat

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Download from [https://ollama.ai](https://ollama.ai)
3. **Ollama Model** - Download a model (e.g., `llama2`, `mistral`, `phi`)

## Installation

### 1. Install Ollama

**For Windows:**
1. Visit [https://ollama.ai](https://ollama.ai) and click "Download"
2. Download the Windows installer (OllamaSetup.exe)
3. Run the installer and follow the setup wizard
4. Ollama will be added to your PATH automatically

**For macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Verify Installation:**
```bash
ollama --version
```

### 2. Start Ollama Service

**Windows:**
- Ollama runs as a service automatically after installation
- You can verify it's running by opening a new terminal and running:
```bash
ollama list
```

**Manual Start (if needed):**
```bash
ollama serve
```

### 3. Download a Model

In a terminal, download a model. For first-time users, we recommend starting with a smaller model:

**Small & Fast Models (Recommended for testing):**
```bash
ollama pull phi          # ~1.6GB - Very fast, good for testing
ollama pull tinyllama    # ~637MB - Smallest, fastest
```

**Medium Models (Better quality):**
```bash
ollama pull llama2       # ~3.8GB - Popular, balanced
ollama pull mistral      # ~4.1GB - High quality
```

**Large Models (Best quality, slower):**
```bash
ollama pull llama2:13b   # ~7.3GB - Better quality
ollama pull codellama    # ~3.8GB - Good for code
```

**Check installed models:**
```bash
ollama list
```

### 4. Install Python Dependencies

```bash
cd pdf_chatbot
pip install -r requirements.txt
```

**Note**: The first time you run the application, it will download the embedding model (`all-MiniLM-L6-v2`) which is about 80MB. This is a one-time download.

## Usage

### Option 1: Run Everything Together (Recommended)

```bash
python main.py
```

This will start both the FastAPI server and Gradio interface.

### Option 2: Run Separately

**Terminal 1 - Start FastAPI:**
```bash
python api.py
```

**Terminal 2 - Start Gradio:**
```bash
python gradio_app.py
```

### Access the Application

1. Open your browser and go to: `http://localhost:7860`
2. Upload a PDF file
3. Start chatting!

## Project Structure

```
pdf_chatbot/
├── api.py              # FastAPI backend server
├── gradio_app.py       # Gradio user interface
├── main.py             # Main application (runs both)
├── pdf_processor.py    # PDF text extraction and processing
├── vector_store.py     # FAISS vector store for similarity search
├── chat_engine.py      # Chat engine with Ollama integration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

1. **PDF Upload**: When you upload a PDF, the system:
   - Extracts text from all pages
   - Splits text into chunks
   - Generates embeddings for each chunk
   - Stores embeddings in a FAISS vector store

2. **Chatting**: When you ask a question:
   - Your question is converted to an embedding
   - Similar chunks are retrieved from the PDF
   - Context is sent to Ollama along with your question
   - Ollama generates an answer based on the PDF context

## API Endpoints

The FastAPI server provides these endpoints:

- `GET /` - API status
- `POST /upload-pdf` - Upload and process PDF
- `POST /chat` - Send a chat message
- `GET /status` - Get system status
- `POST /clear` - Clear current PDF and history

## Troubleshooting

### Ollama Connection Error

**Problem**: "Ollama is not connected"

**Solution**: 
- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Download the model: `ollama pull llama2`

### PDF Processing Error

**Problem**: "No text extracted from PDF"

**Solution**: 
- Make sure the PDF contains selectable text (not just images)
- Try a different PDF file

### Embedding Model Download

**Problem**: Slow first run

**Solution**: 
- The embedding model downloads automatically on first use (~80MB)
- This is a one-time download and will be cached

### Port Already in Use

**Problem**: Port 8000 or 7860 already in use

**Solution**: 
- Change ports in `api.py` and `gradio_app.py`
- Or stop the process using those ports

## Customization

### Change Ollama Model

Edit `chat_engine.py`:

```python
chat_engine = ChatEngine(model_name="mistral")  # or any other model
```

### Adjust Chunk Size

Edit `pdf_processor.py`:

```python
chunks = self.chunk_text(text, chunk_size=1000, overlap=100)
```

### Change Embedding Model

Edit `pdf_processor.py`:

```python
pdf_processor = PDFProcessor(model_name="all-mpnet-base-v2")  # Larger, more accurate
```

## License

This project is open source and available for personal and commercial use.

## Notes

- The application runs completely offline after initial setup
- First run will download the embedding model (~80MB)
- Make sure you have enough RAM for the LLM model (varies by model size)
- PDF processing works best with text-based PDFs (not scanned images)

