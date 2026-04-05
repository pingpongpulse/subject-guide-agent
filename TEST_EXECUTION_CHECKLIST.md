# Test Execution Checklist

## Pre-Test Setup

### Environment Variables
- [ ] `GROQ_API_KEY` is set
  ```bash
  echo $GROQ_API_KEY  # Should print your key
  ```

### File System
- [ ] `sample_docs/` directory exists
  ```bash
  ls sample_docs/
  ```
- [ ] At least one PDF file in `sample_docs/`
  ```bash
  ls sample_docs/*.pdf
  ```

### Dependencies
- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```
- [ ] Required packages installed
  ```bash
  pip install groq langchain chromadb python-dotenv PyPDF2
  ```

### Vector Database
- [ ] ChromaDB initialized
- [ ] Documents ingested
  ```bash
  python vectorstore/ingest.py
  ```

---

## Study Plan Test Execution

### Start Test
```bash
python tests/test_study_plan.py
```

### Monitor Output

#### ✓ Step 1: Finding Syllabus PDF
- [ ] PDF file found in sample_docs/
- [ ] File size shown (KB)
- [ ] Path displayed correctly

#### ✓ Step 2: Module Extraction
- [ ] "Successfully extracted X modules" message
- [ ] At least 3 modules listed
- [ ] Module names are relevant to topic
- [ ] No duplicate modules
- [ ] ✓ Module extraction successful! displayed

#### ✓ Step 3: Module-to-Document Mapping
- [ ] Maps show "Successfully mapped modules to documents"
- [ ] Each module has priority score (0.0-1.0)
- [ ] Each module shows 2-3 related documents
- [ ] Documents have source file and page number
- [ ] Content preview shown for each document
- [ ] ✓ Module mapping successful! displayed

#### ✓ Step 4: Study Plan Generation
- [ ] Study plan generated successfully message
- [ ] Week count matches expected (e.g., 4 weeks)
- [ ] Each week shows: Topics, Hours, Focus Area
- [ ] Topics are from extracted modules
- [ ] Hours allocation shown
- [ ] ✓ Study plan generation successful! displayed

#### ✓ Step 5: Full Pipeline Test
- [ ] "Full pipeline completed" message
- [ ] Metadata section shows info
- [ ] Modules Analyzed count displayed
- [ ] Sources Used count displayed
- [ ] Sample week data shown
- [ ] ✓ Full pipeline completed! displayed

### Test Summary
- [ ] "TEST SUMMARY" section appears
- [ ] Shows 4 test results
- [ ] All 4 tests show ✓ PASS
- [ ] Total shows "4/4 tests passed"
- [ ] 🎉 All tests PASSED! message shown
- [ ] Exit code: 0 (success)

---

## Summary Test Execution

### Start Test
```bash
python tests/test_summary.py
```

### Monitor Output

#### ✓ Test 1: Standard Summary
- [ ] Summary generated successfully
- [ ] 6 sections detected (TOPIC, CORE IDEA, KEY CONCEPTS, IMPORTANT POINTS, EXAM FOCUS, EXAMPLE)
- [ ] 6+ bullet points found
- [ ] Citations listed (minimum 2 sources)
- [ ] "✓ PASS" shown for test
- [ ] "Structure Verification" shows sections found

#### ✓ Test 2: Revision Summary
- [ ] Summary generated successfully
- [ ] Word count shown (should be 150-400)
- [ ] "✓ Condensed format verified!" displayed
- [ ] 5+ bullet points present
- [ ] "✓ Key points in bullet format!" shown
- [ ] 1-2 citations present
- [ ] "✓ PASS" shown for test

#### ✓ Test 3: Detailed Summary
- [ ] Summary generated successfully
- [ ] Word count shown (should be 800+)
- [ ] "✓ Comprehensive detail level verified!" displayed
- [ ] Contains examples section
- [ ] "✓" shown for contains examples
- [ ] 3-4 citations present
- [ ] "✓ PASS" shown for test

#### ✓ Test 4: Modes Comparison
- [ ] All three modes generated
- [ ] Comparison table shown with metrics:
  - [ ] Mode name
  - [ ] Character count
  - [ ] Word count
  - [ ] Bullet count
  - [ ] Source count
- [ ] Length order verified: Revision < Standard < Detailed
- [ ] "✓ Length hierarchy correct!" displayed
- [ ] "✓ PASS" shown for test

#### ✓ Test 5: Document Retrieval
- [ ] "Retrieved X documents" message (5 documents)
- [ ] Each document shows:
  - [ ] Source filename
  - [ ] Document type (pdf/pptx)
  - [ ] Page number
  - [ ] Content preview (first 100 chars)
- [ ] All 5 documents listed
- [ ] "✓ PASS" shown for test

### Test Summary
- [ ] "TEST SUMMARY" section appears
- [ ] Shows 5 test results
- [ ] All 5 tests show ✓ PASS
- [ ] Total shows "5/5 tests passed"
- [ ] 🎉 All tests PASSED! message shown
- [ ] Exit code: 0 (success)

---

## Manual Verification Checklist

### Study Plan Outputs

#### Module Extraction
- [ ] Modules make sense for the topic
- [ ] No garbage or malformed text
- [ ] At least 3-5 distinct modules
- [ ] Module names are complete sentences or clear phrases

#### Module Mapping
- [ ] Each module maps to relevant documents
- [ ] Priority scores are between 0 and 1
- [ ] Related documents contain relevant content
- [ ] Source files are actual uploaded documents

#### Study Plan Structure
- [ ] All requested weeks are present
- [ ] Each week has topics, hours, and focus
- [ ] Topics progress logically week to week
- [ ] Total hours per week matches requested

#### Plan Metadata
- [ ] Timestamp is recent
- [ ] Module count matches extracted modules
- [ ] Sources are from uploaded documents
- [ ] Plan data is properly formatted JSON

### Summary Outputs

#### Standard Summary Verification
- [ ] All 6 sections present and clear
- [ ] Content is academically appropriate
- [ ] Bullet points are substantive
- [ ] Citations reference actual documents
- [ ] No hallucinations or false claims

#### Revision Summary Verification
- [ ] Significantly shorter than standard (~50% length)
- [ ] 5 key points capture essence
- [ ] Suitable for quick review
- [ ] Citations are present
- [ ] Can be used for exam prep

#### Detailed Summary Verification
- [ ] Longest of the three (~3x standard)
- [ ] Includes examples and explanations
- [ ] Covers topic comprehensively
- [ ] More citations than other modes
- [ ] Suitable for deep learning

#### Citation Verification
- [ ] Citations reference uploaded documents
- [ ] Page numbers are valid (not negative)
- [ ] Source files are readable/listed
- [ ] Multiple sources used (not just one)
- [ ] Citations appear in summary context

---

## Common Output Patterns

### ✓ Successful Run

```
✓ Successfully extracted 5 modules
✓ Module map successful!
✓ Study plan generated successfully!
✓ Full pipeline completed!

TEST SUMMARY
  ✓ PASS - Module extraction
  ✓ PASS - Module mapping
  ✓ PASS - Study plan generation
  ✓ PASS - Full pipeline

  Total: 4/4 tests passed
  🎉 All tests PASSED!
```

### ⚠️ Warning Signs (May Still Pass)

```
⚠️ No documents retrieved
  → Indicates vector DB may be empty
  → Run: python vectorstore/ingest.py

⚠️ Module count mismatch
  → Some modules not processed
  → Can still be acceptable
```

### ❌ Failure Indicators (Fix Before Proceeding)

```
❌ Error: GROQ_API_KEY not configured
  → Set: export GROQ_API_KEY=your_key

❌ Error retrieving modules
  → Verify PDF is readable
  → Check API connectivity

❌ No PDF files found in sample_docs/
  → Add PDF to sample_docs/ directory

❌ Test did not pass (< expected count)
  → Check logs above for specific errors
```

---

## Test Duration

| Phase | Expected Time |
|-------|---|
| Study Plan Test | 30-60 seconds |
| Summary Test | 45-90 seconds |
| Total | 75-150 seconds |

**If tests take > 3 minutes**: Check network connectivity and API responsiveness

---

## Recording Test Results

### Study Plan Test Results

**Date**: ________________
**Time**: ________________
**Status**: [ ] PASSED [ ] FAILED

Modules Extracted: ______
Documents Mapped: ______
Weeks Generated: _______ (Expected: 3-4)

**Issues Found**:
```




```

### Summary Test Results

**Date**: ________________
**Time**: ________________
**Status**: [ ] PASSED [ ] FAILED

Standard Summary: [ ] Good [ ] Issues
Revision Summary: [ ] Good [ ] Issues
Detailed Summary: [ ] Good [ ] Issues
Document Retrieval: [ ] Good [ ] Issues

**Citation Quality**: [ ] Excellent [ ] Good [ ] Needs Work

**Issues Found**:
```




```

---

## Next Steps After Tests

### If All Tests Pass ✓
1. [ ] Document the results
2. [ ] Note test date/time
3. [ ] Proceed with frontend integration
4. [ ] Test with Streamlit interface

### If Some Tests Fail ✗
1. [ ] Review error messages above
2. [ ] Check prerequisites checklist
3. [ ] Rerun failed test
4. [ ] If persistent, check logs for API errors

### If Tests Error Out ❌
1. [ ] Check API key is valid
2. [ ] Verify network connectivity
3. [ ] Ensure vector DB is populated
4. [ ] Try running again after 30 seconds

---

## Support Information

### Quick Fixes

| Error | Fix |
|-------|-----|
| "API key not set" | `export GROQ_API_KEY=xxx` |
| "No PDF found" | Add PDF to `sample_docs/` |
| "No documents" | Run `python vectorstore/ingest.py` |
| "Connection error" | Check internet, wait 30s, retry |
| "Module not found" | Install: `pip install -r requirements.txt` |

### Documentation

- Full test guide: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- Quick reference: [QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md)
- Router info: [ROUTER_INTEGRATION_SUMMARY.md](ROUTER_INTEGRATION_SUMMARY.md)

---

**Print this page for test day!**

**Status**: Ready for Testing ✅
**Last Updated**: December 2024
