"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class EmailInput(BaseModel):
    """Schema for single email prediction request."""
    sender: str = Field(..., description="Email sender address", min_length=1)
    receiver: Optional[str] = Field(None, description="Email receiver address")
    subject: str = Field(..., description="Email subject line", min_length=1)
    body: str = Field(..., description="Email body content", min_length=1)
    urls: Optional[int] = Field(0, description="Number of URLs in email (0 or 1)", ge=0, le=1)

    @field_validator('urls')
    @classmethod
    def validate_urls(cls, v):
        """Validate urls field is 0 or 1."""
        if v not in [0, 1]:
            raise ValueError("urls must be 0 or 1")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "user@example.com",
                "receiver": "admin@company.com",
                "subject": "Urgent: Verify your account",
                "body": "Click here to verify your account immediately...",
                "urls": 1
            }
        }


class RiskIndicator(BaseModel):
    """Single risk indicator with evidence."""
    indicator: str = Field(..., description="Description of the risk indicator")
    evidence: List[str] = Field(default=[], description="Evidence supporting this indicator")
    severity: Optional[str] = Field(default="medium", description="Severity level: critical, high, medium, low")


class PhishingExplanation(BaseModel):
    """Explanation for phishing prediction - why the model classified the email."""
    risk_indicators: List[RiskIndicator] = Field(default=[], description="List of risk indicators found in the email with evidence")
    suspicious_terms: List[str] = Field(default=[], description="Suspicious terms found in the email content")
    summary: str = Field(..., description="Human-readable summary of the prediction reasoning")
    total_indicators: Optional[int] = Field(default=0, description="Total number of indicators detected")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_indicators": [
                    {
                        "indicator": "Contiene URLs/enlaces",
                        "evidence": ["https://suspicious-link.com/login", "http://fake-bank.com/verify"],
                        "severity": "high"
                    },
                    {
                        "indicator": "Contiene lenguaje de urgencia",
                        "evidence": ["...Your account will be SUSPENDED immediately..."],
                        "severity": "medium"
                    }
                ],
                "suspicious_terms": ["free", "click", "winner", "urgent"],
                "summary": "Este email muestra 2 indicadores de phishing con 95.2% de confianza.",
                "total_indicators": 2
            }
        }


class PredictionMetadata(BaseModel):
    """Metadata for prediction response."""
    model: str = Field(..., description="Model name used for prediction")
    features_count: int = Field(..., description="Total number of features used")
    timestamp: str = Field(..., description="Prediction timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class PredictionResponse(BaseModel):
    """Schema for single email prediction response."""
    prediction: int = Field(..., description="Prediction result (0=Legitimate, 1=Phishing)")
    prediction_label: str = Field(..., description="Human-readable prediction label")
    confidence: float = Field(..., description="Confidence score for prediction (0.0-1.0)")
    probability_legitimate: float = Field(..., description="Probability of being legitimate")
    probability_phishing: float = Field(..., description="Probability of being phishing")
    explanation: PhishingExplanation = Field(..., description="Explanation of why this prediction was made")
    metadata: PredictionMetadata = Field(..., description="Prediction metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1,
                "prediction_label": "Phishing",
                "confidence": 0.9927,
                "probability_legitimate": 0.0073,
                "probability_phishing": 0.9927,
                "explanation": {
                    "risk_indicators": [
                        "Contains URLs/links",
                        "Contains urgent language"
                    ],
                    "suspicious_terms": ["click", "urgent", "verify"],
                    "summary": "Este email muestra 2 indicadores de phishing con 99.3% de confianza."
                },
                "metadata": {
                    "model": "Gradient Boosting",
                    "features_count": 1016,
                    "timestamp": "2026-01-10T15:30:45.123Z",
                    "processing_time_ms": 45.2
                }
            }
        }


class BatchEmailInput(BaseModel):
    """Schema for batch email prediction request."""
    emails: List[EmailInput] = Field(..., description="List of emails to predict", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "emails": [
                    {
                        "sender": "boss@company.com",
                        "subject": "Meeting tomorrow",
                        "body": "Let's meet at 10am"
                    },
                    {
                        "sender": "scam@phishing.com",
                        "subject": "You won $1M!",
                        "body": "Click here to claim..."
                    }
                ]
            }
        }


class SingleBatchPrediction(BaseModel):
    """Schema for single prediction in batch response."""
    email_index: int = Field(..., description="Index of email in batch")
    prediction: int = Field(..., description="Prediction result (0=Legitimate, 1=Phishing)")
    prediction_label: str = Field(..., description="Human-readable prediction label")
    confidence: float = Field(..., description="Confidence score for prediction")
    explanation: PhishingExplanation = Field(..., description="Explanation of why this prediction was made")


class BatchMetadata(BaseModel):
    """Metadata for batch prediction response."""
    total_emails: int = Field(..., description="Total number of emails processed")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


class BatchPredictionResponse(BaseModel):
    """Schema for batch email prediction response."""
    predictions: List[SingleBatchPrediction] = Field(..., description="List of predictions")
    metadata: BatchMetadata = Field(..., description="Batch processing metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "email_index": 0,
                        "prediction": 0,
                        "prediction_label": "Legitimate",
                        "confidence": 0.9856
                    },
                    {
                        "email_index": 1,
                        "prediction": 1,
                        "prediction_label": "Phishing",
                        "confidence": 0.9943
                    }
                ],
                "metadata": {
                    "total_emails": 2,
                    "processing_time_ms": 78.5
                }
            }
        }


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="API status")
    message: str = Field(..., description="API message")
    model: str = Field(..., description="Model name in use")
    version: str = Field(..., description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "message": "Phishing Detection API",
                "model": "Gradient Boosting",
                "version": "1.0.0"
            }
        }


class ModelMetrics(BaseModel):
    """Model performance metrics."""
    f1_score: float = Field(..., description="F1 score")
    accuracy: float = Field(..., description="Accuracy")
    precision: float = Field(..., description="Precision")
    recall: float = Field(..., description="Recall")
    roc_auc: float = Field(..., description="ROC-AUC score")


class ModelFeatures(BaseModel):
    """Model features information."""
    total: int = Field(..., description="Total number of features")
    tfidf: int = Field(..., description="Number of TF-IDF features")
    numeric: int = Field(..., description="Number of numeric features")


class TrainingData(BaseModel):
    """Training data information."""
    total_samples: int = Field(..., description="Total number of samples")
    train_samples: int = Field(..., description="Number of training samples")
    test_samples: int = Field(..., description="Number of test samples")


class ModelInfoResponse(BaseModel):
    """Schema for model info response."""
    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    training_date: str = Field(..., description="Training date")
    metrics: ModelMetrics = Field(..., description="Model performance metrics")
    features: ModelFeatures = Field(..., description="Features information")
    training_data: TrainingData = Field(..., description="Training data information")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "Gradient Boosting",
                "model_version": "1.0.0",
                "training_date": "2026-01-10",
                "metrics": {
                    "f1_score": 0.9909,
                    "accuracy": 0.9898,
                    "precision": 0.9891,
                    "recall": 0.9927,
                    "roc_auc": 0.9990
                },
                "features": {
                    "total": 1016,
                    "tfidf": 1000,
                    "numeric": 16
                },
                "training_data": {
                    "total_samples": 39154,
                    "train_samples": 31323,
                    "test_samples": 7831
                }
            }
        }
