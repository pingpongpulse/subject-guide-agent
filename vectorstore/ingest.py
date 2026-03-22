import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vectorstore.store import get_vector_store, add_documents
from document_processor.pdf_loader import load_pdf
from document_processor.classifier import classify_document
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def detect_subject(filename):
    filename = filename.lower()
    if any(w in filename for w in ["os", "operating", "process", "memory", "deadlock"]):
        return "os"
    elif any(w in filename for w in ["dbms", "database", "sql", "normalization"]):
        return "dbms"
    elif any(w in filename for w in ["cn", "network", "tcp", "protocol"]):
        return "cn"
    elif any(w in filename for w in ["ds", "data structure", "tree", "graph"]):
        return "ds"
    else:
        return "general"


def ingest_pdf(filepath):
    print(f"\nIngesting: {filepath}")
    pages = load_pdf(filepath)
    print(f"Loaded {len(pages)} pages")

    text_preview = pages[0]['text'][:300] if pages else ""
    doc_type = classify_document(filepath, text_preview)
    subject = detect_subject(filepath)
    print(f"Doc type: {doc_type} | Subject: {subject}")

    documents = []
    for page in pages:
        doc = Document(
            page_content=page['text'],
            metadata={
                "source_file": page['source_file'],
                "page_number": page['page_number'],
                "doc_type": doc_type,
                "subject": subject
            }
        )
        documents.append(doc)

    add_documents(documents)
    print(f"Stored {len(documents)} chunks")


if __name__ == "__main__":
    docs_folder = "sample_docs"
    pdf_files = [f for f in os.listdir(docs_folder) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in data/sample_docs/")
        print("Add PDF files and run again")
    else:
        for pdf_file in pdf_files:
            ingest_pdf(os.path.join(docs_folder, pdf_file))

    print(f"\nDone! Processed {len(pdf_files)} PDFs")