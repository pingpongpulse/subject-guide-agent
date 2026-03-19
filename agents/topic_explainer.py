
import os
from dotenv import load_dotenv
from utils.context_formatter import format_context

load_dotenv()


def _get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    # Import inside function so the module can still be imported when the key is not set.
    from groq import Groq

    return Groq(api_key=api_key)


def format_context(docs):
    """Formats retrieved docs into a readable context string."""
    context = ""
    for i, doc in enumerate(docs):
        if hasattr(doc, 'metadata'):
            # langchain Document
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
            doc_type = doc.metadata.get("doc_type", "notes")
            text = doc.page_content[:500]
        else:
            # dict
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
            doc_type = doc.get("doc_type", "notes")
            text = doc.get("text", "")[:500]
        context += f"\n[Source {i+1}: {source} | Page {page} | Type: {doc_type}]\n{text}\n"
    return context


def explain_topic(query, docs):
    """Takes a query and retrieved docs, returns structured explanation."""
    context = format_context(docs)

    groq_client = _get_groq_client()
    if not groq_client:
        # Fallback when GROQ_API_KEY is not provided.
        if docs:
            preview = docs[0].page_content.strip().replace("\n", " ")
            preview = preview[:500] + ("..." if len(preview) > 500 else "")
            return (
                "⚠️ GROQ_API_KEY not set. Returning a simple fallback answer based on the retrieved documents.\n\n"
                f"Top document excerpt: {preview}"
            )
        return "⚠️ GROQ_API_KEY not set and no documents are available to answer the query."

    prompt = f"""
You are an expert academic tutor helping a student understand a topic.

Using the context below from the student's uploaded study materials, answer the query in this exact structure:

**Definition:**
(clear one-line definition)

**Explanation:**
(detailed explanation in simple terms)

**Sources:**
(list the source files and page numbers used)

---
Context from uploaded materials:
{context}

---
Student Query: {query}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Test with dummy docs until retriever is ready
    dummy_docs = [
        {
            "text": "Demand paging is a method of virtual memory management where pages are loaded into memory only when demanded during execution.",
            "source_file": "os_notes.pdf",
            "page_number": 10,
            "doc_type": "notes"
        },
        {
            "text": "In demand paging, a page fault occurs when a process accesses a page not currently in memory.",
            "source_file": "os_textbook.pdf",
            "page_number": 45,
            "doc_type": "textbook"
        }
    ]

    answer = explain_topic("Explain demand paging", dummy_docs)
    print(answer)