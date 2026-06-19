"""OpenAI-compatible API for SWE Agent.

Provides OpenAI-like API endpoints for integration with any IDE,
LLM client, or application that supports OpenAI API format.
"""

from fastapi import APIRouter, HTTPException, status
from loguru import logger
from datetime import datetime
from typing import List, Optional
import uuid

from app.agent import SWEAgent
from app.ollama_client import OllamaClient
from config import settings

router = APIRouter(prefix="/v1", tags=["openai-compatible"])

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
    specializations=settings.get_specializations_list()
)

# OpenAI-compatible Models
class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

@router.get("/models")
async def list_models():
    """
    List available models (OpenAI-compatible).
    """
    return {
        "object": "list",
        "data": [
            {
                "id": settings.ollama_model,
                "object": "model",
                "created": int(datetime.utcnow().timestamp()),
                "owned_by": "swe-agent",
                "permission": [],
                "root": settings.ollama_model,
                "parent": None
            }
        ]
    }

@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """
    Get model details (OpenAI-compatible).
    """
    if model_id != settings.ollama_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_id} not found"
        )
    
    return {
        "id": settings.ollama_model,
        "object": "model",
        "created": int(datetime.utcnow().timestamp()),
        "owned_by": "swe-agent",
        "permission": [],
        "root": settings.ollama_model,
        "parent": None
    }

@router.post("/chat/completions")
async def chat_completions(request: dict):
    """
    Chat completions endpoint (OpenAI-compatible).
    
    Request format:
    {
        "model": "RoandaiG-4-31IT:latest",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"}
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": false
    }
    """
    try:
        model = request.get("model", settings.ollama_model)
        messages = request.get("messages", [])
        temperature = request.get("temperature", settings.temperature)
        max_tokens = request.get("max_tokens", settings.max_tokens)
        stream = request.get("stream", False)
        
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="messages field is required"
            )
        
        # Get the last user message as the primary prompt
        user_message = None
        system_message = None
        
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content")
            elif msg.get("role") == "user":
                user_message = msg.get("content")
        
        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one user message is required"
            )
        
        # Get response from agent
        result = await swe_agent.ollama_client.chat(
            messages=messages,
            system_prompt=system_message
        )
        
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error")
            )
        
        # Return OpenAI-compatible response
        response_text = result.get("text", "")
        tokens = result.get("tokens", {})
        
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(datetime.utcnow().timestamp()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": tokens.get("prompt_eval_count", 0),
                "completion_tokens": tokens.get("eval_count", 0),
                "total_tokens": tokens.get("prompt_eval_count", 0) + tokens.get("eval_count", 0)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat completions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat completions failed: {str(e)}"
        )

@router.post("/completions")
async def completions(request: dict):
    """
    Text completions endpoint (OpenAI-compatible).
    
    Request format:
    {
        "model": "RoandaiG-4-31IT:latest",
        "prompt": "def hello():",
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": false
    }
    """
    try:
        model = request.get("model", settings.ollama_model)
        prompt = request.get("prompt", "")
        temperature = request.get("temperature", settings.temperature)
        max_tokens = request.get("max_tokens", settings.max_tokens)
        
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="prompt field is required"
            )
        
        # Get response from agent
        result = await swe_agent.ollama_client.generate(
            prompt=prompt
        )
        
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error")
            )
        
        # Return OpenAI-compatible response
        response_text = result.get("text", "")
        tokens = result.get("tokens", {})
        
        return {
            "id": f"cmpl-{uuid.uuid4()}",
            "object": "text_completion",
            "created": int(datetime.utcnow().timestamp()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "text": response_text,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": tokens.get("prompt_eval_count", 0),
                "completion_tokens": tokens.get("eval_count", 0),
                "total_tokens": tokens.get("prompt_eval_count", 0) + tokens.get("eval_count", 0)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Completions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Completions failed: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    try:
        ollama_connected = await ollama_client.check_connection()
        
        return {
            "status": "healthy" if ollama_connected else "degraded",
            "model": settings.ollama_model,
            "ollama_connected": ollama_connected,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )
