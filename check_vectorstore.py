#!/usr/bin/env python3
"""Diagnostic script to check ChromaDB contents"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vectorstore.store import get_vector_store
from vectorstore.retriever import retrieve_docs

print("[*] Checking ChromaDB...")
print(f"[*] Working directory: {os.getcwd()}")
print(f"[*] Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Try to get vector store
try:
    vector_store = get_vector_store()
    print("[OK] Vector store loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load vector store: {e}")
    sys.exit(1)

# Check ChromaDB contents
try:
    all_docs = vector_store.get()
    doc_count = len(all_docs['ids'])
    print(f"[OK] ChromaDB contains {doc_count} documents")
    
    if doc_count > 0:
        print(f"[OK] Sample documents:")
        for i in range(min(5, len(all_docs['ids']))):
            print(f"  {i+1}. {all_docs['metadatas'][i]}")
    else:
        print("[WARN] No documents in ChromaDB!")
except Exception as e:
    print(f"[ERROR] Failed to read documents: {e}")
    import traceback
    traceback.print_exc()

# Try a retrieval test
print("\n[*] Testing document retrieval...")
try:
    query = "Explain Deadlock in OS"
    docs = retrieve_docs(query, k=5)
    print(f"[OK] Retrieved {len(docs)} documents for query: {query}")
    
    if docs:
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc.metadata.get('source_file')} (Page {doc.metadata.get('page_number')})")
            print(f"     Type: {doc.metadata.get('doc_type')} | Subject: {doc.metadata.get('subject')}")
            print(f"     Preview: {doc.page_content[:60]}...")
    else:
        print("[WARN] No documents retrieved!")
except Exception as e:
    print(f"[ERROR] Retrieval failed: {e}")
    import traceback
    traceback.print_exc()

print("\n[OK] Diagnostics complete!")
