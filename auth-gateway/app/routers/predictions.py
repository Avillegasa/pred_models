"""
Predictions router - handles manual prediction storage and statistics
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models.prediction import Prediction
from ..models.user import User
from ..schemas.prediction import PredictionCreate, PredictionResponse, PredictionStats
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(
    prediction_data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Store a manual prediction result.
    """
    # Create prediction record
    prediction = Prediction(
        model_type=prediction_data.model_type.lower(),
        created_by=current_user.id,
        prediction=prediction_data.prediction,
        prediction_label=prediction_data.prediction_label,
        confidence=prediction_data.confidence,
        input_data=json.dumps(prediction_data.input_data) if prediction_data.input_data else None,
        explanation=json.dumps(prediction_data.explanation) if prediction_data.explanation else None
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return PredictionResponse(
        id=prediction.id,
        model_type=prediction.model_type,
        prediction=prediction.prediction,
        prediction_label=prediction.prediction_label,
        confidence=prediction.confidence,
        created_at=prediction.created_at,
        created_by_name=current_user.username
    )


@router.get("/", response_model=List[PredictionResponse])
async def list_predictions(
    skip: int = 0,
    limit: int = 100,
    model_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List manual predictions with optional filtering.
    """
    query = db.query(Prediction).join(User, Prediction.created_by == User.id)

    if model_type:
        query = query.filter(Prediction.model_type == model_type.lower())

    predictions = query.order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()

    return [
        PredictionResponse(
            id=p.id,
            model_type=p.model_type,
            prediction=p.prediction,
            prediction_label=p.prediction_label,
            confidence=p.confidence,
            created_at=p.created_at,
            created_by_name=p.creator.username if p.creator else None
        )
        for p in predictions
    ]


@router.get("/stats", response_model=PredictionStats)
async def get_prediction_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics for manual predictions.
    Used by the dashboard to show real-time stats.
    """
    # Total counts
    total = db.query(func.count(Prediction.id)).scalar() or 0
    threats = db.query(func.count(Prediction.id)).filter(Prediction.prediction == 1).scalar() or 0
    benign = total - threats

    # Average confidence
    avg_conf = db.query(func.avg(Prediction.confidence)).scalar() or 0

    # By model type
    by_model = {
        "phishing": {"total": 0, "threats": 0},
        "ato": {"total": 0, "threats": 0},
        "brute_force": {"total": 0, "threats": 0}
    }

    model_stats = db.query(
        Prediction.model_type,
        func.count(Prediction.id).label("total"),
        func.sum(Prediction.prediction).label("threats")
    ).group_by(Prediction.model_type).all()

    for stat in model_stats:
        model = stat.model_type.lower()
        if model in by_model:
            by_model[model]["total"] = stat.total or 0
            by_model[model]["threats"] = int(stat.threats or 0)

    return PredictionStats(
        total_predictions=total,
        threats_detected=threats,
        benign_count=benign,
        avg_confidence=round(float(avg_conf) * 100, 1) if avg_conf else 0,
        by_model=by_model
    )
