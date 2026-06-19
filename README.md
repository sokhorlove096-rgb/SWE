# SWE Agent Platform

A FastAPI-based Software Engineer agent specialized in React (all variants) and Python, powered by Ollama.

## Features

- **Specialized in**: React, React Native, Next.js, and Python
- **Backend**: FastAPI
- **AI Model**: Ollama (RoandaiG-4-31IT:latest)
- **Capabilities**:
  - Code analysis and generation
  - Bug detection and fixing
  - Architecture design
  - Code review
  - Documentation generation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sokhorlove096-rgb/SWE.git
   cd SWE
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration.

## Running the Agent

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Check agent status

### Code Analysis
- `POST /analyze` - Analyze code for issues

### Code Generation
- `POST /generate` - Generate code based on requirements

### Code Review
- `POST /review` - Review code quality

### Chat
- `POST /chat` - Chat with the SWE agent

## Environment Variables

- `OLLAMA_BASE_URL` - Ollama server URL
- `OLLAMA_MODEL` - Model name to use
- `FAST_API_HOST` - FastAPI host
- `FAST_API_PORT` - FastAPI port
- `DEBUG` - Debug mode
- `AGENT_NAME` - Agent name
- `AGENT_SPECIALIZATIONS` - Comma-separated specializations
- `MAX_TOKENS` - Maximum tokens for responses
- `TEMPERATURE` - Temperature for model responses
- `LOG_LEVEL` - Logging level

## Project Structure

```
SWE/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── .env.example          # Environment variables template
├── README.md             # This file
└── app/
    ├── __init__.py
    ├── models.py         # Pydantic models
    ├── ollama_client.py  # Ollama integration
    ├── agent.py          # SWE Agent logic
    └── routes.py         # API routes
```

## Architecture

### Core Components

1. **OllamaClient**: Handles communication with Ollama server
2. **SWEAgent**: Main agent logic for code understanding and generation
3. **FastAPI Routes**: HTTP endpoints for agent interaction
4. **Configuration**: Environment-based configuration management

## Usage Examples

### Analyze Code

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(hello)",
    "language": "python"
  }'
```

### Generate Code

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": "Create a React component for a todo list",
    "language": "jsx"
  }'
```

### Chat with Agent

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I handle state in React?"
  }'
```

## Development

### Running with auto-reload:

```bash
python -m uvicorn app.main:app --reload
```

### Running tests (when added):

```bash
pytest
```

## License

MIT
