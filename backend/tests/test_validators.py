"""Test validators"""
import pytest
from app.utils.validators import (
    validate_user_id,
    validate_currency,
    validate_bet_amount,
    validate_win_amount,
    validate_multiplier,
)


def test_validate_user_id_valid():
    """Test valid user ID"""
    assert validate_user_id("12345") == "12345"
    assert validate_user_id("user_123") == "user_123"
    assert validate_user_id("user-123") == "user-123"


def test_validate_user_id_none():
    """Test None user ID"""
    assert validate_user_id(None) is None


def test_validate_user_id_invalid():
    """Test invalid user ID"""
    with pytest.raises(ValueError):
        validate_user_id("user@invalid")


def test_validate_currency_valid():
    """Test valid currency"""
    assert validate_currency("IDR") == "IDR"
    assert validate_currency("idr") == "IDR"
    assert validate_currency("usd") == "USD"


def test_validate_currency_invalid():
    """Test invalid currency"""
    with pytest.raises(ValueError):
        validate_currency("IDRI")  # Too long
    
    with pytest.raises(ValueError):
        validate_currency("ID")  # Too short


def test_validate_bet_amount_valid():
    """Test valid bet amount"""
    assert validate_bet_amount(1000) == 1000
    assert validate_bet_amount(0) == 0
    assert validate_bet_amount(999.99) == 999.99


def test_validate_bet_amount_negative():
    """Test negative bet amount"""
    with pytest.raises(ValueError):
        validate_bet_amount(-1000)


def test_validate_win_amount_valid():
    """Test valid win amount"""
    assert validate_win_amount(1000) == 1000
    assert validate_win_amount(0) == 0
    assert validate_win_amount(999.99) == 999.99


def test_validate_win_amount_negative():
    """Test negative win amount"""
    with pytest.raises(ValueError):
        validate_win_amount(-1000)


def test_validate_multiplier_valid():
    """Test valid multiplier"""
    assert validate_multiplier(2.5) == 2.5
    assert validate_multiplier(0) == 0
    assert validate_multiplier(None) is None


def test_validate_multiplier_negative():
    """Test negative multiplier"""
    with pytest.raises(ValueError):
        validate_multiplier(-1.5)
