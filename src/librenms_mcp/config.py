from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


dotenv_path = Path('.') / '.env'
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    api_url: str = 'http://localhost:8000'
    api_token: str = ''

    class Config:
        env_prefix = 'LIBRENMS_'
        env_file = dotenv_path
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
