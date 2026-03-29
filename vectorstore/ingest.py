import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_processor.pdf_loader import load_pdf
from document_processor.docx_loader import load_docx
from document_processor.pptx_loader import load_pptx
from document_processor.ocr_loader import load_scanned_pdf, load_image
from document_processor.classifier import classify_document
from vectorstore.store import get_vector_store, add_documents
from langchain_core.documents import Document
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg"]


def detect_subject(filename, text_preview=""):
    filename = filename.lower()
    combined = filename + " " + text_preview.lower()

    subject_map = {
        "os": ["operating system", "process scheduling", "deadlock",
               "memory management", "virtual memory", "semaphore", "banker"],
        "dbms": ["database", "sql", "normalization", "transaction",
                 "relational", "entity relationship", "acid"],
        "cn": ["computer network", "tcp", "ip address", "routing",
               "protocol", "osi model", "dns", "http", "subnet"],
        "ds": ["data structure", "linked list", "stack", "queue",
               "tree", "graph", "sorting", "hashing"],
        "algo": ["algorithm", "complexity", "dynamic programming",
                 "greedy", "divide and conquer", "big o"],
        "oops": ["object oriented", "class", "inheritance",
                 "polymorphism", "encapsulation", "java", "c++"],
        "iot": ["internet of things", "iot", "sensor", "mqtt",
                "arduino", "raspberry pi", "embedded"],
        "ml": ["machine learning", "neural network", "deep learning",
               "classification", "regression", "clustering"],
        "ai": ["artificial intelligence", "search algorithm",
               "expert system", "heuristic", "planning"],
        "cloud": ["cloud computing", "aws", "azure", "virtualization",
                  "docker", "kubernetes", "microservice"],
        "cyber": ["cybersecurity", "cryptography", "encryption",
                  "firewall", "vulnerability", "authentication"],
        "maths": ["mathematics", "calculus", "integration",
                  "differentiation", "algebra", "trigonometry", "matrix"],
        "stats": ["statistics", "probability", "distribution",
                  "hypothesis", "regression", "sampling", "bayes"],
        "discrete": ["discrete mathematics", "set theory", "logic",
                     "boolean", "graph theory", "combinatorics"],
        "physics": ["physics", "mechanics", "thermodynamics",
                    "optics", "electromagnetism", "quantum", "wave"],
        "chemistry": ["chemistry", "organic", "inorganic",
                      "reaction", "periodic table", "molecule"],
        "biology": ["biology", "cell", "genetics", "evolution",
                    "photosynthesis", "dna", "rna", "organism"],
        "electronics": ["electronics", "diode", "transistor",
                        "amplifier", "circuit", "resistor", "op amp"],
        "electrical": ["electrical", "voltage", "current", "power",
                       "motor", "transformer", "generator"],
        "mechanical": ["mechanical", "fluid mechanics",
                       "manufacturing", "heat transfer", "turbine"],
        "civil": ["civil", "structural", "concrete", "soil",
                  "surveying", "construction", "beam"],
        "management": ["management", "organization", "leadership",
                       "strategy", "hrm", "marketing", "accounting"],
        "economics": ["economics", "demand", "supply", "gdp",
                      "inflation", "microeconomics", "macroeconomics"],
        "english": ["english", "grammar", "vocabulary",
                    "comprehension", "essay", "literature"],
        "hindi": ["hindi", "vyakaran", "nibandh", "kavita",
                  "sahitya", "shabd"],
        "se": ["software engineering", "sdlc", "agile",
               "waterfall", "testing", "uml", "design pattern"],
    }

    scores = {subject: 0 for subject in subject_map}
    for subject, keywords in subject_map.items():
        for keyword in keywords:
            if keyword in combined:
                scores[subject] += 1

    best_match = max(scores, key=scores.get)
    best_score = scores[best_match]

    if best_score == 0:
        print("  Subject unclear — asking LLM...")
        return llm_detect_subject(text_preview)

    return best_match


def llm_detect_subject(text_preview):
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
You are a subject classifier for an academic assistant.
Given this text preview identify the subject it belongs to.
Reply with ONLY a short label like: os, dbms, maths, physics, iot, ml, english etc.
Nothing else.

Text: {text_preview[:300]}
Subject:"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().lower()


def load_file(filepath):
    """
    Smart file router — picks the right loader for each file type.
    Automatically falls back to OCR for scanned PDFs.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        pages = load_pdf(filepath)
        total_text = " ".join([p['text'] for p in pages])
        if len(total_text.strip()) < 100:
            print("  Low text detected — switching to OCR...")
            pages = load_scanned_pdf(filepath)
        return pages

    elif ext == ".docx":
        return load_docx(filepath)

    elif ext == ".pptx":
        return load_pptx(filepath)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return load_image(filepath)

    else:
        print(f"  Unsupported file type: {ext}")
        return []


def ingest_file(filepath):
    """
    Ingests any supported file into the vector database.
    """
    if os.path.basename(filepath).startswith("~$"):
        print(f"Skipping temp file in ingest_file: {filepath}")
        return

    print(f"\nIngesting: {filepath}")

    pages = load_file(filepath)

    if not pages:
        print(f"  No text extracted from {filepath} — skipping")
        return

    text_preview = pages[0]['text'][:300] if pages else ""
    doc_type = classify_document(filepath, text_preview)
    subject = detect_subject(filepath, text_preview)
    print(f"  Doc type: {doc_type} | Subject: {subject}")

    documents = []
    for page in pages:
        doc = Document(
            page_content=page['text'],
            metadata={
                "source_file": page['source_file'],
                "page_number": page['page_number'],
                "doc_type": doc_type,
                "subject": subject,
                "extraction_method": page.get('extraction_method', 'unknown')
            }
        )
        documents.append(doc)

    add_documents(documents)
    print(f"  Stored {len(documents)} chunks")


if __name__ == "__main__":
    docs_folder = "sample_docs"

    all_files = [
        f for f in os.listdir(docs_folder)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        and not os.path.basename(f).startswith("~$")
    ]

    if not all_files:
        print(f"No supported files found in {docs_folder}/")
        print(f"Supported types: {SUPPORTED_EXTENSIONS}")
    else:
        print(f"Found {len(all_files)} files to ingest")
        for filename in all_files:
            if os.path.basename(filename).startswith("~$"):
                print(f"Skipping temp file: {filename}")
                continue
            ingest_file(os.path.join(docs_folder, filename))

    print(f"\nDone! Processed {len(all_files)} files")
