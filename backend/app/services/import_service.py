"""Service for importing data"""
from datetime import datetime
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.services.parser import Parser
from app.services.history_service import HistoryService
from app.utils.logger import logger


class ImportService:
    """Service for importing game history"""
    
    @staticmethod
    def import_from_json(
        db: Session,
        content: str,
        user_id: str = None
    ) -> Dict[str, Any]:
        """Import from JSON"""
        result = {
            "success": True,
            "total": 0,
            "saved": 0,
            "skipped": 0,
            "errors": [],
            "warnings": [],
        }
        
        try:
            # Parse JSON
            records = Parser.parse_json(content)
            result["total"] = len(records)
            
            # Process each record
            for i, raw_record in enumerate(records):
                is_valid, normalized, error = Parser.validate_and_normalize(raw_record)
                
                if not is_valid:
                    result["skipped"] += 1
                    result["errors"].append(f"Baris {i + 1}: {error}")
                    continue
                
                # Compute hash
                hash_value = Parser.compute_hash(normalized)
                
                # Get user
                rec_user_id = normalized.get("user_id") or user_id
                if rec_user_id:
                    user = HistoryService.get_or_create_user(db, rec_user_id)
                    user_db_id = user.id
                else:
                    user_db_id = None
                
                # Get game
                game = HistoryService.get_or_create_game(
                    db,
                    normalized["game"],
                    normalized.get("provider"),
                    "slot"  # Default game type
                )
                
                # Save round
                success, _, msg = HistoryService.save_game_round(
                    db,
                    user_db_id,
                    game.id,
                    normalized["round_id"],
                    normalized["timestamp"],
                    normalized["bet_amount"],
                    normalized["win_amount"],
                    normalized.get("multiplier"),
                    normalized["currency"],
                    normalized.get("result", "UNKNOWN"),
                    hash_value
                )
                
                if success:
                    result["saved"] += 1
                else:
                    result["skipped"] += 1
                    result["warnings"].append(f"Baris {i + 1}: {msg}")
        
        except Exception as e:
            logger.error(f"Error impor JSON: {str(e)}")
            result["success"] = False
            result["errors"].append(f"Kesalahan impor: {str(e)}")
        
        return result
    
    @staticmethod
    def import_from_csv(
        db: Session,
        content: str,
        user_id: str = None
    ) -> Dict[str, Any]:
        """Import from CSV"""
        result = {
            "success": True,
            "total": 0,
            "saved": 0,
            "skipped": 0,
            "errors": [],
            "warnings": [],
        }
        
        try:
            # Parse CSV
            records = Parser.parse_csv(content)
            result["total"] = len(records)
            
            # Process each record
            for i, raw_record in enumerate(records):
                is_valid, normalized, error = Parser.validate_and_normalize(raw_record)
                
                if not is_valid:
                    result["skipped"] += 1
                    result["errors"].append(f"Baris {i + 2}: {error}")  # +2 because header is row 1
                    continue
                
                # Compute hash
                hash_value = Parser.compute_hash(normalized)
                
                # Get user
                rec_user_id = normalized.get("user_id") or user_id
                if rec_user_id:
                    user = HistoryService.get_or_create_user(db, rec_user_id)
                    user_db_id = user.id
                else:
                    user_db_id = None
                
                # Get game
                game = HistoryService.get_or_create_game(
                    db,
                    normalized["game"],
                    normalized.get("provider"),
                    "slot"
                )
                
                # Save round
                success, _, msg = HistoryService.save_game_round(
                    db,
                    user_db_id,
                    game.id,
                    normalized["round_id"],
                    normalized["timestamp"],
                    normalized["bet_amount"],
                    normalized["win_amount"],
                    normalized.get("multiplier"),
                    normalized["currency"],
                    normalized.get("result", "UNKNOWN"),
                    hash_value
                )
                
                if success:
                    result["saved"] += 1
                else:
                    result["skipped"] += 1
                    result["warnings"].append(f"Baris {i + 2}: {msg}")
        
        except Exception as e:
            logger.error(f"Error impor CSV: {str(e)}")
            result["success"] = False
            result["errors"].append(f"Kesalahan impor: {str(e)}")
        
        return result
