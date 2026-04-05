"""
INTEGRATION GUIDE: Study Plan Agent & Summary Generator

This document explains how to integrate and use the new agents in your frontend and backend.
"""

# ==================== QUICK START ====================

## Study Plan Agent

### Basic Usage

from agents.study_plan_agent import generate_study_plan_from_query

# User asks: "Create a 7 day study plan for my OS exam"
query = "Create a 7 day study plan for my OS exam"
study_plan = generate_study_plan_from_query(query, days=7, hours_per_day=6)
print(study_plan)

# User asks: "I have 5 days and 4 hours per day"
query_custom = "5 day study plan with 4 hours per day for DBMS"
study_plan_custom = generate_study_plan_from_query(query_custom)
# Automatically extracts: days=5, hours_per_day=4


### Advanced Usage

from agents.study_plan_agent import generate_study_plan_with_references

# For more control over study plan parameters:
topics = """
Module 1: SQL Basics
- DDL, DML, DCL
- Data types

Module 2: Normalization
- 1NF, 2NF, 3NF, BCNF
"""

plan = generate_study_plan_with_references(
    topics_text=topics,
    days=10,
    hours_per_day=5
)


### Router Integration

from agents.router import route_query

# When user says "create a study plan"
result = route_query(
    query="5 day study plan with 8 hours daily for OS",
    subject="OS",
    study_plan_days=5,  # Override if needed
    study_plan_hours=8  # Override if needed
)

print(f"Agent: {result['agent']}")  # StudyPlanAgent
print(f"Answer: {result['answer']}")


---

## Summary Generator Agent

### Format Options

from agents.summary_generator import generate_summary

# 1. STANDARD FORMAT - Comprehensive yet concise
summary_standard = generate_summary("Virtual Memory", format_type="standard")
# Output includes:
# - Key Concepts
# - Important Formulas/Theorems
# - Step-by-Step Explanation
# - Real-World Examples
# - Common Mistakes
# - Quick Facts
# - Exam Questions
# - Citations

# 2. LIGHTNING FORMAT - Maximum density, minimum time
summary_lightning = generate_summary("Process Scheduling", format_type="lightning")
# Output includes:
# - 30 Essential One-Liners
# - 15 Key Definitions  
# - 10 Key Formulas
# - 20 Expected Exam Questions
# - Memory Tricks

# 3. DETAILED FORMAT - Deep understanding
summary_detailed = generate_summary("Deadlocks", format_type="detailed")
# Output includes:
# - Introduction & Context
# - Fundamental Definitions
# - Detailed Explanation
# - Mathematical Foundations with Derivations
# - Worked Examples (step-by-step)
# - Application Areas
# - Common Misconceptions
# - Important Variations
# - Connections to Other Topics
# - Exam Strategy

# 4. CHECKLIST FORMAT - Structured study guide
summary_checklist = generate_summary("File Systems", format_type="checklist")
# Output includes:
# - Prerequisites Checklist
# - Must-Know Concepts Checklist
# - Formulas to Memorize Checklist
# - Problem-Solving Steps
# - Practice Questions
# - Common Pitfalls
# - Time Allocation
# - Last-Minute Revision Priority


### Auto-Detection from Query

from agents.router import route_query

# Query with explicit format request
result = route_query("Lightning summary of page replacement algorithms")
# Automatically detects: format="lightning"
# Routes to: SummaryGeneratorAgent

result = route_query("Give me detailed notes on virtual memory")
# Automatically detects: format="detailed"
# Routes to: SummaryGeneratorAgent


---

# ==================== FRONTEND INTEGRATION ====================

## Streamlit Integration

### Adding Summary Tab

import streamlit as st
from agents.router import route_query
from utils.context_formatter import format_sources_list

def show_summary_page():
    st.header("Summary / Revision")
    
    query = st.text_area("What would you like to summarize?", 
                        placeholder="e.g., Lightning summary of virtual memory")
    
    # Let user choose format explicitly if desired
    summary_format = st.selectbox(
        "Summary Format",
        ["Auto-detect", "Standard", "Lightning", "Detailed", "Checklist"]
    )
    
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            result = route_query(
                query=query,
                summary_format=None if summary_format == "Auto-detect" else summary_format.lower()
            )
            
            st.markdown("### Summary")
            st.markdown(result['answer'])
            
            # Display sources
            if 'sources' in result:
                st.markdown("### Sources")
                for source in result['sources']:
                    st.write(f"- {source['file']} | Page {source['page']}")


### Adding Study Plan Tab

def show_study_plan_page():
    st.header("Study Plan Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        num_days = st.number_input("Number of days", min_value=1, max_value=30, value=7)
    with col2:
        hours_per_day = st.number_input("Hours per day", min_value=1, max_value=12, value=6)
    
    query = st.text_input("What subjects/topics to plan for?",
                         placeholder="e.g., OS exam preparation")
    
    if st.button("Generate Study Plan"):
        with st.spinner("Creating your study plan..."):
            result = route_query(
                query=query,
                study_plan_days=num_days,
                study_plan_hours=hours_per_day
            )
            
            st.markdown("### Your Personalized Study Plan")
            st.markdown(result['answer'])


### Enhanced Main App

def main():
    st.set_page_config(page_title="Subject Guide Agent", layout="wide")
    
    st.sidebar.title("Subject Guide Agent")
    page = st.sidebar.radio("Go to", [
        "Upload Documents",
        "Ask Question",
        "Study Plan",        # NEW
        "Summary/Revision",  # NEW
        "Previous Year Questions"
    ])
    
    if page == "Upload Documents":
        show_upload_page()
    elif page == "Ask Question":
        show_query_page()
    elif page == "Study Plan":
        show_study_plan_page()
    elif page == "Summary/Revision":
        show_summary_page()
    elif page == "Previous Year Questions":
        show_pyq_page()


---

# ==================== OUTPUT STRUCTURES ====================

## Study Plan Output Structure

Study plans are generated with this structure:

Day 1: [Main Topic]
- Morning (3h): Topic A — Key concepts: [list]
- Afternoon/Evening: Topic B — Practice: [recommendations]
- Study Material: Use notes/textbooks
- [Additional tips]

Day 2: [Main Topic]
- ...

Extracted from course materials:
- filename1.pdf | Page 15
- filename2.pdf | Page 42


## Summary Output Structure - Standard Format

**Key Concepts:**
- Concept 1: [definition] [Source 1]
- Concept 2: [definition] [Source 2]

**Important Formulas/Theorems:**
- Formula 1 [Source X]
- Formula 2 [Source Y]

**Step-by-Step Explanation:**
[Detailed with source references]

**Real-World Examples:**
Example 1: [description] [Source X]
Example 2: [description] [Source Y]

**Common Mistakes to Avoid:**
1. Mistake 1 → How to fix
2. Mistake 2 → How to fix

**Quick Facts:**
1. [Memorable fact]
2. [Memorable fact]
...

**Frequently Asked Exam Questions:**
1. [Question]
2. [Question]

**Citations:**
[1] filename | Page number
[2] filename | Page number


## Summary Output Structure - Lightning Format

**30 Essential One-Liners:**
1. Term: [one-line fact] [Source X]
2. Term: [one-line fact] [Source Y]
...

**15 Key Definitions:**
[Similar structure]

**10 Key Formulas:**
[Formulas with sources]

**20 Expected Exam Questions:**
[Questions with sources]

**Memory Tricks:**
[Mnemonics and tricks]

**Source References:**
[1] filename | Page number
...


---

# ==================== USING DATA MODELS ====================

from utils.data_models import (
    Summary, SummaryFormat, StudyPlan, Citation,
    KeyConcept, Formula, WorkedExample
)

# Create structured response for API integration
citation1 = Citation("os_notes.pdf", "15", "notes")
citation2 = Citation("os_textbook.pdf", "234", "textbook")

concept = KeyConcept(
    term="Virtual Memory",
    definition="Abstraction that gives each process its own address space",
    explanation="Allows running larger programs than physical memory",
    citations=[citation1, citation2],
    related_terms=["Paging", "Segmentation", "TLB"]
)

formula = Formula(
    name="Page Replacement",
    formula="LRU: Replace page not used for longest time",
    description="Least Recently Used algorithm for page replacement",
    variables={"LRU": "Least Recently Used", "TLB": "Translation Lookaside Buffer"},
    derivation="Based on locality of reference principle",
    citations=[citation1],
    use_cases=["Virtual memory management", "Cache optimization"]
)

summary = Summary(
    topic="Virtual Memory",
    format=SummaryFormat.STANDARD,
    key_concepts=[concept],
    formulas=[formula]
)

# Convert to dict for JSON serialization
summary_dict = summary.to_dict()
print(json.dumps(summary_dict, indent=2))


---

# ==================== CITATION HANDLING ====================

## How Citations Work

Each retrieved document includes metadata:
{
    "source_file": "os_chapter_3.pdf",
    "page_number": 45,
    "doc_type": "textbook",
    "subject": "OS"
}

Agents use this metadata to:
1. Tag each retrieved chunk with [Source X]
2. Generate formatted citations at end: [X] os_chapter_3.pdf | Page 45
3. Ensure no claims are made without source attribution

## Citation Best Practices

✓ DO: Create citations from retrieved documents
✓ DO: Group related citations together
✓ DO: Display full citations at end
✗ DON'T: Make claims without source reference
✗ DON'T: Mix cited and non-cited content


---

# ==================== ERROR HANDLING ====================

## Common Issues

1. No documents uploaded
   - Study plan: Returns message asking for syllabus/materials
   - Summary: Returns message asking to upload materials

2. Query too vague
   - Use subject filter to narrow search
   - Specify exact topic name

3. No matching documents
   - Upload more relevant materials
   - Broaden query terms

## Validation

All agents validate:
- No hallucination (only use retrieved docs)
- Proper citations included
- Valid JSON output format
- Structured content requirements met


---

# ==================== TESTING ====================

Run the test suite:

python tests/test_new_agents.py

This validates:
- Study plan parameter extraction
- Summary format detection
- Router integration
- Data model serialization
- Citation accuracy
- No-hallucination constraint
- Structured format compliance


---

# ==================== API REFERENCE ====================

## Study Plan Agent

generate_study_plan_from_query(
    query: str,           # User query, can include day/hour parameters
    days: int = 7,        # Override number of days
    hours_per_day: int = 6  # Override hours per day
) -> str                  # Returns formatted study plan with citations


## Summary Generator

generate_summary(
    query: str,           # Topic to summarize
    format_type: str = "standard"  # One of: standard, lightning, detailed, checklist
) -> str                  # Returns formatted summary with citations


## Router

route_query(
    query: str,
    doc_type: str = None,
    subject: str = None,
    difficulty: str = "intermediate",
    summary_format: str = None,
    study_plan_days: int = None,
    study_plan_hours: int = None
) -> Dict


---

# ==================== BEST PRACTICES ====================

1. Always retrieve documents before LLM call
2. Use metadata filtering when possible (doc_type, subject)
3. Include full citations in final output
4. Validate structured output against data models
5. Test with real user queries before deployment
6. Log queries and responses for analysis
7. Handle edge cases (no documents, empty queries)
8. Provide fallback messages when needed
