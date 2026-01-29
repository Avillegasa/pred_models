"""
Script para crear dataset BALANCEADO V2 del RBA con los 141 casos de ATO
**VERSION 2**: Usa seed aleatorio diferente para obtener OTROS casos normales

Este script toma:
- TODOS los 141 casos de Account Takeover (mismos que V1)
- ~141,000 casos normales DIFERENTES muestreados con otro seed
- Resultado: Dataset balanceado V2 con ratio 1:1000 (Normal:ATO)

Diferencia con V1:
- V1 usa RANDOM_STATE = 42
- V2 usa RANDOM_STATE = 123 → DATOS NORMALES DIFERENTES

Total: ~141,141 registros balanceados para entrenar
"""

import pandas as pd
import numpy as np
from datetime import datetime
import gc

# Configuración
ATO_CASES_CSV = "../analysis/all_ato_cases.csv"
DATASET_ORIGINAL = "../dataset/rba-dataset.csv"
OUTPUT_CSV = "rba_balanced_v2.csv"  # Nuevo archivo V2
BALANCE_RATIO = 1000  # 1000 normales por cada ATO
CHUNK_SIZE = 2_000_000  # 2M por chunk (más rápido que 1M)
RANDOM_STATE = 123  # <<<< SEED DIFERENTE A V1 (V1=42, V2=123)

print("=" * 80)
print("   CREACIÓN DE DATASET BALANCEADO V2 - RBA")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Casos ATO: {ATO_CASES_CSV}")
print(f"📁 Dataset original: {DATASET_ORIGINAL}")
print(f"💾 Output: {OUTPUT_CSV}")
print(f"🎯 Ratio objetivo: {BALANCE_RATIO}:1 (Normal:ATO)")
print(f"🎲 RANDOM_STATE: {RANDOM_STATE} (DIFERENTE a V1=42)")

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
    print("   Ejecuta primero el script de extracción de ATOs")
    exit(1)

# PASO 2: Calcular cuántos casos normales necesitamos
normal_needed = len(df_ato) * BALANCE_RATIO
print(f"\n📊 OBJETIVO DE BALANCE:")
print(f"   • Casos ATO: {len(df_ato)}")
print(f"   • Casos Normal necesarios: {normal_needed:,}")
print(f"   • Total dataset balanceado: {len(df_ato) + normal_needed:,} registros")

# PASO 3: Muestrear casos normales del dataset original (CON SEED DIFERENTE)
print("\n" + "=" * 80)
print("PASO 3: MUESTREANDO CASOS NORMALES (SEED DIFERENTE)")
print("=" * 80)
print("⏳ Procesando dataset original por chunks...")
print("⚠️  NOTA: Esto tomará ~10-20 minutos leyendo del dataset de 8.5 GB\n")

np.random.seed(RANDOM_STATE)  # Seed diferente = datos diferentes

# Calcular probabilidad de muestreo por chunk
# Dataset tiene ~31M registros normales
# Necesitamos ~141K normales → ~0.5% de cada chunk (con buffer)
sample_prob = normal_needed / 31_000_000 * 1.3  # 1.3 = buffer 30%

print(f"   Probabilidad de muestreo: {sample_prob*100:.4f}%")
print(f"   Chunks de {CHUNK_SIZE:,} registros cada uno\n")

normal_samples = []
total_sampled = 0
chunk_num = 0
start_time = datetime.now()

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
                # SEED DIFERENTE POR CHUNK para mayor variabilidad
                sample = normal_in_chunk.sample(
                    n=sample_size,
                    random_state=RANDOM_STATE + chunk_num
                )
                normal_samples.append(sample)
                total_sampled += len(sample)

        # Mostrar progreso cada 3 chunks
        if chunk_num % 3 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = chunk_num / elapsed * 60  # chunks/min
            print(f"   Chunk {chunk_num:2d}: {total_sampled:,} normales | "
                  f"Velocidad: {rate:.1f} chunks/min")

        # Si ya tenemos suficientes, parar
        if total_sampled >= normal_needed:
            print(f"\n✅ Objetivo alcanzado: {total_sampled:,} casos normales")
            break

        # Liberar memoria
        del chunk, normal_in_chunk
        gc.collect()

    elapsed_total = (datetime.now() - start_time).total_seconds()
    print(f"✅ Chunks procesados: {chunk_num} en {elapsed_total/60:.1f} minutos")

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

# Liberar memoria
del normal_samples, df_normal_combined
gc.collect()

# PASO 5: Combinar ATO + Normal y mezclar
print("\n" + "=" * 80)
print("PASO 5: CREANDO DATASET BALANCEADO V2")
print("=" * 80)

print("⏳ Combinando casos ATO + Normal...")
df_balanced = pd.concat([df_ato, df_normal], ignore_index=True)

print("⏳ Mezclando aleatoriamente...")
df_balanced = df_balanced.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print(f"✅ Dataset balanceado V2 creado: {len(df_balanced):,} registros")

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
print(f"\n📊 ESTADÍSTICAS DEL DATASET V2:")
print(f"   • Usuarios únicos: {df_balanced['User ID'].nunique():,}")
print(f"   • IPs únicas: {df_balanced['IP Address'].nunique():,}")
print(f"   • Países únicos: {df_balanced['Country'].nunique()}")
print(f"   • Login exitosos: {df_balanced['Login Successful'].sum():,} ({df_balanced['Login Successful'].sum()/len(df_balanced)*100:.1f}%)")

# Comparar con V1 si existe
try:
    df_v1 = pd.read_csv("rba_balanced.csv")

    # Contar cuántos registros normales son iguales entre V1 y V2
    df_normal_v1 = df_v1[df_v1['Is Account Takeover'] == False]
    df_normal_v2 = df_normal[df_normal['Is Account Takeover'] == False]

    # Comparar por User ID + Login Timestamp (identificadores únicos)
    # Convertir ambas columnas a string primero para evitar errores de tipo
    v1_ids = set(df_normal_v1['User ID'].astype(str) + "_" + df_normal_v1['Login Timestamp'].astype(str))
    v2_ids = set(df_normal_v2['User ID'].astype(str) + "_" + df_normal_v2['Login Timestamp'].astype(str))

    overlap = len(v1_ids.intersection(v2_ids))
    overlap_pct = overlap / len(v2_ids) * 100 if len(v2_ids) > 0 else 0

    print(f"\n📊 COMPARACIÓN CON V1:")
    print(f"   • Registros normales solapados: {overlap:,} ({overlap_pct:.2f}%)")
    print(f"   • Registros normales únicos de V2: {len(v2_ids) - overlap:,}")
    print(f"   • ✅ Dataset V2 contiene {100-overlap_pct:.1f}% de datos DIFERENTES a V1")

except FileNotFoundError:
    print(f"\n⚠️ No se encontró rba_balanced.csv (V1) para comparar")
except Exception as e:
    print(f"\n⚠️ Error al comparar con V1: {e}")

# PASO 7: Guardar CSV
print("\n" + "=" * 80)
print("PASO 7: GUARDANDO DATASET BALANCEADO V2")
print("=" * 80)

print(f"⏳ Guardando en {OUTPUT_CSV}...")
df_balanced.to_csv(OUTPUT_CSV, index=False)

import os
file_size_mb = os.path.getsize(OUTPUT_CSV) / (1024 * 1024)

print(f"✅ Archivo guardado exitosamente")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")

# RESUMEN FINAL
print("\n" + "=" * 80)
print("✅ DATASET BALANCEADO V2 CREADO EXITOSAMENTE")
print("=" * 80)

print(f"\n📁 Archivo: {OUTPUT_CSV}")
print(f"📊 Registros: {len(df_balanced):,}")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")
print(f"🎯 Ratio: {actual_ratio:.0f}:1 (Normal:ATO)")
print(f"⚖️ Balance: {ato_count} ATO ({ato_count/len(df_balanced)*100:.4f}%)")

print(f"\n💡 VENTAJAS DE DATASET V2:")
print(f"   • Mismos {ato_count} casos de ATO que V1")
print(f"   • DATOS NORMALES DIFERENTES (seed {RANDOM_STATE} vs 42 en V1)")
print(f"   • Permite validación cruzada con V1")
print(f"   • Mismo ratio entrenable 1:{actual_ratio:.0f}")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"   1. Actualizar notebook EDA: DATASET_PATH = '../processed_data/{OUTPUT_CSV}'")
print(f"   2. Ejecutar EDA con dataset balanceado V2")
print(f"   3. Comparar resultados con V1")
print(f"   4. Feature engineering y modelado con V2")

print("\n" + "=" * 80)
