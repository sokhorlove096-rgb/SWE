from fastapi import APIRouter, HTTPException, status
from loguru import logger
from app.models import (
    AnalyzeCodeRequest, AnalysisResult,
    GenerateCodeRequest, GeneratedCode,
    CodeReviewRequest, ReviewResult,
    ChatRequest, ChatResponse,
    HealthResponse
)
from app.agent import SWEAgent
from app.ollama_client import OllamaClient
from config import settings
from datetime import datetime

router = APIRouter(prefix="", tags=["agent"])

# Initialize Ollama client and agent
ollama_client = OllamaClient(
    base_url=settings.ollama_base_url,
    model=settings.ollama_model,
    max_tokens=settings.max_tokens,
    temperature=settings.temperature
)

swe_agent = SWEAgent(
    ollama_client=ollama_client,
    name=settings.agent_name,
    specializations=settings.agent_specializations
)

@router.get("/health", response_model=dict, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    """
    try:
        ollama_connected = await ollama_client.check_connection()
        
        return {
            "status": "healthy" if ollama_connected else "degraded",
            "agent_name": swe_agent.name,
            "specializations": swe_agent.specializations,
            "ollama_connected": ollama_connected,
            "model": settings.ollama_model,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )

@router.post("/analyze", response_model=dict, status_code=status.HTTP_200_OK)
async def analyze_code(request: AnalyzeCodeRequest):
    """
    Analyze code for issues and improvements.
    
    - **code**: Code to analyze
    - **language**: Programming language (default: python)
    - **include_suggestions**: Include improvement suggestions (default: true)
    """
    try:
        logger.info(f"Analyzing code: {len(request.code)} chars, language: {request.language}")
        
        result = await swe_agent.analyze_code(
            code=request.code,
            language=request.language,
            include_suggestions=request.include_suggestions
        )
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Code analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/generate", response_model=dict, status_code=status.HTTP_200_OK)
async def generate_code(request: GenerateCodeRequest):
    """
    Generate code based on requirements.
    
    - **requirements**: Code requirements
    - **language**: Programming language (default: python)
    - **framework**: Framework (e.g., React, FastAPI)
    - **context**: Additional context
    """
    try:
        logger.info(f"Generating code: {request.language}, framework: {request.framework}")
        
        result = await swe_agent.generate_code(
            requirements=request.requirements,
            language=request.language,
            framework=request.framework,
            context=request.context
        )
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )

@router.post("/review", response_model=dict, status_code=status.HTTP_200_OK)
async def review_code(request: CodeReviewRequest):
    """
    Review code quality.
    
    - **code**: Code to review
    - **language**: Programming language (default: python)
    - **focus_areas**: Areas to focus on (performance, security, readability)
    """
    try:
        logger.info(f"Reviewing code: {len(request.code)} chars, language: {request.language}")
        
        result = await swe_agent.review_code(
            code=request.code,
            language=request.language,
            focus_areas=request.focus_areas
        )
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Code review error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Review failed: {str(e)}"
        )

@router.post("/chat", response_model=dict, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest):
    """
    Chat with the SWE agent.
    
    - **message**: Message for the agent
    - **context**: Additional context
    - **conversation_history**: Previous messages for context
    """
    try:
        logger.info(f"Chat message: {request.message[:50]}...")
        
        result = await swe_agent.chat(
            message=request.message,
            context=request.context,
            conversation_history=request.conversation_history
        )
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )
