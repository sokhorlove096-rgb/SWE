import aiohttp
import asyncio
from typing import Optional, Dict, Any
from loguru import logger
import time

class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama server URL
            model: Model name
            max_tokens: Maximum tokens for responses
            temperature: Temperature for model responses
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = aiohttp.ClientTimeout(total=300)  # 5 minute timeout
        
    async def check_connection(self) -> bool:
        """Check if Ollama server is accessible."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    ssl=False  # For self-signed certificates
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Input prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated response with metadata
        """
        try:
            start_time = time.time()
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "top_k": 40,
                "top_p": 0.9,
                "stream": False,
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    ssl=False
                ) as response:
                    if response.status != 200:
                        logger.error(f"Ollama API error: {response.status}")
                        return {
                            "text": "",
                            "error": f"API returned status {response.status}",
                            "generation_time": time.time() - start_time
                        }
                    
                    data = await response.json()
                    generation_time = time.time() - start_time
                    
                    logger.info(f"Generation completed in {generation_time:.2f}s")
                    
                    return {
                        "text": data.get("response", ""),
                        "generation_time": generation_time,
                        "model": data.get("model"),
                        "tokens": {
                            "prompt_eval_count": data.get("prompt_eval_count", 0),
                            "eval_count": data.get("eval_count", 0)
                        }
                    }
        except asyncio.TimeoutError:
            logger.error("Ollama request timeout")
            return {
                "text": "",
                "error": "Request timeout",
                "generation_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return {
                "text": "",
                "error": str(e),
                "generation_time": time.time() - start_time
            }
    
    async def chat(
        self,
        messages: list,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Chat with Ollama model.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            
        Returns:
            Chat response with metadata
        """
        try:
            start_time = time.time()
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "stream": False,
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    ssl=False
                ) as response:
                    if response.status != 200:
                        logger.error(f"Ollama API error: {response.status}")
                        return {
                            "text": "",
                            "error": f"API returned status {response.status}",
                            "response_time": time.time() - start_time
                        }
                    
                    data = await response.json()
                    response_time = time.time() - start_time
                    
                    logger.info(f"Chat completed in {response_time:.2f}s")
                    
                    return {
                        "text": data.get("message", {}).get("content", ""),
                        "response_time": response_time,
                        "model": data.get("model"),
                        "tokens": {
                            "prompt_eval_count": data.get("prompt_eval_count", 0),
                            "eval_count": data.get("eval_count", 0)
                        }
                    }
        except asyncio.TimeoutError:
            logger.error("Ollama chat request timeout")
            return {
                "text": "",
                "error": "Request timeout",
                "response_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return {
                "text": "",
                "error": str(e),
                "response_time": time.time() - start_time
            }
