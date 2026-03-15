import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.router import route_query

# Dummy docs simulating what retriever will return
dummy_docs = [
    {
        "text": "Demand paging is a technique where pages are brought into memory only when required by the process.",
        "source_file": "os_notes.pdf",
        "page_number": 10,
        "doc_type": "notes"
    },
    {
        "text": "Page fault occurs when the required page is not in memory. OS handles it by loading the page from disk.",
        "source_file": "os_textbook.pdf",
        "page_number": 45,
        "doc_type": "textbook"
    },
    {
        "text": "Advantages of demand paging: less memory usage, faster startup, supports large virtual address spaces.",
        "source_file": "os_notes.pdf",
        "page_number": 11,
        "doc_type": "notes"
    },
    {
        "text": "Q. Explain demand paging with example. (10 marks) - 2022 OS exam paper",
        "source_file": "os_pyq_2022.pdf",
        "page_number": 2,
        "doc_type": "pyq"
    }
]

result = route_query("Explain demand paging", dummy_docs)

print(f"\nAgent: {result['agent']}")
print(f"Retrieved chunks: {len(dummy_docs)}")
print(f"\n{result['answer']}")