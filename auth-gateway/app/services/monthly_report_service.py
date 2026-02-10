"""
Monthly Report Service
Aggregates predictions and alerts by month for reporting
Timezone: America/La_Paz (UTC-4)
"""
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from ..models.prediction import Prediction
from ..models.alert import Alert
from ..schemas.monthly_report import (
    MonthlyReportResponse,
    Summary,
    Period,
    ModelStats,
    AlertsStats,
    AlertsBySeverity,
    AlertsByStatus,
    DailyTrend,
    ConfidenceDistribution,
    TopThreat,
    BenignInsights,
    ModelBenignInsight,
    AvailableMonth,
    AvailableMonthsResponse,
)

LA_PAZ_TZ = ZoneInfo("America/La_Paz")

MONTH_NAMES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

# Common patterns for benign classifications by model
BENIGN_PATTERNS = {
    "phishing": [
        "Dominios corporativos verificados",
        "Sin URLs sospechosas",
        "Remitentes conocidos",
        "Contenido sin urgencia indebida",
        "Sin adjuntos ejecutables",
    ],
    "ato": [
        "Sin cambio de pais",
        "IPs consistentes",
        "Horarios normales de acceso",
        "Dispositivo reconocido",
        "Sin actividad rapida sospechosa",
    ],
    "brute_force": [
        "Duracion normal de conexion",
        "Tasa de paquetes humana",
        "Sin patrones repetitivos",
        "Tamano de paquetes variado",
        "Flujo de trafico natural",
    ],
}


class MonthlyReportService:
    @classmethod
    def get_monthly_report(
        cls, year: int, month: int, db: Session
    ) -> MonthlyReportResponse:
        """Generate a complete monthly report for the specified month"""
        # Calculate period bounds in La Paz timezone
        start_date = datetime(year, month, 1, 0, 0, 0, tzinfo=LA_PAZ_TZ)

        # Get the last day of the month
        if month == 12:
            next_month = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=LA_PAZ_TZ)
        else:
            next_month = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=LA_PAZ_TZ)
        end_date = next_month - timedelta(seconds=1)

        # Convert to UTC for database queries
        start_utc = start_date.astimezone(ZoneInfo("UTC"))
        end_utc = end_date.astimezone(ZoneInfo("UTC"))

        # Query predictions for the month
        predictions = db.query(Prediction).filter(
            Prediction.created_at >= start_utc,
            Prediction.created_at <= end_utc
        ).all()

        # Query alerts for the month
        alerts = db.query(Alert).filter(
            Alert.created_at >= start_utc,
            Alert.created_at <= end_utc
        ).all()

        # Build report
        return cls._build_report(
            year=year,
            month=month,
            start_date=start_date,
            end_date=end_date,
            predictions=predictions,
            alerts=alerts,
        )

    @classmethod
    def _build_report(
        cls,
        year: int,
        month: int,
        start_date: datetime,
        end_date: datetime,
        predictions: List[Prediction],
        alerts: List[Alert],
    ) -> MonthlyReportResponse:
        """Build the complete monthly report from raw data"""
        # Summary
        total_predictions = len(predictions)
        threats = [p for p in predictions if p.prediction == 1]
        benign = [p for p in predictions if p.prediction == 0]
        threats_detected = len(threats)
        benign_count = len(benign)

        threat_rate = (threats_detected / total_predictions * 100) if total_predictions > 0 else 0
        avg_confidence = (
            sum(p.confidence for p in predictions) / total_predictions * 100
            if total_predictions > 0
            else 0
        )

        summary = Summary(
            total_predictions=total_predictions,
            threats_detected=threats_detected,
            benign_count=benign_count,
            threat_rate_percent=round(threat_rate, 2),
            avg_confidence=round(avg_confidence, 1),
        )

        # By model
        by_model = cls._aggregate_by_model(predictions)

        # Alerts
        alerts_stats = cls._aggregate_alerts(alerts)

        # Daily trend
        daily_trend = cls._build_daily_trend(year, month, predictions)

        # Confidence distribution
        confidence_distribution = cls._build_confidence_distribution(predictions)

        # Top threats
        top_threats = cls._get_top_threats(threats)

        # Benign insights
        benign_insights = cls._build_benign_insights(benign)

        return MonthlyReportResponse(
            year=year,
            month=month,
            month_name=MONTH_NAMES.get(month, str(month)),
            timezone="America/La_Paz",
            period=Period(
                start=start_date.isoformat(),
                end=end_date.isoformat(),
            ),
            summary=summary,
            by_model=by_model,
            alerts=alerts_stats,
            daily_trend=daily_trend,
            confidence_distribution=confidence_distribution,
            top_threats=top_threats,
            benign_insights=benign_insights,
        )

    @classmethod
    def _aggregate_by_model(cls, predictions: List[Prediction]) -> Dict[str, ModelStats]:
        """Aggregate predictions by model type"""
        models = {"phishing": [], "ato": [], "brute_force": []}

        for p in predictions:
            model_type = p.model_type.lower()
            if model_type in models:
                models[model_type].append(p)

        result = {}
        for model_type, preds in models.items():
            total = len(preds)
            threats = len([p for p in preds if p.prediction == 1])
            benign = total - threats
            avg_conf = (
                sum(p.confidence for p in preds) / total * 100 if total > 0 else 0
            )

            result[model_type] = ModelStats(
                total=total,
                threats=threats,
                benign=benign,
                avg_confidence=round(avg_conf, 1),
            )

        return result

    @classmethod
    def _aggregate_alerts(cls, alerts: List[Alert]) -> AlertsStats:
        """Aggregate alert statistics"""
        total = len(alerts)

        by_severity = defaultdict(int)
        by_status = defaultdict(int)

        for alert in alerts:
            severity = alert.severity.lower() if alert.severity else "medium"
            status = alert.status.lower() if alert.status else "unread"

            by_severity[severity] += 1
            by_status[status] += 1

        return AlertsStats(
            total=total,
            by_severity=AlertsBySeverity(
                critical=by_severity.get("critical", 0),
                high=by_severity.get("high", 0),
                medium=by_severity.get("medium", 0),
            ),
            by_status=AlertsByStatus(
                unread=by_status.get("unread", 0),
                read=by_status.get("read", 0),
                acknowledged=by_status.get("acknowledged", 0),
            ),
        )

    @classmethod
    def _build_daily_trend(
        cls, year: int, month: int, predictions: List[Prediction]
    ) -> List[DailyTrend]:
        """Build daily trend data for the month"""
        # Get number of days in month
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        days_in_month = (next_month - datetime(year, month, 1)).days

        # Initialize daily counts
        daily_data = {
            day: {"threats": 0, "benign": 0}
            for day in range(1, days_in_month + 1)
        }

        # Aggregate by day
        for p in predictions:
            # Convert to La Paz timezone for correct day
            created_at = p.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=ZoneInfo("UTC"))
            local_time = created_at.astimezone(LA_PAZ_TZ)

            day = local_time.day
            if day in daily_data:
                if p.prediction == 1:
                    daily_data[day]["threats"] += 1
                else:
                    daily_data[day]["benign"] += 1

        # Build trend list
        trend = []
        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            threats = daily_data[day]["threats"]
            benign = daily_data[day]["benign"]
            trend.append(
                DailyTrend(
                    day=day,
                    date=date_str,
                    threats=threats,
                    benign=benign,
                    total=threats + benign,
                )
            )

        return trend

    @classmethod
    def _build_confidence_distribution(
        cls, predictions: List[Prediction]
    ) -> List[ConfidenceDistribution]:
        """Build confidence distribution histogram buckets"""
        buckets = {
            "50-60%": 0,
            "60-70%": 0,
            "70-80%": 0,
            "80-90%": 0,
            "90-100%": 0,
        }

        for p in predictions:
            conf_pct = p.confidence * 100
            if conf_pct >= 90:
                buckets["90-100%"] += 1
            elif conf_pct >= 80:
                buckets["80-90%"] += 1
            elif conf_pct >= 70:
                buckets["70-80%"] += 1
            elif conf_pct >= 60:
                buckets["60-70%"] += 1
            elif conf_pct >= 50:
                buckets["50-60%"] += 1

        return [
            ConfidenceDistribution(range=range_str, count=count)
            for range_str, count in buckets.items()
        ]

    @classmethod
    def _get_top_threats(cls, threats: List[Prediction], limit: int = 10) -> List[TopThreat]:
        """Get top N threats by confidence"""
        # Sort by confidence descending
        sorted_threats = sorted(threats, key=lambda p: p.confidence, reverse=True)[:limit]

        result = []
        for p in sorted_threats:
            # Extract explanation summary
            explanation_summary = None
            if p.explanation:
                try:
                    exp = json.loads(p.explanation)
                    explanation_summary = exp.get("summary", None)
                    if not explanation_summary and "risk_indicators" in exp:
                        indicators = exp.get("risk_indicators", [])
                        if indicators:
                            explanation_summary = "; ".join(
                                i.get("evidence", i.get("indicator", ""))[:50]
                                for i in indicators[:3]
                            )
                except (json.JSONDecodeError, TypeError):
                    pass

            result.append(
                TopThreat(
                    id=p.id,
                    model_type=p.model_type,
                    prediction_label=p.prediction_label,
                    confidence=round(p.confidence * 100, 1),
                    created_at=p.created_at,
                    explanation_summary=explanation_summary,
                )
            )

        return result

    @classmethod
    def _build_benign_insights(cls, benign: List[Prediction]) -> BenignInsights:
        """Build insights about benign/legitimate traffic"""
        by_model = defaultdict(list)

        for p in benign:
            model_type = p.model_type.lower()
            by_model[model_type].append(p)

        model_insights = {}
        for model_type in ["phishing", "ato", "brute_force"]:
            preds = by_model.get(model_type, [])
            count = len(preds)
            avg_conf = (
                sum(p.confidence for p in preds) / count * 100 if count > 0 else 0
            )

            # Get patterns for this model
            patterns = BENIGN_PATTERNS.get(model_type, [])[:3]

            model_insights[model_type] = ModelBenignInsight(
                count=count,
                avg_confidence=round(avg_conf, 1),
                common_patterns=patterns,
            )

        return BenignInsights(
            total_benign=len(benign),
            by_model=model_insights,
        )

    @classmethod
    def get_available_months(cls, db: Session) -> AvailableMonthsResponse:
        """Get list of months that have data available"""
        # Get distinct year-month combinations from predictions
        pred_months = db.query(
            extract("year", Prediction.created_at).label("year"),
            extract("month", Prediction.created_at).label("month"),
            func.count(Prediction.id).label("count"),
        ).group_by(
            extract("year", Prediction.created_at),
            extract("month", Prediction.created_at),
        ).all()

        # Get distinct year-month combinations from alerts
        alert_months = db.query(
            extract("year", Alert.created_at).label("year"),
            extract("month", Alert.created_at).label("month"),
            func.count(Alert.id).label("count"),
        ).group_by(
            extract("year", Alert.created_at),
            extract("month", Alert.created_at),
        ).all()

        # Combine and deduplicate
        months_data = {}
        for year, month, count in pred_months:
            if year and month:
                key = (int(year), int(month))
                if key not in months_data:
                    months_data[key] = {"prediction_count": 0, "alert_count": 0}
                months_data[key]["prediction_count"] = count

        for year, month, count in alert_months:
            if year and month:
                key = (int(year), int(month))
                if key not in months_data:
                    months_data[key] = {"prediction_count": 0, "alert_count": 0}
                months_data[key]["alert_count"] = count

        # Build response
        months = []
        for (year, month), data in sorted(months_data.items(), reverse=True):
            months.append(
                AvailableMonth(
                    year=year,
                    month=month,
                    month_name=MONTH_NAMES.get(month, str(month)),
                    prediction_count=data["prediction_count"],
                    alert_count=data["alert_count"],
                )
            )

        return AvailableMonthsResponse(months=months)
