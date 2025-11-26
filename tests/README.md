# Test Configuration

This directory contains test configuration files and pytest settings.

## Running Tests

### All Tests
```bash
pytest
```

### Unit Tests Only
```bash
pytest tests/unit/
```

### Integration Tests Only
```bash
pytest tests/integration/
```

### With Coverage
```bash
pytest --cov=src --cov-report=html
```

### Specific Test File
```bash
pytest tests/unit/test_supervisor.py
```

### Specific Test Function
```bash
pytest tests/unit/test_supervisor.py::TestSupervisorAgent::test_audit_supplier_happy_path
```

## Test Structure

- `tests/unit/` - Unit tests for individual components
  - `test_supervisor.py` - Tests for Supervisor Agent
  - `test_investigator.py` - Tests for Investigator Agent
  - `test_auditor.py` - Tests for Auditor Agent

- `tests/integration/` - Integration tests for complete workflows
  - `test_workflow.py` - End-to-end audit workflow tests

## Writing Tests

### Unit Test Template
```python
import pytest
from src.module import MyClass

class TestMyClass:
    def setup_method(self):
        self.instance = MyClass()
    
    def test_something(self):
        result = self.instance.method()
        assert result == expected_value
```

### Integration Test Template
```python
def test_end_to_end_flow():
    # Arrange
    setup_data()
    
    # Act
    result = run_complete_workflow()
    
    # Assert
    assert result.success
```

## Test Data

Mock data is used for unit and integration tests. For AWS integration tests with real Bedrock agents, see AWS-specific test configuration.

## Continuous Integration

Tests should be run as part of CI/CD pipeline. See `.github/workflows/` for CI configuration (if available).
