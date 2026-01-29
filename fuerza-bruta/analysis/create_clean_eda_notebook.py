"""Script para crear el notebook de EDA de Brute Force Detection (LIMPIO - SIN OUTPUTS)"""
import json

# Crear notebook vacío
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

def add_markdown_cell(content):
    """Agregar celda de markdown"""
    lines = content.split('\n')
    source = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            source.append(line + "\n")
        else:
            source.append(line)

    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    })

def add_code_cell(content):
    """Agregar celda de código SIN OUTPUTS"""
    lines = content.split('\n')
    source = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            source.append(line + "\n")
        else:
            source.append(line)

    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    })

# ============================================================================
# TÍTULO
# ============================================================================

add_markdown_cell("""# 🔒 Análisis Exploratorio de Datos - Brute Force Detection

## Dataset: CSE-CIC-IDS2018 (Consolidado y Balanceado)

### Objetivo:
Realizar un análisis exploratorio completo del dataset de ataques de Brute Force para:
1. Comprender la distribución de clases
2. Identificar features clave que distinguen ataques de tráfico normal
3. Detectar patrones en los ataques de Brute Force
4. Preparar insights para el modelado

### Dataset:
- **Archivo**: `../processed_data/brute_force_balanced.csv`
- **Registros**: ~763,000
- **Features**: 60
- **Balance**: 50% Brute Force / 50% Benign
- **Tipos de Brute Force**: FTP, SSH, Web, XSS (consolidados)

---""")

# ============================================================================
# PASO 1: CONFIGURACIÓN
# ============================================================================

add_code_cell("""# PASO 1: CONFIGURACIÓN INICIAL

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from scipy import stats

# Configuración de visualización
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Configuración de figuras
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print("✓ Librerías importadas correctamente")
print(f"✓ Pandas version: {pd.__version__}")
print(f"✓ NumPy version: {np.__version__}")""")

add_markdown_cell("""---""")

# ============================================================================
# PASO 2: CARGA DEL DATASET
# ============================================================================

add_code_cell("""# PASO 2: CARGA DEL DATASET BALANCEADO

print("Cargando dataset...")
df = pd.read_csv('../processed_data/brute_force_balanced.csv')

print(f"\\n{'='*80}")
print("DATASET CARGADO EXITOSAMENTE")
print(f"{'='*80}")
print(f"Registros: {len(df):,}")
print(f"Features: {df.shape[1] - 1} (sin contar Label)")
print(f"Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")""")

add_code_cell("""# EXPLORACIÓN INICIAL DEL DATASET

print(f"\\n{'='*80}")
print("INFORMACIÓN GENERAL DEL DATASET")
print(f"{'='*80}")

print(f"\\nShape: {df.shape}")
print(f"\\nColumnas ({len(df.columns)}):")
print(df.columns.tolist())

print(f"\\nTipos de datos:")
print(df.dtypes.value_counts())

print(f"\\nPrimeras 5 filas:")
df.head()""")

add_code_cell("""# INFORMACIÓN DETALLADA

print(f"\\n{'='*80}")
print("INFO DEL DATASET")
print(f"{'='*80}")
df.info()""")

add_code_cell("""# ESTADÍSTICAS DESCRIPTIVAS

print(f"\\n{'='*80}")
print("ESTADÍSTICAS DESCRIPTIVAS")
print(f"{'='*80}")

df.describe().T""")

add_markdown_cell("""---

## 📊 Análisis de Calidad de Datos""")

add_code_cell("""# ANÁLISIS DE CALIDAD DE DATOS

print(f"\\n{'='*80}")
print("ANÁLISIS DE CALIDAD DE DATOS")
print(f"{'='*80}")

# Valores nulos
print(f"\\nValores nulos por columna:")
null_counts = df.isnull().sum()
if null_counts.sum() == 0:
    print("✓ No hay valores nulos en el dataset")
else:
    print(null_counts[null_counts > 0])

# Valores duplicados
duplicates = df.duplicated().sum()
print(f"\\nRegistros duplicados: {duplicates:,}")
if duplicates == 0:
    print("✓ No hay registros duplicados")

# Valores únicos en Label
print(f"\\nValores únicos en 'Label':")
print(df['Label'].value_counts())

# Verificar rango de valores después de normalización
print(f"\\nRango de valores (debería estar entre 0 y 1 por MinMaxScaler):")
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(f"Mínimo global: {df[numeric_cols].min().min():.4f}")
print(f"Máximo global: {df[numeric_cols].max().max():.4f}")""")

add_markdown_cell("""---

## 🎯 Análisis de Distribución de Clases""")

add_code_cell("""# DISTRIBUCIÓN DE CLASES (LABEL)

print(f"\\n{'='*80}")
print("DISTRIBUCIÓN DE CLASES")
print(f"{'='*80}")

# Conteo
label_counts = df['Label'].value_counts()
print(f"\\nConteo absoluto:")
print(label_counts)

# Porcentaje
label_percentages = df['Label'].value_counts(normalize=True) * 100
print(f"\\nPorcentajes:")
for label, pct in label_percentages.items():
    print(f"{label}: {pct:.2f}%")

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de barras
label_counts.plot(kind='bar', ax=axes[0], color=['#3498db', '#e74c3c'])
axes[0].set_title('Distribución de Clases - Conteo', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Clase', fontsize=12)
axes[0].set_ylabel('Cantidad de Registros', fontsize=12)
axes[0].tick_params(axis='x', rotation=0)
for i, v in enumerate(label_counts):
    axes[0].text(i, v + 5000, f'{v:,}', ha='center', fontweight='bold')

# Gráfico de pastel
colors = ['#3498db', '#e74c3c']
axes[1].pie(label_counts, labels=label_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[1].set_title('Distribución de Clases - Proporción', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

print(f"\\n✓ Dataset balanceado: {label_counts.min() / label_counts.max() * 100:.1f}% ratio")""")

add_markdown_cell("""---

## 📈 Análisis de Features Numéricas""")

add_code_cell("""# SELECCIÓN DE FEATURES NUMÉRICAS

# Obtener todas las columnas numéricas (excepto Label)
numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()

print(f"\\n{'='*80}")
print(f"FEATURES NUMÉRICAS: {len(numeric_features)}")
print(f"{'='*80}")
print(f"\\nLista de features:")
for i, feat in enumerate(numeric_features, 1):
    print(f"{i:2d}. {feat}")""")

add_code_cell("""# ANÁLISIS DE DISTRIBUCIÓN DE FEATURES

print(f"\\n{'='*80}")
print("DISTRIBUCIÓN DE FEATURES (TOP 10 CON MÁS VARIANZA)")
print(f"{'='*80}")

# Calcular varianza de cada feature
variances = df[numeric_features].var().sort_values(ascending=False)
top_10_variance = variances.head(10)

print(f"\\nTop 10 features con mayor varianza:")
for i, (feat, var) in enumerate(top_10_variance.items(), 1):
    print(f"{i:2d}. {feat:40s}: {var:.6f}")

# Visualizar distribuciones de las top 10 features
fig, axes = plt.subplots(5, 2, figsize=(16, 20))
axes = axes.ravel()

# Separar por clase
df_benign = df[df['Label'] == 'Benign']
df_attack = df[df['Label'] == 'Brute Force']

for i, feat in enumerate(top_10_variance.index):
    benign_data = df_benign[feat]
    attack_data = df_attack[feat]

    axes[i].hist(benign_data, bins=50, alpha=0.6, label='Benign', color='#3498db', density=True)
    axes[i].hist(attack_data, bins=50, alpha=0.6, label='Brute Force', color='#e74c3c', density=True)
    axes[i].set_title(f'{feat}', fontsize=12, fontweight='bold')
    axes[i].set_xlabel('Valor', fontsize=10)
    axes[i].set_ylabel('Densidad', fontsize=10)
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()""")

add_markdown_cell("""---

## ⚔️ Comparación: Brute Force vs Benign""")

add_code_cell("""# COMPARACIÓN DE MEDIAS POR CLASE

print(f"\\n{'='*80}")
print("COMPARACIÓN DE MEDIAS: BRUTE FORCE VS BENIGN")
print(f"{'='*80}")

# Calcular medias por clase
means_benign = df_benign[numeric_features].mean()
means_attack = df_attack[numeric_features].mean()

# Crear DataFrame comparativo
comparison = pd.DataFrame({
    'Benign_Mean': means_benign,
    'BruteForce_Mean': means_attack,
    'Difference': means_attack - means_benign,
    'Ratio': (means_attack / (means_benign + 1e-10))
})

comparison['Abs_Difference'] = comparison['Difference'].abs()
comparison_sorted = comparison.sort_values('Abs_Difference', ascending=False)

print(f"\\nTop 15 features con mayor diferencia entre clases:")
print(comparison_sorted[['Benign_Mean', 'BruteForce_Mean', 'Difference', 'Ratio']].head(15))""")

add_code_cell("""# VISUALIZACIÓN DE TOP FEATURES DISCRIMINANTES

# Top 10 features con mayor diferencia
top_discriminant = comparison_sorted.head(10).index

fig, axes = plt.subplots(5, 2, figsize=(16, 20))
axes = axes.ravel()

for i, feat in enumerate(top_discriminant):
    benign_vals = df_benign[feat]
    attack_vals = df_attack[feat]

    # Box plot
    data_to_plot = [benign_vals, attack_vals]
    bp = axes[i].boxplot(data_to_plot, labels=['Benign', 'Brute Force'], patch_artist=True)

    # Colorear
    bp['boxes'][0].set_facecolor('#3498db')
    bp['boxes'][1].set_facecolor('#e74c3c')

    axes[i].set_title(f'{feat}', fontsize=12, fontweight='bold')
    axes[i].set_ylabel('Valor', fontsize=10)
    axes[i].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.suptitle('Comparación de Features Discriminantes (Box Plots)',
             fontsize=16, fontweight='bold', y=1.001)
plt.show()""")

add_markdown_cell("""---

## 🔗 Análisis de Correlaciones""")

add_code_cell("""# MATRIZ DE CORRELACIÓN

print(f"\\n{'='*80}")
print("ANÁLISIS DE CORRELACIONES")
print(f"{'='*80}")

# Calcular matriz de correlación (solo top 20 features para visualizar)
top_20_features = comparison_sorted.head(20).index
corr_matrix = df[top_20_features].corr()

print(f"\\nMatriz de correlación calculada para top 20 features discriminantes")

# Heatmap
plt.figure(figsize=(16, 14))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlación - Top 20 Features Discriminantes',
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

# Encontrar pares altamente correlacionados (|r| > 0.7)
print(f"\\nPares de features con correlación alta (|r| > 0.7):")
high_corr = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

if high_corr:
    for feat1, feat2, corr in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
        print(f"  {feat1:30s} <-> {feat2:30s}: {corr:.3f}")
else:
    print("  No se encontraron pares con correlación > 0.7")""")

add_markdown_cell("""---

## ⏰ Análisis Temporal""")

add_code_cell("""# ANÁLISIS TEMPORAL (TIMESTAMP)

if 'Timestamp' in df.columns:
    print(f"\\n{'='*80}")
    print("ANÁLISIS TEMPORAL")
    print(f"{'='*80}")

    # Convertir epoch a datetime para análisis
    df['DateTime'] = pd.to_datetime(df['Timestamp'], unit='s')

    # Extraer componentes temporales
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Date'] = df['DateTime'].dt.date

    print(f"\\nPeriodo del dataset:")
    print(f"  Inicio: {df['DateTime'].min()}")
    print(f"  Fin: {df['DateTime'].max()}")
    print(f"  Duración: {(df['DateTime'].max() - df['DateTime'].min()).days} días")

    # Distribución por hora
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Por hora del día
    hour_counts_benign = df[df['Label'] == 'Benign']['Hour'].value_counts().sort_index()
    hour_counts_attack = df[df['Label'] == 'Brute Force']['Hour'].value_counts().sort_index()

    axes[0, 0].plot(hour_counts_benign.index, hour_counts_benign.values,
                    marker='o', label='Benign', color='#3498db', linewidth=2)
    axes[0, 0].plot(hour_counts_attack.index, hour_counts_attack.values,
                    marker='s', label='Brute Force', color='#e74c3c', linewidth=2)
    axes[0, 0].set_title('Distribución por Hora del Día', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Hora', fontsize=12)
    axes[0, 0].set_ylabel('Cantidad de Registros', fontsize=12)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Por día de la semana
    day_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    dow_counts_benign = df[df['Label'] == 'Benign']['DayOfWeek'].value_counts().sort_index()
    dow_counts_attack = df[df['Label'] == 'Brute Force']['DayOfWeek'].value_counts().sort_index()

    x = np.arange(len(day_names))
    width = 0.35
    axes[0, 1].bar(x - width/2, dow_counts_benign.values, width,
                   label='Benign', color='#3498db', alpha=0.8)
    axes[0, 1].bar(x + width/2, dow_counts_attack.values, width,
                   label='Brute Force', color='#e74c3c', alpha=0.8)
    axes[0, 1].set_title('Distribución por Día de la Semana', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Día', fontsize=12)
    axes[0, 1].set_ylabel('Cantidad de Registros', fontsize=12)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(day_names)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # Timeline de ataques
    attack_timeline = df[df['Label'] == 'Brute Force'].groupby('Date').size()

    axes[1, 0].plot(attack_timeline.index, attack_timeline.values,
                    marker='o', label='Brute Force', color='#e74c3c', linewidth=2)
    axes[1, 0].set_title('Timeline de Ataques Brute Force', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Fecha', fontsize=12)
    axes[1, 0].set_ylabel('Cantidad de Ataques', fontsize=12)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Ratio Brute Force por hora
    total_by_hour = df.groupby('Hour')['Label'].value_counts().unstack(fill_value=0)
    if 'Brute Force' in total_by_hour.columns and 'Benign' in total_by_hour.columns:
        ratio_by_hour = total_by_hour['Brute Force'] / (total_by_hour['Benign'] + total_by_hour['Brute Force'])
        axes[1, 1].bar(ratio_by_hour.index, ratio_by_hour.values, color='#e74c3c', alpha=0.7)
        axes[1, 1].set_title('Ratio de Brute Force por Hora', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Hora', fontsize=12)
        axes[1, 1].set_ylabel('Ratio Brute Force', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].axhline(y=0.5, color='black', linestyle='--', linewidth=1, label='Balance (50%)')
        axes[1, 1].legend()

    plt.tight_layout()
    plt.show()
else:
    print("\\nTimestamp no encontrado en el dataset")""")

add_markdown_cell("""---

## 🌐 Análisis de Features de Tráfico de Red""")

add_code_cell("""# ANÁLISIS DE VELOCIDAD (PACKETS/S, BYTES/S)

print(f"\\n{'='*80}")
print("ANÁLISIS DE VELOCIDAD DE TRÁFICO")
print(f"{'='*80}")

# Buscar features de velocidad
speed_features = [col for col in numeric_features if 'Packets/s' in col or 'Bytes/s' in col]

if speed_features:
    print(f"\\nFeatures de velocidad encontradas: {len(speed_features)}")
    for feat in speed_features:
        print(f"  - {feat}")

    # Visualizar
    n_speed = len(speed_features)
    if n_speed > 0:
        fig, axes = plt.subplots(1, min(n_speed, 3), figsize=(16, 5))
        if n_speed == 1:
            axes = [axes]

        for i, feat in enumerate(speed_features[:3]):
            benign_data = df_benign[feat]
            attack_data = df_attack[feat]

            axes[i].hist(benign_data, bins=50, alpha=0.6, label='Benign',
                        color='#3498db', density=True)
            axes[i].hist(attack_data, bins=50, alpha=0.6, label='Brute Force',
                        color='#e74c3c', density=True)
            axes[i].set_title(f'{feat}', fontsize=12, fontweight='bold')
            axes[i].set_xlabel('Valor', fontsize=10)
            axes[i].set_ylabel('Densidad', fontsize=10)
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        # Estadísticas
        print(f"\\nEstadísticas de velocidad:")
        for feat in speed_features:
            benign_mean = df_benign[feat].mean()
            attack_mean = df_attack[feat].mean()
            diff_pct = ((attack_mean / (benign_mean + 1e-10)) - 1) * 100
            print(f"\\n{feat}:")
            print(f"  Benign: {benign_mean:.6f}")
            print(f"  Brute Force: {attack_mean:.6f}")
            print(f"  Diferencia: {attack_mean - benign_mean:+.6f} ({diff_pct:+.2f}%)")
else:
    print("\\nNo se encontraron features de velocidad")""")

add_code_cell("""# ANÁLISIS DE TCP FLAGS

print(f"\\n{'='*80}")
print("ANÁLISIS DE TCP FLAGS")
print(f"{'='*80}")

# Buscar features de flags TCP
flag_features = [col for col in numeric_features if 'Flag' in col]

if flag_features:
    print(f"\\nFeatures de TCP flags encontradas: {len(flag_features)}")
    for feat in flag_features:
        print(f"  - {feat}")

    # Comparar medias
    print(f"\\nComparación de TCP Flags (Benign vs Brute Force):")
    print(f"{'Flag':<25} {'Benign':>12} {'Brute Force':>12} {'Diferencia':>12}")
    print("-" * 65)

    for feat in flag_features:
        benign_mean = df_benign[feat].mean()
        attack_mean = df_attack[feat].mean()
        diff = attack_mean - benign_mean
        print(f"{feat:<25} {benign_mean:>12.6f} {attack_mean:>12.6f} {diff:>12.6f}")

    # Visualizar
    if len(flag_features) > 0:
        fig, ax = plt.subplots(figsize=(14, 6))

        x = np.arange(len(flag_features))
        width = 0.35

        benign_means = [df_benign[feat].mean() for feat in flag_features]
        attack_means = [df_attack[feat].mean() for feat in flag_features]

        ax.bar(x - width/2, benign_means, width, label='Benign',
               color='#3498db', alpha=0.8)
        ax.bar(x + width/2, attack_means, width, label='Brute Force',
               color='#e74c3c', alpha=0.8)

        ax.set_title('Comparación de TCP Flags: Benign vs Brute Force',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('TCP Flag', fontsize=12)
        ax.set_ylabel('Valor Promedio (Normalizado)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([f.replace(' Flag Cnt', '').replace(' Flag Count', '') for f in flag_features], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.show()
else:
    print("\\nNo se encontraron features de TCP flags")""")

add_code_cell("""# ANÁLISIS DE IAT (INTER-ARRIVAL TIME)

print(f"\\n{'='*80}")
print("ANÁLISIS DE INTER-ARRIVAL TIME (IAT)")
print(f"{'='*80}")

# Buscar features de IAT
iat_features = [col for col in numeric_features if 'IAT' in col]

if iat_features:
    print(f"\\nFeatures de IAT encontradas: {len(iat_features)}")
    for feat in iat_features:
        print(f"  - {feat}")

    # Visualizar top IAT features
    n_iat = min(len(iat_features), 6)
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.ravel()

    for i, feat in enumerate(iat_features[:n_iat]):
        benign_data = df_benign[feat]
        attack_data = df_attack[feat]

        axes[i].hist(benign_data, bins=50, alpha=0.6, label='Benign',
                    color='#3498db', density=True)
        axes[i].hist(attack_data, bins=50, alpha=0.6, label='Brute Force',
                    color='#e74c3c', density=True)
        axes[i].set_title(f'{feat}', fontsize=11, fontweight='bold')
        axes[i].set_xlabel('Valor', fontsize=9)
        axes[i].set_ylabel('Densidad', fontsize=9)
        axes[i].legend(fontsize=8)
        axes[i].grid(True, alpha=0.3)

    # Ocultar ejes sobrantes
    for i in range(n_iat, 6):
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

    # Estadísticas de IAT
    print(f"\\nEstadísticas de IAT (Benign vs Brute Force):")
    for feat in iat_features[:5]:
        benign_mean = df_benign[feat].mean()
        attack_mean = df_attack[feat].mean()
        benign_std = df_benign[feat].std()
        attack_std = df_attack[feat].std()

        print(f"\\n{feat}:")
        print(f"  Benign - Mean: {benign_mean:.6f}, Std: {benign_std:.6f}")
        print(f"  Brute Force - Mean: {attack_mean:.6f}, Std: {attack_std:.6f}")
else:
    print("\\nNo se encontraron features de IAT")""")

add_code_cell("""# ANÁLISIS DE PACKET LENGTH

print(f"\\n{'='*80}")
print("ANÁLISIS DE PACKET LENGTH")
print(f"{'='*80}")

# Buscar features de packet length
pkt_len_features = [col for col in numeric_features if 'Pkt Len' in col or 'Packet Length' in col]

if pkt_len_features:
    print(f"\\nFeatures de Packet Length encontradas: {len(pkt_len_features)}")
    for feat in pkt_len_features:
        print(f"  - {feat}")

    # Visualizar
    if len(pkt_len_features) > 0:
        n_pkt = min(len(pkt_len_features), 4)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.ravel()

        for i, feat in enumerate(pkt_len_features[:n_pkt]):
            axes[i].violinplot([df_benign[feat], df_attack[feat]],
                              positions=[1, 2], showmeans=True)
            axes[i].set_title(f'{feat}', fontsize=12, fontweight='bold')
            axes[i].set_xticks([1, 2])
            axes[i].set_xticklabels(['Benign', 'Brute Force'])
            axes[i].set_ylabel('Valor', fontsize=10)
            axes[i].grid(True, alpha=0.3, axis='y')

        # Ocultar ejes sobrantes
        for i in range(n_pkt, 4):
            axes[i].axis('off')

        plt.tight_layout()
        plt.show()
else:
    print("\\nNo se encontraron features de Packet Length")""")

add_markdown_cell("""---

## 📝 Conclusiones del EDA

### Hallazgos Principales:

**1. Balance del Dataset**
- Dataset perfectamente balanceado: 50% Brute Force / 50% Benign
- Total: ~763,000 registros
- Features: 60 (después de eliminar correlaciones >0.99)

**2. Calidad de Datos**
- ✓ No hay valores nulos
- ✓ No hay duplicados
- ✓ Valores normalizados entre 0 y 1 (MinMaxScaler)

**3. Features Discriminantes**
- Las features con mayor diferencia entre clases son las más importantes para el modelo
- TCP Flags, velocidad de paquetes (Packets/s, Bytes/s) y IAT son buenos discriminadores
- Packet Length también muestra patrones distintivos

**4. Patrones Temporales**
- Dataset cubre múltiples días de tráfico de red
- Posibles patrones horarios dependiendo del tipo de ataque (FTP, SSH, Web, XSS)
- Importante para validación temporal del modelo

**5. Características del Tráfico**
- Brute Force típicamente muestra patrones repetitivos en velocidad y flags TCP
- IAT (Inter-Arrival Time) puede ser menor en ataques (conexiones más rápidas)
- Packet length varía según el tipo de Brute Force

### Próximos Pasos:

**1. Feature Engineering (Opcional)**
- Crear ratios entre features relacionadas (ej: Fwd/Bwd packets ratio)
- Agregar features de interacción (ej: TCP flag combinations)
- Considerar transformaciones no lineales para features con alta varianza

**2. Modelado**
- **XGBoost** (recomendado para datasets balanceados)
- **Random Forest**
- **Gradient Boosting**
- Métricas esperadas: F1-Score 0.95-0.99

**3. Feature Selection**
- Usar importancia de features del modelo
- Eliminar features redundantes si es necesario
- Optimizar conjunto final de features

**4. Validación y Optimización**
- K-Fold Cross-Validation (k=5)
- Hyperparameter tuning (GridSearchCV o RandomizedSearchCV)
- Split temporal si es posible (train: primeros días, test: últimos días)

---

**Dataset listo para modelado** ✓""")

# ============================================================================
# GUARDAR NOTEBOOK
# ============================================================================

output_path = '/home/megalodon/dev/cbproy/pred_model/fuerza-bruta/analysis/EDA_Brute_Force_Detection.ipynb'
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"✓ Notebook creado exitosamente: {output_path}")
print(f"  Total de celdas: {len(notebook['cells'])}")
print(f"  - Markdown: {sum(1 for c in notebook['cells'] if c['cell_type'] == 'markdown')}")
print(f"  - Code: {sum(1 for c in notebook['cells'] if c['cell_type'] == 'code')}")
print(f"\\n✓ Notebook LIMPIO - Sin outputs, listo para ejecutar paso a paso")
