"""
FastAPI application entry point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv

from app.api.routes import webhook, health
from app.core.kb.manager import init_pinecone_if_needed

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings from environment
APP_NAME = os.getenv("APP_NAME", "Vagner Sales Agent")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8001"))

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="WhatsApp AI Sales Agent with voice support and knowledge base",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(webhook.router, tags=["Webhook"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Ensure folders exist
    temp_folder = os.getenv("TEMP_FOLDER", "materials/temp")
    media_folder = os.getenv("MEDIA_FOLDER", "materials/media")
    pdf_folder = os.getenv("PDF_FOLDER", "materials/pdfs")
    
    for folder in [temp_folder, media_folder, pdf_folder]:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Folder ready: {folder}")
    
    logger.info("✅ Folders initialized")
    
    # Initialize Pinecone
    try:
        init_pinecone_if_needed()
        logger.info("✅ Pinecone initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Pinecone: {e}")
        raise
    
    logger.info(f"🚀 Application started successfully on {HOST}:{PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )

