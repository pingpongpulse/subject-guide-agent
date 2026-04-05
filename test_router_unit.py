"""
Simpler router unit tests - checking helper functions and parameter extraction
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parameter_extraction():
    """Test parameter detection from queries"""
    print("\n" + "="*70)
    print("TEST 1: Parameter Extraction")
    print("="*70)
    from agents.router import _extract_study_plan_params
    
    # Test weeks extraction
    result = _extract_study_plan_params("Generate a 2-week study plan")
    print(f"Query: 'Generate a 2-week study plan'")
    print(f"Extracted: weeks={result['weeks']}, hours_per_week={result['hours_per_week']}")
    assert result['weeks'] == 2, f"Expected weeks=2, got {result['weeks']}"
    print("✓ PASSED")
    
    # Test hours extraction
    result = _extract_study_plan_params("with 30 hours per week")
    print(f"Query: 'with 30 hours per week'")
    print(f"Extracted: weeks={result['weeks']}, hours_per_week={result['hours_per_week']}")
    assert result['hours_per_week'] == 30, f"Expected hours=30, got {result['hours_per_week']}"
    print("✓ PASSED")
    
    # Test default values
    result = _extract_study_plan_params("just generate a plan")
    print(f"Query: 'just generate a plan'")
    print(f"Extracted: weeks={result['weeks']}, hours_per_week={result['hours_per_week']}")
    assert result['weeks'] == 8, f"Expected default weeks=8, got {result['weeks']}"
    assert result['hours_per_week'] == 20, f"Expected default hours=20, got {result['hours_per_week']}"
    print("✓ PASSED")

def test_summary_mode_detection():
    """Test summary mode detection"""
    print("\n" + "="*70)
    print("TEST 2: Summary Mode Detection")
    print("="*70)
    from agents.router import _detect_summary_format
    
    # Test revision mode
    mode = _detect_summary_format("Quick summary of virtual memory")
    print(f"Query: 'Quick summary of virtual memory'")
    print(f"Detected mode: {mode}")
    assert mode == "revision", f"Expected mode='revision', got '{mode}'"
    print("✓ PASSED")
    
    # Test detailed mode
    mode = _detect_summary_format("Detailed summary of deadlocks")
    print(f"Query: 'Detailed summary of deadlocks'")
    print(f"Detected mode: {mode}")
    assert mode == "detailed", f"Expected mode='detailed', got '{mode}'"
    print("✓ PASSED")
    
    # Test standard mode
    mode = _detect_summary_format("Summarize process scheduling")
    print(f"Query: 'Summarize process scheduling'")
    print(f"Detected mode: {mode}")
    assert mode == "standard", f"Expected mode='standard', got '{mode}'"
    print("✓ PASSED")
    
    # Test lightning -> revision mapping
    mode = _detect_summary_format("Lightning notes on file systems")
    print(f"Query: 'Lightning notes on file systems'")
    print(f"Detected mode: {mode}")
    assert mode == "revision", f"Expected lightning to map to 'revision', got '{mode}'"
    print("✓ PASSED")
    
    # Test no format
    mode = _detect_summary_format("Tell me about caching")
    print(f"Query: 'Tell me about caching'")
    print(f"Detected mode: {mode}")
    assert mode is None, f"Expected mode=None, got '{mode}'"
    print("✓ PASSED")

def test_router_initialization():
    """Test that router module can be imported successfully"""
    print("\n" + "="*70)
    print("TEST 3: Router Module Initialization")
    print("="*70)
    try:
        # Try to import critical components
        from agents.router import route_query, _extract_study_plan_params, _detect_summary_format
        print("✓ Successfully imported route_query")
        print("✓ Successfully imported _extract_study_plan_params")
        print("✓ Successfully imported _detect_summary_format")
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        raise

if __name__ == "__main__":
    try:
        test_parameter_extraction()
        test_summary_mode_detection()
        test_router_initialization()
        
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
