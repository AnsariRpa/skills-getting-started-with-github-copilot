# Tests Directory

This directory contains comprehensive backend tests for the Mergington High School Activities API.

## Test Structure

- `test_activities.py` - Main test suite covering all API endpoints
- `__init__.py` - Package marker for Python

## Dependencies

Make sure to install all dependencies:

```bash
pip install -r requirements.txt
```

Required packages for testing:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `fastapi` - API framework (with TestClient for testing)

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_activities.py

# Run specific test class
pytest tests/test_activities.py::TestSignupForActivity

# Run specific test method
pytest tests/test_activities.py::TestSignupForActivity::test_signup_success
```

## Test Coverage

The tests cover all API endpoints using the AAA (Arrange-Act-Assert) pattern:

### GET /activities
- ✅ Successful retrieval of activities data
- ✅ Proper data structure validation

### POST /activities/{activity_name}/signup
- ✅ Successful signup
- ✅ Activity not found error
- ✅ Duplicate participant error

### DELETE /activities/{activity_name}/participants
- ✅ Successful participant removal
- ✅ Activity not found error
- ✅ Participant not found error

### GET /
- ✅ Root endpoint redirect functionality

## Test Framework

- **pytest** - Test runner and framework
- **pytest-asyncio** - Async test support
- **FastAPI TestClient** - Isolated API testing without server startup