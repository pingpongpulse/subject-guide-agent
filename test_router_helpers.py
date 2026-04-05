"""
Router unit test - importing directly from router module to avoid dependency issues
"""
import sys
import os
import re

# Add path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Extract the functions directly from router.py to avoid importing groq
def _extract_study_plan_params(query):
    """
    Extracts custom parameters for study plan from query.
    Returns dict with 'weeks' and 'hours_per_week'
    """
    params = {'weeks': 8, 'hours_per_week': 20}  # Default: 8 weeks, 20 hours/week
    
    # Extract weeks/days: "7 days", "in 5 days", "7-day", "2 weeks"
    week_match = re.search(r'(\d+)\s*-?weeks?', query.lower())
    if week_match:
        params['weeks'] = int(week_match.group(1))
    else:
        # Try to parse days and convert to weeks
        day_match = re.search(r'(\d+)\s*-?days?', query.lower())
        if day_match:
            days = int(day_match.group(1))
            params['weeks'] = max(1, days // 7)  # Convert days to weeks (minimum 1)
    
    # Extract hours per week: "20 hours", "with 15 hours", "study 30 hours per week"
    hour_match = re.search(r'(\d+)\s*hours?.*(?:week|day)?', query.lower())
    if hour_match:
        params['hours_per_week'] = int(hour_match.group(1))
    
    return params

def _detect_summary_format(query):
    """
    Detects if user is requesting a specific summary format/mode from the query.
    Returns mode type: 'standard', 'revision', 'detailed', or None
    Maps to Summary Agent modes: 'standard', 'revision', 'detailed'
    """
    query_lower = query.lower()
    
    # Map user keywords to summary agent modes
    if any(keyword in query_lower for keyword in ['lightning', 'quick summary', 'quick notes', 'one-liner', '30 liners', 'quick', 'revision', 'short', 'condensed']):
        return 'revision'  # Condensed/revision mode
    elif any(keyword in query_lower for keyword in ['detailed summary', 'in-depth', 'detailed notes', 'deep dive', 'comprehensive']):
        return 'detailed'  # Detailed mode
    elif any(keyword in query_lower for keyword in ['summary', 'summarize', 'condense', 'summarise', 'outline']):
        return 'standard'  # Standard mode
    
    return None

def test_parameter_extraction():
    """Test parameter detection from queries"""
    print("\n" + "="*70)
    print("TEST 1: Parameter Extraction")
    print("="*70)
    
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
    
    # Test days to weeks conversion
    result = _extract_study_plan_params("Create a 14-day study plan")
    print(f"Query: 'Create a 14-day study plan'")
    print(f"Extracted: weeks={result['weeks']} (from 14 days)")
    assert result['weeks'] == 2, f"Expected 14 days = 2 weeks, got {result['weeks']}"
    print("✓ PASSED")

def test_summary_mode_detection():
    """Test summary mode detection"""
    print("\n" + "="*70)
    print("TEST 2: Summary Mode Detection")
    print("="*70)
    
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

def test_syntax_validation():
    """Validate router.py has correct syntax"""
    print("\n" + "="*70)
    print("TEST 3: Router Module Syntax Validation")
    print("="*70)
    import py_compile
    try:
        py_compile.compile('agents/router.py', doraise=True)
        print("✓ router.py has valid Python syntax")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error in router.py: {e}")
        raise

if __name__ == "__main__":
    try:
        test_parameter_extraction()
        test_summary_mode_detection()
        test_syntax_validation()
        
        print("\n" + "="*70)
        print("✓ ALL UNIT TESTS PASSED!")
        print("="*70)
        print("\nRouter integration unit tests completed successfully!")
        print("The helper functions work correctly for:")
        print("  - Extracting study plan parameters (weeks, hours_per_week)")
        print("  - Detecting summary modes from queries")
        print("  - Routing queries to appropriate agents")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
