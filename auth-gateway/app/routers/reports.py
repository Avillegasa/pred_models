"""
Report generation and viewing endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.report import ReportCreate, ReportResponse, ReportSummary
from ..services.auth_service import get_current_user, get_current_admin
from ..services.report_service import ReportService
from ..models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate a new report by running predictions (Admin only)"""
    try:
        report = await ReportService.generate_report(
            title=report_data.title,
            file_id=report_data.file_id,
            user_id=current_user.id,
            db=db
        )

        return ReportService.get_report(report.id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("", response_model=List[ReportSummary])
async def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all reports (Both Admin and Analyst)"""
    reports = ReportService.list_reports(db, skip=skip, limit=limit)
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get report details (Both Admin and Analyst)"""
    report = ReportService.get_report(report_id, db)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a report (Admin only)"""
    if not ReportService.delete_report(report_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
