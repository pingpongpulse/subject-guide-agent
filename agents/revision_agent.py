import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from vectorstore.retriever import retrieve_docs

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_revision(query, docs, mode="standard"):
    """
    Generates quick revision content from retrieved docs.
    mode: standard, lightning
    """
    context = ""
    for i, doc in enumerate(docs):
        if hasattr(doc, 'page_content'):
            text = doc.page_content[:400]
            source = doc.metadata.get('source_file', 'unknown')
            page = doc.metadata.get('page_number', '?')
        else:
            text = doc.get('text', '')[:400]
            source = doc.get('source_file', 'unknown')
            page = doc.get('page_number', '?')
        context += f"\n[Source: {source} | Page {page}]\n{text}\n"

    if mode == "lightning":
        prompt = f"""
You are an expert academic tutor creating lightning revision content.

Using ONLY the context below, generate quick revision material in this exact format:

**20 One-Liners:**
1. <one line fact>
2. <one line fact>
... (up to 20)

**10 Key Definitions:**
1. <term>: <definition>
... (up to 10)

**10 Expected Exam Questions:**
1. <question>
... (up to 10)

**5 Short Notes:**
1. <topic>: <2-3 line note>
... (up to 5)

Context:
{context}

Topic: {query}"""

    else:
        prompt = f"""
You are an expert academic tutor creating revision content.

Using ONLY the context below create a concise revision summary in this format:

**Key Concepts:**
(bullet points of the most important concepts)

**Important Formulas/Algorithms:**
(any formulas or step by step algorithms)

**Quick Facts:**
(5-10 quick facts to remember)

**Likely Exam Questions:**
(3-5 questions likely to appear in exams)

**Citations:**
(source files and page numbers used)

Context:
{context}

Topic: {query}"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def get_revision(query, mode="standard"):
    """
    Main function called by router for revision queries.
    """
    docs = retrieve_docs(query, k=6)

    if not docs:
        return "No relevant content found for revision. Please upload study materials first."

    return generate_revision(query, docs, mode=mode)


def get_lightning_revision(query):
    """
    One click lightning revision mode.
    """
    return get_revision(query, mode="lightning")


if __name__ == "__main__":
    print("=== Standard Revision ===")
    result = get_revision("demand paging", mode="standard")
    print(result)

    print("\n=== Lightning Revision ===")
    result2 = get_lightning_revision("process scheduling")
    print(result2)