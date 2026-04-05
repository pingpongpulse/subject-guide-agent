import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from vectorstore.retriever import retrieve_docs
from vectorstore.store import get_vector_store
from collections import defaultdict

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _get_groq_client():
    """Safely get Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def extract_document_topics():
    """
    Intelligently extracts topics from all uploaded documents.
    Maps topics to their source documents for citations.
    """
    vector_store = get_vector_store()
    all_docs = vector_store.get()
    
    if not all_docs or not all_docs.get('documents'):
        return {}
    
    client = _get_groq_client()
    if not client:
        return {}
    
    # Sample documents to extract key topics
    sample_size = min(20, len(all_docs['documents']))
    sampled_docs = all_docs['documents'][:sample_size]
    sample_text = "\n---\n".join(sampled_docs[:10])
    
    prompt = f"""
You are an academic curriculum analyst.

From the course materials below, extract and list all main topics with their brief descriptions.
Format as:
Topic Name | Brief Description

Return ONLY the list, one per line. Max 15 topics.

Course Materials Sample:
{sample_text[:3000]}

Topics List:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def get_topic_references(query):
    """
    Retrieves documents relevant to a topic for citation purposes.
    """
    docs = retrieve_docs(query, k=3)
    references = []
    
    for doc in docs:
        if hasattr(doc, 'metadata'):
            references.append({
                "file": doc.metadata.get("source_file", "unknown"),
                "page": doc.metadata.get("page_number", "?"),
                "doc_type": doc.metadata.get("doc_type", "notes")
            })
        else:
            references.append({
                "file": doc.get("source_file", "unknown"),
                "page": doc.get("page_number", "?"),
                "doc_type": doc.get("doc_type", "notes")
            })
    
    return references


def extract_topics_from_syllabus(syllabus_text):
    """
    Uses LLM to extract modules and topics from syllabus text.
    """
    client = _get_groq_client()
    if not client:
        return "Topics extraction unavailable"
    
    prompt = f"""
You are an academic assistant analyzing a course syllabus.

Extract all the modules and their topics from this syllabus text.
Return them as a structured list like this:

Module 1: <module name>
- Topic 1
- Topic 2

Module 2: <module name>
- Topic 1
- Topic 2

Syllabus text:
{syllabus_text[:2000]}

Extracted modules and topics:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_study_plan_with_references(topics_text, days=7, hours_per_day=6):
    """
    Generates a detailed, day-wise study plan with document references.
    
    Args:
        topics_text: Extracted topics from syllabus or documents
        days: Number of days for study plan
        hours_per_day: Available study hours per day
    
    Returns:
        Structured study plan with citations
    """
    client = _get_groq_client()
    if not client:
        return "Study plan generation unavailable"

    prompt = f"""
You are an expert academic planner helping a student prepare for exams.

Based on these topics extracted from the syllabus/documents, create a detailed
{days}-day study plan. Each day has approximately {hours_per_day} study hours.

Structure your response EXACTLY like this:

**Day 1: <main topic>**
- Morning ({hours_per_day//2}h): <topic> — Key concepts: <key points>
- Afternoon/Evening: <topic> — Practice: <practice recommendations>
- Study Material: Use your notes/textbooks on this topic

**Day 2: <main topic>**
...continue for all {days} days

Requirements:
1. Distribute topics logically across days
2. Start with fundamentals
3. Build complexity gradually
4. Include 1-2 revision days
5. Focus on frequently tested topics (if from PYQs)
6. Each day should have a clear learning objective

Topics to Cover:
{topics_text}

{days}-Day Study Plan:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_study_plan_from_query(query, days=7, hours_per_day=6):
    """
    Main function called by router when student asks for a study plan.
    Retrieves syllabus/topics from vector DB and generates plan.
    
    Args:
        query: User's study plan request
        days: Number of days (customizable)
        hours_per_day: Available study hours per day
    
    Returns:
        Detailed study plan with document references
    """
    # Try to get explicit syllabus first
    docs = retrieve_docs(query, k=6, doc_type="syllabus")
    
    if not docs:
        # Fall back to extracting topics from general documents
        docs = retrieve_docs(query, k=8)
    
    if not docs:
        return "No study materials found. Please upload your syllabus or course materials first."
    
    # Extract combined context
    context_text = "\n".join([
        (doc.page_content if hasattr(doc, 'page_content') else doc.get('text', ''))
        for doc in docs
    ])
    
    # Extract terms like "7 days", "5 days" etc. from query
    import re
    day_match = re.search(r'(\d+)\s*days?', query.lower())
    if day_match:
        days = int(day_match.group(1))
    
    hour_match = re.search(r'(\d+)\s*hours?', query.lower())
    if hour_match:
        hours_per_day = int(hour_match.group(1))
    
    # Generate topics if explicit syllabus not found
    topics_text = extract_topics_from_syllabus(context_text) if "syllabus" in [d.metadata.get("doc_type", "").lower() if hasattr(d, 'metadata') else d.get("doc_type", "").lower() for d in docs] else context_text[:3000]
    
    # Generate and return plan
    plan = generate_study_plan_with_references(topics_text, days=days, hours_per_day=hours_per_day)
    
    # Add sources section
    plan += "\n\n**Extracted from course materials:**\n"
    seen_sources = set()
    for doc in docs:
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
        else:
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
        
        key = f"{source}_{page}"
        if key not in seen_sources:
            seen_sources.add(key)
            plan += f"- {source} | Page {page}\n"
    
    return plan


if __name__ == "__main__":
    dummy_syllabus = """
    Module 1: Process Management
    - Process states and transitions
    - Process scheduling algorithms
    - Inter process communication

    Module 2: Memory Management
    - Paging and segmentation
    - Virtual memory
    - Page replacement algorithms

    Module 3: Deadlocks
    - Deadlock conditions
    - Banker's algorithm
    - Deadlock detection and recovery

    Module 4: File Systems
    - File allocation methods
    - Directory structures
    - File system implementation
    """

    plan = generate_study_plan_with_references(dummy_syllabus, days=7, hours_per_day=6)
    print(plan)