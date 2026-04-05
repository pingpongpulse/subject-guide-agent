"""
Test Study Plan Generator Agent
Tests module extraction, study plan generation, and week structure

Usage:
    python tests/test_study_plan.py

Requirements:
    - Syllabus PDF in sample_docs/ or provide path as argument
    - GROQ_API_KEY environment variable set
"""

import sys
import os
import json
from pathlib import Path
from pprint import pprint

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.study_plan_generator import (
    extract_modules_from_syllabus,
    map_modules_to_docs,
    generate_study_plan,
    generate_study_plan_from_query
)
from vectorstore.retriever import retrieve_docs


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_section(title):
    """Print formatted section"""
    print(f"\n{'─'*80}")
    print(f"  {title}")
    print(f"{'─'*80}")


def test_find_syllabus_pdf():
    """Find a syllabus PDF in sample_docs"""
    print_header("STEP 1: Finding Syllabus PDF")
    
    sample_docs = Path("sample_docs")
    if not sample_docs.exists():
        print(f"❌ sample_docs directory not found at {sample_docs.absolute()}")
        return None
    
    pdf_files = list(sample_docs.glob("*.pdf"))
    if not pdf_files:
        print(f"⚠️  No PDF files found in sample_docs/")
        print(f"   Available files: {list(sample_docs.glob('*'))}")
        return None
    
    syllabus_pdf = str(pdf_files[0])
    print(f"✓ Found PDF: {pdf_files[0].name}")
    print(f"  Path: {syllabus_pdf}")
    print(f"  Size: {os.path.getsize(syllabus_pdf) / 1024:.2f} KB")
    
    return syllabus_pdf


def test_module_extraction(syllabus_pdf):
    """Test module extraction from syllabus"""
    print_header("STEP 2: Module Extraction from Syllabus")
    
    if not syllabus_pdf:
        print("❌ No syllabus PDF provided")
        return None
    
    print(f"Extracting from: {os.path.basename(syllabus_pdf)}")
    print("Using LLM to identify modules...")
    
    try:
        modules = extract_modules_from_syllabus(syllabus_pdf)
        
        if not modules:
            print("❌ No modules extracted")
            return None
        
        print(f"\n✓ Successfully extracted {len(modules)} modules:")
        print_section("EXTRACTED MODULES")
        
        for i, module in enumerate(modules, 1):
            print(f"\n  {i}. {module}")
        
        print(f"\n✓ Module extraction successful!")
        return modules
        
    except Exception as e:
        print(f"❌ Error extracting modules: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_module_to_docs_mapping(modules):
    """Test mapping modules to vector store documents"""
    print_header("STEP 3: Module-to-Document Mapping")
    
    if not modules:
        print("❌ No modules provided")
        return None
    
    print(f"Mapping {len(modules)} modules to available documents...")
    print("Querying vector database...")
    
    try:
        mapped_modules = map_modules_to_docs(modules, retriever_k=3)
        
        print(f"\n✓ Successfully mapped modules to documents:")
        print_section("MAPPED MODULES")
        
        for i, (module, data) in enumerate(mapped_modules.items(), 1):
            print(f"\n  {i}. MODULE: {module}")
            print(f"     Priority Score: {data.get('priority_score', 'N/A'):.2f}")
            
            related_docs = data.get('related_docs', [])
            print(f"     Related Documents ({len(related_docs)}):")
            
            for j, doc in enumerate(related_docs[:3], 1):  # Show top 3
                source = doc.get('source_file', 'unknown')
                page = doc.get('page_number', '?')
                content_preview = doc.get('content', '')[:60]
                print(f"       {j}. {source} (Page {page})")
                print(f"          {content_preview}...")
        
        print(f"\n✓ Module mapping successful!")
        return mapped_modules
        
    except Exception as e:
        print(f"❌ Error mapping modules: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_study_plan_generation(mapped_modules):
    """Test study plan generation"""
    print_header("STEP 4: Study Plan Generation")
    
    if not mapped_modules:
        print("❌ No mapped modules provided")
        return None
    
    weeks = 4
    hours_per_week = 15
    
    print(f"Generating {weeks}-week study plan ({hours_per_week} hours/week)...")
    print(f"Total modules: {len(mapped_modules)}")
    
    try:
        study_plan = generate_study_plan(
            mapped_modules,
            weeks=weeks,
            hours_per_week=hours_per_week
        )
        
        if not study_plan or not isinstance(study_plan, dict):
            print("❌ Invalid study plan returned")
            return None
        
        print(f"\n✓ Study plan generated successfully!")
        print_section("STUDY PLAN STRUCTURE")
        
        # Verify weeks structure
        week_keys = sorted([k for k in study_plan.keys() if k.startswith('week_')])
        total_weeks = len(week_keys)
        
        print(f"\n  Total weeks: {total_weeks}")
        print(f"  Expected weeks: {weeks}")
        
        if total_weeks == weeks:
            print(f"  ✓ Week structure is correct!")
        else:
            print(f"  ⚠️  Week count mismatch!")
        
        # Display each week
        for week_key in week_keys[:3]:  # Show first 3 weeks
            week_data = study_plan[week_key]
            print(f"\n  {week_key.upper().replace('_', ' ')}:")
            
            if isinstance(week_data, dict):
                for key, value in week_data.items():
                    if key == "topics":
                        print(f"    • Topics ({len(value) if isinstance(value, list) else 'N/A'}):")
                        if isinstance(value, list):
                            for topic in value[:3]:
                                print(f"      - {topic}")
                    elif key == "hours":
                        print(f"    • Allocated Hours: {value}")
                    elif key == "focus_area":
                        print(f"    • Focus Area: {value}")
        
        if total_weeks > 3:
            print(f"\n  ... and {total_weeks - 3} more weeks")
        
        print(f"\n✓ Study plan generation successful!")
        return study_plan
        
    except Exception as e:
        print(f"❌ Error generating study plan: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_full_pipeline(syllabus_pdf):
    """Test complete study plan generation pipeline"""
    print_header("STEP 5: Full Pipeline Test")
    
    print(f"Running complete pipeline with: {os.path.basename(syllabus_pdf)}")
    print("Parameters:")
    print("  • Weeks: 3")
    print("  • Hours per week: 15")
    print("  • Retriever K: 5")
    
    try:
        plan_data = generate_study_plan_from_query(
            syllabus_pdf_path=syllabus_pdf,
            weeks=3,
            hours_per_week=15,
            retriever_k=5
        )
        
        print(f"\n✓ Full pipeline completed!")
        print_section("COMPLETE PLAN DATA")
        
        # Display key information
        print(f"\n  Metadata:")
        metadata = plan_data.get('metadata', {})
        for key, value in metadata.items():
            print(f"    • {key}: {value}")
        
        print(f"\n  Modules Analyzed: {len(plan_data.get('modules_analyzed', []))}")
        for module in plan_data.get('modules_analyzed', [])[:5]:
            print(f"    • {module}")
        
        print(f"\n  Sources Used: {len(plan_data.get('sources', []))}")
        for source in plan_data.get('sources', [])[:5]:
            print(f"    • {source}")
        
        print(f"\n  Plan Structure:")
        plan = plan_data.get('plan', {})
        week_keys = sorted([k for k in plan.keys() if k.startswith('week_')])
        print(f"    • Total weeks: {len(week_keys)}")
        
        if week_keys:
            print(f"\n  Sample Week ({week_keys[0]}):")
            sample_week = plan.get(week_keys[0], {})
            if isinstance(sample_week, dict):
                for key, value in list(sample_week.items())[:3]:
                    if isinstance(value, list):
                        print(f"    • {key}: {len(value)} items")
                    else:
                        print(f"    • {key}: {value}")
        
        return plan_data
        
    except Exception as e:
        print(f"❌ Error in full pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    checks = [
        ("Module extraction", results.get('modules_extracted', False)),
        ("Module mapping", results.get('modules_mapped', False)),
        ("Study plan generation", results.get('plan_generated', False)),
        ("Full pipeline", results.get('full_pipeline', False)),
    ]
    
    print("\n  Test Results:")
    passed = 0
    for check_name, passed_check in checks:
        status = "✓ PASS" if passed_check else "✗ FAIL"
        print(f"    {status} - {check_name}")
        if passed_check:
            passed += 1
    
    print(f"\n  Total: {passed}/{len(checks)} tests passed")
    
    if passed == len(checks):
        print("\n  🎉 All tests PASSED!")
        return True
    else:
        print(f"\n  ⚠️  {len(checks) - passed} test(s) FAILED")
        return False


def main():
    """Run all tests"""
    print_header("STUDY PLAN GENERATOR TEST SUITE")
    print("\nTesting module extraction, study plan generation, and week structure validation")
    
    results = {
        'modules_extracted': False,
        'modules_mapped': False,
        'plan_generated': False,
        'full_pipeline': False,
    }
    
    # Step 1: Find syllabus PDF
    syllabus_pdf = test_find_syllabus_pdf()
    if not syllabus_pdf:
        print("\n⚠️  Cannot proceed without syllabus PDF")
        print_summary(results)
        return False
    
    # Step 2: Extract modules
    modules = test_module_extraction(syllabus_pdf)
    if modules:
        results['modules_extracted'] = True
    else:
        print("\n⚠️  Cannot proceed without modules")
        print_summary(results)
        return False
    
    # Step 3: Map modules to documents
    mapped_modules = test_module_to_docs_mapping(modules)
    if mapped_modules:
        results['modules_mapped'] = True
    else:
        print("\n⚠️  Cannot proceed without mapped modules")
    
    # Step 4: Generate study plan
    study_plan = test_study_plan_generation(mapped_modules)
    if study_plan:
        results['plan_generated'] = True
    
    # Step 5: Full pipeline
    plan_data = test_full_pipeline(syllabus_pdf)
    if plan_data:
        results['full_pipeline'] = True
    
    # Print summary
    success = print_summary(results)
    
    print_header("END OF TEST")
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)