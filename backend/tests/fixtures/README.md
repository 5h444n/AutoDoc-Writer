# Test Fixtures (Weird Code)

This directory contains edge-case code snippets used to test the robustness of the AutoDoc AI Parser.

## Files
1. **`syntax_error.js`**: Contains intentional syntax errors (missing brackets) to test parser resilience.
2. **`hardcoded_secrets.py`**: Contains fake AWS keys to ensure the AI detects (or ignores) sensitive data.
3. **`legacy_algo.cpp`**: C++ pointer logic to test multi-language support.
4. **`unicode_stress.py`**: Contains Emojis and Chinese characters to test UTF-8 encoding handling.
5. **`massive_file.py`**: A 600+ line auto-generated file to test Token Limit handling and truncation strategies.

## Usage
Do not import these files into the main application. They are for `pytest` ingestion only.