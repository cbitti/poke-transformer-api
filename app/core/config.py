from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    PROJECT_NAME: str = "Poke Transformer API"
    DATABASE_URL: str = "sqlite:///./poke.db"
    # Later add DB URL, etc

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
