"""Health check endpoint"""
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "Sehat",
        "message": "Backend Game History Analyzer berjalan normal"
    }
