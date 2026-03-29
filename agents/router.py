import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from agents.query_classifier import classify_query
from agents.topic_explainer import explain_topic
from agents.question_solver import solve_question
from agents.pyq_analyzer import get_top_topics
from agents.revision_agent import get_revision
from agents.study_plan_agent import generate_study_plan_from_query
from vectorstore.retriever import retrieve_docs

load_dotenv()


def route_query(query, doc_type=None, subject=None, difficulty="intermediate"):
    print(f"\nQuery received: {query}")

    category = classify_query(query)
    print(f"Query classified as: {category}")

    if category == "topic_explanation":
        agent_name = "TopicExplainerAgent"
        print(f"Selected agent: {agent_name}")
        docs = retrieve_docs(query, k=4)
        print(f"Retriever returned {len(docs)} chunks")
        answer = explain_topic(query, docs, difficulty=difficulty)

    elif category == "question_solving":
        agent_name = "QuestionSolverAgent"
        print(f"Selected agent: {agent_name}")
        docs = retrieve_docs(query, k=4)
        print(f"Retriever returned {len(docs)} chunks")
        answer = solve_question(query, docs, difficulty=difficulty)

    elif category == "revision":
        agent_name = "RevisionAgent"
        print(f"Selected agent: {agent_name}")
        answer = get_revision(query, mode="standard")

    elif category == "study_plan":
        agent_name = "StudyPlanAgent"
        print(f"Selected agent: {agent_name}")
        answer = generate_study_plan_from_query(query, days=7)

    elif category == "pyq_analysis":
        agent_name = "PYQAnalyzerAgent"
        print(f"Selected agent: {agent_name}")
        answer = get_top_topics(n=10)

    else:
        agent_name = "TopicExplainerAgent"
        print(f"Selected agent: {agent_name}")
        docs = retrieve_docs(query, k=4)
        answer = explain_topic(query, docs, difficulty=difficulty)

    return {
        "agent": agent_name,
        "category": category,
        "answer": answer
    }


if __name__ == "__main__":
    queries = [
        ("give me a quick revision of demand paging", "intermediate"),
        ("create a 7 day study plan for os exam", "intermediate"),
        ("what are the most repeated topics", "intermediate"),
    ]

    for query, difficulty in queries:
        result = route_query(query, difficulty=difficulty)
        print(f"\nAgent: {result['agent']}")
        print(f"Answer:\n{result['answer']}")
        print("\n" + "="*60)