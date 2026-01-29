#!/usr/bin/env python3
"""
Script para regenerar reportes después de corregir el procesamiento.
Usa los archivos ya subidos (IDs más recientes).
"""

import requests
import time

BASE_URL = "http://localhost:8003"


def login(username: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    response.raise_for_status()
    return response.json()["access_token"]


def generate_report(token: str, title: str, file_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/reports/generate",
        headers=headers,
        json={"title": title, "file_id": file_id}
    )
    response.raise_for_status()
    return response.json()


def main():
    print("Regenerando reportes con el procesamiento corregido...\n")

    # Login
    token = login("admin", "admin123")
    print("Login exitoso\n")

    # Archivos a usar (los más recientes con 50 filas)
    reports_to_generate = [
        (14, "Campaña Phishing Detectada - Enero 2026"),
        (15, "Revisión de Correos - Semana 4"),
        (16, "Análisis Emails Sospechosos - Q1"),
        (17, "Incidente Account Takeover - 15 Ene"),
        (18, "Actividad Normal de Logins - Semana 4"),
        (19, "Auditoría de Accesos - Enero"),
        (20, "Ataque Brute Force Detectado - 20 Ene"),
        (21, "Baseline de Tráfico - Enero"),
        (22, "Análisis de Firewall - Semana 4"),
    ]

    for file_id, title in reports_to_generate:
        try:
            report = generate_report(token, title, file_id)
            threats = report.get('threats_detected', 0)
            total = report.get('total_records', 0)
            benign = report.get('benign_count', 0)
            confidence = report.get('avg_confidence', 0)
            model = report.get('model_type', 'unknown')

            status = "AMENAZAS DETECTADAS" if threats > 0 else "Sin amenazas"
            print(f"✓ {title}")
            print(f"  Modelo: {model} | {status}")
            print(f"  Resultados: {threats} amenazas / {benign} benignos")
            print(f"  Confianza promedio: {confidence:.1f}%")
            print()
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ Error en '{title}': {e}\n")

    print("\nReportes regenerados. Verifica en http://localhost:5173/reports")


if __name__ == "__main__":
    main()
