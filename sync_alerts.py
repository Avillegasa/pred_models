#!/usr/bin/env python3
"""
Script para sincronizar alertas con los reportes existentes.
Recorre todos los reportes completados y genera alertas retroactivas
para las predicciones que superen los umbrales configurados.
"""

import sys
import os
import json

# Add auth-gateway to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth-gateway"))

from app.database import SessionLocal, engine, Base
from app.models.alert import Alert
from app.models.report import Report
from app.services.alert_service import AlertService


def main():
    print("=" * 60)
    print("SYNC ALERTS - Generar alertas desde reportes existentes")
    print("=" * 60)

    # Create alerts table if it doesn't exist
    print("\n[1/3] Creando tabla de alertas si no existe...")
    Base.metadata.create_all(bind=engine)
    print("    OK")

    db = SessionLocal()

    try:
        # Check existing alerts
        existing_alerts = db.query(Alert).count()
        print(f"\n[2/3] Estado actual: {existing_alerts} alertas en la base de datos")

        if existing_alerts > 0:
            print("    Limpiando alertas existentes para regenerar...")
            db.query(Alert).delete()
            db.commit()
            print("    OK")

        # Get all completed reports
        reports = db.query(Report).filter(Report.status == "completed").all()
        print(f"\n[3/3] Procesando {len(reports)} reportes completados...")

        total_alerts = 0

        for report in reports:
            if not report.results_json:
                print(f"    - Reporte #{report.id} '{report.title}': sin resultados, saltando")
                continue

            try:
                predictions = json.loads(report.results_json)
            except json.JSONDecodeError:
                print(f"    - Reporte #{report.id} '{report.title}': JSON invalido, saltando")
                continue

            # Count threats in this report
            threats = [p for p in predictions if p.get("is_threat", False)]

            # Generate alerts
            alerts = AlertService.generate_alerts_from_predictions(
                model_type=report.model_type,
                report_id=report.id,
                predictions=predictions,
                db=db
            )

            total_alerts += len(alerts)

            # Summary per report
            if alerts:
                severities = {}
                for a in alerts:
                    severities[a.severity] = severities.get(a.severity, 0) + 1
                sev_str = ", ".join(f"{k}: {v}" for k, v in sorted(severities.items()))
                print(f"    + Reporte #{report.id} '{report.title}' ({report.model_type})")
                print(f"      {len(threats)} amenazas -> {len(alerts)} alertas generadas [{sev_str}]")
            else:
                print(f"    - Reporte #{report.id} '{report.title}' ({report.model_type})")
                print(f"      {len(threats)} amenazas -> 0 alertas (bajo umbral)")

        # Final stats
        stats = AlertService.get_alert_stats(db)
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"  Total alertas generadas: {total_alerts}")
        print(f"  Sin leer: {stats['unread']}")
        print(f"  Por severidad:")
        print(f"    Criticas: {stats['by_severity']['critical']}")
        print(f"    Altas:    {stats['by_severity']['high']}")
        print(f"    Medias:   {stats['by_severity']['medium']}")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()
