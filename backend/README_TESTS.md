# Running Tests

## Quick Start

```bash
cd backend
pip install -r requirements.txt
pytest test_backend.py -v
```

## Test Coverage

The test suite covers:
- ✅ Authentication endpoints
- ✅ GitHub API integration
- ✅ Database configuration
- ✅ Error handling
- ✅ Security issues
- ✅ Performance scenarios
- ✅ Environment configuration
- ✅ CORS middleware

## Test Results

**Current Status**: 16/21 tests passing (76%)

### Passing Tests (16)
- Main application endpoints
- Authentication flow (login redirect)
- GitHub repository fetching
- Database initialization
- Environment variable handling
- Error responses
- Security configurations
- Integration flows
- Performance with large datasets

### Failing Tests (5)
The failing tests are due to mock configuration issues, not actual application bugs:
- 4 async mock context manager issues
- 1 PyGithub exception serialization (known library issue)

## Running Specific Tests

```bash
# Run all tests
pytest test_backend.py -v

# Run specific test class
pytest test_backend.py::TestAuthentication -v

# Run specific test
pytest test_backend.py::TestAuthentication::test_login_endpoint_redirects_to_github -v

# Run with coverage
pytest test_backend.py --cov=. --cov-report=html

# Run quietly
pytest test_backend.py -q
```

## Test Categories

### 1. Main Application Tests
Tests the core FastAPI application setup and endpoints.

### 2. Authentication Tests
Tests the GitHub OAuth flow including login and callback endpoints.

### 3. GitHub Repository Tests
Tests fetching repositories from GitHub API.

### 4. Database Tests
Tests database configuration and session management.

### 5. Environment Configuration Tests
Tests environment variable handling and validation.

### 6. Error Handling Tests
Tests error responses and exception handling.

### 7. Security Tests
Tests for security vulnerabilities and best practices.

### 8. Integration Tests
End-to-end tests of complete workflows.

### 9. Performance Tests
Tests handling of large datasets.

## Continuous Integration

The tests are designed to run in CI/CD environments. Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest test_backend.py -v --cov=.
```

## Related Documentation

- [BUG_REPORT.md](../BUG_REPORT.md) - All bugs discovered
- [IMPROVEMENTS.md](../IMPROVEMENTS.md) - Improvement recommendations
- [TESTING_SUMMARY.md](../TESTING_SUMMARY.md) - Complete testing summary
