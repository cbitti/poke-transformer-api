from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Environment / runtime mode
    APP_ENV: Literal["development", "test", "production"] = "development"

    # FastAPI / API config
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Poke Transformer API"
    DEBUG: bool = True

    # Database URLs
    # Main application database
    DATABASE_URL: str = "sqlite:///./poke.db"
    # Optional test-only database (used by pytest fixtures)
    TEST_DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars instead of erroring
    )


settings = Settings()
