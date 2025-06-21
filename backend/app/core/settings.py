from pydantic_settings import BaseSettings
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
    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
