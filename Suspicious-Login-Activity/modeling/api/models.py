"""
Pydantic models for Account Takeover Detection API request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class LoginInput(BaseModel):
    """Schema for single login prediction request."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "ip_address": "192.168.1.100",
                "country": "US",
                "region": "California",
                "city": "San Francisco",
                "browser": "Chrome 120.0",
                "os": "Windows 10",
                "device": "Desktop",
                "login_successful": 1,
                "is_attack_ip": 0,
                "asn": 15169,
                "rtt": 45.5,
                "login_timestamp": "2026-01-15T10:30:00Z"
            }
        }
    }

    user_id: str = Field(..., description="User ID", min_length=1)
    ip_address: str = Field(..., description="IP address", min_length=1)
    country: str = Field(..., description="Country code (e.g., 'US', 'RO')", min_length=2, max_length=2)
    region: str = Field(..., description="Region/State", min_length=1)
    city: str = Field(..., description="City name", min_length=1)
    browser: str = Field(..., description="Browser name and version", min_length=1)
    os: str = Field(..., description="Operating system name and version", min_length=1)
    device: str = Field(..., description="Device type (e.g., 'Desktop', 'Mobile')", min_length=1)
    login_successful: int = Field(..., description="Login success (1) or failure (0)", ge=0, le=1)
    is_attack_ip: int = Field(..., description="Whether IP is known attack IP (1) or not (0)", ge=0, le=1)
    asn: int = Field(..., description="Autonomous System Number", ge=0)
    rtt: float = Field(..., description="Round-Trip Time in milliseconds", ge=0)
    login_timestamp: Optional[str] = Field(
        default=None,
        description="Login timestamp (ISO format). If not provided, current time will be used."
    )

    @field_validator('login_successful', 'is_attack_ip')
    @classmethod
    def validate_binary(cls, v):
        """Validate binary fields are 0 or 1."""
        if v not in [0, 1]:
            raise ValueError("Must be 0 or 1")
        return v


class RiskIndicator(BaseModel):
    """Single risk indicator with evidence."""
    indicator: str = Field(..., description="Description of the risk indicator")
    evidence: List[str] = Field(default=[], description="Evidence supporting this indicator")
    severity: Optional[str] = Field(default="medium", description="Severity level: critical, high, medium, low")


class ATOExplanation(BaseModel):
    """Explanation for account takeover prediction - why the model flagged this login."""
    risk_indicators: List[RiskIndicator] = Field(default=[], description="List of risk indicators detected with evidence")
    risk_factors: dict = Field(default={}, description="Risk factor contributions (feature: weight)")
    key_features: dict = Field(default={}, description="Key feature values that influenced the prediction")
    geo_info: Optional[dict] = Field(default=None, description="Geographic information about the login")
    summary: str = Field(..., description="Human-readable summary of the prediction reasoning")
    total_indicators: Optional[int] = Field(default=0, description="Total number of indicators detected")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_indicators": [
                    {
                        "indicator": "Cambio de pais detectado",
                        "evidence": ["Pais anterior: US", "Pais actual: RO"],
                        "severity": "high"
                    },
                    {
                        "indicator": "Cambio de direccion IP",
                        "evidence": ["IP anterior: 192.168.1.1", "IP actual: 89.46.23.10"],
                        "severity": "medium"
                    }
                ],
                "risk_factors": {
                    "country_changed": 0.35,
                    "ip_changed": 0.15,
                    "is_night": 0.10
                },
                "key_features": {
                    "country_changed": True,
                    "ip_changed": True,
                    "is_night": True,
                    "is_attack_ip": False
                },
                "geo_info": {
                    "country": "RO",
                    "region": "Bucharest",
                    "city": "Bucharest",
                    "asn": 9050
                },
                "summary": "Login de alto riesgo: 2 indicadores detectados (1 criticos).",
                "total_indicators": 2
            }
        }


class PredictionMetadata(BaseModel):
    """Metadata for prediction response."""
    model_config = {"protected_namespaces": ()}  # Allow fields starting with "model_"

    model: str = Field(..., description="Model name used for prediction")
    features_count: int = Field(..., description="Total number of features used")
    threshold: float = Field(..., description="Classification threshold used")
    timestamp: str = Field(..., description="Prediction timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class PredictionResponse(BaseModel):
    """Schema for single login prediction response."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "prediction": 1,
                "prediction_label": "Account Takeover",
                "confidence": 0.8521,
                "probability_normal": 0.1479,
                "probability_ato": 0.8521,
                "risk_score": 85.21,
                "explanation": {
                    "behavioral_changes": [
                        "Country change detected",
                        "IP address change detected"
                    ],
                    "risk_factors": {
                        "country_changed": 0.35,
                        "ip_changed": 0.15
                    },
                    "key_features": {
                        "country_changed": True,
                        "ip_changed": True
                    },
                    "summary": "Login de alto riesgo: 2 cambios de comportamiento detectados."
                },
                "metadata": {
                    "model": "Gradient Boosting",
                    "features_count": 35,
                    "threshold": 0.0041,
                    "timestamp": "2026-01-15T15:30:45.123Z",
                    "processing_time_ms": 12.5
                }
            }
        }
    }

    prediction: int = Field(..., description="Prediction result (0=Normal, 1=Account Takeover)")
    prediction_label: str = Field(..., description="Human-readable prediction label")
    confidence: float = Field(..., description="Confidence score for prediction (0.0-1.0)")
    probability_normal: float = Field(..., description="Probability of being normal login")
    probability_ato: float = Field(..., description="Probability of being account takeover")
    risk_score: float = Field(..., description="Risk score (0-100, higher is riskier)")
    explanation: ATOExplanation = Field(..., description="Explanation of why this prediction was made")
    metadata: PredictionMetadata = Field(..., description="Prediction metadata")


class BatchLoginInput(BaseModel):
    """Schema for batch login prediction request."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "logins": [
                    {
                        "user_id": "user123",
                        "ip_address": "192.168.1.100",
                        "country": "US",
                        "region": "California",
                        "city": "San Francisco",
                        "browser": "Chrome 120.0",
                        "os": "Windows 10",
                        "device": "Desktop",
                        "login_successful": 1,
                        "is_attack_ip": 0,
                        "asn": 15169,
                        "rtt": 45.5
                    },
                    {
                        "user_id": "user456",
                        "ip_address": "89.46.23.10",
                        "country": "RO",
                        "region": "Bucharest",
                        "city": "Bucharest",
                        "browser": "Firefox 115.0",
                        "os": "Linux",
                        "device": "Desktop",
                        "login_successful": 1,
                        "is_attack_ip": 1,
                        "asn": 9050,
                        "rtt": 673.2
                    }
                ]
            }
        }
    }

    logins: List[LoginInput] = Field(..., description="List of logins to predict", min_length=1)


class SingleBatchPrediction(BaseModel):
    """Schema for single prediction in batch response."""
    login_index: int = Field(..., description="Index of login in batch")
    user_id: str = Field(..., description="User ID")
    prediction: int = Field(..., description="Prediction result (0=Normal, 1=Account Takeover)")
    prediction_label: str = Field(..., description="Human-readable prediction label")
    confidence: float = Field(..., description="Confidence score for prediction")
    risk_score: float = Field(..., description="Risk score (0-100)")
    explanation: ATOExplanation = Field(..., description="Explanation of why this prediction was made")


class BatchMetadata(BaseModel):
    """Metadata for batch prediction response."""
    model_config = {"protected_namespaces": ()}  # Allow fields starting with "model_"

    total_logins: int = Field(..., description="Total number of logins processed")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")
    model: str = Field(..., description="Model name used")


class BatchPredictionResponse(BaseModel):
    """Schema for batch login prediction response."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "predictions": [
                    {
                        "login_index": 0,
                        "user_id": "user123",
                        "prediction": 0,
                        "prediction_label": "Normal",
                        "confidence": 0.9523,
                        "risk_score": 4.77
                    },
                    {
                        "login_index": 1,
                        "user_id": "user456",
                        "prediction": 1,
                        "prediction_label": "Account Takeover",
                        "confidence": 0.8521,
                        "risk_score": 85.21
                    }
                ],
                "metadata": {
                    "total_logins": 2,
                    "processing_time_ms": 25.8,
                    "model": "Gradient Boosting"
                }
            }
        }
    }

    predictions: List[SingleBatchPrediction] = Field(..., description="List of predictions")
    metadata: BatchMetadata = Field(..., description="Batch processing metadata")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    model_config = {
        "protected_namespaces": (),  # Allow fields starting with "model_"
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "message": "Account Takeover Detection API",
                "model": "Gradient Boosting",
                "version": "1.0.0"
            }
        }
    }

    status: str = Field(..., description="API status")
    message: str = Field(..., description="API message")
    model: str = Field(..., description="Model name in use")
    version: str = Field(..., description="API version")


class ModelMetrics(BaseModel):
    """Model performance metrics."""
    f1_score: float = Field(..., description="F1 score")
    accuracy: float = Field(..., description="Accuracy")
    precision: float = Field(..., description="Precision")
    recall: float = Field(..., description="Recall")
    roc_auc: float = Field(..., description="ROC-AUC score")
    auc_pr: float = Field(..., description="AUC-PR score")


class ModelFeatures(BaseModel):
    """Model features information."""
    total: int = Field(..., description="Total number of features")
    temporal: int = Field(..., description="Number of temporal features")
    behavioral: int = Field(..., description="Number of behavioral features")
    aggregated: int = Field(..., description="Number of aggregated features")
    categorical: int = Field(..., description="Number of categorical features")
    numeric: int = Field(..., description="Number of numeric features")


class TrainingData(BaseModel):
    """Training data information."""
    total_samples: int = Field(..., description="Total number of samples")
    train_samples: int = Field(..., description="Number of training samples")
    test_samples: int = Field(..., description="Number of test samples")
    ato_samples: int = Field(..., description="Number of ATO samples in test set")
    normal_samples: int = Field(..., description="Number of normal samples in test set")


class ThresholdInfo(BaseModel):
    """Threshold information."""
    optimal_threshold: float = Field(..., description="Optimal classification threshold")
    default_threshold: float = Field(..., description="Default threshold (0.5)")
    f1_improvement_pct: float = Field(..., description="F1-Score improvement percentage")


class ModelInfoResponse(BaseModel):
    """Schema for model info response."""
    model_config = {
        "protected_namespaces": (),  # Allow fields starting with "model_"
        "json_schema_extra": {
            "example": {
                "model_name": "Gradient Boosting",
                "model_version": "1.0.0",
                "training_date": "2026-01-15",
                "metrics": {
                    "f1_score": 0.8108,
                    "accuracy": 0.9975,
                    "precision": 0.7143,
                    "recall": 0.9524,
                    "roc_auc": 0.9772,
                    "auc_pr": 0.7955
                },
                "features": {
                    "total": 35,
                    "temporal": 7,
                    "behavioral": 8,
                    "aggregated": 10,
                    "categorical": 6,
                    "numeric": 4
                },
                "training_data": {
                    "total_samples": 85141,
                    "train_samples": 68112,
                    "test_samples": 17029,
                    "ato_samples": 42,
                    "normal_samples": 16987
                },
                "threshold": {
                    "optimal_threshold": 0.0041,
                    "default_threshold": 0.5,
                    "f1_improvement_pct": 9.3
                }
            }
        }
    }

    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    training_date: str = Field(..., description="Training date")
    metrics: ModelMetrics = Field(..., description="Model performance metrics")
    features: ModelFeatures = Field(..., description="Features information")
    training_data: TrainingData = Field(..., description="Training data information")
    threshold: ThresholdInfo = Field(..., description="Threshold information")
