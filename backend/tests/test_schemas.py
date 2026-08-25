"""Test Pydantic schemas"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.game import GameSchema, GameCreateSchema
from app.schemas.game_round import GameRoundSchema, GameRoundImportSchema
from app.schemas.user import UserSchema


def test_game_create_schema_valid():
    """Test valid game creation schema"""
    game = GameCreateSchema(
        game_name="Test Game",
        provider="Test Provider",
        game_type="slot"
    )
    
    assert game.game_name == "Test Game"
    assert game.provider == "Test Provider"
    assert game.game_type == "slot"


def test_game_create_schema_missing_required():
    """Test game creation schema with missing required fields"""
    with pytest.raises(ValidationError):
        GameCreateSchema(
            provider="Test Provider",
            game_type="slot"
            # Missing game_name
        )


def test_game_round_import_schema_valid():
    """Test valid game round import schema"""
    round_data = GameRoundImportSchema(
        game="Test Game",
        round_id="ROUND001",
        timestamp=datetime.utcnow(),
        bet_amount=1000.0,
        win_amount=2500.0,
        currency="IDR"
    )
    
    assert round_data.game == "Test Game"
    assert round_data.bet_amount == 1000.0
    assert round_data.currency == "IDR"


def test_game_round_import_schema_missing_required():
    """Test game round import schema with missing required fields"""
    with pytest.raises(ValidationError):
        GameRoundImportSchema(
            game="Test Game",
            round_id="ROUND001",
            # Missing required fields
        )
