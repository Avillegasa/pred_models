"""
File upload and management endpoints (Admin only)
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.file import FileResponse, FilePreview
from ..services.auth_service import get_current_admin
from ..services.file_service import FileService
from ..models.user import User
from ..models.file import UploadedFile

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Upload a CSV or Excel file for batch prediction (Admin only)"""
    try:
        db_file = await FileService.save_file(file, current_user.id, db)

        return FileResponse(
            id=db_file.id,
            filename=db_file.filename,
            original_filename=db_file.original_filename,
            uploaded_by=db_file.uploaded_by,
            uploaded_at=db_file.uploaded_at,
            row_count=db_file.row_count,
            columns=json.loads(db_file.columns_json) if db_file.columns_json else None,
            detected_model=db_file.detected_model
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[FileResponse])
async def list_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """List all uploaded files (Admin only)"""
    files = FileService.list_files(db, skip=skip, limit=limit)

    return [
        FileResponse(
            id=f.id,
            filename=f.filename,
            original_filename=f.original_filename,
            uploaded_by=f.uploaded_by,
            uploaded_at=f.uploaded_at,
            row_count=f.row_count,
            columns=json.loads(f.columns_json) if f.columns_json else None,
            detected_model=f.detected_model
        )
        for f in files
    ]


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get file details (Admin only)"""
    db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        id=db_file.id,
        filename=db_file.filename,
        original_filename=db_file.original_filename,
        uploaded_by=db_file.uploaded_by,
        uploaded_at=db_file.uploaded_at,
        row_count=db_file.row_count,
        columns=json.loads(db_file.columns_json) if db_file.columns_json else None,
        detected_model=db_file.detected_model
    )


@router.get("/{file_id}/preview", response_model=FilePreview)
async def get_file_preview(
    file_id: int,
    rows: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get preview of file contents (Admin only)"""
    try:
        preview = FileService.get_file_preview(file_id, db, num_rows=rows)
        return FilePreview(**preview)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete uploaded file (Admin only)"""
    if not FileService.delete_file(file_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
