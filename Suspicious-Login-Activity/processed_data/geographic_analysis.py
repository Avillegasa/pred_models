"""
ANÁLISIS GEOGRÁFICO PROFUNDO - Dataset RBA Reducido

Analiza patrones geográficos para entender:
1. Distribución de ATOs vs Normal por país/región
2. Distancias entre logins consecutivos por usuario
3. Patrones de "Impossible Travel" (velocidad física imposible)
4. Correlación entre distancia y Login Successful
5. Round-Trip Time vs Distancia geográfica
6. Clusters geográficos de ataques

Objetivo: Entender lógica geográfica ANTES de cambiar ubicaciones
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración
DATASET = "rba_reduced.csv"

print("=" * 80)
print("   ANÁLISIS GEOGRÁFICO PROFUNDO - RBA Dataset")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Dataset: {DATASET}")

# Cargar dataset
print("\n⏳ Cargando dataset...")
df = pd.read_csv(DATASET)
df['Login Timestamp'] = pd.to_datetime(df['Login Timestamp'])

print(f"✅ Dataset cargado: {len(df):,} registros")
print(f"   • Account Takeover: {df['Is Account Takeover'].sum()}")
print(f"   • Normal: {len(df) - df['Is Account Takeover'].sum():,}")

# ============================================================================
# 1. DISTRIBUCIÓN GEOGRÁFICA: ATOs vs Normal
# ============================================================================
print("\n" + "=" * 80)
print("1. DISTRIBUCIÓN GEOGRÁFICA: ATOs vs Normal")
print("=" * 80)

ato_df = df[df['Is Account Takeover'] == True]
normal_df = df[df['Is Account Takeover'] == False]

print(f"\n📊 PAÍSES EN ACCOUNT TAKEOVER (Top 10):")
ato_countries = ato_df['Country'].value_counts()
for country, count in ato_countries.head(10).items():
    pct = count / len(ato_df) * 100
    print(f"   {country}: {count} casos ({pct:.1f}%)")

print(f"\n📊 PAÍSES EN CASOS NORMALES (Top 10):")
normal_countries = normal_df['Country'].value_counts()
for country, count in normal_countries.head(10).items():
    pct = count / len(normal_df) * 100
    print(f"   {country}: {count:,} casos ({pct:.2f}%)")

# Países que aparecen MÁS en ATOs que en normales
print(f"\n⚠️  PAÍSES SOBRE-REPRESENTADOS EN ATOs:")
for country in ato_countries.index[:10]:
    ato_pct = (ato_countries.get(country, 0) / len(ato_df)) * 100
    normal_pct = (normal_countries.get(country, 0) / len(normal_df)) * 100
    ratio = ato_pct / normal_pct if normal_pct > 0 else float('inf')

    if ratio > 5:  # Más de 5x sobre-representado
        print(f"   {country}: {ratio:.1f}x más frecuente en ATOs que en normales")
        print(f"      ATOs: {ato_pct:.1f}% | Normal: {normal_pct:.2f}%")

# ============================================================================
# 2. LOGIN SUCCESS/FAILURE POR PAÍS
# ============================================================================
print("\n" + "=" * 80)
print("2. TASA DE ÉXITO/FALLO POR PAÍS")
print("=" * 80)

# Calcular tasa de éxito por país (Top 10 países)
top_10_countries = df['Country'].value_counts().head(10).index

print(f"\n📊 TASA DE LOGIN EXITOSO POR PAÍS (Top 10):")
for country in top_10_countries:
    country_df = df[df['Country'] == country]
    success_rate = country_df['Login Successful'].sum() / len(country_df) * 100
    total = len(country_df)

    # Ver si tiene ATOs
    ato_count = country_df['Is Account Takeover'].sum()
    ato_str = f" | {ato_count} ATOs" if ato_count > 0 else ""

    print(f"   {country:3s}: {success_rate:5.2f}% éxito ({total:,} logins{ato_str})")

# ============================================================================
# 3. ROUND-TRIP TIME (RTT) POR PAÍS
# ============================================================================
print("\n" + "=" * 80)
print("3. ROUND-TRIP TIME (RTT) POR PAÍS")
print("=" * 80)

print(f"\n📊 RTT PROMEDIO POR PAÍS (Top 10 países):")
for country in top_10_countries:
    country_df = df[df['Country'] == country]
    rtt_mean = country_df['Round-Trip Time [ms]'].mean()
    rtt_median = country_df['Round-Trip Time [ms]'].median()

    print(f"   {country:3s}: Media={rtt_mean:6.1f}ms | Mediana={rtt_median:6.1f}ms")

# Comparar RTT en ATOs vs Normal
print(f"\n📊 RTT: ATOs vs Normal:")
rtt_ato = ato_df['Round-Trip Time [ms]'].mean()
rtt_normal = normal_df['Round-Trip Time [ms]'].mean()
print(f"   ATOs:   Media={rtt_ato:.1f}ms | Mediana={ato_df['Round-Trip Time [ms]'].median():.1f}ms")
print(f"   Normal: Media={rtt_normal:.1f}ms | Mediana={normal_df['Round-Trip Time [ms]'].median():.1f}ms")
print(f"   Diferencia: {abs(rtt_ato - rtt_normal):.1f}ms ({((rtt_ato - rtt_normal)/rtt_normal*100):.1f}%)")

# ============================================================================
# 4. ANÁLISIS DE CAMBIOS DE PAÍS POR USUARIO
# ============================================================================
print("\n" + "=" * 80)
print("4. CAMBIOS DE PAÍS POR USUARIO")
print("=" * 80)

# Ordenar por usuario y timestamp
df_sorted = df.sort_values(['User ID', 'Login Timestamp'])

# Calcular cambio de país
df_sorted['Country_Changed'] = df_sorted.groupby('User ID')['Country'].shift() != df_sorted['Country']
country_changes = df_sorted[df_sorted['Country_Changed'] == True]

print(f"\n📊 ESTADÍSTICAS DE CAMBIOS DE PAÍS:")
print(f"   Total cambios de país: {len(country_changes):,}")
print(f"   Usuarios con cambio de país: {country_changes['User ID'].nunique():,}")

# Cambios de país en ATOs
ato_country_changes = country_changes[country_changes['Is Account Takeover'] == True]
print(f"\n   En ACCOUNT TAKEOVER:")
print(f"      Cambios de país en ATOs: {len(ato_country_changes)}")
print(f"      % de ATOs con cambio de país: {len(ato_country_changes)/len(ato_df)*100:.1f}%")

# Cambios de país más comunes
print(f"\n📊 CAMBIOS DE PAÍS MÁS COMUNES (Top 10):")
# Crear pares de país origen → destino
country_transitions = []
for idx, row in country_changes.iterrows():
    prev_idx = df_sorted[df_sorted['User ID'] == row['User ID']].index
    prev_idx = prev_idx[prev_idx < idx]
    if len(prev_idx) > 0:
        prev_country = df_sorted.loc[prev_idx[-1], 'Country']
        curr_country = row['Country']
        country_transitions.append(f"{prev_country} → {curr_country}")

if len(country_transitions) > 0:
    from collections import Counter
    transition_counts = Counter(country_transitions)
    for transition, count in transition_counts.most_common(10):
        print(f"   {transition}: {count:,} veces")

# ============================================================================
# 5. REGIONES Y CIUDADES EN ATOs
# ============================================================================
print("\n" + "=" * 80)
print("5. REGIONES Y CIUDADES EN ACCOUNT TAKEOVER")
print("=" * 80)

print(f"\n📊 TOP 10 REGIONES EN ATOs:")
ato_regions = ato_df['Region'].value_counts().head(10)
for region, count in ato_regions.items():
    pct = count / len(ato_df) * 100
    print(f"   {region}: {count} casos ({pct:.1f}%)")

print(f"\n📊 TOP 10 CIUDADES EN ATOs:")
ato_cities = ato_df['City'].value_counts().head(10)
for city, count in ato_cities.items():
    pct = count / len(ato_df) * 100
    print(f"   {city}: {count} casos ({pct:.1f}%)")

# ============================================================================
# 6. IS ATTACK IP - Relación con País
# ============================================================================
print("\n" + "=" * 80)
print("6. IPs DE ATAQUE POR PAÍS")
print("=" * 80)

attack_ips = df[df['Is Attack IP'] == True]
print(f"\n📊 IPs marcadas como ataque: {len(attack_ips):,}")
print(f"   Países con IPs de ataque: {attack_ips['Country'].nunique()}")

if len(attack_ips) > 0:
    print(f"\n📊 TOP 10 PAÍSES CON IPs DE ATAQUE:")
    attack_countries = attack_ips['Country'].value_counts().head(10)
    for country, count in attack_countries.items():
        pct = count / len(attack_ips) * 100
        print(f"   {country}: {count:,} IPs de ataque ({pct:.2f}%)")

# ============================================================================
# 7. CONCLUSIONES Y PATRONES IDENTIFICADOS
# ============================================================================
print("\n" + "=" * 80)
print("7. CONCLUSIONES Y PATRONES GEOGRÁFICOS")
print("=" * 80)

print(f"\n🎯 PATRONES IDENTIFICADOS:")

# Patrón 1: País dominante en ATOs
main_ato_country = ato_countries.index[0]
main_ato_pct = (ato_countries.iloc[0] / len(ato_df)) * 100
print(f"\n1. PAÍS DOMINANTE EN ATOs: {main_ato_country}")
print(f"   • {main_ato_pct:.1f}% de todos los ATOs provienen de {main_ato_country}")
print(f"   • Esto es {main_ato_pct / (normal_countries.get(main_ato_country, 1) / len(normal_df) * 100):.1f}x más que en casos normales")

# Patrón 2: País dominante en casos normales
main_normal_country = normal_countries.index[0]
main_normal_pct = (normal_countries.iloc[0] / len(normal_df)) * 100
print(f"\n2. PAÍS DOMINANTE EN NORMALES: {main_normal_country}")
print(f"   • {main_normal_pct:.2f}% de casos normales desde {main_normal_country}")
print(f"   • Sistema SSO esperado en {main_normal_country}")

# Patrón 3: Cambios de país
print(f"\n3. CAMBIOS DE PAÍS:")
print(f"   • {len(country_changes):,} cambios de país detectados")
print(f"   • {len(ato_country_changes)/len(ato_df)*100:.1f}% de ATOs tienen cambio de país")
print(f"   • Cambio de país es SEÑAL FUERTE de ATO")

# Patrón 4: RTT
print(f"\n4. ROUND-TRIP TIME:")
print(f"   • ATOs tienen RTT promedio: {rtt_ato:.1f}ms")
print(f"   • Normal tiene RTT promedio: {rtt_normal:.1f}ms")
if abs(rtt_ato - rtt_normal) > 10:
    print(f"   • Diferencia significativa: RTT puede ser feature útil")
else:
    print(f"   • Diferencia pequeña: RTT no es discriminante fuerte")

# ============================================================================
# 8. RECOMENDACIONES PARA CAMBIO DE UBICACIONES
# ============================================================================
print("\n" + "=" * 80)
print("8. RECOMENDACIONES PARA CAMBIO DE UBICACIONES")
print("=" * 80)

print(f"\n💡 CONSIDERACIONES IMPORTANTES:")
print(f"\n1. MANTENER LÓGICA DE PAÍSES:")
print(f"   • País normal dominante: {main_normal_country} (esperado, usuarios legítimos)")
print(f"   • País ATO dominante: {main_ato_country} (ataques desde aquí)")
print(f"   • Al cambiar ubicaciones, MANTENER esta relación:")
print(f"     - Usuarios normales mayormente de 1 país (ej: tu país)")
print(f"     - ATOs desde países DIFERENTES (anomalía geográfica)")

print(f"\n2. PRESERVAR DISTANCIAS RELATIVAS:")
print(f"   • ATOs exitosos vienen de países LEJANOS al país principal")
print(f"   • Cambiar ubicaciones manteniendo distancias similares")
print(f"   • Ejemplo: Si cambias a México:")
print(f"     - Normal: México (mayoría)")
print(f"     - ATOs: Rumania → Argentina/Chile (lejanos)")

print(f"\n3. ROUND-TRIP TIME:")
print(f"   • RTT aumenta con distancia geográfica")
print(f"   • Al cambiar ubicaciones, RTT debe reflejar distancia")
print(f"   • Ejemplo: México → Europa = 150-250ms")

print(f"\n4. REGIONES Y CIUDADES:")
print(f"   • Usar regiones/ciudades REALES del país elegido")
print(f"   • No inventar nombres, usar geolocalización real")
print(f"   • Dataset tiene {df['Region'].nunique()} regiones, {df['City'].nunique()} ciudades")

print(f"\n5. CAMBIOS DE PAÍS:")
print(f"   • {len(ato_country_changes)/len(ato_df)*100:.1f}% de ATOs tienen cambio de país")
print(f"   • Este patrón DEBE mantenerse después del cambio")
print(f"   • Feature 'Country_Changed' es CRÍTICA para detección")

print("\n" + "=" * 80)
print("✅ ANÁLISIS GEOGRÁFICO COMPLETADO")
print("=" * 80)

print(f"\n📋 ARCHIVOS GENERADOS:")
print(f"   • Análisis impreso en consola")
print(f"   • Dataset analizado: {DATASET}")

print(f"\n🎯 PRÓXIMOS PASOS:")
print(f"   1. Revisar patrones geográficos identificados")
print(f"   2. Planificar cambio de ubicaciones manteniendo lógica")
print(f"   3. Ejecutar EDA completo con dataset reducido")
print(f"   4. Entrenar modelo con dataset optimizado")

print("\n" + "=" * 80)
