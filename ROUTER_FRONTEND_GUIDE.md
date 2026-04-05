# Router Integration - Frontend Developer Guide

This guide shows how to use the updated `route_query()` function in frontend applications (Streamlit, Flask, etc.).

## Quick Start

### Import the Router
```python
from agents.router import route_query
```

### Basic Query Routing
```python
# Simple query - auto-routes to appropriate agent
result = route_query("What is demand paging?")
print(result["agent"])        # "TopicExplainerAgent"
print(result["answer"])       # Explanation text
print(result["sources"])      # List of source documents
```

## Common Use Cases

### 1. Topic Explanation Query
```python
result = route_query(
    query="Explain virtual memory in detail",
    difficulty="intermediate"  # beginner, intermediate, exam
)

# Response structure:
# {
#   "agent": "TopicExplainerAgent",
#   "category": "topic_explanation",
#   "answer": "...formatted explanation...",
#   "sources": ["os_notes.pdf Page 5", "textbook.pdf Page 12"],
#   "status": "success"
# }
```

### 2. Question Solving
```python
result = route_query(
    query="Solve: What causes page faults?",
    difficulty="exam"
)

# Response structure:
# {
#   "agent": "QuestionSolverAgent",
#   "category": "question_solving",
#   "answer": "...step-by-step solution...",
#   "sources": [...],
#   "status": "success"
# }
```

### 3. Generate Summary (Auto Mode Detection)
```python
# Mode is auto-detected from keywords
result = route_query("Quick summary of deadlocks")
print(result["agent"])    # "SummaryAgent"
print(result["mode"])     # "revision" (auto-detected from "quick")

# Response structure:
# {
#   "agent": "SummaryAgent",
#   "category": "revision",
#   "answer": "...condensed summary with 5 key points...",
#   "sources": [...],
#   "mode": "revision",
#   "status": "success"
# }
```

### 4. Generate Summary (Forced Mode)
```python
# Force a specific summary mode
result = route_query(
    query="Summarize file systems",
    summary_mode="detailed"  # Override auto-detection
)
print(result["mode"])     # "detailed"

# Available modes:
# - "standard": 6-section structured summary
# - "revision": 5-point condensed summary (for quick review)
# - "detailed": 9-section comprehensive summary with examples
```

### 5. Generate Study Plan
```python
result = route_query(
    query="Create a 2-week study plan focusing on 15 hours per week",
    syllabus_pdf_path="/absolute/path/to/syllabus.pdf"
)

# Response structure:
# {
#   "agent": "StudyPlanAgent",
#   "category": "study_plan",
#   "answer": {
#     "week_1": {...},
#     "week_2": {...},
#     ...
#   },
#   "sources": [...referenced_documents...],
#   "modules_analyzed": ["Module 1", "Module 2", ...],
#   "study_plan_metadata": {...},
#   "status": "success"
# }

# Access study plan data
plan_dict = result["answer"]  # Dictionary of week-by-week plans
weeks_covered = len([k for k in plan_dict.keys() if k.startswith('week_')])
modules = result.get("modules_analyzed", [])
```

### 6. Previous Year Questions Analysis
```python
result = route_query("Show top exam topics from previous questions")

# Response structure:
# {
#   "agent": "PYQAnalyzerAgent",
#   "category": "pyq_analysis",
#   "answer": {...pyq_analysis_data...},
#   "status": "success"
# }
```

## Parameter Reference

### Core Parameters

| Parameter | Type | Required | Default | Purpose |
|-----------|------|----------|---------|---------|
| `query` | str | ✅ Yes | - | User's question or request |
| `doc_type` | str | ❌ No | None | Filter by document type ("pdf", "docx", etc.) |
| `subject` | str | ❌ No | None | Filter by subject area |
| `difficulty` | str | ❌ No | "intermediate" | Query difficulty level |
| `summary_mode` | str | ❌ No | None | Force summary mode: "standard", "revision", "detailed" |
| `syllabus_pdf_path` | str | ❌ No | None | **Required for study_plan queries** |

### Query Classification

The router automatically classifies queries into categories:

| Category | Triggers | Default Agent |
|----------|----------|---|
| `topic_explanation` | General questions | TopicExplainerAgent |
| `question_solving` | Problem-solving questions | QuestionSolverAgent |
| `revision` | Revision/summary requests | RevisionAgent or SummaryAgent |
| `study_plan` | Study planning requests | StudyPlanAgent |
| `pyq_analysis` | Previous year questions | PYQAnalyzerAgent |

## Response Structure

Every response has this guaranteed structure:

```python
{
    "agent": str,              # Which agent handled the query
    "category": str,           # Query category
    "answer": str|dict,        # Main response (type depends on agent)
    "sources": list,           # Source documents used
    "status": "success" or "error",  # Execution status
    "error": str|None,         # Error message if status=="error"
    
    # Optional fields per agent:
    "mode": str,               # For SummaryAgent (revision/standard/detailed)
    "study_plan_metadata": dict,  # For StudyPlanAgent
    "modules_analyzed": list,  # For StudyPlanAgent
}
```

## Error Handling

### Handling Errors
```python
result = route_query(
    query="Create study plan",
    # Missing: syllabus_pdf_path
)

if result["status"] == "error":
    print(f"Error: {result['error']}")
    # Output: "Error: No syllabus PDF path provided"
else:
    # Process successful result
    answer = result["answer"]
```

### Error Types

| Scenario | Status | Error Message |
|----------|--------|---|
| Study plan without PDF | `error` | "No syllabus PDF path provided" |
| Failed document retrieval | `error` | "Error retrieving documents: ..." |
| Missing API key | `error` | "Error: GROQ_API_KEY not configured" |
| Query classification failure | `success` (fallback) | Falls back to topic_explanation |

## Streamlit Integration Example

```python
import streamlit as st
from agents.router import route_query

st.set_page_config(page_title="Academic Assistant", layout="wide")

# Sidebar for query parameters
with st.sidebar:
    difficulty = st.select_slider("Difficulty", 
                                   options=["beginner", "intermediate", "exam"])
    doc_type = st.text_input("Document type filter (optional)")
    subject = st.text_input("Subject filter (optional)")

# Main query interface
query = st.text_area("Ask a question:")

if st.button("Get Answer"):
    with st.spinner("Processing..."):
        result = route_query(
            query=query,
            doc_type=doc_type or None,
            subject=subject or None,
            difficulty=difficulty
        )
    
    # Display results
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Answer from {result['agent']}")
        if result["status"] == "error":
            st.error(result["error"])
        else:
            # Format answer based on type
            if isinstance(result["answer"], dict):
                st.json(result["answer"])
            else:
                st.markdown(result["answer"])
    
    with col2:
        st.metric("Sources", len(result.get("sources", [])))
        if result.get("mode"):
            st.info(f"Mode: {result['mode']}")
```

## Study Plan Tab Integration

```python
if selected_tab == "Study Plan":
    uploaded_file = st.file_uploader("Upload Syllabus PDF", type="pdf")
    
    col1, col2 = st.columns(2)
    with col1:
        weeks = st.number_input("Weeks:", min_value=1, max_value=16, value=8)
    with col2:
        hours = st.number_input("Hours per week:", min_value=5, max_value=50, value=20)
    
    if st.button("Generate Study Plan") and uploaded_file:
        # Save uploaded file
        pdf_path = f"/tmp/{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Generate plan
        result = route_query(
            query=f"Generate {weeks}-week study plan with {hours} hours per week",
            syllabus_pdf_path=pdf_path
        )
        
        if result["status"] == "success":
            plan = result["answer"]
            
            # Display each week
            for week_key in sorted(plan.keys()):
                with st.expander(f"📅 {week_key}"):
                    st.write(plan[week_key])
            
            # Show metadata
            if result.get("modules_analyzed"):
                st.info(f"Modules analyzed: {', '.join(result['modules_analyzed'])}")
```

## Summary Tab Integration

```python
if selected_tab == "Summary":
    mode_col, auto_col = st.columns([2, 1])
    
    with mode_col:
        mode = st.radio("Summary Type", 
                       ["Auto-detect", "Standard", "Revision", "Detailed"],
                       horizontal=True)
    
    query = st.text_area("Topic to summarize:")
    
    if st.button("Generate Summary"):
        # Map UI selection to mode
        mode_map = {
            "Auto-detect": None,
            "Standard": "standard",
            "Revision": "revision",
            "Detailed": "detailed"
        }
        
        result = route_query(
            query=query,
            summary_mode=mode_map[mode]
        )
        
        if result["status"] == "success":
            st.markdown(result["answer"])
            
            with st.expander("📚 Sources"):
                for source in result.get("sources", []):
                    st.caption(source)
            
            if result.get("mode"):
                st.caption(f"Generated in {result['mode']} mode")
```

## Mode Detection Examples

The router automatically detects summary modes from keywords:

```python
queries_and_modes = [
    # Revision mode keywords
    ("Give me quick notes", "revision"),
    ("Lightning summary", "revision"),
    ("Condensed overview", "revision"),
    ("Show me a revision sheet", "revision"),
    
    # Detailed mode keywords
    ("Comprehensive summary", "detailed"),
    ("Deep dive into", "detailed"),
    ("Explain in detail", "detailed"),
    
    # Standard mode keywords
    ("Summarize this", "standard"),
    ("Condense the key points", "standard"),
    ("Create an outline", "standard"),
]

for query, expected_mode in queries_and_modes:
    from agents.router import _detect_summary_format
    detected = _detect_summary_format(query)
    print(f"{query} → {detected}")
```

## Logging and Debugging

The router provides detailed logging for debugging:

```python
import logging

# Enable logging to see router decisions
logging.basicConfig(level=logging.INFO)

result = route_query("What is deadlock?")
# Console output:
# Query received: What is deadlock?
# Query classified as: topic_explanation
# Selected agent: TopicExplainerAgent
# Retriever returned 4 chunks
# Response status: success
# Sources extracted: 3
```

## Best Practices

1. **Always check response status**
   ```python
   if result["status"] != "success":
       handle_error(result["error"])
   ```

2. **Provide PDF path for study plans**
   ```python
   assert syllabus_pdf_path, "Study plan requires PDF path"
   ```

3. **Cache results when possible**
   ```python
   @st.cache_data(ttl=3600)
   def get_summary(query, mode):
       return route_query(query, summary_mode=mode)
   ```

4. **Validate user inputs**
   ```python
   if not query.strip():
       st.warning("Please enter a query")
       return
   ```

5. **Handle large responses**
   ```python
   if len(result["answer"]) > 5000:
       st.info("Large response detected. Showing summary...")
       st.text(result["answer"][:5000] + "...")
   ```

---

## Questions?

For implementation questions, refer to:
- [Router Integration Summary](./ROUTER_INTEGRATION_SUMMARY.md)
- [Study Plan Generator](./agents/study_plan_generator.py)
- [Summary Agent](./agents/summary_agent.py)
