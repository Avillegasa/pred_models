"""
Brute Force Dataset Preprocessing Script
=========================================

Dataset: CSE-CIC-IDS2018 (02-14-2018.csv)
Ataques: FTP-BruteForce, SSH-Bruteforce

Pipeline de Preprocessing:
1. Cargar dataset 02-14-2018.csv
2. Eliminar columnas string
3. Limpiar inf/-inf y NaN
4. Convertir Timestamp a epoch
5. Convertir tipos de datos
6. Filtrar outliers (Z-score)
7. Normalizar (MinMaxScaler)
8. Eliminar features correlacionadas
9. Balancear dataset

Output: brute_force_balanced.csv (listo para EDA)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import os
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATASET_PATH = '../dataset/02-14-2018.csv'
OUTPUT_DIR = '.'
ZSCORE_THRESHOLD = 7
CORRELATION_THRESHOLD = 0.99

print("=" * 80)
print("BRUTE FORCE DATASET PREPROCESSING")
print("=" * 80)
print(f"\nInicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Dataset: {DATASET_PATH}")

# ============================================================================
# PASO 1: CARGAR DATASET
# ============================================================================

print("\n" + "=" * 80)
print("PASO 1: CARGANDO DATASET")
print("=" * 80)

df = pd.read_csv(DATASET_PATH, low_memory=False)
print(f"Shape original: {df.shape}")
print(f"\nDistribución de clases:")
print(df['Label'].value_counts())
print(f"\nMemoria usada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ============================================================================
# PASO 2: ELIMINAR COLUMNAS STRING
# ============================================================================

print("\n" + "=" * 80)
print("PASO 2: ELIMINANDO COLUMNAS STRING")
print("=" * 80)

string_columns = ['Flow ID', 'Src IP', 'Dst IP']
existing_string_columns = [col for col in string_columns if col in df.columns]
print(f"Columnas a eliminar: {existing_string_columns}")

df.drop(existing_string_columns, axis=1, inplace=True)
print(f"Shape después de eliminar columnas: {df.shape}")

# ============================================================================
# PASO 3: LIMPIAR INF/-INF Y NaN
# ============================================================================

print("\n" + "=" * 80)
print("PASO 3: LIMPIANDO INF/-INF Y NaN")
print("=" * 80)

# Contar inf antes
inf_count = np.sum(df.values == np.inf)
neg_inf_count = np.sum(df.values == -np.inf)
print(f"Valores +inf: {inf_count}")
print(f"Valores -inf: {neg_inf_count}")

# Reemplazar inf con NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Contar NaN antes de eliminar
nan_count_before = df.isna().sum().sum()
print(f"Valores NaN (antes de dropna): {nan_count_before}")

# Eliminar NaN
df.dropna(inplace=True)
print(f"Shape después de eliminar NaN: {df.shape}")

# ============================================================================
# PASO 4: CONVERTIR TIMESTAMP A EPOCH
# ============================================================================

print("\n" + "=" * 80)
print("PASO 4: CONVIRTIENDO TIMESTAMP A EPOCH")
print("=" * 80)

if 'Timestamp' in df.columns:
    print(f"Timestamp antes: {df['Timestamp'].iloc[0]}")

    # Convertir a datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    # Convertir a epoch (segundos desde 1970-01-01)
    df['Timestamp'] = (df['Timestamp'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    print(f"Timestamp después (epoch): {df['Timestamp'].iloc[0]}")

    # Eliminar NaN generados por errores de conversión
    df.dropna(inplace=True)
    print(f"Shape después de convertir Timestamp: {df.shape}")
else:
    print("Columna Timestamp no encontrada")

# ============================================================================
# PASO 5: CONVERTIR TIPOS DE DATOS A FLOAT
# ============================================================================

print("\n" + "=" * 80)
print("PASO 5: CONVIRTIENDO TIPOS DE DATOS")
print("=" * 80)

# Identificar columnas object
object_columns = df.select_dtypes(include=['object']).columns.tolist()
object_columns = [col for col in object_columns if col != 'Label']
print(f"Columnas tipo object (excepto Label): {len(object_columns)}")

# Convertir a numeric
for col in object_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Eliminar NaN generados
df.dropna(inplace=True)
print(f"Shape después de conversión: {df.shape}")

# ============================================================================
# PASO 6: FILTRAR OUTLIERS (Z-SCORE)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 6: FILTRANDO OUTLIERS (Z-SCORE)")
print("=" * 80)

print(f"Z-score threshold: {ZSCORE_THRESHOLD}")

# Separar FTP, SSH y Benign
df_ftp = df[df['Label'] == 'FTP-BruteForce'].copy()
df_ssh = df[df['Label'] == 'SSH-Bruteforce'].copy()
df_benign = df[df['Label'] == 'Benign'].copy()

print(f"\nAntes del filtrado:")
print(f"FTP-BruteForce: {df_ftp.shape[0]:,}")
print(f"SSH-Bruteforce: {df_ssh.shape[0]:,}")
print(f"Benign: {df_benign.shape[0]:,}")


def filter_outliers_zscore(data, threshold):
    """Filtrar outliers usando Z-score"""
    numeric_cols = [col for col in data.columns if col != 'Label']
    z_scores = np.abs(stats.zscore(data[numeric_cols]))
    outlier_mask = (z_scores > threshold).any(axis=1)
    return data[~outlier_mask]


# Aplicar filtrado a cada clase
df_ftp_filtered = filter_outliers_zscore(df_ftp, ZSCORE_THRESHOLD)
df_ssh_filtered = filter_outliers_zscore(df_ssh, ZSCORE_THRESHOLD)
df_benign_filtered = filter_outliers_zscore(df_benign, ZSCORE_THRESHOLD)

print(f"\nDespués del filtrado:")
print(f"FTP-BruteForce: {df_ftp_filtered.shape[0]:,} (eliminados: {df_ftp.shape[0] - df_ftp_filtered.shape[0]:,})")
print(f"SSH-Bruteforce: {df_ssh_filtered.shape[0]:,} (eliminados: {df_ssh.shape[0] - df_ssh_filtered.shape[0]:,})")
print(f"Benign: {df_benign_filtered.shape[0]:,} (eliminados: {df_benign.shape[0] - df_benign_filtered.shape[0]:,})")

# Recombinar
df = pd.concat([df_ftp_filtered, df_ssh_filtered, df_benign_filtered], axis=0)
print(f"\nShape después de filtrar outliers: {df.shape}")

# ============================================================================
# PASO 7: NORMALIZAR (MINMAXSCALER)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 7: NORMALIZANDO FEATURES (0-1)")
print("=" * 80)

numeric_cols = [col for col in df.columns if col != 'Label']
print(f"Columnas numéricas a normalizar: {len(numeric_cols)}")

# Antes de normalizar
print(f"\nEjemplo antes de normalizar (primera fila):")
print(df[numeric_cols].iloc[0].head(5))

# Normalizar
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Después de normalizar
print(f"\nEjemplo después de normalizar (primera fila):")
print(df[numeric_cols].iloc[0].head(5))

# Limpiar inf/-inf y NaN generados
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
print(f"\nShape después de normalizar: {df.shape}")

# ============================================================================
# PASO 8: ELIMINAR FEATURES CORRELACIONADAS
# ============================================================================

print("\n" + "=" * 80)
print("PASO 8: ELIMINANDO FEATURES CORRELACIONADAS")
print("=" * 80)

print(f"Correlation threshold: {CORRELATION_THRESHOLD}")

# Calcular matriz de correlación
corr_matrix = df[numeric_cols].corr().abs()

# Encontrar features con alta correlación
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if any(upper[column] > CORRELATION_THRESHOLD)]

print(f"\nFeatures a eliminar: {len(to_drop)}")
print(f"Features: {to_drop}")

# Eliminar features
df.drop(to_drop, axis=1, inplace=True)
print(f"\nShape después de eliminar correlaciones: {df.shape}")
print(f"Features finales: {df.shape[1] - 1} (sin contar Label)")

# ============================================================================
# PASO 9: BALANCEAR DATASET
# ============================================================================

print("\n" + "=" * 80)
print("PASO 9: BALANCEANDO DATASET")
print("=" * 80)

# Separar nuevamente
df_ftp = df[df['Label'] == 'FTP-BruteForce'].copy()
df_ssh = df[df['Label'] == 'SSH-Bruteforce'].copy()
df_benign = df[df['Label'] == 'Benign'].copy()

print(f"\nAntes del balanceo:")
print(f"FTP-BruteForce: {df_ftp.shape[0]:,}")
print(f"SSH-Bruteforce: {df_ssh.shape[0]:,}")
print(f"Benign: {df_benign.shape[0]:,}")

# Estrategia de balanceo
# Opción 1: Mantener FTP y SSH separados, balancear cada uno con Benign
print("\nCreando datasets balanceados...")

# Dataset 1: FTP-BruteForce balanceado
df_ftp_shuffled = df_ftp.sample(frac=1, random_state=42)
df_benign_for_ftp = df_benign.sample(n=df_ftp.shape[0], random_state=42)
df_balanced_ftp = pd.concat([df_benign_for_ftp, df_ftp_shuffled], axis=0)
df_balanced_ftp = df_balanced_ftp.sample(frac=1, random_state=42)  # Shuffle final

print(f"\nDataset FTP-BruteForce balanceado:")
print(df_balanced_ftp['Label'].value_counts())

# Dataset 2: SSH-Bruteforce balanceado
df_ssh_shuffled = df_ssh.sample(frac=1, random_state=42)
df_benign_for_ssh = df_benign.sample(n=df_ssh.shape[0], random_state=43)
df_balanced_ssh = pd.concat([df_benign_for_ssh, df_ssh_shuffled], axis=0)
df_balanced_ssh = df_balanced_ssh.sample(frac=1, random_state=42)  # Shuffle final

print(f"\nDataset SSH-Bruteforce balanceado:")
print(df_balanced_ssh['Label'].value_counts())

# Dataset 3: Brute Force unificado (FTP + SSH vs Benign)
total_attacks = df_ftp.shape[0] + df_ssh.shape[0]
df_benign_for_unified = df_benign.sample(n=total_attacks, random_state=44)

# Mapear etiquetas a binario
df_ftp_binary = df_ftp.copy()
df_ssh_binary = df_ssh.copy()
df_ftp_binary['Label'] = 'Brute Force'
df_ssh_binary['Label'] = 'Brute Force'

df_balanced_unified = pd.concat([df_benign_for_unified, df_ftp_binary, df_ssh_binary], axis=0)
df_balanced_unified = df_balanced_unified.sample(frac=1, random_state=42)  # Shuffle final

print(f"\nDataset Brute Force unificado balanceado:")
print(df_balanced_unified['Label'].value_counts())

# ============================================================================
# GUARDAR DATASETS
# ============================================================================

print("\n" + "=" * 80)
print("GUARDANDO DATASETS PROCESADOS")
print("=" * 80)

# Guardar datasets balanceados
output_path_ftp = os.path.join(OUTPUT_DIR, 'brute_force_ftp_balanced.csv')
df_balanced_ftp.to_csv(output_path_ftp, index=False)
print(f"\n✓ Guardado: {output_path_ftp}")
print(f"  Shape: {df_balanced_ftp.shape}")
print(f"  Tamaño: {os.path.getsize(output_path_ftp) / 1024**2:.2f} MB")

output_path_ssh = os.path.join(OUTPUT_DIR, 'brute_force_ssh_balanced.csv')
df_balanced_ssh.to_csv(output_path_ssh, index=False)
print(f"\n✓ Guardado: {output_path_ssh}")
print(f"  Shape: {df_balanced_ssh.shape}")
print(f"  Tamaño: {os.path.getsize(output_path_ssh) / 1024**2:.2f} MB")

output_path_unified = os.path.join(OUTPUT_DIR, 'brute_force_balanced.csv')
df_balanced_unified.to_csv(output_path_unified, index=False)
print(f"\n✓ Guardado: {output_path_unified}")
print(f"  Shape: {df_balanced_unified.shape}")
print(f"  Tamaño: {os.path.getsize(output_path_unified) / 1024**2:.2f} MB")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

print(f"\nDatasets generados:")
print(f"1. brute_force_ftp_balanced.csv - FTP-BruteForce vs Benign (balanceado 50/50)")
print(f"2. brute_force_ssh_balanced.csv - SSH-Bruteforce vs Benign (balanceado 50/50)")
print(f"3. brute_force_balanced.csv - Brute Force vs Benign (balanceado 50/50) ← RECOMENDADO PARA EDA")

print(f"\nFeatures finales: {df_balanced_unified.shape[1] - 1}")
print(f"Registros totales (unified): {df_balanced_unified.shape[0]:,}")

print(f"\nPróximo paso:")
print(f"→ Realizar EDA con: fuerza-bruta/processed_data/brute_force_balanced.csv")

print(f"\nFin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
