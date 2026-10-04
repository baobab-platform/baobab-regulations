"""Application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BAOBAB_REG_", env_file=".env", extra="ignore")

    app_name: str = "baobab-regulations"
    environment: str = "local"
    database_url: str = "postgresql://baobab:baobab@localhost:5432/baobab_regulations"
    opa_url: str = "http://localhost:8181"
    api_host: str = "0.0.0.0"
    api_port: int = 8080


@lru_cache
def get_settings() -> Settings:
    return Settings()
