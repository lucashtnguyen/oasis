"""Centralised settings for ChatGPT Stock Advisor."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError, model_validator
from dotenv import load_dotenv

# Load .env if present (noop in most CI environments)
load_dotenv(Path(__file__).with_name(".env"))


class Settings(BaseSettings):
    """Strongly-typed runtime configuration."""

    openai_api_key: str | None = None
    run_openai_tests: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    @model_validator(mode="after")
    def _check_api_key(cls, values: "Settings") -> "Settings":
        if values.run_openai_tests and not values.openai_api_key:
            raise ValidationError(
                [
                    {
                        "loc": ("openai_api_key",),
                        "msg": "openai_api_key required when run_openai_tests is True",
                        "type": "value_error",
                    }
                ],
                Settings,
            )
        return values


settings = Settings()  # import-safe singleton
