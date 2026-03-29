import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def format_context(docs):
    """
    Formats retrieved docs into a clean context string for LLM prompts.
    Handles both Document objects and plain dicts.
    """
    context = ""
    for i, doc in enumerate(docs):
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
            doc_type = doc.metadata.get("doc_type", "notes")
            subject = doc.metadata.get("subject", "general")
            text = doc.page_content[:500]
        else:
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")
            doc_type = doc.get("doc_type", "notes")
            subject = doc.get("subject", "general")
            text = doc.get("text", "")[:500]

        context += (
            f"\n[Source {i+1}: {source} | "
            f"Page {page} | "
            f"Type: {doc_type} | "
            f"Subject: {subject}]\n{text}\n"
        )
    return context


def format_sources_list(docs):
    """
    Returns a clean list of sources for display.
    """
    sources = []
    seen = set()

    for doc in docs:
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page_number", "?")
        else:
            source = doc.get("source_file", "unknown")
            page = doc.get("page_number", "?")

        key = f"{source}_page_{page}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": source,
                "page": page
            })

    return sources


def format_answer_with_sources(answer, docs):
    """
    Appends a formatted sources section to any answer.
    """
    sources = format_sources_list(docs)

    if not sources:
        return answer

    sources_text = "\n\n**Sources Used:**\n"
    for s in sources:
        sources_text += f"- {s['file']} | Page {s['page']}\n"

    return answer + sources_text


if __name__ == "__main__":
    dummy_docs = [
        {
            "text": "Demand paging loads pages only when needed.",
            "source_file": "os_notes.pdf",
            "page_number": 10,
            "doc_type": "notes",
            "subject": "os"
        },
        {
            "text": "Page fault occurs when page is not in memory.",
            "source_file": "os_textbook.pdf",
            "page_number": 45,
            "doc_type": "textbook",
            "subject": "os"
        }
    ]

    print(format_context(dummy_docs))
    print(format_sources_list(dummy_docs))