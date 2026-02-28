from vectorstore.store import get_vector_store
from langchain_core.documents import Document

def retrieve(
    query: str,
    top_k: int = 5,
    doc_type: str = None,      # e.g. "pyq", "notes", "textbook"
    subject: str = None         # e.g. "dbms", "os"
) -> list[Document]:
    """
    Main retrieval function.
    Returns top_k most relevant chunks, optionally filtered by metadata.
    
    Usage examples:
        retrieve("explain B+ trees")
        retrieve("solve Q3 from 2022 paper", doc_type="pyq")
        retrieve("normalization", subject="dbms", top_k=8)
    """
    vector_store = get_vector_store()

    # Build metadata filter if any filters were provided
    where_filter = {}
    if doc_type:
        where_filter["doc_type"] = doc_type
    if subject:
        where_filter["subject"] = subject

    # Perform similarity search
    if where_filter:
        results = vector_store.similarity_search(
            query=query,
            k=top_k,
            filter=where_filter
        )
    else:
        results = vector_store.similarity_search(
            query=query,
            k=top_k
        )

    return results

def retrieve_with_scores(
    query: str,
    top_k: int = 5,
    doc_type: str = None,
    subject: str = None
) -> list[tuple[Document, float]]:
    """
    Same as retrieve() but also returns similarity scores.
    Useful for debugging — if scores are low, your chunks are bad.
    Score is between 0-1, higher = more relevant.
    """
    vector_store = get_vector_store()

    where_filter = {}
    if doc_type:
        where_filter["doc_type"] = doc_type
    if subject:
        where_filter["subject"] = subject

    if where_filter:
        results = vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=top_k,
            filter=where_filter
        )
    else:
        results = vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=top_k
        )

    return results

def format_chunks_for_prompt(chunks: list[Document]) -> str:
    """
    Converts retrieved chunks into a clean string for LLM prompts.
    Every agent will use this to build context.
    """
    formatted = []
    for i, doc in enumerate(chunks):
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page_number", "?")
        doc_type = doc.metadata.get("doc_type", "unknown")
        
        formatted.append(
            f"[Source {i+1}: {source} | Page {page} | Type: {doc_type}]\n"
            f"{doc.page_content}"
        )
    
    # Ensure this return is OUTSIDE the for loop
    return "\n\n---\n\n".join(formatted)