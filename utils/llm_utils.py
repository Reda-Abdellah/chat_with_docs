# utils/llm_utils.py
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config import OLLAMA_MODEL, OLLAMA_EMBEDDINGS_MODEL
from prompts.chat_with_docs import template

# Initialize embeddings and LLM
embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDINGS_MODEL)
model = OllamaLLM(model=OLLAMA_MODEL)

def answer_question(question, documents):
    """Generate an answer using the LLM."""
    if len(documents) > 0:
        context = "\n\n".join([doc.page_content for doc in documents])
    else:
        context = "No related documents were found."
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})