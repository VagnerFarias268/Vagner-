#!/usr/bin/env python
"""
Quick start script for development
"""
import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          Vagner Sales Agent - Development Server          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Starting server...
  📍 Host: {settings.HOST}:{settings.PORT}
  🔧 Mode: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}
  📚 Docs: http://{settings.HOST}:{settings.PORT}/docs
  ❤️  Health: http://{settings.HOST}:{settings.PORT}/health

Press CTRL+C to stop
""")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

