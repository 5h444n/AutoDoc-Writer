"""AI persona prompts for different documentation styles.

This module provides structured prompts for generating documentation
in various styles using Google Gemini AI.
"""

from typing import Dict, Optional


class DocumentationPrompts:
    """Centralized documentation generation prompts."""
    
    # Maximum token limit for code input (to prevent API errors)
    MAX_CODE_TOKENS = 2000
    MAX_CODE_CHARS = 8000  # Approximate: 1 token ≈ 4 chars
    
    PLAIN_ENGLISH = """You are a friendly, experienced software mentor explaining code to a junior developer.

Your goal is to make complex code understandable and accessible.

Guidelines:
1. Use simple, conversational language
2. Explain technical concepts in everyday terms
3. Use analogies when helpful
4. Focus on "what" and "why" rather than just "how"
5. Break down complex logic into digestible parts
6. Highlight important patterns or best practices
7. Point out potential issues or areas for improvement
8. Use bullet points and clear structure

Format:
- Start with a brief overview (2-3 sentences)
- Main explanation in clear paragraphs
- Use code examples if clarifying
- End with a summary of key points

Tone: Friendly, encouraging, educational"""

    RESEARCH_THESIS = """You are a formal academic researcher documenting software for a research paper or thesis.

Your goal is to provide precise, scholarly documentation suitable for academic publication.

Guidelines:
1. Use passive voice and formal academic language
2. Provide rigorous technical precision
3. Include algorithmic complexity analysis where relevant
4. Reference theoretical foundations or design patterns
5. Use proper technical terminology
6. Structure with clear sections and subsections
7. Focus on methodology and rationale
8. Cite relevant computer science concepts

Format:
- Abstract: Brief summary of the code's purpose and approach
- Introduction: Context and problem statement
- Methodology: Detailed technical explanation
- Implementation: Specific design decisions
- Complexity Analysis: Time and space complexity
- Conclusion: Summary and potential improvements

Tone: Formal, objective, scholarly"""

    LATEX = """You are a LaTeX specialist converting code documentation into publication-ready LaTeX format.

Your goal is to produce properly formatted LaTeX suitable for academic journals, theses, or technical reports.

Guidelines:
1. Use proper LaTeX syntax and environments
2. Format code with \\begin{lstlisting} or \\begin{verbatim}
3. Use \\section, \\subsection for structure
4. Escape special LaTeX characters: \\, {, }, &, %, #, _, ~, ^
5. Use math mode for algorithms: $O(n)$, $\\theta(n\\log n)$
6. Include proper spacing and formatting
7. Use \\texttt{} for inline code
8. Use \\emph{} for emphasis

Format:
\\section{Code Analysis}
\\subsection{Overview}
[Description]

\\subsection{Implementation}
\\begin{lstlisting}[language=Python]
[Code examples if needed]
\\end{lstlisting}

\\subsection{Complexity Analysis}
Time complexity: $O(n)$

\\subsection{Key Features}
\\begin{itemize}
    \\item Feature 1
    \\item Feature 2
\\end{itemize}

Tone: Technical, precise, formal"""

    @staticmethod
    def get_prompt(style: str) -> str:
        """Get the system prompt for a documentation style.
        
        Args:
            style: Documentation style (plain, research, latex)
            
        Returns:
            System prompt string
            
        Raises:
            ValueError: If style is invalid
        """
        prompts = {
            "plain": DocumentationPrompts.PLAIN_ENGLISH,
            "research": DocumentationPrompts.RESEARCH_THESIS,
            "latex": DocumentationPrompts.LATEX,
        }
        
        if style not in prompts:
            raise ValueError(f"Invalid style: {style}. Must be one of: {', '.join(prompts.keys())}")
        
        return prompts[style]
    
    @staticmethod
    def truncate_code(code: str, max_chars: Optional[int] = None) -> tuple[str, bool]:
        """Truncate code if it exceeds token limits.
        
        Args:
            code: Source code to potentially truncate
            max_chars: Maximum characters (defaults to MAX_CODE_CHARS)
            
        Returns:
            Tuple of (truncated_code, was_truncated)
        """
        max_chars = max_chars or DocumentationPrompts.MAX_CODE_CHARS
        
        if len(code) <= max_chars:
            return code, False
        
        # Truncate with a message
        truncated = code[:max_chars]
        truncated += "\n\n[... Code truncated due to length ...]"
        return truncated, True
    
    @staticmethod
    def build_user_prompt(code: str, style: str, filename: Optional[str] = None) -> str:
        """Build the user prompt with code.
        
        Args:
            code: Source code to document
            style: Documentation style
            filename: Optional filename for context
            
        Returns:
            Formatted user prompt
        """
        # Truncate if necessary
        code, was_truncated = DocumentationPrompts.truncate_code(code)
        
        filename_context = f"File: {filename}\n\n" if filename else ""
        truncation_note = "\n\nNote: Code was truncated to fit within token limits." if was_truncated else ""
        
        prompt = f"""{filename_context}Please analyze and document the following code in {style} style:

```
{code}
```{truncation_note}
"""
        return prompt
    
    @staticmethod
    def validate_output(output: str, style: str) -> bool:
        """Validate AI output based on style requirements.
        
        Args:
            output: Generated documentation
            style: Documentation style
            
        Returns:
            True if output appears valid
        """
        if not output or len(output) < 50:
            return False
        
        # Style-specific validation
        if style == "latex":
            # Should contain LaTeX commands
            has_latex = any(cmd in output for cmd in ["\\section", "\\subsection", "\\begin", "\\end"])
            return has_latex
        
        elif style == "research":
            # Should have formal structure
            has_sections = any(word in output.lower() for word in ["abstract", "introduction", "methodology", "conclusion"])
            return has_sections
        
        elif style == "plain":
            # Should be conversational
            # Just check it's not too short and has some structure
            return len(output) > 100
        
        return True
    
    @staticmethod
    def get_example_output(style: str) -> str:
        """Get example output for a style (for testing/documentation).
        
        Args:
            style: Documentation style
            
        Returns:
            Example documentation string
        """
        examples = {
            "plain": """## Code Overview
This function handles user authentication by checking credentials against the database.

**What it does:**
- Takes a username and password
- Looks up the user in the database
- Verifies the password hash
- Returns a session token if successful

**Key Points:**
• Uses bcrypt for secure password hashing
• Implements rate limiting to prevent brute force attacks
• Returns clear error messages for debugging""",
            
            "research": """**Abstract**
This module implements a secure authentication mechanism utilizing bcrypt hashing and session-based tokens.

**Methodology**
The authentication process employs a three-stage verification protocol:
1. User credential retrieval from persistent storage
2. Cryptographic hash validation using bcrypt
3. Session token generation and assignment

**Complexity Analysis**
Time Complexity: O(1) for database lookup, O(n) for bcrypt verification
Space Complexity: O(1)""",
            
            "latex": """\\section{Authentication Module}

\\subsection{Overview}
The authentication system implements secure user verification using bcrypt hashing.

\\subsection{Algorithm}
\\begin{enumerate}
    \\item Retrieve user credentials from database
    \\item Verify password hash using bcrypt
    \\item Generate session token
\\end{enumerate}

\\subsection{Complexity}
Time complexity: $O(1)$ for lookup, $O(n)$ for hash verification."""
        }
        
        return examples.get(style, "")
