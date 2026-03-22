import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vectorstore.store import get_vector_store
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import re

def tokenize(text):
    """Simple tokenization: lowercase, remove punctuation, split."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()


def normalize_doc_type_filter(doc_type):
    """Normalize doc_type to None, string, or list of strings."""
    if doc_type is None:
        return None

    if isinstance(doc_type, str):
        cleaned = [entry.strip().lower() for entry in doc_type.split(",") if entry.strip()]
        if not cleaned:
            return None
        if len(cleaned) == 1:
            return cleaned[0]
        return cleaned

    if isinstance(doc_type, (list, tuple, set)):
        cleaned = [str(entry).strip().lower() for entry in doc_type if str(entry).strip()]
        if not cleaned:
            return None
        return list(dict.fromkeys(cleaned))  # preserve uniqueness

    raise ValueError("doc_type must be None, str, list, tuple, or set")


def get_bm25_results(query, top_k=5, doc_type=None, subject=None):
    vector_store = get_vector_store()
    
    # Normalize and support multiple doc_type values.
    doc_type = normalize_doc_type_filter(doc_type)

    # Get all documents
    all_docs = vector_store.get()
    documents = []
    metadatas = []
    ids = []
    
    for i, doc_id in enumerate(all_docs['ids']):
        metadata = all_docs['metadatas'][i]

        if doc_type:
            actual_type = (metadata.get('doc_type') or "").lower()
            if isinstance(doc_type, list):
                if actual_type not in doc_type:
                    continue
            elif actual_type != doc_type:
                continue

        if subject and metadata.get('subject') != subject:
            continue

        documents.append(all_docs['documents'][i])
        metadatas.append(metadata)
        ids.append(doc_id)
    
    if not documents:
        return []
    
    # Tokenize corpus
    corpus = [tokenize(doc) for doc in documents]
    
    # Build BM25 index
    bm25 = BM25Okapi(corpus)
    
    # Tokenize query
    query_tokens = tokenize(query)
    
    # Get scores
    scores = bm25.get_scores(query_tokens)
    
    # Get top k indices
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    
    results = []
    for idx in top_indices:
        if scores[idx] > 0:  # Only include if score > 0
            metadata = metadatas[idx].copy()
            metadata['id'] = ids[idx]  # Add id to metadata for uniqueness
            doc = Document(page_content=documents[idx], metadata=metadata)
            results.append((doc, scores[idx]))
    
    return results

def retrieve_with_scores(query, top_k=5, doc_type=None, subject=None):
    vector_store = get_vector_store()
    doc_type = normalize_doc_type_filter(doc_type)

    # Build filter for Chroma. If multiple values, use $in; otherwise exact match.
    where_filter = {}
    if subject:
        where_filter["subject"] = subject

    if doc_type:
        if isinstance(doc_type, list):
            where_filter["doc_type"] = {"$in": doc_type}
        else:
            where_filter["doc_type"] = doc_type

    # Similarity search with scores
    if where_filter:
        try:
            results = vector_store.similarity_search_with_relevance_scores(
                query=query,
                k=top_k,
                filter=where_filter
            )
        except Exception:
            # Fallback: fetch from unfiltered and apply client-side doc_type filter.
            results = vector_store.similarity_search_with_relevance_scores(query=query, k=top_k*3)

            if doc_type:
                filtered = []
                allowed = set(doc_type) if isinstance(doc_type, list) else {doc_type}
                for doc, score in results:
                    if (doc.metadata.get("doc_type") or "").lower() in allowed:
                        filtered.append((doc, score))
                return filtered[:top_k]

        return results

    return vector_store.similarity_search_with_relevance_scores(query=query, k=top_k)

def merge_results(vector_results, bm25_results, top_k=4):
    """Merge vector and BM25 results, removing duplicates and keeping top k."""
    seen_ids = set()
    merged = []
    
    # Add vector results first
    for doc, score in vector_results:
        doc_id = doc.metadata.get('id', doc.page_content[:100])  # Use id or first 100 chars as unique key
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            merged.append((doc, score, 'vector'))
    
    # Add BM25 results
    for doc, score in bm25_results:
        doc_id = doc.metadata.get('id', doc.page_content[:100])
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            merged.append((doc, score, 'bm25'))
    
    # Sort by score descending
    merged.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k
    return merged[:top_k]

def retrieve_docs(query, k=4, doc_type=None, subject=None, score_threshold=-1):
    """The main entry point for Person 1's agents. Now uses both vector and BM25 search."""
    # Get vector results
    vector_results = retrieve_with_scores(query, top_k=k*2, doc_type=doc_type, subject=subject)
    
    # Get BM25 results
    bm25_results = get_bm25_results(query, top_k=k*2, doc_type=doc_type, subject=subject)
    
    # Merge results
    merged = merge_results(vector_results, bm25_results, top_k=k)
    
    filtered = []
    for doc, score, source in merged:
        if score >= score_threshold:
            doc.metadata["relevance_score"] = round(score, 3)
            doc.metadata["search_source"] = source
            filtered.append(doc)
    return filtered
if __name__ == "__main__":
    test_queries = [
        "Explain Banker's algorithm",
        "What is demand paging",
    ]
    for query in test_queries:
        print(f"\nQuery: {query}")
        docs = retrieve_docs(query, k=4)
        print(f"Chunks returned: {len(docs)}")
        for doc in docs:
            print(f"  Source: {doc.metadata.get('source_file')} | Page: {doc.metadata.get('page_number')}")
            print(f"  Preview: {doc.page_content[:100]}...")