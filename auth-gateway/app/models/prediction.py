"""
Prediction model for storing manual predictions
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String(50), nullable=False)  # 'phishing', 'ato', 'brute_force'
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Prediction results
    prediction = Column(Integer, nullable=False)  # 0=benign, 1=threat
    prediction_label = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)

    # Input data (JSON string)
    input_data = Column(Text)

    # Explanation (JSON string)
    explanation = Column(Text)

    # Relationships
    creator = relationship("User", backref="predictions")
