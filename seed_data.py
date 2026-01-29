#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos realistas.
Usa los datasets existentes y las APIs en ejecución.
"""

import requests
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime

BASE_URL = "http://localhost:8003"
PHISHING_DATA = "/home/megalodon/dev/cbproy/pred_model/Phishing/processed_data/test.csv"
ATO_DATA = "/home/megalodon/dev/cbproy/pred_model/Suspicious-Login-Activity/processed_data/rba_reduced.csv"
BRUTE_FORCE_DATA = "/home/megalodon/dev/cbproy/pred_model/fuerza-bruta/processed_data/brute_force_balanced.csv"


def login(username: str, password: str) -> str:
    """Obtener token JWT."""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    response.raise_for_status()
    return response.json()["access_token"]


def upload_file(token: str, file_content: bytes, filename: str) -> dict:
    """Subir archivo CSV."""
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (filename, file_content, "text/csv")}
    response = requests.post(
        f"{BASE_URL}/files/upload",
        headers=headers,
        files=files
    )
    response.raise_for_status()
    return response.json()


def generate_report(token: str, title: str, file_id: int) -> dict:
    """Generar reporte a partir de archivo."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/reports/generate",
        headers=headers,
        json={"title": title, "file_id": file_id}
    )
    response.raise_for_status()
    return response.json()


def create_phishing_samples():
    """Crear muestras de datos de phishing."""
    df = pd.read_csv(PHISHING_DATA)

    # Muestra 1: Mayoría phishing (campaña detectada)
    phishing_df = df[df['label'] == 1].sample(n=min(40, len(df[df['label'] == 1])), random_state=42)
    legit_df = df[df['label'] == 0].sample(n=min(10, len(df[df['label'] == 0])), random_state=42)
    sample1 = pd.concat([phishing_df, legit_df]).sample(frac=1, random_state=42)

    # Muestra 2: Mayoría legítimo (operación normal)
    phishing_df2 = df[df['label'] == 1].sample(n=min(5, len(df[df['label'] == 1])), random_state=123)
    legit_df2 = df[df['label'] == 0].sample(n=min(45, len(df[df['label'] == 0])), random_state=123)
    sample2 = pd.concat([phishing_df2, legit_df2]).sample(frac=1, random_state=123)

    # Muestra 3: Mixta
    phishing_df3 = df[df['label'] == 1].sample(n=min(25, len(df[df['label'] == 1])), random_state=456)
    legit_df3 = df[df['label'] == 0].sample(n=min(25, len(df[df['label'] == 0])), random_state=456)
    sample3 = pd.concat([phishing_df3, legit_df3]).sample(frac=1, random_state=456)

    return [
        ("phishing_campaign_enero_2026.csv", sample1, "Análisis Campaña Phishing - Enero 2026"),
        ("emails_revision_semanal.csv", sample2, "Revisión Semanal de Correos - Semana 3"),
        ("emails_sospechosos_q1.csv", sample3, "Emails Sospechosos Q1 2026"),
    ]


def create_ato_samples():
    """Crear muestras de datos de Account Takeover."""
    df = pd.read_csv(ATO_DATA)

    # Renombrar columnas para que coincidan con lo esperado por la API
    df = df.rename(columns={
        'User ID': 'user_id',
        'IP Address': 'ip_address',
        'Country': 'country',
        'Region': 'region',
        'City': 'city',
        'Browser Name and Version': 'browser',
        'OS Name and Version': 'os',
        'Device Type': 'device',
        'Login Successful': 'login_successful',
        'Is Attack IP': 'is_attack_ip',
        'Is Account Takeover': 'is_ato',
        'ASN': 'asn',
        'Round-Trip Time [ms]': 'rtt'
    })

    # Convertir booleanos a int
    df['login_successful'] = df['login_successful'].astype(int)
    df['is_attack_ip'] = df['is_attack_ip'].astype(int)

    # Rellenar valores nulos
    df['rtt'] = df['rtt'].fillna(50.0)
    df['region'] = df['region'].fillna('Unknown')
    df['city'] = df['city'].fillna('Unknown')
    df['device'] = df['device'].fillna('Desktop')

    # Convertir user_id a string
    df['user_id'] = df['user_id'].astype(str)

    # Seleccionar solo las columnas necesarias (sin is_attack_ip para el upload)
    cols_for_api = ['user_id', 'ip_address', 'country', 'region', 'city', 'browser', 'os',
                    'device', 'login_successful', 'is_attack_ip', 'asn', 'rtt']

    # Muestra 1: Algunos ATOs (incidente detectado)
    ato_df = df[df['is_attack_ip'] == 1].sample(n=min(8, len(df[df['is_attack_ip'] == 1])), random_state=42)
    normal_df = df[df['is_attack_ip'] == 0].sample(n=min(42, len(df[df['is_attack_ip'] == 0])), random_state=42)
    sample1 = pd.concat([ato_df, normal_df]).sample(frac=1, random_state=42)[cols_for_api]

    # Muestra 2: Todo normal
    sample2 = df[df['is_attack_ip'] == 0].sample(n=min(50, len(df[df['is_attack_ip'] == 0])), random_state=123)[cols_for_api]

    # Muestra 3: Actividad sospechosa variada
    ato_df3 = df[df['is_attack_ip'] == 1].sample(n=min(15, len(df[df['is_attack_ip'] == 1])), random_state=456)
    normal_df3 = df[df['is_attack_ip'] == 0].sample(n=min(35, len(df[df['is_attack_ip'] == 0])), random_state=456)
    sample3 = pd.concat([ato_df3, normal_df3]).sample(frac=1, random_state=456)[cols_for_api]

    return [
        ("logins_incidente_20260115.csv", sample1, "Incidente ATO Detectado - 15 Enero"),
        ("logins_normales_semana3.csv", sample2, "Actividad de Logins - Semana 3"),
        ("logins_revision_mensual.csv", sample3, "Revisión Mensual de Accesos - Enero"),
    ]


def create_brute_force_samples():
    """Crear muestras de datos de Brute Force."""
    df = pd.read_csv(BRUTE_FORCE_DATA)

    # Renombrar columnas para el formato esperado (lowercase con underscore)
    col_mapping = {
        'Dst Port': 'dst_port',
        'Protocol': 'protocol',
        'Timestamp': 'timestamp',
        'Flow Duration': 'flow_duration',
        'Tot Fwd Pkts': 'tot_fwd_pkts',
        'Tot Bwd Pkts': 'tot_bwd_pkts',
        'TotLen Fwd Pkts': 'totlen_fwd_pkts',
        'Fwd Pkt Len Max': 'fwd_pkt_len_max',
        'Fwd Pkt Len Min': 'fwd_pkt_len_min',
        'Fwd Pkt Len Mean': 'fwd_pkt_len_mean',
        'Fwd Pkt Len Std': 'fwd_pkt_len_std',
        'Bwd Pkt Len Max': 'bwd_pkt_len_max',
        'Bwd Pkt Len Min': 'bwd_pkt_len_min',
        'Bwd Pkt Len Mean': 'bwd_pkt_len_mean',
        'Bwd Pkt Len Std': 'bwd_pkt_len_std',
        'Flow Byts/s': 'flow_byts_s',
        'Flow Pkts/s': 'flow_pkts_s',
        'Flow IAT Mean': 'flow_iat_mean',
        'Flow IAT Std': 'flow_iat_std',
        'Flow IAT Max': 'flow_iat_max',
        'Fwd IAT Std': 'fwd_iat_std',
        'Bwd IAT Tot': 'bwd_iat_tot',
        'Bwd IAT Mean': 'bwd_iat_mean',
        'Bwd IAT Std': 'bwd_iat_std',
        'Bwd IAT Max': 'bwd_iat_max',
        'Bwd IAT Min': 'bwd_iat_min',
        'Fwd PSH Flags': 'fwd_psh_flags',
        'Bwd PSH Flags': 'bwd_psh_flags',
        'Fwd URG Flags': 'fwd_urg_flags',
        'Bwd URG Flags': 'bwd_urg_flags',
        'Fwd Pkts/s': 'fwd_pkts_s',
        'Bwd Pkts/s': 'bwd_pkts_s',
        'Pkt Len Min': 'pkt_len_min',
        'Pkt Len Max': 'pkt_len_max',
        'Pkt Len Mean': 'pkt_len_mean',
        'Pkt Len Std': 'pkt_len_std',
        'Pkt Len Var': 'pkt_len_var',
        'FIN Flag Cnt': 'fin_flag_cnt',
        'RST Flag Cnt': 'rst_flag_cnt',
        'PSH Flag Cnt': 'psh_flag_cnt',
        'ACK Flag Cnt': 'ack_flag_cnt',
        'URG Flag Cnt': 'urg_flag_cnt',
        'CWE Flag Count': 'cwe_flag_count',
        'Down/Up Ratio': 'down_up_ratio',
        'Fwd Byts/b Avg': 'fwd_byts_b_avg',
        'Fwd Pkts/b Avg': 'fwd_pkts_b_avg',
        'Fwd Blk Rate Avg': 'fwd_blk_rate_avg',
        'Bwd Byts/b Avg': 'bwd_byts_b_avg',
        'Bwd Pkts/b Avg': 'bwd_pkts_b_avg',
        'Bwd Blk Rate Avg': 'bwd_blk_rate_avg',
        'Init Fwd Win Byts': 'init_fwd_win_byts',
        'Init Bwd Win Byts': 'init_bwd_win_byts',
        'Fwd Act Data Pkts': 'fwd_act_data_pkts',
        'Fwd Seg Size Min': 'fwd_seg_size_min',
        'Active Mean': 'active_mean',
        'Active Std': 'active_std',
        'Active Max': 'active_max',
        'Active Min': 'active_min',
        'Idle Mean': 'idle_mean',
        'Idle Std': 'idle_std',
        'Label': 'label'
    }

    df = df.rename(columns=col_mapping)

    # Eliminar Timestamp si existe (no se usa en el modelo)
    if 'timestamp' in df.columns:
        df = df.drop(columns=['timestamp'])

    # Crear columna binaria para filtrado (Label es "Benign" o "Brute Force")
    df['is_attack'] = (df['label'] == 'Brute Force').astype(int)

    # Columnas para el archivo (sin label)
    feature_cols = [c for c in df.columns if c not in ['label', 'is_attack']]

    # Muestra 1: Ataque activo (mayoría ataques)
    attack_df = df[df['is_attack'] == 1].sample(n=min(45, len(df[df['is_attack'] == 1])), random_state=42)
    benign_df = df[df['is_attack'] == 0].sample(n=min(5, len(df[df['is_attack'] == 0])), random_state=42)
    sample1 = pd.concat([attack_df, benign_df]).sample(frac=1, random_state=42)[feature_cols]

    # Muestra 2: Tráfico normal
    sample2 = df[df['is_attack'] == 0].sample(n=min(50, len(df[df['is_attack'] == 0])), random_state=123)[feature_cols]

    # Muestra 3: Detección mixta
    attack_df3 = df[df['is_attack'] == 1].sample(n=min(30, len(df[df['is_attack'] == 1])), random_state=456)
    benign_df3 = df[df['is_attack'] == 0].sample(n=min(20, len(df[df['is_attack'] == 0])), random_state=456)
    sample3 = pd.concat([attack_df3, benign_df3]).sample(frac=1, random_state=456)[feature_cols]

    return [
        ("netflow_ataque_ssh_20260120.csv", sample1, "Ataque SSH Brute Force - 20 Enero"),
        ("netflow_baseline_enero.csv", sample2, "Baseline de Red - Enero 2026"),
        ("netflow_revision_firewall.csv", sample3, "Análisis Firewall - Semana 3"),
    ]


def main():
    print("=" * 60)
    print("SEED DATA - Sistema de Predicción de Ciberseguridad")
    print("=" * 60)

    # Login como admin
    print("\n[1/4] Autenticando como admin...")
    try:
        token = login("admin", "admin123")
        print("    ✓ Login exitoso")
    except Exception as e:
        print(f"    ✗ Error de login: {e}")
        return

    # Generar muestras
    print("\n[2/4] Generando muestras de datasets...")
    all_samples = []

    print("    - Phishing samples...")
    all_samples.extend(create_phishing_samples())

    print("    - Account Takeover samples...")
    all_samples.extend(create_ato_samples())

    print("    - Brute Force samples...")
    all_samples.extend(create_brute_force_samples())

    print(f"    ✓ {len(all_samples)} muestras generadas")

    # Subir archivos y generar reportes
    print("\n[3/4] Subiendo archivos...")
    uploaded_files = []

    for filename, df, report_title in all_samples:
        try:
            # Convertir DataFrame a CSV bytes
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode('utf-8')

            # Subir archivo
            file_info = upload_file(token, csv_bytes, filename)
            uploaded_files.append((file_info, report_title))
            print(f"    ✓ {filename} ({file_info['row_count']} filas, modelo: {file_info['detected_model']})")
        except Exception as e:
            print(f"    ✗ Error subiendo {filename}: {e}")

    # Generar reportes
    print("\n[4/4] Generando reportes...")
    reports_created = 0

    for file_info, report_title in uploaded_files:
        try:
            report = generate_report(token, report_title, file_info['id'])
            threats = report.get('threats_detected', 0)
            total = report.get('total_records', 0)
            confidence = report.get('avg_confidence', 0)
            print(f"    ✓ '{report_title}'")
            print(f"      Amenazas: {threats}/{total} | Confianza: {confidence:.1f}%")
            reports_created += 1
            time.sleep(0.5)  # Pequeña pausa entre reportes
        except Exception as e:
            print(f"    ✗ Error generando reporte '{report_title}': {e}")

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"  Archivos subidos: {len(uploaded_files)}")
    print(f"  Reportes generados: {reports_created}")
    print("\n  Puedes ver los datos en: http://localhost:5173")
    print("  Login: admin / admin123")
    print("=" * 60)


if __name__ == "__main__":
    main()
