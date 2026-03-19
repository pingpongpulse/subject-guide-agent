import os
from dotenv import load_dotenv

load_dotenv()


def _get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    # Import inside function so the module can still be imported when the key is not set.
    from groq import Groq

    return Groq(api_key=api_key)


def classify_query(query):
    """Classifies user query into one of 4 categories."""

    # If no Groq key is configured, fall back to a default category so the UI can still work.
    groq_client = _get_groq_client()
    if not groq_client:
        return "topic_explanation"

    prompt = f"""
You are a query classifier for a student study assistant.

Classify this query into exactly ONE of these categories:
- topic_explanation (user wants to understand a concept)
- question_solving (user wants to solve a problem or PYQ)
- revision (user wants quick revision or summary)
- study_plan (user wants a study plan or schedule)

Query: "{query}"

Reply with ONLY the category label, nothing else.
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    label = response.choices[0].message.content.strip().lower()
    valid_labels = ["topic_explanation", "question_solving", "revision", "study_plan"]
    if label not in valid_labels:
        return "topic_explanation"  # default fallback
    return label


if __name__ == "__main__":
    test_queries = [
        "What is demand paging?",
        "Explain virtual memory",
        "Give quick revision of page replacement",
        "Solve this paging problem",
        "Create a 7 day study plan for OS exam"
    ]
    for q in test_queries:
        label = classify_query(q)
        print(f"Query: {q}")
        print(f"Classified as: {label}")
        print()