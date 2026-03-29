import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.pyq_heatmap import get_heatmap_data, get_top_n_topics

print("="*60)
print("Test 1: Full heatmap data")
print("="*60)
data = get_heatmap_data()
print(f"Status: {data['message']}")
print(f"Total topics: {len(data['topics'])}")
print(f"Topics: {data['topics'][:5]}")
print(f"Frequencies: {data['frequencies'][:5]}")

print("\n" + "="*60)
print("Test 2: Top 15 topics only")
print("="*60)
top = get_top_n_topics(n=15)
for topic, freq in top.items():
    print(f"  {topic}: {freq}")