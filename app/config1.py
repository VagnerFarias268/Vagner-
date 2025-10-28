"""Configuration management"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = Field(default="Vagner Sales Agent")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # API Keys
    OPENAI_API_KEY: str = Field(default="")
    PINECONE_API_KEY: str = Field(default="")
    PINECONE_ENV: str = Field(default="us-east-1")
    PINECONE_INDEX: str = Field(default="sales-agent-kb")
    WHATSAPP_ACCESS_TOKEN: str = Field(default="")
    WHATSAPP_PHONE_ID: str = Field(default="")
    WHATSAPP_VERIFY_TOKEN: str = Field(default="your-verify-token-here")
    ELEVENLABS_API_KEY: str = Field(default="")
    ELEVENLABS_VOICE_ID: str = Field(default="")
    ELEVENLABS_VOICE_NAME: str = Field(default="")
    
    # LLM Settings
    LLM_MODEL: str = Field(default="gpt-4")
    
    # Folders
    TEMP_FOLDER: str = Field(default="materials/temp")
    MEDIA_FOLDER: str = Field(default="materials/media")
    PDF_FOLDER: str = Field(default="materials/pdfs")
    
    # Payment Links
    PAYMENT_LINK_NORMAL: str = Field(default="https://pay.example.com/normal")
    PAYMENT_LINK_DISCOUNT40: str = Field(default="https://pay.example.com/discount40")
    PAYMENT_LINK_DISCOUNT50: str = Field(default="https://pay.example.com/discount50")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


def ensure_folders():
    """Ensure required folders exist"""
    settings = get_settings()
    folders = [
        settings.TEMP_FOLDER,
        settings.MEDIA_FOLDER,
        settings.PDF_FOLDER,
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Folder ready: {folder}")

