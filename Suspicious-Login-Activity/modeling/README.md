# Suspicious Login Activity - Account Takeover Detection

## 📋 Descripción

Sistema de Machine Learning para detección de **Account Takeover (ATO)** en eventos de autenticación. Utiliza el dataset balanceado RBA (Risk-Based Authentication) con 141K registros que incluyen **TODOS los 141 casos de ATO** del dataset original de 31M logins.

## 🎯 Objetivo

Identificar accesos sospechosos que, aunque técnicamente exitosos, presentan características anómalas como:
- Cambios súbitos de geolocalización (Impossible Travel)
- Cambios de dispositivo/browser inusuales
- Acceso desde IPs maliciosas
- Patrones temporales anormales

## 📊 Dataset

**Fuente**: RBA Dataset (DAS Group - KIT)
- **Original**: 31,269,265 logins (8.5 GB)
- **Balanceado**: 141,141 logins (39 MB) ✅ **Se usa este**
  - 141 casos de Account Takeover (100% incluidos)
  - 141,000 casos normales (muestreados)
  - Ratio 1:1000 (entrenable con SMOTE/class weights)

**Location**: `../processed_data/rba_balanced.csv`

## 🔧 Feature Engineering

### Features Temporales
- `hour`, `day_of_week`, `day_of_month`, `month`
- `is_weekend`, `is_night`, `is_business_hours`

### Features de Comportamiento
- `ip_changed`, `country_changed`, `browser_changed`, `device_changed`, `os_changed`
- `time_since_last_login_hours`, `is_rapid_login`, `is_long_gap`

### Features Agregados
- `ip_count_per_user`, `country_count_per_user`, `browser_count_per_user`
- `total_logins_per_user`, `success_rate_per_user`
- `user_count_per_ip`, `is_suspicious_ip`

### Features de Red
- `rtt_zscore`, `is_abnormal_rtt`
- `Is Attack IP` (directo del dataset)

### Features Categóricos Encoded
- Browser, OS, Device Type, Country, Region, City, ISP, ASN Organization

**Total**: ~35-40 features

## 🤖 Modelos Entrenados

1. **Logistic Regression** (baseline interpretable)
2. **Random Forest** (ensemble robusto)
3. **SVM** (Support Vector Machine)
4. **Gradient Boosting** (modelo avanzado)

**Técnicas de balance**:
- `class_weight='balanced'` en LR, RF, SVM
- Gradient Boosting con subsample

## 📈 Métricas de Evaluación

**Métricas clave** (NO usar Accuracy por desbalance):
- **F1-Score**: Balance entre Precision y Recall
- **Recall**: % de ATO detectados (crítico)
- **Precision**: % de predicciones ATO correctas
- **ROC-AUC**: Área bajo curva ROC
- **AUC-PR**: Área bajo curva Precision-Recall

**Objetivo de negocio**:
- Maximizar Recall (no dejar pasar ATOs)
- Minimizar FPR (no bloquear usuarios legítimos)

## 🚀 Ejecución

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar Pipeline Completo

```bash
cd /home/megalodon/dev/cbproy/pred_model/Suspicious-Login-Activity/modeling
python3 main_pipeline.py
```

El pipeline ejecuta automáticamente:
1. Carga del dataset balanceado
2. Feature engineering completo
3. Split train/test estratificado (80/20)
4. Entrenamiento de 4 modelos
5. Comparación y selección del mejor
6. Guardado de resultados

**Tiempo estimado**: 10-30 minutos (dependiendo del hardware)

## 📁 Estructura de Outputs

```
outputs/
├── models/
│   ├── best_model.pkl                    # Mejor modelo (basado en F1-Score)
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── svm.pkl
│   ├── gradient_boosting.pkl
│   └── model_info.json                   # Metadata y métricas
│
├── features/
│   ├── features.csv                      # Features engineered completas
│   └── label_encoders.pkl                # Encoders para features categóricos
│
└── reports/
    ├── models_comparison_report.txt      # Reporte comparativo
    ├── roc_curves_comparison.png         # Curvas ROC
    ├── precision_recall_curves_comparison.png
    ├── logistic_regression_confusion_matrix.png
    ├── random_forest_confusion_matrix.png
    ├── svm_confusion_matrix.png
    └── gradient_boosting_confusion_matrix.png
```

## 📊 Ejemplo de Resultados Esperados

Basado en el análisis del EDA y características del dataset:

```
Mejor Modelo: Gradient Boosting / Random Forest (esperado)
F1-Score: 0.85-0.95 (con class weights)
Recall: 0.80-0.95 (prioridad: detectar ATOs)
Precision: 0.70-0.90 (minimizar falsos positivos)
ROC-AUC: 0.90-0.98
```

## 🔍 Análisis de Errores

**False Positives (FP)**: Usuarios legítimos marcados como ATO
- Causa común: Usuario viajando, cambió de dispositivo legítimamente
- Impacto: Mala UX (bloqueo innecesario)

**False Negatives (FN)**: ATOs no detectados
- Causa común: Atacante imita comportamiento normal
- Impacto: Compromiso de cuenta (MÁS COSTOSO)

**Objetivo**: Minimizar FN (prioridad) manteniendo FP aceptables

## 📋 Próximos Pasos

1. ✅ Feature Engineering completado
2. ✅ Entrenamiento de modelos completado
3. 🔜 **Threshold Tuning**: Optimizar threshold de clasificación
4. 🔜 **API REST**: Crear endpoint FastAPI (similar a Phishing)
5. 🔜 **Frontend Integration**: Conectar con dashboard React

## 🔑 Notas Importantes

- **Dataset balanceado**: Usamos 141K registros (no 31M) por limitaciones de RAM
- **Todos los ATO incluidos**: Los 141 casos reales están en el dataset balanceado
- **Class weights**: Crítico para manejar el desbalance 1:1000
- **Stratified split**: Mantiene proporción de clases en train/test
- **Temporal features**: Basados en análisis EDA de patrones horarios/semanales

## 📚 Referencias

- **Dataset**: [RBA Dataset (DAS Group - KIT)](https://www.kaggle.com/datasets/dasgroup/rba-dataset)
- **Paper**: Risk-Based Authentication Dataset for Single Sign-On
- **EDA**: `../analysis/EDA_Suspicious_Login_RBA.ipynb`

---

**Autor**: Proyecto académico de predicción de incidentes de ciberseguridad

**Fecha**: 2026-01-12

**Contacto**: Ver CLAUDE.md en raíz del proyecto
