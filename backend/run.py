"""Main application entry point"""
import os
import sys
from pathlib import Path

# Ensure data directory exists
data_dir = Path("./data")
data_dir.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    print("\n" + "="*60)
    print("🎮 Game History Analyzer - Backend API")
    print("="*60)
    print(f"📍 Running at: http://{settings.api_host}:{settings.api_port}")
    print(f"📚 API Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"💾 Database: {settings.database_url}")
    print("="*60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
