"""
Week 1 Demo Test — Run this to verify the full pipeline works end to end.
Expected output: retrieved chunks printed with sources and scores.
"""
import os
from vectorstore.chunker import chunk_document
from vectorstore.store import add_documents, clear_vector_store
from vectorstore.retriever import retrieve, retrieve_with_scores, format_chunks_for_prompt

# ── CONFIG ──────────────────────────────────────────────
# Updated to match your actual files in sample_docs
TEST_FILES = [
    ("sample_docs/test.pdf", "general"),
    ("sample_docs/test.docx", "general"),
    ("sample_docs/test.pptx", "general"),
    ("sample_docs/Operating_Systems.pdf","general"),
    ("sample_docs/test.png", "general"),
]

# Note: test.png is skipped in this version to avoid OCR errors.

TEST_QUERIES = [
    # Query 1: Specifically targeting the Demand Paging content from your PNG
    ("Explain the concept of Demand Paging and Page Faults", None, None),
    
    # Query 2: Checking for the process flow (Swapping/Lazy Swapper)
    ("What is the role of the pager or swapper in memory management?", None,None),
    
    # Query 3: General check for OS performance
    ("What are the advantages of using Demand Paging?", None, None),
    ("What is virtual file system?", None, None),
]
# ────────────────────────────────────────────────────────

def run_test():
    # Ensure sample_docs folder exists to avoid early crashes
    if not os.path.exists("sample_docs"):
        print("❌ Error: 'sample_docs' folder not found. Please create it.")
        return

    print("=" * 60)
    print("STEP 1: Clearing old vector store for clean test")
    print("=" * 60)
    clear_vector_store()

    print("\n" + "=" * 60)
    print("STEP 2: Processing and chunking documents")
    print("=" * 60)
    
    all_chunks = []
    for file_path, subject in TEST_FILES:
        if os.path.exists(file_path):
            chunks = chunk_document(file_path, subject=subject)
            all_chunks.extend(chunks)
        else:
            print(f"⚠️  Skipping {file_path}: File not found.")
    
    if not all_chunks:
        print("❌ No chunks created. Check if your PDFs/Docs have actual text.")
        return

    print(f"\nTotal chunks across all docs: {len(all_chunks)}")

    print("\n" + "=" * 60)
    print("STEP 3: Storing chunks in ChromaDB (HuggingFace Embeddings)")
    print("=" * 60)
    add_documents(all_chunks)

    print("\n" + "=" * 60)
    print("STEP 4: Testing retrieval queries")
    print("=" * 60)
    
    for query, doc_type, subject in TEST_QUERIES:
        print(f"\n🔍 Query: '{query}'")
        if doc_type:
            print(f"   Filter: doc_type={doc_type}")
        if subject:
            print(f"   Filter: subject={subject}")
        
        # Use the scoring retrieval to see how well it's working
        results = retrieve_with_scores(
            query=query,
            top_k=2,
            doc_type=doc_type,
            subject=subject
        )
        
        if not results:
            print("   ⚠️  No results found — check your filters or doc content")
            continue
            
        for doc, score in results:
            source = doc.metadata.get("source_file")
            page = doc.metadata.get("page_number")
            dtype = doc.metadata.get("doc_type")
            print(f"\n   📄 Relevance Score: {score:.3f} | {source} | Page {page} | {dtype}")
            print(f"   Preview: {doc.page_content[:150].replace('\n', ' ')}...")

    print("\n" + "=" * 60)
    print("STEP 5: Testing formatted output for LLM prompt")
    print("=" * 60)
    
    # Generic search for formatting test
    chunks = retrieve(TEST_QUERIES[0][0], top_k=2)
    formatted = format_chunks_for_prompt(chunks)
    print("\nFormatted context (this is what the Groq Agent will see):")
    print("-" * 30)
    print(formatted[:500] + "...")

    print("\n✅ Pipeline test complete!")
    print("If you see scores and previews, your Week 1 Backend is ready.")

if __name__ == "__main__":
    run_test()