# 🚀 Quick Start - Account Takeover Detection API

## ⚠️ IMPORTANTE: Versión de scikit-learn

El modelo fue entrenado con **scikit-learn 1.8.0**. Debes usar la misma versión o superior.

## 🔧 Solución al Error "No module named '_loss'"

Este error ocurre cuando hay incompatibilidad de versiones de scikit-learn.

### Paso 1: Detener el servidor

Si está corriendo, presiona `CTRL+C`

### Paso 2: Actualizar scikit-learn

```bash
# Asegúrate de estar en el entorno virtual
pip install --upgrade scikit-learn

# Verificar versión (debe ser >= 1.8.0)
python3 -c "import sklearn; print(sklearn.__version__)"
```

### Paso 3: Reiniciar la API

```bash
cd Suspicious-Login-Activity/modeling/api
uvicorn app:app --port 8001 --reload
```

## ✅ Verificación Rápida

Una vez iniciada, prueba:

```bash
# Health check
curl http://localhost:8001/

# Debe retornar:
# {"status":"ok","message":"Account Takeover Detection API","model":"Gradient Boosting","version":"1.0.0"}
```

## 🧪 Prueba de Predicción

```bash
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
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
    "rtt": 673.2
  }'
```

Debería retornar `"prediction_label": "Account Takeover"` con risk_score alto.

## 📚 Documentación Completa

Una vez corriendo, visita: http://localhost:8001/docs

## ❓ Problemas Comunes

### Error: "Model file not found"

Verifica que el modelo existe:
```bash
ls -la ../outputs/models/gradient_boosting.pkl
```

### Error: "Encoders file not found"

Verifica que los encoders existen:
```bash
ls -la ../outputs/features/label_encoders.pkl
```

### Warnings de Pydantic

Los warnings sobre `model_` namespace ya están solucionados. Si aún aparecen, actualiza pydantic:
```bash
pip install --upgrade pydantic
```
