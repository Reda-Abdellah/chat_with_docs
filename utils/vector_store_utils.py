# utils/vector_store_utils.py
from langchain_chroma import Chroma
from utils.llm_utils import embeddings

def get_vector_store(brain_name):
    """Get or create a Chroma vector store for a brain."""
    return Chroma(
        collection_name=brain_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )

def index_docs(documents, brain_name):
    """Index documents into the brain's vector store."""
    vector_store = get_vector_store(brain_name)
    existing_hashes = read_hashes(brain_name)  # Read existing hashes
    for doc in documents:
        doc_hash = generate_hash(doc.page_content)
        if doc_hash in existing_hashes:
            st.warning(f"Document with hash {doc_hash} already exists in the brain '{brain_name}'.")
            continue
        else:
            # Add the document to the vector store
            vector_store.add_documents([doc])
            write_hash(brain_name, doc_hash)  # Update the hash file
            st.success(f"Document with hash {doc_hash} added to the brain '{brain_name}'.")
    # vector_store.persist()

def retrieve_docs(query, brain_name):
    """Retrieve documents from the brain's vector store."""
    vector_store = get_vector_store(brain_name)
    if vector_store.get()['documents']:
        docs = vector_store.similarity_search(query)
    else:
        docs = []
    return docs