# config.py
import os

# Constants
OLLAMA_MODEL = 'deepseek-r1:1.5b'
OLLAMA_EMBEDDINGS_MODEL = 'deepseek-r1:1.5b'
PDFS_BASE_DIR = 'pdfs/'
CHROMA_PERSIST_DIR = "./chroma_langchain_db"
HASH_FILE = "uploaded_hashes.txt"  # File to store hashes of uploaded documents

# Environment variables
os.environ['NO_PROXY'] = "http://127.0.0.1,localhost"