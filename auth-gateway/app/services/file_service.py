"""
File upload and management service
"""
import os
import json
import uuid
from typing import List, Optional
import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..config import get_settings
from ..models.file import UploadedFile
from .column_detector import ColumnDetector

settings = get_settings()


class FileService:
    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

    @classmethod
    def validate_file(cls, filename: str) -> bool:
        """Check if file has allowed extension"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in cls.ALLOWED_EXTENSIONS

    @classmethod
    async def save_file(
        cls,
        file: UploadFile,
        user_id: int,
        db: Session
    ) -> UploadedFile:
        """Save uploaded file and create database record"""
        # Validate extension
        if not cls.validate_file(file.filename):
            raise ValueError(f"Invalid file type. Allowed: {cls.ALLOWED_EXTENSIONS}")

        # Generate unique filename
        ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Save file
        content = await file.read()

        # Check file size
        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if len(content) > max_size:
            raise ValueError(f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB")

        with open(file_path, "wb") as f:
            f.write(content)

        # Read file to get metadata
        try:
            df = cls.read_file(file_path)
            columns = df.columns.tolist()
            row_count = len(df)
            detected_model = ColumnDetector.detect_model(columns)
        except Exception as e:
            # Clean up file if reading fails
            os.remove(file_path)
            raise ValueError(f"Error reading file: {str(e)}")

        # Create database record
        db_file = UploadedFile(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            uploaded_by=user_id,
            row_count=row_count,
            columns_json=json.dumps(columns),
            detected_model=detected_model
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    @classmethod
    def read_file(cls, file_path: str) -> pd.DataFrame:
        """Read CSV or Excel file into DataFrame"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            return pd.read_csv(file_path)
        elif ext in {".xlsx", ".xls"}:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @classmethod
    def get_file_preview(cls, file_id: int, db: Session, num_rows: int = 5) -> dict:
        """Get preview of file contents"""
        db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not db_file:
            raise ValueError("File not found")

        df = cls.read_file(db_file.file_path)
        preview_df = df.head(num_rows)

        # Convert to list of dicts, handling NaN values
        preview_rows = preview_df.fillna("").to_dict(orient="records")

        return {
            "id": db_file.id,
            "filename": db_file.original_filename,
            "columns": json.loads(db_file.columns_json),
            "row_count": db_file.row_count,
            "detected_model": db_file.detected_model,
            "preview_rows": preview_rows
        }

    @classmethod
    def get_file_data(cls, file_id: int, db: Session) -> List[dict]:
        """Get all data from file as list of dicts"""
        db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not db_file:
            raise ValueError("File not found")

        df = cls.read_file(db_file.file_path)
        # Convert to list of dicts, handling NaN values
        return df.fillna("").to_dict(orient="records")

    @classmethod
    def list_files(
        cls,
        db: Session,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[UploadedFile]:
        """List uploaded files"""
        query = db.query(UploadedFile)
        if user_id:
            query = query.filter(UploadedFile.uploaded_by == user_id)
        return query.order_by(UploadedFile.uploaded_at.desc()).offset(skip).limit(limit).all()

    @classmethod
    def delete_file(cls, file_id: int, db: Session) -> bool:
        """Delete file and its database record"""
        db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not db_file:
            return False

        # Delete physical file
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)

        # Delete database record
        db.delete(db_file)
        db.commit()
        return True
