"""
Quick test of router integration with new agents
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.router import route_query

def test_topic_explanation():
    """Test existing agent still works"""
    print("\n" + "="*70)
    print("TEST 1: Topic Explanation (Existing Agent)")
    print("="*70)
    result = route_query("What is demand paging?", difficulty="intermediate")
    print(f"Agent: {result['agent']}")
    print(f"Category: {result['category']}")
    print(f"Status: {result['status']}")
    assert result['agent'] == "TopicExplainerAgent"
    assert result['status'] == "success"
    print("✓ PASSED")

def test_revision_without_format():
    """Test revision agent fallback"""
    print("\n" + "="*70)
    print("TEST 2: Revision Query (No Format Specified)")
    print("="*70)
    result = route_query("Give me revision notes on virtual memory")
    print(f"Agent: {result['agent']}")
    print(f"Category: {result['category']}")
    print(f"Status: {result['status']}")
    assert result['category'] == "revision"
    assert result['status'] == "success"
    print("✓ PASSED")

def test_revision_with_format():
    """Test revision routed to summary agent with format detection"""
    print("\n" + "="*70)
    print("TEST 3: Revision Query with Format (Should Use Summary Agent)")
    print("="*70)
    result = route_query("Quick summary of deadlocks")
    print(f"Agent: {result['agent']}")
    print(f"Category: {result['category']}")
    print(f"Status: {result['status']}")
    if 'mode' in result:
        print(f"Mode: {result['mode']}")
    assert result['category'] == "revision"
    assert result['status'] == "success"
    print("✓ PASSED")

def test_study_plan_without_path():
    """Test study plan generation without PDF path"""
    print("\n" + "="*70)
    print("TEST 4: Study Plan Query (Without PDF Path)")
    print("="*70)
    result = route_query("Generate a 2-week study plan with 10 hours per week")
    print(f"Agent: {result['agent']}")
    print(f"Category: {result['category']}")
    print(f"Status: {result['status']}")
    print(f"Error: {result['error']}")
    assert result['category'] == "study_plan"
    assert result['status'] == "error"  # Should error without PDF path
    print("✓ PASSED (error as expected - no PDF provided)")

def test_parameter_extraction():
    """Test parameter detection from queries"""
    print("\n" + "="*70)
    print("TEST 5: Parameter Extraction")
    print("="*70)
    from agents.router import _extract_study_plan_params
    
    # Test weeks extraction
    result = _extract_study_plan_params("Generate a 2-week study plan")
    print(f"Query: 'Generate a 2-week study plan'")
    print(f"Extracted: weeks={result['weeks']}, hours_per_week={result['hours_per_week']}")
    assert result['weeks'] == 2
    print("✓ PASSED")
    
    # Test hours extraction
    result = _extract_study_plan_params("with only 30 hours total")
    print(f"Query: 'with only 30 hours total'")
    print(f"Extracted: weeks={result['weeks']}, hours_per_week={result['hours_per_week']}")
    assert result['hours_per_week'] == 30
    print("✓ PASSED")

def test_summary_mode_detection():
    """Test summary mode detection"""
    print("\n" + "="*70)
    print("TEST 6: Summary Mode Detection")
    print("="*70)
    from agents.router import _detect_summary_format
    
    # Test revision mode
    mode = _detect_summary_format("Quick summary of virtual memory")
    print(f"Query: 'Quick summary of virtual memory'")
    print(f"Detected mode: {mode}")
    assert mode == "revision"
    print("✓ PASSED")
    
    # Test detailed mode
    mode = _detect_summary_format("Detailed summary of deadlocks")
    print(f"Query: 'Detailed summary of deadlocks'")
    print(f"Detected mode: {mode}")
    assert mode == "detailed"
    print("✓ PASSED")
    
    # Test standard mode
    mode = _detect_summary_format("Summarize process scheduling")
    print(f"Query: 'Summarize process scheduling'")
    print(f"Detected mode: {mode}")
    assert mode == "standard"
    print("✓ PASSED")

if __name__ == "__main__":
    try:
        test_topic_explanation()
        test_revision_without_format()
        test_revision_with_format()
        test_parameter_extraction()
        test_summary_mode_detection()
        
        # Note: test_study_plan_without_path would need actual retriever/LLM setup
        print("\n" + "="*70)
        print("✓ ALL UNIT TESTS PASSED!")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
