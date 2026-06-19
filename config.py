import os
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = Field(
        default="https://roandaiserver.com:441",
        description="Ollama server URL"
    )
    ollama_model: str = Field(
        default="RoandaiG-4-31IT:latest",
        description="Ollama model name"
    )
    
    # FastAPI Configuration
    fast_api_host: str = Field(
        default="0.0.0.0",
        description="FastAPI host"
    )
    fast_api_port: int = Field(
        default=8000,
        description="FastAPI port"
    )
    debug: bool = Field(
        default=True,
        description="Debug mode"
    )
    
    # LSP Configuration
    lsp_host: str = Field(
        default="127.0.0.1",
        description="LSP server host"
    )
    lsp_port: int = Field(
        default=8080,
        description="LSP server port"
    )
    
    # Agent Configuration
    agent_name: str = Field(
        default="SWE",
        description="Agent name"
    )
    agent_specializations: str = Field(
        default="React,React Native,Next.js,Python",
        description="Comma-separated agent specializations"
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum tokens for responses"
    )
    temperature: float = Field(
        default=0.7,
        description="Temperature for model responses"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        """Parse debug flag."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)
    
    @field_validator("fast_api_port", "lsp_port", "max_tokens", mode="before")
    @classmethod
    def parse_int(cls, v):
        """Parse integer values."""
        if isinstance(v, str):
            return int(v)
        return v
    
    @field_validator("temperature", mode="before")
    @classmethod
    def parse_float(cls, v):
        """Parse float values."""
        if isinstance(v, str):
            return float(v)
        return v
    
    def get_specializations_list(self) -> list:
        """Get agent specializations as a list."""
        return [s.strip() for s in self.agent_specializations.split(",") if s.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
