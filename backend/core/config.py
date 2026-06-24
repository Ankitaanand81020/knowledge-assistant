import os
from dotenv import load_dotenv

# Load .env from backend root
load_dotenv()

# Environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

# Optional debug check
print("✅ CONFIG LOADED")
print("OLLAMA_URL =", OLLAMA_URL)
print("OLLAMA_MODEL =", OLLAMA_MODEL)