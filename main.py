#!/usr/bin/env python3
"""
SWE Agent Platform - FastAPI Server with OpenAI-Compatible API

A FastAPI-based Software Engineer agent specialized in React and Python,
powered by Ollama with OpenAI-compatible endpoints for IDE integration.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from config import settings
from app.openai_routes import router as openai_router

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)

# Create FastAPI app
app = FastAPI(
    title="SWE Agent Platform - OpenAI Compatible",
    description="A FastAPI-based Software Engineer agent with OpenAI-compatible API endpoints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include OpenAI-compatible routes
app.include_router(openai_router)

@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("="*60)
    logger.info(f"Starting {settings.agent_name} Agent Platform - OpenAI Compatible")
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Model: {settings.ollama_model}")
    logger.info(f"Specializations: {', '.join(settings.get_specializations_list())}")
    logger.info(f"API Base URL: http://{settings.fast_api_host}:{settings.fast_api_port}")
    logger.info("="*60)

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info(f"Shutting down {settings.agent_name} Agent Platform")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.agent_name} Agent Platform - OpenAI Compatible API",
        "api_base": f"http://{settings.fast_api_host}:{settings.fast_api_port}",
        "model": settings.ollama_model,
        "docs": "/docs",
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "completions": "/v1/completions",
            "models": "/v1/models",
            "health": "/v1/health"
        },
        "example_clients": {
            "python": "pip install openai && OpenAI(api_key='fake', base_url='http://localhost:8000/v1')",
            "curl": "curl -X POST http://localhost:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{...}'",
            "openai_cli": "OPENAI_API_KEY=fake OPENAI_API_BASE=http://localhost:8000/v1 openai ..."
        }
    }

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.fast_api_host}:{settings.fast_api_port}")
    uvicorn.run(
        "main:app",
        host=settings.fast_api_host,
        port=settings.fast_api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
