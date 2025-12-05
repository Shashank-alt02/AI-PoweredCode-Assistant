"""AI-Powered Code Assistant - Main Module

This module provides the core functionality for the AI-powered code assistant,
including code completion, bug detection, and automated refactoring.
"""

import os
import re
import ast
from typing import List, Dict, Optional, Tuple
import openai
from dataclasses import dataclass


@dataclass
class CodeSuggestion:
    """Represents a code suggestion from the AI."""
    code: str
    confidence: float
    explanation: str
    category: str


@dataclass
class BugReport:
    """Represents a detected bug or code issue."""
    line_number: int
    severity: str
    description: str
    fix_suggestion: Optional[str] = None


class AICodeAssistant:
    """Main class for AI-powered code assistance."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the AI Code Assistant.
        
        Args:
            api_key: OpenAI API key
            model: GPT model to use (default: gpt-4)
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
        
    def complete_code(self, code_context: str, max_suggestions: int = 3) -> List[CodeSuggestion]:
        """
        Generate intelligent code completions based on context.
        
        Args:
            code_context: The current code context
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of code suggestions
        """
        prompt = f"""Complete the following code with best practices:
        
{code_context}

Provide {max_suggestions} different completion suggestions."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert programming assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            suggestions = self._parse_suggestions(response.choices[0].message.content)
            return suggestions
            
        except Exception as e:
            print(f"Error generating code completion: {e}")
            return []
    
    def analyze_code(self, code: str) -> List[BugReport]:
        """
        Analyze code for potential bugs and issues.
        
        Args:
            code: The code to analyze
            
        Returns:
            List of bug reports
        """
        bugs = []
        
        # Static analysis using AST
        try:
            tree = ast.parse(code)
            bugs.extend(self._ast_analysis(tree))
        except SyntaxError as e:
            bugs.append(BugReport(
                line_number=e.lineno or 0,
                severity="HIGH",
                description=f"Syntax Error: {e.msg}"
            ))
        
        # AI-powered analysis
        bugs.extend(self._ai_bug_detection(code))
        
        return bugs
    
    def refactor(self, code: str, style: str = "clean_code") -> str:
        """
        Automatically refactor code to improve quality.
        
        Args:
            code: The code to refactor
            style: Refactoring style (clean_code, performance, readability)
            
        Returns:
            Refactored code
        """
        prompt = f"""Refactor this code following {style} principles:
        
{code}

Provide the refactored version with improvements."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a code refactoring expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            refactored_code = self._extract_code(response.choices[0].message.content)
            return refactored_code
            
        except Exception as e:
            print(f"Error refactoring code: {e}")
            return code
    
    def generate_documentation(self, code: str) -> str:
        """
        Generate documentation for the provided code.
        
        Args:
            code: The code to document
            
        Returns:
            Generated documentation
        """
        prompt = f"""Generate comprehensive documentation for this code:
        
{code}

Include:
- Overview
- Parameters/Arguments
- Return values
- Usage examples
- Edge cases"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating documentation: {e}")
            return ""
    
    def explain_code(self, code: str) -> str:
        """
        Explain what the code does in natural language.
        
        Args:
            code: The code to explain
            
        Returns:
            Natural language explanation
        """
        prompt = f"""Explain this code in simple terms:
        
{code}

Provide a clear, beginner-friendly explanation."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a patient coding instructor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error explaining code: {e}")
            return ""
    
    def _parse_suggestions(self, response_text: str) -> List[CodeSuggestion]:
        """Parse AI response into structured suggestions."""
        # Implementation would parse the response
        return []
    
    def _ast_analysis(self, tree: ast.AST) -> List[BugReport]:
        """Perform AST-based static analysis."""
        bugs = []
        # Check for common patterns
        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                bugs.append(BugReport(
                    line_number=node.lineno,
                    severity="MEDIUM",
                    description="Bare except clause - specify exception type",
                    fix_suggestion="except Exception as e:"
                ))
        return bugs
    
    def _ai_bug_detection(self, code: str) -> List[BugReport]:
        """Use AI to detect potential bugs."""
        prompt = f"""Analyze this code for bugs, security issues, and problems:
        
{code}

List any issues found with severity and line numbers."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a security and code quality expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response into BugReports
            # Implementation would extract structured data
            return []
            
        except Exception as e:
            print(f"Error in AI bug detection: {e}")
            return []
    
    def _extract_code(self, text: str) -> str:
        """Extract code blocks from AI response."""
        # Look for code blocks
        code_pattern = r'```(?:python)?\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        return matches[0] if matches else text


def main():
    """Example usage of the AI Code Assistant."""
    # Initialize assistant
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    assistant = AICodeAssistant(api_key=api_key)
    
    # Example: Code completion
    print("\n=== Code Completion ===")
    code_context = "def calculate_fibonacci(n):"
    suggestions = assistant.complete_code(code_context)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\nSuggestion {i}:")
        print(suggestion.code)
    
    # Example: Bug detection
    print("\n=== Bug Detection ===")
    buggy_code = """
def divide(a, b):
    return a / b

try:
    result = divide(10, 0)
except:
    pass
"""
    bugs = assistant.analyze_code(buggy_code)
    for bug in bugs:
        print(f"Line {bug.line_number}: [{bug.severity}] {bug.description}")
    
    # Example: Code refactoring
    print("\n=== Code Refactoring ===")
    messy_code = """
def calc(x,y,z):
    a=x+y
    b=a*z
    return b
"""
    refactored = assistant.refactor(messy_code)
    print("Refactored code:")
    print(refactored)
    
    # Example: Code explanation
    print("\n=== Code Explanation ===")
    complex_code = "lambda x: reduce(lambda a,b: a*b, range(1, x+1))"
    explanation = assistant.explain_code(complex_code)
    print(explanation)


if __name__ == "__main__":
    main()
