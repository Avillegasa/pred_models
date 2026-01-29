"""
Script para crear dataset BALANCEADO del RBA con los 141 casos de ATO

Este script toma:
- TODOS los 141 casos de Account Takeover (ya extraídos)
- ~141,000 casos normales muestreados del dataset original
- Resultado: Dataset balanceado con ratio 1:1000 (Normal:ATO)

Total: ~141,141 registros balanceados para entrenar
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuración
ATO_CASES_CSV = "../analysis/all_ato_cases.csv"
DATASET_ORIGINAL = "../dataset/rba-dataset.csv"
OUTPUT_CSV = "rba_balanced.csv"
BALANCE_RATIO = 1000  # 1000 normales por cada ATO
CHUNK_SIZE = 1_000_000
RANDOM_STATE = 42

print("=" * 80)
print("   CREACIÓN DE DATASET BALANCEADO - RBA")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Casos ATO: {ATO_CASES_CSV}")
print(f"📁 Dataset original: {DATASET_ORIGINAL}")
print(f"💾 Output: {OUTPUT_CSV}")
print(f"🎯 Ratio objetivo: {BALANCE_RATIO}:1 (Normal:ATO)")

# PASO 1: Cargar los 141 casos de ATO
print("\n" + "=" * 80)
print("PASO 1: CARGANDO CASOS DE ACCOUNT TAKEOVER")
print("=" * 80)

try:
    df_ato = pd.read_csv(ATO_CASES_CSV)
    print(f"✅ Casos ATO cargados: {len(df_ato)}")

    # Verificar que todos son ATO
    if not (df_ato['Is Account Takeover'] == True).all():
        print("⚠️ ADVERTENCIA: Algunos registros no son ATO")
        df_ato = df_ato[df_ato['Is Account Takeover'] == True]
        print(f"   Filtrados: {len(df_ato)} casos ATO válidos")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró {ATO_CASES_CSV}")
    print("   Ejecuta primero: python3 ../analysis/EDA_Complete_Chunks.py")
    exit(1)

# PASO 2: Calcular cuántos casos normales necesitamos
normal_needed = len(df_ato) * BALANCE_RATIO
print(f"\n📊 OBJETIVO DE BALANCE:")
print(f"   • Casos ATO: {len(df_ato)}")
print(f"   • Casos Normal necesarios: {normal_needed:,}")
print(f"   • Total dataset balanceado: {len(df_ato) + normal_needed:,} registros")

# PASO 3: Muestrear casos normales del dataset original
print("\n" + "=" * 80)
print("PASO 3: MUESTREANDO CASOS NORMALES")
print("=" * 80)
print("⏳ Procesando dataset original por chunks...")

np.random.seed(RANDOM_STATE)

# Calcular probabilidad de muestreo por chunk
# Dataset tiene ~31M registros, ~31M normales
# Necesitamos ~141K normales, así que ~0.45% de cada chunk
sample_prob = normal_needed / 31_000_000 * 1.2  # 1.2 = buffer 20%

print(f"   Probabilidad de muestreo: {sample_prob*100:.4f}%")

normal_samples = []
total_sampled = 0
chunk_num = 0

try:
    for chunk in pd.read_csv(DATASET_ORIGINAL, chunksize=CHUNK_SIZE):
        chunk_num += 1

        # Filtrar solo casos normales
        normal_in_chunk = chunk[chunk['Is Account Takeover'] == False]

        if len(normal_in_chunk) > 0:
            # Muestrear aleatoriamente según probabilidad
            sample_size = int(len(normal_in_chunk) * sample_prob)
            sample_size = min(sample_size, len(normal_in_chunk))

            if sample_size > 0:
                sample = normal_in_chunk.sample(n=sample_size, random_state=RANDOM_STATE + chunk_num)
                normal_samples.append(sample)
                total_sampled += len(sample)

        # Mostrar progreso cada 5 chunks
        if chunk_num % 5 == 0:
            print(f"   Chunk {chunk_num:2d}: {total_sampled:,} normales muestreados")

        # Si ya tenemos suficientes, parar
        if total_sampled >= normal_needed:
            print(f"\n✅ Objetivo alcanzado: {total_sampled:,} casos normales")
            break

    print(f"✅ Chunks procesados: {chunk_num}")

except Exception as e:
    print(f"❌ ERROR al procesar chunks: {e}")
    exit(1)

# PASO 4: Combinar muestras normales
print("\n" + "=" * 80)
print("PASO 4: COMBINANDO CASOS NORMALES")
print("=" * 80)

print(f"⏳ Combinando {len(normal_samples)} chunks...")
df_normal_combined = pd.concat(normal_samples, ignore_index=True)
print(f"   Total combinado: {len(df_normal_combined):,} casos normales")

# Ajustar al número exacto necesario
if len(df_normal_combined) > normal_needed:
    print(f"⏳ Ajustando a {normal_needed:,} casos exactos...")
    df_normal = df_normal_combined.sample(n=normal_needed, random_state=RANDOM_STATE)
else:
    df_normal = df_normal_combined
    print(f"⚠️ Solo se obtuvieron {len(df_normal):,} casos (objetivo: {normal_needed:,})")

print(f"✅ Casos normales finales: {len(df_normal):,}")

# PASO 5: Combinar ATO + Normal y mezclar
print("\n" + "=" * 80)
print("PASO 5: CREANDO DATASET BALANCEADO")
print("=" * 80)

print("⏳ Combinando casos ATO + Normal...")
df_balanced = pd.concat([df_ato, df_normal], ignore_index=True)

print("⏳ Mezclando aleatoriamente...")
df_balanced = df_balanced.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print(f"✅ Dataset balanceado creado: {len(df_balanced):,} registros")

# PASO 6: Validación
print("\n" + "=" * 80)
print("PASO 6: VALIDACIÓN DEL DATASET")
print("=" * 80)

ato_count = df_balanced['Is Account Takeover'].sum()
normal_count = len(df_balanced) - ato_count
actual_ratio = normal_count / ato_count if ato_count > 0 else 0

print(f"\n📊 DISTRIBUCIÓN FINAL:")
print(f"   • Total: {len(df_balanced):,} registros")
print(f"   • Account Takeover: {ato_count} ({ato_count/len(df_balanced)*100:.4f}%)")
print(f"   • Normal: {normal_count:,} ({normal_count/len(df_balanced)*100:.4f}%)")
print(f"   • Ratio real: {actual_ratio:.1f}:1")
print(f"   • Ratio objetivo: {BALANCE_RATIO}:1")

if abs(actual_ratio - BALANCE_RATIO) < BALANCE_RATIO * 0.05:
    print("\n✅ Ratio alcanzado exitosamente")
else:
    print(f"\n⚠️ Ratio difiere ligeramente del objetivo (aceptable)")

# Estadísticas adicionales
print(f"\n📊 ESTADÍSTICAS:")
print(f"   • Usuarios únicos: {df_balanced['User ID'].nunique():,}")
print(f"   • IPs únicas: {df_balanced['IP Address'].nunique():,}")
print(f"   • Países únicos: {df_balanced['Country'].nunique()}")
print(f"   • Login exitosos: {df_balanced['Login Successful'].sum():,} ({df_balanced['Login Successful'].sum()/len(df_balanced)*100:.1f}%)")

# PASO 7: Guardar CSV
print("\n" + "=" * 80)
print("PASO 7: GUARDANDO DATASET BALANCEADO")
print("=" * 80)

print(f"⏳ Guardando en {OUTPUT_CSV}...")
df_balanced.to_csv(OUTPUT_CSV, index=False)

import os
file_size_mb = os.path.getsize(OUTPUT_CSV) / (1024 * 1024)

print(f"✅ Archivo guardado exitosamente")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")

# RESUMEN FINAL
print("\n" + "=" * 80)
print("✅ DATASET BALANCEADO CREADO EXITOSAMENTE")
print("=" * 80)

print(f"\n📁 Archivo: {OUTPUT_CSV}")
print(f"📊 Registros: {len(df_balanced):,}")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")
print(f"🎯 Ratio: {actual_ratio:.0f}:1 (Normal:ATO)")
print(f"⚖️ Balance: {ato_count} ATO ({ato_count/len(df_balanced)*100:.4f}%)")

print(f"\n💡 VENTAJAS DE ESTE DATASET:")
print(f"   • TODOS los {ato_count} casos de ATO del dataset original")
print(f"   • Ratio 1:{actual_ratio:.0f} entrenable con SMOTE/class weights")
print(f"   • {len(df_balanced):,} registros suficientes para modelado robusto")
print(f"   • Más balanceado que el original (1:221,767 → 1:{actual_ratio:.0f})")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"   1. Actualizar notebook EDA para usar: ../processed_data/{OUTPUT_CSV}")
print(f"   2. Ejecutar EDA con dataset balanceado")
print(f"   3. Feature engineering y modelado")

print("\n" + "=" * 80)
