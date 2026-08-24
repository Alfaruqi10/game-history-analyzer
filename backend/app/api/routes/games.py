"""Games endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models import Game
from app.schemas.game import GameSchema, GameCreateSchema
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["games"])


@router.get("/games", response_model=list[GameSchema])
async def list_games(db: Session = Depends(get_db)):
    """Daftar semua permainan"""
    try:
        games = db.query(Game).all()
        return games
    except Exception as e:
        logger.error(f"Error mengambil daftar permainan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")


@router.post("/games", response_model=GameSchema)
async def create_game(game: GameCreateSchema, db: Session = Depends(get_db)):
    """Buat permainan baru"""
    try:
        # Check if exists
        existing = db.query(Game).filter(Game.game_name == game.game_name).first()
        if existing:
            raise HTTPException(status_code=409, detail="Permainan sudah ada")
        
        db_game = Game(
            game_name=game.game_name,
            provider=game.provider,
            game_type=game.game_type
        )
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        
        logger.info(f"Permainan baru dibuat: {game.game_name}")
        return db_game
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error membuat permainan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")
