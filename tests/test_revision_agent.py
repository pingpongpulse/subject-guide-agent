import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.revision_agent import get_revision, get_lightning_revision

print("="*60)
print("Test 1: Standard Revision")
print("="*60)
result = get_revision("demand paging", mode="standard")
print(result)

print("\n" + "="*60)
print("Test 2: Lightning Revision Mode")
print("="*60)
result2 = get_lightning_revision("process scheduling")
print(result2)