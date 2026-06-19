#!/usr/bin/env python3
"""
SWE Agent Platform - FastAPI Server

A FastAPI-based Software Engineer agent specialized in React and Python,
powered by Ollama.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from config import settings
from app.routes import router

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)

# Create FastAPI app
app = FastAPI(
    title="SWE Agent Platform",
    description="A FastAPI-based Software Engineer agent specialized in React and Python",
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

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("="*50)
    logger.info(f"Starting {settings.agent_name} Agent Platform")
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Model: {settings.ollama_model}")
    logger.info(f"Specializations: {', '.join(settings.agent_specializations)}")
    logger.info("="*50)

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info(f"Shutting down {settings.agent_name} Agent Platform")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.agent_name} Agent Platform",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "/health"
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
