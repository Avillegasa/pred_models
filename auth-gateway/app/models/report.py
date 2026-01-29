"""
Report model for storing prediction results
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    model_type = Column(String(50), nullable=False)  # 'phishing', 'ato', 'brute_force'
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    total_records = Column(Integer)
    threats_detected = Column(Integer)
    benign_count = Column(Integer)
    avg_confidence = Column(Float)
    results_json = Column(Text)  # JSON string of full results
    status = Column(String(20), default="completed")  # 'pending', 'processing', 'completed', 'failed'

    file = relationship("UploadedFile", backref="reports")
    creator = relationship("User", backref="reports")
