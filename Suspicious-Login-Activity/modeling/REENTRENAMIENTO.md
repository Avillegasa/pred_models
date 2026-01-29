# 🔄 Re-entrenar Modelo con Versiones Correctas

## ⚠️ PROBLEMA

El modelo fue entrenado con versiones de librerías más nuevas que las usadas en la API:
- Notebook: numpy 2.4.0, scikit-learn 1.8.0, etc.
- API: numpy >=1.24.0, scikit-learn >=1.3.0 (versiones de Phishing)

Esto causa errores de pickle/compatibilidad al cargar el modelo.

## ✅ SOLUCIÓN

Re-entrenar el modelo usando el MISMO entorno virtual que la API.

## 📋 PASOS

### 1. Activar el entorno virtual correcto

```bash
cd /home/megalodon/dev/cbproy
source venv/bin/activate
```

### 2. Abrir Jupyter Notebook con el venv activado

```bash
cd /home/megalodon/dev/cbproy/pred_model/Suspicious-Login-Activity/modeling/notebooks
jupyter notebook
```

### 3. Seleccionar el kernel correcto

En Jupyter:
- **Kernel** → **Change Kernel** → Selecciona el kernel que usa tu venv
- O crea un nuevo kernel: `python -m ipykernel install --user --name=venv --display-name="Python (venv)"`

### 4. Verificar versiones ANTES de entrenar

Ejecuta esta celda al inicio del notebook:

```python
import pandas as pd
import numpy as np
import sklearn
import joblib

print("✅ Versiones instaladas:")
print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print(f"joblib: {joblib.__version__}")

# Verificar que son compatibles con la API
assert pd.__version__ >= "2.0.0", "pandas version too old"
assert np.__version__ >= "1.24.0", "numpy version too old"
assert sklearn.__version__ >= "1.3.0", "scikit-learn version too old"
assert joblib.__version__ >= "1.3.0", "joblib version too old"

print("\n✅ Todas las versiones son compatibles con la API")
```

### 5. Ejecutar el notebook completo

- **Kernel** → **Restart & Run All**
- Espera 15-30 minutos
- Verifica que se guardan estos archivos:
  - `outputs/models/gradient_boosting.pkl`
  - `outputs/features/label_encoders.pkl`
  - `outputs/models/model_info.json`
  - `outputs/models/optimal_threshold.pkl`

### 6. Verificar que se guardaron correctamente

```bash
ls -lh outputs/models/
ls -lh outputs/features/
```

Deberías ver:
- `gradient_boosting.pkl` (~1-2 MB)
- `label_encoders.pkl` (~80 KB)
- `model_info.json` (~2-3 KB)
- `optimal_threshold.pkl` (~1 KB)

### 7. Probar la API

```bash
cd ../../api
uvicorn app:app --port 8001 --reload
```

Debería iniciar SIN ERRORES:

```
🚀 Starting Account Takeover Detection API...
🔧 Initializing AccountTakeoverPredictor...
📦 Loading model from: .../gradient_boosting.pkl
📦 Loading encoders from: .../label_encoders.pkl
✅ Model loaded: Gradient Boosting
✅ Features: 35
✅ Threshold: 0.5 (o 0.0041 si guardaste optimal_threshold.pkl)
✅ API ready to accept requests
```

## 🎯 RESUMEN

1. ✅ Activar venv con versiones de Phishing
2. ✅ Abrir Jupyter con ese venv
3. ✅ Verificar versiones al inicio
4. ✅ Ejecutar Restart & Run All
5. ✅ Verificar archivos guardados
6. ✅ Probar API

## ⚠️ IMPORTANTE

**NO instales librerías adicionales en el notebook**. Usa solo las que ya están en el venv con las versiones de Phishing.

Si necesitas instalar algo:
```bash
# Agregar al requirements.txt de la API primero
# Luego instalar en el venv
pip install nombre_paquete
```

---

**Tiempo estimado**: 20-35 minutos (incluyendo re-entrenamiento)
