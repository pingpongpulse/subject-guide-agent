import os
from dotenv import load_dotenv
from agents.query_classifier import classify_query
from agents.topic_explainer import explain_topic
from agents.question_solver import solve_question
from vectorstore.retriever import retrieve_docs

load_dotenv()


def route_query(query, doc_type=None, subject=None, difficulty="intermediate"):
    """
    Routes query to correct agent based on classification.
    """
    print(f"\nQuery received: {query}")

    # Step 1: Classify query
    category = classify_query(query)
    print(f"Query classified as: {category}")

    # Step 2: Retrieve relevant docs
    docs = retrieve_docs(query, k=4, doc_type=doc_type, subject=subject)
    print(f"Retriever returned {len(docs)} chunks")

    # Step 3: Route to correct agent
    if category == "topic_explanation":
        agent_name = "TopicExplainerAgent"
        print(f"Selected agent: {agent_name}")
        answer = explain_topic(query, docs, difficulty=difficulty)

    elif category == "question_solving":
        agent_name = "QuestionSolverAgent"
        print(f"Selected agent: {agent_name}")
        answer = solve_question(query, docs, difficulty=difficulty)

    elif category == "revision":
        agent_name = "RevisionAgent"
        print(f"Selected agent: {agent_name}")
        answer = "[RevisionAgent coming in Week 5]"

    elif category == "study_plan":
        agent_name = "StudyPlanAgent"
        print(f"Selected agent: {agent_name}")
        answer = "[StudyPlanAgent coming in Week 5]"

    else:
        agent_name = "TopicExplainerAgent"
        print(f"Selected agent: {agent_name}")
        answer = explain_topic(query, docs, difficulty=difficulty)

    return {
        "agent": agent_name,
        "category": category,
        "answer": answer
    }


if __name__ == "__main__":
    result = route_query(
        "Explain the Banker's algorithm for deadlock avoidance",
        difficulty="intermediate"
    )
    print(f"\nAgent: {result['agent']}")
    print(f"\n{result['answer']}")