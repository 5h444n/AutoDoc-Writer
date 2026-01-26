"""Tests for AI documentation prompts system."""

import pytest
from app.core.prompts import DocumentationPrompts


class TestDocumentationPrompts:
    """Test suite for DocumentationPrompts class."""
    
    def test_get_prompt_plain(self):
        """Test retrieval of plain English prompt."""
        prompt = DocumentationPrompts.get_prompt("plain")
        assert "mentor" in prompt.lower()
        assert "conversational" in prompt.lower()
    
    def test_get_prompt_research(self):
        """Test retrieval of research/thesis prompt."""
        prompt = DocumentationPrompts.get_prompt("research")
        assert "academic" in prompt.lower()
        assert "formal" in prompt.lower()
    
    def test_get_prompt_latex(self):
        """Test retrieval of LaTeX prompt."""
        prompt = DocumentationPrompts.get_prompt("latex")
        assert "latex" in prompt.lower()
        assert "\\section" in prompt or "section" in prompt.lower()
    
    def test_get_prompt_invalid_style(self):
        """Test error on invalid style."""
        with pytest.raises(ValueError):
            DocumentationPrompts.get_prompt("invalid_style")
    
    def test_truncate_code_no_truncation(self):
        """Test code truncation when code is short enough."""
        code = "def hello():\n    print('world')"
        result, was_truncated = DocumentationPrompts.truncate_code(code)
        assert result == code
        assert was_truncated is False
    
    def test_truncate_code_with_truncation(self):
        """Test code truncation when code exceeds limit."""
        code = "x" * 10000
        result, was_truncated = DocumentationPrompts.truncate_code(code, max_chars=1000)
        assert len(result) < len(code)
        assert was_truncated is True
        assert "truncated" in result.lower()
    
    def test_build_user_prompt_basic(self):
        """Test building basic user prompt."""
        code = "def test():\n    pass"
        prompt = DocumentationPrompts.build_user_prompt(code, "plain")
        assert code in prompt
        assert "plain" in prompt
    
    def test_build_user_prompt_with_filename(self):
        """Test building user prompt with filename."""
        code = "def test():\n    pass"
        filename = "test.py"
        prompt = DocumentationPrompts.build_user_prompt(code, "plain", filename)
        assert code in prompt
        assert filename in prompt
    
    def test_build_user_prompt_truncates_long_code(self):
        """Test that user prompt builder truncates long code."""
        code = "x" * 10000
        prompt = DocumentationPrompts.build_user_prompt(code, "plain")
        assert "truncated" in prompt.lower()
    
    def test_validate_output_plain_valid(self):
        """Test validation of valid plain output."""
        output = "This is a comprehensive explanation of the code. " * 10
        assert DocumentationPrompts.validate_output(output, "plain") is True
    
    def test_validate_output_plain_too_short(self):
        """Test rejection of too-short plain output."""
        output = "Short"
        assert DocumentationPrompts.validate_output(output, "plain") is False
    
    def test_validate_output_research_valid(self):
        """Test validation of valid research output."""
        output = "Abstract: This paper presents... Introduction: The methodology employed... Conclusion: Results demonstrate..."
        assert DocumentationPrompts.validate_output(output, "research") is True
    
    def test_validate_output_research_missing_sections(self):
        """Test rejection of research output without proper sections."""
        output = "Just some random text without proper academic structure."
        assert DocumentationPrompts.validate_output(output, "research") is False
    
    def test_validate_output_latex_valid(self):
        """Test validation of valid LaTeX output."""
        output = "\\section{Introduction}\\nThis code implements...\\n\\subsection{Details}"
        assert DocumentationPrompts.validate_output(output, "latex") is True
    
    def test_validate_output_latex_no_commands(self):
        """Test rejection of LaTeX output without LaTeX commands."""
        output = "Plain text without any LaTeX commands"
        assert DocumentationPrompts.validate_output(output, "latex") is False
    
    def test_get_example_output_all_styles(self):
        """Test that example outputs exist for all styles."""
        styles = ["plain", "research", "latex"]
        for style in styles:
            example = DocumentationPrompts.get_example_output(style)
            assert len(example) > 0
    
    def test_max_code_tokens_constant(self):
        """Test that max tokens constant is set reasonably."""
        assert DocumentationPrompts.MAX_CODE_TOKENS > 0
        assert DocumentationPrompts.MAX_CODE_CHARS > 0
        # Roughly 1 token = 4 chars
        assert DocumentationPrompts.MAX_CODE_CHARS >= DocumentationPrompts.MAX_CODE_TOKENS * 3
