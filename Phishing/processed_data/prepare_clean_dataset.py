#!/usr/bin/env python3
"""
Script para extraer y guardar el dataset limpio con los 39,154 registros
que fueron parseados correctamente y usados en el EDA.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime

print("="*70)
print("PREPARACIÓN DE DATASET LIMPIO PARA MODELADO")
print("="*70)

# 1. CARGAR DATASET ORIGINAL
print("\n📂 Cargando dataset original...")
df = pd.read_csv("../dataset/CEAS_08.csv", encoding='utf-8')
print(f"✅ Dataset cargado: {df.shape[0]:,} registros x {df.shape[1]} columnas")

# 2. VERIFICAR QUE SON LOS MISMOS DATOS DEL EDA
expected_records = 39154
if df.shape[0] == expected_records:
    print(f"✅ VERIFICADO: Dataset tiene exactamente {expected_records:,} registros del EDA")
else:
    print(f"⚠️ ADVERTENCIA: Se esperaban {expected_records:,} pero se cargaron {df.shape[0]:,} registros")

# 3. MOSTRAR DISTRIBUCIÓN DE CLASES
print("\n📊 Distribución de clases:")
class_dist = df['label'].value_counts().sort_index()
for label in [0, 1]:
    count = class_dist[label]
    percentage = (count / len(df)) * 100
    label_name = "Legítimo" if label == 0 else "Spam/Phishing"
    print(f"   • Clase {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# 4. GUARDAR DATASET LIMPIO COMPLETO
output_clean = "CEAS_08_clean.csv"
print(f"\n💾 Guardando dataset limpio completo: {output_clean}")
df.to_csv(output_clean, index=False, encoding='utf-8')
print(f"✅ Guardado: {output_clean}")

# 5. CREAR SPLITS TRAIN/TEST (80/20 ESTRATIFICADO)
print("\n🔀 Creando splits Train/Test (80/20 estratificado)...")

X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print(f"✅ Train: {len(X_train):,} registros ({len(X_train)/len(df)*100:.1f}%)")
print(f"✅ Test: {len(X_test):,} registros ({len(X_test)/len(df)*100:.1f}%)")

# Verificar balance en cada split
print("\n📊 Distribución en Train:")
train_dist = y_train.value_counts().sort_index()
for label in [0, 1]:
    count = train_dist[label]
    percentage = (count / len(y_train)) * 100
    label_name = "Legítimo" if label == 0 else "Spam/Phishing"
    print(f"   • Clase {label} ({label_name}): {count:,} ({percentage:.2f}%)")

print("\n📊 Distribución en Test:")
test_dist = y_test.value_counts().sort_index()
for label in [0, 1]:
    count = test_dist[label]
    percentage = (count / len(y_test)) * 100
    label_name = "Legítimo" if label == 0 else "Spam/Phishing"
    print(f"   • Clase {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# 6. GUARDAR SPLITS
print("\n💾 Guardando splits...")

# Train set
train_df = pd.concat([X_train, y_train], axis=1)
train_df.to_csv("train.csv", index=False, encoding='utf-8')
print(f"✅ Guardado: train.csv ({len(train_df):,} registros)")

# Test set
test_df = pd.concat([X_test, y_test], axis=1)
test_df.to_csv("test.csv", index=False, encoding='utf-8')
print(f"✅ Guardado: test.csv ({len(test_df):,} registros)")

# 7. CREAR ARCHIVO DE METADATA
print("\n📝 Creando metadata...")
metadata = {
    'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_registros': len(df),
    'train_registros': len(train_df),
    'test_registros': len(test_df),
    'train_percentage': f"{len(train_df)/len(df)*100:.1f}%",
    'test_percentage': f"{len(test_df)/len(df)*100:.1f}%",
    'clase_0_total': int(class_dist[0]),
    'clase_1_total': int(class_dist[1]),
    'clase_0_percentage': f"{(class_dist[0]/len(df)*100):.2f}%",
    'clase_1_percentage': f"{(class_dist[1]/len(df)*100):.2f}%",
    'random_state': 42,
    'stratified': True
}

import json
with open("dataset_metadata.json", 'w') as f:
    json.dump(metadata, f, indent=4)
print("✅ Guardado: dataset_metadata.json")

# 8. RESUMEN FINAL
print("\n" + "="*70)
print("✅ DATASET LIMPIO PREPARADO EXITOSAMENTE")
print("="*70)
print("\n📁 Archivos generados:")
print(f"   1. CEAS_08_clean.csv       → Dataset completo ({len(df):,} registros)")
print(f"   2. train.csv               → Train set ({len(train_df):,} registros)")
print(f"   3. test.csv                → Test set ({len(test_df):,} registros)")
print(f"   4. dataset_metadata.json   → Metadata del split")
print("\n🎯 Listos para modelado con datos consistentes del EDA")
print("="*70)
