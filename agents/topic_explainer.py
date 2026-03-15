import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def format_context(docs):
    """
    Formats retrieved docs into a readable context string.
    """
    context = ""
    for i, doc in enumerate(docs):
        source = doc.get("source_file", "unknown")
        page = doc.get("page_number", "?")
        doc_type = doc.get("doc_type", "notes")
        text = doc.get("text", "")[:500]
        context += f"\n[Source {i+1}: {source} | Page {page} | Type: {doc_type}]\n{text}\n"
    return context


def explain_topic(query, docs):
    """
    Takes a query and retrieved docs, returns structured explanation.
    """
    context = format_context(docs)

    prompt = f"""
You are an expert academic tutor helping a student understand a topic.

Using the context below from the student's uploaded study materials, answer the query in this exact structure:

**Definition:**
(clear one-line definition)

**Explanation:**
(detailed explanation in simple terms)

**Example:**
(a concrete example)

**Related PYQs:**
(any related exam questions found in the context, or say "Not found in uploaded materials")

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