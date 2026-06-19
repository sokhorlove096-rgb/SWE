# IDE Integration Guide

The SWE Agent can be integrated with any LSP-compatible IDE. This guide provides instructions for popular IDEs.

## Supported IDEs

- [VS Code](#vs-code)
- [Cursor](#cursor)
- [Neovim](#neovim)
- [Sublime Text](#sublime-text)
- [Vim (with coc.nvim)](#vim-with-cocnvim)
- [Emacs](#emacs)
- [OpenCode](#opencode)
- [Other LSP-Compatible Editors](#other-lsp-compatible-editors)

## Setup

### Prerequisites

1. **SWE Agent Running**: Start the main FastAPI server
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`

2. **LSP Server Running**: Start the LSP server in a separate terminal
   ```bash
   python lsp_main.py
   ```
   LSP server runs on `127.0.0.1:8080`

3. **Generate IDE Configurations**:
   ```bash
   python generate_ide_configs.py
   ```
   This creates configuration files in `./ide-extensions/`

## VS Code

### Installation

1. **Create Extension Structure**:
   ```bash
   mkdir -p ~/.vscode/extensions/swe-agent
   cp ide-extensions/vscode/package.json ~/.vscode/extensions/swe-agent/
   ```

2. **Install Dependencies**:
   ```bash
   cd ~/.vscode/extensions/swe-agent
   npm install
   ```

3. **Configure Settings** (`settings.json`):
   ```json
   {
     "[python]": {
       "editor.defaultFormatter": "ms-python.python"
     },
     "swe-agent.lspHost": "127.0.0.1",
     "swe-agent.lspPort": 8080,
     "swe-agent.apiHost": "http://localhost:8000",
     "swe-agent.autoAnalyze": true
   }
   ```

### Usage

- **Analyze Code**: `Ctrl+Shift+A` (Windows/Linux) or `Cmd+Shift+A` (Mac)
- **Generate Code**: `Ctrl+Shift+G` (Windows/Linux) or `Cmd+Shift+G` (Mac)
- **Review Code**: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- **Open Chat**: `Ctrl+Shift+C` (Windows/Linux) or `Cmd+Shift+C` (Mac)

### Features

- Real-time code completion
- Hover documentation
- Code diagnostics
- Quick fixes
- Go to definition
- Find references

## Cursor

Cursor uses VS Code extensions, so the setup is similar.

### Installation

1. Copy the VS Code extension to Cursor extensions:
   ```bash
   cp -r ~/.vscode/extensions/swe-agent ~/.cursor/extensions/
   ```

2. Restart Cursor

### Features

All VS Code features are available, plus Cursor-specific optimizations:
- Enhanced code generation
- AI-powered refactoring
- Natural language queries

## Neovim

### Installation

1. **Install LSP Configuration**:
   ```bash
   mkdir -p ~/.config/nvim
   cp ide-extensions/neovim/lspconfig.lua ~/.config/nvim/lspconfig-swe.lua
   ```

2. **Add to `init.lua`**:
   ```lua
   require('lspconfig-swe')
   ```

3. **Install Neovim LSP Client** (if not already installed):
   ```bash
   # Using packer.nvim
   use 'neovim/nvim-lspconfig'
   
   # Or using vim-plug
   Plug 'neovim/nvim-lspconfig'
   ```

### Usage

- **Code completion**: `<C-x><C-o>`
- **Go to definition**: `gd`
- **Hover**: `K`
- **Show diagnostics**: `:LspDiagnosticsShow`

## Sublime Text

### Installation

1. **Install LSP Package**:
   - Open Command Palette: `Ctrl+Shift+P`
   - Type: `Package Control: Install Package`
   - Search and install: `LSP`

2. **Copy Configuration**:
   ```bash
   cp ide-extensions/sublime/LSP.json ~/.config/sublime-text-3/Packages/User/LSP.json
   ```

3. **Restart Sublime**

### Usage

- **Code completion**: `Ctrl+Space`
- **Show diagnostics**: `Ctrl+Shift+E`
- **Go to definition**: `Ctrl+G`

## Vim (with coc.nvim)

### Installation

1. **Install coc.nvim** (if not already installed):
   ```bash
   # Using vim-plug
   Plug 'neoclide/coc.nvim', {'branch': 'release'}
   ```

2. **Add Configuration**:
   ```bash
   cat ide-extensions/vim/coc-config.vim >> ~/.vimrc
   ```

3. **Restart Vim** and run `:PlugInstall`

### Usage

- **Code completion**: `<Tab>`
- **Show hover info**: `K`
- **Go to definition**: `gd`
- **Find references**: `gr`

## Emacs

### Installation

1. **Install lsp-mode** (if not already installed):
   ```elisp
   (use-package lsp-mode
     :ensure t)
   ```

2. **Add Configuration**:
   ```bash
   cat ide-extensions/emacs/lsp-config.el >> ~/.emacs.d/init.el
   ```

3. **Restart Emacs** or evaluate the configuration

### Usage

- **Code completion**: `M-x completion-at-point`
- **Show hover info**: `M-x lsp-describe-thing-at-point`
- **Go to definition**: `M-x lsp-goto-type-definition`
- **Find references**: `M-x lsp-find-references`

## OpenCode

### Installation

1. **Check for LSP support** in OpenCode documentation
2. **Add LSP server configuration**:
   ```json
   {
     "lspServers": [
       {
         "name": "swe-agent",
         "command": ["python", "-m", "app.lsp_server"],
         "languages": ["python", "javascript", "typescript"]
       }
     ]
   }
   ```

## Other LSP-Compatible Editors

For any editor supporting LSP:

1. **Configure the LSP server**:
   - Server: Python module `app.lsp_server`
   - Host: `127.0.0.1`
   - Port: `8080`

2. **Supported file types**:
   - Python (`.py`)
   - JavaScript (`.js`, `.jsx`)
   - TypeScript (`.ts`, `.tsx`)
   - React (`.react`)

3. **Features available**:
   - Code completion
   - Hover documentation
   - Diagnostics
   - Code actions
   - Go to definition
   - Find references

## Troubleshooting

### LSP Server Not Connecting

1. **Check if LSP server is running**:
   ```bash
   curl http://127.0.0.1:8080/health
   ```

2. **Check logs**:
   ```bash
   tail -f lsp_server.log
   ```

3. **Verify configuration**:
   - Host: `127.0.0.1` (not `localhost`)
   - Port: `8080`
   - Model running in Ollama

### Slow Responses

1. **Check Ollama connection**:
   ```bash
   curl https://roandaiserver.com:441/api/tags
   ```

2. **Verify model is loaded**:
   ```bash
   curl https://roandaiserver.com:441/api/tags | grep RoandaiG-4-31IT
   ```

3. **Check network latency**:
   ```bash
   ping roandaiserver.com
   ```

### Extension Not Loading

1. **Restart IDE**: Close and reopen the editor
2. **Check extension logs**: Most IDEs have a developer console
3. **Verify Python installation**: `python --version`
4. **Reinstall dependencies**: `pip install -r requirements.txt`

## Configuration Options

### Common Settings

```json
{
  "swe-agent.lspHost": "127.0.0.1",
  "swe-agent.lspPort": 8080,
  "swe-agent.apiHost": "http://localhost:8000",
  "swe-agent.autoAnalyze": true,
  "swe-agent.maxTokens": 4096,
  "swe-agent.temperature": 0.7,
  "swe-agent.completionTriggers": [".", " ", ":"],
  "swe-agent.showDiagnostics": true
}
```

## Advanced Usage

### Custom Commands

Add custom commands to your IDE configuration:

```json
{
  "swe-agent.customCommands": [
    {
      "name": "Refactor",
      "request": "code_action",
      "kind": "refactor"
    },
    {
      "name": "Format",
      "request": "code_action",
      "kind": "source.formatDocument"
    }
  ]
}
```

### Performance Tuning

1. **Disable auto-analysis for large files**:
   ```json
   {
     "swe-agent.maxFileSize": 1000000
   }
   ```

2. **Adjust completion timeout**:
   ```json
   {
     "swe-agent.completionTimeout": 5000
   }
   ```

## Contributing

To add support for a new IDE:

1. Create a new method in `IDEExtensionManager` class
2. Add configuration generation for the IDE
3. Test with the IDE's native LSP client
4. Document the setup process
5. Submit a pull request

## Resources

- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [Ollama Documentation](https://github.com/jmorganca/ollama)
