#!/usr/bin/env python3
"""
Script rápido para re-entrenar el modelo de Phishing Detection
con la versión actual de NumPy/Scikit-learn.

Este script reproduce el pipeline del notebook original y guarda
los modelos compatibles con las versiones actuales.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Flush output para ver progreso en tiempo real
import functools
print = functools.partial(print, flush=True)
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
import joblib
import json
from datetime import datetime

from features.feature_engineering import engineer_features

def main():
    print("=" * 70)
    print("🔄 RE-ENTRENAMIENTO DE MODELO PHISHING DETECTION")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 NumPy: {np.__version__}")

    # Rutas
    data_dir = '../processed_data'
    output_dir = 'outputs/models'
    os.makedirs(output_dir, exist_ok=True)

    # 1. Cargar datos
    print("\n📂 Cargando datos...")
    train_df = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    test_df = pd.read_csv(os.path.join(data_dir, 'test.csv'))
    print(f"   Train: {len(train_df):,} registros")
    print(f"   Test: {len(test_df):,} registros")

    # 2. Feature Engineering
    print("\n🔧 Feature Engineering...")
    config = {
        'max_features': 1000,
        'ngram_range': (1, 2),
        'min_df': 5
    }

    # Train features
    train_features, tfidf_vectorizer = engineer_features(
        train_df,
        tfidf_vectorizer=None,
        fit_tfidf=True,
        config=config
    )

    # Test features (usar el mismo vectorizador)
    test_features, _ = engineer_features(
        test_df,
        tfidf_vectorizer=tfidf_vectorizer,
        fit_tfidf=False,
        config=config
    )

    # Separar X e y
    X_train = train_features.drop('label', axis=1)
    y_train = train_features['label']
    X_test = test_features.drop('label', axis=1)
    y_test = test_features['label']

    print(f"\n📊 Features: {X_train.shape[1]}")
    print(f"   Train samples: {len(X_train):,}")
    print(f"   Test samples: {len(X_test):,}")

    # 3. Entrenar modelos
    print("\n" + "=" * 70)
    print("🤖 ENTRENANDO MODELOS...")
    print("=" * 70)

    # SVM omitido porque es muy lento con datasets grandes
    models = {
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            n_jobs=-1,
            random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            max_iter=2000,
            random_state=42
        ),
    }

    results = {}
    best_model_name = None
    best_f1 = 0

    for name, model in models.items():
        print(f"\n🔄 Entrenando {name}...")
        model.fit(X_train, y_train)

        # Predicciones
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

        # Métricas
        f1 = f1_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
        cm = confusion_matrix(y_test, y_pred)

        results[name] = {
            'model': model,
            'f1_score': f1,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'roc_auc': auc,
            'confusion_matrix': {
                'TN': int(cm[0, 0]),
                'FP': int(cm[0, 1]),
                'FN': int(cm[1, 0]),
                'TP': int(cm[1, 1])
            }
        }

        print(f"   ✅ F1: {f1:.4f} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    # 4. Guardar modelos
    print("\n" + "=" * 70)
    print("💾 GUARDANDO MODELOS...")
    print("=" * 70)

    # Guardar todos los modelos
    for name, data in results.items():
        filename = name.lower().replace(' ', '_') + '.pkl'
        filepath = os.path.join(output_dir, filename)
        joblib.dump(data['model'], filepath)
        print(f"   ✅ {name}: {filepath}")

    # Guardar mejor modelo como best_model.pkl
    best_model_path = os.path.join(output_dir, 'best_model.pkl')
    joblib.dump(results[best_model_name]['model'], best_model_path)
    print(f"\n   🏆 Mejor modelo ({best_model_name}): {best_model_path}")

    # Guardar vectorizador TF-IDF
    vectorizer_path = os.path.join(output_dir, 'tfidf_vectorizer.pkl')
    joblib.dump(tfidf_vectorizer, vectorizer_path)
    print(f"   ✅ TF-IDF Vectorizer: {vectorizer_path}")

    # 5. Guardar metadata
    model_info = {
        'timestamp': datetime.now().isoformat(),
        'numpy_version': np.__version__,
        'best_model': best_model_name,
        'best_metrics': {
            'f1_score': results[best_model_name]['f1_score'],
            'accuracy': results[best_model_name]['accuracy'],
            'precision': results[best_model_name]['precision'],
            'recall': results[best_model_name]['recall'],
            'roc_auc': results[best_model_name]['roc_auc'],
            'confusion_matrix': results[best_model_name]['confusion_matrix']
        },
        'n_features': X_train.shape[1],
        'n_train_samples': len(X_train),
        'n_test_samples': len(X_test),
        'all_models_metrics': {
            name: {k: v for k, v in data.items() if k != 'model'}
            for name, data in results.items()
        }
    }

    info_path = os.path.join(output_dir, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"   ✅ Metadata: {info_path}")

    # Resumen final
    print("\n" + "=" * 70)
    print("🏆 RESUMEN FINAL")
    print("=" * 70)
    print(f"\nMejor modelo: {best_model_name}")
    print(f"F1-Score: {results[best_model_name]['f1_score']:.4f}")
    print(f"Accuracy: {results[best_model_name]['accuracy']:.4f}")
    print(f"Precision: {results[best_model_name]['precision']:.4f}")
    print(f"Recall: {results[best_model_name]['recall']:.4f}")

    print("\n✅ Re-entrenamiento completado exitosamente!")
    print("   Ahora puedes reiniciar la API de Phishing.")

if __name__ == "__main__":
    main()
