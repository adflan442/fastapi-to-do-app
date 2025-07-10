from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    
    # __file__ = backend/app/settings.py
    # .parent = backend/app
    # .parent.parent = backend/
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding = 'utf-8'
    )
    print("Loading env file from:", (Path(__file__).resolve().parents[2] / ".env"))


settings = Settings()
