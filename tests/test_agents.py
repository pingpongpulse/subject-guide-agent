import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.router import route_query

result = route_query("Explain demand paging")

print(f"\nAgent: {result['agent']}")
print(f"\n{result['answer']}")