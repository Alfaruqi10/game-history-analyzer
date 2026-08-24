"""Test sanitizer"""
from app.services.sanitizer import Sanitizer


def test_sanitize_headers():
    """Test header sanitization"""
    headers = {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json",
        "Cookie": "session=abc123"
    }
    
    sanitized = Sanitizer.sanitize_headers(headers)
    
    assert sanitized["Authorization"] == "[REDACTED]"
    assert sanitized["Content-Type"] == "application/json"
    assert sanitized["Cookie"] == "[REDACTED]"


def test_sanitize_json():
    """Test JSON sanitization"""
    data = {
        "username": "john",
        "password": "secret123",
        "token": "abc123",
        "api_key": "xyz789"
    }
    
    sanitized = Sanitizer.sanitize_json(data)
    
    assert sanitized["username"] == "john"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["token"] == "[REDACTED]"
    assert sanitized["api_key"] == "[REDACTED]"


def test_sanitize_nested_json():
    """Test nested JSON sanitization"""
    data = {
        "user": {
            "name": "john",
            "password": "secret"
        },
        "tokens": ["token1", "token2"]
    }
    
    sanitized = Sanitizer.sanitize_json(data)
    
    assert sanitized["user"]["name"] == "john"
    assert sanitized["user"]["password"] == "[REDACTED]"


def test_sanitize_string():
    """Test string sanitization"""
    text = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    
    sanitized = Sanitizer.sanitize_string(text)
    
    assert "[REDACTED]" in sanitized
    assert "Bearer" not in sanitized or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in sanitized


def test_no_credential_exposure():
    """Ensure credentials are never exposed"""
    sensitive_data = {
        "password": "my_password_123",
        "api_key": "sk_live_51234567890",
        "session_id": "sess_abc123xyz",
        "authorization": "Bearer token_xyz"
    }
    
    sanitized = Sanitizer.sanitize_json(sensitive_data)
    
    for value in sanitized.values():
        assert value == "[REDACTED]"
        assert "my_password_123" not in str(sanitized)
        assert "sk_live_51234567890" not in str(sanitized)
        assert "token_xyz" not in str(sanitized)
