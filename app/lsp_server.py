"""LSP (Language Server Protocol) Server implementation for SWE Agent."""

from pygls.server import LanguageServer
from pygls.lsp.methods import (
    COMPLETION,
    HOVER,
    DEFINITION,
    REFERENCES,
    CODE_ACTION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    INITIALIZE,
)
from pygls.lsp.types import (
    CompletionItem,
    CompletionItemKind,
    Hover,
    MarkupContent,
    MarkupKind,
    Location,
    Range,
    Position,
    CodeAction,
    CodeActionKind,
    Diagnostic,
    DiagnosticSeverity,
)
from loguru import logger
import asyncio
from typing import Optional, List
from app.agent import SWEAgent
from app.ollama_client import OllamaClient
from config import settings


class SWELanguageServer:
    """Language Server Protocol (LSP) implementation for SWE Agent."""

    def __init__(self):
        """Initialize LSP server."""
        self.server = LanguageServer("swe-agent", "v1.0")
        self.document_cache = {}
        
        # Initialize Ollama and Agent
        self.ollama_client = OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature
        )
        
        self.swe_agent = SWEAgent(
            ollama_client=self.ollama_client,
            name=settings.agent_name,
            specializations=settings.agent_specializations
        )
        
        self._setup_handlers()
        logger.info("SWE Language Server initialized")

    def _setup_handlers(self):
        """Setup LSP message handlers."""
        
        @self.server.feature(INITIALIZE)
        async def initialize(params):
            """Initialize LSP server."""
            logger.info("LSP server initialized")
            return {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {"resolveProvider": True},
                    "hoverProvider": True,
                    "definitionProvider": True,
                    "referencesProvider": True,
                    "codeActionProvider": True,
                }
            }

        @self.server.feature(TEXT_DOCUMENT_DID_OPEN)
        async def did_open(params):
            """Handle document open."""
            uri = params.textDocument.uri
            text = params.textDocument.text
            self.document_cache[uri] = text
            logger.info(f"Document opened: {uri}")

        @self.server.feature(TEXT_DOCUMENT_DID_CHANGE)
        async def did_change(params):
            """Handle document change."""
            uri = params.textDocument.uri
            for change in params.contentChanges:
                if "range" in change:
                    # Incremental change
                    if uri in self.document_cache:
                        self.document_cache[uri] = change.text
                else:
                    # Full document change
                    self.document_cache[uri] = change.text
            logger.debug(f"Document changed: {uri}")

        @self.server.feature(COMPLETION)
        async def completions(params):
            """Provide code completions."""
            uri = params.textDocument.uri
            line = params.position.line
            char = params.position.character
            
            if uri not in self.document_cache:
                return []
            
            code = self.document_cache[uri]
            language = self._get_language_from_uri(uri)
            
            try:
                # Get context around cursor
                lines = code.split('\n')
                context_start = max(0, line - 5)
                context_end = min(len(lines), line + 2)
                context = '\n'.join(lines[context_start:context_end])
                
                prompt = f"""Given the following {language} code context, suggest the next 5 code completions.
Context (cursor is at end):
```{language}
{context}
```

Provide only the completion suggestions, one per line, without explanations."""
                
                result = await self.swe_agent.ollama_client.generate(
                    prompt=prompt,
                    system_prompt="You are a code completion expert. Provide only relevant code suggestions."
                )
                
                completions_text = result.get("text", "")
                suggestions = [s.strip() for s in completions_text.split('\n') if s.strip()]
                
                completion_items = [
                    CompletionItem(
                        label=suggestion[:50],
                        kind=CompletionItemKind.Snippet,
                        detail=f"SWE Agent suggestion"
                    )
                    for suggestion in suggestions[:5]
                ]
                
                return completion_items
            except Exception as e:
                logger.error(f"Completion error: {e}")
                return []

        @self.server.feature(HOVER)
        async def hover(params):
            """Provide hover information."""
            uri = params.textDocument.uri
            line = params.position.line
            char = params.position.character
            
            if uri not in self.document_cache:
                return None
            
            code = self.document_cache[uri]
            language = self._get_language_from_uri(uri)
            
            try:
                lines = code.split('\n')
                if line >= len(lines):
                    return None
                
                current_line = lines[line]
                start = max(0, char - 20)
                end = min(len(current_line), char + 20)
                context = current_line[start:end]
                
                prompt = f"""Explain this {language} code snippet in one line:
`{context}`

Provide a concise explanation."""
                
                result = await self.swe_agent.ollama_client.generate(
                    prompt=prompt,
                    system_prompt="You are a code documentation expert. Provide brief, helpful explanations."
                )
                
                explanation = result.get("text", "")
                
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"**SWE Agent**\n\n{explanation}"
                    )
                )
            except Exception as e:
                logger.error(f"Hover error: {e}")
                return None

        @self.server.feature(CODE_ACTION)
        async def code_actions(params):
            """Provide code actions for diagnostics."""
            uri = params.textDocument.uri
            range_ = params.range
            diagnostics = params.context.diagnostics
            
            if uri not in self.document_cache or not diagnostics:
                return []
            
            code = self.document_cache[uri]
            language = self._get_language_from_uri(uri)
            
            actions = []
            
            try:
                for diagnostic in diagnostics:
                    prompt = f"""Given this {language} code with an issue:
{code}

Issue: {diagnostic.message}

Suggest a fix or improvement."""
                    
                    result = await self.swe_agent.ollama_client.generate(
                        prompt=prompt,
                        system_prompt="You are a code fixer. Provide practical solutions."
                    )
                    
                    fix = result.get("text", "")
                    
                    if fix:
                        action = CodeAction(
                            title=f"Fix: {diagnostic.message[:30]}...",
                            kind=CodeActionKind.QuickFix,
                            edit={
                                "changes": {
                                    uri: [
                                        {
                                            "range": range_,
                                            "newText": fix
                                        }
                                    ]
                                }
                            }
                        )
                        actions.append(action)
                
                return actions
            except Exception as e:
                logger.error(f"Code action error: {e}")
                return []

        @self.server.feature(REFERENCES)
        async def references(params):
            """Find references to symbol."""
            uri = params.textDocument.uri
            line = params.position.line
            char = params.position.character
            
            if uri not in self.document_cache:
                return []
            
            code = self.document_cache[uri]
            language = self._get_language_from_uri(uri)
            
            try:
                lines = code.split('\n')
                if line >= len(lines):
                    return []
                
                current_line = lines[line]
                # Extract word at cursor
                start = char
                while start > 0 and current_line[start - 1].isalnum() or current_line[start - 1] == '_':
                    start -= 1
                end = char
                while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                    end += 1
                
                symbol = current_line[start:end]
                
                if not symbol:
                    return []
                
                # Find all occurrences
                references = []
                for i, line_text in enumerate(lines):
                    col = 0
                    while True:
                        col = line_text.find(symbol, col)
                        if col == -1:
                            break
                        references.append(
                            Location(
                                uri=uri,
                                range=Range(
                                    start=Position(line=i, character=col),
                                    end=Position(line=i, character=col + len(symbol))
                                )
                            )
                        )
                        col += len(symbol)
                
                return references
            except Exception as e:
                logger.error(f"References error: {e}")
                return []

    def _get_language_from_uri(self, uri: str) -> str:
        """Determine programming language from file URI."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'jsx',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.react': 'jsx',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
        }
        
        for ext, lang in extension_map.items():
            if uri.endswith(ext):
                return lang
        
        return 'python'  # Default

    def start(self, host: str = "127.0.0.1", port: int = 8080):
        """Start the LSP server."""
        logger.info(f"Starting SWE LSP server on {host}:{port}")
        self.server.start_tcp(host, port)
