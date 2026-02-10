"""
Monthly Report schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class ModelStats(BaseModel):
    """Statistics for a single model"""
    total: int = 0
    threats: int = 0
    benign: int = 0
    avg_confidence: float = 0.0


class AlertsByStatus(BaseModel):
    """Alerts breakdown by status"""
    unread: int = 0
    read: int = 0
    acknowledged: int = 0


class AlertsBySeverity(BaseModel):
    """Alerts breakdown by severity"""
    critical: int = 0
    high: int = 0
    medium: int = 0


class AlertsStats(BaseModel):
    """Alert statistics for the monthly report"""
    total: int = 0
    by_severity: AlertsBySeverity = AlertsBySeverity()
    by_status: AlertsByStatus = AlertsByStatus()


class DailyTrend(BaseModel):
    """Daily trend data point"""
    day: int
    date: str
    threats: int = 0
    benign: int = 0
    total: int = 0


class ConfidenceDistribution(BaseModel):
    """Confidence distribution bucket"""
    range: str
    count: int = 0


class TopThreat(BaseModel):
    """Top threat entry"""
    model_config = {"protected_namespaces": ()}

    id: int
    model_type: str
    prediction_label: str
    confidence: float
    created_at: datetime
    explanation_summary: Optional[str] = None


class ModelBenignInsight(BaseModel):
    """Benign insight for a specific model"""
    count: int = 0
    avg_confidence: float = 0.0
    common_patterns: List[str] = []


class BenignInsights(BaseModel):
    """Insights about benign/legitimate traffic"""
    total_benign: int = 0
    by_model: Dict[str, ModelBenignInsight] = {}


class Period(BaseModel):
    """Report period"""
    start: str
    end: str


class Summary(BaseModel):
    """Report summary statistics"""
    total_predictions: int = 0
    threats_detected: int = 0
    benign_count: int = 0
    threat_rate_percent: float = 0.0
    avg_confidence: float = 0.0


class MonthlyReportResponse(BaseModel):
    """Complete monthly report response"""
    model_config = {"protected_namespaces": ()}

    year: int
    month: int
    month_name: str
    timezone: str = "America/La_Paz"
    period: Period
    summary: Summary
    by_model: Dict[str, ModelStats] = {}
    alerts: AlertsStats = AlertsStats()
    daily_trend: List[DailyTrend] = []
    confidence_distribution: List[ConfidenceDistribution] = []
    top_threats: List[TopThreat] = []
    benign_insights: BenignInsights = BenignInsights()


class AvailableMonth(BaseModel):
    """Available month with data"""
    year: int
    month: int
    month_name: str
    prediction_count: int
    alert_count: int


class AvailableMonthsResponse(BaseModel):
    """Response with available months"""
    months: List[AvailableMonth] = []
