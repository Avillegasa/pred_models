# Account Takeover Detection API

API REST para detección en tiempo real de Account Takeover (ATO) usando Machine Learning.

## 📋 Características

- **Modelo**: Gradient Boosting (F1-Score: 0.7416, Recall: 0.7857)
- **Threshold Óptimo**: 0.0041 (ajustado para máximo F1-Score)
- **Features**: 35 features (temporal, behavioral, aggregated, categorical)
- **Endpoints**: `/predict`, `/predict/batch`, `/model/info`, `/health`

## 🚀 Instalación

### 1. Instalar dependencias

```bash
cd Suspicious-Login-Activity/modeling/api
pip install -r requirements.txt
```

O si usas un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Verificar archivos del modelo

Asegúrate de que estos archivos existan:

```bash
ls -la ../outputs/models/gradient_boosting.pkl
ls -la ../outputs/features/label_encoders.pkl
ls -la ../outputs/models/model_info.json
```

**IMPORTANTE**: Si no ejecutaste las celdas finales del notebook que guardan el threshold óptimo, crea el archivo manualmente ejecutando esta celda en el notebook:

```python
# Guardar threshold óptimo
if y_pred_proba is not None and 'optimal_threshold' in locals():
    threshold_info = {
        'optimal_threshold': float(optimal_threshold),
        'default_threshold': 0.5,
        'f1_default': float(f1_default),
        'f1_tuned': float(f1_tuned),
        'improvement_pct': float((f1_tuned - f1_default)/f1_default*100),
        'metrics_with_optimal': {
            'accuracy': float(metrics_tuned['accuracy']),
            'precision': float(metrics_tuned['precision']),
            'recall': float(metrics_tuned['recall']),
            'f1_score': float(metrics_tuned['f1_score'])
        }
    }

    threshold_path = f'{OUTPUT_DIR}/models/optimal_threshold.pkl'
    joblib.dump(threshold_info, threshold_path)
    print(f"✅ Threshold óptimo guardado: {threshold_path}")
```

### 3. Configurar variables de entorno (opcional)

Copia el archivo de ejemplo y edítalo según tus necesidades:

```bash
cp .env.example .env
# Editar .env si necesitas cambiar rutas o puerto
```

## 🏃 Ejecución

### Opción 1: Uvicorn directo (recomendado para desarrollo)

```bash
cd Suspicious-Login-Activity/modeling/api
uvicorn app:app --port 8001 --reload
```

### Opción 2: Python directo

```bash
cd Suspicious-Login-Activity/modeling/api
python3 app.py
```

### Opción 3: Ejecutar en background

```bash
cd Suspicious-Login-Activity/modeling/api
nohup uvicorn app:app --port 8001 > api.log 2>&1 &
```

## 📚 Documentación de la API

Una vez iniciada la API, accede a:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/

## 🔗 Endpoints

### 1. Health Check

```bash
GET /
```

Verifica que la API esté funcionando y el modelo cargado.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Account Takeover Detection API",
  "model": "Gradient Boosting",
  "version": "1.0.0"
}
```

### 2. Predicción Individual

```bash
POST /predict
Content-Type: application/json

{
  "user_id": "user123",
  "ip_address": "89.46.23.10",
  "country": "RO",
  "region": "Bucharest",
  "city": "Bucharest",
  "browser": "Chrome 120.0",
  "os": "Windows 10",
  "device": "Desktop",
  "login_successful": 1,
  "is_attack_ip": 1,
  "asn": 9050,
  "rtt": 673.2,
  "login_timestamp": "2026-01-15T10:30:00Z"
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "prediction_label": "Account Takeover",
  "confidence": 0.8521,
  "probability_normal": 0.1479,
  "probability_ato": 0.8521,
  "risk_score": 85.21,
  "metadata": {
    "model": "Gradient Boosting",
    "features_count": 35,
    "threshold": 0.0041,
    "timestamp": "2026-01-15T15:30:45.123Z",
    "processing_time_ms": 12.5
  }
}
```

### 3. Predicción en Batch

```bash
POST /predict/batch
Content-Type: application/json

{
  "logins": [
    {
      "user_id": "user123",
      "ip_address": "192.168.1.100",
      "country": "US",
      ...
    },
    {
      "user_id": "user456",
      "ip_address": "89.46.23.10",
      "country": "RO",
      ...
    }
  ]
}
```

### 4. Información del Modelo

```bash
GET /model/info
```

Devuelve información detallada sobre el modelo: métricas, features, datos de entrenamiento, threshold.

## 🧪 Pruebas

### Curl (Normal Login)

```bash
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "ip_address": "192.168.1.100",
    "country": "US",
    "region": "California",
    "city": "San Francisco",
    "browser": "Chrome 120.0",
    "os": "Windows 10",
    "device": "Desktop",
    "login_successful": 1,
    "is_attack_ip": 0,
    "asn": 15169,
    "rtt": 45.5
  }'
```

### Curl (Account Takeover)

```bash
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456",
    "ip_address": "89.46.23.10",
    "country": "RO",
    "region": "Bucharest",
    "city": "Bucharest",
    "browser": "Firefox 115.0",
    "os": "Linux",
    "device": "Desktop",
    "login_successful": 1,
    "is_attack_ip": 1,
    "asn": 9050,
    "rtt": 673.2
  }'
```

## 📊 Features del Modelo

### Temporal (7 features)
- `hour`, `day_of_week`, `is_weekend`, `is_night`, `is_business_hours`

### Behavioral (8 features)
- `ip_changed`, `country_changed`, `browser_changed`, `device_changed`, `os_changed`
- `time_since_last_login_hours`

### Aggregated (10 features)
- `ip_count_per_user`, `country_count_per_user`, `success_rate_per_user`
- `user_count_per_ip`, `is_suspicious_ip`, `rtt_zscore`, `is_abnormal_rtt`

### Numeric (4 features)
- `Round-Trip Time (RTT) (ms)`, `ASN`, `Login Successful`, `Is Attack IP`

### Categorical Encoded (6 features)
- `Browser Name and Version`, `OS Name and Version`, `Device Type`
- `Country`, `Region`, `City`

## ⚙️ Configuración

Variables de entorno en `.env`:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host del servidor |
| `PORT` | `8001` | Puerto del servidor |
| `RELOAD` | `true` | Auto-reload en desarrollo |
| `DEBUG` | `false` | Modo debug |
| `MODEL_PATH` | `../outputs/models/gradient_boosting.pkl` | Ruta al modelo |
| `ENCODERS_PATH` | `../outputs/features/label_encoders.pkl` | Ruta a encoders |
| `THRESHOLD_PATH` | `../outputs/models/optimal_threshold.pkl` | Ruta a threshold |
| `MODEL_INFO_PATH` | `../outputs/models/model_info.json` | Ruta a metadata |

## 🔧 Troubleshooting

### Error: "Model file not found"

Verifica que ejecutaste el notebook de entrenamiento y los archivos se guardaron correctamente:

```bash
ls -la ../outputs/models/
ls -la ../outputs/features/
```

### Error: "No module named 'uvicorn'"

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Puerto 8001 ya en uso

Cambia el puerto en `.env` o usa:

```bash
uvicorn app:app --port 8002 --reload
```

### Threshold file not found

Si el archivo `optimal_threshold.pkl` no existe, la API usará threshold 0.5 por defecto. Para usar el threshold óptimo, ejecuta la celda correspondiente en el notebook de entrenamiento.

## 🌐 Integración con Frontend

El frontend ya tiene el servicio mock implementado en:
```
frontend/src/services/ataquesSospechososService.js
```

Para conectar con la API real, edita el archivo y cambia la URL base a:
```javascript
const API_URL = 'http://localhost:8001';
```

## 📝 Logs

Los logs se muestran en la consola con formato:
```
2026-01-15 15:30:45 - __main__ - INFO - 🚀 Starting Account Takeover Detection API...
2026-01-15 15:30:46 - __main__ - INFO - ✅ Model loaded: Gradient Boosting
2026-01-15 15:30:46 - __main__ - INFO - ✅ Features: 35
2026-01-15 15:30:46 - __main__ - INFO - ✅ Threshold: 0.0041
2026-01-15 15:30:46 - __main__ - INFO - ✅ API ready to accept requests
```

## 🎯 Próximos Pasos

1. ✅ API creada y documentada
2. 🔜 Conectar frontend con API real
3. 🔜 Probar end-to-end con dashboard
4. 🔜 Implementar caché Redis para user history (producción)
5. 🔜 Implementar rate limiting (producción)

---

**Última Actualización**: 2026-01-15
