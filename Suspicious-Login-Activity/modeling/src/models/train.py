"""
ENTRENAMIENTO DE MODELOS para Account Takeover Detection
Versión local (sin Azure ML ni MLflow)

Entrena múltiples modelos de clasificación con manejo de desbalance:
- Logistic Regression
- Random Forest
- SVM (Support Vector Machine)
- Gradient Boosting

Selecciona el mejor modelo basado en F1-Score y guarda resultados completos.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve,
    average_precision_score, precision_recall_curve
)
import joblib
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# XGBoost para manejo óptimo de desbalance
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost no disponible. Instalar con: pip install xgboost")


def evaluate_model(y_true, y_pred, y_pred_proba, model_name):
    """
    Evaluar modelo y retornar métricas completas

    Args:
        y_true: Labels reales
        y_pred: Predicciones del modelo
        y_pred_proba: Probabilidades predichas (para AUC-ROC)
        model_name: Nombre del modelo

    Returns:
        dict: Diccionario con todas las métricas
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0)
    }

    # AUC-ROC (si hay probabilidades)
    if y_pred_proba is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
            metrics['average_precision'] = average_precision_score(y_true, y_pred_proba)
        except:
            metrics['roc_auc'] = None
            metrics['average_precision'] = None

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    metrics['confusion_matrix'] = {
        'TN': int(cm[0, 0]),
        'FP': int(cm[0, 1]),
        'FN': int(cm[1, 0]),
        'TP': int(cm[1, 1])
    }

    # False Positive Rate y False Negative Rate
    total_negative = cm[0, 0] + cm[0, 1]
    total_positive = cm[1, 0] + cm[1, 1]
    metrics['false_positive_rate'] = cm[0, 1] / total_negative if total_negative > 0 else 0
    metrics['false_negative_rate'] = cm[1, 0] / total_positive if total_positive > 0 else 0

    print(f"\n📊 Métricas para {model_name}:")
    print(f"   Accuracy:  {metrics['accuracy']:.4f}")
    print(f"   Precision: {metrics['precision']:.4f}")
    print(f"   Recall:    {metrics['recall']:.4f}")
    print(f"   F1-Score:  {metrics['f1_score']:.4f}")
    if metrics['roc_auc'] is not None:
        print(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
        print(f"   AUC-PR:    {metrics['average_precision']:.4f}")
    print(f"   FPR:       {metrics['false_positive_rate']:.4f}")
    print(f"   FNR:       {metrics['false_negative_rate']:.4f}")

    print(f"\n   Confusion Matrix:")
    print(f"   TN: {metrics['confusion_matrix']['TN']:5d}  FP: {metrics['confusion_matrix']['FP']:5d}")
    print(f"   FN: {metrics['confusion_matrix']['FN']:5d}  TP: {metrics['confusion_matrix']['TP']:5d}")

    return metrics


def plot_confusion_matrix(cm, model_name, save_path):
    """Graficar y guardar matriz de confusión"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Normal', 'Account Takeover'],
                yticklabels=['Normal', 'Account Takeover'])
    plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontweight='bold')
    plt.xlabel('Predicted Label', fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_roc_curves(models_results, save_path):
    """Graficar curvas ROC de todos los modelos"""
    plt.figure(figsize=(10, 8))

    for model_name, results in models_results.items():
        if 'roc_curve' in results and results['roc_curve'] is not None:
            fpr, tpr, _ = results['roc_curve']
            auc = results['metrics']['roc_auc']
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.4f})', linewidth=2)

    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontweight='bold', fontsize=12)
    plt.ylabel('True Positive Rate (Recall)', fontweight='bold', fontsize=12)
    plt.title('ROC Curves - All Models', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_precision_recall_curves(models_results, save_path):
    """Graficar curvas Precision-Recall de todos los modelos"""
    plt.figure(figsize=(10, 8))

    for model_name, results in models_results.items():
        if 'pr_curve' in results and results['pr_curve'] is not None:
            precision, recall, _ = results['pr_curve']
            auc_pr = results['metrics']['average_precision']
            plt.plot(recall, precision, label=f'{model_name} (AUC-PR = {auc_pr:.4f})', linewidth=2)

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall', fontweight='bold', fontsize=12)
    plt.ylabel('Precision', fontweight='bold', fontsize=12)
    plt.title('Precision-Recall Curves - All Models', fontsize=14, fontweight='bold')
    plt.legend(loc='lower left', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def train_models(X_train, X_test, y_train, y_test, config=None):
    """
    Entrenar todos los modelos y evaluar

    Args:
        X_train: Features de entrenamiento
        X_test: Features de prueba
        y_train: Labels de entrenamiento
        y_test: Labels de prueba
        config: Configuración de modelos (opcional)

    Returns:
        dict: Resultados de todos los modelos
    """
    print("🚀 Iniciando entrenamiento de modelos para ACCOUNT TAKEOVER DETECTION...")
    print(f"🔄 Train set: {X_train.shape[0]:,} samples, {X_train.shape[1]} features")
    print(f"🔄 Test set: {X_test.shape[0]:,} samples")
    print(f"📊 Train balance: ATO={y_train.sum()} ({y_train.sum()/len(y_train)*100:.2f}%), Normal={len(y_train)-y_train.sum()} ({(len(y_train)-y_train.sum())/len(y_train)*100:.2f}%)")
    print(f"📊 Test balance: ATO={y_test.sum()} ({y_test.sum()/len(y_test)*100:.2f}%), Normal={len(y_test)-y_test.sum()} ({(len(y_test)-y_test.sum())/len(y_test)*100:.2f}%)")

    # Configuración por defecto con class_weight='balanced' para manejar desbalance
    if config is None:
        config = {
            'random_state': 42,
            'logistic_regression': {'max_iter': 1000, 'n_jobs': -1, 'class_weight': 'balanced'},
            'random_forest': {'n_estimators': 100, 'max_depth': 10, 'n_jobs': -1, 'class_weight': 'balanced'},
            'svm': {'kernel': 'rbf', 'probability': True, 'class_weight': 'balanced'},
            'gradient_boosting': {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 0.1}
        }

    random_state = config.get('random_state', 42)

    # Definir modelos
    models = {
        'Logistic Regression': LogisticRegression(
            random_state=random_state,
            **config.get('logistic_regression', {'max_iter': 1000, 'n_jobs': -1, 'class_weight': 'balanced'})
        ),
        'Random Forest': RandomForestClassifier(
            random_state=random_state,
            **config.get('random_forest', {'n_estimators': 100, 'max_depth': 10, 'n_jobs': -1, 'class_weight': 'balanced'})
        ),
        'SVM': SVC(
            random_state=random_state,
            **config.get('svm', {'kernel': 'rbf', 'probability': True, 'class_weight': 'balanced'})
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            random_state=random_state,
            **config.get('gradient_boosting', {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 0.1})
        )
    }

    # Agregar XGBoost si está disponible
    if XGBOOST_AVAILABLE and 'xgboost' in config:
        models['XGBoost'] = XGBClassifier(
            random_state=random_state,
            **config.get('xgboost', {
                'n_estimators': 100,
                'max_depth': 7,
                'learning_rate': 0.1,
                'scale_pos_weight': 1,
                'eval_metric': 'aucpr'
            })
        )

    models_results = {}

    # Entrenar cada modelo
    for model_name, model in models.items():
        print(f"\n{'='*70}")
        print(f"🤖 Entrenando: {model_name}")
        print(f"{'='*70}")

        # Entrenar
        model.fit(X_train, y_train)

        # Predicciones
        y_pred = model.predict(X_test)

        # Probabilidades (si el modelo lo soporta)
        try:
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        except:
            y_pred_proba = None

        # Evaluar
        metrics = evaluate_model(y_test, y_pred, y_pred_proba, model_name)

        # Calcular ROC curve
        roc_curve_data = None
        pr_curve_data = None
        if y_pred_proba is not None:
            try:
                fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
                roc_curve_data = (fpr, tpr, thresholds)

                precision, recall, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)
                pr_curve_data = (precision, recall, pr_thresholds)
            except:
                pass

        # Guardar resultados
        models_results[model_name] = {
            'model': model,
            'metrics': metrics,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'roc_curve': roc_curve_data,
            'pr_curve': pr_curve_data
        }

    return models_results


def select_best_model(models_results, metric='f1_score'):
    """
    Seleccionar mejor modelo basado en una métrica

    Args:
        models_results: Diccionario con resultados de todos los modelos
        metric: Métrica para selección ('f1_score', 'recall', 'roc_auc', etc.)

    Returns:
        tuple: (nombre_del_mejor_modelo, objeto_modelo, métricas)
    """
    best_model_name = max(
        models_results.keys(),
        key=lambda x: models_results[x]['metrics'].get(metric, 0)
    )

    best_model = models_results[best_model_name]['model']
    best_metrics = models_results[best_model_name]['metrics']

    print(f"\n{'='*70}")
    print(f"🏆 MEJOR MODELO: {best_model_name}")
    print(f"{'='*70}")
    print(f"🎯 {metric.upper()}: {best_metrics[metric]:.4f}")
    print(f"📊 Precision: {best_metrics['precision']:.4f}")
    print(f"📊 Recall: {best_metrics['recall']:.4f}")
    print(f"📊 F1-Score: {best_metrics['f1_score']:.4f}")

    return best_model_name, best_model, best_metrics


def save_results(models_results, best_model_name, output_dir, X_train, y_test):
    """Guardar todos los resultados: modelos, métricas, visualizaciones"""
    os.makedirs(output_dir, exist_ok=True)
    models_dir = os.path.join(output_dir, 'models')
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print(f"\n💾 Guardando resultados en: {output_dir}")

    # 1. Guardar mejor modelo
    best_model = models_results[best_model_name]['model']
    best_model_path = os.path.join(models_dir, 'best_model.pkl')
    joblib.dump(best_model, best_model_path)
    print(f"✅ Mejor modelo guardado: {best_model_path}")

    # 2. Guardar todos los modelos
    for model_name, results in models_results.items():
        model_filename = model_name.lower().replace(' ', '_') + '.pkl'
        model_path = os.path.join(models_dir, model_filename)
        joblib.dump(results['model'], model_path)

    # 3. Guardar metadata completa
    model_info = {
        'timestamp': datetime.now().isoformat(),
        'best_model': best_model_name,
        'best_metrics': models_results[best_model_name]['metrics'],
        'n_features': X_train.shape[1],
        'n_train_samples': X_train.shape[0],
        'n_test_samples': len(y_test),
        'all_models_metrics': {
            name: results['metrics']
            for name, results in models_results.items()
        }
    }

    model_info_path = os.path.join(models_dir, 'model_info.json')
    with open(model_info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"✅ Metadata guardada: {model_info_path}")

    # 4. Guardar matrices de confusión
    for model_name, results in models_results.items():
        cm = confusion_matrix(y_test, results['predictions'])
        cm_filename = model_name.lower().replace(' ', '_') + '_confusion_matrix.png'
        cm_path = os.path.join(reports_dir, cm_filename)
        plot_confusion_matrix(cm, model_name, cm_path)

    print(f"✅ Matrices de confusión guardadas en: {reports_dir}")

    # 5. Guardar curvas ROC
    roc_path = os.path.join(reports_dir, 'roc_curves_comparison.png')
    plot_roc_curves(models_results, roc_path)
    print(f"✅ Curvas ROC guardadas: {roc_path}")

    # 6. Guardar curvas Precision-Recall
    pr_path = os.path.join(reports_dir, 'precision_recall_curves_comparison.png')
    plot_precision_recall_curves(models_results, pr_path)
    print(f"✅ Curvas Precision-Recall guardadas: {pr_path}")

    # 7. Crear reporte comparativo en texto
    report_path = os.path.join(reports_dir, 'models_comparison_report.txt')
    with open(report_path, 'w') as f:
        f.write("="*70 + "\n")
        f.write("REPORTE DE COMPARACIÓN DE MODELOS - ACCOUNT TAKEOVER DETECTION\n")
        f.write("="*70 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Features: {X_train.shape[1]}\n")
        f.write(f"Train samples: {X_train.shape[0]:,}\n")
        f.write(f"Test samples: {len(y_test):,}\n\n")

        for model_name, results in models_results.items():
            f.write(f"\n{'-'*70}\n")
            f.write(f"MODELO: {model_name}\n")
            f.write(f"{'-'*70}\n")
            metrics = results['metrics']
            f.write(f"Accuracy:  {metrics['accuracy']:.4f}\n")
            f.write(f"Precision: {metrics['precision']:.4f}\n")
            f.write(f"Recall:    {metrics['recall']:.4f}\n")
            f.write(f"F1-Score:  {metrics['f1_score']:.4f}\n")
            if metrics.get('roc_auc'):
                f.write(f"ROC-AUC:   {metrics['roc_auc']:.4f}\n")
                f.write(f"AUC-PR:    {metrics['average_precision']:.4f}\n")
            f.write(f"FPR:       {metrics['false_positive_rate']:.4f}\n")
            f.write(f"FNR:       {metrics['false_negative_rate']:.4f}\n")

            cm = metrics['confusion_matrix']
            f.write(f"\nConfusion Matrix:\n")
            f.write(f"  TN: {cm['TN']:5d}  FP: {cm['FP']:5d}\n")
            f.write(f"  FN: {cm['FN']:5d}  TP: {cm['TP']:5d}\n")

        f.write(f"\n{'='*70}\n")
        f.write(f"MEJOR MODELO: {best_model_name}\n")
        f.write(f"F1-Score: {models_results[best_model_name]['metrics']['f1_score']:.4f}\n")
        f.write(f"Recall: {models_results[best_model_name]['metrics']['recall']:.4f}\n")
        f.write(f"Precision: {models_results[best_model_name]['metrics']['precision']:.4f}\n")
        f.write(f"{'='*70}\n")

    print(f"✅ Reporte comparativo guardado: {report_path}")

    return model_info


if __name__ == "__main__":
    print("⚠️ NOTA: Este script debe ser llamado desde el pipeline principal.")
    print("⚠️ Ver: main_pipeline.py para ejecución completa.")
