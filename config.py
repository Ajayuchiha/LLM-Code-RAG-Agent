import os
from dotenv import load_dotenv

load_dotenv()

# Ollama and vectorstore configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3")
VECTOR_DIR = os.getenv("VECTOR_DIR", "vectorstore")

# Export for convenience
CONFIG = {
    "OLLAMA_URL": OLLAMA_URL,
    "LLAMA_MODEL": LLAMA_MODEL,
    "VECTOR_DIR": VECTOR_DIR
}
