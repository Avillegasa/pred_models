"""
PIPELINE PRINCIPAL DE MODELADO - ACCOUNT TAKEOVER DETECTION

Script principal que ejecuta el pipeline completo:
1. Carga del dataset balanceado RBA
2. Feature Engineering completo
3. Split Train/Test estratificado
4. Entrenamiento de 4 modelos (LR, RF, SVM, GB)
5. Comparación y selección del mejor modelo
6. Guardado de resultados completos

Uso:
    python3 main_pipeline.py
"""

import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import warnings

# Agregar src al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from features.feature_engineering import engineer_features, save_features_and_encoders
from models.train import train_models, select_best_model, save_results

warnings.filterwarnings('ignore')


def print_section_header(title):
    """Imprimir header de sección con estilo"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Pipeline principal de modelado"""

    print_section_header("🔐 ACCOUNT TAKEOVER DETECTION - PIPELINE DE MODELADO")
    print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # ============================================================================
    # PASO 1: CARGAR DATASET BALANCEADO
    # ============================================================================
    print_section_header("PASO 1: CARGA DE DATASET BALANCEADO")

    # Path relativo al dataset balanceado
    data_path = os.path.join(
        os.path.dirname(__file__),
        '../processed_data/rba_balanced.csv'
    )

    print(f"📂 Cargando dataset desde: {data_path}")

    if not os.path.exists(data_path):
        print(f"❌ ERROR: No se encontró el dataset en {data_path}")
        print("   Ejecuta primero: create_balanced_dataset.py")
        sys.exit(1)

    df = pd.read_csv(data_path)

    print(f"✅ Dataset cargado exitosamente")
    print(f"   • Registros: {len(df):,}")
    print(f"   • Columnas: {len(df.columns)}")
    print(f"   • Account Takeover: {df['Is Account Takeover'].sum()} ({df['Is Account Takeover'].sum()/len(df)*100:.4f}%)")
    print(f"   • Normal: {len(df) - df['Is Account Takeover'].sum():,} ({(len(df) - df['Is Account Takeover'].sum())/len(df)*100:.4f}%)")

    # ============================================================================
    # PASO 2: FEATURE ENGINEERING
    # ============================================================================
    print_section_header("PASO 2: FEATURE ENGINEERING")

    features_df, encoders = engineer_features(df, fit_encoders=True)

    print(f"\n✅ Feature Engineering completado")
    print(f"   • Features creadas: {features_df.shape[1] - 1}")  # -1 por el label
    print(f"   • Registros procesados: {len(features_df):,}")

    # Guardar features y encoders
    output_features_dir = os.path.join(os.path.dirname(__file__), 'outputs/features')
    save_features_and_encoders(features_df, encoders, output_features_dir)

    # ============================================================================
    # PASO 3: SPLIT TRAIN/TEST ESTRATIFICADO
    # ============================================================================
    print_section_header("PASO 3: SPLIT TRAIN/TEST")

    # Separar X y y
    X = features_df.drop('label', axis=1)
    y = features_df['label']

    # Split estratificado para mantener proporción de clases
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Mantener proporción de ATO vs Normal
    )

    print(f"✅ Split realizado con stratification")
    print(f"\n   📊 TRAIN SET:")
    print(f"      • Total: {len(X_train):,} samples")
    print(f"      • Account Takeover: {y_train.sum()} ({y_train.sum()/len(y_train)*100:.4f}%)")
    print(f"      • Normal: {len(y_train) - y_train.sum():,} ({(len(y_train) - y_train.sum())/len(y_train)*100:.4f}%)")

    print(f"\n   📊 TEST SET:")
    print(f"      • Total: {len(X_test):,} samples")
    print(f"      • Account Takeover: {y_test.sum()} ({y_test.sum()/len(y_test)*100:.4f}%)")
    print(f"      • Normal: {len(y_test) - y_test.sum():,} ({(len(y_test) - y_test.sum())/len(y_test)*100:.4f}%)")

    # ============================================================================
    # PASO 4: ENTRENAMIENTO DE MODELOS
    # ============================================================================
    print_section_header("PASO 4: ENTRENAMIENTO DE MODELOS")

    # Configuración de modelos con class_weight='balanced' para manejar desbalance
    config = {
        'random_state': 42,
        'logistic_regression': {
            'max_iter': 1000,
            'n_jobs': -1,
            'class_weight': 'balanced',
            'solver': 'lbfgs'
        },
        'random_forest': {
            'n_estimators': 100,
            'max_depth': 10,
            'n_jobs': -1,
            'class_weight': 'balanced',
            'min_samples_split': 5,
            'min_samples_leaf': 2
        },
        'svm': {
            'kernel': 'rbf',
            'probability': True,
            'class_weight': 'balanced',
            'gamma': 'scale',
            'C': 1.0
        },
        'gradient_boosting': {
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'min_samples_split': 5
        }
    }

    print("⚙️  Configuración de modelos:")
    print("   • Logistic Regression: class_weight='balanced', max_iter=1000")
    print("   • Random Forest: class_weight='balanced', n_estimators=100, max_depth=10")
    print("   • SVM: class_weight='balanced', kernel='rbf'")
    print("   • Gradient Boosting: n_estimators=100, max_depth=5, learning_rate=0.1")

    # Entrenar modelos
    models_results = train_models(X_train, X_test, y_train, y_test, config=config)

    # ============================================================================
    # PASO 5: SELECCIÓN DEL MEJOR MODELO
    # ============================================================================
    print_section_header("PASO 5: SELECCIÓN DEL MEJOR MODELO")

    # Seleccionar basado en F1-Score (balance entre Precision y Recall)
    best_model_name, best_model, best_metrics = select_best_model(
        models_results,
        metric='f1_score'
    )

    print(f"\n🎯 MÉTRICAS DEL MEJOR MODELO ({best_model_name}):")
    print(f"   • F1-Score:  {best_metrics['f1_score']:.4f}")
    print(f"   • Precision: {best_metrics['precision']:.4f}")
    print(f"   • Recall:    {best_metrics['recall']:.4f}")
    print(f"   • Accuracy:  {best_metrics['accuracy']:.4f}")
    if best_metrics.get('roc_auc'):
        print(f"   • ROC-AUC:   {best_metrics['roc_auc']:.4f}")
        print(f"   • AUC-PR:    {best_metrics['average_precision']:.4f}")

    # ============================================================================
    # PASO 6: GUARDAR RESULTADOS
    # ============================================================================
    print_section_header("PASO 6: GUARDADO DE RESULTADOS")

    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    model_info = save_results(models_results, best_model_name, output_dir, X_train, y_test)

    # ============================================================================
    # RESUMEN FINAL
    # ============================================================================
    print_section_header("✅ PIPELINE COMPLETADO EXITOSAMENTE")

    print("📊 RESUMEN:")
    print(f"   • Dataset: {len(df):,} registros balanceados")
    print(f"   • Features: {X_train.shape[1]}")
    print(f"   • Modelos entrenados: 4 (LR, RF, SVM, GB)")
    print(f"   • Mejor modelo: {best_model_name}")
    print(f"   • F1-Score: {best_metrics['f1_score']:.4f}")

    print(f"\n💾 ARCHIVOS GENERADOS:")
    print(f"   • Modelo: outputs/models/best_model.pkl")
    print(f"   • Encoders: outputs/features/label_encoders.pkl")
    print(f"   • Features: outputs/features/features.csv")
    print(f"   • Reportes: outputs/reports/")
    print(f"   • Metadata: outputs/models/model_info.json")

    print(f"\n📋 PRÓXIMOS PASOS:")
    print(f"   1. Revisar reportes en: outputs/reports/")
    print(f"   2. Analizar confusion matrices y curvas ROC/PR")
    print(f"   3. Crear API REST usando el mejor modelo")
    print(f"   4. Integrar con frontend React dashboard")

    print("\n" + "=" * 80)
    print(f"🎉 ¡Modelado completado! Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
