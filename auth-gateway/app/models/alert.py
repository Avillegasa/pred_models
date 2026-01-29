"""
Alert model for storing prediction-based alerts
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Alert metadata
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(20), nullable=False)  # 'critical', 'high', 'medium'
    status = Column(String(20), default="unread")  # 'unread', 'read', 'acknowledged'

    # Source information
    model_type = Column(String(50), nullable=False)  # 'phishing', 'ato', 'brute_force'
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=True)
    prediction_index = Column(Integer)  # Index in the results array

    # Prediction details
    confidence = Column(Float, nullable=False)  # 0-100
    prediction_label = Column(String(255))
    risk_level = Column(String(20))  # 'low', 'medium', 'high', 'critical'

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Raw prediction data for detailed investigation
    raw_data_json = Column(Text)

    # Relationships
    report = relationship("Report", backref="alerts")
    acknowledger = relationship("User", foreign_keys=[acknowledged_by], backref="acknowledged_alerts")
