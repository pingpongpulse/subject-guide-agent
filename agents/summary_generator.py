"""
Summary Generator Agent

Generates comprehensive, citation-grounded summaries for revision.
Supports multiple output formats optimized for different learning styles.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from vectorstore.retriever import retrieve_docs
from utils.context_formatter import format_context

load_dotenv()


def _get_groq_client():
    """Safely get Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def _build_cited_context(docs, max_per_section=400):
    """
    Build context with clear source markers for citation tracking.
    Each piece of text is tagged with its source.
    """
    context = ""
    for i, doc in enumerate(docs):
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
            doc_type = doc.metadata.get("doc_type", "notes")
            text = doc.page_content[:max_per_section]
        else:
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
            doc_type = doc.get("doc_type", "notes")
            text = doc.get("text", "")[:max_per_section]
        
        context += f"\n[Source {i+1}: {source} | Page {page}]\n{text}\n"
    
    return context


def generate_standard_summary(query, docs):
    """
    Generate a comprehensive, well-structured summary.
    Output includes: concepts, formulas, key points, examples, citations.
    """
    client = _get_groq_client()
    if not client:
        return "Please set GROQ_API_KEY environment variable to enable summary generation."
    
    context = _build_cited_context(docs)
    
    prompt = f"""
You are an expert academic tutor creating a comprehensive revision summary.

Using ONLY the context provided, generate a detailed yet concise summary.
STRICTLY cite sources - reference source numbers [Source 1], [Source 2] etc. for every major claim.

Structure your response EXACTLY as:

**Key Concepts:**
(3-5 main concepts with definitions. Reference sources for each)

**Important Formulas/Theorems:**
(All formulas, equations, or key theorems. Reference sources)

**Step-by-Step Explanation:**
(Detailed explanation with examples. Reference sources)

**Real-World Examples:**
(2-3 concrete examples. Reference sources)

**Common Mistakes to Avoid:**
(3-5 common errors students make)

**Quick Facts:**
(7-10 memorable one-liners)

**Frequently Asked Exam Questions:**
(3-5 likely exam questions on this topic)

**Citations:**
(Numbered list of all sources used: [1] filename | Page number, [2] filename | Page number, etc.)

---
Context from uploaded materials:
{context}

---
Topic: {query}

Generate Summary:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def generate_lightning_summary(query, docs):
    """
    Generate a ultra-concise revision summary for last-minute studying.
    Perfect for quick memorization before exams.
    """
    client = _get_groq_client()
    if not client:
        return "Please set GROQ_API_KEY environment variable"
    
    context = _build_cited_context(docs, max_per_section=300)
    
    prompt = f"""
You are an expert at creating ultra-concise revision notes for students.

From the context provided, extract ONLY the most critical information.
Format as:

**30 Essential One-Liners:**
1. <Term>: <definition in one line> [Source X]
2. <Term>: <definition in one line> [Source X]
[...up to 30]

**15 Key Definitions:**
1. <Term>: <5-10 word definition> [Source X]
[...up to 15]

**Top 10 Formulas:**
1. <Formula> [Source X]
[...up to 10]

**20 Expected Exam Questions:**
1. <Question> [Source X]
[...up to 20]

**Memory Tricks:**
- <Mnemonic or trick> [Source X]
- <Mnemonic or trick> [Source X]

**Source References:**
[1] filename | Page number
[2] filename | Page number

---
Context:
{context}

---
Topic: {query}

Generate Lightning Notes:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message


def generate_detailed_summary(query, docs):
    """
    Generate an in-depth summary with detailed explanations and derivations.
    Best for deep understanding before exams.
    """
    client = _get_groq_client()
    if not client:
        return "Please set GROQ_API_KEY environment variable"
    
    context = _build_cited_context(docs, max_per_section=500)
    
    prompt = f"""
You are an expert professor creating detailed lecture notes for exam preparation.

Using the context provided, create comprehensive notes with full derivations.
Reference sources [Source X] for every claim, formula, and example.

Structure as:

**1. Introduction & Context:**
(Brief background on why this topic matters)

**2. Fundamental Definitions:**
(All key terms with detailed definitions)

**3. Detailed Explanation:**
(In-depth explanation with derived relationships)

**4. Mathematical/Theoretical Foundations:**
(All formulas with derivations, proofs, or justifications)

**5. Worked Examples:**
(2-3 complete solved examples step-by-step)

**6. Application Areas:**
(Real-world and exam-relevant applications)

**7. Common Misconceptions:**
(What students often get wrong and why)

**8. Important Variations:**
(Different cases, special scenarios, edge cases)

**9. Connection to Other Topics:**
(How this relates to prerequisites and advanced topics)

**10. Exam Strategy:**
(How this topic typically appears in exams, what to focus on)

**Citations by Section:**
[1] filename | Page number
[2] filename | Page number

---
Context:
{context}

---
Topic: {query}

Generate Detailed Summary:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def generate_checklist_summary(query, docs):
    """
    Generate a checklist-style summary: what to study, what's important, practice problems.
    Best for structured exam prep.
    """
    client = _get_groq_client()
    if not client:
        return "Please set GROQ_API_KEY environment variable"
    
    context = _build_cited_context(docs)
    
    prompt = f"""
You are an exam preparation coach creating a study checklist.

From the provided materials, generate a practical checklist format:

**Prerequisites to Know:**
☐ Concept 1 (explanation)
☐ Concept 2 (explanation)

**Must-Know Concepts:**
☐ Concept 1 [Source X]
☐ Concept 2 [Source X]

**Key Formulas (Memorize These):**
☐ Formula 1 [Source X]
☐ Formula 2 [Source X]

**Problem-Solving Steps:**
For [problem type]:
1. Step 1
2. Step 2
3. Step 3

**Practice Questions to Try:**
1. Question Type 1 (expected difficulty)
2. Question Type 2 (expected difficulty)

**Common Pitfalls:**
✗ Pitfall 1 → How to avoid
✗ Pitfall 2 → How to avoid

**Time Allocation (in exam):**
- Part 1: X minutes
- Part 2: Y minutes

**Last-Minute Revision Priority:**
1. [Most Important]
2. [Important]
3. [Nice to Know]

**Source References:**
[1] filename | Page number
[2] filename | Page number

---
Context:
{context}

---
Topic: {query}

Generate Study Checklist:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def generate_summary(query, format_type="standard"):
    """
    Main entry point for summary generation.
    Routes to appropriate summary generator based on format.
    
    Args:
        query: Topic to summarize
        format_type: One of ['standard', 'lightning', 'detailed', 'checklist']
    
    Returns:
        Generated summary with citations
    """
    # Retrieve relevant documents
    docs = retrieve_docs(query, k=6)
    
    if not docs:
        return f"No materials found for '{query}'. Please upload study materials first."
    
    format_type = format_type.lower().strip()
    
    if format_type == "lightning":
        summary = generate_lightning_summary(query, docs)
    elif format_type == "detailed":
        summary = generate_detailed_summary(query, docs)
    elif format_type == "checklist":
        summary = generate_checklist_summary(query, docs)
    else:
        summary = generate_standard_summary(query, docs)
    
    return summary


if __name__ == "__main__":
    # Test the summary generator
    print("=" * 60)
    print("STANDARD SUMMARY TEST")
    print("=" * 60)
    dummy_docs = [
        {
            "text": "Demand paging is a memory management technique where pages are loaded into memory only when needed. It reduces memory usage and supports larger virtual address spaces.",
            "source_file": "os_notes.pdf",
            "page_number": 25,
            "doc_type": "notes"
        },
        {
            "text": "Page replacement algorithms like LRU, FIFO, and Optimal are used to decide which page to remove when memory is full.",
            "source_file": "os_textbook.pdf",
            "page_number": 110,
            "doc_type": "textbook"
        }
    ]
    
    print("Testing with dummy documents...")
    print("Note: Actual execution requires GROQ_API_KEY")
