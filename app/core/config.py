from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application
    APP_NAME: str = "MediaVault"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./mediavault.db"
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 15
    UPLOAD_DIR: str = "uploads"
    ALLOWED_MIME_TYPES: list[str] = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]
    
    # OCR
    TESSERACT_CMD: Optional[str] = None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
