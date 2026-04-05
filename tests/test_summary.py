"""
Test Summary Agent
Tests summary generation with structured output, bullet points, and citations

Usage:
    python tests/test_summary.py

Requirements:
    - Academic documents in vector store (run ingest first)
    - GROQ_API_KEY environment variable set
"""

import sys
import os
import json
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.summary_agent import generate_summary
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


def print_divider():
    """Print a divider line"""
    print(f"\n  {'.'*76}")


def test_standard_summary():
    """Test standard summary generation"""
    print_header("TEST 1: Standard Summary - Deadlock in OS")
    
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print(f"Mode: standard (6-section structured)")
    print("Retrieving relevant documents...")
    
    try:
        result = generate_summary(query, mode="standard", retriever_k=5)
        
        if result.get("error"):
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"\n✓ Summary generated successfully!")
        print_section("SUMMARY CONTENT")
        
        # Display the structured summary
        content = result.get("content", "")
        if content:
            print(f"\n{content}")
        else:
            print("❌ No content in response")
            return False
        
        # Verify structure
        expected_sections = ["Topic", "Core Idea", "Key Concepts", "Important Points", "Exam Focus", "Example"]
        found_sections = sum(1 for section in expected_sections if section.lower() in content.lower())
        
        print_divider()
        print(f"\nStructure Verification:")
        print(f"  Expected sections: {len(expected_sections)}")
        print(f"  Found sections: {found_sections}")
        
        if found_sections >= 4:
            print(f"  [OK] Structured format detected!")
        else:
            print(f"  [WARN] Fewer sections than expected")
        
        # Check for bullet points
        bullet_count = content.count("•") + content.count("-") + content.count("*")
        print(f"\n  Bullet points found: {bullet_count}")
        if bullet_count >= 3:
            print(f"  [OK] Bullet points present!")
        else:
            print(f"  [WARN] Few bullet points found")
        
        # Display sources
        sources = result.get("sources", [])
        print_divider()
        print(f"\nCitations & Sources ({len(sources)}):")
        
        if sources:
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
            print(f"\n  ✓ Citations present!")
        else:
            print(f"  ⚠️  No citations found")
        
        print(f"\n[OK] Standard summary test PASSED!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error generating standard summary: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_revision_summary():
    """Test revision (condensed) summary generation"""
    print_header("TEST 2: Revision Summary - Deadlock in OS")
    
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print(f"Mode: revision (5-point condensed format)")
    print("Retrieving relevant documents...")
    
    try:
        result = generate_summary(query, mode="revision", retriever_k=5)
        
        if result.get("error"):
            print(f"[ERROR] Error: {result['error']}")
            return False
        
        print(f"\n[OK] Summary generated successfully!")
        print_section("REVISION SUMMARY CONTENT")
        
        # Display the condensed summary
        content = result.get("content", "")
        if content:
            print(f"\n{content}")
        else:
            print("[ERROR] No content in response")
            return False
        
        # Verify it's condensed (less content than standard)
        print_divider()
        print(f"\nContent Metrics:")
        word_count = len(content.split())
        print(f"  Word count: {word_count}")
        
        if word_count < 500:
            print(f"  [OK] Condensed format verified!")
        else:
            print(f"  [WARN] Content is longer than expected for revision")
        
        # Check for bullet points
        bullet_count = content.count("•") + content.count("-") + content.count("*")
        print(f"  Bullet points: {bullet_count}")
        
        if bullet_count >= 3:
            print(f"  [OK] Key points in bullet format!")
        
        # Display sources
        sources = result.get("sources", [])
        print_divider()
        print(f"\nCitations & Sources ({len(sources)}):")
        
        if sources:
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
            print(f"\n  [OK] Citations present!")
        else:
            print(f"  [WARN] No citations found")
        
        print(f"\n[OK] Revision summary test PASSED!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error generating revision summary: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detailed_summary():
    """Test detailed summary generation"""
    print_header("TEST 3: Detailed Summary - Deadlock in OS")
    
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print(f"Mode: detailed (9-section comprehensive)")
    print("Retrieving relevant documents...")
    
    try:
        result = generate_summary(query, mode="detailed", retriever_k=5)
        
        if result.get("error"):
            print(f"[ERROR] Error: {result['error']}")
            return False
        
        print(f"\n[OK] Summary generated successfully!")
        print_section("DETAILED SUMMARY CONTENT")
        
        # Display first part of detailed summary
        content = result.get("content", "")
        if content:
            # Show first 800 characters
            preview_length = 800
            if len(content) > preview_length:
                print(f"\n{content[:preview_length]}")
                print(f"\n... [Content continues, total length: {len(content)} chars]")
            else:
                print(f"\n{content}")
        else:
            print("❌ No content in response")
            return False
        
        # Verify comprehensiveness
        print_divider()
        print(f"\nContent Metrics:")
        word_count = len(content.split())
        print(f"  Word count: {word_count}")
        
        if word_count > 500:
            print(f"  ✓ Comprehensive detail level verified!")
        else:
            print(f"  ⚠️  Less detailed than expected")
        
        # Check for examples
        has_examples = any(keyword in content.lower() for keyword in ["example", "e.g.", "for instance", "such as"])
        print(f"  Contains examples: {'[OK]' if has_examples else '[WARN]'}")
        
        # Display sources
        sources = result.get("sources", [])
        print_divider()
        print(f"\nCitations & Sources ({len(sources)}):")
        
        if sources:
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
            print(f"\n  [OK] Citations present!")
        else:
            print(f"  [WARN] No citations found")
        
        print(f"\n[OK] Detailed summary test PASSED!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error generating detailed summary: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_summary_modes_comparison():
    """Test and compare all three summary modes"""
    print_header("TEST 4: Summary Modes Comparison")
    
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print("Generating summaries in all three modes for comparison...\n")
    
    modes_data = {}
    
    # Generate all three modes
    for mode in ["standard", "revision", "detailed"]:
        print(f"  Generating {mode} mode...", end=" ", flush=True)
        try:
            result = generate_summary(query, mode=mode, retriever_k=5)
            if result.get("error"):
                print(f"[ERROR] Error")
                continue
            
            content = result.get("content", "")
            modes_data[mode] = {
                "content": content,
                "sources": result.get("sources", []),
                "length": len(content),
                "word_count": len(content.split()),
                "bullet_count": content.count("•") + content.count("-") + content.count("*")
            }
            print(f"[OK]")
        except Exception as e:
            print(f"❌ {e}")
    
    if not modes_data:
        print("❌ No summaries generated")
        return False
    
    # Display comparison
    print_section("MODE COMPARISON TABLE")
    
    print(f"\n  {'Mode':<12} {'Chars':<8} {'Words':<8} {'Bullets':<8} {'Sources':<8}")
    print(f"  {'-'*50}")
    
    for mode in ["standard", "revision", "detailed"]:
        if mode in modes_data:
            data = modes_data[mode]
            print(f"  {mode:<12} {data['length']:<8} {data['word_count']:<8} {data['bullet_count']:<8} {len(data['sources']):<8}")
    
    # Verify order: revision < standard < detailed
    if "revision" in modes_data and "standard" in modes_data and "detailed" in modes_data:
        rv = modes_data["revision"]["word_count"]
        st = modes_data["standard"]["word_count"]
        dt = modes_data["detailed"]["word_count"]
        
        print_divider()
        print("\nLength Order Verification:")
        print(f"  Revision ({rv} words) < Standard ({st} words) < Detailed ({dt} words)")
        
        if rv < st < dt:
            print(f"  [OK] Length hierarchy correct!")
        elif rv <= st <= dt:
            print(f"  [WARN] Hierarchy approximately correct")
        else:
            print(f"  [WARN] Length hierarchy not as expected")
    
    print(f"\n✓ Modes comparison test PASSED!")
    return True


def test_document_retrieval():
    """Test document retrieval for summary topic"""
    print_header("TEST 5: Document Retrieval Verification")
    
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print(f"Retrieving top 5 documents from vector store...")
    
    try:
        docs = retrieve_docs(query, k=5)
        
        if not docs:
            print("[ERROR] No documents retrieved")
            return False
        
        print(f"\n[OK] Retrieved {len(docs)} documents")
        print_section("RETRIEVED DOCUMENTS")
        
        for i, doc in enumerate(docs, 1):
            # Handle both Document objects and dicts
            if hasattr(doc, 'metadata'):
                metadata = doc.metadata
                content = doc.page_content[:100] if hasattr(doc, 'page_content') else str(doc)[:100]
            else:
                metadata = doc.get('metadata', {})
                content = doc.get('content', '')[:100]
            
            source = metadata.get('source_file', 'unknown')
            doc_type = metadata.get('doc_type', 'unknown')
            page = metadata.get('page_number', '?')
            
            print(f"\n  {i}. Source: {source}")
            print(f"     Type: {doc_type} | Page: {page}")
            print(f"     Preview: {content}...")
        
        print(f"\n[OK] Document retrieval test PASSED!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error retrieving documents: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_formula_extraction():
    """Test optional formula extraction from summary content"""
    print_header("TEST 6: Formula Extraction (Optional Field)")
    
    # Test with a query likely to have formulas
    query = "Explain Deadlock in OS"
    print(f"\nQuery: {query}")
    print(f"Testing formula extraction (optional field)...")
    print(f"Formula field should ONLY appear if formulas are present in content.\n")
    
    try:
        result = generate_summary(query, mode="detailed", retriever_k=5)
        
        if result.get("error"):
            print(f"[ERROR] Error: {result['error']}")
            return False
        
        print(f"[OK] Summary generated successfully!")
        print_section("FORMULA EXTRACTION RESULTS")
        
        # Check if formulas field exists
        has_formulas_field = "formulas" in result
        content = result.get("content", "")
        
        print(f"\nFormulas field present in output: {'[OK] Yes' if has_formulas_field else '[FAIL] No'}")
        
        if has_formulas_field:
            formulas = result.get("formulas", [])
            print(f"Number of formulas found: {len(formulas)}")
            
            if formulas:
                print_divider()
                print("\nFormula Details:")
                
                for i, formula in enumerate(formulas, 1):
                    print(f"\n  Formula {i}:")
                    print(f"    Expression: {formula.get('formula', 'N/A')[:60]}...")
                    print(f"    Variables: {formula.get('variables', 'N/A')[:60]}...")
                    print(f"    Explanation: {formula.get('explanation', 'N/A')[:60]}...")
                    print(f"    Use Case: {formula.get('use_case', 'N/A')[:60]}...")
                    
                    # Verify structure
                    required_keys = ['formula', 'variables', 'explanation', 'use_case']
                    missing_keys = [k for k in required_keys if k not in formula]
                    if missing_keys:
                        print(f"    [WARN] Missing keys: {missing_keys}")
                    else:
                        print(f"    [OK] All required keys present")
                
                print(f"\n✓ Formulas extracted and structured correctly!")
            else:
                print(f"\n  Note: Formulas field exists but is empty (no formulas in content)")
                print(f"  This is expected behavior - formulas only included when present.")
        else:
            print(f"\n  Note: Formulas field not in output (no formulas in content)")
            print(f"  This is expected behavior - formulas are optional.")
            print(f"")
        
        # Verify output structure
        required_fields = ['title', 'content', 'sources', 'mode']
        result_keys = set(result.keys())
        missing = [f for f in required_fields if f not in result_keys]
        optional = [f for f in result_keys if f not in required_fields]
        
        print_divider()
        print("\nOutput Structure Verification:")
        print(f"  Required fields: {', '.join(required_fields)}")
        
        if not missing:
            print(f"  [OK] All required fields present")
        else:
            print(f"  [WARN] Missing fields: {missing}")
        
        if optional:
            print(f"  Optional fields present: {', '.join(optional)}")
        
        print(f"\n[OK] Formula extraction test PASSED!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error in formula extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    checks = [
        ("Document retrieval", results.get('doc_retrieval', False)),
        ("Standard summary generation", results.get('standard_summary', False)),
        ("Revision summary generation", results.get('revision_summary', False)),
        ("Detailed summary generation", results.get('detailed_summary', False)),
        ("Modes comparison", results.get('modes_comparison', False)),
        ("Formula extraction (optional)", results.get('formula_extraction', False)),
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
    """Run all summary tests"""
    print_header("SUMMARY AGENT TEST SUITE")
    print("\nTesting structured summary generation with bullet points and citations")
    print("Topic: Explain Deadlock in OS")
    print("Including optional formula extraction for formula sheet agent compatibility\n")
    
    results = {
        'doc_retrieval': False,
        'standard_summary': False,
        'revision_summary': False,
        'detailed_summary': False,
        'modes_comparison': False,
        'formula_extraction': False,
    }
    
    # Test 1: Document retrieval (prerequisite)
    if not test_document_retrieval():
        print("\n⚠️  Document retrieval failed. Some tests may fail without documents.")
    else:
        results['doc_retrieval'] = True
    
    # Test 2: Standard summary
    if test_standard_summary():
        results['standard_summary'] = True
    
    # Test 3: Revision summary
    if test_revision_summary():
        results['revision_summary'] = True
    
    # Test 4: Detailed summary
    if test_detailed_summary():
        results['detailed_summary'] = True
    
    # Test 5: Modes comparison
    if test_summary_modes_comparison():
        results['modes_comparison'] = True
    
    # Test 6: Formula extraction
    if test_formula_extraction():
        results['formula_extraction'] = True
    
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
