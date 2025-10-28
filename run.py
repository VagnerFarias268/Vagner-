#!/usr/bin/env python
"""
Quick start script for development
"""
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          Vagner Sales Agent - Development Server          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Starting server...
  📍 Host: {HOST}:{PORT}
  🔧 Mode: {'DEBUG' if DEBUG else 'PRODUCTION'}
  📚 Docs: http://{HOST}:{PORT}/docs
  ❤️  Health: http://{HOST}:{PORT}/health

Press CTRL+C to stop
""")
    
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )

