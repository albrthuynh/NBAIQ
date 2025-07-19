# API Testing Guide

This directory contains comprehensive tests for the NBA IQ App API endpoints.

## Test Files Created

1. **`test_api.py`** - Unit tests using pytest and mocking
2. **`manual_test.py`** - Manual integration tests using real HTTP requests
3. **`run_tests.sh`** - Script to set up environment and run unit tests
4. **`requirements-test.txt`** - Testing dependencies

## API Endpoints Tested

### POST /api/users
- ✅ Successful user creation
- ✅ User already exists scenario
- ✅ Missing JSON data
- ✅ Missing required fields
- ✅ Database insertion failure

### GET /api/users/{user_id}
- ✅ Successful user retrieval
- ✅ Missing authorization header
- ✅ Invalid authorization format
- ✅ Invalid JWT token
- ✅ User not found
- ✅ Server errors

## Running Unit Tests (Recommended)

### Option 1: Using the provided script
```bash
./run_tests.sh
```

### Option 2: Manual setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-test.txt

# Run tests
python -m pytest test_api.py -v
```

## Running Manual Integration Tests

**Important**: Make sure your Flask app is running first!

```bash
# In one terminal, start your Flask app
python app.py

# In another terminal, run manual tests
python manual_test.py
```

The manual tests will:
- Test actual HTTP requests to your running server
- Verify error handling for various scenarios
- Show detailed response information

## Test Coverage

The tests cover:
- ✅ Happy path scenarios
- ✅ Error conditions
- ✅ Input validation
- ✅ Authentication/Authorization
- ✅ Database interaction (mocked in unit tests)
- ✅ HTTP status codes
- ✅ Response format validation

## Understanding the Tests

### Unit Tests (`test_api.py`)
- Use mocking to isolate the API logic from external dependencies
- Test the Flask application logic without needing a real database
- Fast execution and reliable results
- Best for development and CI/CD pipelines

### Manual Tests (`manual_test.py`)
- Make real HTTP requests to your running server
- Test the complete integration including CORS, JSON parsing, etc.
- Useful for verifying the app works end-to-end
- Good for debugging and manual verification

## Expected Test Results

When you run the unit tests, you should see output like:
```
test_api.py::TestUserEndpoints::test_home_endpoint PASSED
test_api.py::TestUserEndpoints::test_create_user_success PASSED
test_api.py::TestUserEndpoints::test_create_user_already_exists PASSED
test_api.py::TestUserEndpoints::test_create_user_missing_data PASSED
...
```

## Notes

- The unit tests use mocking so they don't require a real Supabase connection
- The manual tests require your Flask app to be running on port 5000
- Environment variables (.env.local) are needed for the app to start
- CORS is configured for localhost:5173 and localhost:5174
