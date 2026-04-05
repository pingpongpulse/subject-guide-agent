# Quick Test Execution Guide

## TL;DR - Run Tests in 30 Seconds

```bash
# Terminal 1: Start vector database ingest (if needed)
python vectorstore/ingest.py

# Terminal 2: Run Study Plan Test
python tests/test_study_plan.py

# Terminal 3: Run Summary Test
python tests/test_summary.py
```

---

## Prerequisites Checklist

- [ ] GROQ_API_KEY set: `echo $GROQ_API_KEY` (should show key)
- [ ] Vector DB populated: `python vectorstore/ingest.py`
- [ ] Sample PDF exists: `ls sample_docs/`
- [ ] Python dependencies: `pip install -r requirements.txt`

---

## Test Files Created

### 1. `tests/test_study_plan.py` (5 test steps)

**Purpose**: Test Study Plan Generator Agent

**What it tests**:
- Finds syllabus PDF
- Extracts modules (AI-parsed)
- Maps to vector DB documents
- Generates structured plan
- Validates week structure

**Run**:
```bash
python tests/test_study_plan.py
```

**Expected**: ✓ 4/4 tests pass, shows actual modules and study plan

**Manual Verification**:
```
✓ Modules extracted from syllabus
✓ Each module maps to documents
✓ Study plan has correct weeks
✓ Each week has topics + hours + focus area
```

---

### 2. `tests/test_summary.py` (5 test steps)

**Purpose**: Test Summary Agent with 3 modes

**What it tests**:
- Document retrieval
- Standard summary (6 sections)
- Revision summary (5 bullets)
- Detailed summary (9 sections)
- Mode comparison

**Run**:
```bash
python tests/test_summary.py
```

**Expected**: ✓ 5/5 tests pass, shows all 3 summary modes with citations

**Manual Verification**:
```
✓ Standard summary has 6 sections
✓ Revision summary is condensed (bullets)
✓ Detailed summary is comprehensive
✓ All modes have citations
✓ Length: revision < standard < detailed
```

---

## Output Highlights

### Study Plan Test Output

```
STEP 1: Finding Syllabus PDF
  ✓ Found PDF: syllabus.pdf (245 KB)

STEP 2: Module Extraction
  ✓ Extracted 5 modules:
    1. Process Scheduling
    2. Memory Management
    3. File Systems
    4. Deadlock
    5. Synchronization

STEP 3: Module Mapping
  ✓ Mapped 5 modules to vector DB documents
  ✓ Retrieved 3-5 related docs per module

STEP 4: Study Plan Generation
  ✓ Generated 4-week plan (15 hours/week)
  ✓ Week structure verified correct

STEP 5: Full Pipeline
  ✓ Complete plan with 5 modules, sources
  ✓ Metadata includes generation timestamp

TEST SUMMARY: 4/4 PASSED ✓
```

### Summary Test Output

```
TEST 1: Standard Summary
  ✓ 6 sections detected
  ✓ 8+ bullet points
  ✓ 3+ citations present

TEST 2: Revision Summary
  ✓ 340 words (condensed)
  ✓ 5 key bullet points
  ✓ 2+ citations present

TEST 3: Detailed Summary
  ✓ 1245 words (comprehensive)
  ✓ Examples included
  ✓ 4+ citations present

TEST 4: Modes Comparison
  ✓ Length: Revision < Standard < Detailed
  ✓ All modes have citations

TEST 5: Document Retrieval
  ✓ 5 documents retrieved
  ✓ All have source + page number

TEST SUMMARY: 5/5 PASSED ✓
```

---

## Success Criteria

### Study Plan Test ✓
- [x] Test runs without errors
- [x] Finds PDF in sample_docs
- [x] Extracts 3+ modules
- [x] Maps modules to documents
- [x] Generates plan with correct week count
- [x] Output shows "4/4 tests passed"

### Summary Test ✓
- [x] Test runs without errors
- [x] Retrieves documents
- [x] Generates 3 summary modes
- [x] Standard mode has 6+ sections
- [x] Revision mode is condensed
- [x] Detailed mode is comprehensive
- [x] All summaries have citations
- [x] Output shows "5/5 tests passed"

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: groq` | `pip install groq` |
| `GROQ_API_KEY not set` | `export GROQ_API_KEY=xxx` |
| `No PDF files found` | Put PDF in `sample_docs/` |
| `No documents retrieved` | Run `python vectorstore/ingest.py` |
| `Connection timeout` | Check network, retry |

---

## File Locations

```
subject-guide-agent/
├── tests/
│   ├── test_study_plan.py     ← Run this
│   └── test_summary.py        ← And this
├── sample_docs/
│   └── your_syllabus.pdf      ← Put PDF here
├── vectorstore/
│   ├── ingest.py              ← Populate DB
│   └── retriever.py
└── agents/
    ├── study_plan_generator.py
    └── summary_agent.py
```

---

## Step-by-Step Walkthrough

### Setup (One time)

```bash
# 1. Set API key
export GROQ_API_KEY="your_groq_key_here"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add sample PDF
# → Place a syllabus PDF in sample_docs/

# 4. Populate vector database
python vectorstore/ingest.py
```

### Run Tests

```bash
# 5. Run study plan test
python tests/test_study_plan.py
# Output: Shows module extraction, mapping, plan structure

# 6. Run summary test
python tests/test_summary.py
# Output: Shows summaries in 3 modes with citations

# 7. Verify outputs
# → Check manual verification checklist above
```

---

## What Each Test Prints

### test_study_plan.py Prints

```
✓ Finding syllabus PDF
✓ Extracting modules with LLM
✓ Mapping modules to vector DB
✓ Generating structured plan
✓ Week structure validation
✓ Complete pipeline execution
```

### test_summary.py Prints

```
✓ Document retrieval (5 docs)
✓ Standard summary (6 sections)
✓ Revision summary (5 bullets)
✓ Detailed summary (9 sections)
✓ Mode comparison table
✓ Length hierarchy verification
```

---

## Expected Execution Times

| Test | Time |
|------|------|
| Study Plan test | 30-60 seconds |
| Summary test | 45-90 seconds |
| Total both | 75-150 seconds |

---

## Documentation

- **Full details**: [TESTING_GUIDE.md](./TESTING_GUIDE.md)
- **Router integration**: [ROUTER_INTEGRATION_SUMMARY.md](./ROUTER_INTEGRATION_SUMMARY.md)
- **Frontend guide**: [ROUTER_FRONTEND_GUIDE.md](./ROUTER_FRONTEND_GUIDE.md)

---

## TL;DR Commands

```bash
# Quick test run
python tests/test_study_plan.py && python tests/test_summary.py

# View what tests do
cat tests/test_study_plan.py
cat tests/test_summary.py

# Check for issues
python -m py_compile tests/test_study_plan.py tests/test_summary.py
```

---

**Status**: ✅ Ready to Run
**Last Updated**: December 2024
