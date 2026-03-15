from langchain_core.documents import Document

def format_context(docs: list[Document]) -> str:
    """
    Converts retrieved documents into a clean string
    that gets pasted directly into the LLM prompt.
    
    Every agent calls this — do not change the output format
    without telling Person 1.
    
    Output looks like:
    [Source 1: Operating_Systems.pdf | Page 12 | Type: notes | Score: 0.748]
    Introduction to Virtual File System (VFS)...
    
    ---
    
    [Source 2: test.png | Page 1 | Type: notes | Score: 0.496]
    Demand paging content...
    """
    if not docs:
        return "No relevant content found in uploaded documents."

    formatted_parts = []

    for i, doc in enumerate(docs):
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page_number", "?")
        doc_type = doc.metadata.get("doc_type", "unknown")
        score = doc.metadata.get("relevance_score", "?")

        header = f"[Source {i+1}: {source} | Page {page} | Type: {doc_type} | Score: {score}]"
        content = doc.page_content.strip()

        formatted_parts.append(f"{header}\n{content}")

    return "\n\n---\n\n".join(formatted_parts)


def format_sources_list(docs: list[Document]) -> list[str]:
    """
    Returns a clean list of source strings for display in UI.
    
    Output:
    ["Operating_Systems.pdf — Page 12", "test.png — Page 1"]
    """
    sources = []
    seen = set()

    for doc in docs:
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page_number", "?")
        label = f"{source} — Page {page}"

        if label not in seen:
            sources.append(label)
            seen.add(label)

    return sources