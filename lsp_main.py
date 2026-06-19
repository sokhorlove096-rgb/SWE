#!/usr/bin/env python3
"""
SWE Agent LSP Server

Language Server Protocol implementation for IDE integration.
Supports VS Code, Cursor, Neovim, Sublime, Vim, Emacs, and more.
"""

import sys
from loguru import logger
from config import settings
from app.lsp_server import SWELanguageServer

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)

if __name__ == "__main__":
    logger.info("Initializing SWE Agent LSP Server...")
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Model: {settings.ollama_model}")
    logger.info(f"Specializations: {', '.join(settings.agent_specializations)}")
    
    try:
        lsp_server = SWELanguageServer()
        lsp_server.start(host="127.0.0.1", port=8080)
    except KeyboardInterrupt:
        logger.info("LSP Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"LSP Server error: {e}")
        sys.exit(1)
