"""
Application configuration and environment variables
"""
import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Vagner Sales Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # OpenAI
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    LLM_MODEL: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    
    # Pinecone
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_ENV: Optional[str] = Field(default=None, env="PINECONE_ENV")
    PINECONE_INDEX: str = Field(default="sales-agent-kb", env="PINECONE_INDEX")
    
    # WhatsApp
    WHATSAPP_ACCESS_TOKEN: str = Field(..., env="WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_ID: str = Field(..., env="WHATSAPP_PHONE_ID")
    WHATSAPP_VERIFY_TOKEN: Optional[str] = Field(default=None, env="WHATSAPP_VERIFY_TOKEN")
    
    # ElevenLabs
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID: Optional[str] = Field(default=None, env="ELEVENLABS_VOICE_ID")
    ELEVENLABS_VOICE_NAME: Optional[str] = Field(default=None, env="ELEVENLABS_VOICE_NAME")
    
    # Folders
    MEDIA_FOLDER: str = Field(default="materials/media", env="MEDIA_FOLDER")
    PDF_FOLDER: str = Field(default="materials/pdfs", env="PDF_FOLDER")
    TEMP_FOLDER: str = Field(default="materials/temp", env="TEMP_FOLDER")
    
    # Payment Links
    PAYMENT_LINK_NORMAL: str = Field(default="https://pay.example.com/linkA", env="PAYMENT_LINK_NORMAL")
    PAYMENT_LINK_DISCOUNT40: str = Field(default="https://pay.example.com/linkA?disc=40", env="PAYMENT_LINK_DISCOUNT40")
    PAYMENT_LINK_DISCOUNT50: str = Field(default="https://pay.example.com/linkA?disc=50", env="PAYMENT_LINK_DISCOUNT50")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Ensure required folders exist
def ensure_folders():
    """Create necessary folders if they don't exist"""
    settings = get_settings()
    folders = [
        settings.MEDIA_FOLDER,
        settings.PDF_FOLDER,
        settings.TEMP_FOLDER,
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

