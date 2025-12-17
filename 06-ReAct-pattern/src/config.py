"""Pydantic configuration for ReAct agent."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Get project and parent root directories
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
PARENT_ROOT = PROJECT_ROOT.parent.resolve()


class Settings(BaseSettings):
    """Application settings with type validation."""

    openai_api_key: str
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.2
    default_max_tokens: int = 300
    
    model_config = SettingsConfigDict(
        # Search for .env in project dir, then parent dir (like load_env)
        env_file=(
            str(PROJECT_ROOT / ".env"),
            str(PARENT_ROOT / ".env"),
        ),
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields from .env
    )


# Global settings instance - auto-loads from .env
settings = Settings()
