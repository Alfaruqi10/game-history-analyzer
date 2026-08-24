"""Security sanitizer for sensitive data"""
import re
import json
from typing import Any, Dict, List
from app.utils.logger import logger

SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
    "x-access-token",
}

SENSITIVE_JSON_KEYS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "session",
    "secret",
    "api_key",
    "apikey",
    "auth_token",
    "authorization",
    "bearer",
    "sid",
    "ssid",
    "lsid",
}


class Sanitizer:
    """Sanitizer for removing sensitive data"""
    
    @staticmethod
    def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
        """Sanitize HTTP headers"""
        sanitized = {}
        
        for key, value in headers.items():
            if key.lower() in SENSITIVE_HEADERS:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def sanitize_json(data: Any) -> Any:
        """Recursively sanitize JSON data"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key.lower() in SENSITIVE_JSON_KEYS:
                    sanitized[key] = "[REDACTED]"
                else:
                    sanitized[key] = Sanitizer.sanitize_json(value)
            return sanitized
        
        elif isinstance(data, list):
            return [Sanitizer.sanitize_json(item) for item in data]
        
        else:
            return data
    
    @staticmethod
    def sanitize_string(text: str) -> str:
        """Sanitize string for logging"""
        if not text:
            return text
        
        # Redact common patterns
        patterns = [
            (r"Bearer\s+\S+", "[REDACTED]"),
            (r"Authorization:\s+\S+", "[REDACTED]"),
            (r"token[=:]\s*['\"]?[^'\"\s]+['\"]?", "token=[REDACTED]"),
            (r"password[=:]\s*['\"]?[^'\"\s]+['\"]?", "password=[REDACTED]"),
        ]
        
        result = text
        for pattern, replacement in patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    @staticmethod
    def sanitize_for_logging(data: Any) -> str:
        """Sanitize data for logging"""
        if isinstance(data, str):
            return Sanitizer.sanitize_string(data)
        
        if isinstance(data, dict):
            sanitized = Sanitizer.sanitize_json(data)
            return json.dumps(sanitized, default=str)
        
        return str(data)


# Global sanitizer instance
sanitizer = Sanitizer()
