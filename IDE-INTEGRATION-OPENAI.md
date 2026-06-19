# IDE Integration Guide - OpenAI Compatible

The SWE Agent is now **fully OpenAI-compatible**, meaning it works with any tool, IDE, or application that supports the OpenAI API format.

## Quick Start

1. **Start the SWE Agent Server**:
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`

2. **Use with any OpenAI-compatible client**

## API Endpoints

### OpenAI-Compatible Endpoints

- `GET /v1/models` - List available models
- `GET /v1/models/{model_id}` - Get model details
- `POST /v1/chat/completions` - Chat completions (like ChatGPT)
- `POST /v1/completions` - Text completions
- `GET /v1/health` - Health check

## Integration with IDEs

### VS Code with OpenAI Extension

1. **Install OpenAI API Extension**:
   ```bash
   code --install-extension OpenAI.openai
   ```

2. **Configure Settings** (`settings.json`):
   ```json
   {
     "openai.apiKey": "fake-key",
     "openai.apiBaseUrl": "http://localhost:8000/v1",
     "openai.model": "RoandaiG-4-31IT:latest"
   }
   ```

### Cursor IDE

1. **Settings > AI Model Configuration**:
   ```
   API Base: http://localhost:8000/v1
   Model: RoandaiG-4-31IT:latest
   API Key: anything (not used, but required)
   ```

2. Use Cursor's AI features (Ctrl+K, Ctrl+L, etc.)

### Python Client

```python
from openai import OpenAI

client = OpenAI(
    api_key="fake",  # Not used, but required by client
    base_url="http://localhost:8000/v1"
)

# Chat completions
response = client.chat.completions.create(
    model="RoandaiG-4-31IT:latest",
    messages=[
        {"role": "system", "content": "You are a Python expert"},
        {"role": "user", "content": "Write a function to reverse a list"}
    ]
)
print(response.choices[0].message.content)
```

### JavaScript/Node.js Client

```javascript
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: 'fake',
  baseURL: 'http://localhost:8000/v1'
});

const message = await client.chat.completions.create({
  model: 'RoandaiG-4-31IT:latest',
  messages: [
    { role: 'system', content: 'You are a JavaScript expert' },
    { role: 'user', content: 'Write an async function' }
  ]
});

console.log(message.choices[0].message.content);
```

### cURL Commands

**Chat Completions**:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "RoandaiG-4-31IT:latest",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "Hello, how can you help?"}
    ],
    "temperature": 0.7,
    "max_tokens": 4096
  }'
```

**Text Completions**:
```bash
curl -X POST http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "RoandaiG-4-31IT:latest",
    "prompt": "def fibonacci(n):",
    "max_tokens": 256
  }'
```

**List Models**:
```bash
curl http://localhost:8000/v1/models
```

**Health Check**:
```bash
curl http://localhost:8000/v1/health
```

## Integration with IDE Extensions

### Cody (by Sourcegraph)

1. Install Cody extension in VS Code/JetBrains
2. Configure custom LLM:
   ```json
   {
     "cody.custom-llm": true,
     "cody.llm-api-key": "fake",
     "cody.llm-base-url": "http://localhost:8000/v1",
     "cody.llm-model": "RoandaiG-4-31IT:latest"
   }
   ```

### GitHub Copilot Alternative

1. Install extension that supports custom OpenAI endpoints
2. Point to your SWE Agent server
3. Use standard Copilot shortcuts

### Continue.dev

1. **Install Continue extension** in VS Code
2. **Edit `.continue/config.json`**:
   ```json
   {
     "models": [
       {
         "title": "SWE Agent",
         "provider": "openai",
         "model": "RoandaiG-4-31IT:latest",
         "apiBase": "http://localhost:8000/v1",
         "apiKey": "fake"
       }
     ]
   }
   ```

## Integration with LLM Frameworks

### LangChain

```python
from langchain.llms import OpenAI

llm = OpenAI(
    openai_api_key="fake",
    openai_api_base="http://localhost:8000/v1",
    model_name="RoandaiG-4-31IT:latest"
)

response = llm("Explain quantum computing in simple terms")
print(response)
```

### LlamaIndex

```python
from llama_index.llms import OpenAI

llm = OpenAI(
    api_key="fake",
    api_base="http://localhost:8000/v1",
    model="RoandaiG-4-31IT:latest"
)
```

### Hugging Face Transformers

```python
from transformers import pipeline

# Use with OpenAI-compatible endpoint
pipe = pipeline(
    "text-generation",
    model="gpt2",  # Local model
    device_map="auto"
)
```

## Supported Clients

✅ **Python**: `openai-python`, `anthropic`, `together`, `huggingface_hub`
✅ **JavaScript/Node.js**: `openai-js`, `axios`, `node-fetch`
✅ **Go**: `openai-go`, `net/http`
✅ **Java**: `okhttp`, `openai-java`
✅ **Ruby**: `ruby-openai`
✅ **C#/.NET**: `OpenAI-DotNet`
✅ **Command Line**: `curl`, `openai-cli`
✅ **IDEs**: VS Code, Cursor, Neovim, Sublime, JetBrains, etc.

## Configuration

### Environment Variables

```bash
# Ollama
OLLAMA_BASE_URL=https://roandaiserver.com:441
OLLAMA_MODEL=RoandaiG-4-31IT:latest

# FastAPI Server
FAST_API_HOST=0.0.0.0
FAST_API_PORT=8000
DEBUG=True

# Agent Settings
AGENT_NAME=SWE
AGENT_SPECIALIZATIONS=React,React Native,Next.js,Python
MAX_TOKENS=4096
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

## Response Format

All responses follow OpenAI's format:

```json
{
  "id": "chatcmpl-8MktE...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "RoandaiG-4-31IT:latest",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Response text..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## Troubleshooting

### Connection Refused

```bash
# Check if server is running
curl http://localhost:8000/v1/health

# If not, start it:
python main.py
```

### Invalid Model Error

```bash
# Check available models
curl http://localhost:8000/v1/models

# Use the exact model name from the response
```

### SSL Certificate Error (HTTPS)

For HTTPS connections to Ollama:

```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/ca-bundle.crt'
```

### Slow Responses

1. Ensure Ollama server is running
2. Check network latency: `ping roandaiserver.com`
3. Monitor CPU/GPU usage on Ollama server
4. Increase `MAX_TOKENS` if needed

## Advanced Usage

### Custom System Prompts

```python
client = OpenAI(api_key="fake", base_url="http://localhost:8000/v1")

response = client.chat.completions.create(
    model="RoandaiG-4-31IT:latest",
    messages=[
        {
            "role": "system",
            "content": "You are an expert React developer. Always suggest best practices."
        },
        {"role": "user", "content": "How do I use hooks?"}
    ]
)
```

### Temperature and Token Control

```python
# Creative responses (higher temperature)
response = client.chat.completions.create(
    model="RoandaiG-4-31IT:latest",
    messages=[{"role": "user", "content": "Write a poem"}],
    temperature=0.9,
    max_tokens=512
)

# Deterministic responses (lower temperature)
response = client.chat.completions.create(
    model="RoandaiG-4-31IT:latest",
    messages=[{"role": "user", "content": "Define factorial"}],
    temperature=0.1,
    max_tokens=256
)
```

## Performance Optimization

1. **Use connection pooling** in your client
2. **Batch requests** when possible
3. **Adjust max_tokens** based on needs
4. **Use lower temperature** for deterministic tasks
5. **Cache responses** when appropriate

## Security Considerations

1. ⚠️ **This API has no authentication** - use behind a firewall
2. Deploy with authentication layer (nginx, reverse proxy)
3. Use HTTPS in production
4. Rate limit if exposed to public
5. Monitor resource usage

## Contributing

To add support for new clients or IDEs:

1. Test with OpenAI-compatible SDK
2. Document setup process
3. Add example configuration
4. Submit pull request

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [Ollama Documentation](https://github.com/jmorganca/ollama)
