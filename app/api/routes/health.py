"""Health check endpoints"""
import os
from fastapi import APIRouter
from dotenv import load_dotenv
from app.models.responses import HealthResponse

load_dotenv()

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Check service availability
    services = {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "pinecone": bool(os.getenv("PINECONE_API_KEY")),
        "whatsapp": bool(os.getenv("WHATSAPP_ACCESS_TOKEN")),
        "elevenlabs": bool(os.getenv("ELEVENLABS_API_KEY")),
    }
    
    all_healthy = all(services.values())
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        version=os.getenv("APP_VERSION", "1.0.0"),
        services=services
    )


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": os.getenv("APP_NAME", "Vagner Sales Agent"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "running"
    }

