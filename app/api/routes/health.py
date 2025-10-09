"""Health check endpoints"""
from fastapi import APIRouter
from app.models.responses import HealthResponse
from app.config import get_settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    
    # Check service availability
    services = {
        "openai": bool(settings.OPENAI_API_KEY),
        "pinecone": bool(settings.PINECONE_API_KEY),
        "whatsapp": bool(settings.WHATSAPP_ACCESS_TOKEN),
        "elevenlabs": bool(settings.ELEVENLABS_API_KEY),
    }
    
    all_healthy = all(services.values())
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        version=settings.APP_VERSION,
        services=services
    )


@router.get("/")
async def root():
    """Root endpoint"""
    settings = get_settings()
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

