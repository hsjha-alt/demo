"""
Ollama Connection Diagnostic Tool
Checks if Ollama is properly configured and accessible
"""
import sys

def check_ollama():
    """Check Ollama connection and model availability"""
    print("=" * 60)
    print("Ollama Connection Diagnostic")
    print("=" * 60)
    
    # Check if ollama module is installed
    try:
        import ollama
        print("[OK] Ollama Python library is installed")
    except ImportError:
        print("[ERROR] Ollama Python library is not installed")
        print("   Run: pip install ollama")
        return False
    
    # Check if Ollama service is running
    try:
        models = ollama.list()
        print("[OK] Ollama service is running and accessible")
    except Exception as e:
        print(f"[ERROR] Cannot connect to Ollama service: {str(e)}")
        print("   Make sure Ollama is installed and running")
        print("   On Windows, Ollama usually runs as a service automatically")
        print("   You can also start it manually: ollama serve")
        return False
    
    # List available models
    available_models = [model['name'] for model in models.get('models', [])]
    print(f"\n[INFO] Available models: {available_models}")
    
    # Check for common models
    common_models = ['phi', 'llama2', 'mistral', 'gemma']
    found_models = []
    for model in common_models:
        for available in available_models:
            if available.startswith(model):
                found_models.append(available)
                break
    
    if found_models:
        print(f"[OK] Found compatible models: {found_models}")
    else:
        print("[WARNING] No common models found. You may need to download one:")
        print("   ollama pull phi        (small, fast)")
        print("   ollama pull llama2     (better quality)")
        print("   ollama pull mistral    (good balance)")
    
    # Test model generation
    if available_models:
        test_model = available_models[0]
        try:
            print(f"\n[TEST] Testing model generation with '{test_model}'...")
            response = ollama.generate(
                model=test_model,
                prompt="Say hello",
                stream=False
            )
            if 'response' in response:
                print("[OK] Model generation test: SUCCESS")
                preview = response['response'][:50].encode('ascii', 'ignore').decode('ascii')
                print(f"   Response preview: {preview}...")
            else:
                print("[WARNING] Model generation returned unexpected format")
        except Exception as e:
            print(f"[ERROR] Model generation test failed: {str(e)}")
            return False
    
    print("\n" + "=" * 60)
    print("[OK] All checks passed! Ollama is ready to use.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = check_ollama()
    sys.exit(0 if success else 1)

