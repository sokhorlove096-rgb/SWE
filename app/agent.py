from typing import Optional, List, Dict, Any
from loguru import logger
from app.ollama_client import OllamaClient
import time

class SWEAgent:
    """Software Engineer Agent specialized in React and Python."""
    
    SYSTEM_PROMPTS = {
        "analyzer": """You are an expert software engineer specializing in React (React, React Native, Next.js) and Python.
        When analyzing code:
        - Identify bugs and potential issues
        - Check for performance problems
        - Review security concerns
        - Suggest best practices
        - Provide actionable improvements
        
        Format your analysis as JSON with keys: issues, suggestions, severity.""",
        
        "generator": """You are an expert software engineer specializing in React (React, React Native, Next.js) and Python.
        When generating code:
        - Follow best practices and coding standards
        - Include proper error handling
        - Add meaningful comments
        - Use modern language features
        - Ensure code is production-ready
        
        Provide clean, well-structured code.""",
        
        "reviewer": """You are an expert code reviewer specializing in React (React, React Native, Next.js) and Python.
        When reviewing code:
        - Check code quality and readability
        - Verify best practices are followed
        - Identify potential bugs
        - Suggest performance improvements
        - Review security
        
        Format your review as JSON with keys: overall_score, issues, improvements, summary.""",
        
        "general": """You are an expert Software Engineer (SWE) specializing in React (all variants) and Python.
        You provide:
        - Code reviews and analysis
        - Architecture design assistance
        - Best practice guidance
        - Debugging help
        - Development tips and tricks
        
        Be concise, practical, and focused on solving real problems."""
    }
    
    def __init__(
        self,
        ollama_client: OllamaClient,
        name: str = "SWE",
        specializations: List[str] = None
    ):
        """
        Initialize SWE Agent.
        
        Args:
            ollama_client: OllamaClient instance
            name: Agent name
            specializations: List of specializations
        """
        self.ollama_client = ollama_client
        self.name = name
        self.specializations = specializations or ["React", "React Native", "Next.js", "Python"]
        logger.info(f"Initialized {self.name} agent with specializations: {self.specializations}")
    
    async def analyze_code(
        self,
        code: str,
        language: str = "python",
        include_suggestions: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze code for issues and improvements.
        
        Args:
            code: Code to analyze
            language: Programming language
            include_suggestions: Whether to include suggestions
            
        Returns:
            Analysis result
        """
        logger.info(f"Analyzing {language} code")
        start_time = time.time()
        
        prompt = f"""Analyze the following {language} code for issues and improvements:
        
```{language}
{code}
```

{"Include suggestions for improvement." if include_suggestions else "Only list critical issues."}
        
Provide a structured analysis."""
        
        result = await self.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPTS["analyzer"]
        )
        
        analysis_time = time.time() - start_time
        
        return {
            "analysis": result.get("text", ""),
            "language": language,
            "analysis_time": analysis_time,
            "tokens": result.get("tokens", {}),
            "error": result.get("error")
        }
    
    async def generate_code(
        self,
        requirements: str,
        language: str = "python",
        framework: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate code based on requirements.
        
        Args:
            requirements: Code requirements
            language: Programming language
            framework: Optional framework
            context: Additional context
            
        Returns:
            Generated code
        """
        logger.info(f"Generating {language} code for: {requirements[:50]}...")
        start_time = time.time()
        
        framework_mention = f" using {framework}" if framework else ""
        context_mention = f"\nContext: {context}" if context else ""
        
        prompt = f"""Generate production-ready {language} code{framework_mention}.

Requirements:
{requirements}{context_mention}

Provide only the code with minimal comments."""
        
        result = await self.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPTS["generator"]
        )
        
        generation_time = time.time() - start_time
        
        return {
            "code": result.get("text", ""),
            "language": language,
            "framework": framework,
            "generation_time": generation_time,
            "tokens": result.get("tokens", {}),
            "error": result.get("error")
        }
    
    async def review_code(
        self,
        code: str,
        language: str = "python",
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Review code quality.
        
        Args:
            code: Code to review
            language: Programming language
            focus_areas: Areas to focus on
            
        Returns:
            Review result
        """
        logger.info(f"Reviewing {language} code")
        start_time = time.time()
        
        focus = ""
        if focus_areas:
            focus = f"\nFocus on: {', '.join(focus_areas)}"
        
        prompt = f"""Review the following {language} code:

```{language}
{code}
```
{focus}

Provide a detailed review with:
- Overall score (0-100)
- List of issues
- Improvement suggestions
- Summary"""
        
        result = await self.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPTS["reviewer"]
        )
        
        review_time = time.time() - start_time
        
        return {
            "review": result.get("text", ""),
            "language": language,
            "focus_areas": focus_areas,
            "review_time": review_time,
            "tokens": result.get("tokens", {}),
            "error": result.get("error")
        }
    
    async def chat(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[dict]] = None
    ) -> Dict[str, Any]:
        """
        Chat with the agent.
        
        Args:
            message: User message
            context: Additional context
            conversation_history: Previous messages
            
        Returns:
            Agent response
        """
        logger.info(f"Chat message: {message[:50]}...")
        start_time = time.time()
        
        # Build message history
        messages = conversation_history or []
        
        # Add context if provided
        if context:
            messages.append({
                "role": "user",
                "content": f"Context: {context}"
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        result = await self.ollama_client.chat(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPTS["general"]
        )
        
        response_time = time.time() - start_time
        
        return {
            "response": result.get("text", ""),
            "response_time": response_time,
            "tokens": result.get("tokens", {}),
            "error": result.get("error")
        }
