"""
Alert management endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.alert import (
    AlertResponse, AlertDetail, AlertStats,
    AlertAcknowledge, AlertThresholdsResponse, UnreadCountResponse
)
from ..services.auth_service import get_current_user
from ..services.alert_service import AlertService
from ..models.user import User
from ..config import ALERT_THRESHOLDS

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    status: Optional[str] = Query(None, description="Filter by status: unread, read, acknowledged"),
    severity: Optional[str] = Query(None, description="Filter by severity: critical, high, medium"),
    model_type: Optional[str] = Query(None, description="Filter by model: phishing, ato, brute_force"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all alerts with optional filters"""
    return AlertService.list_alerts(
        db, status=status, severity=severity,
        model_type=model_type, skip=skip, limit=limit
    )


@router.get("/unread/count", response_model=UnreadCountResponse)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread alerts (for badge in TopBar)"""
    count = AlertService.get_unread_count(db)
    return {"count": count}


@router.get("/stats", response_model=AlertStats)
async def get_alert_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert statistics for dashboard"""
    return AlertService.get_alert_stats(db)


@router.get("/thresholds", response_model=AlertThresholdsResponse)
async def get_thresholds(
    current_user: User = Depends(get_current_user)
):
    """Get current alert thresholds by model"""
    return ALERT_THRESHOLDS


@router.get("/{alert_id}", response_model=AlertDetail)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert details"""
    alert_detail = AlertService.get_alert_detail(alert_id, db)
    if not alert_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    # Mark as read when viewed
    alert = AlertService.get_alert(alert_id, db)
    if alert and alert.status == "unread":
        AlertService.mark_as_read(alert_id, db)

    return alert_detail


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Acknowledge a single alert"""
    alert = AlertService.acknowledge_alert(alert_id, current_user.id, db)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.post("/acknowledge/bulk")
async def bulk_acknowledge(
    data: AlertAcknowledge,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Acknowledge multiple alerts at once"""
    count = AlertService.bulk_acknowledge(data.alert_ids, current_user.id, db)
    return {"acknowledged": count}


@router.post("/mark-all-read")
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all unread alerts as read"""
    count = AlertService.mark_all_as_read(db)
    return {"marked_read": count}
