"""Configuration module for GenQuestAI."""

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    max_iterations: int = Field(
        default=50,
        ge=1,
        description="Maximum number of game iterations",
    )
    ollama_model: str = Field(
        default="qwen2.5:14b",
        description="Ollama model name to use",
    )
    ollama_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API URL",
    )
    zork_game_path: str = Field(
        default="/usr/games/zork",
        description="Path to Zork game executable",
    )
    verbose: bool = Field(
        default=True,
        description="Show full game output",
    )

    @field_validator("max_iterations")
    @classmethod
    def validate_positive(cls, value: int) -> int:
        """Ensure max_iterations is positive."""
        if value <= 0:
            raise ValueError("max_iterations must be greater than 0")
        return value

    @field_validator("ollama_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        """Ensure URL starts with http or https."""
        if not value.startswith(("http://", "https://")):
            raise ValueError("ollama_url must start with http:// or https://")
        return value
