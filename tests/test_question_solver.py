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
        "query": "A system has 3 processes P1 P2 P3 and 3 resources. Available resources are 3 3 2. Allocation matrix is P1: 0 1 0, P2: 2 0 0, P3: 3 0 2. Max matrix is P1: 7 5 3, P2: 3 2 2, P3: 9 0 2. Find if the system is in a safe state using Banker's algorithm and find the safe sequence.",
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