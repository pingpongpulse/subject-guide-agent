import os
from dotenv import load_dotenv
from agents.query_classifier import classify_query
from agents.topic_explainer import explain_topic
from vectorstore.retriever import retrieve_docs

load_dotenv()

def route_query(query, doc_type=None, subject=None):
    """
    Routes query to the correct agent based on classification.
    """
    print(f"\nQuery received: {query}")

    # Step 1: Classify
    category = classify_query(query)
    print(f"Query classified as: {category}")
    docs = retrieve_docs(query, k=4)
    print(f"Retriever returned {len(docs)} chunks")

    # Step 2: Route to correct agent
    if category == "topic_explanation":
        agent_name = "TopicExplainerAgent"
        print(f"Selected agent: {agent_name}")
        print(f"Retrieved chunks: {len(docs)}")
        answer = explain_topic(query, docs)

    elif category == "question_solving":
        agent_name = "QuestionSolverAgent"
        print(f"Selected agent: {agent_name}")
        answer = "[QuestionSolverAgent coming in Week 3]"

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
        answer = explain_topic(query, docs)

    return {
        "agent": agent_name,
        "category": category,
        "answer": answer
    }


if __name__ == "__main__":
    # Test with dummy docs
    dummy_docs = [
        {
            "text": "Demand paging loads pages into memory only when they are needed during execution.",
            "source_file": "os_notes.pdf",
            "page_number": 10,
            "doc_type": "notes"
        }
    ]

    result = route_query("Explain demand paging", dummy_docs)
    print("\n--- FINAL OUTPUT ---")
    print(f"Agent: {result['agent']}")
    print(f"Answer:\n{result['answer']}")