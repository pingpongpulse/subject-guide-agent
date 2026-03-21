import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def _get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    # Import inside function so the module can still be imported when the key is not set.
    from groq import Groq

    return Groq(api_key=api_key)


def format_context(docs):
    context = ""
    for i, doc in enumerate(docs):
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
            doc_type = doc.metadata.get("doc_type", "notes")
            text = doc.page_content[:500]
        else:
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
            doc_type = doc.get("doc_type", "notes")
            text = doc.get("text", "")[:500]

        context += f"\n[Source {i+1}: {source} | Page {page} | Type: {doc_type}]\n{text}\n"
    return context


def get_difficulty_instruction(difficulty):
    if difficulty == "beginner":
        return "Use very simple language. Avoid jargon. Use real life examples. Explain every term."
    elif difficulty == "exam":
        return "Be concise. Use bullet points. Focus only on exam relevant content."
    else:
        return "Use standard academic language. Balance detail and clarity."


def explain_topic(query, docs, difficulty="intermediate"):
    # If no Groq key is configured, return a placeholder message so the UI can still work.
    groq_client = _get_groq_client()
    if not groq_client:
        return "Please set GROQ_API_KEY environment variable to enable AI responses."

    context = format_context(docs)
    difficulty_instruction = get_difficulty_instruction(difficulty)

    prompt = f"""
You are an expert academic tutor helping a student understand a topic.
{difficulty_instruction}

Using ONLY the context below from uploaded study materials, answer the query
in this exact structure:

**Definition:**
(clear one line definition)

**Explanation:**
(detailed explanation)

**Example:**
(a concrete example)

**Related PYQs:**
(any related exam questions found in context, or say "Not found in uploaded materials")

**Citations:**
(list every source used as: [filename | Page number])

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
    dummy_docs = [
        {
            "text": "Demand paging is a method of virtual memory management where pages are loaded only when needed.",
            "source_file": "os_notes.pdf",
            "page_number": 10,
            "doc_type": "notes"
        }
    ]
    print(explain_topic("Explain demand paging", dummy_docs, difficulty="beginner"))
    print("\n--- EXAM MODE ---\n")
    print(explain_topic("Explain demand paging", dummy_docs, difficulty="exam"))