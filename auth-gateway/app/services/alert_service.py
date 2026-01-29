"""
Alert generation and management service
"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from ..models.alert import Alert
from ..models.user import User
from ..models.report import Report
from ..config import ALERT_THRESHOLDS, DEFAULT_ALERT_THRESHOLDS


class AlertService:

    @classmethod
    def get_thresholds(cls, model_type: str) -> Dict[str, float]:
        """Get alert thresholds for a specific model"""
        return ALERT_THRESHOLDS.get(model_type, DEFAULT_ALERT_THRESHOLDS)

    @classmethod
    def determine_severity(cls, model_type: str, confidence: float) -> Optional[str]:
        """
        Determine alert severity based on confidence and model type.
        Returns None if confidence doesn't meet minimum threshold.
        """
        thresholds = cls.get_thresholds(model_type)

        if confidence >= thresholds["critical"]:
            return "critical"
        elif confidence >= thresholds["high"]:
            return "high"
        elif confidence >= thresholds["medium"]:
            return "medium"
        return None  # No alert needed

    @classmethod
    def generate_alerts_from_predictions(
        cls,
        model_type: str,
        report_id: int,
        predictions: List[Dict[str, Any]],
        db: Session
    ) -> List[Alert]:
        """
        Generate alerts from a list of predictions.
        Only creates alerts for threats that meet threshold criteria.
        """
        alerts_created = []

        for idx, pred in enumerate(predictions):
            # Only create alerts for threats
            if not pred.get("is_threat", False):
                continue

            confidence = pred.get("confidence", 0)
            severity = cls.determine_severity(model_type, confidence)

            # Skip if doesn't meet minimum threshold
            if severity is None:
                continue

            # Build alert title based on model type
            title = cls._build_alert_title(model_type, pred)
            description = cls._build_alert_description(model_type, pred, idx)

            alert = Alert(
                title=title,
                description=description,
                severity=severity,
                status="unread",
                model_type=model_type,
                report_id=report_id,
                prediction_index=idx,
                confidence=confidence,
                prediction_label=pred.get("label", ""),
                risk_level=pred.get("risk_level", "high"),
                raw_data_json=json.dumps(pred)
            )

            db.add(alert)
            alerts_created.append(alert)

        if alerts_created:
            db.commit()
            for alert in alerts_created:
                db.refresh(alert)

        return alerts_created

    @classmethod
    def _build_alert_title(cls, model_type: str, pred: Dict) -> str:
        """Build descriptive alert title"""
        confidence = pred.get('confidence', 0)
        titles = {
            "phishing": f"Email Phishing Detectado ({confidence:.1f}%)",
            "ato": f"Intento de Account Takeover ({confidence:.1f}%)",
            "brute_force": f"Ataque Brute Force: {pred.get('attack_type', 'Unknown')} ({confidence:.1f}%)"
        }
        return titles.get(model_type, f"Amenaza Detectada ({confidence:.1f}%)")

    @classmethod
    def _build_alert_description(cls, model_type: str, pred: Dict, idx: int) -> str:
        """Build detailed alert description including explanation insights"""
        base = f"Registro #{idx + 1}: {pred.get('label', 'Amenaza detectada')}"

        if model_type == "ato":
            risk_score = pred.get("risk_score", pred.get("confidence", 0))
            base += f"\nRisk Score: {risk_score:.1f}"
        elif model_type == "brute_force":
            attack_type = pred.get("attack_type", "Unknown")
            base += f"\nTipo de Ataque: {attack_type}"

        # Add explanation summary if available
        explanation = pred.get("explanation", {})
        if explanation:
            summary = explanation.get("summary", "")
            if summary:
                base += f"\n\n{summary}"

            # Add key indicators based on model type
            if model_type == "phishing":
                indicators = explanation.get("risk_indicators", [])
                if indicators and indicators[0] != "No se detectaron indicadores de riesgo especificos":
                    base += "\n\nIndicadores:"
                    for ind in indicators[:3]:  # Top 3 indicators
                        base += f"\n  - {ind}"
            elif model_type == "ato":
                changes = explanation.get("behavioral_changes", [])
                if changes and changes[0] != "No se detectaron cambios de comportamiento":
                    base += "\n\nCambios detectados:"
                    for change in changes[:3]:
                        base += f"\n  - {change}"
            elif model_type == "brute_force":
                anomalies = explanation.get("network_anomalies", [])
                if anomalies:
                    base += "\n\nAnomalias de red:"
                    for anomaly in anomalies[:3]:
                        base += f"\n  - {anomaly}"

        return base

    @classmethod
    def list_alerts(
        cls,
        db: Session,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        model_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Alert]:
        """List alerts with optional filters"""
        query = db.query(Alert)

        if status:
            query = query.filter(Alert.status == status)
        if severity:
            query = query.filter(Alert.severity == severity)
        if model_type:
            query = query.filter(Alert.model_type == model_type)

        return query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()

    @classmethod
    def get_unread_count(cls, db: Session) -> int:
        """Get count of unread alerts"""
        return db.query(Alert).filter(Alert.status == "unread").count()

    @classmethod
    def get_alert_stats(cls, db: Session) -> Dict[str, Any]:
        """Get alert statistics for dashboard"""
        total = db.query(Alert).count()
        unread = db.query(Alert).filter(Alert.status == "unread").count()

        # Count by severity (only active alerts)
        critical = db.query(Alert).filter(
            and_(Alert.severity == "critical", Alert.status.in_(["unread", "read"]))
        ).count()
        high = db.query(Alert).filter(
            and_(Alert.severity == "high", Alert.status.in_(["unread", "read"]))
        ).count()
        medium = db.query(Alert).filter(
            and_(Alert.severity == "medium", Alert.status.in_(["unread", "read"]))
        ).count()

        return {
            "total": total,
            "unread": unread,
            "by_severity": {
                "critical": critical,
                "high": high,
                "medium": medium
            }
        }

    @classmethod
    def get_alert(cls, alert_id: int, db: Session) -> Optional[Alert]:
        """Get single alert by ID"""
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @classmethod
    def get_alert_detail(cls, alert_id: int, db: Session) -> Optional[Dict]:
        """Get alert with related information"""
        result = db.query(Alert, User.full_name, Report.title).outerjoin(
            User, Alert.acknowledged_by == User.id
        ).outerjoin(
            Report, Alert.report_id == Report.id
        ).filter(Alert.id == alert_id).first()

        if not result:
            return None

        alert, acknowledger_name, report_title = result

        return {
            "id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "status": alert.status,
            "model_type": alert.model_type,
            "report_id": alert.report_id,
            "prediction_index": alert.prediction_index,
            "confidence": alert.confidence,
            "prediction_label": alert.prediction_label,
            "risk_level": alert.risk_level,
            "created_at": alert.created_at,
            "read_at": alert.read_at,
            "acknowledged_at": alert.acknowledged_at,
            "acknowledged_by": alert.acknowledged_by,
            "raw_data": json.loads(alert.raw_data_json) if alert.raw_data_json else None,
            "acknowledger_name": acknowledger_name,
            "report_title": report_title
        }

    @classmethod
    def mark_as_read(cls, alert_id: int, db: Session) -> Optional[Alert]:
        """Mark alert as read"""
        alert = cls.get_alert(alert_id, db)
        if alert and alert.status == "unread":
            alert.status = "read"
            alert.read_at = datetime.utcnow()
            db.commit()
            db.refresh(alert)
        return alert

    @classmethod
    def acknowledge_alert(
        cls,
        alert_id: int,
        user_id: int,
        db: Session
    ) -> Optional[Alert]:
        """Acknowledge an alert"""
        alert = cls.get_alert(alert_id, db)
        if alert:
            alert.status = "acknowledged"
            alert.acknowledged_at = datetime.utcnow()
            alert.acknowledged_by = user_id
            db.commit()
            db.refresh(alert)
        return alert

    @classmethod
    def bulk_acknowledge(
        cls,
        alert_ids: List[int],
        user_id: int,
        db: Session
    ) -> int:
        """Acknowledge multiple alerts at once"""
        count = db.query(Alert).filter(Alert.id.in_(alert_ids)).update(
            {
                "status": "acknowledged",
                "acknowledged_at": datetime.utcnow(),
                "acknowledged_by": user_id
            },
            synchronize_session=False
        )
        db.commit()
        return count

    @classmethod
    def mark_all_as_read(cls, db: Session) -> int:
        """Mark all unread alerts as read"""
        count = db.query(Alert).filter(Alert.status == "unread").update(
            {"status": "read", "read_at": datetime.utcnow()},
            synchronize_session=False
        )
        db.commit()
        return count
