from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Request Models
class AnalyzeCodeRequest(BaseModel):
    """Code analysis request."""
    code: str = Field(..., description="Code to analyze")
    language: str = Field(default="python", description="Programming language")
    include_suggestions: bool = Field(default=True, description="Include improvement suggestions")

class GenerateCodeRequest(BaseModel):
    """Code generation request."""
    requirements: str = Field(..., description="Code requirements")
    language: str = Field(default="python", description="Programming language")
    framework: Optional[str] = Field(None, description="Framework (e.g., React, FastAPI)")
    context: Optional[str] = Field(None, description="Additional context")

class CodeReviewRequest(BaseModel):
    """Code review request."""
    code: str = Field(..., description="Code to review")
    language: str = Field(default="python", description="Programming language")
    focus_areas: Optional[List[str]] = Field(None, description="Areas to focus on (performance, security, readability)")

class ChatRequest(BaseModel):
    """Chat request."""
    message: str = Field(..., description="Message for the agent")
    context: Optional[str] = Field(None, description="Additional context")
    conversation_history: Optional[List[dict]] = Field(None, description="Previous messages")

# Response Models
class AnalysisResult(BaseModel):
    """Code analysis result."""
    issues: List[dict] = Field(default=[], description="Found issues")
    suggestions: List[dict] = Field(default=[], description="Improvement suggestions")
    severity: str = Field(description="Overall severity: critical, high, medium, low")
    analysis_time: float = Field(description="Analysis time in seconds")

class GeneratedCode(BaseModel):
    """Generated code response."""
    code: str = Field(description="Generated code")
    language: str = Field(description="Programming language")
    explanation: str = Field(description="Explanation of generated code")
    generation_time: float = Field(description="Generation time in seconds")

class ReviewResult(BaseModel):
    """Code review result."""
    overall_score: float = Field(description="Overall score 0-100")
    issues: List[dict] = Field(default=[], description="Found issues")
    improvements: List[dict] = Field(default=[], description="Suggested improvements")
    summary: str = Field(description="Review summary")
    review_time: float = Field(description="Review time in seconds")

class ChatResponse(BaseModel):
    """Chat response."""
    response: str = Field(description="Agent response")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model: str = Field(description="Model used")
    tokens_used: dict = Field(description="Token usage")

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="Agent status")
    agent_name: str = Field(description="Agent name")
    specializations: List[str] = Field(description="Agent specializations")
    ollama_connected: bool = Field(description="Ollama connection status")
    model: str = Field(description="Current model")
