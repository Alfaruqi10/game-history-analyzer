"""Test parser"""
import json
from datetime import datetime
from app.services.parser import Parser


def test_parse_json_array():
    """Test JSON array parsing"""
    data = [
        {
            "round_id": "ROUND1",
            "timestamp": "2026-08-24T10:00:00Z",
            "bet_amount": 1000,
            "win_amount": 2500,
            "game": "Example Game",
            "currency": "IDR",
            "result": "WIN"
        }
    ]
    
    json_str = json.dumps(data)
    parsed = Parser.parse_json(json_str)
    
    assert len(parsed) == 1
    assert parsed[0]["round_id"] == "ROUND1"


def test_parse_json_object():
    """Test JSON object parsing"""
    data = {
        "round_id": "ROUND1",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": 1000,
        "win_amount": 2500,
        "game": "Example Game",
        "currency": "IDR",
        "result": "WIN"
    }
    
    json_str = json.dumps(data)
    parsed = Parser.parse_json(json_str)
    
    assert len(parsed) == 1
    assert parsed[0]["round_id"] == "ROUND1"


def test_parse_invalid_json():
    """Test invalid JSON parsing"""
    json_str = "{invalid json}"
    
    try:
        Parser.parse_json(json_str)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "JSON tidak valid" in str(e) or "JSON" in str(e)


def test_parse_csv():
    """Test CSV parsing"""
    csv_content = """round_id,timestamp,bet_amount,win_amount,game,currency,result
ROUND1,2026-08-24T10:00:00Z,1000,2500,Example Game,IDR,WIN
ROUND2,2026-08-24T10:05:00Z,500,0,Example Game,IDR,LOSE"""
    
    parsed = Parser.parse_csv(csv_content)
    
    assert len(parsed) == 2
    assert parsed[0]["round_id"] == "ROUND1"
    assert parsed[1]["round_id"] == "ROUND2"


def test_parse_empty_csv():
    """Test empty CSV parsing"""
    csv_content = ""
    
    try:
        Parser.parse_csv(csv_content)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "kosong" in str(e).lower() or "csv" in str(e).lower()


def test_normalize_record():
    """Test record normalization"""
    raw = {
        "user_id": "12345",
        "game_name": "Example Game",
        "roundid": "ROUND1",
        "time": "2026-08-24T10:00:00Z",
        "bet": 1000,
        "win": 2500,
        "curr": "IDR",
        "outcome": "WIN"
    }
    
    normalized = Parser.normalize_record(raw)
    
    assert "game" in normalized
    assert "round_id" in normalized
    assert "timestamp" in normalized
    assert "bet_amount" in normalized
    assert "win_amount" in normalized


def test_validate_and_normalize_valid():
    """Test valid record validation and normalization"""
    raw = {
        "user_id": "12345",
        "game": "Test Game",
        "round_id": "ROUND1",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": 1000,
        "win_amount": 2500,
        "multiplier": 2.5,
        "currency": "IDR",
        "result": "WIN"
    }
    
    is_valid, normalized, error = Parser.validate_and_normalize(raw)
    
    assert is_valid == True
    assert error is None
    assert normalized["bet_amount"] == 1000
    assert normalized["currency"] == "IDR"


def test_validate_negative_bet():
    """Test validation of negative bet amount"""
    raw = {
        "user_id": "12345",
        "game": "Test Game",
        "round_id": "ROUND1",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": -1000,  # Invalid
        "win_amount": 2500,
        "currency": "IDR",
        "result": "WIN"
    }
    
    is_valid, normalized, error = Parser.validate_and_normalize(raw)
    
    assert is_valid == False
    assert "negatif" in error.lower() or "negative" in error.lower()


def test_compute_hash():
    """Test hash computation"""
    record = {
        "round_id": "ROUND1",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": 1000,
        "win_amount": 2500
    }
    
    hash1 = Parser.compute_hash(record)
    hash2 = Parser.compute_hash(record)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex is 64 characters


def test_hash_different_for_different_records():
    """Test that different records produce different hashes"""
    record1 = {
        "round_id": "ROUND1",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": 1000,
        "win_amount": 2500
    }
    
    record2 = {
        "round_id": "ROUND2",
        "timestamp": "2026-08-24T10:00:00Z",
        "bet_amount": 1000,
        "win_amount": 2500
    }
    
    hash1 = Parser.compute_hash(record1)
    hash2 = Parser.compute_hash(record2)
    
    assert hash1 != hash2
