"""API routes"""
from fastapi import APIRouter
from .routes import health, games, history, import_data

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(games.router)
api_router.include_router(history.router)
api_router.include_router(import_data.router)
