"""
Prediction schemas
"""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class PredictionCreate(BaseModel):
    model_config = {"protected_namespaces": ()}

    model_type: str  # 'phishing', 'ato', 'brute_force'
    prediction: int  # 0=benign, 1=threat
    prediction_label: str
    confidence: float
    input_data: Optional[dict[str, Any]] = None
    explanation: Optional[dict[str, Any]] = None


class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": (), "from_attributes": True}

    id: int
    model_type: str
    prediction: int
    prediction_label: str
    confidence: float
    created_at: datetime
    created_by_name: Optional[str] = None


class PredictionStats(BaseModel):
    total_predictions: int
    threats_detected: int
    benign_count: int
    avg_confidence: float
    by_model: dict[str, dict[str, int]]
