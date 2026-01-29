"""
File schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class FileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    uploaded_by: Optional[int] = None
    uploaded_at: datetime
    row_count: Optional[int] = None
    columns: Optional[List[str]] = None
    detected_model: Optional[str] = None

    class Config:
        from_attributes = True


class FilePreview(BaseModel):
    id: int
    filename: str
    columns: List[str]
    row_count: int
    detected_model: Optional[str] = None
    preview_rows: List[dict[str, Any]]  # First 5 rows
