"""
Report schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ReportCreate(BaseModel):
    title: str
    file_id: int


class ReportSummary(BaseModel):
    model_config = {"protected_namespaces": (), "from_attributes": True}

    id: int
    title: str
    model_type: str
    created_at: datetime
    total_records: int
    threats_detected: int
    benign_count: int
    avg_confidence: Optional[float] = None
    status: str
    created_by_name: Optional[str] = None


class ReportResponse(ReportSummary):
    model_config = {"protected_namespaces": (), "from_attributes": True}

    file_name: Optional[str] = None
    results: Optional[List[dict[str, Any]]] = None
