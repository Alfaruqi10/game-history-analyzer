"""Data parsers for CSV and JSON"""
import json
import csv
import hashlib
from io import StringIO
from datetime import datetime
from typing import List, Dict, Any
from pydantic import ValidationError
from app.schemas.game_round import GameRoundImportSchema
from app.utils.validators import (
    validate_user_id,
    validate_currency,
    validate_bet_amount,
    validate_win_amount,
    validate_multiplier,
    validate_timestamp,
)
from app.utils.logger import logger


class Parser:
    """Parser for import data"""
    
    @staticmethod
    def parse_json(content: str) -> List[Dict[str, Any]]:
        """Parse JSON content"""
        try:
            data = json.loads(content)
            
            if isinstance(data, dict):
                # If it's a single object, wrap it in a list
                data = [data]
            
            if not isinstance(data, list):
                raise ValueError("JSON harus berupa array atau objek")
            
            return data
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Format JSON tidak valid: {str(e)}")
    
    @staticmethod
    def parse_csv(content: str) -> List[Dict[str, Any]]:
        """Parse CSV content"""
        try:
            f = StringIO(content)
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                raise ValueError("CSV kosong atau tidak memiliki header")
            
            rows = []
            for i, row in enumerate(reader, start=2):  # Start from 2 (header is 1)
                # Remove empty values
                row = {k: v for k, v in row.items() if v}
                if row:  # Only add non-empty rows
                    rows.append(row)
            
            return rows
        
        except Exception as e:
            raise ValueError(f"Format CSV tidak valid: {str(e)}")
    
    @staticmethod
    def normalize_record(raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw record to standard format"""
        
        # Map possible field names to standard names
        field_mappings = {
            "user_id": ["user_id", "userid", "user", "account", "id"],
            "game": ["game", "game_name", "gamename", "product"],
            "provider": ["provider", "game_provider", "platform"],
            "round_id": ["round_id", "roundid", "round", "transaction_id"],
            "timestamp": ["timestamp", "time", "date", "created_at", "played_at"],
            "bet_amount": ["bet_amount", "betamount", "bet", "wager"],
            "win_amount": ["win_amount", "winamount", "win", "payout", "winnings"],
            "multiplier": ["multiplier", "mult", "factor"],
            "currency": ["currency", "curr", "coin"],
            "result": ["result", "outcome", "status"],
        }
        
        normalized = {}
        
        for standard_key, possible_names in field_mappings.items():
            for possible_name in possible_names:
                if possible_name in raw_record:
                    normalized[standard_key] = raw_record[possible_name]
                    break
        
        # Convert timestamp if needed
        if "timestamp" in normalized:
            ts_value = normalized["timestamp"]
            if isinstance(ts_value, str):
                try:
                    # Try ISO format first
                    normalized["timestamp"] = datetime.fromisoformat(ts_value.replace("Z", "+00:00"))
                except:
                    try:
                        # Try common formats
                        for fmt in ["%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S"]:
                            try:
                                normalized["timestamp"] = datetime.strptime(ts_value, fmt)
                                break
                            except ValueError:
                                continue
                    except:
                        pass
        
        return normalized
    
    @staticmethod
    def validate_and_normalize(
        raw_record: Dict[str, Any]
    ) -> tuple[bool, Dict[str, Any], str]:
        """
        Validate and normalize a record
        
        Returns: (is_valid, normalized_record, error_message)
        """
        try:
            # Normalize
            normalized = Parser.normalize_record(raw_record)
            
            # Validate with Pydantic
            validated = GameRoundImportSchema(**normalized)
            
            # Convert to dict
            record_dict = validated.model_dump()
            
            # Additional validation
            if record_dict.get("bet_amount"):
                validate_bet_amount(record_dict["bet_amount"])
            
            if record_dict.get("win_amount"):
                validate_win_amount(record_dict["win_amount"])
            
            if record_dict.get("multiplier"):
                validate_multiplier(record_dict["multiplier"])
            
            if record_dict.get("currency"):
                validate_currency(record_dict["currency"])
            
            return True, record_dict, None
        
        except ValidationError as e:
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            return False, {}, f"Validasi gagal: {errors}"
        
        except ValueError as e:
            return False, {}, f"Nilai tidak valid: {str(e)}"
        
        except Exception as e:
            return False, {}, f"Kesalahan: {str(e)}"
    
    @staticmethod
    def compute_hash(record: Dict[str, Any]) -> str:
        """Compute hash for duplicate detection"""
        # Use key fields for hashing
        key_fields = [
            str(record.get("round_id", "")),
            str(record.get("timestamp", "")),
            str(record.get("bet_amount", "")),
            str(record.get("win_amount", "")),
        ]
        
        hash_input = "|".join(key_fields)
        return hashlib.sha256(hash_input.encode()).hexdigest()
