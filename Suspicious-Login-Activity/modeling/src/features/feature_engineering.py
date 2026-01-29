"""
FEATURE ENGINEERING para Suspicious Login Activity Detection (Account Takeover)
Adaptado para ejecución local con dataset balanceado RBA

Este módulo extrae features de logins para clasificación de Account Takeover:
- Features temporales (hora, día, tiempo desde último login)
- Features de comportamiento (cambios de IP, browser, device, país)
- Features geográficos (país, región, impossible travel)
- Features de red (RTT, ASN, Attack IP)
- Features categóricos (Browser, OS, Device)
- Features agregados (conteos por usuario, por IP)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from datetime import datetime
import warnings
import joblib
import os

warnings.filterwarnings('ignore')


def parse_timestamps(df):
    """
    Convertir Login Timestamp a datetime y extraer features temporales

    Args:
        df: DataFrame con columna 'Login Timestamp'

    Returns:
        df: DataFrame con features temporales agregadas
    """
    print("🕒 Parseando timestamps y extrayendo features temporales...")

    # Convertir a datetime
    df['timestamp'] = pd.to_datetime(df['Login Timestamp'], errors='coerce')

    # Extraer componentes temporales
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['day_of_month'] = df['timestamp'].dt.day
    df['month'] = df['timestamp'].dt.month

    # Features temporales binarias
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)  # Sábado o Domingo
    df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)  # 10pm-6am
    df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)  # 9am-5pm

    print(f"   ✅ Extracted temporal features: hour, day_of_week, is_weekend, is_night, is_business_hours")

    return df


def calculate_user_behavioral_features(df):
    """
    Calcular features de comportamiento por usuario:
    - Cambios de IP, browser, device, país
    - Conteo de logins
    - Tasa de éxito

    Args:
        df: DataFrame ordenado por User ID y timestamp

    Returns:
        df: DataFrame con features de comportamiento agregadas
    """
    print("👤 Calculando features de comportamiento por usuario...")

    # Ordenar por User ID y timestamp para análisis temporal
    df = df.sort_values(['User ID', 'timestamp']).reset_index(drop=True)

    # --- Cambios de contexto vs login anterior del mismo usuario ---
    df['ip_changed'] = (df.groupby('User ID')['IP Address']
                        .transform(lambda x: (x != x.shift()).astype(int)))

    df['country_changed'] = (df.groupby('User ID')['Country']
                             .transform(lambda x: (x != x.shift()).astype(int)))

    df['browser_changed'] = (df.groupby('User ID')['Browser Name and Version']
                             .transform(lambda x: (x != x.shift()).astype(int)))

    df['device_changed'] = (df.groupby('User ID')['Device Type']
                            .transform(lambda x: (x != x.shift()).astype(int)))

    df['os_changed'] = (df.groupby('User ID')['OS Name and Version']
                        .transform(lambda x: (x != x.shift()).astype(int)))

    # Primer login del usuario (sin login anterior para comparar)
    # Lo marcamos como 0 (no cambió, porque no hay anterior)
    df.loc[df.groupby('User ID').head(1).index,
           ['ip_changed', 'country_changed', 'browser_changed', 'device_changed', 'os_changed']] = 0

    # --- Tiempo desde último login del mismo usuario ---
    df['time_since_last_login_hours'] = (
        df.groupby('User ID')['timestamp']
        .diff()
        .dt.total_seconds() / 3600  # Convertir a horas
    )
    df['time_since_last_login_hours'] = df['time_since_last_login_hours'].fillna(-1)  # -1 = primer login

    # Features derivadas de tiempo
    df['is_rapid_login'] = (df['time_since_last_login_hours'] < 1).astype(int)  # Login en < 1 hora
    df['is_long_gap'] = (df['time_since_last_login_hours'] > 24).astype(int)  # Gap > 24 horas

    # --- Agregaciones por usuario ---
    user_stats = df.groupby('User ID').agg({
        'IP Address': 'nunique',
        'Country': 'nunique',
        'Browser Name and Version': 'nunique',
        'Device Type': 'nunique',
        'Login Successful': ['sum', 'count']
    }).reset_index()

    user_stats.columns = ['User ID', 'ip_count_per_user', 'country_count_per_user',
                          'browser_count_per_user', 'device_count_per_user',
                          'successful_logins_per_user', 'total_logins_per_user']

    # Tasa de éxito por usuario
    user_stats['success_rate_per_user'] = (
        user_stats['successful_logins_per_user'] / user_stats['total_logins_per_user']
    )

    # Merge back al dataframe original
    df = df.merge(user_stats, on='User ID', how='left')

    print(f"   ✅ Behavioral features: ip_changed, country_changed, browser_changed, device_changed, os_changed")
    print(f"   ✅ User aggregations: ip_count_per_user, country_count_per_user, success_rate_per_user")

    return df


def calculate_ip_features(df):
    """
    Calcular features de IP:
    - Conteo de usuarios por IP (credential stuffing)
    - IP es nueva para el usuario

    Args:
        df: DataFrame con columnas 'IP Address' y 'User ID'

    Returns:
        df: DataFrame con features de IP agregadas
    """
    print("🌐 Calculando features de IP y red...")

    # Usuarios por IP (posible credential stuffing)
    ip_stats = df.groupby('IP Address')['User ID'].nunique().reset_index()
    ip_stats.columns = ['IP Address', 'user_count_per_ip']
    df = df.merge(ip_stats, on='IP Address', how='left')

    # IP sospechosa (múltiples usuarios)
    df['is_suspicious_ip'] = (df['user_count_per_ip'] > 10).astype(int)

    # RTT Z-score (anomalía de latencia)
    # Nombre correcto de la columna: 'Round-Trip Time [ms]'
    rtt_col = 'Round-Trip Time [ms]' if 'Round-Trip Time [ms]' in df.columns else 'Round-Trip Time (RTT)'
    if rtt_col in df.columns:
        rtt_mean = df[rtt_col].mean()
        rtt_std = df[rtt_col].std()
        df['rtt_zscore'] = (df[rtt_col] - rtt_mean) / (rtt_std + 1e-6)
        df['is_abnormal_rtt'] = (np.abs(df['rtt_zscore']) > 2).astype(int)  # > 2 std deviations
    else:
        df['rtt_zscore'] = 0
        df['is_abnormal_rtt'] = 0

    print(f"   ✅ IP features: user_count_per_ip, is_suspicious_ip, rtt_zscore, is_abnormal_rtt")

    return df


def encode_categorical_features(df, encoders=None, fit=True):
    """
    Encoding de features categóricos usando LabelEncoder

    Args:
        df: DataFrame con features categóricos
        encoders: Diccionario de encoders pre-entrenados (para test set)
        fit: Si True, fit nuevos encoders; si False, usar existentes

    Returns:
        df: DataFrame con features encoded
        encoders: Diccionario de encoders (para guardar y reutilizar)
    """
    print("🏷️  Encoding categorical features...")

    # Categorical features (solo los que existen en el dataset)
    categorical_features = [
        'Browser Name and Version',
        'OS Name and Version',
        'Device Type',
        'Country',
        'Region',
        'City'
        # 'ISP' y 'ASN Organization' no están en este dataset
    ]

    if encoders is None:
        encoders = {}

    for feature in categorical_features:
        if feature not in df.columns:
            continue

        if fit:
            # Fit nuevo encoder
            le = LabelEncoder()
            # Manejar valores nulos
            df[feature] = df[feature].fillna('Unknown')
            df[f'{feature}_encoded'] = le.fit_transform(df[feature].astype(str))
            encoders[feature] = le
        else:
            # Usar encoder existente
            if feature not in encoders:
                print(f"   ⚠️  Warning: No encoder found for {feature}, skipping...")
                continue

            le = encoders[feature]
            df[feature] = df[feature].fillna('Unknown')

            # Manejar categorías nuevas no vistas en training
            def safe_transform(x):
                try:
                    return le.transform([str(x)])[0]
                except:
                    return -1  # Unknown category

            df[f'{feature}_encoded'] = df[feature].astype(str).apply(safe_transform)

    print(f"   ✅ Encoded {len(categorical_features)} categorical features")

    return df, encoders


def create_final_features(df):
    """
    Seleccionar y organizar features finales para modelado

    Args:
        df: DataFrame con todas las features engineered

    Returns:
        features_df: DataFrame solo con features finales
    """
    print("🔗 Creando conjunto final de features...")

    # Features numéricas directas (verificar nombres correctos)
    numeric_features = []

    # RTT - verificar nombre correcto
    if 'Round-Trip Time [ms]' in df.columns:
        numeric_features.append('Round-Trip Time [ms]')
    elif 'Round-Trip Time (RTT)' in df.columns:
        numeric_features.append('Round-Trip Time (RTT)')

    # Otras features numéricas
    if 'ASN' in df.columns:
        numeric_features.append('ASN')
    if 'Login Successful' in df.columns:
        numeric_features.append('Login Successful')
    if 'Is Attack IP' in df.columns:
        numeric_features.append('Is Attack IP')

    # Features temporales
    temporal_features = [
        'hour',
        'day_of_week',
        'day_of_month',
        'month',
        'is_weekend',
        'is_night',
        'is_business_hours'
    ]

    # Features de comportamiento
    behavioral_features = [
        'ip_changed',
        'country_changed',
        'browser_changed',
        'device_changed',
        'os_changed',
        'time_since_last_login_hours',
        'is_rapid_login',
        'is_long_gap'
    ]

    # Features agregados
    aggregated_features = [
        'ip_count_per_user',
        'country_count_per_user',
        'browser_count_per_user',
        'device_count_per_user',
        'total_logins_per_user',
        'success_rate_per_user',
        'user_count_per_ip',
        'is_suspicious_ip',
        'rtt_zscore',
        'is_abnormal_rtt'
    ]

    # Features categóricos encoded (solo los que existen)
    categorical_encoded_features = [
        f'{feat}_encoded' for feat in [
            'Browser Name and Version',
            'OS Name and Version',
            'Device Type',
            'Country',
            'Region',
            'City'
        ] if f'{feat}_encoded' in df.columns
    ]

    # Combinar todas las features
    all_features = (numeric_features + temporal_features + behavioral_features +
                   aggregated_features + categorical_encoded_features)

    # Filtrar solo features que existen
    available_features = [f for f in all_features if f in df.columns]

    features_df = df[available_features].copy()

    # Agregar target si existe
    if 'Is Account Takeover' in df.columns:
        features_df['label'] = df['Is Account Takeover'].astype(int)

    # Manejar valores infinitos y NaN
    features_df = features_df.replace([np.inf, -np.inf], np.nan)

    # Llenar NaN con 0 (estrategia simple pero efectiva)
    features_df = features_df.fillna(0)

    print(f"   ✅ Total features: {len(available_features)}")
    print(f"      - Numeric: {len(numeric_features)}")
    print(f"      - Temporal: {len(temporal_features)}")
    print(f"      - Behavioral: {len(behavioral_features)}")
    print(f"      - Aggregated: {len(aggregated_features)}")
    print(f"      - Categorical Encoded: {len([f for f in categorical_encoded_features if f in available_features])}")

    if 'label' in features_df.columns:
        print(f"\n   📊 Label distribution:")
        print(f"      - Account Takeover: {features_df['label'].sum()} ({features_df['label'].sum()/len(features_df)*100:.4f}%)")
        print(f"      - Normal: {len(features_df) - features_df['label'].sum()} ({(len(features_df) - features_df['label'].sum())/len(features_df)*100:.4f}%)")

    return features_df


def engineer_features(df, encoders=None, fit_encoders=True):
    """
    Pipeline completo de feature engineering para Account Takeover detection

    Args:
        df: DataFrame con datos raw del RBA dataset
        encoders: Diccionario de encoders pre-entrenados (para test set)
        fit_encoders: Si True, fit nuevos encoders; si False, usar existentes

    Returns:
        features_df: DataFrame con features engineered
        encoders: Diccionario de encoders (para guardar y reutilizar)
    """
    print("=" * 80)
    print("🔧 INICIANDO FEATURE ENGINEERING - ACCOUNT TAKEOVER DETECTION")
    print("=" * 80)
    print(f"\n📊 Dataset input: {len(df):,} registros, {len(df.columns)} columnas")

    df = df.copy()

    # 1. Parse timestamps y features temporales
    df = parse_timestamps(df)

    # 2. Features de comportamiento por usuario
    df = calculate_user_behavioral_features(df)

    # 3. Features de IP y red
    df = calculate_ip_features(df)

    # 4. Encoding de categóricos
    df, encoders = encode_categorical_features(df, encoders=encoders, fit=fit_encoders)

    # 5. Crear conjunto final de features
    features_df = create_final_features(df)

    print("\n" + "=" * 80)
    print("✅ FEATURE ENGINEERING COMPLETADO")
    print("=" * 80)
    print(f"📊 Features creadas: {features_df.shape[1] - (1 if 'label' in features_df.columns else 0)}")
    print(f"📊 Registros finales: {len(features_df):,}")

    return features_df, encoders


def save_features_and_encoders(features_df, encoders, output_dir):
    """Guardar features y encoders"""
    os.makedirs(output_dir, exist_ok=True)

    # Guardar features
    features_path = os.path.join(output_dir, 'features.csv')
    features_df.to_csv(features_path, index=False)
    print(f"💾 Features guardadas en: {features_path}")

    # Guardar encoders
    encoders_path = os.path.join(output_dir, 'label_encoders.pkl')
    joblib.dump(encoders, encoders_path)
    print(f"💾 Encoders guardados en: {encoders_path}")

    return features_path, encoders_path


def load_encoders(encoders_path):
    """Cargar encoders guardados"""
    return joblib.load(encoders_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Feature Engineering para Account Takeover Detection')
    parser.add_argument('--input_data', type=str, required=True, help='Path al CSV de entrada')
    parser.add_argument('--output_dir', type=str, required=True, help='Directorio de salida')

    args = parser.parse_args()

    # Cargar datos
    print(f"📂 Cargando datos desde: {args.input_data}")
    df = pd.read_csv(args.input_data)

    # Feature engineering
    features_df, encoders = engineer_features(df, fit_encoders=True)

    # Guardar
    save_features_and_encoders(features_df, encoders, args.output_dir)

    print("\n🎯 Feature Engineering completado exitosamente!")
