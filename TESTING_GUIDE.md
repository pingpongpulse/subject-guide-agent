# Test Suites Documentation

## Overview

Two comprehensive test suites have been created for the newly integrated agents:

1. **`tests/test_study_plan.py`** - Tests Study Plan Generator Agent
2. **`tests/test_summary.py`** - Tests Summary Agent

Both test files stress-test the agents with real-world scenarios and provide detailed output for manual verification.

---

## Test Study Plan (`tests/test_study_plan.py`)

### Purpose
Tests the complete Study Plan Generator pipeline including module extraction, mapping to documents, and plan generation.

### Test Coverage

| Test | What It Tests | Verifies |
|------|---------------|----------|
| STEP 1: Finding Syllabus PDF | Document discovery | PDF exists and is readable |
| STEP 2: Module Extraction | Syllabus parsing | Modules are extracted from PDF |
| STEP 3: Module-to-Document Mapping | Vector DB retrieval | Modules map to retrieved documents |
| STEP 4: Study Plan Generation | Plan structure | Weeks are properly structured |
| STEP 5: Full Pipeline | End-to-end execution | Complete plan with metadata |

### Running the Test

```bash
cd subject-guide-agent
python tests/test_study_plan.py
```

### Expected Output Structure

```
================================================================================
  STUDY PLAN GENERATOR TEST SUITE
================================================================================

================================================================================
  STEP 1: Finding Syllabus PDF
================================================================================
✓ Found PDF: syllabus.pdf
  Path: sample_docs/syllabus.pdf
  Size: 245.32 KB

────────────────────────────────────────────────────────────────────────────────
  EXTRACTED MODULES
────────────────────────────────────────────────────────────────────────────────

  1. Process Scheduling
  2. Memory Management
  3. File Systems
  4. Synchronization
  5. Deadlock

✓ Module extraction successful!

────────────────────────────────────────────────────────────────────────────────
  MAPPED MODULES
────────────────────────────────────────────────────────────────────────────────

  1. MODULE: Process Scheduling
     Priority Score: 0.85
     Related Documents (3):
       1. os_notes.pdf (Page 5)
          Discusses CPU scheduling algorithms...
       2. textbook.pdf (Page 42)
          Process scheduling in modern OS...

  ...

✓ Module mapping successful!

────────────────────────────────────────────────────────────────────────────────
  STUDY PLAN STRUCTURE
────────────────────────────────────────────────────────────────────────────────

  Total weeks: 4
  Expected weeks: 4
  ✓ Week structure is correct!

  WEEK 1:
    • Topics (3):
      - Process Scheduling
      - CPU Scheduling Algorithms
      - Context Switching
    • Allocated Hours: 15
    • Focus Area: Fundamentals

  WEEK 2:
    ...

  ... and 2 more weeks

✓ Study plan generation successful!

================================================================================
  TEST SUMMARY
================================================================================

  Test Results:
    ✓ PASS - Module extraction
    ✓ PASS - Module mapping
    ✓ PASS - Study plan generation
    ✓ PASS - Full pipeline

  Total: 4/4 tests passed

  🎉 All tests PASSED!

================================================================================
  END OF TEST
================================================================================
```

### What to Verify Manually

1. **Module Extraction**
   - ✓ At least 5 modules extracted
   - ✓ Module names are relevant to the PDF
   - ✓ No empty or duplicate modules

2. **Module Mapping**
   - ✓ Each module has priority score 0.0-1.0
   - ✓ Each module has related documents
   - ✓ Documents have source file and page numbers

3. **Study Plan Structure**
   - ✓ Correct number of weeks generated (matching requested weeks)
   - ✓ Each week has topics, hours, and focus area
   - ✓ Topics align with extracted modules

4. **Metadata**
   - ✓ Modules analyzed count matches extracted count
   - ✓ Sources list includes document references
   - ✓ Plan data is properly nested and typed

---

## Test Summary (`tests/test_summary.py`)

### Purpose
Tests the Summary Agent's ability to generate structured summaries in different modes with citations.

### Test Coverage

| Test | What It Tests | Verifies |
|------|---------------|----------|
| TEST 1: Standard Summary | 6-section structured format | Sections present, bullets exist |
| TEST 2: Revision Summary | 5-point condensed format | Condensed length, key points |
| TEST 3: Detailed Summary | 9-section comprehensive format | Detailed length, examples included |
| TEST 4: Modes Comparison | All three modes together | Length hierarchy correct |
| TEST 5: Document Retrieval | Vector DB functionality | Documents retrieved successfully |

### Running the Test

```bash
cd subject-guide-agent
python tests/test_summary.py
```

### Expected Output Structure

```
================================================================================
  SUMMARY AGENT TEST SUITE
================================================================================

================================================================================
  TEST 1: Standard Summary - Deadlock in OS
================================================================================

Query: Explain Deadlock in OS
Mode: standard (6-section structured)
Retrieving relevant documents...

✓ Summary generated successfully!

────────────────────────────────────────────────────────────────────────────────
  SUMMARY CONTENT
────────────────────────────────────────────────────────────────────────────────

TOPIC: Deadlock in Operating Systems

CORE IDEA:
A deadlock is a situation where a set of processes are blocked because each 
process is holding a resource and waiting for a resource held by another process...

KEY CONCEPTS:
• Resource allocation
• Circular wait
• Mutual exclusion
• Hold and wait condition

IMPORTANT POINTS:
• Deadlocks require four conditions to occur simultaneously
• Prevention strategies involve breaking one or more conditions
• Detection algorithms can identify deadlock cycles

EXAM FOCUS:
Students should understand the four necessary conditions for deadlock and be able 
to identify deadlock scenarios in pseudocode.

EXAMPLE:
Two processes: Process A holds Resource 1 and waits for Resource 2.
Process B holds Resource 2 and waits for Resource 1. This creates circular wait.

  ·────────────────────────────────────────────────────────────────────────────

Structure Verification:
  Expected sections: 6
  Found sections: 6
  ✓ Structured format detected!

  Bullet points found: 8
  ✓ Bullet points present!

  ·────────────────────────────────────────────────────────────────────────────

Citations & Sources (3):
  1. os_notes.pdf Page 12
  2. textbook.pdf Page 178
  3. lecture_slides.pdf Page 45

  ✓ Citations present!

✓ Standard summary test PASSED!

================================================================================
  TEST 2: Revision Summary - Deadlock in OS
================================================================================

Query: Explain Deadlock in OS
Mode: revision (5-point condensed format)
Retrieving relevant documents...

✓ Summary generated successfully!

────────────────────────────────────────────────────────────────────────────────
  REVISION SUMMARY CONTENT
────────────────────────────────────────────────────────────────────────────────

DEADLOCK: Quick Revision Points

• Definition: Situation where processes are blocked in circular wait for resources
• Four Conditions: Mutual exclusion, hold & wait, no preemption, circular wait
• Prevention: Break one of the four conditions (most common: preemption)
• Detection: Use resource allocation graph or deadlock detection algorithms
• Recovery: Process termination or resource preemption

  ·────────────────────────────────────────────────────────────────────────────

Content Metrics:
  Word count: 340
  ✓ Condensed format verified!
  Bullet points: 5
  ✓ Key points in bullet format!

  ·────────────────────────────────────────────────────────────────────────────

Citations & Sources (2):
  1. os_notes.pdf Page 12
  2. textbook.pdf Page 178

  ✓ Citations present!

✓ Revision summary test PASSED!

================================================================================
  TEST 3: Detailed Summary - Deadlock in OS
================================================================================

Query: Explain Deadlock in OS
Mode: detailed (9-section comprehensive)
Retrieving relevant documents...

✓ Summary generated successfully!

────────────────────────────────────────────────────────────────────────────────
  DETAILED SUMMARY CONTENT
────────────────────────────────────────────────────────────────────────────────

DEADLOCK IN OPERATING SYSTEMS: Comprehensive Analysis

SECTION 1: DEFINITION AND OVERVIEW
A deadlock is a situation where a set of processes are blocked indefinitely 
because each process is holding a resource and waiting for a resource held by 
another process in the set. This creates a circular chain of dependencies...

[Content continues, total length: 2847 chars]

  ·────────────────────────────────────────────────────────────────────────────

Content Metrics:
  Word count: 1245
  ✓ Comprehensive detail level verified!
  Contains examples: ✓

  ·────────────────────────────────────────────────────────────────────────────

Citations & Sources (4):
  1. os_notes.pdf Page 12
  2. textbook.pdf Page 178
  3. lecture_slides.pdf Page 45
  4. assignment_solutions.pdf Page 8

  ✓ Citations present!

✓ Detailed summary test PASSED!

================================================================================
  TEST 4: Summary Modes Comparison
================================================================================

Query: Explain Deadlock in OS
Generating summaries in all three modes for comparison...

  Generating standard mode... ✓
  Generating revision mode... ✓
  Generating detailed mode... ✓

────────────────────────────────────────────────────────────────────────────────
  MODE COMPARISON TABLE
────────────────────────────────────────────────────────────────────────────────

  Mode        Chars    Words    Bullets  Sources
  ──────────────────────────────────────────────
  standard    1803     345      8        3
  revision    1124     215      5        2
  detailed    2847     1245     12       4

  ·────────────────────────────────────────────────────────────────────────────

Length Order Verification:
  Revision (215 words) < Standard (345 words) < Detailed (1245 words)
  ✓ Length hierarchy correct!

✓ Modes comparison test PASSED!

================================================================================
  TEST 5: Document Retrieval Verification
================================================================================

Query: Explain Deadlock in OS
Retrieving top 5 documents from vector store...

✓ Retrieved 5 documents

────────────────────────────────────────────────────────────────────────────────
  RETRIEVED DOCUMENTS
────────────────────────────────────────────────────────────────────────────────

  1. Source: os_notes.pdf
     Type: pdf | Page: 12
     Preview: Deadlock is a situation in resource allocation where processes...

  2. Source: textbook.pdf
     Type: pdf | Page: 178
     Preview: In this chapter, we explore deadlock prevention and recovery...

  3. Source: lecture_slides.pdf
     Type: pptx | Page: 45
     Preview: Deadlock Detection Algorithm: We use a variation of the banker's...

  4. Source: assignment_solutions.pdf
     Type: pdf | Page: 8
     Preview: Solution to Deadlock Problem: Consider two processes P1 and P2...

  5. Source: prev_year_questions.pdf
     Type: pdf | Page: 23
     Preview: Q: Explain the four conditions necessary for deadlock to occur...

✓ Document retrieval test PASSED!

================================================================================
  TEST SUMMARY
================================================================================

  Test Results:
    ✓ PASS - Document retrieval
    ✓ PASS - Standard summary generation
    ✓ PASS - Revision summary generation
    ✓ PASS - Detailed summary generation
    ✓ PASS - Modes comparison

  Total: 5/5 tests passed

  🎉 All tests PASSED!

================================================================================
  END OF TEST
================================================================================
```

### What to Verify Manually

1. **Standard Summary**
   - ✓ Contains 6 clear sections (TOPIC, CORE IDEA, KEY CONCEPTS, etc.)
   - ✓ Bullet points (8+) present
   - ✓ Citation references included (3+)
   - ✓ Professional academic tone

2. **Revision Summary**
   - ✓ Condensed format (200-400 words typically)
   - ✓ 5 key bullet points
   - ✓ Quick review format suitable for exams
   - ✓ Citations present (2+)

3. **Detailed Summary**
   - ✓ Comprehensive coverage (1000+ words)
   - ✓ Multiple sections with examples
   - ✓ Deep explanations and context
   - ✓ More citations (3+)

4. **Mode Hierarchy**
   - ✓ Revision < Standard < Detailed (by word count)
   - ✓ Each mode serves a distinct purpose
   - ✓ All modes include citations

5. **Document Retrieval**
   - ✓ Relevant documents returned
   - ✓ Source files identified correctly
   - ✓ Page numbers included
   - ✓ Content previews are accurate

---

## Running Both Tests

```bash
# Run both test suites
python tests/test_study_plan.py
python tests/test_summary.py

# Or run sequentially
python tests/test_study_plan.py && python tests/test_summary.py
```

## Prerequisites

Before running tests, ensure:

1. ✅ **Vector Database Populated**
   ```bash
   python vectorstore/ingest.py  # Upload documents to ChromaDB
   ```

2. ✅ **Environment Configured**
   ```bash
   # Set API key
   export GROQ_API_KEY="your_key_here"  # Linux/Mac
   set GROQ_API_KEY=your_key_here       # Windows
   ```

3. ✅ **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

4. ✅ **Sample Documents Available**
   - For Study Plan test: PDF in `sample_docs/` directory
   - For Summary test: Documents already ingested into vector store

---

## Troubleshooting

### Issue: "No PDF files found in sample_docs/"
**Solution**: 
- Place a syllabus PDF in the `sample_docs/` directory
- Ensure file has `.pdf` extension
- File should contain structured content with modules/topics

### Issue: "No documents retrieved"
**Solution**:
- Run `python vectorstore/ingest.py` to populate ChromaDB
- Ensure documents are uploaded successfully
- Check `GROQ_API_KEY` is set correctly

### Issue: "Module extraction failed"
**Solution**:
- Verify GROQ_API_KEY is valid
- Check PDF is readable and contains text (not image-only)
- Ensure PDF has clear module/topic structure

### Issue: "Summary generation error"
**Solution**:
- Verify vector database is populated
- Check API key is set
- Allow 10-15 seconds for LLM response
- Check network connectivity

---

## Test Output Files

Both test files generate console output suitable for:
- ✓ Manual verification of agent outputs
- ✓ Understanding agent behavior
- ✓ Debugging issues
- ✓ Documentation examples

The detailed printed output shows:
- Each processing step
- Intermediate results
- Verification checks
- Final summary statistics

---

## Integration with CI/CD

These tests can be integrated into CI/CD pipelines:

```yaml
# Example: GitHub Actions
- name: Test Study Plan Agent
  run: python tests/test_study_plan.py
  
- name: Test Summary Agent
  run: python tests/test_summary.py
```

Success is determined by:
- ✓ Test exits with code 0
- ✓ All verification checks pass
- ✓ Output shows "All tests PASSED!"

---

## Test Statistics

| Metric | Study Plan | Summary |
|--------|-----------|---------|
| Test Points | 5 | 5 |
| Expected Output Lines | 100+ | 150+ |
| Total Execution Time | 30-60s | 45-90s |
| Agent Coverage | 100% | 100% |

---

**Status**: ✅ Ready for Testing
**Last Updated**: December 2024
