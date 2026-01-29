# 🤖 Phishing Email Detection - Modelado de Machine Learning

Proyecto completo de modelado para detección de emails phishing usando Machine Learning.
**Versión local** (sin Azure ML) con 4 modelos: Logistic Regression, Random Forest, SVM y Gradient Boosting.

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Modelos Incluidos](#-modelos-incluidos)
- [Feature Engineering](#-feature-engineering)
- [Configuración](#-configuración)
- [Resultados](#-resultados)
- [Archivos Generados](#-archivos-generados)

---

## 🎯 Descripción General

Este proyecto implementa un sistema de clasificación binaria para detectar emails de phishing vs emails legítimos. Basado en el dataset CEAS_08 con 39,154 emails limpios.

### Características Principales

- ✅ **4 modelos de ML**: Logistic Regression, Random Forest, SVM, Gradient Boosting
- ✅ **Feature Engineering completo**: TF-IDF + metadata + sentiment analysis
- ✅ **Sin Azure ML**: Ejecución 100% local
- ✅ **Evaluación exhaustiva**: ROC curves, confusion matrices, métricas completas
- ✅ **Modular y extensible**: Fácil agregar nuevos modelos o features
- ✅ **Configuración centralizada**: Todo configurable desde `config.yaml`

### Dataset

- **Total**: 39,154 emails
- **Train**: 31,323 (80%)
- **Test**: 7,831 (20%)
- **Clases**:
  - 0 = Legítimo (44.22%)
  - 1 = Phishing (55.78%)

---

## 📁 Estructura del Proyecto

```
modeling/
├── config/
│   └── config.yaml                    # Configuración centralizada
├── src/
│   ├── features/
│   │   └── feature_engineering.py    # Extracción de features
│   └── models/
│       └── train.py                   # Entrenamiento de modelos
├── notebooks/
│   └── Phishing_Detection_Modeling.ipynb  # Notebook principal
├── outputs/
│   ├── models/                        # Modelos entrenados (.pkl)
│   ├── reports/                       # Visualizaciones y reportes
│   └── features/                      # Features procesadas
├── requirements.txt                   # Dependencias
└── README.md                          # Esta documentación
```

---

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.9+
- pip o conda

### 2. Instalar Dependencias

```bash
cd modeling
pip install -r requirements.txt
```

**Dependencias principales**:
- pandas, numpy, scikit-learn
- matplotlib, seaborn
- jupyter, jupyterlab
- pyyaml

---

## 💻 Uso

### Opción 1: Notebook Interactivo (Recomendado)

```bash
# Navegar al directorio de notebooks
cd modeling/notebooks

# Iniciar Jupyter
jupyter notebook Phishing_Detection_Modeling.ipynb
```

Ejecutar las celdas secuencialmente. El notebook incluye:
1. Carga de datos
2. Feature engineering
3. Entrenamiento de 4 modelos
4. Comparación de métricas
5. Selección del mejor modelo
6. Guardado de resultados

### Opción 2: Scripts Individuales

**Feature Engineering**:
```bash
python src/features/feature_engineering.py \
    --input_data ../processed_data/train.csv \
    --output_dir outputs/features \
    --max_features 1000 \
    --ngram_min 1 \
    --ngram_max 2
```

**Entrenamiento** (requiere features pre-procesadas):
```bash
python src/models/train.py \
    --features_path outputs/features/features.csv \
    --output_dir outputs \
    --random_state 42
```

---

## 🤖 Modelos Incluidos

| Modelo | Descripción | Hiperparámetros Principales |
|--------|-------------|------------------------------|
| **Logistic Regression** | Baseline rápido y interpretable | `max_iter=1000`, `penalty='l2'` |
| **Random Forest** | Ensemble de árboles | `n_estimators=100`, `max_depth=10` |
| **SVM** | Support Vector Machine | `kernel='rbf'`, `probability=True` |
| **Gradient Boosting** | Boosting secuencial | `n_estimators=100`, `learning_rate=0.1` |

Todos los modelos son configurables desde `config/config.yaml`.

---

## 🔧 Feature Engineering

### Features Creadas (Total: ~1,015)

#### 1. Features Numéricas (15)
- `subject_length`, `subject_words`, `subject_special`
- `body_length`, `body_words`, `body_special`
- `url_count`, `urls` (binario)
- `sender_domain_encoded` (top 50 dominios)
- `subject_sentiment`, `body_sentiment` (basado en keywords)
- `subject_body_ratio`, `special_chars_ratio`
- `has_urgent`, `has_free`, `has_click` (keywords binarios)

#### 2. Features TF-IDF (~1,000)
- Vectorización de subject + body combinados
- Configuración:
  - `max_features`: 1,000
  - `ngram_range`: (1, 2) - unigrams y bigrams
  - `min_df`: 5 (mínima frecuencia documental)
  - `stop_words`: 'english'

### Proceso de Feature Engineering

1. **Limpieza**: Rellenar nulos en subject/body/sender
2. **Extracción de texto**: Longitudes, palabras, caracteres especiales
3. **Metadata**: Dominio del sender, conteo de URLs
4. **Sentiment**: Score basado en keywords phishing vs legítimos
5. **Features derivadas**: Ratios, presencia de keywords críticas
6. **TF-IDF**: Vectorización del contenido textual
7. **Encoding**: Label encoding de dominios frecuentes

---

## ⚙️ Configuración

Toda la configuración está en `config/config.yaml`:

```yaml
project:
  name: "phishing_detection_local"
  version: "1.0.0"

data:
  train_file: "train.csv"
  test_file: "test.csv"
  random_state: 42

features:
  tfidf:
    max_features: 1000
    ngram_range: [1, 2]
    min_df: 5

models:
  random_state: 42
  logistic_regression:
    max_iter: 1000
  random_forest:
    n_estimators: 100
    max_depth: 10
  svm:
    kernel: 'rbf'
  gradient_boosting:
    n_estimators: 100
    learning_rate: 0.1

evaluation:
  primary_metric: 'f1_score'
```

### Modificar Configuración

Editar `config/config.yaml` para:
- Cambiar hiperparámetros de modelos
- Ajustar TF-IDF (max_features, ngrams, etc.)
- Cambiar métrica de selección (f1_score, accuracy, roc_auc)

---

## 📊 Resultados

Al finalizar el entrenamiento, se genera:

### 1. Métricas de Todos los Modelos

Comparación en tabla y gráficos:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### 2. Visualizaciones

- **Confusion Matrices**: Por cada modelo
- **ROC Curves**: Comparación de todos los modelos
- **Gráficos de barras**: Comparación de métricas

### 3. Mejor Modelo

Selección automática basado en F1-Score (configurable).

**Ejemplo de resultados esperados**:
```
🏆 Mejor Modelo: Logistic Regression
🎯 F1-Score: 0.9759
📈 Accuracy: 0.9729
```

---

## 📦 Archivos Generados

Todos los outputs se guardan en `outputs/`:

### `outputs/models/`
```
best_model.pkl               # Mejor modelo serializado
logistic_regression.pkl      # Todos los modelos individuales
random_forest.pkl
svm.pkl
gradient_boosting.pkl
model_info.json              # Metadata completa con métricas
```

### `outputs/reports/`
```
logistic_regression_confusion_matrix.png
random_forest_confusion_matrix.png
svm_confusion_matrix.png
gradient_boosting_confusion_matrix.png
roc_curves_comparison.png
models_comparison_report.txt  # Reporte en texto plano
```

### `outputs/features/`
```
train_features.csv           # Features procesadas de train
test_features.csv            # Features procesadas de test
tfidf_vectorizer.pkl         # Vectorizador TF-IDF entrenado
```

---

## 📈 Cómo Usar el Modelo Entrenado

### Cargar el Mejor Modelo

```python
import joblib
import pandas as pd

# Cargar modelo
model = joblib.load('outputs/models/best_model.pkl')

# Cargar vectorizador TF-IDF
tfidf_vectorizer = joblib.load('outputs/features/tfidf_vectorizer.pkl')

# Procesar nuevos emails
from src.features.feature_engineering import engineer_features

new_emails_df = pd.read_csv('new_emails.csv')
new_features, _ = engineer_features(
    new_emails_df,
    tfidf_vectorizer=tfidf_vectorizer,
    fit_tfidf=False  # Solo transform
)

# Predecir
X_new = new_features.drop('label', axis=1)  # Si no tiene label, omitir
predictions = model.predict(X_new)
probabilities = model.predict_proba(X_new)

print(f"Predicción: {predictions}")  # 0=Legítimo, 1=Phishing
print(f"Probabilidades: {probabilities}")
```

---

## 🔍 Análisis de Errores

El notebook incluye análisis de:

- **False Positives**: Emails legítimos marcados como phishing
- **False Negatives**: Emails phishing marcados como legítimos

Revisar estos casos ayuda a mejorar el modelo.

---

## 🛠️ Troubleshooting

### Error: Módulos no encontrados

```bash
# Asegurarse de estar en el directorio correcto
cd modeling/notebooks

# Verificar que sys.path incluye ../src
import sys
sys.path.append('../src')
```

### Error: Archivo no encontrado

Verificar que los datos procesados están en:
```
Phishing/processed_data/
├── train.csv
├── test.csv
└── CEAS_08_clean.csv
```

### Error: TF-IDF vocabulary mismatch

Asegurarse de:
1. Usar el mismo vectorizador para train y test
2. `fit_tfidf=True` en train, `fit_tfidf=False` en test

---

## 📚 Próximos Pasos

1. **Optimización de hiperparámetros**: GridSearch o RandomSearch
2. **Feature selection**: Eliminar features poco importantes
3. **Ensemble stacking**: Combinar predicciones de múltiples modelos
4. **Deep Learning**: LSTM, BERT para análisis de texto avanzado
5. **Deploy**: API REST con Flask/FastAPI para predicciones en tiempo real

---

## 👥 Autores

Proyecto creado para trabajo académico de predicción de incidentes de ciberseguridad.

---

## 📅 Fecha

Enero 2026

---

## 📄 Licencia

Uso académico y educativo.

---

**¿Preguntas o problemas?** Revisar la documentación en cada script (`feature_engineering.py`, `train.py`) o contactar al equipo.
