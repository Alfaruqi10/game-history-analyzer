"""Test games endpoint"""
from fastapi.testclient import TestClient
from app.main import app


def test_list_games():
    """Test listing games"""
    client = TestClient(app)
    response = client.get("/api/games")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_game():
    """Test creating a game"""
    client = TestClient(app)
    
    game_data = {
        "game_name": "Test Game 1",
        "provider": "Test Provider",
        "game_type": "slot"
    }
    
    response = client.post("/api/games", json=game_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["game_name"] == "Test Game 1"
    assert data["provider"] == "Test Provider"
    assert data["game_type"] == "slot"
    assert "id" in data


def test_create_duplicate_game():
    """Test creating duplicate game"""
    client = TestClient(app)
    
    game_data = {
        "game_name": "Duplicate Game",
        "provider": "Test Provider",
        "game_type": "slot"
    }
    
    # First creation should succeed
    response1 = client.post("/api/games", json=game_data)
    assert response1.status_code == 200
    
    # Duplicate should fail
    response2 = client.post("/api/games", json=game_data)
    assert response2.status_code == 409
    assert "sudah ada" in response2.json()["detail"].lower()
