# Test Files Structure - Internal Reference

## test_study_plan.py (337 lines)

### Module Organization

```python
# IMPORTS & SETUP (Lines 1-20)
├── System imports (sys, os, json, pathlib)
├── Project path setup
└── Agent imports (study_plan_generator functions)

# HELPER FUNCTIONS (Lines 22-60)
├── print_header(title)         # Formatted section header
├── print_section(title)        # Formatted subsection  
└── print_divider()             # Visual separator

# TEST FUNCTIONS (Lines 62-280)
├── test_find_syllabus_pdf()
│   ├── Searches sample_docs/
│   ├── Validates PDF exists
│   └── Returns pdf path
│
├── test_module_extraction(syllabus_pdf)
│   ├── Calls extract_modules_from_syllabus()
│   ├── Validates module count
│   ├── Prints each module
│   └── Returns modules list
│
├── test_module_to_docs_mapping(modules)
│   ├── Calls map_modules_to_docs()
│   ├── Displays priority scores
│   ├── Shows related documents
│   └── Returns mapped_modules dict
│
├── test_study_plan_generation(mapped_modules)
│   ├── Calls generate_study_plan()
│   ├── Verifies week count
│   ├── Displays week data
│   └── Returns study_plan dict
│
├── test_full_pipeline(syllabus_pdf)
│   ├── Calls generate_study_plan_from_query()
│   ├── Displays metadata
│   ├── Shows modules analyzed
│   └── Returns complete plan_data
│
└── print_summary(results)
    ├── Compiles test results
    ├── Displays pass/fail status
    └── Shows total score

# MAIN EXECUTION (Lines 282-337)
├── main()
│   ├── Initializes results dict
│   ├── Runs tests sequentially
│   ├── Prints summary
│   └── Returns success boolean
│
└── if __name__ == "__main__"
    ├── Calls main()
    └── Exits with code 0/1
```

### Test Flow Diagram

```
START
  ↓
[Test 1: Find PDF]
  ├─ Search sample_docs/
  ├─ Validate exists & readable
  └─ Extract path
  ↓
[Test 2: Extract Modules]
  ├─ Read PDF with PyPDF2
  ├─ Send to LLM (Groq)
  ├─ Parse response
  └─ Validate module count ≥ 3
  ↓
[Test 3: Module Mapping]
  ├─ For each module:
  │  ├─ Query ChromaDB
  │  ├─ Get 3-5 documents
  │  └─ Calculate priority
  └─ Return mapping dict
  ↓
[Test 4: Plan Generation]
  ├─ Input: mapped modules
  ├─ Call LLM for planning
  ├─ Structure by weeks
  └─ Validate week count
  ↓
[Test 5: Full Pipeline]
  ├─ Call wrapper function
  ├─ Get complete plan_data
  ├─ Extract metadata
  └─ Display results
  ↓
[Print Summary]
  ├─ Count passes
  ├─ Display results
  └─ Show 🎉 or ⚠️
  ↓
END (exit 0/1)
```

### Output Sections

```
1. Print Header
   └─ "STUDY PLAN GENERATOR TEST SUITE"

2. Step 1: Finding PDF
   ├─ Print header
   ├─ Search & validate
   ├─ Show file info
   └─ Print results

3. Step 2: Module Extraction
   ├─ Print header
   ├─ Call extraction
   ├─ Print each module
   └─ Print results

4. Step 3: Module Mapping
   ├─ Print header
   ├─ Map modules
   ├─ Print mapping details
   └─ Print results

5. Step 4: Study Plan
   ├─ Print header
   ├─ Generate plan
   ├─ Print plan structure
   └─ Print results

6. Step 5: Full Pipeline
   ├─ Print header
   ├─ Run complete pipeline
   ├─ Print metadata
   └─ Print results

7. Summary
   ├─ Print header
   ├─ Display test results
   ├─ Show scores
   └─ Print 🎉 or ⚠️
```

---

## test_summary.py (419 lines)

### Module Organization

```python
# IMPORTS & SETUP (Lines 1-20)
├── System imports (sys, os, json, typing)
├── Project path setup
└── Agent imports (summary_agent, retriever)

# HELPER FUNCTIONS (Lines 22-70)
├── print_header(title)         # Formatted section header
├── print_section(title)        # Formatted subsection
└── print_divider()             # Visual separator

# CORE TEST FUNCTIONS (Lines 72-320)
├── test_document_retrieval(query)
│   ├─ Retrieves docs from ChromaDB
│   ├─ Validates count ≥ 5
│   ├─ Displays doc metadata
│   └─ Returns success boolean
│
├── test_standard_summary()
│   ├─ Query: "Explain Deadlock in OS"
│   ├─ Call generate_summary(..., mode="standard")
│   ├─ Verify 6 sections present
│   ├─ Count bullets (8+)
│   ├─ Display sources
│   └─ Return pass/fail
│
├── test_revision_summary()
│   ├─ Call generate_summary(..., mode="revision")
│   ├─ Verify condensed format
│   ├─ Verify 5-point bullets
│   ├─ Check word count
│   ├─ Display sources
│   └─ Return pass/fail
│
├── test_detailed_summary()
│   ├─ Call generate_summary(..., mode="detailed")
│   ├─ Verify comprehensive format
│   ├─ Check word count (1000+)
│   ├─ Verify examples present
│   ├─ Display sources
│   └─ Return pass/fail
│
├── test_summary_modes_comparison()
│   ├─ Generate all 3 modes
│   ├─ Create comparison table
│   ├─ Compare metrics (chars, words, bullets, sources)
│   ├─ Verify hierarchy: revision < standard < detailed
│   └─ Return pass/fail
│
└── print_summary(results)
    ├─ Compile test results
    ├─ Display pass/fail
    └─ Show total score

# MAIN EXECUTION (Lines 360-419)
├── main()
│   ├─ Initialize results dict (5 tests)
│   ├─ Run tests sequentially
│   ├─ Print summary
│   └─ Return success boolean
│
└── if __name__ == "__main__"
    ├─ Calls main()
    └─ Exits with code 0/1
```

### Test Flow Diagram

```
START (Topic: "Explain Deadlock in OS")
  ↓
[Test 1: Document Retrieval]
  ├─ Query vector DB
  ├─ Get top 5 docs
  ├─ Verify metadata
  └─ Show doc list
  ↓
[Test 2: Standard Summary]
  ├─ Call generate_summary(mode="standard")
  ├─ Parse response
  ├─ Verify structure (6 sections)
  ├─ Count bullets (8+)
  ├─ Show citations
  └─ Validate pass
  ↓
[Test 3: Revision Summary]
  ├─ Call generate_summary(mode="revision")
  ├─ Verify condensed (< 400 words)
  ├─ Count bullets (5)
  ├─ Show citations
  └─ Validate pass
  ↓
[Test 4: Detailed Summary]
  ├─ Call generate_summary(mode="detailed")
  ├─ Verify comprehensive (1000+ words)
  ├─ Check for examples
  ├─ Show citations
  └─ Validate pass
  ↓
[Test 5: Modes Comparison]
  ├─ Create comparison table:
  │  ├─ Mode | Chars | Words | Bullets | Sources
  │  ├─ standard: x1 | x1 | x1 | x1
  │  ├─ revision: 0.6x | 0.6x | 0.6x | 0.7x
  │  └─ detailed: 1.6x | 3.6x | 1.5x | 1.3x
  ├─ Verify hierarchy
  └─ Validate pass
  ↓
[Print Summary]
  ├─ Count passes
  ├─ Display results
  └─ Show 🎉 or ⚠️
  ↓
END (exit 0/1)
```

### Output Sections

```
1. Print Header
   └─ "SUMMARY AGENT TEST SUITE"

2. Test 1: Document Retrieval
   ├─ Print header
   ├─ Show "Retrieving top 5 documents"
   ├─ Display each doc (source, type, page, preview)
   └─ Verify count ≥ 5

3. Test 2: Standard Summary
   ├─ Print header
   ├─ Generate summary
   ├─ Show full content
   ├─ Verify structure (6 sections)
   ├─ Count bullets
   ├─ Show sources
   └─ Print result

4. Test 3: Revision Summary
   ├─ Print header
   ├─ Generate summary
   ├─ Show content
   ├─ Verify condensed
   ├─ Show metrics
   ├─ Show sources
   └─ Print result

5. Test 4: Detailed Summary
   ├─ Print header
   ├─ Generate summary
   ├─ Show first 800 chars + preview of full length
   ├─ Verify comprehensive
   ├─ Check for examples
   ├─ Show sources
   └─ Print result

6. Test 5: Comparison
   ├─ Print header
   ├─ Show comparison table
   ├─ Verify hierarchy
   ├─ Display metrics
   └─ Print result

7. Summary
   ├─ Print header
   ├─ Display 5 test results
   ├─ Show scores (5/5)
   └─ Print 🎉 or ⚠️
```

---

## Key Differences Between Tests

### Study Plan Test
- **Input**: Real PDF file from filesystem
- **Processing**: Multi-step sequential pipeline
- **Output**: Structured study plan with weeks/topics
- **Verification**: Week count, topic assignment, hours
- **Tests**: 5 (including full pipeline)

### Summary Test
- **Input**: Text query from user
- **Processing**: 3 parallel modes tested
- **Output**: Summaries in 3 different formats
- **Verification**: Format validation, citations, length
- **Tests**: 5 (including comparison and retrieval)

---

## Code Quality Features

### Both Test Files Include

```python
# 1. Error Handling
try:
    result = function()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    return False

# 2. Comprehensive Logging
print(f"✓ Successfully extracted {len(modules)} modules:")

# 3. Result Tracking
results = {
    'test_1': False,
    'test_2': False,
}

# 4. Clear Output Formatting
print("="*80)
print(f"  {title}")
print("="*80)

# 5. Return Values
return success_boolean  # 0/1

# 6. Exit Codes
sys.exit(0 if success else 1)  # For CI/CD
```

---

## How Tests Are Structured

### Organizational Pattern

```python
# HEADER
"""Docstring with purpose"""

# IMPORTS
import sys, os

# HELPERS
def print_header():
    pass

# TESTS
def test_one():
    pass

def test_two():
    pass

# SUMMARY
def print_summary():
    pass

# MAIN
def main():
    pass

# EXECUTION
if __name__ == "__main__":
    pass
```

---

## Test Execution Sequence

### Study Plan Test Timeline

```
0s    - START
0-2s  - Find PDF
2-15s - Extract modules (LLM call)
15-20s- Map to docs (DB queries)
20-25s- Generate plan (LLM planning)
25-30s- Full pipeline
30-33s- Print summary
33s   - END ✓
```

### Summary Test Timeline

```
0s    - START
0-3s  - Retrieve documents
3-12s - Standard summary (LLM)
12-20s- Revision summary (LLM)  
20-28s- Detailed summary (LLM)
28-45s- Comparison & analysis
45-50s- Print summary
50s   - END ✓
```

---

## Expected Behavior Matrix

| Test | Condition | Response |
|------|-----------|----------|
| PDF not found | ❌ FAIL | Error message + exit |
| PDF found | ✅ PASS | Continue to extraction |
| Modules < 3 | ❌ FAIL | Exit, "No modules" |
| Modules ≥ 3 | ✅ PASS | Continue to mapping |
| Docs retrieved | ✅ PASS | Continue to plan |
| Docs not retrieved | ⚠️ WARN | Continue but warn |
| Plan generated | ✅ PASS | Validate structure |
| Wrong week count | ❌ FAIL | Display mismatch |

---

## Summary & Statistics

| Aspect | Study Plan | Summary |
|--------|-----------|---------|
| Lines | 337 | 419 |
| Test Functions | 6 | 6 |
| Helper Functions | 3 | 3 |
| API Calls | 1 Extract + 1 Generate | 3 Generate + 1 Retrieve |
| Outputs | 5 Steps | 5 Tests |
| Expected Pass % | 80%+ | 85%+ |

---

**Status**: Ready for Reference ✅
**Last Updated**: December 2024
