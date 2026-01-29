"""Script rápido para inspeccionar las etiquetas de cada dataset"""
import pandas as pd
import os

dataset_dir = '../dataset'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith('.csv')])

print("=" * 80)
print("INSPECCIÓN DE DATASETS CSE-CIC-IDS2018")
print("=" * 80)

for file in files:
    filepath = os.path.join(dataset_dir, file)
    print(f"\n{'=' * 80}")
    print(f"Archivo: {file}")
    print(f"{'=' * 80}")

    # Leer solo la columna Label para ser eficiente
    df = pd.read_csv(filepath, usecols=['Label'], low_memory=False)

    print(f"Total de registros: {len(df):,}")
    print(f"\nDistribución de clases:")
    print(df['Label'].value_counts())
