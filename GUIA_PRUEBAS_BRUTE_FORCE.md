# 🧪 Guía de Pruebas - Brute Force Detection

Guía paso a paso para probar la integración completa de la API de Brute Force Detection con el frontend.

## 📋 Pre-requisitos

Antes de comenzar, asegúrate de tener:

- ✅ Modelo entrenado: `fuerza-bruta/modeling/outputs/models/random_forest_20260117_021309.pkl`
- ✅ Python venv activado en: `/home/megalodon/dev/cbproy/venv`
- ✅ Node.js instalado (para el frontend)
- ✅ Puerto 8002 disponible (API)
- ✅ Puerto 5173 disponible (Frontend)

---

## 🚀 Paso 1: Iniciar la API de Brute Force

### Opción A: Script Automático (Recomendado)

```bash
cd /home/megalodon/dev/cbproy/pred_model/fuerza-bruta/modeling/api
./start.sh
```

### Opción B: Manual

```bash
cd /home/megalodon/dev/cbproy/pred_model/fuerza-bruta/modeling/api
source /home/megalodon/dev/cbproy/venv/bin/activate
python app.py
```

### ✅ Verificar que la API esté corriendo

Deberías ver en la consola:
```
🚀 Starting Brute Force Detection API...
✅ Model loaded: RandomForestClassifier
✅ Features: 60
✅ API ready to accept requests
INFO:     Uvicorn running on http://0.0.0.0:8002
```

---

## 🧪 Paso 2: Probar la API Directamente

Abre una **nueva terminal** y ejecuta estos comandos:

### 2.1 Health Check

```bash
curl http://localhost:8002/
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "message": "Brute Force Detection API",
  "model": "RandomForestClassifier",
  "version": "1.0.0"
}
```

### 2.2 Model Info

```bash
curl http://localhost:8002/model/info | python3 -m json.tool
```

**Respuesta esperada** (parcial):
```json
{
  "model_name": "RandomForestClassifier",
  "metrics": {
    "f1_score": 0.9997,
    "accuracy": 0.9997,
    "precision": 1.0000,
    "recall": 0.9994
  },
  "features": {
    "total": 60
  }
}
```

### 2.3 Predicción con Ejemplo de Brute Force

```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d @/home/megalodon/dev/cbproy/pred_model/fuerza-bruta/modeling/api/sample_flow.json
```

**Respuesta esperada:**
```json
{
  "prediction": 1,
  "prediction_label": "Brute Force",
  "confidence": 0.73,
  "probabilities": {
    "Benign": 0.27,
    "Brute Force": 0.73
  },
  "processing_time_ms": 67.24,
  "model_name": "RandomForestClassifier"
}
```

---

## 🌐 Paso 3: Iniciar el Frontend

Abre **otra terminal nueva**:

```bash
cd /home/megalodon/dev/cbproy/pred_model/frontend
npm run dev
```

**Deberías ver:**
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## 🖱️ Paso 4: Probar en el Frontend

### 4.1 Abrir el Dashboard

1. Abre tu navegador en: **http://localhost:5173**
2. Deberías ver el dashboard con 3 modelos
3. El modelo "Fuerza Bruta" ahora debería mostrar:
   - Estado: **ACTIVE** (ya no MOCK)
   - Icono: 🌐

### 4.2 Seleccionar Brute Force Detection

1. Click en la card de **"Brute Force Attack Detection"**
2. Verás el formulario de predicción

### 4.3 Modo de Prueba: Usar Ejemplos Pre-cargados

El formulario del frontend debería tener un botón **"Cargar Ejemplo"** con dos opciones:

#### Opción 1: Ejemplo de Ataque Brute Force
- Selecciona: "SSH Brute Force Attack"
- Click "Predict"
- **Resultado esperado**:
  - Predicción: ⚠️ **Ataque de Fuerza Bruta**
  - Confianza: ~73%
  - Nivel de amenaza: High/Moderate
  - Recomendaciones: Lista de acciones

#### Opción 2: Ejemplo de Tráfico Normal
- Selecciona: "Normal Web Traffic"
- Click "Predict"
- **Resultado esperado**:
  - Predicción: ✅ **Actividad Normal**
  - Confianza: ~50-80%
  - Sin amenaza

---

## 🔍 Paso 5: Verificar Logs

### 5.1 Logs de la API

En la terminal donde corre la API, deberías ver:

```
INFO: 📊 Received prediction request
INFO: ✅ Prediction: Brute Force (confidence: 0.7326)
INFO: "POST /predict HTTP/1.1" 200 OK
```

### 5.2 Logs del Frontend

En la consola del navegador (F12 → Console), deberías ver:

```
Brute Force Service: Sending prediction request
Brute Force Service: Received response from API
```

---

## ✅ Checklist de Pruebas

Marca cada ítem cuando lo hayas probado exitosamente:

### API (Terminal)
- [ ] Health check (`/`) responde OK
- [ ] Model info (`/model/info`) muestra métricas correctas
- [ ] Predicción con sample_flow.json detecta "Brute Force"
- [ ] API logs muestran requests correctamente

### Frontend (Navegador)
- [ ] Dashboard carga correctamente
- [ ] Card de Brute Force muestra status "ACTIVE"
- [ ] Formulario de predicción se abre
- [ ] Ejemplo "SSH Brute Force" predice ataque correctamente
- [ ] Ejemplo "Normal Traffic" predice benign correctamente
- [ ] Resultados muestran confianza y recomendaciones
- [ ] No hay errores en consola del navegador

---

## 🐛 Solución de Problemas

### Problema 1: API no inicia

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solución**:
```bash
# Asegúrate de usar el venv correcto
source /home/megalodon/dev/cbproy/venv/bin/activate
python app.py
```

### Problema 2: Modelo no encontrado

**Error**: `Model file not found`

**Solución**:
```bash
# Verifica que el modelo exista
ls -lh /home/megalodon/dev/cbproy/pred_model/fuerza-bruta/modeling/outputs/models/random_forest_20260117_021309.pkl

# Si no existe, ejecuta el notebook de modelado primero
```

### Problema 3: Frontend no conecta con API

**Error**: `Failed to connect to Brute Force Detection API`

**Verificar:**
1. API esté corriendo en puerto 8002
   ```bash
   curl http://localhost:8002/
   ```

2. Variable de entorno esté configurada
   ```bash
   cat frontend/.env.development | grep BRUTE_FORCE
   # Debería mostrar: VITE_BRUTE_FORCE_API_URL=http://localhost:8002
   ```

3. Reiniciar frontend después de cambiar .env
   ```bash
   # En la terminal del frontend: Ctrl+C
   npm run dev
   ```

### Problema 4: CORS Error

**Error**: `Access to fetch at 'http://localhost:8002' ... has been blocked by CORS`

**Solución**: La API ya tiene CORS habilitado para desarrollo. Verifica que la API esté corriendo correctamente.

---

## 📊 Métricas Esperadas del Modelo

Cuando pruebes la API, estos son los valores esperados:

| Métrica | Valor |
|---------|-------|
| **F1-Score** | 99.97% |
| **Accuracy** | 99.97% |
| **Precision** | 100.00% |
| **Recall** | 99.94% |
| **ROC-AUC** | 99.99% |

### Confusion Matrix (152,714 flows de test):
- True Negatives: 76,357 ✅
- False Positives: 0 ✅✅ (¡Perfecto!)
- False Negatives: 43 ⚠️
- True Positives: 76,314 ✅

---

## 🎯 Próximos Pasos

Una vez que todas las pruebas pasen:

1. ✅ Probar con diferentes ejemplos
2. ✅ Verificar tiempos de respuesta (<100ms típicamente)
3. ✅ Probar con múltiples predicciones consecutivas
4. ✅ Documentar cualquier comportamiento inesperado

---

## 📝 Notas Importantes

### Sobre el Modelo

- El modelo fue entrenado con **tráfico de red real** del dataset CSE-CIC-IDS2018
- Detecta 4 tipos de ataques: FTP, SSH, Web, XSS Brute Force
- **NO es un modelo de detección de login attempts** (por eso necesita features de red)
- En producción, este modelo se conectaría a un sistema de monitoreo de red (ej: Suricata, Zeek)

### Sobre las Features

- Las 60 features están **normalizadas entre 0 y 1**
- Son extraídas de paquetes de red usando herramientas como CICFlowMeter
- No son datos que un usuario ingrese manualmente
- Por eso el frontend usa ejemplos pre-cargados

---

## ✨ ¿Todo Funciona?

Si todas las pruebas pasan, ¡felicidades! 🎉

Tienes un sistema completo de:
- ✅ API REST funcional (puerto 8002)
- ✅ Modelo Random Forest (99.97% F1-Score)
- ✅ Frontend conectado y funcionando
- ✅ Ejemplos pre-cargados para pruebas

---

**Fecha**: 2026-01-17
**Versión API**: 1.0.0
**Modelo**: Random Forest (CSE-CIC-IDS2018)
