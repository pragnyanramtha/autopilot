# Tests

Test files for AI Automation Assistant.

---

## 🧪 Running Tests

### All Tests
```cmd
cd ..
venv\Scripts\activate.bat
python tests\test_complex_workflows.py
```

### Specific Tests
```cmd
python tests\test_communication.py
python tests\test_executor.py
python tests\test_ai_brain_main.py
```

---

## 📋 Test Files

### Core Tests
- **`test_complex_workflows.py`** - Complex workflow generation tests
- **`test_communication.py`** - Inter-component communication tests
- **`test_executor.py`** - Automation executor tests

### Integration Tests
- **`test_ai_brain_main.py`** - AI Brain integration tests
- **`test_automation_engine_main.py`** - Automation Engine integration tests
- **`test_integration_full_flow.py`** - End-to-end tests

### Examples
- **`example_communication_flow.py`** - Communication examples
- **`test_quick.py`** - Quick sanity checks

---

## ✅ What Tests Cover

### Unit Tests
- Command parsing
- Workflow generation
- Step execution
- Communication layer

### Integration Tests
- AI Brain + Gemini API
- Automation Engine + PyAutoGUI
- Full workflow execution

### Feature Tests
- Complex workflows
- Content generation
- Search functionality
- Social media posting

---

## 🔧 Test Requirements

All tests require:
- Virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)
- API key in `.env` file (for AI Brain tests)

---

## 📊 Expected Results

All tests should pass:
```
✓ Simple command test passed
✓ Complex command structure test passed
✓ Content generation test passed (with API key)
✓ Research capability test passed (with API key)
✓ Workflow validation test passed
✓ New action types test passed
```

---

**Back to [Main README](../README.md)**
