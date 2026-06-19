#!/usr/bin/env python3
"""
Generate IDE extension configurations.

This script generates configuration files for various IDEs to integrate with the SWE Agent.
"""

import sys
from loguru import logger
from app.ide_extensions import IDEExtensionManager

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

if __name__ == "__main__":
    logger.info("Generating IDE extension configurations...")
    
    try:
        IDEExtensionManager.save_all_extensions(output_dir="./ide-extensions")
        logger.info("✓ IDE extension configurations generated successfully!")
        logger.info("Available configurations:")
        logger.info("  - VS Code: ./ide-extensions/vscode/package.json")
        logger.info("  - Cursor: ./ide-extensions/cursor/package.json")
        logger.info("  - Neovim: ./ide-extensions/neovim/lspconfig.lua")
        logger.info("  - Sublime: ./ide-extensions/sublime/LSP.json")
        logger.info("  - Vim/Neovim: ./ide-extensions/vim/coc-config.vim")
        logger.info("  - Emacs: ./ide-extensions/emacs/lsp-config.el")
    except Exception as e:
        logger.error(f"Error generating IDE configurations: {e}")
        sys.exit(1)
