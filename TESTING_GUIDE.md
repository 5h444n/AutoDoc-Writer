# Testing Guide for AutoDoc-Writer

## Quick Start

### Running Tests

```bash
# Navigate to backend
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/security/
pytest tests/performance/

# Run specific test file
pytest tests/unit/test_main.py

# Run specific test
pytest tests/unit/test_main.py::test_root_endpoint_returns_success

# Run tests matching a pattern
pytest -k "github"
pytest -k "security"

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then all others
pytest --ff
```

### Test Categories

Tests are organized into categories using markers:

```bash
# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only security tests
pytest -m security

# Run only performance tests
pytest -m performance

# Exclude slow tests
pytest -m "not slow"
```

---

## Test Structure

```
backend/tests/
├── conftest.py              # Shared fixtures
├── __init__.py
│
├── unit/                    # Unit tests (isolated, fast)
│   ├── test_main.py         # Main application tests
│   ├── core/
│   │   └── test_config.py   # Configuration tests
│   └── services/
│       └── test_github_service.py
│
├── integration/             # Integration tests
│   └── test_api_integration.py
│
├── security/                # Security tests
│   └── test_authentication.py
│
└── performance/             # Performance tests
    └── test_performance.py
```

---

## Writing Tests

### Basic Test Template

```python
import pytest

def test_something():
    """Test description in docstring."""
    # Arrange - Set up test data and conditions
    expected_value = 42
    
    # Act - Execute the code being tested
    result = function_to_test()
    
    # Assert - Verify the results
    assert result == expected_value
```

### Using Fixtures

```python
def test_with_client(client):
    """Test using the test client fixture."""
    response = client.get("/")
    assert response.status_code == 200
```

### Using Mocks

```python
from unittest.mock import patch, Mock

@patch('app.services.github_service.Github')
def test_with_mock(mock_github):
    """Test with mocked external dependency."""
    # Configure mock
    mock_github.return_value.get_user.return_value = Mock(login="testuser")
    
    # Execute test
    result = some_function()
    
    # Verify
    assert result == expected_value
    mock_github.assert_called_once()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input, expected):
    """Test multiplication with multiple inputs."""
    assert input * 2 == expected
```

---

## Test Coverage

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Open HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Targets

| Module | Target | Current |
|--------|--------|---------|
| Overall | 80% | ~60% |
| Core Services | 90% | ~100% |
| API Endpoints | 85% | ~80% |
| Models | 90% | ~40% |

---

## Common Test Scenarios

### Testing API Endpoints

```python
def test_api_endpoint(client):
    """Test API endpoint returns correct response."""
    response = client.get("/api/v1/repos/?access_token=test")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_repos" in data
    assert isinstance(data["repos"], list)
```

### Testing Database Operations

```python
def test_database_create(test_db):
    """Test creating a database record."""
    from app.models.user import User
    
    user = User(github_username="testuser", access_token="token")
    test_db.add(user)
    test_db.commit()
    
    # Query back
    retrieved = test_db.query(User).filter_by(github_username="testuser").first()
    assert retrieved is not None
    assert retrieved.github_username == "testuser"
```

### Testing Error Handling

```python
def test_error_handling(client):
    """Test that errors are handled correctly."""
    response = client.get("/api/v1/repos/")  # Missing required param
    
    assert response.status_code == 422
    assert "detail" in response.json()
```

### Testing Security

```python
def test_authentication_required(client):
    """Test that endpoint requires authentication."""
    response = client.get("/api/v1/repos/")
    assert response.status_code in [401, 422]
```

---

## Debugging Tests

### Run with Debugging

```bash
# Run with Python debugger
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show local variables on failure
pytest -l

# Capture stdout (print statements)
pytest -s

# More verbose output
pytest -vv
```

### Using Print Debugging

```python
def test_with_debug(client):
    """Test with debug output."""
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
```

Run with: `pytest -s tests/unit/test_main.py::test_with_debug`

---

## CI/CD Integration

Tests are automatically run on every push and pull request via GitHub Actions.

### Workflow Triggers

- **Push to main**: Full test suite + coverage report
- **Pull request**: Full test suite + security scan
- **Nightly**: Full test suite + performance benchmarks

### Required Checks

All PRs must:
- ✅ Pass all tests (100%)
- ✅ Maintain or improve coverage
- ✅ Pass security scan
- ✅ Pass linting

---

## Performance Testing

### Running Performance Tests

```bash
# Run only performance tests
pytest tests/performance/

# Run with timing information
pytest --durations=10

# Run performance benchmarks
pytest tests/performance/ --benchmark-only
```

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| API Response Time | <200ms | <100ms ✅ |
| Concurrent Requests | 50+ | 50+ ✅ |
| Database Queries | <100ms | <100ms ✅ |

---

## Security Testing

### Running Security Tests

```bash
# Run security test suite
pytest tests/security/

# Run security scan with bandit
cd backend
bandit -r app/ -f json -o bandit-report.json

# Check dependencies for vulnerabilities
safety check
```

### Security Checklist

- [ ] Authentication tests passing
- [ ] Authorization tests passing
- [ ] Input validation tests passing
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No exposed secrets in code
- [ ] Rate limiting implemented
- [ ] HTTPS enforced

---

## Troubleshooting

### Common Issues

#### Tests Fail with Import Errors

**Solution**: Make sure you're in the backend directory and have installed dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### Database Errors in Tests

**Solution**: Tests use in-memory SQLite database. Check that `DATABASE_URL` in conftest.py is set to `sqlite:///:memory:`

#### Mock Not Working

**Solution**: Ensure you're mocking at the right level:
```python
# Mock where it's used, not where it's defined
@patch('app.services.github_service.Github')  # ✅ Correct
@patch('github.Github')                        # ❌ Wrong
```

#### Async Test Errors

**Solution**: Use `pytest-asyncio` and mark async tests:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

---

## Best Practices

### ✅ Do

- Write tests before fixing bugs (TDD)
- Keep tests small and focused
- Use descriptive test names
- Test edge cases and error conditions
- Mock external dependencies
- Use fixtures for common setup
- Aim for >80% code coverage
- Run tests before committing

### ❌ Don't

- Test implementation details
- Write tests that depend on each other
- Use sleep() in tests (use mocks/fixtures)
- Leave commented-out test code
- Skip tests without good reason
- Test third-party libraries
- Write slow tests without marking them

---

## Test Metrics

Current test metrics (as of latest run):

```
Total Tests: 75
Passing: 67 (89%)
Failing: 8 (11%)
Execution Time: <1 second
Coverage: ~60%
```

**Goal**: 150+ tests, 100% pass rate, 80%+ coverage

---

## Additional Resources

### Documentation

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)

### Tools

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-asyncio**: Async test support
- **pytest-mock**: Enhanced mocking
- **pytest-xdist**: Parallel execution
- **bandit**: Security linting
- **safety**: Dependency scanning

---

## Getting Help

If you encounter issues with tests:

1. Check this guide first
2. Review test output carefully
3. Check the [COMPREHENSIVE_TEST_REPORT.md](./COMPREHENSIVE_TEST_REPORT.md)
4. Review [RECOMMENDATIONS.md](./RECOMMENDATIONS.md)
5. Open an issue with:
   - Test output
   - Environment details
   - Steps to reproduce

---

**Happy Testing! 🧪**
