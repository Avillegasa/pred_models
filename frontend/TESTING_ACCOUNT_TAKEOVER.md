# 🧪 Testing Account Takeover Detection

## ✅ COMPLETADO

El frontend ahora está conectado a la API REAL de Account Takeover (puerto 8001).

## 🚀 CÓMO PROBAR

### 1. Iniciar las APIs

Necesitas **2 terminales**:

#### Terminal 1: API de Phishing (puerto 8000)
```bash
cd Phishing/modeling/api
source /home/megalodon/dev/cbproy/venv/bin/activate
uvicorn app:app --reload
```

#### Terminal 2: API de Account Takeover (puerto 8001)
```bash
cd Suspicious-Login-Activity/modeling/api
source /home/megalodon/dev/cbproy/venv/bin/activate
uvicorn app:app --port 8001 --reload
```

### 2. Iniciar el Frontend

#### Terminal 3: Frontend React
```bash
cd frontend
npm run dev
```

Abre: **http://localhost:5173**

### 3. Probar Account Takeover

En el dashboard:

1. Busca la sección **"Logins Sospechosos"** o **"Account Takeover Detection"**
2. Debería mostrar status: **ACTIVE** (no "MOCK")
3. Ingresa datos de login para probar

#### Ejemplo de Login Normal (bajo riesgo):
```
User ID: user123
IP Address: 192.168.1.100
Country: US
Region: California
City: San Francisco
Browser: Chrome 120.0
OS: Windows 10
Device: Desktop
Login Successful: Yes (1)
Is Attack IP: No (0)
ASN: 15169
RTT: 45.5
```

**Resultado esperado**: Risk Score ~5-15%, "Login Normal"

#### Ejemplo de Account Takeover (alto riesgo):
```
User ID: user456
IP Address: 89.46.23.10
Country: RO
Region: Bucharest
City: Bucharest
Browser: Firefox 115.0
OS: Linux
Device: Desktop
Login Successful: Yes (1)
Is Attack IP: Yes (1)
ASN: 9050
RTT: 673.2
```

**Resultado esperado**: Risk Score ~80-95%, "Login Sospechoso"

## 🔍 VERIFICAR INTEGRACIÓN

### Indicadores de que funciona correctamente:

1. ✅ **Status Badge**: Muestra "ACTIVE" en verde (no "MOCK")
2. ✅ **Nombre**: "Account Takeover Detection" o "Logins Sospechosos"
3. ✅ **Icono**: 🔐 (candado)
4. ✅ **Respuesta real**: Incluye `risk_score`, `severity`, `threshold` en metadata
5. ✅ **Tiempo de respuesta**: ~10-50ms (no ~700-900ms como el mock)
6. ✅ **Modelo**: "Gradient Boosting" (no "Network Intrusion Detection (Mock)")

### Consola del navegador:

Abre DevTools (F12) → Console:

- ✅ No debería haber errores de red
- ✅ Las llamadas a `http://localhost:8001/predict` deberían ser 200 OK
- ✅ Ver logs: "Account Takeover API..." si hay errores

### Si ves errores de red:

```
Error: No se pudo conectar con la API. Verifica que el servidor esté corriendo en http://localhost:8001
```

**Solución**: Verifica que la API de Account Takeover esté corriendo en puerto 8001.

## 📊 MODELO INFO

En el dashboard, busca "Model Info" o "Información del Modelo":

Deberías ver:
- Model Name: **Gradient Boosting**
- F1-Score: **~0.74-0.81**
- Recall: **~0.78-0.95**
- Features: **35**
- Training Samples: **85,141**
- Threshold: **0.5** (o 0.0041 si guardaste optimal_threshold.pkl)

## 🎯 MAPEO DE CAMPOS

El servicio mapea automáticamente los campos del frontend a la API:

| Frontend | API |
|----------|-----|
| `userId` | `user_id` |
| `sourceIp` / `ipAddress` | `ip_address` |
| `country` | `country` |
| `region` | `region` |
| `city` | `city` |
| `browser` | `browser` |
| `os` | `os` |
| `device` | `device` |
| `loginSuccessful` | `login_successful` (0 o 1) |
| `isAttackIp` | `is_attack_ip` (0 o 1) |
| `asn` | `asn` |
| `rtt` | `rtt` |
| `timestamp` | `login_timestamp` |

## 🐛 TROUBLESHOOTING

### API no responde

```bash
# Verificar que las APIs estén corriendo
curl http://localhost:8000/
curl http://localhost:8001/
```

Ambas deberían responder con JSON.

### CORS Errors

Si ves errores de CORS en la consola, verifica que las APIs tengan CORS habilitado (ya deberían tenerlo).

### Frontend no actualiza

```bash
# Reiniciar el servidor de desarrollo
cd frontend
npm run dev
```

### Cache del navegador

Si los cambios no se reflejan:
- CTRL + Shift + R (hard reload)
- Borrar cache del navegador
- Cerrar y abrir DevTools

## ✅ CHECKLIST COMPLETO

- [ ] API Phishing corriendo en puerto 8000
- [ ] API Account Takeover corriendo en puerto 8001
- [ ] Frontend corriendo en puerto 5173
- [ ] Status badge muestra "ACTIVE"
- [ ] Predicciones funcionan (no errores)
- [ ] Risk scores tienen sentido (0-100)
- [ ] Model info muestra datos reales
- [ ] Consola sin errores de red

---

**Última Actualización**: 2026-01-15
