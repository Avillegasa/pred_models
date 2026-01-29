"""
Script para crear dataset REDUCIDO (<100K registros) del RBA

Toma:
- TODOS los 141 casos de Account Takeover
- ~85,000 casos normales (para total ~85K, <100K)
- Resultado: Dataset reducido con ratio 1:600 (Normal:ATO)

Ventajas:
- Más rápido de entrenar (<100K registros)
- Mantiene todos los ATOs del dataset original
- Balance suficiente para ML con class_weight='balanced'
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuración
DATASET_V2 = "rba_balanced_v2.csv"
OUTPUT_CSV = "rba_reduced.csv"
NORMAL_SAMPLES = 85_000  # Para tener <100K total
RANDOM_STATE = 42

print("=" * 80)
print("   CREACIÓN DE DATASET REDUCIDO - RBA (<100K registros)")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Dataset V2: {DATASET_V2}")
print(f"💾 Output: {OUTPUT_CSV}")
print(f"🎯 Target: <100K registros totales")

# PASO 1: Cargar dataset V2
print("\n" + "=" * 80)
print("PASO 1: CARGANDO DATASET V2")
print("=" * 80)

df = pd.read_csv(DATASET_V2)
print(f"✅ Dataset V2 cargado: {len(df):,} registros")

# Separar ATOs y normales
df_ato = df[df['Is Account Takeover'] == True]
df_normal = df[df['Is Account Takeover'] == False]

print(f"\n📊 Distribución V2:")
print(f"   • Account Takeover: {len(df_ato)}")
print(f"   • Normal: {len(df_normal):,}")

# PASO 2: Muestrear casos normales
print("\n" + "=" * 80)
print("PASO 2: MUESTREANDO CASOS NORMALES")
print("=" * 80)

print(f"⏳ Tomando {NORMAL_SAMPLES:,} casos normales aleatorios...")

np.random.seed(RANDOM_STATE)
df_normal_reduced = df_normal.sample(n=NORMAL_SAMPLES, random_state=RANDOM_STATE)

print(f"✅ Muestreados: {len(df_normal_reduced):,} casos normales")

# PASO 3: Combinar ATO + Normal reducido
print("\n" + "=" * 80)
print("PASO 3: CREANDO DATASET REDUCIDO")
print("=" * 80)

print("⏳ Combinando ATOs + Normal reducido...")
df_reduced = pd.concat([df_ato, df_normal_reduced], ignore_index=True)

print("⏳ Mezclando aleatoriamente...")
df_reduced = df_reduced.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print(f"✅ Dataset reducido creado: {len(df_reduced):,} registros")

# PASO 4: Validación
print("\n" + "=" * 80)
print("PASO 4: VALIDACIÓN DEL DATASET REDUCIDO")
print("=" * 80)

ato_count = df_reduced['Is Account Takeover'].sum()
normal_count = len(df_reduced) - ato_count
actual_ratio = normal_count / ato_count if ato_count > 0 else 0

print(f"\n📊 DISTRIBUCIÓN FINAL:")
print(f"   • Total: {len(df_reduced):,} registros")
print(f"   • Account Takeover: {ato_count} ({ato_count/len(df_reduced)*100:.4f}%)")
print(f"   • Normal: {normal_count:,} ({normal_count/len(df_reduced)*100:.4f}%)")
print(f"   • Ratio: {actual_ratio:.1f}:1 (Normal:ATO)")

if len(df_reduced) < 100_000:
    print(f"\n✅ Dataset es <100K registros: {len(df_reduced):,}")
else:
    print(f"\n⚠️ Dataset excede 100K: {len(df_reduced):,}")

# Estadísticas adicionales
print(f"\n📊 ESTADÍSTICAS:")
print(f"   • Usuarios únicos: {df_reduced['User ID'].nunique():,}")
print(f"   • IPs únicas: {df_reduced['IP Address'].nunique():,}")
print(f"   • Países únicos: {df_reduced['Country'].nunique()}")
print(f"   • Regiones únicas: {df_reduced['Region'].nunique()}")
print(f"   • Ciudades únicas: {df_reduced['City'].nunique()}")
print(f"   • Login exitosos: {df_reduced['Login Successful'].sum():,} ({df_reduced['Login Successful'].sum()/len(df_reduced)*100:.1f}%)")

# Distribución geográfica
print(f"\n📊 DISTRIBUCIÓN GEOGRÁFICA (Top 10 países):")
top_countries = df_reduced['Country'].value_counts().head(10)
for country, count in top_countries.items():
    pct = count / len(df_reduced) * 100
    print(f"   {country}: {count:,} ({pct:.2f}%)")

# ATOs por país
print(f"\n📊 ACCOUNT TAKEOVER POR PAÍS:")
ato_by_country = df_reduced[df_reduced['Is Account Takeover'] == True]['Country'].value_counts()
for country, count in ato_by_country.items():
    pct = count / ato_count * 100
    print(f"   {country}: {count} casos ({pct:.1f}%)")

# PASO 5: Guardar CSV
print("\n" + "=" * 80)
print("PASO 5: GUARDANDO DATASET REDUCIDO")
print("=" * 80)

print(f"⏳ Guardando en {OUTPUT_CSV}...")
df_reduced.to_csv(OUTPUT_CSV, index=False)

import os
file_size_mb = os.path.getsize(OUTPUT_CSV) / (1024 * 1024)

print(f"✅ Archivo guardado exitosamente")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")

# RESUMEN FINAL
print("\n" + "=" * 80)
print("✅ DATASET REDUCIDO CREADO EXITOSAMENTE")
print("=" * 80)

print(f"\n📁 Archivo: {OUTPUT_CSV}")
print(f"📊 Registros: {len(df_reduced):,} (<100K ✓)")
print(f"💾 Tamaño: {file_size_mb:.2f} MB")
print(f"🎯 Ratio: {actual_ratio:.0f}:1 (Normal:ATO)")
print(f"⚖️ Balance: {ato_count} ATO ({ato_count/len(df_reduced)*100:.4f}%)")

print(f"\n💡 VENTAJAS DEL DATASET REDUCIDO:")
print(f"   • <100K registros (más rápido de entrenar)")
print(f"   • Mismos {ato_count} casos de ATO")
print(f"   • Ratio 1:{actual_ratio:.0f} entrenable con class_weight='balanced'")
print(f"   • {len(df_reduced):,} registros suficientes para ML robusto")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"   1. Análisis geográfico del dataset reducido")
print(f"   2. Ejecutar EDA con {OUTPUT_CSV}")
print(f"   3. Modelado con dataset optimizado")

print("\n" + "=" * 80)
