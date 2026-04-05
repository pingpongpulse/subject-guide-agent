import sys
import os
import re
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from agents.query_classifier import classify_query
from agents.topic_explainer import explain_topic
from agents.question_solver import solve_question
from agents.pyq_analyzer import get_top_topics
from agents.revision_agent import get_revision
from agents.study_plan_generator import generate_study_plan_from_query
from agents.summary_agent import generate_summary
from vectorstore.retriever import retrieve_docs

load_dotenv()


def _detect_summary_format(query):
    """
    Detects if user is requesting a specific summary format/mode from the query.
    Returns mode type: 'standard', 'revision', 'detailed', or None
    Maps to Summary Agent modes: 'standard', 'revision', 'detailed'
    """
    query_lower = query.lower()
    
    # Map user keywords to summary agent modes
    if any(keyword in query_lower for keyword in ['lightning', 'quick summary', 'quick notes', 'one-liner', '30 liners', 'quick', 'revision', 'short', 'condensed']):
        return 'revision'  # Condensed/revision mode
    elif any(keyword in query_lower for keyword in ['detailed summary', 'in-depth', 'detailed notes', 'deep dive', 'comprehensive']):
        return 'detailed'  # Detailed mode
    elif any(keyword in query_lower for keyword in ['summary', 'summarize', 'condense', 'summarise', 'outline']):
        return 'standard'  # Standard mode
    
    return None


def _extract_study_plan_params(query):
    """
    Extracts custom parameters for study plan from query.
    Returns dict with 'weeks' and 'hours_per_week'
    """
    params = {'weeks': 8, 'hours_per_week': 20}  # Default: 8 weeks, 20 hours/week
    
    # Extract weeks/days: "7 days", "in 5 days", "7-day", "2 weeks"
    week_match = re.search(r'(\d+)\s*-?weeks?', query.lower())
    if week_match:
        params['weeks'] = int(week_match.group(1))
    else:
        # Try to parse days and convert to weeks
        day_match = re.search(r'(\d+)\s*-?days?', query.lower())
        if day_match:
            days = int(day_match.group(1))
            params['weeks'] = max(1, days // 7)  # Convert days to weeks (minimum 1)
    
    # Extract hours per week: "20 hours", "with 15 hours", "study 30 hours per week"
    hour_match = re.search(r'(\d+)\s*hours?.*(?:week|day)?', query.lower())
    if hour_match:
        params['hours_per_week'] = int(hour_match.group(1))
    
    return params


def route_query(query, doc_type=None, subject=None, difficulty="intermediate", 
                summary_mode=None, syllabus_pdf_path=None):
    """
    Routes user query to appropriate agent.
    
    Args:
        query: User query string
        doc_type: Filter by document type (optional)
        subject: Filter by subject (optional)
        difficulty: 'beginner', 'intermediate', 'exam'
        summary_mode: Force specific summary mode ('standard', 'revision', 'detailed')
        syllabus_pdf_path: Path to syllabus PDF for study plan generation
    
    Returns:
        Dict with 'agent', 'category', 'answer', 'sources', and logging info
    """
    print(f"\n{'='*70}")
    print(f"Query received: {query}")
    print(f"Parameters: doc_type={doc_type}, subject={subject}, difficulty={difficulty}")

    # Classify query
    try:
        category = classify_query(query)
        print(f"Query classified as: {category}")
    except Exception as e:
        print(f"Error classifying query: {e}")
        category = "topic_explanation"
    
    result = {
        "agent": None,
        "category": category,
        "answer": None,
        "sources": [],
        "status": "success",
        "error": None
    }

    try:
        if category == "topic_explanation":
            result["agent"] = "TopicExplainerAgent"
            print(f"Selected agent: {result['agent']}")
            docs = retrieve_docs(query, k=4, subject=subject, doc_type=doc_type)
            print(f"  Retriever returned {len(docs)} chunks")
            result["answer"] = explain_topic(query, docs, difficulty=difficulty)
            # Extract sources from docs
            for doc in docs[:3]:  # Limit to top 3 sources
                if hasattr(doc, 'metadata'):
                    source = f"{doc.metadata.get('source_file', 'unknown')} Page {doc.metadata.get('page_number', '?')}"
                else:
                    source = f"{doc.get('source_file', 'unknown')} Page {doc.get('page_number', '?')}"
                if source not in result["sources"]:
                    result["sources"].append(source)

        elif category == "question_solving":
            result["agent"] = "QuestionSolverAgent"
            print(f"Selected agent: {result['agent']}")
            docs = retrieve_docs(query, k=4, subject=subject, doc_type=doc_type)
            print(f"  Retriever returned {len(docs)} chunks")
            result["answer"] = solve_question(query, docs, difficulty=difficulty)
            # Extract sources
            for doc in docs[:3]:
                if hasattr(doc, 'metadata'):
                    source = f"{doc.metadata.get('source_file', 'unknown')} Page {doc.metadata.get('page_number', '?')}"
                else:
                    source = f"{doc.get('source_file', 'unknown')} Page {doc.get('page_number', '?')}"
                if source not in result["sources"]:
                    result["sources"].append(source)

        elif category == "revision":
            # Determine which mode to use
            mode = summary_mode or _detect_summary_format(query)
            
            if mode:  # User requested summary
                result["agent"] = "SummaryAgent"
                print(f"Selected agent: {result['agent']} (mode: {mode})")
                summary_data = generate_summary(query, mode=mode, retriever_k=5)
                result["answer"] = summary_data.get("content", "")
                result["sources"] = summary_data.get("sources", [])
                result["mode"] = mode
                
                # Pass formulas if present (optional field)
                if "formulas" in summary_data:
                    result["formulas"] = summary_data["formulas"]
                    print(f"  Formulas extracted: {len(summary_data['formulas'])} found")
                
                print(f"  Summary generated in {mode} mode")
                print(f"  Sources: {len(result['sources'])} documents")
            else:  # Standard revision
                result["agent"] = "RevisionAgent"
                print(f"Selected agent: {result['agent']}")
                result["answer"] = get_revision(query, mode="standard")
                print(f"  Revision notes generated")

        elif category == "study_plan":
            result["agent"] = "StudyPlanAgent"
            print(f"Selected agent: {result['agent']}")
            
            # Use provided syllabus path or prompt user
            if not syllabus_pdf_path:
                print("  Warning: No syllabus PDF path provided")
                result["answer"] = "Error: Please provide path to syllabus PDF for study plan generation."
                result["status"] = "error"
                result["error"] = "No syllabus PDF path provided"
            else:
                # Extract parameters from query
                params = _extract_study_plan_params(query)
                print(f"  Study plan parameters: weeks={params['weeks']}, hours_per_week={params['hours_per_week']}")
                
                try:
                    plan_data = generate_study_plan_from_query(
                        syllabus_pdf_path,
                        weeks=params['weeks'],
                        hours_per_week=params['hours_per_week'],
                        retriever_k=5
                    )
                    result["answer"] = plan_data.get("plan", {})
                    result["sources"] = plan_data.get("sources", [])
                    result["study_plan_metadata"] = plan_data.get("metadata", {})
                    result["modules_analyzed"] = plan_data.get("modules_analyzed", [])
                    print(f"  Study plan generated: {len(plan_data.get('modules_analyzed', []))} modules")
                    print(f"  Sources: {len(result['sources'])} documents")
                except Exception as e:
                    result["status"] = "error"
                    result["error"] = str(e)
                    result["answer"] = f"Error generating study plan: {str(e)}"
                    print(f"  Error: {e}")

        elif category == "pyq_analysis":
            result["agent"] = "PYQAnalyzerAgent"
            print(f"Selected agent: {result['agent']}")
            result["answer"] = get_top_topics(n=10)
            print(f"  PYQ analysis generated")

        else:
            # Default to topic explanation
            result["agent"] = "TopicExplainerAgent"
            print(f"Selected agent: {result['agent']} (default fallback)")
            docs = retrieve_docs(query, k=4, subject=subject, doc_type=doc_type)
            print(f"  Retriever returned {len(docs)} chunks")
            result["answer"] = explain_topic(query, docs, difficulty=difficulty)
            # Extract sources
            for doc in docs[:3]:
                if hasattr(doc, 'metadata'):
                    source = f"{doc.metadata.get('source_file', 'unknown')} Page {doc.metadata.get('page_number', '?')}"
                else:
                    source = f"{doc.get('source_file', 'unknown')} Page {doc.get('page_number', '?')}"
                if source not in result["sources"]:
                    result["sources"].append(source)

    except Exception as e:
        print(f"Error in route_query: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["answer"] = f"Error processing query: {str(e)}"
        result["agent"] = "ErrorHandler"
    
    print(f"Response status: {result['status']}")
    print(f"Sources extracted: {len(result['sources'])}")
    print(f"{'='*70}\n")
    
    return result


if __name__ == "__main__":
    # Test queries covering all agents
    test_queries = [
        # Topic explanation
        ("What is demand paging?", "intermediate"),
        
        # Question solving
        ("Solve this OS problem", "exam"),
        
        # Revision
        ("Give me revision notes on process scheduling", "intermediate"),
        
        # Summary with formats
        ("Lightning summary of virtual memory", "intermediate"),
        ("Detailed summary of deadlocks", "intermediate"),
        
        # Study plan with custom parameters
        ("Create a 5 day study plan for os", "intermediate"),
        ("Generate 10 day study plan with 8 hours per day", "intermediate"),
        
        # PYQ Analysis
        ("What topics appeared most in previous exams?", "intermediate"),
    ]

    for query, difficulty in test_queries:
        print("\n" + "="*70)
        result = route_query(query, difficulty=difficulty)
        print(f"\nAgent: {result['agent']}")
        print(f"Category: {result['category']}")
        if 'format' in result:
            print(f"Format: {result['format']}")
        print(f"\nAnswer Preview (first 300 chars):\n{result['answer'][:300]}...")
        print("="*70)