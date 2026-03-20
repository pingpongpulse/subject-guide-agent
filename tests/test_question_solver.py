import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.router import route_query

test_questions = [
    {
        "query": "Explain the Banker's algorithm for deadlock avoidance with example",
        "difficulty": "intermediate"
    },
    {
        "query": "A system has 3 processes and 4 resources. Find if the system is in safe state.",
        "difficulty": "intermediate"
    },
    {
        "query": "Derive the expression for effective access time in demand paging",
        "difficulty": "exam"
    }
]

for test in test_questions:
    print("\n" + "="*60)
    print(f"Testing: {test['query'][:50]}...")
    print("="*60)

    result = route_query(
        test["query"],
        difficulty=test["difficulty"]
    )

    print(f"\nAgent: {result['agent']}")
    print(f"Category: {result['category']}")
    print(f"\n{result['answer']}")
    print("\n")