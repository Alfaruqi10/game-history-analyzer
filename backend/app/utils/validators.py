"""Data validators"""
from datetime import datetime
from typing import Optional
import re


def validate_user_id(user_id: Optional[str]) -> Optional[str]:
    """Validate user ID format"""
    if not user_id:
        return None
    
    # User ID should be numeric or alphanumeric
    if not re.match(r"^[a-zA-Z0-9_-]+$", str(user_id)):
        raise ValueError(f"ID pengguna tidak valid: {user_id}")
    
    return str(user_id)


def validate_currency(currency: str) -> str:
    """Validate currency code"""
    if not currency or len(currency) != 3:
        raise ValueError(f"Kode mata uang tidak valid: {currency}")
    return currency.upper()


def validate_bet_amount(amount: float) -> float:
    """Validate bet amount"""
    if amount < 0:
        raise ValueError(f"Jumlah taruhan tidak boleh negatif: {amount}")
    return amount


def validate_win_amount(amount: float) -> float:
    """Validate win amount"""
    if amount < 0:
        raise ValueError(f"Jumlah kemenangan tidak boleh negatif: {amount}")
    return amount


def validate_multiplier(multiplier: Optional[float]) -> Optional[float]:
    """Validate multiplier"""
    if multiplier is None:
        return None
    
    if multiplier < 0:
        raise ValueError(f"Multiplier tidak boleh negatif: {multiplier}")
    
    return multiplier


def validate_timestamp(timestamp: datetime) -> datetime:
    """Validate timestamp"""
    if not isinstance(timestamp, datetime):
        raise ValueError(f"Format waktu tidak valid")
    return timestamp
