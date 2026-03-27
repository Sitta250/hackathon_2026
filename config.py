from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    app_name: str = "Bremo"
    environment: str = os.getenv("ENVIRONMENT", "dev")

    provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o")
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")

    data_dir: Path = Path(os.getenv("DATA_DIR", "data"))
    logs_dir: Path = Path(os.getenv("LOGS_DIR", "logs"))

    def validate(self) -> None:
        if self.provider not in {"openai", "anthropic"}:
            raise ValueError(f"Unsupported provider: {self.provider}")

        if self.provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

        if self.provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    return settings