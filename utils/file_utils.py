# utils/file_utils.py
import os
import streamlit as st
from config import PDFS_BASE_DIR
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_brain_directory(brain_name):
    """Get the directory path for a brain."""
    return os.path.join(PDFS_BASE_DIR, brain_name)

def upload_pdf(file, brain_name):
    """Upload a PDF to the brain's directory."""
    brain_dir = get_brain_directory(brain_name)
    os.makedirs(brain_dir, exist_ok=True)
    file_path = os.path.join(brain_dir, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

def load_pdf(file_path):
    """Load a PDF document."""
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def split_text(documents):
    """Split text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def list_uploaded_documents(brain_name):
    """List all uploaded PDF documents in the brain's directory."""
    brain_dir = get_brain_directory(brain_name)
    if os.path.exists(brain_dir):
        pdf_files = [f for f in os.listdir(brain_dir) if f.endswith(".pdf")]
        return pdf_files
    return []