import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.pyq_analyzer import analyze_pyq_frequency, get_top_topics
from agents.router import route_query

print("="*60)
print("Test 1: Direct PYQ frequency analysis")
print("="*60)
frequency = analyze_pyq_frequency()

if frequency:
    print(f"\nTotal unique topics found: {len(frequency)}")
    print("Top 5 topics:")
    for topic, count in list(frequency.items())[:5]:
        print(f"  {topic}: {count} times")
else:
    print("No PYQ docs found — upload past papers first")

print("\n" + "="*60)
print("Test 2: Router triggered by student query")
print("="*60)
result = route_query("What are the most repeated topics in past papers?")
print(f"\nAgent: {result['agent']}")
print(f"\n{result['answer']}")

print("\n" + "="*60)
print("Test 3: Another trigger phrase")
print("="*60)
result2 = route_query("What should I focus on for my exam?")
print(f"\nAgent: {result2['agent']}")
print(f"\n{result2['answer']}")