# 🧪 Instrucciones para Probar Account Takeover Detection

## 📋 CHECKLIST DE LO QUE YA ESTÁ HECHO

- ✅ Modelo entrenado (Gradient Boosting, F1=0.7416)
- ✅ API corriendo en puerto 8001
- ✅ Service layer actualizado (`ataquesSospechososService.js`)
- ✅ Model metadata actualizado (`modelService.js` - status: 'active')
- ✅ Form component actualizado (`AtaquesSospechososForm.jsx`)

---

## 🚀 CÓMO VER LOS CAMBIOS

### 1. Reiniciar el Frontend

Desde la terminal donde corre el frontend (puerto 5173):

```bash
# 1. Detener el servidor (CTRL + C)

# 2. Limpiar cache de Vite (opcional pero recomendado)
rm -rf node_modules/.vite

# 3. Reiniciar
npm run dev
```

### 2. Refrescar el Navegador

Una vez que el servidor arranque:

```bash
# Abre el navegador en: http://localhost:5173
```

Luego haz **Hard Reload**:
- **Windows/Linux**: `CTRL + Shift + R`
- **Mac**: `Cmd + Shift + R`

O borra cache manualmente:
- F12 (DevTools) → Network tab → Check "Disable cache"
- F12 → Application → Clear storage → Clear site data

---

## ✅ QUÉ DEBERÍAS VER AHORA

### En el Dashboard:

Busca la sección de **"Account Takeover Detection"** o **"Logins Sospechosos"**:

1. ✅ **Badge**: Muestra **"ACTIVE"** (en verde, no "MOCK")
2. ✅ **Título**: "Account Takeover Detection"
3. ✅ **Icono**: 🔐
4. ✅ **Campos del formulario**:
   - User ID
   - IP Address
   - Country (2 caracteres)
   - Region
   - City
   - Browser
   - Operating System
   - Device Type (dropdown: Desktop/Mobile/Tablet)
   - ASN (número)
   - RTT (ms) (número con decimales)
   - Login Successful (checkbox)
   - Is Attack IP (checkbox)

5. ✅ **Botones de ejemplo**:
   - 📋 Load Normal Example
   - 🚨 Load ATO Example

### ❌ Lo que YA NO deberías ver:

- ❌ "Suspicious Network Attack Detection"
- ❌ Badge "MOCK"
- ❌ Campos: Source IP, Target Port, Protocol, Packet Count, Payload

---

## 🧪 PROBAR LAS PREDICCIONES

### Opción 1: Usar los botones de ejemplo (Rápido)

1. Click en **"📋 Load Normal Example"**
2. Click en **"Predict"**
3. Deberías ver:
   - Risk Score: ~5-15%
   - Prediction: "Login Normal"
   - Confidence: Alta

4. Click en **"🚨 Load ATO Example"**
5. Click en **"Predict"**
6. Deberías ver:
   - Risk Score: ~70-95%
   - Prediction: "Login Sospechoso"
   - Confidence: Alta

### Opción 2: Ingresar manualmente

#### Ejemplo Normal:
```
User ID: user123
IP Address: 192.168.1.100
Country: US
Region: California
City: San Francisco
Browser: Chrome 120.0
OS: Windows 10
Device: Desktop
Login Successful: ✓ (checked)
Is Attack IP: ☐ (unchecked)
ASN: 15169
RTT: 45.5
```

**Resultado esperado**: Risk Score bajo (~5-15%)

#### Ejemplo ATO:
```
User ID: user456
IP Address: 89.46.23.10
Country: RO
Region: Bucharest
City: Bucharest
Browser: Firefox 115.0
OS: Linux
Device: Desktop
Login Successful: ✓ (checked)
Is Attack IP: ✓ (checked)
ASN: 9050
RTT: 673.2
```

**Resultado esperado**: Risk Score alto (~70-95%)

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### 1. Abrir DevTools (F12)

Ve a la consola y verifica:

✅ **Sin errores de red**:
- No debería haber errores 404 o CORS
- Llamadas a `http://localhost:8001/predict` deberían ser **200 OK**

✅ **Logs esperados**:
```
Prediction success: {prediction: 0, prediction_label: "Login Normal", ...}
```

### 2. Verificar la Respuesta de la API

En DevTools → Network → Click en la request `/predict`:

```json
{
  "prediction": 0,
  "prediction_label": "Normal Login",
  "confidence": 0.95,
  "probability_normal": 0.95,
  "probability_ato": 0.05,
  "risk_score": 5.0,
  "metadata": {
    "model": "Gradient Boosting",
    "features_count": 35,
    "threshold": 0.5,
    "processing_time_ms": 15
  }
}
```

---

## 🐛 SI TIENES PROBLEMAS

### Problema 1: No veo los cambios

**Solución**:
```bash
# 1. Detener frontend (CTRL+C)
# 2. Limpiar cache
rm -rf node_modules/.vite
# 3. Reiniciar
npm run dev
# 4. Hard reload en navegador (CTRL+Shift+R)
```

### Problema 2: Error "API no disponible"

**Causa**: API de Account Takeover no está corriendo en puerto 8001

**Solución**:
```bash
# En otra terminal:
cd Suspicious-Login-Activity/modeling/api
source /home/megalodon/dev/cbproy/venv/bin/activate
uvicorn app:app --port 8001 --reload
```

Verifica que esté corriendo:
```bash
curl http://localhost:8001/
```

### Problema 3: Error de CORS

**Causa**: API no tiene CORS habilitado

**Solución**: La API ya tiene CORS configurado en `app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Si persiste, reinicia la API.

### Problema 4: Campos del formulario no coinciden

**Causa**: Cache del navegador

**Solución**:
- F12 → Application → Clear storage → Clear site data
- O usa modo incógnito

---

## 📊 INFORMACIÓN DEL MODELO

Si quieres ver los detalles del modelo:

```bash
curl http://localhost:8001/model/info | jq
```

Deberías ver:
```json
{
  "model_name": "Gradient Boosting",
  "model_version": "1.0.0",
  "training_date": "2026-01-16",
  "metrics": {
    "f1_score": 0.7416,
    "accuracy": 0.9998,
    "precision": 0.7941,
    "recall": 0.6970,
    "roc_auc": 0.9896,
    "auc_pr": 0.8509
  },
  "features": {
    "total": 35,
    "temporal": 11,
    "behavioral": 9,
    "aggregated": 10,
    "categorical": 6
  }
}
```

---

## ✅ CHECKLIST FINAL

Antes de cerrar, verifica:

- [ ] Frontend corriendo en puerto 5173
- [ ] API corriendo en puerto 8001
- [ ] Formulario muestra "Account Takeover Detection" con badge "ACTIVE"
- [ ] Campos correctos (User ID, IP, Country, etc.)
- [ ] Botones de ejemplo funcionan
- [ ] Predicción normal retorna Risk Score bajo
- [ ] Predicción ATO retorna Risk Score alto
- [ ] Sin errores en consola del navegador
- [ ] Respuesta de API tiene formato correcto

---

**Última Actualización**: 2026-01-16
