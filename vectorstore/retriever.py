from vectorstore.store import get_vector_store
from langchain_core.documents import Document

def retrieve_with_scores(query, top_k=5, doc_type=None, subject=None):
    vector_store = get_vector_store()
    where_filter = {}
    if doc_type: where_filter["doc_type"] = doc_type
    if subject: where_filter["subject"] = subject

    # Similarity search with scores
    if where_filter:
        return vector_store.similarity_search_with_relevance_scores(
            query=query, k=top_k, filter=where_filter
        )
    return vector_store.similarity_search_with_relevance_scores(query=query, k=top_k)

def retrieve_docs(query, k=4, doc_type=None, subject=None, score_threshold=0.1):
    """The main entry point for Person 1's agents."""
    results = retrieve_with_scores(query, top_k=k, doc_type=doc_type, subject=subject)
    
    filtered = []
    for doc, score in results:
        if score >= score_threshold:
            doc.metadata["relevance_score"] = round(score, 3)
            filtered.append(doc)
    return filtered