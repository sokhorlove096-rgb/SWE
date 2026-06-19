import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "https://roandaiserver.com:441")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "RoandaiG-4-31IT:latest")
    
    # FastAPI Configuration
    fast_api_host: str = os.getenv("FAST_API_HOST", "0.0.0.0")
    fast_api_port: int = int(os.getenv("FAST_API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Agent Configuration
    agent_name: str = os.getenv("AGENT_NAME", "SWE")
    agent_specializations: list = os.getenv("AGENT_SPECIALIZATIONS", "React,React Native,Next.js,Python").split(",")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
