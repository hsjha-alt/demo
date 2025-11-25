# Quick Setup Guide for PDF Chatbot

## Step-by-Step Installation

### Step 1: Install Ollama

1. **Download Ollama for Windows:**
   - Go to: https://ollama.ai
   - Click "Download" 
   - Download `OllamaSetup.exe`
   - Run the installer

2. **Verify Installation:**
   Open PowerShell or Command Prompt and run:
   ```bash
   ollama --version
   ```
   You should see the version number.

### Step 2: Download a Model

Open PowerShell/Command Prompt and run one of these:

**For quick testing (small & fast):**
```bash
ollama pull phi
```

**For better quality:**
```bash
ollama pull llama2
```

**Check if model is downloaded:**
```bash
ollama list
```

### Step 3: Install Python Dependencies

1. Open PowerShell/Command Prompt
2. Navigate to the pdf_chatbot folder:
   ```bash
   cd pdf_chatbot
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** This will download the embedding model (~80MB) on first use.

### Step 4: Run the Application

**Option A: Run everything together (Recommended)**
```bash
python main.py
```

**Option B: Run separately**

Terminal 1 - Start FastAPI:
```bash
python api.py
```

Terminal 2 - Start Gradio:
```bash
python gradio_app.py
```

### Step 5: Access the Application

1. Open your web browser
2. Go to: `http://localhost:7860`
3. Upload a PDF file
4. Start chatting!

## Troubleshooting

### "Ollama is not recognized"
- Make sure Ollama is installed
- Restart your terminal after installation
- Check if Ollama is in your PATH

### "Model not found"
- Make sure you downloaded a model: `ollama pull phi`
- Check installed models: `ollama list`

### "Cannot connect to API"
- Make sure FastAPI server is running
- Check if port 8000 is available

### "Port already in use"
- Close other applications using ports 8000 or 7860
- Or change ports in `api.py` and `gradio_app.py`

## Recommended Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| phi | ~1.6GB | ⚡⚡⚡ | ⭐⭐⭐ | Quick testing |
| tinyllama | ~637MB | ⚡⚡⚡ | ⭐⭐ | Fastest, smallest |
| llama2 | ~3.8GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced |
| mistral | ~4.1GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality |

## System Requirements

- **RAM:** At least 8GB (16GB recommended for larger models)
- **Storage:** 5-10GB free space for models
- **Python:** 3.8+ (you have 3.14, which is perfect!)
- **OS:** Windows 10/11, macOS, or Linux

## Next Steps

1. ✅ Install Ollama
2. ✅ Download a model
3. ✅ Install Python dependencies
4. ✅ Run the application
5. 🎉 Start chatting with your PDFs!

