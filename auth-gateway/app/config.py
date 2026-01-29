"""
Configuration settings for Auth Gateway
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Database
    DATABASE_URL: str = "sqlite:///./auth_gateway.db"

    # ML APIs
    PHISHING_API_URL: str = "http://localhost:8000"
    ATO_API_URL: str = "http://localhost:8001"
    BRUTE_FORCE_API_URL: str = "http://localhost:8002"

    # File Upload
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


# Alert Thresholds by Model (confidence percentage 0-100)
# Based on model performance:
# - Phishing: F1 99.01% - high precision, can use higher threshold
# - ATO: F1 75.86% - lower precision, more conservative thresholds
# - Brute Force: F1 99.97% - very high precision, highest thresholds
ALERT_THRESHOLDS = {
    "phishing": {
        "critical": 95.0,  # >= 95% confidence
        "high": 85.0,      # >= 85% confidence
        "medium": 75.0     # >= 75% confidence
    },
    "ato": {
        "critical": 90.0,  # Lower due to 75.86% F1
        "high": 80.0,
        "medium": 70.0
    },
    "brute_force": {
        "critical": 98.0,  # Higher due to 99.97% F1
        "high": 90.0,
        "medium": 80.0
    }
}

# Default thresholds for unknown models
DEFAULT_ALERT_THRESHOLDS = {
    "critical": 95.0,
    "high": 85.0,
    "medium": 70.0
}
