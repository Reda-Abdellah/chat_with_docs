# app.py
import streamlit as st
from utils.file_utils import upload_pdf, list_uploaded_documents, get_brain_directory, split_text, load_pdf
from utils.vector_store_utils import index_docs, retrieve_docs
from utils.llm_utils import answer_question
from config import PDFS_BASE_DIR
import os

# Initialize session state for screen management
if "screen" not in st.session_state:
    st.session_state.screen = "select_brain"  # Default to the first screen

# Function to go back to the first screen
def go_to_select_brain():
    st.session_state.screen = "select_brain"

# First Screen: Select or Create a Brain
def select_brain_screen():
    st.title("Chat with Documents")
    os.makedirs(PDFS_BASE_DIR, exist_ok=True)

    # Brain Selection or Creation
    brains = [d for d in os.listdir(PDFS_BASE_DIR) if os.path.isdir(os.path.join(PDFS_BASE_DIR, d))]
    selected_brain = st.selectbox("Select a Brain", brains, index=0 if brains else None)
    new_brain = st.text_input("Or create a new brain")

    if new_brain:
        if new_brain in brains:
            st.warning(f"A brain named '{new_brain}' already exists.")
        else:
            brains.append(new_brain)
            selected_brain = new_brain
            os.makedirs(get_brain_directory(new_brain), exist_ok=True)  # Create directory for the new brain
            st.success(f"Created new brain: '{new_brain}'")

    if selected_brain:
        if st.button("Go to Brain"):
            st.session_state.screen = "brain_operations"
            st.session_state.selected_brain = selected_brain

# Second Screen: Upload, Chat, and Show Documents
def brain_operations_screen():
    st.title(f"Brain: {st.session_state.selected_brain}")

    # Add a button to go back to the first screen
    if st.button("Back to Brain Selection"):
        go_to_select_brain()

    # Show a scrolling list of uploaded documents
    st.subheader("Uploaded Documents")
    uploaded_documents = list_uploaded_documents(st.session_state.selected_brain)
    if uploaded_documents:
        st.write("Documents in this brain:")
        st.write(
            f'<div style="height: 150px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">'
            f'{"<br>".join(uploaded_documents)}'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.write("No documents have been uploaded to this brain yet.")

    # PDF Upload and Processing
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        accept_multiple_files=False
    )

    if uploaded_file:
        file_path = upload_pdf(uploaded_file, st.session_state.selected_brain)
        documents = load_pdf(file_path)
        chunked_documents = split_text(documents)
        index_docs(chunked_documents, st.session_state.selected_brain)
        st.rerun()  # Refresh the page to update the list of uploaded documents

    # Question Answering
    question = st.chat_input("Ask a question about the documents in this brain")
    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question, st.session_state.selected_brain)
        answer = answer_question(question, related_documents)
        st.chat_message("assistant").write(answer)

# Main App Logic
if st.session_state.screen == "select_brain":
    select_brain_screen()
elif st.session_state.screen == "brain_operations":
    brain_operations_screen()