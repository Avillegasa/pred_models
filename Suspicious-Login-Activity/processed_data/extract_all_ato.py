"""
Script para extraer TODOS los casos de Account Takeover del dataset RBA

Este script escanea los 31M+ registros y extrae únicamente los casos
donde Is Account Takeover == True, guardándolos en un CSV separado.

Resultado: CSV con ~141 casos de Account Takeover puros
"""

import pandas as pd
from datetime import datetime

# Configuración
DATASET_PATH = "../dataset/rba-dataset.csv"
OUTPUT_PATH = "../analysis/all_ato_cases.csv"  # Guardar en analysis/
CHUNK_SIZE = 2_000_000  # 2M por chunk para más velocidad

print("=" * 80)
print("   EXTRACCIÓN DE TODOS LOS CASOS DE ACCOUNT TAKEOVER")
print("=" * 80)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Dataset original: {DATASET_PATH}")
print(f"💾 Output: {OUTPUT_PATH}")
print(f"🎯 Objetivo: Extraer TODOS los casos de ATO")

print("\n⏳ Escaneando dataset completo por chunks...")
print("   (Esto puede tomar 3-5 minutos)\n")

ato_chunks = []
total_records_scanned = 0
ato_found = 0
chunk_num = 0

try:
    for chunk in pd.read_csv(DATASET_PATH, chunksize=CHUNK_SIZE):
        chunk_num += 1
        total_records_scanned += len(chunk)

        # Filtrar solo Account Takeover == True
        ato_in_chunk = chunk[chunk['Is Account Takeover'] == True]

        if len(ato_in_chunk) > 0:
            ato_chunks.append(ato_in_chunk)
            ato_found += len(ato_in_chunk)
            print(f"   ✅ Chunk {chunk_num:2d}: {len(ato_in_chunk):2d} casos ATO | Total: {ato_found:3d} | Escaneados: {total_records_scanned:,}")
        else:
            print(f"   ⚪ Chunk {chunk_num:2d}: 0 casos ATO  | Total: {ato_found:3d} | Escaneados: {total_records_scanned:,}")

    print(f"\n{'=' * 80}")
    print("✅ ESCANEO COMPLETADO")
    print("=" * 80)

    if ato_found == 0:
        print("\n❌ ERROR: No se encontraron casos de Account Takeover")
        print("   Verifica que la columna 'Is Account Takeover' exista en el dataset")
        exit(1)

    # Combinar todos los chunks con ATO
    print(f"\n⏳ Combinando {len(ato_chunks)} chunks con casos ATO...")
    df_ato = pd.concat(ato_chunks, ignore_index=True)

    print(f"✅ Total de casos ATO combinados: {len(df_ato):,}")

    # Validación
    print(f"\n📊 VALIDACIÓN:")
    print(f"   • Registros escaneados: {total_records_scanned:,}")
    print(f"   • Account Takeover encontrados: {len(df_ato):,}")
    print(f"   • Porcentaje del dataset: {len(df_ato)/total_records_scanned*100:.6f}%")
    print(f"   • Ratio: 1:{total_records_scanned//len(df_ato):,}")

    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS DE LOS CASOS ATO:")
    print(f"   • Columnas: {len(df_ato.columns)}")
    print(f"   • Login exitosos: {df_ato['Login Successful'].sum()} ({df_ato['Login Successful'].sum()/len(df_ato)*100:.1f}%)")
    print(f"   • Usuarios únicos: {df_ato['User ID'].nunique()}")
    print(f"   • IPs únicas: {df_ato['IP Address'].nunique()}")
    print(f"   • Países únicos: {df_ato['Country'].nunique()}")
    print(f"   • Browsers únicos: {df_ato['Browser Name and Version'].nunique()}")

    # Guardar CSV
    print(f"\n⏳ Guardando casos ATO en {OUTPUT_PATH}...")
    df_ato.to_csv(OUTPUT_PATH, index=False)

    import os
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"✅ Archivo guardado exitosamente")
    print(f"💾 Tamaño: {file_size / 1024:.2f} KB")

    # Mostrar muestra
    print(f"\n📋 PRIMEROS 5 CASOS DE ACCOUNT TAKEOVER:")
    print("=" * 80)
    print(df_ato[['Login Timestamp', 'User ID', 'IP Address', 'Country',
                  'Browser Name and Version', 'Login Successful', 'Is Account Takeover']].head())

    print(f"\n{'=' * 80}")
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\n📁 Archivo generado: {OUTPUT_PATH}")
    print(f"📊 Casos ATO: {len(df_ato)}")
    print(f"💾 Tamaño: {file_size / 1024:.2f} KB")

    print(f"\n💡 PRÓXIMOS PASOS:")
    print(f"   1. Revisar los casos ATO en {OUTPUT_PATH}")
    print(f"   2. Usarlos para crear dataset balanceado")
    print(f"   3. Analizar patrones comunes en estos {len(df_ato)} casos")

except FileNotFoundError:
    print(f"\n❌ ERROR: No se encontró el archivo {DATASET_PATH}")
    print("   Verifica que el dataset esté en la ubicación correcta")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
