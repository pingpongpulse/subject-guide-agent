import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vectorstore.retriever import retrieve_docs, retrieve_with_scores
from utils.context_formatter import format_context, format_sources_list

QUERIES = [
    {"query": "Explain demand paging", "doc_type": None, "subject": None},
    {"query": "What is virtual file system", "doc_type": None, "subject": None},
    {"query": "Advantages of demand paging", "doc_type": None, "subject": None},
    {"query": "Explain demand paging", "doc_type": None, "subject": "os"},
    {"query": "What is virtual file system", "doc_type": None, "subject": "os"},
]


def setup_test_data():
    from vectorstore.chunker import chunk_document
    from vectorstore.store import add_documents, clear_vector_store

    print("=" * 60)
    print("SETUP: Loading documents into ChromaDB")
    print("=" * 60)

    sample_folder = "sample_docs"
    if not os.path.exists(sample_folder):
        print("❌ sample_docs folder not found.")
        return

    supported = ["pdf", "docx", "pptx", "png", "jpg"]
    files = [f for f in os.listdir(sample_folder)
             if f.split(".")[-1].lower() in supported]

    if not files:
        print("❌ No files found in sample_docs/")
        return

    clear_vector_store()
    all_chunks = []

    for file_name in files:
        file_path = os.path.join(sample_folder, file_name)
        try:
            # Assign subject based on filename
            if "operating" in file_name.lower():
                subject = "os"
            elif "database" in file_name.lower() or "dbms" in file_name.lower():
                subject = "dbms"
            elif "network" in file_name.lower() or "cn" in file_name.lower():
                subject = "cn"
            else:
                subject = "general"
            
            chunks = chunk_document(file_path, subject=subject)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"⚠️  Skipped {file_name}: {e}")

    if all_chunks:
        add_documents(all_chunks)
        print(f"✅ {len(all_chunks)} chunks loaded from {len(files)} files\n")


def test_basic_retrieval():
    print("=" * 60)
    print("TEST 1: Basic Retrieval with Scores")
    print("=" * 60)

    for item in QUERIES:
        query = item["query"]
        print(f"\n🔍 Query: '{query}'")

        results = retrieve_with_scores(query=query, top_k=3)

        if not results:
            print("   ⚠️  No results returned")
            continue

        for doc, score in results:
            source = doc.metadata.get("source_file")
            page = doc.metadata.get("page_number")
            preview = doc.page_content[:120].replace("\n", " ")
            print(f"   📄 Score: {score:.3f} | {source} | Page {page}")
            print(f"       Preview: {preview}...")


def test_metadata_filtering():
    print("\n" + "=" * 60)
    print("TEST 2: Metadata Filtering")
    print("=" * 60)

    print("\n🔍 Filter: doc_type='notes'")
    docs = retrieve_docs("file system", doc_type="notes", k=3)
    print(f"   Returned {len(docs)} chunks")
    for doc in docs:
        print(f"   - {doc.metadata.get('source_file')} | "
              f"{doc.metadata.get('doc_type')} | "
              f"score: {doc.metadata.get('relevance_score')}")

    print("\n🔍 Filter: subject='general'")
    docs = retrieve_docs("virtual memory", subject="general", k=3)
    print(f"   Returned {len(docs)} chunks")
    for doc in docs:
        print(f"   - {doc.metadata.get('source_file')} | "
              f"{doc.metadata.get('subject')} | "
              f"score: {doc.metadata.get('relevance_score')}")

    print("\n🔍 Filter: doc_type in ['notes','pyq','textbook']")
    docs = retrieve_docs("file system", doc_type=['notes', 'pyq', 'textbook'], k=3)
    print(f"   Returned {len(docs)} chunks")
    for doc in docs:
        print(f"   - {doc.metadata.get('source_file')} | "
              f"{doc.metadata.get('doc_type')} | "
              f"score: {doc.metadata.get('relevance_score')}")


def test_score_threshold():
    print("\n" + "=" * 60)
    print("TEST 3: Score Threshold Filtering")
    print("=" * 60)

    query = "Explain demand paging"
    print(f"\n🔍 Query: '{query}'")

    all_results = retrieve_with_scores(query=query, top_k=5)
    print(f"\n   All results (no threshold): {len(all_results)} chunks")
    for doc, score in all_results:
        print(f"   Score: {score:.3f} | {doc.metadata.get('source_file')}")

    filtered = retrieve_docs(query=query, k=5, score_threshold=0.1)
    print(f"\n   After threshold (≥ 0.1): {len(filtered)} chunks kept")
    for doc in filtered:
        print(f"   Score: {doc.metadata.get('relevance_score')} | "
              f"{doc.metadata.get('source_file')}")

    filtered_strict = retrieve_docs(query=query, k=5, score_threshold=0.4)
    print(f"\n   After strict threshold (≥ 0.4): {len(filtered_strict)} chunks kept")
    for doc in filtered_strict:
        print(f"   Score: {doc.metadata.get('relevance_score')} | "
              f"{doc.metadata.get('source_file')}")


def test_context_formatter():
    print("\n" + "=" * 60)
    print("TEST 4: Context Formatter Output")
    print("=" * 60)

    query = "What is virtual file system?"
    docs = retrieve_docs(query=query, k=3)

    print(f"\n🔍 Query: '{query}'")
    print(f"   Chunks retrieved: {len(docs)}")

    print("\n--- FORMATTED CONTEXT (what LLM will see) ---\n")
    context = format_context(docs)
    print(context[:800] + "..." if len(context) > 800 else context)

    print("\n--- SOURCES LIST (what UI will show) ---\n")
    sources = format_sources_list(docs)
    for s in sources:
        print(f"   • {s}")


if __name__ == "__main__":
    setup_test_data()
    test_basic_retrieval()
    test_metadata_filtering()
    test_score_threshold()
    test_context_formatter()

    print("\n" + "=" * 60)
    print("✅ All retrieval tests complete.")
    print("   Person 1 can now import:")
    print("   from vectorstore.retriever import retrieve_docs")
    print("   from utils.context_formatter import format_context, format_sources_list")
    print("=" * 60)