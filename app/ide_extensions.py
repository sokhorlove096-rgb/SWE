"""IDE Extension configurations for VS Code, Cursor, OpenCode, etc."""

import json
import os
from pathlib import Path
from loguru import logger
from typing import Dict, Any


class IDEExtensionManager:
    """Manages IDE extension configurations."""

    @staticmethod
    def generate_vscode_extension_config(lsp_host: str = "127.0.0.1", lsp_port: int = 8080) -> Dict[str, Any]:
        """
        Generate VS Code extension configuration.
        
        Args:
            lsp_host: LSP server host
            lsp_port: LSP server port
            
        Returns:
            VS Code extension config
        """
        return {
            "name": "swe-agent",
            "displayName": "SWE Agent - AI-Powered Code Assistant",
            "description": "FastAPI-based Software Engineer agent with Ollama integration",
            "version": "1.0.0",
            "publisher": "swe-agent",
            "engines": {
                "vscode": "^1.60.0"
            },
            "categories": [
                "Programming Languages",
                "Linters",
                "Debuggers",
                "AI"
            ],
            "keywords": [
                "react",
                "python",
                "code-analysis",
                "code-generation",
                "ai",
                "ollama"
            ],
            "contributes": {
                "languages": [
                    {
                        "id": "python",
                        "extensions": [".py"]
                    },
                    {
                        "id": "javascript",
                        "extensions": [".js", ".jsx"]
                    },
                    {
                        "id": "typescript",
                        "extensions": [".ts", ".tsx"]
                    }
                ],
                "commands": [
                    {
                        "command": "swe-agent.analyze",
                        "title": "SWE: Analyze Code",
                        "category": "SWE Agent"
                    },
                    {
                        "command": "swe-agent.generate",
                        "title": "SWE: Generate Code",
                        "category": "SWE Agent"
                    },
                    {
                        "command": "swe-agent.review",
                        "title": "SWE: Review Code",
                        "category": "SWE Agent"
                    },
                    {
                        "command": "swe-agent.chat",
                        "title": "SWE: Open Chat",
                        "category": "SWE Agent"
                    }
                ],
                "keybindings": [
                    {
                        "command": "swe-agent.analyze",
                        "key": "ctrl+shift+a",
                        "mac": "cmd+shift+a",
                        "when": "editorTextFocus"
                    },
                    {
                        "command": "swe-agent.generate",
                        "key": "ctrl+shift+g",
                        "mac": "cmd+shift+g",
                        "when": "editorTextFocus"
                    },
                    {
                        "command": "swe-agent.review",
                        "key": "ctrl+shift+r",
                        "mac": "cmd+shift+r",
                        "when": "editorTextFocus"
                    },
                    {
                        "command": "swe-agent.chat",
                        "key": "ctrl+shift+c",
                        "mac": "cmd+shift+c"
                    }
                ],
                "configuration": {
                    "title": "SWE Agent Configuration",
                    "properties": {
                        "swe-agent.lspHost": {
                            "type": "string",
                            "default": lsp_host,
                            "description": "LSP server host address"
                        },
                        "swe-agent.lspPort": {
                            "type": "number",
                            "default": lsp_port,
                            "description": "LSP server port"
                        },
                        "swe-agent.apiHost": {
                            "type": "string",
                            "default": "http://localhost:8000",
                            "description": "SWE Agent API host"
                        },
                        "swe-agent.autoAnalyze": {
                            "type": "boolean",
                            "default": True,
                            "description": "Auto-analyze code on save"
                        },
                        "swe-agent.maxTokens": {
                            "type": "number",
                            "default": 4096,
                            "description": "Maximum tokens for AI responses"
                        }
                    }
                }
            }
        }

    @staticmethod
    def generate_cursor_extension_config(lsp_host: str = "127.0.0.1", lsp_port: int = 8080) -> Dict[str, Any]:
        """
        Generate Cursor IDE extension configuration.
        
        Args:
            lsp_host: LSP server host
            lsp_port: LSP server port
            
        Returns:
            Cursor extension config
        """
        config = IDEExtensionManager.generate_vscode_extension_config(lsp_host, lsp_port)
        config["name"] = "swe-agent-cursor"
        config["displayName"] = "SWE Agent - Cursor Edition"
        config["description"] = "AI-Powered Code Assistant for Cursor IDE"
        config["engines"]["cursor"] = "^0.1.0"
        return config

    @staticmethod
    def generate_nvim_config() -> str:
        """
        Generate Neovim LSP configuration.
        
        Returns:
            Neovim Lua configuration
        """
        return '''-- SWE Agent LSP Configuration for Neovim

local nvim_lsp = require('lspconfig')

nvim_lsp.swe_agent.setup {
  cmd = { "python", "-m", "app.lsp_server" },
  filetypes = { "python", "javascript", "typescript", "jsx", "tsx" },
  root_dir = nvim_lsp.util.root_pattern(".git", "pyproject.toml", "package.json"),
  settings = {
    lspHost = "127.0.0.1",
    lspPort = 8080,
    apiHost = "http://localhost:8000",
    autoAnalyze = true,
    maxTokens = 4096
  }
}
'''

    @staticmethod
    def generate_sublime_config() -> Dict[str, Any]:
        """
        Generate Sublime Text LSP client configuration.
        
        Returns:
            Sublime LSP configuration
        """
        return {
            "clients": {
                "swe_agent": {
                    "enabled": True,
                    "command": ["python", "-m", "app.lsp_server"],
                    "languages": [
                        {
                            "languageId": "python",
                            "scopes": ["source.python"],
                            "syntaxes": ["Packages/Python/Python.sublime-syntax"]
                        },
                        {
                            "languageId": "javascript",
                            "scopes": ["source.js"],
                            "syntaxes": ["Packages/JavaScript/JavaScript.sublime-syntax"]
                        },
                        {
                            "languageId": "typescript",
                            "scopes": ["source.ts"],
                            "syntaxes": ["Packages/TypeScript/TypeScript.sublime-syntax"]
                        }
                    ],
                    "settings": {
                        "lsp_host": "127.0.0.1",
                        "lsp_port": 8080,
                        "api_host": "http://localhost:8000"
                    }
                }
            }
        }

    @staticmethod
    def generate_vim_config() -> str:
        """
        Generate Vim/Neovim coc.nvim configuration.
        
        Returns:
            Vim configuration
        """
        return '''" SWE Agent LSP Configuration for Vim (coc.nvim)

let g:coc_global_extensions = ['coc-swe-agent']

if has('nvim')
  call coc#config('languageserver', {
    \ 'swe-agent': {
    \   'command': 'python',
    \   'args': ['-m', 'app.lsp_server'],
    \   'filetypes': ['python', 'javascript', 'typescript', 'jsx', 'tsx'],
    \   'initializationOptions': {
    \     'lspHost': '127.0.0.1',
    \     'lspPort': 8080,
    \     'apiHost': 'http://localhost:8000'
    \   }
    \ }
  \ })
endif
'''

    @staticmethod
    def generate_emacs_config() -> str:
        """
        Generate Emacs lsp-mode configuration.
        
        Returns:
            Emacs Lisp configuration
        """
        return '''(require 'lsp-mode)

(lsp-register-client
  (make-lsp-client
    :new-connection (lsp-stdio-connection
      '("python" "-m" "app.lsp_server"))
    :major-modes '(python-mode js-mode typescript-mode)
    :server-id 'swe-agent
    :initialization-options
    '((lspHost . "127.0.0.1")
      (lspPort . 8080)
      (apiHost . "http://localhost:8000")))
  'swe-agent)

(add-hook 'python-mode-hook #'lsp)
(add-hook 'js-mode-hook #'lsp)
(add-hook 'typescript-mode-hook #'lsp)
'''

    @staticmethod
    def save_vscode_extension(output_dir: str = "./ide-extensions/vscode"):
        """
        Save VS Code extension files.
        
        Args:
            output_dir: Output directory
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        config = IDEExtensionManager.generate_vscode_extension_config()
        
        with open(os.path.join(output_dir, "package.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"VS Code extension config saved to {output_dir}")

    @staticmethod
    def save_all_extensions(output_dir: str = "./ide-extensions"):
        """
        Save all IDE extension configurations.
        
        Args:
            output_dir: Output directory
        """
        # VS Code
        vscode_dir = os.path.join(output_dir, "vscode")
        Path(vscode_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(vscode_dir, "package.json"), "w") as f:
            json.dump(IDEExtensionManager.generate_vscode_extension_config(), f, indent=2)
        
        # Cursor
        cursor_dir = os.path.join(output_dir, "cursor")
        Path(cursor_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(cursor_dir, "package.json"), "w") as f:
            json.dump(IDEExtensionManager.generate_cursor_extension_config(), f, indent=2)
        
        # Neovim
        nvim_dir = os.path.join(output_dir, "neovim")
        Path(nvim_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(nvim_dir, "lspconfig.lua"), "w") as f:
            f.write(IDEExtensionManager.generate_nvim_config())
        
        # Sublime
        sublime_dir = os.path.join(output_dir, "sublime")
        Path(sublime_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(sublime_dir, "LSP.json"), "w") as f:
            json.dump(IDEExtensionManager.generate_sublime_config(), f, indent=2)
        
        # Vim/Neovim
        vim_dir = os.path.join(output_dir, "vim")
        Path(vim_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(vim_dir, "coc-config.vim"), "w") as f:
            f.write(IDEExtensionManager.generate_vim_config())
        
        # Emacs
        emacs_dir = os.path.join(output_dir, "emacs")
        Path(emacs_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(emacs_dir, "lsp-config.el"), "w") as f:
            f.write(IDEExtensionManager.generate_emacs_config())
        
        logger.info(f"All IDE extension configurations saved to {output_dir}")
