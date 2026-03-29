import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from vectorstore.retriever import retrieve_docs

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_topics_from_syllabus(syllabus_text):
    """
    Uses LLM to extract modules and topics from syllabus text.
    """
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

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_study_plan(syllabus_text, days=7):
    """
    Takes syllabus text and generates a day wise study plan.
    """
    topics = extract_topics_from_syllabus(syllabus_text)

    prompt = f"""
You are an expert academic planner helping a student prepare for exams.

Based on these modules and topics extracted from the syllabus, create a detailed
{days}-day study plan. For each day specify exactly what to study.

Structure your response like this:

**Day 1:**
- Topic: <topic name>
- What to cover: <brief description>
- Time needed: <estimated hours>

**Day 2:**
...and so on

Make sure all topics are covered across the {days} days.
Prioritize topics that are fundamental and build on each other logically.

Modules and Topics:
{topics}

{days}-Day Study Plan:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_study_plan_from_query(query, days=7):
    """
    Called by router when student asks for a study plan.
    Retrieves syllabus from vector DB and generates plan.
    """
    docs = retrieve_docs(query, k=6, doc_type="syllabus")

    if not docs:
        docs = retrieve_docs(query, k=6)

    if not docs:
        return "No syllabus found in uploaded documents. Please upload your syllabus PDF first."

    syllabus_text = "\n".join([
        doc.page_content if hasattr(doc, 'page_content')
        else doc.get('text', '')
        for doc in docs
    ])

    return generate_study_plan(syllabus_text, days=days)


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

    plan = generate_study_plan(dummy_syllabus, days=7)
    print(plan)