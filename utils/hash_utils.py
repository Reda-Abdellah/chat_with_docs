# utils/hash_utils.py
import hashlib

def generate_hash(document_content):
    """Generate a SHA-256 hash for the document content."""
    return hashlib.sha256(document_content.encode('utf-8')).hexdigest()

def read_hashes(brain_name):
    """Read the hashes of uploaded documents from the text file."""
    hash_file_path = os.path.join(get_brain_directory(brain_name), HASH_FILE)
    if os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as f:
            return set(f.read().splitlines())
    return set()

def write_hash(brain_name, doc_hash):
    """Write a new hash to the text file."""
    hash_file_path = os.path.join(get_brain_directory(brain_name), HASH_FILE)
    with open(hash_file_path, "a") as f:
        f.write(doc_hash + "\n")