"""
Report generation and management service
"""
import json
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.report import Report
from ..models.file import UploadedFile
from ..models.user import User
from .file_service import FileService
from .prediction_client import PredictionClient
from .alert_service import AlertService


class ReportService:
    @classmethod
    async def generate_report(
        cls,
        title: str,
        file_id: int,
        user_id: int,
        db: Session
    ) -> Report:
        """Generate a report by running predictions on file data"""
        # Get file info
        db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not db_file:
            raise ValueError("File not found")

        if not db_file.detected_model:
            raise ValueError("Could not detect model type for this file")

        # Create report record with pending status
        report = Report(
            title=title,
            model_type=db_file.detected_model,
            file_id=file_id,
            created_by=user_id,
            status="processing",
            total_records=db_file.row_count,
            threats_detected=0,
            benign_count=0
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        try:
            # Get file data
            records = FileService.get_file_data(file_id, db)

            # Call prediction API
            result = await PredictionClient.predict_batch(
                db_file.detected_model,
                records
            )

            # Process results
            processed = cls._process_results(db_file.detected_model, result)

            # Update report with results
            report.threats_detected = processed["threats_detected"]
            report.benign_count = processed["benign_count"]
            report.avg_confidence = processed["avg_confidence"]
            report.results_json = json.dumps(processed["results"])
            report.status = "completed"

            # Generate alerts for threats that exceed thresholds
            AlertService.generate_alerts_from_predictions(
                model_type=db_file.detected_model,
                report_id=report.id,
                predictions=processed["results"],
                db=db
            )

        except Exception as e:
            report.status = "failed"
            report.results_json = json.dumps({"error": str(e)})

        db.commit()
        db.refresh(report)
        return report

    @classmethod
    def _process_results(cls, model_type: str, api_response: dict) -> dict:
        """Process API response and extract summary statistics"""
        results = []
        threats = 0
        total_confidence = 0.0

        predictions = api_response.get("predictions", [])

        for pred in predictions:
            # APIs return prediction as 0/1 integer, not strings
            # prediction=1 means threat, prediction=0 means benign
            prediction_value = pred.get("prediction", 0)
            is_threat = prediction_value == 1 or prediction_value == "1"

            confidence = pred.get("confidence", 0)
            if is_threat:
                threats += 1
            total_confidence += confidence

            # Build result entry with label from prediction_label field
            label = pred.get("prediction_label", "Benign" if not is_threat else "Threat")

            # Get explanation if present
            explanation = pred.get("explanation", None)

            if model_type == "phishing":
                result_entry = {
                    "is_threat": is_threat,
                    "label": label,
                    "confidence": confidence * 100,  # Convert to percentage
                    "risk_level": pred.get("risk_level", "high" if is_threat else "low")
                }
                if explanation:
                    result_entry["explanation"] = explanation
                results.append(result_entry)
            elif model_type == "ato":
                result_entry = {
                    "is_threat": is_threat,
                    "label": label,
                    "confidence": confidence * 100,
                    "risk_level": pred.get("risk_level", "high" if is_threat else "low"),
                    "risk_score": pred.get("risk_score", confidence * 100)
                }
                if explanation:
                    result_entry["explanation"] = explanation
                results.append(result_entry)
            elif model_type == "brute_force":
                result_entry = {
                    "is_threat": is_threat,
                    "label": label,
                    "confidence": confidence * 100,
                    "attack_type": pred.get("attack_type", "Brute Force" if is_threat else "Benign")
                }
                if explanation:
                    result_entry["explanation"] = explanation
                results.append(result_entry)
            else:
                result_entry = {
                    "is_threat": is_threat,
                    "label": label,
                    "confidence": confidence * 100
                }
                if explanation:
                    result_entry["explanation"] = explanation
                results.append(result_entry)

        total = len(results)
        avg_confidence = (total_confidence / total * 100) if total > 0 else 0

        return {
            "threats_detected": threats,
            "benign_count": total - threats,
            "avg_confidence": round(avg_confidence, 2),
            "results": results
        }

    @classmethod
    def list_reports(
        cls,
        db: Session,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """List reports with creator info"""
        query = db.query(Report, User.full_name).join(
            User, Report.created_by == User.id
        )

        reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()

        result = []
        for report, creator_name in reports:
            result.append({
                "id": report.id,
                "title": report.title,
                "model_type": report.model_type,
                "created_at": report.created_at,
                "total_records": report.total_records,
                "threats_detected": report.threats_detected,
                "benign_count": report.benign_count,
                "avg_confidence": report.avg_confidence,
                "status": report.status,
                "created_by_name": creator_name
            })

        return result

    @classmethod
    def get_report(cls, report_id: int, db: Session) -> Optional[dict]:
        """Get report details with full results"""
        result = db.query(Report, User.full_name, UploadedFile.original_filename).join(
            User, Report.created_by == User.id
        ).outerjoin(
            UploadedFile, Report.file_id == UploadedFile.id
        ).filter(Report.id == report_id).first()

        if not result:
            return None

        report, creator_name, file_name = result

        return {
            "id": report.id,
            "title": report.title,
            "model_type": report.model_type,
            "created_at": report.created_at,
            "total_records": report.total_records,
            "threats_detected": report.threats_detected,
            "benign_count": report.benign_count,
            "avg_confidence": report.avg_confidence,
            "status": report.status,
            "created_by_name": creator_name,
            "file_name": file_name,
            "results": json.loads(report.results_json) if report.results_json else None
        }

    @classmethod
    def delete_report(cls, report_id: int, db: Session) -> bool:
        """Delete a report"""
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            return False

        db.delete(report)
        db.commit()
        return True
