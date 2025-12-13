# Test Fixtures (Weird Code)

This directory contains edge-case code snippets used to test the robustness of the AutoDoc AI Parser.

## Files
1. **`syntax_error.js`**: Contains intentional syntax errors (missing brackets) to test parser resilience.
2. **`hardcoded_secrets.py`**: Contains fake AWS keys to ensure the AI detects (or ignores) sensitive data.
3. **`legacy_algo.cpp`**: C++ pointer logic to test multi-language support.
4. **`unicode_stress.py`**: Contains Emojis and Chinese characters to test UTF-8 encoding handling.
5. **`massive_file.py`**: A 600+ line auto-generated file to test Token Limit handling and truncation strategies.
...
6. **`dangerous.sh`**: Contains `rm -rf` and fork bombs to test security filters.
7. **`minified_hell.js`**: Single-line minified code to test parser line-wrapping.
8. **`sql_injection.sql`**: SQL injection patterns.
9. **`infinite_loop.py`**: Infinite recursion to test analysis timeouts.
10. **`corrupt.py.png`**: Binary garbage disguised as code.
11. **`empty.ts`**: Zero-byte file.
12. **`mixed_indentation.py`**: Invalid tabs/spaces mixing.
13. **`reserved_keywords.java`**: Illegal variable names.
14. **`only_comments.go`**: File with comments only (no logic).
15. **`notebook_mess.py`**: Mixed JSON/Python metadata artifacts.

## Usage
Do not import these files into the main application. They are for `pytest` ingestion only.