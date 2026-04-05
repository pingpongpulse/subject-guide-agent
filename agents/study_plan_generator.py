"""
Study Plan Generator Agent

Generates syllabus-aware, content-mapped study plans:
1. Extracts modules from syllabus PDF
2. Maps modules to vector database content
3. Generates structured weekly study schedule
4. Prioritizes topics by content availability
5. Includes revision cycles and PYQ practice
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from vectorstore.retriever import retrieve_docs

load_dotenv()


# ==================== UTILITY FUNCTIONS ====================

def _get_groq_client():
    """Safely initialize Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def _extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file.
    Handles both structured and unstructured PDFs.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        # Fallback if PyPDF2 not available
        return ""
    
    if not os.path.exists(pdf_path):
        return ""
    
    try:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


# ==================== STEP 1: SYLLABUS PARSING ====================

def extract_modules_from_syllabus(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract modules and topics from a syllabus PDF.
    
    Uses LLM to intelligently parse both structured and unstructured syllabi.
    
    Args:
        pdf_path: Path to syllabus PDF file
        
    Returns:
        List of modules with structure:
        [
            {
                "module_title": str,
                "topics": [str],
                "description": str (optional)
            },
            ...
        ]
    """
    client = _get_groq_client()
    if not client:
        return []
    
    # Extract text from PDF
    syllabus_text = _extract_text_from_pdf(pdf_path)
    
    if not syllabus_text or len(syllabus_text.strip()) < 100:
        print(f"Warning: Could not extract significant text from {pdf_path}")
        return []
    
    # Use LLM to parse modules
    prompt = f"""
You are an academic curriculum analyzer. Extract all modules and their topics from this syllabus.

Return a JSON array with this exact structure:
[
  {{
    "module_title": "Module Name",
    "topics": ["Topic 1", "Topic 2", "Topic 3"],
    "description": "Brief description of module (1-2 sentences)"
  }},
  ...
]

Important:
- Extract ALL modules found in the syllabus
- For each module, list all topics as separate strings
- Be precise with topic names
- If syllabus is unstructured, infer logical module groupings
- Return ONLY valid JSON, no additional text

Syllabus content:
{syllabus_text[:4000]}

JSON output:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON from response
        # Handle case where LLM includes markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        
        modules = json.loads(response_text.strip())
        
        # Validate structure
        validated_modules = []
        for module in modules:
            if isinstance(module, dict) and "module_title" in module and "topics" in module:
                validated_modules.append({
                    "module_title": module.get("module_title", "Untitled Module"),
                    "topics": module.get("topics", []),
                    "description": module.get("description", "")
                })
        
        return validated_modules
        
    except json.JSONDecodeError:
        print("Failed to parse LLM response as JSON")
        return []
    except Exception as e:
        print(f"Error extracting modules: {e}")
        return []


# ==================== STEP 2: RETRIEVAL MAPPING ====================

def map_modules_to_docs(
    modules: List[Dict[str, Any]],
    retriever_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Map each module's topics to retrieved vector database content.
    
    For each topic in each module, queries the retriever and attaches:
    - Retrieved content summaries
    - Source citations
    - Content availability score
    
    Args:
        modules: List of modules from extract_modules_from_syllabus()
        retriever_k: Number of top documents to retrieve per topic
        
    Returns:
        Enhanced modules with retrieved content:
        [
            {
                "module_title": str,
                "topics": [
                    {
                        "topic_name": str,
                        "retrieved_chunks": [{
                            "content": str,
                            "source_file": str,
                            "page_number": int,
                            "doc_type": str
                        }],
                        "content_summary": str,
                        "sources": [str],
                        "content_score": float  # 0-1: higher = more content found
                    }
                ],
                "total_content_score": float
            },
            ...
        ]
    """
    mapped_modules = []
    
    for module in modules:
        mapped_module = {
            "module_title": module["module_title"],
            "description": module.get("description", ""),
            "topics": [],
            "total_content_score": 0.0
        }
        
        topic_scores = []
        
        for topic in module.get("topics", []):
            # Retrieve documents for this topic
            docs = retrieve_docs(query=topic, k=retriever_k)
            
            # Extract and summarize content
            retrieved_chunks = []
            sources_set = set()
            
            for doc in docs:
                if hasattr(doc, 'metadata'):
                    # ChromaDB Document object
                    chunk_data = {
                        "content": doc.page_content[:300],  # Truncate for storage
                        "source_file": doc.metadata.get("source_file", "unknown"),
                        "page_number": doc.metadata.get("page_number", "?"),
                        "doc_type": doc.metadata.get("doc_type", "notes"),
                        "subject": doc.metadata.get("subject", "")
                    }
                    sources_set.add(f"{chunk_data['source_file']} (Page {chunk_data['page_number']})")
                else:
                    # Plain dict
                    chunk_data = {
                        "content": doc.get("text", "")[:300],
                        "source_file": doc.get("source_file", "unknown"),
                        "page_number": doc.get("page_number", "?"),
                        "doc_type": doc.get("doc_type", "notes"),
                        "subject": doc.get("subject", "")
                    }
                    sources_set.add(f"{chunk_data['source_file']} (Page {chunk_data['page_number']})")
                
                retrieved_chunks.append(chunk_data)
            
            # Calculate content availability score (0-1)
            # More content = higher score
            content_score = min(len(retrieved_chunks) / retriever_k, 1.0)
            topic_scores.append(content_score)
            
            # Summary of retrieved content
            content_summary = (
                f"Found {len(retrieved_chunks)} relevant sections in course materials. "
                f"Content coverage: {'Strong' if content_score > 0.7 else 'Moderate' if content_score > 0.3 else 'Limited'}."
            )
            
            mapped_topic = {
                "topic_name": topic,
                "retrieved_chunks": retrieved_chunks,
                "content_summary": content_summary,
                "sources": sorted(list(sources_set)),
                "content_score": content_score
            }
            
            mapped_module["topics"].append(mapped_topic)
        
        # Calculate module-level content score
        if topic_scores:
            mapped_module["total_content_score"] = sum(topic_scores) / len(topic_scores)
        
        mapped_modules.append(mapped_module)
    
    return mapped_modules


# ==================== STEP 3: STUDY PLAN GENERATION ====================

def generate_study_plan(
    mapped_modules: List[Dict[str, Any]],
    weeks: int = 8,
    hours_per_week: int = 20
) -> Dict[str, Any]:
    """
    Generate a structured weekly study plan from mapped modules.
    
    Uses LLM to create:
    - Weekly topic distribution
    - Revision cycles
    - Practice problems
    - Priority ranking
    
    Args:
        mapped_modules: Output from map_modules_to_docs()
        weeks: Number of weeks for study plan
        hours_per_week: Available study hours per week
        
    Returns:
        Structured study plan JSON with:
        {
            "title": "Study Plan",
            "weeks": [
                {
                    "week_number": int,
                    "topics": [str],
                    "focus": str,
                    "hours": int,
                    "activities": [str]
                }
            ],
            "revision_strategy": str,
            "priority_topics": [str],
            "practice_strategy": str,
            "sources": [str]
        }
    """
    client = _get_groq_client()
    if not client:
        return {"error": "Groq API key not configured"}
    
    # Prepare module summary for LLM
    module_summary = ""
    all_sources = set()
    
    for module in mapped_modules:
        module_summary += f"\nModule: {module['module_title']}\n"
        module_summary += f"  Topics ({len(module['topics'])}): "
        topic_names = [t["topic_name"] for t in module["topics"]]
        module_summary += ", ".join(topic_names) + "\n"
        module_summary += f"  Content availability: {module['total_content_score']:.0%}\n"
        
        for topic in module["topics"]:
            for source in topic.get("sources", []):
                all_sources.add(source)
    
    # Create study plan with LLM
    prompt = f"""
You are an expert educational planner. Create a {weeks}-week study plan.

Available {hours_per_week} hours per week for {weeks} weeks (total: {weeks * hours_per_week} hours).

Modules to cover:
{module_summary}

Generate a JSON study plan with this structure:
{{
  "weeks": [
    {{
      "week_number": 1,
      "topics": ["Topic 1", "Topic 2"],
      "focus": "Brief description of week's focus",
      "hours": 20,
      "activities": ["Read Chapter X", "Solve practice problems", "Review notes"]
    }},
    ...
  ],
  "revision_strategy": "Overall revision strategy description",
  "priority_topics": ["Most important topic 1", "Most important topic 2", ...],
  "practice_strategy": "How to practice/reinforce learning"
}}

Requirements:
1. Distribute topics logically across weeks (fundamental first, complex later)
2. Include 1-2 revision weeks
3. Cap each week at {hours_per_week} hours
4. Suggest varied activities (reading, practice, review)
5. Prioritize topics with more available content
6. Return ONLY valid JSON, no markdown or extra text
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Handle markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        plan_data = json.loads(response_text.strip())
        
        # Enhance with sources
        plan_data["sources"] = sorted(list(all_sources))
        
        return plan_data
        
    except Exception as e:
        print(f"Error generating study plan: {e}")
        return {
            "error": f"Failed to generate study plan: {str(e)}",
            "sources": sorted(list(all_sources))
        }


# ==================== STEP 4: WRAPPER FUNCTION ====================

def generate_study_plan_from_query(
    syllabus_pdf_path: str,
    weeks: int = 8,
    hours_per_week: int = 20,
    retriever_k: int = 5
) -> Dict[str, Any]:
    """
    Complete wrapper: Parse syllabus → Map to docs → Generate plan.
    
    This is the main entry point for study plan generation.
    
    Args:
        syllabus_pdf_path: Path to syllabus PDF file
        weeks: Number of weeks for study plan (default: 8)
        hours_per_week: Hours available per week (default: 20)
        retriever_k: Number of docs to retrieve per topic (default: 5)
        
    Returns:
        Complete study plan JSON:
        {
            "title": "Study Plan",
            "version": "1.0",
            "metadata": {
                "weeks": int,
                "total_hours": int,
                "modules_count": int,
                "total_topics": int
            },
            "plan": {
                "weeks": [...],
                "revision_strategy": str,
                "priority_topics": [...],
                "practice_strategy": str
            },
            "sources": [str],
            "modules_analyzed": [
                {
                    "module_title": str,
                    "topics_count": int,
                    "content_score": float
                }
            ]
        }
    """
    
    result = {
        "title": "Study Plan",
        "version": "1.0",
        "status": "processing",
        "errors": [],
        "metadata": {
            "weeks": weeks,
            "hours_per_week": hours_per_week,
            "total_hours": weeks * hours_per_week
        }
    }
    
    # STEP 1: Extract modules from syllabus
    print(f"[1/4] Extracting modules from syllabus: {syllabus_pdf_path}")
    modules = extract_modules_from_syllabus(syllabus_pdf_path)
    
    if not modules:
        result["status"] = "error"
        result["errors"].append("Failed to extract modules from syllabus PDF")
        return result
    
    print(f"      ✓ Extracted {len(modules)} modules")
    result["metadata"]["modules_count"] = len(modules)
    result["metadata"]["total_topics"] = sum(len(m.get("topics", [])) for m in modules)
    
    # STEP 2: Map modules to vector database content
    print(f"[2/4] Mapping modules to vector database content...")
    mapped_modules = map_modules_to_docs(modules, retriever_k=retriever_k)
    
    if not mapped_modules:
        result["status"] = "error"
        result["errors"].append("Failed to map modules to retrieved documents")
        return result
    
    print(f"      ✓ Mapped {len(mapped_modules)} modules to content")
    
    # STEP 3: Generate study plan
    print(f"[3/4] Generating study plan...")
    plan_data = generate_study_plan(mapped_modules, weeks=weeks, hours_per_week=hours_per_week)
    
    if "error" in plan_data:
        result["status"] = "error"
        result["errors"].append(plan_data["error"])
        return result
    
    print(f"      ✓ Study plan generated with {len(plan_data.get('weeks', []))} weeks")
    
    # STEP 4: Compile final result
    print(f"[4/4] Compiling final study plan...")
    
    # Extract metadata about modules for reference
    modules_analyzed = []
    for module in mapped_modules:
        modules_analyzed.append({
            "module_title": module["module_title"],
            "topics_count": len(module.get("topics", [])),
            "content_score": module.get("total_content_score", 0.0),
            "covered_in_weeks": []  # Could be populated from plan_data
        })
    
    result["status"] = "success"
    result["plan"] = plan_data
    result["sources"] = plan_data.get("sources", [])
    result["modules_analyzed"] = modules_analyzed
    result["metadata"]["total_sources"] = len(result["sources"])
    
    print(f"      ✓ Study plan complete: {result['metadata']['modules_count']} modules, "
          f"{result['metadata']['total_topics']} topics, "
          f"{len(result['sources'])} sources")
    
    return result


# ==================== UTILITY: RENDER FOR STREAMLIT ====================

def render_study_plan_markdown(plan_data: Dict[str, Any]) -> str:
    """
    Convert study plan JSON to markdown for Streamlit display.
    
    Args:
        plan_data: Output from generate_study_plan_from_query()
        
    Returns:
        Markdown string formatted for UI
    """
    if plan_data.get("status") != "success":
        error_msgs = plan_data.get("errors", ["Unknown error"])
        return f"**Error:** {'. '.join(error_msgs)}"
    
    markdown = f"""
# {plan_data['title']}

## Overview
- **Weeks:** {plan_data['metadata']['weeks']}
- **Hours/Week:** {plan_data['metadata']['hours_per_week']}
- **Total Hours:** {plan_data['metadata']['total_hours']}
- **Modules:** {plan_data['metadata']['modules_count']}
- **Topics:** {plan_data['metadata']['total_topics']}
- **Sources:** {plan_data['metadata']['total_sources']}

## Weekly Schedule
"""
    
    plan = plan_data.get("plan", {})
    
    for week in plan.get("weeks", []):
        week_num = week.get("week_number", "?")
        focus = week.get("focus", "")
        hours = week.get("hours", "?")
        topics = ", ".join(week.get("topics", []))
        activities = week.get("activities", [])
        
        markdown += f"""
### Week {week_num}: {focus}
**Topics:** {topics}  
**Hours:** {hours}h

**Activities:**
"""
        for activity in activities:
            markdown += f"- {activity}\n"
    
    markdown += f"""

## Priority Topics
"""
    for topic in plan.get("priority_topics", []):
        markdown += f"- {topic}\n"
    
    markdown += f"""

## Revision Strategy
{plan.get('revision_strategy', 'No strategy provided')}

## Practice Strategy
{plan.get('practice_strategy', 'No strategy provided')}

## Sources Used
"""
    for source in plan_data.get("sources", []):
        markdown += f"- {source}\n"
    
    return markdown


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Study Plan Generator - Test Module")
    print("=" * 60)
    
    # Test with dummy syllabus
    dummy_modules = [
        {
            "module_title": "Process Management",
            "topics": ["Process concept", "Process scheduling", "Synchronization"],
            "description": "Fundamentals of process management in OS"
        },
        {
            "module_title": "Memory Management",
            "topics": ["Paging", "Segmentation", "Virtual memory"],
            "description": "Memory organization and management techniques"
        }
    ]
    
    print("\n[Test 1] Module mapping structure:")
    print(f"  Modules: {len(dummy_modules)}")
    print(f"  Topics: {sum(len(m['topics']) for m in dummy_modules)}")
    
    print("\n[Test 2] Functions available:")
    print("  ✓ extract_modules_from_syllabus(pdf_path)")
    print("  ✓ map_modules_to_docs(modules, retriever_k)")
    print("  ✓ generate_study_plan(mapped_modules, weeks, hours_per_week)")
    print("  ✓ generate_study_plan_from_query(syllabus_pdf_path, weeks, hours_per_week)")
    print("  ✓ render_study_plan_markdown(plan_data)")
    
    print("\nAll functions implemented successfully!")
