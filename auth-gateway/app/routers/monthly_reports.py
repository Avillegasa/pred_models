"""
Monthly Reports router - aggregated monthly statistics
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.monthly_report import MonthlyReportResponse, AvailableMonthsResponse
from ..services.auth_service import get_current_user
from ..services.monthly_report_service import MonthlyReportService
from ..models.user import User

router = APIRouter(prefix="/monthly-reports", tags=["Monthly Reports"])


@router.get("", response_model=MonthlyReportResponse)
async def get_monthly_report(
    year: int = Query(..., ge=2020, le=2100, description="Report year"),
    month: int = Query(..., ge=1, le=12, description="Report month (1-12)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get monthly report with aggregated statistics.

    Returns comprehensive monthly statistics including:
    - Summary metrics (total predictions, threats, benign)
    - Breakdown by model (phishing, ATO, brute force)
    - Alert statistics by severity and status
    - Daily trend for the month
    - Confidence distribution histogram
    - Top 10 threats with highest confidence
    - Benign traffic insights

    Timezone: America/La_Paz (UTC-4)
    """
    try:
        report = MonthlyReportService.get_monthly_report(year, month, db)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating monthly report: {str(e)}"
        )


@router.get("/available", response_model=AvailableMonthsResponse)
async def get_available_months(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get list of months with available data.

    Returns months that have predictions or alerts recorded,
    sorted by date descending (most recent first).
    """
    try:
        return MonthlyReportService.get_available_months(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching available months: {str(e)}"
        )
