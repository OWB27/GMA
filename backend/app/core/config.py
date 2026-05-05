from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GMA Backend"
    app_version: str = "0.1.0"
    environment: str = Field(default="local", alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+psycopg://gma:gma@localhost:5432/gma",
        alias="DATABASE_URL",
    )
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
