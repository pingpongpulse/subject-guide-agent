import os
import shutil
from langchain_chroma import Chroma  # Updated import for newer versions
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Path where ChromaDB saves data to disk
CHROMA_PATH = "./chroma_db"

def get_embedding_function():
    """
    Returns a FREE local embedding model. 
    'all-MiniLM-L6-v2' is small, fast, and perfect for college notes.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store() -> Chroma:
    """Load or create the ChromaDB vector store."""
    embeddings = get_embedding_function()
    
    return Chroma(
        collection_name="academic_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

def add_documents(documents: list[Document]) -> None:
    """Adds Document chunks to the vector store."""
    if not documents:
        print("⚠️ No documents to add.")
        return

    vector_store = get_vector_store()
    
    # Process in batches
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vector_store.add_documents(batch)
        print(f"  Added batch {i//batch_size + 1} ({len(batch)} chunks)")

    print(f"✅ Total {len(documents)} chunks successfully stored in ChromaDB")

def clear_vector_store() -> None:
    """Deletes the existing database. Use this if you change your embedding model."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("🗑️ Vector store cleared.")