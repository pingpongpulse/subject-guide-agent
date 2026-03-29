import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.pyq_analyzer import analyze_pyq_frequency


def get_heatmap_data():
    """
    Gets topic frequency data formatted for heatmap display.
    Returns a dict with topics and their frequencies.
    """
    frequency = analyze_pyq_frequency()

    if not frequency:
        return {
            "topics": [],
            "frequencies": [],
            "message": "No PYQ documents found. Please upload past question papers first."
        }

    topics = list(frequency.keys())
    frequencies = list(frequency.values())

    return {
        "topics": topics,
        "frequencies": frequencies,
        "message": "success"
    }


def get_subject_wise_heatmap_data():
    """
    Gets topic frequency broken down by subject.
    Returns dict with subject as key and topic frequencies as value.
    """
    from vectorstore.store import get_vector_store
    vector_store = get_vector_store()

    all_docs = vector_store.get()
    subject_chunks = {}

    for i, doc_id in enumerate(all_docs['ids']):
        metadata = all_docs['metadatas'][i]
        if metadata.get('doc_type', '').lower() == 'pyq':
            subject = metadata.get('subject', 'general')
            if subject not in subject_chunks:
                subject_chunks[subject] = []
            subject_chunks[subject].append(all_docs['documents'][i])

    return subject_chunks


def get_top_n_topics(n=15):
    """
    Returns only top n topics for cleaner heatmap display.
    """
    frequency = analyze_pyq_frequency()

    if not frequency:
        return {}

    top_n = dict(list(frequency.items())[:n])
    return top_n


if __name__ == "__main__":
    print("Getting heatmap data...")
    data = get_heatmap_data()
    print(f"Total topics: {len(data['topics'])}")
    print("Top 10:")
    for topic, freq in zip(data['topics'][:10], data['frequencies'][:10]):
        print(f"  {topic}: {freq}")