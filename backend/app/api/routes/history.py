"""History endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models import GameRound
from app.schemas.game_round import GameRoundSchema
from app.services.history_service import HistoryService
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history", response_model=dict)
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Dapatkan riwayat permainan dengan paginasi"""
    try:
        records, total = HistoryService.get_history_paginated(
            db,
            skip=skip,
            limit=limit
        )
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": r.id,
                    "external_round_id": r.external_round_id,
                    "timestamp": r.timestamp,
                    "bet_amount": r.bet_amount,
                    "win_amount": r.win_amount,
                    "multiplier": r.multiplier,
                    "currency": r.currency,
                    "result": r.result.value,
                    "game": r.game.game_name if r.game else None,
                    "provider": r.game.provider if r.game else None,
                }
                for r in records
            ]
        }
    
    except Exception as e:
        logger.error(f"Error mengambil riwayat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")


@router.get("/history/{history_id}", response_model=GameRoundSchema)
async def get_history_by_id(history_id: int, db: Session = Depends(get_db)):
    """Dapatkan detail riwayat berdasarkan ID"""
    try:
        record = HistoryService.get_round_by_id(db, history_id)
        
        if not record:
            raise HTTPException(status_code=404, detail="Record tidak ditemukan")
        
        return record
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error mengambil detail riwayat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")


@router.delete("/history")
async def delete_history(db: Session = Depends(get_db)):
    """Hapus semua riwayat permainan"""
    try:
        count = HistoryService.delete_all_history(db)
        return {
            "message": f"{count} record berhasil dihapus",
            "deleted_count": count
        }
    
    except Exception as e:
        logger.error(f"Error menghapus riwayat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")
