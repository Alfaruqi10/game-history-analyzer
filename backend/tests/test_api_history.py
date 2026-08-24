"""Test history endpoint"""
from fastapi.testclient import TestClient
from app.main import app


def test_get_empty_history():
    """Test getting empty history"""
    client = TestClient(app)
    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert "skip" in data
    assert "limit" in data
    assert data["total"] == 0
    assert len(data["data"]) == 0


def test_get_history_pagination():
    """Test history pagination"""
    client = TestClient(app)
    
    # Test with skip and limit
    response = client.get("/api/history?skip=0&limit=25")
    
    assert response.status_code == 200
    data = response.json()
    assert data["skip"] == 0
    assert data["limit"] == 25


def test_get_history_invalid_limit():
    """Test history with invalid limit"""
    client = TestClient(app)
    
    # Limit > 100 should be rejected
    response = client.get("/api/history?limit=150")
    assert response.status_code == 422  # Validation error


def test_delete_history():
    """Test deleting history"""
    client = TestClient(app)
    response = client.delete("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    assert "deleted_count" in data
    assert isinstance(data["deleted_count"], int)
