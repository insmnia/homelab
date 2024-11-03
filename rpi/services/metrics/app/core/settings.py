from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HL_",
        env_nested_delimiter="__",
        extra="ignore",
        populate_by_name=True,
    )
    VERSION: str = "0.0.0"
    DEBUG: bool = False
    LOGGING_CONFIG_PATH: Path | str | None = None
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "CRITICAL"] = "INFO"

    POSTGRES_DSN: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        _env_file=".env"
    )  # TODO: get env file depends on environment LOCAL/PROD
