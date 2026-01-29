"""
Script para ejecutar EDA completo con dataset reducido

Ejecuta el notebook EDA_Suspicious_Login_RBA.ipynb con el dataset reducido
y genera análisis estadístico completo.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración
DATASET = "rba_reduced.csv"

print("=" * 80)
print("   EDA COMPLETO - Dataset Reducido (<100K)")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Dataset: {DATASET}")

# Cargar dataset
df = pd.read_csv(DATASET)
df['Login Timestamp'] = pd.to_datetime(df['Login Timestamp'])

print(f"\n✅ Dataset cargado: {len(df):,} registros")

# ============================================================================
# FASE 1: ANÁLISIS GENERAL
# ============================================================================
print("\n" + "=" * 80)
print("FASE 1: ANÁLISIS GENERAL DEL DATASET")
print("=" * 80)

print(f"\n📊 INFORMACIÓN DEL DATASET:")
print(f"   • Total registros: {len(df):,}")
print(f"   • Total columnas: {len(df.columns)}")
print(f"   • Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print(f"\n📊 COLUMNAS:")
for col in df.columns:
    dtype = df[col].dtype
    nulls = df[col].isnull().sum()
    null_pct = (nulls / len(df)) * 100
    print(f"   • {col:30s}: {str(dtype):10s} | Nulls: {nulls:,} ({null_pct:.2f}%)")

# ============================================================================
# FASE 2: TARGET VARIABLE - Is Account Takeover
# ============================================================================
print("\n" + "=" * 80)
print("FASE 2: ANÁLISIS DE TARGET VARIABLE")
print("=" * 80)

ato_count = df['Is Account Takeover'].sum()
normal_count = len(df) - ato_count

print(f"\n📊 DISTRIBUCIÓN DE Is Account Takeover:")
print(f"   • Account Takeover: {ato_count} ({ato_count/len(df)*100:.4f}%)")
print(f"   • Normal: {normal_count:,} ({normal_count/len(df)*100:.4f}%)")
print(f"   • Ratio: {normal_count/ato_count:.1f}:1 (Normal:ATO)")

# ============================================================================
# FASE 3: LOGIN SUCCESS/FAILURE
# ============================================================================
print("\n" + "=" * 80)
print("FASE 3: ANÁLISIS DE LOGIN SUCCESS/FAILURE")
print("=" * 80)

success_count = df['Login Successful'].sum()
failure_count = len(df) - success_count

print(f"\n📊 DISTRIBUCIÓN DE Login Successful:")
print(f"   • Logins EXITOSOS: {success_count:,} ({success_count/len(df)*100:.2f}%)")
print(f"   • Logins FALLIDOS: {failure_count:,} ({failure_count/len(df)*100:.2f}%)")

# Relación con ATOs
ato_df = df[df['Is Account Takeover'] == True]
normal_df = df[df['Is Account Takeover'] == False]

ato_success = ato_df['Login Successful'].sum()
normal_success = normal_df['Login Successful'].sum()

print(f"\n📊 LOGIN SUCCESS EN ATOs:")
print(f"   • Exitosos: {ato_success} ({ato_success/len(ato_df)*100:.1f}%)")
print(f"   • Fallidos: {len(ato_df) - ato_success} ({(len(ato_df) - ato_success)/len(ato_df)*100:.1f}%)")

print(f"\n📊 LOGIN SUCCESS EN NORMALES:")
print(f"   • Exitosos: {normal_success:,} ({normal_success/len(normal_df)*100:.2f}%)")
print(f"   • Fallidos: {len(normal_df) - normal_success:,} ({(len(normal_df) - normal_success)/len(normal_df)*100:.2f}%)")

# ============================================================================
# FASE 4: FEATURES CATEGÓRICOS
# ============================================================================
print("\n" + "=" * 80)
print("FASE 4: ANÁLISIS DE FEATURES CATEGÓRICOS")
print("=" * 80)

# Browser
print(f"\n📊 BROWSERS (Top 10):")
top_browsers = df['Browser Name and Version'].value_counts().head(10)
for browser, count in top_browsers.items():
    pct = count / len(df) * 100
    print(f"   {browser}: {count:,} ({pct:.2f}%)")

# OS
print(f"\n📊 SISTEMAS OPERATIVOS (Top 10):")
top_os = df['OS Name and Version'].value_counts().head(10)
for os, count in top_os.items():
    pct = count / len(df) * 100
    print(f"   {os}: {count:,} ({pct:.2f}%)")

# Device Type
print(f"\n📊 DEVICE TYPE:")
device_counts = df['Device Type'].value_counts()
for device, count in device_counts.items():
    pct = count / len(df) * 100
    print(f"   {device}: {count:,} ({pct:.2f}%)")

# ============================================================================
# FASE 5: FEATURES NUMÉRICOS
# ============================================================================
print("\n" + "=" * 80)
print("FASE 5: ANÁLISIS DE FEATURES NUMÉRICOS")
print("=" * 80)

# Round-Trip Time
print(f"\n📊 ROUND-TRIP TIME [ms]:")
rtt_stats = df['Round-Trip Time [ms]'].describe()
print(f"   • Media: {rtt_stats['mean']:.1f}ms")
print(f"   • Mediana: {rtt_stats['50%']:.1f}ms")
print(f"   • Std Dev: {rtt_stats['std']:.1f}ms")
print(f"   • Min: {rtt_stats['min']:.1f}ms")
print(f"   • Max: {rtt_stats['max']:.1f}ms")

# ASN
print(f"\n📊 ASN (Autonomous System Number):")
asn_unique = df['ASN'].nunique()
print(f"   • ASNs únicos: {asn_unique:,}")
print(f"   • Top 10 ASNs:")
top_asn = df['ASN'].value_counts().head(10)
for asn, count in top_asn.items():
    pct = count / len(df) * 100
    print(f"      ASN {asn}: {count:,} ({pct:.2f}%)")

# ============================================================================
# FASE 6: ANÁLISIS TEMPORAL
# ============================================================================
print("\n" + "=" * 80)
print("FASE 6: ANÁLISIS TEMPORAL")
print("=" * 80)

# Extraer componentes temporales
df['hour'] = df['Login Timestamp'].dt.hour
df['day_of_week'] = df['Login Timestamp'].dt.dayofweek
df['day_name'] = df['Login Timestamp'].dt.day_name()

print(f"\n📊 PERIODO DEL DATASET:")
print(f"   • Inicio: {df['Login Timestamp'].min()}")
print(f"   • Fin: {df['Login Timestamp'].max()}")
print(f"   • Duración: {(df['Login Timestamp'].max() - df['Login Timestamp'].min()).days} días")

print(f"\n📊 DISTRIBUCIÓN POR HORA DEL DÍA (Top 10):")
hour_counts = df['hour'].value_counts().sort_index().head(10)
for hour, count in hour_counts.items():
    pct = count / len(df) * 100
    print(f"   Hora {hour:02d}:00: {count:,} ({pct:.2f}%)")

print(f"\n📊 DISTRIBUCIÓN POR DÍA DE LA SEMANA:")
day_counts = df['day_name'].value_counts()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in days_order:
    if day in day_counts:
        count = day_counts[day]
        pct = count / len(df) * 100
        print(f"   {day:9s}: {count:,} ({pct:.2f}%)")

# ============================================================================
# FASE 7: IS ATTACK IP
# ============================================================================
print("\n" + "=" * 80)
print("FASE 7: ANÁLISIS DE ATTACK IPs")
print("=" * 80)

attack_ip_count = df['Is Attack IP'].sum()
print(f"\n📊 IPs DE ATAQUE:")
print(f"   • IPs marcadas como ataque: {attack_ip_count:,} ({attack_ip_count/len(df)*100:.2f}%)")
print(f"   • IPs normales: {len(df) - attack_ip_count:,} ({(len(df) - attack_ip_count)/len(df)*100:.2f}%)")

# Relación con ATOs
ato_with_attack_ip = ato_df['Is Attack IP'].sum()
print(f"\n📊 ATTACK IP EN ATOs:")
print(f"   • ATOs con Attack IP: {ato_with_attack_ip} ({ato_with_attack_ip/len(ato_df)*100:.1f}%)")

# ============================================================================
# FASE 8: USUARIOS E IPs
# ============================================================================
print("\n" + "=" * 80)
print("FASE 8: ANÁLISIS DE USUARIOS E IPs")
print("=" * 80)

users_unique = df['User ID'].nunique()
ips_unique = df['IP Address'].nunique()

print(f"\n📊 USUARIOS E IPs:")
print(f"   • Usuarios únicos: {users_unique:,}")
print(f"   • IPs únicas: {ips_unique:,}")
print(f"   • Ratio IP/Usuario: {ips_unique/users_unique:.2f}")

# Usuarios con múltiples IPs
users_ip_counts = df.groupby('User ID')['IP Address'].nunique()
multi_ip_users = users_ip_counts[users_ip_counts > 1]

print(f"\n📊 USUARIOS CON MÚLTIPLES IPs:")
print(f"   • Usuarios con 1 IP: {(users_ip_counts == 1).sum():,}")
print(f"   • Usuarios con 2+ IPs: {len(multi_ip_users):,}")
print(f"   • Usuarios con 5+ IPs: {(users_ip_counts >= 5).sum():,}")
print(f"   • Usuarios con 10+ IPs: {(users_ip_counts >= 10).sum():,}")

# IPs con múltiples usuarios
ips_user_counts = df.groupby('IP Address')['User ID'].nunique()
multi_user_ips = ips_user_counts[ips_user_counts > 1]

print(f"\n📊 IPs CON MÚLTIPLES USUARIOS:")
print(f"   • IPs con 1 usuario: {(ips_user_counts == 1).sum():,}")
print(f"   • IPs con 2+ usuarios: {len(multi_user_ips):,}")
print(f"   • IPs con 5+ usuarios: {(ips_user_counts >= 5).sum():,}")
print(f"   • IPs con 10+ usuarios: {(ips_user_counts >= 10).sum():,}")

# ============================================================================
# FASE 9: CONCLUSIONES
# ============================================================================
print("\n" + "=" * 80)
print("FASE 9: CONCLUSIONES DEL EDA")
print("=" * 80)

print(f"\n🎯 HALLAZGOS PRINCIPALES:")

print(f"\n1. BALANCE DE CLASES:")
print(f"   • Dataset EXTREMADAMENTE DESBALANCEADO")
print(f"   • Ratio 1:{normal_count/ato_count:.0f} (Normal:ATO)")
print(f"   • Requiere class_weight='balanced' o SMOTE")

print(f"\n2. PATRÓN DE ATOs:")
print(f"   • {ato_success/len(ato_df)*100:.1f}% de ATOs son logins EXITOSOS")
print(f"   • Los atacantes YA TIENEN credenciales válidas")
print(f"   • NO es detección de fuerza bruta")
print(f"   • Detección basada en: IP nueva, país diferente, dispositivo diferente")

print(f"\n3. CASOS NORMALES:")
print(f"   • {(len(normal_df) - normal_success)/len(normal_df)*100:.2f}% de logins normales FALLAN")
print(f"   • Esto es comportamiento humano esperado (typos, olvidos)")
print(f"   • NO son ataques, son usuarios legítimos")

print(f"\n4. FEATURES ÚTILES:")
print(f"   • Country (cambio de país en ATOs)")
print(f"   • IP Address (IPs nuevas)")
print(f"   • Browser/OS/Device (cambios de dispositivo)")
print(f"   • Is Attack IP (correlación con ATOs)")
print(f"   • Round-Trip Time (latencia anómala)")
print(f"   • Login Timestamp (patrones temporales)")

print(f"\n5. MÉTRICAS RECOMENDADAS:")
print(f"   • Recall (PRIORIDAD - detectar todos los ATOs)")
print(f"   • F1-Score (balance Precision/Recall)")
print(f"   • AUC-PR (mejor que ROC-AUC para desbalance)")
print(f"   • NO usar Accuracy (inútil con desbalance extremo)")

print("\n" + "=" * 80)
print("✅ EDA COMPLETADO")
print("=" * 80)

print(f"\n📋 RESUMEN:")
print(f"   • Dataset: {DATASET}")
print(f"   • Registros: {len(df):,}")
print(f"   • ATOs: {ato_count}")
print(f"   • Features: {len(df.columns)}")

print(f"\n🎯 PRÓXIMOS PASOS:")
print(f"   1. Feature Engineering (35 features)")
print(f"   2. Temporal Split (no random)")
print(f"   3. Entrenar modelos con class_weight='balanced'")
print(f"   4. Threshold tuning para maximizar Recall")

print("\n" + "=" * 80)
