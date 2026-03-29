import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def fetch_pyq_chunks():
    """
    Fetches only PYQ chunks from vector database.
    """
    from vectorstore.store import get_vector_store
    vector_store = get_vector_store()

    all_docs = vector_store.get()
    pyq_chunks = []

    for i, doc_id in enumerate(all_docs['ids']):
        metadata = all_docs['metadatas'][i]
        if metadata.get('doc_type', '').lower() == 'pyq':
            pyq_chunks.append({
                "text": all_docs['documents'][i],
                "source_file": metadata.get('source_file', 'unknown'),
                "page_number": metadata.get('page_number', '?'),
                "subject": metadata.get('subject', 'general')
            })

    return pyq_chunks


def analyze_pyq_frequency():
    """
    Fetches PYQ chunks and extracts topics in batches.
    10 chunks per API call to save tokens.
    """
    print("Fetching PYQ chunks from database...")
    chunks = fetch_pyq_chunks()

    if not chunks:
        print("No PYQ documents found in database.")
        return {}

    print(f"Found {len(chunks)} PYQ chunks. Extracting topics in batches...")

    topics = []
    batch_size = 10

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_text = ""
        for j, chunk in enumerate(batch):
            batch_text += f"\nChunk {j+1}:\n{chunk['text'][:200]}\n"

        prompt = f"""
You are an academic topic extractor.

For each chunk below identify the main topic being asked about.
Reply with ONLY a numbered list of short topic labels (2-4 words each).
One topic per chunk. Nothing else.

Example response:
1. Banker's Algorithm
2. Demand Paging
3. Process Scheduling

Chunks:
{batch_text}

Topics:"""

        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
            lines = [
                line.split(".", 1)[1].strip()
                for line in result.split("\n")
                if line.strip() and line[0].isdigit()
            ]
            topics.extend(lines)
            print(f"  Processed chunks {i+1} to {min(i+batch_size, len(chunks))}")
            time.sleep(1)

        except Exception as e:
            print(f"  Batch failed: {e} — skipping")
            continue

    frequency = Counter(topics)
    sorted_frequency = dict(
        sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    )

    print("\n--- PYQ Topic Frequency ---")
    for topic, count in sorted_frequency.items():
        print(f"{topic}: {count} times")

    return sorted_frequency


def get_top_topics(n=10):
    """
    Returns top n most repeated topics as formatted string.
    Called by router.
    """
    frequency = analyze_pyq_frequency()

    if not frequency:
        return "No PYQ documents found. Please upload past question papers first."

    top_topics = list(frequency.items())[:n]

    result = "**Most Repeated Topics in Past Question Papers:**\n\n"
    for i, (topic, count) in enumerate(top_topics):
        result += f"{i+1}. {topic} — appeared {count} time{'s' if count > 1 else ''}\n"

    result += "\n**Tip:** Focus on these topics first for exam preparation."
    return result


if __name__ == "__main__":
    frequency = analyze_pyq_frequency()
    if frequency:
        print("\nTop 10 topics:")
        for i, (topic, count) in enumerate(list(frequency.items())[:10]):
            print(f"{i+1}. {topic}: {count} times")