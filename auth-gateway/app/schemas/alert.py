"""
Alert schemas for API requests/responses
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str  # 'critical', 'high', 'medium'
    model_type: str


class AlertResponse(AlertBase):
    model_config = {"from_attributes": True}

    id: int
    status: str
    report_id: Optional[int] = None
    prediction_index: Optional[int] = None
    confidence: float
    prediction_label: Optional[str] = None
    risk_level: Optional[str] = None
    created_at: datetime
    read_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None


class AlertDetail(AlertResponse):
    raw_data: Optional[Any] = None
    acknowledger_name: Optional[str] = None
    report_title: Optional[str] = None


class AlertStats(BaseModel):
    total: int
    unread: int
    by_severity: dict


class AlertAcknowledge(BaseModel):
    alert_ids: List[int]


class AlertThresholds(BaseModel):
    critical: float
    high: float
    medium: float


class AlertThresholdsResponse(BaseModel):
    phishing: AlertThresholds
    ato: AlertThresholds
    brute_force: AlertThresholds


class UnreadCountResponse(BaseModel):
    count: int
