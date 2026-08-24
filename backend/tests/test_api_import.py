"""Test import endpoint"""
import json
from fastapi.testclient import TestClient
from app.main import app


def test_import_json_valid():
    """Test importing valid JSON"""
    client = TestClient(app)
    
    data = [
        {
            "user_id": "12345",
            "game": "Test Game",
            "provider": "Test Provider",
            "round_id": "ROUND_TEST_001",
            "timestamp": "2026-08-24T10:00:00Z",
            "bet_amount": 1000,
            "win_amount": 2500,
            "multiplier": 2.5,
            "currency": "IDR",
            "result": "WIN"
        }
    ]
    
    json_content = json.dumps(data).encode()
    
    response = client.post(
        "/api/history/import",
        files={"file": ("data.json", json_content, "application/json")},
        data={"user_id": "12345"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["total"] == 1
    assert result["saved"] >= 0
    assert "errors" in result
    assert "warnings" in result


def test_import_csv_valid():
    """Test importing valid CSV"""
    client = TestClient(app)
    
    csv_content = b"""user_id,game,provider,round_id,timestamp,bet_amount,win_amount,multiplier,currency,result
12345,Test Game,Test Provider,ROUND_TEST_002,2026-08-24T10:00:00Z,1000,2500,2.5,IDR,WIN"""
    
    response = client.post(
        "/api/history/import",
        files={"file": ("data.csv", csv_content, "text/csv")},
        data={"user_id": "12345"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["total"] == 1


def test_import_unsupported_format():
    """Test importing unsupported format"""
    client = TestClient(app)
    
    content = b"some content"
    
    response = client.post(
        "/api/history/import",
        files={"file": ("data.txt", content, "text/plain")},
        data={"user_id": "12345"}
    )
    
    assert response.status_code == 400
    assert "tidak didukung" in response.json()["detail"].lower()


def test_import_invalid_json():
    """Test importing invalid JSON"""
    client = TestClient(app)
    
    json_content = b"{invalid json"
    
    response = client.post(
        "/api/history/import",
        files={"file": ("data.json", json_content, "application/json")},
        data={"user_id": "12345"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == False or len(result["errors"]) > 0
