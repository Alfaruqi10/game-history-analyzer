"""History service for database operations"""
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import User, Game, GameRound, CollectionRun, ResultEnum
from app.utils.logger import logger


class HistoryService:
    """Service for managing game history"""
    
    @staticmethod
    def get_or_create_user(
        db: Session,
        external_user_id: str,
        username: str = None
    ) -> User:
        """Get or create a user"""
        user = db.query(User).filter(User.external_user_id == external_user_id).first()
        
        if not user:
            user = User(
                external_user_id=external_user_id,
                username=username or external_user_id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Pengguna baru dibuat: {external_user_id}")
        
        return user
    
    @staticmethod
    def get_or_create_game(
        db: Session,
        game_name: str,
        provider: str = None,
        game_type: str = None
    ) -> Game:
        """Get or create a game"""
        game = db.query(Game).filter(Game.game_name == game_name).first()
        
        if not game:
            game = Game(
                game_name=game_name,
                provider=provider,
                game_type=game_type
            )
            db.add(game)
            db.commit()
            db.refresh(game)
            logger.info(f"Permainan baru dibuat: {game_name}")
        
        return game
    
    @staticmethod
    def save_game_round(
        db: Session,
        user_id: Optional[int],
        game_id: int,
        external_round_id: str,
        timestamp: datetime,
        bet_amount: float,
        win_amount: float,
        multiplier: Optional[float],
        currency: str,
        result: str,
        raw_data_hash: str
    ) -> Tuple[bool, GameRound, str]:
        """
        Save a game round
        
        Returns: (success, round_object, message)
        """
        try:
            # Check for duplicate
            existing = db.query(GameRound).filter(
                GameRound.raw_data_hash == raw_data_hash
            ).first()
            
            if existing:
                return False, None, "Duplikat: Record sudah ada"
            
            # Map result
            try:
                result_enum = ResultEnum(result.upper())
            except ValueError:
                result_enum = ResultEnum.UNKNOWN
            
            # Create round
            round_obj = GameRound(
                user_id=user_id,
                game_id=game_id,
                external_round_id=external_round_id,
                timestamp=timestamp,
                bet_amount=bet_amount,
                win_amount=win_amount,
                multiplier=multiplier,
                currency=currency,
                result=result_enum,
                raw_data_hash=raw_data_hash
            )
            
            db.add(round_obj)
            db.commit()
            db.refresh(round_obj)
            
            return True, round_obj, "Tersimpan"
        
        except Exception as e:
            db.rollback()
            logger.error(f"Error menyimpan round: {str(e)}")
            return False, None, f"Gagal: {str(e)}"
    
    @staticmethod
    def get_history_paginated(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        user_id: Optional[int] = None,
        game_id: Optional[int] = None
    ) -> Tuple[List[GameRound], int]:
        """Get paginated history"""
        query = db.query(GameRound)
        
        if user_id:
            query = query.filter(GameRound.user_id == user_id)
        
        if game_id:
            query = query.filter(GameRound.game_id == game_id)
        
        total = query.count()
        
        records = query.order_by(desc(GameRound.timestamp)).offset(skip).limit(limit).all()
        
        return records, total
    
    @staticmethod
    def get_round_by_id(db: Session, round_id: int) -> Optional[GameRound]:
        """Get a single round by ID"""
        return db.query(GameRound).filter(GameRound.id == round_id).first()
    
    @staticmethod
    def delete_all_history(db: Session) -> int:
        """Delete all game history"""
        try:
            count = db.query(GameRound).delete()
            db.commit()
            logger.info(f"Dihapus {count} record histori")
            return count
        
        except Exception as e:
            db.rollback()
            logger.error(f"Error menghapus history: {str(e)}")
            return 0
    
    @staticmethod
    def create_collection_run(
        db: Session,
        status: str = "PENDING"
    ) -> CollectionRun:
        """Create a collection run"""
        run = CollectionRun(status=status)
        db.add(run)
        db.commit()
        db.refresh(run)
        return run
    
    @staticmethod
    def update_collection_run(
        db: Session,
        run_id: int,
        status: str = None,
        records_found: int = None,
        records_saved: int = None,
        records_skipped: int = None,
        error_message: str = None,
        finished_at: datetime = None
    ) -> CollectionRun:
        """Update a collection run"""
        run = db.query(CollectionRun).filter(CollectionRun.id == run_id).first()
        
        if run:
            if status:
                run.status = status
            if records_found is not None:
                run.records_found = records_found
            if records_saved is not None:
                run.records_saved = records_saved
            if records_skipped is not None:
                run.records_skipped = records_skipped
            if error_message:
                run.error_message = error_message
            if finished_at:
                run.finished_at = finished_at
            
            db.commit()
            db.refresh(run)
        
        return run
