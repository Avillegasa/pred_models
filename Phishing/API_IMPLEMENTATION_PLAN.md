# Plan de Implementación: API REST para Detección de Phishing

**Status**: 📋 **PLAN APROBADO** - Listo para implementar
**Fecha**: 2026-01-10
**Modelo a usar**: Gradient Boosting (99.09% F1-Score)

---

## 🎯 Objetivo

Crear un endpoint REST API usando **FastAPI** que permita:
- Enviar emails via **Postman** (o cualquier cliente HTTP)
- Recibir predicciones de phishing en tiempo real
- Usar el modelo Gradient Boosting entrenado (best_model.pkl)

---

## 🏗️ Arquitectura

### Tecnología: FastAPI
**Ventajas:**
- ✅ Validación automática con Pydantic
- ✅ Documentación automática (Swagger UI en `/docs`)
- ✅ Async support
- ✅ Rápido y moderno
- ✅ Fácil testing con Postman

### Estructura de Directorios
```
Phishing/modeling/
└── api/
    ├── app.py                  # Aplicación FastAPI principal
    ├── models.py               # Modelos Pydantic (request/response)
    ├── predictor.py            # Lógica de predicción encapsulada
    ├── requirements.txt        # Dependencias de la API
    ├── test_api.py             # Script de testing
    ├── .env.example            # Variables de entorno ejemplo
    └── README.md               # Documentación de uso
```

---

## 📡 Endpoints a Implementar

### 1. `GET /` - Health Check
Verificar que la API está funcionando.

**Response:**
```json
{
  "status": "ok",
  "message": "Phishing Detection API",
  "model": "Gradient Boosting",
  "version": "1.0.0"
}
```

---

### 2. `POST /predict` - Predicción Principal
Predecir si un email es phishing o legítimo.

**Request:**
```json
{
  "sender": "user@example.com",
  "receiver": "admin@company.com",
  "subject": "Urgent: Verify your account",
  "body": "Click here to verify your account...",
  "urls": 1
}
```

**Campos:**
- `sender` (requerido): Email del remitente
- `receiver` (opcional): Email del destinatario
- `subject` (requerido): Asunto del email
- `body` (requerido): Cuerpo del email
- `urls` (opcional): 0 o 1, indica presencia de URLs (default: 0)

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Phishing",
  "confidence": 0.9927,
  "probability_legitimate": 0.0073,
  "probability_phishing": 0.9927,
  "metadata": {
    "model": "Gradient Boosting",
    "features_count": 1016,
    "timestamp": "2026-01-10T15:30:45.123Z",
    "processing_time_ms": 45.2
  }
}
```

**Interpretación:**
- `prediction`: 0 = Legítimo, 1 = Phishing
- `confidence`: Probabilidad del resultado predicho (0.0 - 1.0)
- `probability_phishing`: Probabilidad específica de ser phishing

---

### 3. `POST /predict/batch` - Predicción en Lote (Opcional)
Predecir múltiples emails en una sola request.

**Request:**
```json
{
  "emails": [
    {
      "sender": "user1@example.com",
      "subject": "Meeting tomorrow",
      "body": "Let's meet at 10am"
    },
    {
      "sender": "scam@phishing.com",
      "subject": "You won $1M!",
      "body": "Click here to claim..."
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "email_index": 0,
      "prediction": 0,
      "prediction_label": "Legitimate",
      "confidence": 0.9856
    },
    {
      "email_index": 1,
      "prediction": 1,
      "prediction_label": "Phishing",
      "confidence": 0.9943
    }
  ],
  "metadata": {
    "total_emails": 2,
    "processing_time_ms": 78.5
  }
}
```

---

### 4. `GET /model/info` - Información del Modelo
Obtener métricas y detalles del modelo en uso.

**Response:**
```json
{
  "model_name": "Gradient Boosting",
  "model_version": "1.0.0",
  "training_date": "2026-01-10",
  "metrics": {
    "f1_score": 0.9909,
    "accuracy": 0.9898,
    "precision": 0.9891,
    "recall": 0.9927,
    "roc_auc": 0.9990
  },
  "features": {
    "total": 1016,
    "tfidf": 1000,
    "numeric": 16
  },
  "training_data": {
    "total_samples": 39154,
    "train_samples": 31323,
    "test_samples": 7831
  }
}
```

---

## 📁 Archivos a Crear

### Orden de Implementación:

#### 1. `api/requirements.txt`
Dependencias necesarias para la API.

```txt
# Core ML
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
joblib>=1.3.0

# API Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6

# Utilities
python-dotenv>=1.0.0
```

---

#### 2. `api/models.py`
Modelos Pydantic para validación de request/response.

**Clases principales:**
- `EmailInput`: Esquema de entrada para un email
- `PredictionResponse`: Esquema de respuesta con predicción
- `BatchEmailInput`: Esquema para múltiples emails
- `HealthResponse`: Esquema para health check

**Validaciones:**
- `sender`, `subject`, `body` → Requeridos
- `receiver` → Opcional
- `urls` → Opcional (0 o 1, default 0)

---

#### 3. `api/predictor.py`
Lógica de predicción encapsulada.

**Clase `PhishingPredictor`:**

```python
class PhishingPredictor:
    def __init__(self, model_path, vectorizer_path):
        # Cargar modelo y vectorizer al inicializar

    def predict_single(self, email_data: dict) -> dict:
        # Predecir un solo email
        # 1. Crear DataFrame
        # 2. Feature engineering (usando vectorizer cargado)
        # 3. Predicción
        # 4. Formatear respuesta

    def predict_batch(self, emails: list[dict]) -> list[dict]:
        # Predecir múltiples emails
```

**Importante:**
- Usa `engineer_features()` con `fit_tfidf=False`
- Siempre usar el vectorizer cargado, no crear uno nuevo
- Retorna diccionario con prediction, confidence, etc.

---

#### 4. `api/app.py`
Aplicación FastAPI principal.

**Funciones clave:**
```python
@app.on_event("startup")
async def startup_event():
    # Cargar modelo y vectorizer una sola vez al iniciar

@app.get("/")
async def health_check():
    # Health check básico

@app.post("/predict")
async def predict_email(email: EmailInput):
    # Predicción principal

@app.post("/predict/batch")
async def predict_batch(batch: BatchEmailInput):
    # Predicción en lote

@app.get("/model/info")
async def model_info():
    # Información del modelo
```

**Características:**
- CORS habilitado para desarrollo
- Manejo de errores global
- Logging de requests
- Tiempos de procesamiento

---

#### 5. `api/.env.example`
Variables de entorno de ejemplo.

```env
# Rutas a modelos (relativas desde api/)
MODEL_PATH=../outputs/models/best_model.pkl
VECTORIZER_PATH=../outputs/features/tfidf_vectorizer.pkl
MODEL_INFO_PATH=../outputs/models/model_info.json

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Logging
LOG_LEVEL=INFO
```

---

#### 6. `api/test_api.py`
Tests automatizados.

**Tests a implementar:**
1. Health check (`GET /`)
2. Predicción de email legítimo
3. Predicción de email phishing
4. Batch prediction
5. Request con campos faltantes (error 422)
6. Request con formato incorrecto

---

#### 7. `api/README.md`
Documentación completa de la API.

**Secciones:**
- Descripción
- Instalación
- Cómo ejecutar
- Endpoints disponibles
- Ejemplos con curl y Postman
- Testing
- Troubleshooting

---

## 🔄 Flujo de Ejecución

### Startup (Una vez):
```
1. FastAPI inicia
2. Cargar best_model.pkl (371KB) → Memoria
3. Cargar tfidf_vectorizer.pkl → Memoria
4. Cargar model_info.json → Metadata
5. API lista para recibir requests ✅
```

### Por Request (`POST /predict`):
```
1. Recibir JSON con email data
2. Validar con Pydantic (campos requeridos)
3. Crear DataFrame de 1 fila
4. Feature engineering (1,016 features):
   - Features de texto (6)
   - Metadata (2)
   - Sentiment (2)
   - Features derivadas (5)
   - Domain encoding (1)
   - TF-IDF transform (1,000) ← Usa vectorizer cargado
5. Extraer X (1,016 features)
6. model.predict(X) → 0 o 1
7. model.predict_proba(X) → [prob_legit, prob_phish]
8. Formatear respuesta JSON
9. Retornar con código 200
```

**Tiempo estimado:** ~50-100ms por predicción

---

## ⚠️ Puntos Críticos

### 1. TF-IDF Vectorizer
**MUY IMPORTANTE:**
- Usar el vectorizer guardado (`tfidf_vectorizer.pkl`)
- **NUNCA** crear un nuevo vectorizer
- Siempre `fit_tfidf=False` en predicciones
- Si se crea nuevo, las features serán incompatibles con el modelo

### 2. Feature Engineering
```python
from src.features.feature_engineering import engineer_features

features_df, _ = engineer_features(
    df,
    tfidf_vectorizer=loaded_vectorizer,  # ← Vectorizer cargado
    fit_tfidf=False,  # ← CRÍTICO: solo transform
    config=None
)
```

### 3. Rutas de Archivos
```
Modelo: ../outputs/models/best_model.pkl
Vectorizer: ../outputs/features/tfidf_vectorizer.pkl
Feature Engineering: ../src/features/feature_engineering.py
```

Todas relativas desde `Phishing/modeling/api/`

---

## 🧪 Testing con Postman

### Setup:
1. Crear colección "Phishing Detection API"
2. Crear environment con variable: `base_url = http://localhost:8000`

### Tests de Ejemplo:

**Test 1: Health Check**
```
GET {{base_url}}/
```

**Test 2: Email Legítimo**
```
POST {{base_url}}/predict
Content-Type: application/json

{
  "sender": "boss@company.com",
  "receiver": "employee@company.com",
  "subject": "Meeting tomorrow at 10am",
  "body": "Hi team, let's discuss the project tomorrow at 10am in room 305.",
  "urls": 0
}
```

**Resultado esperado:** `prediction: 0` (Legitimate)

**Test 3: Email Phishing**
```
POST {{base_url}}/predict
Content-Type: application/json

{
  "sender": "urgent@suspicious.com",
  "receiver": "victim@example.com",
  "subject": "URGENT: Verify your account NOW",
  "body": "Your account will be suspended. Click here immediately to verify: http://phishing-site.com",
  "urls": 1
}
```

**Resultado esperado:** `prediction: 1` (Phishing)

**Test 4: Campo Faltante (Error)**
```
POST {{base_url}}/predict
Content-Type: application/json

{
  "sender": "test@example.com"
}
```

**Resultado esperado:** Error 422 (Validation Error)

---

## 🚀 Cómo Ejecutar

### Instalación:
```bash
cd /home/megalodon/dev/cbproy/datasets_v3/Phishing/modeling/api
pip install -r requirements.txt
```

### Desarrollo (con auto-reload):
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Producción:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceso:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

---

## ✅ Verificación End-to-End

### Paso 1: Instalar dependencias
```bash
cd Phishing/modeling/api
pip install -r requirements.txt
```

### Paso 2: Iniciar servidor
```bash
uvicorn app:app --reload
```

**Output esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Paso 3: Test health check
```bash
curl http://localhost:8000/
```

**Respuesta esperada:**
```json
{"status": "ok", "message": "Phishing Detection API", ...}
```

### Paso 4: Test predicción con Postman
1. Abrir Postman
2. POST `http://localhost:8000/predict`
3. Body → raw → JSON
4. Enviar email de prueba
5. Verificar respuesta con `prediction` y `confidence`

### Paso 5: Ver documentación
Abrir navegador: http://localhost:8000/docs

### Paso 6: Run tests automatizados
```bash
python test_api.py
```

**Esperado:** All tests pass ✅

---

## 📊 Manejo de Errores

### 400 Bad Request
- Campos requeridos faltantes
- Formato incorrecto

### 422 Unprocessable Entity
- Validación de Pydantic falla
- Tipos de datos incorrectos

### 500 Internal Server Error
- Error en feature engineering
- Error en predicción del modelo
- Modelo o vectorizer no cargados

**Formato de error:**
```json
{
  "error": "Bad Request",
  "message": "Campo 'subject' es requerido",
  "details": {...}
}
```

---

## 📝 Estado Actual

- ✅ **Plan aprobado** (2026-01-10)
- ✅ Modelo entrenado disponible (Gradient Boosting, 99.09% F1)
- ✅ Vectorizer guardado
- ✅ Feature engineering disponible
- 📋 **Pendiente**: Implementación de la API (7 archivos)

---

## 🔜 Siguiente Paso

**Implementar en orden:**
1. Crear directorio `api/`
2. `requirements.txt`
3. `models.py`
4. `predictor.py`
5. `app.py`
6. `.env.example`
7. `test_api.py`
8. `README.md`

**Luego:** Ejecutar y probar con Postman

---

**Modelo listo para deployment via API REST** 🚀
