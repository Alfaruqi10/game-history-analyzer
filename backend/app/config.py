"""Konfigurasi aplikasi"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pengaturan aplikasi"""
    
    # Database
    database_url: str = "sqlite:///./data/app.db"
    
    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_version: str = "v1"
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    # Data
    data_dir: str = "./data"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Ensure data directory exists
Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
