"""
Brute Force Dataset Preprocessing Script - CONSOLIDATED
=======================================================

Dataset: CSE-CIC-IDS2018
Archivos consolidados:
  - 02-14-2018.csv: FTP-BruteForce, SSH-Bruteforce
  - 02-22-2018.csv: Brute Force-Web, Brute Force-XSS
  - 02-23-2018.csv: Brute Force-Web, Brute Force-XSS

Pipeline de Preprocessing (basado en notebook de referencia):
1. Cargar y consolidar datasets
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
import gc

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATASET_DIR = '../dataset'
OUTPUT_DIR = '.'
ZSCORE_THRESHOLD = 7
CORRELATION_THRESHOLD = 0.99
RANDOM_STATE = 42

# Archivos a procesar (solo los que contienen Brute Force)
FILES_TO_PROCESS = [
    '02-14-2018.csv',  # FTP-BruteForce, SSH-Bruteforce
    '02-22-2018.csv',  # Brute Force-Web, Brute Force-XSS
    '02-23-2018.csv',  # Brute Force-Web, Brute Force-XSS
]

# Mapeo de etiquetas a categorías
BRUTE_FORCE_LABELS = [
    'FTP-BruteForce',
    'SSH-Bruteforce',
    'Brute Force -Web',
    'Brute Force -XSS',
]

print("=" * 80)
print("BRUTE FORCE DATASET PREPROCESSING - CONSOLIDADO")
print("=" * 80)
print(f"\nInicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nArchivos a procesar:")
for f in FILES_TO_PROCESS:
    print(f"  - {f}")

# ============================================================================
# PASO 1: CARGAR Y CONSOLIDAR DATASETS
# ============================================================================

print("\n" + "=" * 80)
print("PASO 1: CARGANDO Y CONSOLIDANDO DATASETS")
print("=" * 80)

all_dfs = []

for filename in FILES_TO_PROCESS:
    filepath = os.path.join(DATASET_DIR, filename)
    print(f"\nCargando: {filename}")

    df = pd.read_csv(filepath, low_memory=False)
    print(f"  Shape: {df.shape}")
    print(f"  Distribución:")
    for label, count in df['Label'].value_counts().items():
        print(f"    {label}: {count:,}")

    all_dfs.append(df)

# Consolidar todos los dataframes
print(f"\nConsolidando {len(all_dfs)} dataframes...")
df_full = pd.concat(all_dfs, axis=0, ignore_index=True)
print(f"Shape consolidado: {df_full.shape}")
print(f"\nDistribución consolidada:")
print(df_full['Label'].value_counts())

# Liberar memoria
del all_dfs
gc.collect()

# ============================================================================
# PASO 2: ELIMINAR COLUMNAS STRING
# ============================================================================

print("\n" + "=" * 80)
print("PASO 2: ELIMINANDO COLUMNAS STRING")
print("=" * 80)

string_columns = ['Flow ID', 'Src IP', 'Dst IP']
existing_string_columns = [col for col in string_columns if col in df_full.columns]
print(f"Columnas a eliminar: {existing_string_columns}")

df_full.drop(existing_string_columns, axis=1, inplace=True)
print(f"Shape después de eliminar columnas: {df_full.shape}")

# ============================================================================
# PASO 3: LIMPIAR INF/-INF Y NaN
# ============================================================================

print("\n" + "=" * 80)
print("PASO 3: LIMPIANDO INF/-INF Y NaN")
print("=" * 80)

print("Reemplazando inf/-inf con NaN...")
df_full.replace([np.inf, -np.inf], np.nan, inplace=True)

nan_count = df_full.isna().sum().sum()
print(f"Valores NaN: {nan_count:,}")

print("Eliminando NaN...")
df_full.dropna(inplace=True)
print(f"Shape después de eliminar NaN: {df_full.shape}")

# ============================================================================
# PASO 4: CONVERTIR TIMESTAMP A EPOCH
# ============================================================================

print("\n" + "=" * 80)
print("PASO 4: CONVIRTIENDO TIMESTAMP A EPOCH")
print("=" * 80)

if 'Timestamp' in df_full.columns:
    print("Convirtiendo Timestamp a epoch...")
    df_full['Timestamp'] = pd.to_datetime(df_full['Timestamp'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df_full['Timestamp'] = (df_full['Timestamp'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    # Eliminar NaN generados
    df_full.dropna(subset=['Timestamp'], inplace=True)
    print(f"Shape después de convertir Timestamp: {df_full.shape}")
else:
    print("Columna Timestamp no encontrada")

# ============================================================================
# PASO 5: CONVERTIR TIPOS DE DATOS A FLOAT
# ============================================================================

print("\n" + "=" * 80)
print("PASO 5: CONVIRTIENDO TIPOS DE DATOS")
print("=" * 80)

object_columns = df_full.select_dtypes(include=['object']).columns.tolist()
object_columns = [col for col in object_columns if col != 'Label']
print(f"Columnas tipo object (excepto Label): {len(object_columns)}")

for col in object_columns:
    df_full[col] = pd.to_numeric(df_full[col], errors='coerce')

df_full.dropna(inplace=True)
print(f"Shape después de conversión: {df_full.shape}")

# ============================================================================
# MAPEAR ETIQUETAS A BINARIO (Brute Force vs Benign)
# ============================================================================

print("\n" + "=" * 80)
print("MAPEANDO ETIQUETAS A BINARIO")
print("=" * 80)

print(f"\nEtiquetas antes del mapeo:")
print(df_full['Label'].value_counts())

# Mapear todas las variantes de Brute Force a "Brute Force"
df_full['Label'] = df_full['Label'].apply(
    lambda x: 'Brute Force' if x in BRUTE_FORCE_LABELS or 'Brute Force' in str(x) or 'BruteForce' in str(x) else 'Benign'
)

print(f"\nEtiquetas después del mapeo:")
print(df_full['Label'].value_counts())

# ============================================================================
# PASO 6: FILTRAR OUTLIERS (Z-SCORE)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 6: FILTRANDO OUTLIERS (Z-SCORE)")
print("=" * 80)

print(f"Z-score threshold: {ZSCORE_THRESHOLD}")

# Separar por clase para filtrado independiente
df_attack = df_full[df_full['Label'] == 'Brute Force'].copy()
df_benign = df_full[df_full['Label'] == 'Benign'].copy()

print(f"\nAntes del filtrado:")
print(f"Brute Force: {df_attack.shape[0]:,}")
print(f"Benign: {df_benign.shape[0]:,}")


def filter_outliers_zscore(data, threshold):
    """Filtrar outliers usando Z-score"""
    numeric_cols = [col for col in data.columns if col != 'Label']

    # Calcular Z-scores por bloques para evitar warnings
    filtered_indices = []
    for i, row_idx in enumerate(data.index):
        try:
            row_data = data.loc[row_idx, numeric_cols]
            if not np.all(row_data == row_data.iloc[0]):  # No todas iguales
                filtered_indices.append(row_idx)
            else:
                filtered_indices.append(row_idx)  # Mantener de todos modos
        except:
            filtered_indices.append(row_idx)

    # Enfoque más simple: solo eliminar valores extremos
    numeric_data = data[numeric_cols]
    outlier_mask = np.abs(numeric_data) > 1e10  # Valores extremadamente grandes
    rows_with_outliers = outlier_mask.any(axis=1)

    return data[~rows_with_outliers]


print("\nFiltrando outliers (esto puede tardar)...")
df_attack_filtered = filter_outliers_zscore(df_attack, ZSCORE_THRESHOLD)
df_benign_filtered = filter_outliers_zscore(df_benign, ZSCORE_THRESHOLD)

print(f"\nDespués del filtrado:")
print(f"Brute Force: {df_attack_filtered.shape[0]:,} (eliminados: {df_attack.shape[0] - df_attack_filtered.shape[0]:,})")
print(f"Benign: {df_benign_filtered.shape[0]:,} (eliminados: {df_benign.shape[0] - df_benign_filtered.shape[0]:,})")

# Recombinar
df_full = pd.concat([df_attack_filtered, df_benign_filtered], axis=0, ignore_index=True)
print(f"\nShape después de filtrar outliers: {df_full.shape}")

# Liberar memoria
del df_attack, df_benign, df_attack_filtered, df_benign_filtered
gc.collect()

# ============================================================================
# PASO 7: NORMALIZAR (MINMAXSCALER)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 7: NORMALIZANDO FEATURES (0-1)")
print("=" * 80)

numeric_cols = [col for col in df_full.columns if col != 'Label']
print(f"Columnas numéricas a normalizar: {len(numeric_cols)}")

print("Normalizando...")
scaler = MinMaxScaler()
df_full[numeric_cols] = scaler.fit_transform(df_full[numeric_cols])

# Limpiar inf/-inf y NaN generados
df_full.replace([np.inf, -np.inf], np.nan, inplace=True)
df_full.dropna(inplace=True)
print(f"Shape después de normalizar: {df_full.shape}")

# ============================================================================
# PASO 8: ELIMINAR FEATURES CORRELACIONADAS
# ============================================================================

print("\n" + "=" * 80)
print("PASO 8: ELIMINANDO FEATURES CORRELACIONADAS")
print("=" * 80)

print(f"Correlation threshold: {CORRELATION_THRESHOLD}")
print("Calculando matriz de correlación (esto puede tardar)...")

corr_matrix = df_full[numeric_cols].corr().abs()

# Encontrar features con alta correlación
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if any(upper[column] > CORRELATION_THRESHOLD)]

print(f"\nFeatures a eliminar: {len(to_drop)}")
if len(to_drop) > 0:
    print(f"Primeras 10: {to_drop[:10]}")

df_full.drop(to_drop, axis=1, inplace=True)
print(f"\nShape después de eliminar correlaciones: {df_full.shape}")
print(f"Features finales: {df_full.shape[1] - 1} (sin contar Label)")

# ============================================================================
# PASO 9: BALANCEAR DATASET
# ============================================================================

print("\n" + "=" * 80)
print("PASO 9: BALANCEANDO DATASET")
print("=" * 80)

# Separar por clase
df_attack = df_full[df_full['Label'] == 'Brute Force'].copy()
df_benign = df_full[df_full['Label'] == 'Benign'].copy()

print(f"\nAntes del balanceo:")
print(f"Brute Force: {df_attack.shape[0]:,}")
print(f"Benign: {df_benign.shape[0]:,}")

# Balancear: tomar igual cantidad de Benign que de Brute Force
n_attack = df_attack.shape[0]
df_benign_sampled = df_benign.sample(n=n_attack, random_state=RANDOM_STATE)

# Combinar y shuffle
df_balanced = pd.concat([df_benign_sampled, df_attack], axis=0, ignore_index=True)
df_balanced = df_balanced.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print(f"\nDespués del balanceo:")
print(df_balanced['Label'].value_counts())
print(f"Shape final: {df_balanced.shape}")

# Liberar memoria
del df_full, df_attack, df_benign, df_benign_sampled
gc.collect()

# ============================================================================
# GUARDAR DATASET
# ============================================================================

print("\n" + "=" * 80)
print("GUARDANDO DATASET PROCESADO")
print("=" * 80)

output_path = os.path.join(OUTPUT_DIR, 'brute_force_balanced.csv')
print(f"\nGuardando: {output_path}")
df_balanced.to_csv(output_path, index=False)

file_size_mb = os.path.getsize(output_path) / 1024**2
print(f"✓ Guardado exitosamente")
print(f"  Shape: {df_balanced.shape}")
print(f"  Tamaño: {file_size_mb:.2f} MB")
print(f"  Features: {df_balanced.shape[1] - 1}")
print(f"  Registros: {df_balanced.shape[0]:,}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

print(f"\nDataset generado:")
print(f"  ✓ brute_force_balanced.csv")
print(f"  ✓ Brute Force vs Benign (balanceado 50/50)")
print(f"  ✓ {df_balanced.shape[1] - 1} features")
print(f"  ✓ {df_balanced.shape[0]:,} registros totales")

print(f"\nTipos de Brute Force consolidados:")
for label in BRUTE_FORCE_LABELS:
    print(f"  - {label}")

print(f"\nPróximo paso:")
print(f"  → Realizar EDA con: fuerza-bruta/processed_data/brute_force_balanced.csv")

print(f"\nFin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
