"""Test database models"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.database.connection import Base
from app.database.models import User, Game, GameRound, ResultEnum, CollectionRun


@pytest.fixture
def test_db():
    """Create test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_create_user(test_db):
    """Test creating a user"""
    user = User(
        external_user_id="test_user_123",
        username="testuser"
    )
    test_db.add(user)
    test_db.commit()
    
    assert user.id is not None
    assert user.external_user_id == "test_user_123"
    assert user.username == "testuser"


def test_create_game(test_db):
    """Test creating a game"""
    game = Game(
        game_name="Test Game",
        provider="Test Provider",
        game_type="slot"
    )
    test_db.add(game)
    test_db.commit()
    
    assert game.id is not None
    assert game.game_name == "Test Game"
    assert game.provider == "Test Provider"


def test_create_game_round(test_db):
    """Test creating a game round"""
    user = User(external_user_id="user1", username="user1")
    game = Game(game_name="Game1", provider="Provider1", game_type="slot")
    
    test_db.add(user)
    test_db.add(game)
    test_db.commit()
    
    round_obj = GameRound(
        user_id=user.id,
        game_id=game.id,
        external_round_id="ROUND001",
        timestamp=datetime.utcnow(),
        bet_amount=1000.0,
        win_amount=2500.0,
        multiplier=2.5,
        currency="IDR",
        result=ResultEnum.WIN,
        raw_data_hash="abc123def456"
    )
    
    test_db.add(round_obj)
    test_db.commit()
    
    assert round_obj.id is not None
    assert round_obj.external_round_id == "ROUND001"
    assert round_obj.result == ResultEnum.WIN


def test_result_enum():
    """Test result enum values"""
    assert ResultEnum.WIN.value == "WIN"
    assert ResultEnum.LOSE.value == "LOSE"
    assert ResultEnum.DRAW.value == "DRAW"
    assert ResultEnum.UNKNOWN.value == "UNKNOWN"
