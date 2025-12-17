"""Configuration management using Pydantic."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get paths to search for .env files (project and parent, like load_env)
PROJECT_ROOT = Path(__file__).parent.parent
PARENT_ROOT = PROJECT_ROOT.parent


class Settings(BaseSettings):
    """Application settings with type validation."""

    openai_api_key: str
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.2
    default_max_tokens: int = 512

    model_config = SettingsConfigDict(
        # Search for .env in project dir, then parent dir (like load_env)
        env_file=(
            str(PROJECT_ROOT / ".env"),
            str(PARENT_ROOT / ".env"),
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
