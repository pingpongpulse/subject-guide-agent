import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.study_plan_agent import generate_study_plan_from_query

print("="*60)
print("Test: Study Plan Generator")
print("="*60)

result = generate_study_plan_from_query(
    "generate a 7 day study plan for operating systems",
    days=7
)
print(result)