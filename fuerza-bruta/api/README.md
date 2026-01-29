# Brute Force Detection API

API REST para detección en tiempo real de ataques de fuerza bruta utilizando Machine Learning (Random Forest).

## 🎯 Características

- **Modelo**: Random Forest (99.97% F1-Score, 100% Precision)
- **Dataset**: CSE-CIC-IDS2018 (763,568 flows balanceados)
- **Features**: 60 características de tráfico de red normalizadas
- **Velocidad**: <10ms por predicción
- **Endpoints**: Single predict, Batch predict, Model info

## 📊 Métricas del Modelo

| Métrica | Score |
|---------|-------|
| **F1-Score** | 99.972% |
| **Accuracy** | 99.972% |
| **Precision** | **100.000%** (0 Falsos Positivos) |
| **Recall** | 99.944% |
| **ROC-AUC** | 99.999% |

**Confusion Matrix** (152,714 flows de test):
- True Negatives: 76,357 ✅
- False Positives: 0 ✅✅
- False Negatives: 43 ⚠️
- True Positives: 76,314 ✅

## 🚀 Instalación

### Usar venv compartido de cbproy

Esta API usa el entorno virtual compartido del proyecto cbproy que ya tiene todas las dependencias instaladas:

```bash
# El venv está en: /home/megalodon/dev/cbproy/venv
# No necesitas instalar nada, el script start.sh lo usa automáticamente
```

### Verificar modelo

Asegúrate de que el modelo esté en la ubicación correcta:

```bash
ls ../modeling/outputs/models/random_forest_20260117_021309.pkl
ls ../modeling/outputs/results/experiment_metadata_20260117_021309.json
```

## ▶️ Ejecución

### Opción 1: Script Automático (Recomendado)

```bash
cd fuerza-bruta/api
./start.sh
```

El script automáticamente:
- ✅ Usa el venv compartido de cbproy
- ✅ Verifica que todas las dependencias estén disponibles
- ✅ Verifica que el modelo exista
- ✅ Inicia la API en http://localhost:8002

### Opción 2: Manual

```bash
cd fuerza-bruta/api

# Activar venv compartido
source /home/megalodon/dev/cbproy/venv/bin/activate

# Iniciar API
python app.py
```

### Producción

```bash
source /home/megalodon/dev/cbproy/venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8002 --workers 4
```

La API estará disponible en:
- **API**: http://localhost:8002
- **Documentación interactiva**: http://localhost:8002/docs
- **Documentación alternativa**: http://localhost:8002/redoc

## 📚 Endpoints

### 1. Health Check

```bash
GET /
```

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Brute Force Detection API",
  "model": "RandomForestClassifier",
  "version": "1.0.0"
}
```

### 2. Predicción Individual

```bash
POST /predict
```

**Request Body (ejemplo de Brute Force):**
```json
{
  "dst_port": 0.0003,
  "protocol": 0.3529,
  "timestamp": 0.0432,
  "flow_duration": 0.0000,
  "tot_fwd_pkts": 0.0000,
  "tot_bwd_pkts": 0.0000,
  "totlen_fwd_pkts": 0.0000,
  "fwd_pkt_len_max": 0.0000,
  "fwd_pkt_len_min": 0.0000,
  "fwd_pkt_len_mean": 0.0000,
  "fwd_pkt_len_std": 0.0000,
  "bwd_pkt_len_max": 0.0000,
  "bwd_pkt_len_min": 0.0000,
  "bwd_pkt_len_mean": 0.0000,
  "bwd_pkt_len_std": 0.0000,
  "flow_byts_s": 0.0000,
  "flow_pkts_s": 0.5000,
  "flow_iat_mean": 0.0000,
  "flow_iat_std": 0.0000,
  "flow_iat_max": 0.0000,
  "fwd_iat_std": 0.0000,
  "bwd_iat_tot": 0.0000,
  "bwd_iat_mean": 0.0000,
  "bwd_iat_std": 0.0000,
  "bwd_iat_max": 0.0000,
  "bwd_iat_min": 0.0000,
  "fwd_psh_flags": 0.0000,
  "bwd_psh_flags": 0.0000,
  "fwd_urg_flags": 0.0000,
  "bwd_urg_flags": 0.0000,
  "fwd_pkts_s": 0.2500,
  "bwd_pkts_s": 0.5000,
  "pkt_len_min": 0.0000,
  "pkt_len_max": 0.0000,
  "pkt_len_mean": 0.0000,
  "pkt_len_std": 0.0000,
  "pkt_len_var": 0.0000,
  "fin_flag_cnt": 0.0000,
  "rst_flag_cnt": 0.0000,
  "psh_flag_cnt": 1.0000,
  "ack_flag_cnt": 0.0000,
  "urg_flag_cnt": 0.0000,
  "cwe_flag_count": 0.0000,
  "down_up_ratio": 0.0119,
  "fwd_byts_b_avg": 0.0000,
  "fwd_pkts_b_avg": 0.0000,
  "fwd_blk_rate_avg": 0.0000,
  "bwd_byts_b_avg": 0.0000,
  "bwd_pkts_b_avg": 0.0000,
  "bwd_blk_rate_avg": 0.0000,
  "init_fwd_win_byts": 0.4102,
  "init_bwd_win_byts": 0.0000,
  "fwd_act_data_pkts": 0.0000,
  "fwd_seg_size_min": 0.8333,
  "active_mean": 0.0000,
  "active_std": 0.0000,
  "active_max": 0.0000,
  "active_min": 0.0000,
  "idle_mean": 0.0000,
  "idle_std": 0.0000
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "prediction_label": "Brute Force",
  "confidence": 0.98,
  "probabilities": {
    "Benign": 0.02,
    "Brute Force": 0.98
  },
  "processing_time_ms": 3.45,
  "model_name": "RandomForestClassifier"
}
```

### 3. Predicción Batch

```bash
POST /predict/batch
```

**Request Body:**
```json
{
  "flows": [
    { /* flow 1 con 60 features */ },
    { /* flow 2 con 60 features */ },
    { /* flow 3 con 60 features */ }
  ]
}
```

**Respuesta:**
```json
{
  "predictions": [
    {
      "index": 0,
      "prediction": 1,
      "prediction_label": "Brute Force",
      "confidence": 0.98,
      "probabilities": {
        "Benign": 0.02,
        "Brute Force": 0.98
      }
    },
    ...
  ],
  "metadata": {
    "total_flows": 3,
    "processing_time_ms": 8.32,
    "brute_force_count": 2,
    "benign_count": 1
  }
}
```

### 4. Información del Modelo

```bash
GET /model/info
```

**Respuesta:**
```json
{
  "model_name": "RandomForestClassifier",
  "model_version": "1.0.0",
  "training_date": "2026-01-17",
  "metrics": {
    "f1_score": 0.9997,
    "accuracy": 0.9997,
    "precision": 1.0000,
    "recall": 0.9994,
    "roc_auc": 0.9999
  },
  "features": {
    "total": 60,
    "feature_names": ["Dst Port", "Protocol", ...]
  },
  "training_data": {
    "total_samples": 763568,
    "train_samples": 610854,
    "test_samples": 152714,
    "balance": {
      "Benign": 381784,
      "Brute Force": 381784
    }
  }
}
```

## 🔧 Configuración

Edita el archivo `.env` para cambiar la configuración:

```bash
# Server
HOST=0.0.0.0
PORT=8002
RELOAD=true
DEBUG=false

# Model paths
MODEL_PATH=../modeling/outputs/models/random_forest_20260117_021309.pkl
MODEL_INFO_PATH=../modeling/outputs/results/experiment_metadata_20260117_021309.json
```

## 📝 Notas Importantes

### Features Normalizadas

**IMPORTANTE**: Todas las 60 features deben estar normalizadas entre 0 y 1 usando el mismo MinMaxScaler que se usó en el entrenamiento.

### Mapeo de Features

Los nombres de campos en la API (snake_case) se mapean automáticamente a los nombres de features del modelo:

```python
"dst_port" → "Dst Port"
"flow_pkts_s" → "Flow Pkts/s"
"bwd_pkt_len_max" → "Bwd Pkt Len Max"
...
```

### Tipos de Brute Force Detectados

El modelo fue entrenado con 4 tipos de ataques de fuerza bruta del dataset CSE-CIC-IDS2018:

1. **FTP-BruteForce**: Ataques de fuerza bruta en FTP
2. **SSH-Bruteforce**: Ataques de fuerza bruta en SSH
3. **Brute Force-Web**: Ataques de fuerza bruta en aplicaciones web
4. **Brute Force-XSS**: Ataques XSS combinados con fuerza bruta

## 🧪 Testing

Prueba la API con curl:

```bash
# Health check
curl http://localhost:8002/

# Model info
curl http://localhost:8002/model/info

# Predicción (necesitas enviar las 60 features)
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d @sample_flow.json
```

O usa la documentación interactiva en http://localhost:8002/docs

## 🏗️ Arquitectura

```
api/
├── app.py              # FastAPI application
├── models.py           # Pydantic models (request/response)
├── predictor.py        # ML predictor logic
├── requirements.txt    # Python dependencies
├── .env               # Configuration
└── README.md          # This file
```

## 🔒 Características de Seguridad del Modelo

✅ **100% Precision**: No genera falsos positivos (no bloquea tráfico legítimo)
✅ **99.94% Recall**: Detecta casi todos los ataques reales
✅ **Balance perfecto**: Entrenado con 50/50 Benign/Brute Force
✅ **Sin overfitting**: Diferencia train/test < 0.01%

## 📊 Comparación con Otros Modelos

| Modelo | F1-Score | Precision | Tiempo Entrenamiento |
|--------|----------|-----------|---------------------|
| **Random Forest** ✅ | **99.972%** | **100.000%** | **29 seg** |
| Gradient Boosting | 99.994% | 99.995% | 1,431 seg (23.8 min) |
| Linear SVM | 99.881% | 99.893% | 55 seg |
| Logistic Regression | 99.835% | 99.818% | 7 seg |

**Random Forest fue elegido por**:
- 100% Precision (0 Falsos Positivos)
- Excelente F1-Score (99.97%)
- 49x más rápido que Gradient Boosting para re-entrenamiento
- Mismo rendimiento en producción

## 📞 Soporte

Para problemas o preguntas, revisa los logs en consola o contacta al equipo de desarrollo.

---

**Última actualización**: 2026-01-17
**Versión API**: 1.0.0
**Modelo**: Random Forest (CSE-CIC-IDS2018)
