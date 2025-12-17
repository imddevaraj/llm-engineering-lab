# Failure Modes & Hallucination Lab

Intentionally trigger and observe known LLM failure modes in a controlled environment.

This module focuses on understanding *how* and *why* LLMs fail, rather than preventing failures prematurely.

## Problem Statement

LLMs fail silently and confidently. Without proactive testing, failures surface only in production.

---

##  Solution Overview

This lab introduces:
- Failure-specific datasets
- Controlled system prompts
- Failure classification
- Known-failure cataloging

---

## 🔍 Failure Modes Explored

- Hallucination (fabricated facts)
- Overconfidence on unknown topics
- Instruction bypass attempts
- Prompt leakage

---

##  Pattern Introduced

### Failure-First AI Design Pattern

**Principle**
> Design for failure before designing guardrails.

**Benefits**
- Predictable system behavior
- Safer AI deployments
- Easier incident response

---

##  Known Limitations

- Manual failure classification
- No automated enforcement
- No retry or correction logic

These are intentionally deferred.

---

Build a Failure Modes Lab to:

- Intentionally induce LLM failures
- Observe hallucinations, overconfidence, prompt leakage
- Classify failure patterns
- Create a known-failure dataset that feeds guardrails later

Benefit Hypothesis:

- You will expect failures, not be surprised by them
- You’ll have a reusable catalog of AI failure modes
- You’ll lay the foundation for guardrails & safety

## Why This Matters (Very Real World)

In production, LLMs fail by:

- Confidently lying
- Ignoring instructions
- Leaking system prompts
- Answering questions they should refuse
- Making up sources

Most teams only discover this after incidents.

You are doing it proactively.

---

## 🧪 Testing

The hallucination lab includes comprehensive test coverage for all components.

### Running Tests

**Run all tests:**
```bash
cd /Users/devaraj/Documents/personal/llm-engineering-lab
poe test-hallucination
```

**Run tests with coverage:**
```bash
poe test-hallucination-cov
```

**Run specific test files:**
```bash
cd 04-hallucination-lab
pytest tests/unit/test_failure_classifier.py -v
pytest tests/integration/test_failure_runner.py -v
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
  - `test_failure_classifier.py` - Tests for classification logic
  - `test_datasets.py` - Tests for dataset structure validation
  
- **Integration Tests**: Test components working together
  - `test_failure_runner.py` - Tests for runner with mock LLM client
  - `test_end_to_end.py` - End-to-end workflow tests

### Test Coverage

Tests cover:
- ✅ All classification scenarios (safe_response, hallucination, instruction_leak, unknown)
- ✅ Edge cases (empty strings, case sensitivity, special characters)
- ✅ Dataset validation and loading
- ✅ Mock LLM integration (no API costs during testing)
- ✅ Complete workflow from dataset → runner → classification

### Adding New Tests

To add tests for new failure scenarios:

1. Update the classifier logic in `src/classifier/failure_classifier.py`
2. Add test cases to `tests/unit/test_failure_classifier.py`
3. Add dataset tests to `tests/unit/test_datasets.py` if needed
4. Run tests to verify: `poe test-hallucination`