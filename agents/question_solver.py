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


def detect_question_type(question):
    """
    Detects whether question is theory, numerical or derivation.
    """
    # If no Groq key is configured, fall back to a default type so the UI can still work.
    groq_client = _get_groq_client()
    if not groq_client:
        return "theory"

    prompt = f"""
You are a question type classifier for an academic assistant.

Classify this question into exactly ONE of these types:
- theory (conceptual questions, explain, define, describe, compare)
- numerical (problems with calculations, find the value, compute)
- derivation (prove, derive, show that)

Question: "{question}"

Reply with ONLY the type label, nothing else.
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    q_type = response.choices[0].message.content.strip().lower()
    valid_types = ["theory", "numerical", "derivation"]
    if q_type not in valid_types:
        return "theory"
    return q_type


def format_context_with_citations(docs):
    context = ""
    for i, doc in enumerate(docs):
        # Handle both Document objects and plain dicts
        if hasattr(doc, 'metadata'):
            # ChromaDB Document object
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
            doc_type = doc.metadata.get("doc_type", "notes")
            text = doc.page_content[:500]
        else:
            # Plain dict
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
            doc_type = doc.get("doc_type", "notes")
            text = doc.get("text", "")[:500]

        context += f"\n[Source {i+1}: {source} | Page {page} | Type: {doc_type}]\n{text}\n"
    return context


def get_difficulty_instruction(difficulty):
   
    if difficulty == "beginner":
        return "Use very simple language. Avoid technical jargon. Use lots of real life examples. Explain every term you use."
    elif difficulty == "exam":
        return "Be concise and to the point. Use bullet points. Focus only on what matters for exams. No unnecessary explanation."
    else:  # intermediate default
        return "Use standard academic language. Balance between detail and clarity."


def solve_theory(question, docs, difficulty="intermediate"):
    # If no Groq key is configured, return a placeholder message.
    groq_client = _get_groq_client()
    if not groq_client:
        return "Please set GROQ_API_KEY environment variable to enable AI responses."

    context = format_context_with_citations(docs)
    difficulty_instruction = get_difficulty_instruction(difficulty)

    prompt = f"""
You are an expert academic tutor solving an exam question.
{difficulty_instruction}

Answer this theory question using ONLY the context from uploaded study materials.
Structure your answer exactly like this:

**Question Type:** Theory

**Answer:**
(detailed answer in clear paragraphs)

**Key Points:**
(bullet points of most important points)

**Citations:**
(list every source used as: filename | Page number)

---
Context from uploaded materials:
{context}

---
Question: {question}
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def solve_numerical(question, docs, difficulty="intermediate"):
    # If no Groq key is configured, return a placeholder message.
    groq_client = _get_groq_client()
    if not groq_client:
        return "Please set GROQ_API_KEY environment variable to enable AI responses."

    context = format_context_with_citations(docs)
    difficulty_instruction = get_difficulty_instruction(difficulty)

    prompt = f"""
You are an expert academic tutor solving a numerical exam problem.
{difficulty_instruction}

Solve this numerical problem using the context from uploaded study materials.
Structure your answer exactly like this:

**Question Type:** Numerical

**Given:**
(list all given values clearly)

**Formula Used:**
(write the exact formula)

**Step by Step Solution:**
(show every calculation step clearly numbered)

**Final Answer:**
(clearly state the final answer with units)

**Citations:**
(list every source used as: filename | Page number)

---
Context from uploaded materials:
{context}

---
Question: {question}
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def solve_derivation(question, docs, difficulty="intermediate"):
    # If no Groq key is configured, return a placeholder message.
    groq_client = _get_groq_client()
    if not groq_client:
        return "Please set GROQ_API_KEY environment variable to enable AI responses."

    context = format_context_with_citations(docs)
    difficulty_instruction = get_difficulty_instruction(difficulty)

    prompt = f"""
You are an expert academic tutor solving a derivation exam question.
{difficulty_instruction}

Answer this derivation question using the context from uploaded study materials.
Structure your answer exactly like this:

**Question Type:** Derivation

**Assumptions:**
(list any assumptions made)

**Derivation:**
(show every step clearly and logically numbered)

**Result:**
(clearly state the final derived result)

**Citations:**
(list every source used as: filename | Page number)

---
Context from uploaded materials:
{context}

---
Question: {question}
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def solve_question(question, docs, difficulty="intermediate"):
    """
    Main function — detects type and routes to correct solver.
    """
    q_type = detect_question_type(question)
    print(f"Question type detected: {q_type}")

    if q_type == "numerical":
        return solve_numerical(question, docs, difficulty)
    elif q_type == "derivation":
        return solve_derivation(question, docs, difficulty)
    else:
        return solve_theory(question, docs, difficulty)


if __name__ == "__main__":
    dummy_docs = [
        {
            "text": "Banker's algorithm is a deadlock avoidance algorithm that tests for safety by simulating allocation of maximum possible resources.",
            "source_file": "os_notes.pdf",
            "page_number": 23,
            "doc_type": "notes"
        },
        {
            "text": "In Banker's algorithm, when a process requests resources, the system checks if granting the request leaves the system in a safe state.",
            "source_file": "os_textbook.pdf",
            "page_number": 67,
            "doc_type": "textbook"
        }
    ]

    answer = solve_question(
        "Explain the Banker's algorithm for deadlock avoidance with example",
        dummy_docs,
        difficulty="intermediate"
    )
    print(answer)