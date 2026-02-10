# CLAUDE.md

**Sistema de Deteccion de Incidentes de Ciberseguridad** - Proyecto de investigacion academica con 3 modelos de ML en produccion.

> **Tipo de Sistema**: Clasificacion Predictiva en Tiempo Real (detecta amenazas cuando ocurren, no predice eventos futuros)

---

## Estado del Proyecto (2026-02-04)

| Modelo | Dataset | Algoritmo | F1-Score | ROC-AUC | API | Puerto |
|--------|---------|-----------|----------|---------|-----|--------|
| **Phishing Detection** | CEAS_08 (39K emails) | Gradient Boosting | 99.09% | 99.90% | ✅ | 8000 |
| **Account Takeover** | RBA (85K logins) | Gradient Boosting + SMOTE | 75.86% | 98.06% | ✅ | 8001 |
| **Brute Force** | CSE-CIC-IDS2018 (763K flows) | Random Forest | 99.97% | 100% | ✅ | 8002 |
| **Auth Gateway** | - | JWT + SQLite | - | - | ✅ | 8003 |

**Frontend**: React Dashboard en puerto 5173 (dev) / nginx en Docker
**Repositorio**: GitHub con Git LFS para archivos grandes (.pkl, .csv)
**Containerizacion**: Docker Compose con healthchecks

---

## Aclaracion: Tipo de Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ESTE SISTEMA ES: Clasificacion Predictiva en Tiempo Real               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ LO QUE HACE:                                                        │
│     • Recibe un email/login/flujo de red                                │
│     • Clasifica: "ESTO ES phishing/ATO/brute force" (Si/No)             │
│     • Genera alertas si supera umbrales de confianza                    │
│     • Opera en TIEMPO REAL sobre eventos actuales                       │
│                                                                         │
│  ❌ LO QUE NO HACE (seria otro sistema):                                │
│     • Predecir "en 48 horas habra un ataque"                            │
│     • Forecasting temporal de amenazas                                  │
│     • Analisis de tendencias futuras                                    │
│                                                                         │
│  📋 TRABAJO FUTURO (Fase 2):                                            │
│     • Integracion con SIEM (Splunk, Elastic)                            │
│     • Modelos de series temporales para forecasting                     │
│     • Prediccion de probabilidad de ataques futuros                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Documentacion Adicional

| Documento | Descripcion |
|-----------|-------------|
| `VARIABLES_MODELOS.md` | Variables dependientes/independientes de cada modelo, explicacion detallada de cada feature, importancia en la vida real segun investigaciones |
| `CLAUDE.md` | Este archivo - guia tecnica del proyecto |
| `docs/DOCUMENTACION_OBJETIVOS.md` | Documentacion de objetivos del proyecto de investigacion |

---

## 1. Phishing Email Detection

### Dataset
- **Fuente**: CEAS_08
- **Registros**: 39,154 emails (31,323 train / 7,831 test)
- **Balance**: 44% Legitimo / 56% Phishing

### Modelo
- **Algoritmo**: Gradient Boosting
- **Features**: 1,016 (1,000 TF-IDF + 16 numericas)

### Hiperparametros
```yaml
n_estimators: 100
learning_rate: 0.1
max_depth: 5
min_samples_split: 2
min_samples_leaf: 1
subsample: 1.0
```

### Metricas
| Metrica | Valor |
|---------|-------|
| F1-Score | 99.09% |
| Accuracy | 98.98% |
| Precision | 98.91% |
| Recall | 99.27% |
| ROC-AUC | 99.90% |

### Features Criticas (segun investigacion)
| Feature | Importancia | Razon |
|---------|-------------|-------|
| `url_count` | CRITICA | 75% de phishing tiene URLs maliciosas |
| `has_urgent` | CRITICA | Presion psicologica es tactica principal |
| `sender_domain_encoded` | CRITICA | 90%+ usan domain spoofing |
| TF-IDF features | ALTA | Captura vocabulario predecible del phishing |

### Archivos Clave
```
Phishing/
├── modeling/
│   ├── api/                          # API FastAPI
│   │   ├── app.py
│   │   ├── predictor.py
│   │   └── models.py
│   ├── outputs/
│   │   ├── models/best_model.pkl     # Gradient Boosting (via Git LFS)
│   │   └── features/tfidf_vectorizer.pkl
│   └── src/features/feature_engineering.py
└── processed_data/
    ├── train.csv
    └── test.csv
```

### Ejecutar
```bash
cd Phishing/modeling/api && uvicorn app:app --reload
# http://localhost:8000/docs
```

---

## 2. Account Takeover Detection

### Dataset
- **Fuente**: RBA Dataset (Risk-Based Authentication)
- **Registros**: 85,141 (74,814 train / 17,029 test)
- **Balance Original**: 0.17% ATO / 99.83% Normal (muy desbalanceado)
- **Balance con SMOTE**: 9.09% ATO / 90.91% Normal (en train)

### Modelo
- **Algoritmo**: Gradient Boosting + SMOTE
- **Features**: 35 (temporal, comportamiento, agregados)
- **Manejo de Desbalance**: SMOTE aplicado solo a train set

### Hiperparametros
```yaml
n_estimators: 100
learning_rate: 0.1
max_depth: 5
min_samples_split: 5
min_samples_leaf: 1
subsample: 0.8

# SMOTE config
sampling_strategy: 0.1
k_neighbors: 5
```

### Metricas
| Metrica | Valor | Nota |
|---------|-------|------|
| F1-Score | 75.86% | Aceptable dado el desbalance |
| Accuracy | 99.88% | Engañoso por desbalance |
| Precision | 73.33% | |
| Recall | 78.57% | Detecta ~8 de cada 10 ATOs |
| ROC-AUC | 98.06% | Excelente separacion |

### Features Criticas (segun investigacion)
| Feature | Importancia | Razon |
|---------|-------------|-------|
| `country_changed` | CRITICA | **98.6% de ATOs tienen cambio de pais** |
| `ip_changed` | CRITICA | Atacantes no pueden replicar ubicacion |
| `is_suspicious_ip` | CRITICA | VPNs/proxies son red flags |
| `is_rapid_login` | ALTA | "Viaje imposible" es firma de ATO |

### Insight Clave
> **98.6% de ATOs tienen cambio de pais** - Esta es la feature mas discriminante del modelo. Los atacantes fisicamente no pueden estar en el mismo pais que la victima.

### Formulario Frontend (Mejoras 2026-02-04)
- **Region**: Campo opcional (Bolivia no usa regiones comunmente)
- **Pais**: Dropdown con 97 paises organizados por nivel de riesgo:
  - **Bajo Riesgo (13)**: Bolivia, Argentina, Brasil, Chile, etc. (Sudamerica)
  - **Riesgo Medio (37)**: USA, Canada, UK, Alemania, Japon, etc.
  - **Alto Riesgo (47)**: Rusia, China, Nigeria, Iran, Corea del Norte, etc.
- **Pais por defecto**: Bolivia (BO) - contexto local del proyecto
- **Ejemplos precargados**: Login normal desde Bolivia, ATO desde Rusia

### Archivos Clave
```
Suspicious-Login-Activity/
├── modeling/
│   ├── api/                          # API FastAPI
│   │   ├── app.py
│   │   ├── predictor.py
│   │   └── models.py
│   ├── outputs/
│   │   ├── models/best_model.pkl     # Gradient Boosting (via Git LFS)
│   │   └── features/label_encoders.pkl
│   └── src/models/train.py           # Incluye SMOTE
└── processed_data/rba_reduced.csv
```

### Ejecutar
```bash
cd Suspicious-Login-Activity/modeling/api && uvicorn app:app --port 8001 --reload
# http://localhost:8001/docs
```

---

## 3. Brute Force Detection

### Dataset
- **Fuente**: CSE-CIC-IDS2018
- **Registros**: 763,568 flows (balance perfecto 50/50)
- **Tipos de ataque**: FTP, SSH, Web, XSS Brute Force

### Modelo
- **Algoritmo**: Random Forest
- **Features**: 60 (trafico de red normalizado 0-1)

### Hiperparametros
```yaml
n_estimators: 100
max_depth: 20
min_samples_split: 10
min_samples_leaf: 5
n_jobs: -1
```

### Metricas
| Metrica | Valor |
|---------|-------|
| F1-Score | 99.97% |
| Accuracy | 99.97% |
| Precision | 99.99% |
| Recall | 99.99% |
| ROC-AUC | 100% |

### Features Criticas (segun investigacion)
| Feature | Ratio Ataque/Normal | Interpretacion |
|---------|---------------------|----------------|
| `Bwd Pkts/s` | **112.7x** | Velocidad extrema de bots |
| `Flow Pkts/s` | **24.7x** | Ataques automatizados |
| `Flow Duration` | **0.01x** | Intentos muy rapidos |
| `PSH Flag Cnt` | **1.96x** | Firma de herramientas de ataque |

### Concepto: "Trafico Plano"
Los ataques de fuerza bruta generan trafico con caracteristicas uniformes (duracion, tamaño de paquetes, timing) porque son scripts automatizados. Un humano no puede generar cientos de intentos por segundo con tiempos identicos.

### Formulario Frontend (Mejoras 2026-02-04)
- **Modal de Entrada Manual**: Permite ingresar los 60 campos individualmente
- **12 Tabs organizados por categoria**:
  1. Puerto/Protocolo (dst_port, protocol, timestamp)
  2. Duracion del Flujo (flow_duration)
  3. Paquetes Forward (tot_fwd_pkts, fwd_pkt_len_*)
  4. Paquetes Backward (tot_bwd_pkts, bwd_pkt_len_*)
  5. Bytes/Segundo (flow_byts_s, flow_pkts_s)
  6. Tiempos Inter-Arribo (flow_iat_*, fwd_iat_*, bwd_iat_*)
  7. Flags PSH/URG (fwd_psh_flags, bwd_psh_flags, etc.)
  8. Paquetes/Segundo (fwd_pkts_s, bwd_pkts_s, pkt_len_*)
  9. Flags TCP (fin_flag_cnt, rst_flag_cnt, psh_flag_cnt, etc.)
  10. Ratios y Promedios (down_up_ratio, fwd_byts_b_avg, etc.)
  11. Ventanas TCP (init_fwd_win_byts, init_bwd_win_byts, etc.)
  12. Actividad/Inactividad (active_*, idle_*)

- **4 Ejemplos precargados**:
  | Ejemplo | Descripcion | Resultado Esperado |
  |---------|-------------|-------------------|
  | SSH Brute Force | Ataque al puerto 22 | ATAQUE (99%+) |
  | FTP Brute Force | Ataque al puerto 21 | ATAQUE (99%+) |
  | Web Brute Force | Ataque a login web (puerto 80/443) | ATAQUE (99%+) |
  | Trafico Web Normal | Navegacion normal HTTP | NORMAL (99%+) |

### Archivos Clave
```
fuerza-bruta/
├── api/                              # API FastAPI
│   ├── app.py
│   ├── predictor.py
│   └── models.py
├── modeling/outputs/models/
│   └── random_forest_20260117_021309.pkl  # (via Git LFS)
└── processed_data/brute_force_balanced.csv
```

### Ejecutar
```bash
cd fuerza-bruta/api && uvicorn app:app --port 8002 --reload
# http://localhost:8002/docs
```

---

## 4. Auth Gateway (Sistema de Roles)

### Arquitectura
```
[Frontend React]  →  [Auth Gateway :8003]  →  [ML APIs :8000-8002]
                              ↓
                     [SQLite Database]
                     (Users, Files, Reports, Alerts, Predictions)
```

### Configuracion JWT
```yaml
ACCESS_TOKEN_EXPIRE_MINUTES: 480  # 8 horas
ALGORITHM: HS256
MAX_FILE_SIZE_MB: 50
```

### Roles
| Rol | Permisos |
|-----|----------|
| **Admin (Jefe SOC)** | Subir archivos, generar reportes, gestionar usuarios |
| **Analyst** | Ver reportes, prediccion manual |

### Usuarios por Defecto
- `admin` / `admin123` (rol: admin)
- `analyst` / `analyst123` (rol: analyst)

### Endpoints Principales
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| POST | /auth/login | Login, devuelve JWT | Publico |
| GET | /auth/me | Info del usuario actual | Autenticado |
| POST | /files/upload | Subir CSV/Excel | Admin |
| POST | /reports/generate | Generar reporte | Admin |
| GET | /reports | Listar reportes | Todos |
| GET | /alerts | Listar alertas con filtros | Todos |
| GET | /alerts/stats | Estadisticas de alertas | Todos |
| POST | /predictions/ | Guardar prediccion manual | Todos |
| GET | /predictions/ | Listar predicciones con filtros | Todos |
| GET | /predictions/stats | Estadisticas de predicciones | Todos |

### Tabla Predictions (Auditoria de Predicciones Manuales)
```sql
predictions
├── id (PK)
├── model_type (phishing/ato/brute_force)
├── created_by (FK -> users.id)
├── created_at (timestamp)
├── prediction (0/1)
├── prediction_label (string)
├── confidence (float 0-1)
├── input_data (JSON)
└── explanation (JSON)
```

### Archivos Clave
```
auth-gateway/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuracion + umbrales de alertas
│   ├── models/              # ORM models (User, File, Report, Alert, Prediction)
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # Endpoints (auth, users, files, reports, alerts, predictions)
│   └── services/            # Logica de negocio
├── uploads/                 # Archivos subidos (ignorado en git)
└── Dockerfile               # Imagen Docker del servicio
```

### Ejecutar
```bash
cd auth-gateway && uvicorn app.main:app --port 8003 --reload
# http://localhost:8003/docs
```

---

## 5. Sistema de Alertas Tempranas

### Umbrales por Modelo
| Modelo | Critical (>=) | High (>=) | Medium (>=) | Justificacion |
|--------|---------------|-----------|-------------|---------------|
| Phishing | 95% | 85% | 75% | F1 99% - alta precision |
| ATO | 90% | 80% | 70% | F1 75% - mas conservador |
| Brute Force | 98% | 90% | 80% | F1 99.97% - precision muy alta |

### Flujo de Alertas
1. Admin sube archivo CSV y genera reporte
2. `report_service.py` envia datos a API ML correspondiente
3. `AlertService.generate_alerts_from_predictions()` evalua cada amenaza
4. Si `confidence >= umbral_medium`, se crea alerta con severidad correspondiente
5. Frontend muestra badge con conteo en TopBar y Sidebar

---

## 6. Ejemplos de Prediccion Manual (Demo)

### Phishing - Email de Ataque
```
Remitente: security-alert@paypa1.com
Destinatario: victima@empresa.com
Asunto: URGENTE: Su cuenta ha sido suspendida
Cuerpo:
Estimado Cliente,

Su cuenta de PayPal ha sido suspendida temporalmente por actividad inusual.
Haga clic aqui inmediatamente para verificar su identidad: http://paypa1-secure.com/verify

Si no verifica en 24 horas, su cuenta sera cerrada permanentemente.

Equipo de Seguridad PayPal
URLs: 1
```
**Resultado esperado**: PHISHING (97%+ confianza)

### Phishing - Email Legitimo
```
Remitente: juan.perez@miempresa.com
Destinatario: maria.garcia@miempresa.com
Asunto: Reunion de equipo manana
Cuerpo:
Hola Maria,

Te confirmo la reunion de equipo para manana a las 10:00 AM.
Por favor, trae los reportes del mes pasado.

Saludos,
Juan
URLs: 0
```
**Resultado esperado**: LEGITIMO (95%+ confianza)

### Account Takeover - Login Sospechoso
```
Usuario: usuario_victima
Pais: Rusia (RU) - ALTO RIESGO
Region: (vacio)
Login exitoso: No
IP Cambiada: Si
Dispositivo Cambiado: Si
Hora: 03:00 (madrugada)
ASN: 12345
RTT: 450ms (latencia alta)
```
**Resultado esperado**: ACCOUNT TAKEOVER (85%+ confianza)

### Account Takeover - Login Normal
```
Usuario: usuario_normal
Pais: Bolivia (BO) - BAJO RIESGO
Region: (vacio)
Login exitoso: Si
IP Cambiada: No
Dispositivo Cambiado: No
Hora: 09:30 (horario laboral)
ASN: 27839
RTT: 45ms (latencia baja)
```
**Resultado esperado**: LOGIN NORMAL (95%+ confianza)

---

## 7. Explainabilidad de Predicciones

Cada prediccion incluye un campo `explanation` con:
- `risk_indicators`: Lista de indicadores con evidencia y severidad
- `summary`: Resumen en lenguaje natural
- Campos adicionales segun modelo (geo_info, top_features, etc.)

Ver `VARIABLES_MODELOS.md` para explicacion detallada de cada variable.

---

## 8. Frontend (React Dashboard)

### Ejecutar (Desarrollo)
```bash
cd frontend && npm run dev
# http://localhost:5173
```

### Ejecutar (Produccion via Docker)
El frontend se sirve desde nginx:alpine con optimizaciones de cache y headers de seguridad.

### Rutas
| Ruta | Descripcion | Rol |
|------|-------------|-----|
| /login | Pagina de login | Publico |
| /dashboard | Dashboard con estadisticas | Todos |
| /dashboard/predict | Prediccion manual (3 modelos) | Todos |
| /files | Gestion de archivos | Admin |
| /reports | Lista de reportes con graficos | Todos |
| /alerts | Alertas tempranas | Todos |
| /users | Gestion de usuarios | Admin |

### Paleta de Colores (BCP Corporate)
- **Primario**: `#004B8E` (Azul BCP)
- **Acento**: `#F26E29` (Naranja BCP) - usado en TopBar
- **Navy**: `#32335C` (texto oscuro)
- **Status**: Success `#38A169`, Danger `#E53E3E`, Warning `#ECC94B`

### Sistema de Design Tokens (3 niveles)
```
┌─────────────────────────────────────────────────────────────────────┐
│  Nivel 1: Primitives (theme.js)                                     │
│  → Paleta bruta de colores, nunca usar directamente                 │
├─────────────────────────────────────────────────────────────────────┤
│  Nivel 2: Semantic Tokens (theme.js)                                │
│  → backgrounds, text, borders, interactive, status, surfaces        │
├─────────────────────────────────────────────────────────────────────┤
│  Nivel 3: Component Tokens (theme.js)                               │
│  → sidebar, card, input, prediction                                 │
├─────────────────────────────────────────────────────────────────────┤
│  CSS Variables (index.css)                                          │
│  → ~100 variables CSS en :root exportadas desde theme.js            │
└─────────────────────────────────────────────────────────────────────┘
```

### Helper Functions (theme.js)
```javascript
getThreatColor(level)      // 'critical'|'high'|'medium'|'low' → color
getPredictionBg(label)     // prediction label → background color
```

### Nginx (Produccion)
- **Gzip**: Nivel 6, archivos >1KB
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **Cache**: 1 año para assets estaticos (js/css/images)
- **SPA Routing**: Fallback a /index.html
- **Healthcheck**: GET /health → 200 OK

---

## 9. Docker y Containerizacion

### Ejecutar con Docker Compose (Produccion)
```bash
docker-compose up -d
# Frontend: http://localhost:80
# Auth Gateway: http://localhost:8003
# APIs ML: puertos 8000-8002
```

### Ejecutar con Docker Compose (Desarrollo)
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Arquitectura de Contenedores
```
┌─────────────────────────────────────────────────────────────────────┐
│                     cybersecurity-network (bridge)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ phishing-api │  │    ato-api   │  │brute-force-  │               │
│  │    :8000     │  │    :8001     │  │  api :8002   │               │
│  │  healthcheck │  │  healthcheck │  │  healthcheck │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│          │                 │                 │                       │
│          └─────────────────┼─────────────────┘                       │
│                            ▼                                         │
│                  ┌──────────────────┐                                │
│                  │   auth-gateway   │                                │
│                  │      :8003       │                                │
│                  │   healthcheck    │                                │
│                  │  depends_on: ML  │                                │
│                  └────────┬─────────┘                                │
│                           │                                          │
│            ┌──────────────┴──────────────┐                           │
│            ▼                             ▼                           │
│  ┌──────────────────┐         ┌──────────────────┐                   │
│  │ auth-gateway-data│         │auth-gateway-     │                   │
│  │   (SQLite DB)    │         │uploads (files)   │                   │
│  └──────────────────┘         └──────────────────┘                   │
│                                                                      │
│                  ┌──────────────────┐                                │
│                  │     frontend     │                                │
│                  │   :80 (nginx)    │                                │
│                  │   healthcheck    │                                │
│                  │ depends_on: auth │                                │
│                  └──────────────────┘                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Healthchecks
Todos los servicios incluyen healthchecks con:
- **Intervalo**: 30 segundos
- **Timeout**: 10 segundos
- **Retries**: 3
- **Endpoint**: GET /health (o /docs para ML APIs)

### Volumenes Persistentes
| Volumen | Ruta en Container | Proposito |
|---------|-------------------|-----------|
| `auth-gateway-data` | `/app/data` | SQLite database |
| `auth-gateway-uploads` | `/app/uploads` | Archivos subidos |

### Variables de Entorno (Docker)
```yaml
# ML APIs (interno a Docker network)
PHISHING_API_URL: http://phishing-api:8000
ATO_API_URL: http://ato-api:8001
BRUTE_FORCE_API_URL: http://brute-force-api:8002

# Frontend
VITE_API_URL: http://localhost:8003  # Auth Gateway
```

### Dockerfiles
| Servicio | Base Image | Notas |
|----------|------------|-------|
| phishing-api | python:3.12-slim | uvicorn production |
| ato-api | python:3.12-slim | uvicorn production |
| brute-force-api | python:3.12-slim | uvicorn production |
| auth-gateway | python:3.12-slim | uvicorn production |
| frontend | nginx:alpine | Multi-stage build (3 etapas) |

---

## 10. Git y Repositorio

### Git LFS
El proyecto usa Git LFS para archivos grandes:
```bash
# Archivos trackeados por LFS
*.pkl   # Modelos de ML
*.csv   # Datasets
*.joblib
```

### .gitignore
- **Excluye**: datasets originales (~15GB), node_modules, __pycache__, .env, uploads
- **Incluye (via LFS)**: best_model.pkl de cada modelo, tfidf_vectorizer.pkl, label_encoders.pkl

### Configurar Git LFS en nuevo clone
```bash
git lfs install
git lfs pull
```

---

## 11. Ejecutar Sistema Completo

### Opcion A: Docker Compose (Recomendado)
```bash
docker-compose up -d
# Todos los servicios inician automaticamente con healthchecks
```

### Opcion B: Manual (Desarrollo)
```bash
# Terminal 1: Phishing API
cd Phishing/modeling/api && uvicorn app:app --reload

# Terminal 2: Account Takeover API
cd Suspicious-Login-Activity/modeling/api && uvicorn app:app --port 8001 --reload

# Terminal 3: Brute Force API
cd fuerza-bruta/api && uvicorn app:app --port 8002 --reload

# Terminal 4: Auth Gateway API
cd auth-gateway && uvicorn app.main:app --port 8003 --reload

# Terminal 5: Frontend
cd frontend && npm run dev
```

---

## 12. Estructura del Proyecto

```
pred_model/
├── Phishing/                    # Deteccion de emails phishing (Puerto 8000)
│   └── modeling/api/Dockerfile  # Imagen Docker
├── Suspicious-Login-Activity/   # Deteccion de Account Takeover (Puerto 8001)
│   └── modeling/api/Dockerfile  # Imagen Docker
├── fuerza-bruta/                # Deteccion de Brute Force (Puerto 8002)
│   └── api/Dockerfile           # Imagen Docker
├── auth-gateway/                # Auth Gateway (Puerto 8003)
│   └── Dockerfile               # Imagen Docker
├── frontend/                    # React Dashboard (Puerto 5173 dev / 80 prod)
│   ├── Dockerfile               # Multi-stage build
│   └── nginx.conf               # Configuracion nginx produccion
├── docs/                        # Documentacion adicional
│   └── DOCUMENTACION_OBJETIVOS.md
├── test_input_files/            # Archivos de prueba para APIs
├── docker-compose.yml           # Produccion
├── docker-compose.dev.yml       # Desarrollo
├── .dockerignore                # Exclusiones para Docker build
├── seed_data.py                 # Script para poblar BD
├── sync_alerts.py               # Script para sincronizar alertas
├── CLAUDE.md                    # Este archivo
├── VARIABLES_MODELOS.md         # Documentacion de variables
├── .gitignore                   # Configuracion de exclusiones
└── .gitattributes               # Configuracion de Git LFS
```

---

## 13. Notas Tecnicas

### Dependencias
- Python 3.12 con venv en `/home/megalodon/dev/cbproy/venv`
- NumPy 1.26.3, Scikit-learn 1.8.0
- FastAPI + Uvicorn para APIs
- React + Vite para Frontend
- imbalanced-learn para SMOTE (modelo ATO)

### Formato de Respuesta de APIs ML
```json
{
  "prediction": 0,              // 0=benigno, 1=amenaza
  "prediction_label": "...",    // texto descriptivo
  "confidence": 0.95,           // 0-1
  "explanation": {
    "risk_indicators": [...],
    "summary": "...",
    "total_indicators": 2
  }
}
```

### Mapeo de Tipos de Modelo
| Frontend | Backend | Puerto |
|----------|---------|--------|
| `phishing` | `phishing` | 8000 |
| `ataques_sospechosos` | `ato` | 8001 |
| `fuerza_bruta` | `brute_force` | 8002 |

### Servicios Frontend
```
frontend/src/services/
├── api.js                    # Axios instance con interceptores
├── phishingService.js        # Prediccion phishing
├── ataquesSospechososService.js  # Prediccion ATO
├── fuerzaBrutaService.js     # Prediccion brute force
├── modelService.js           # Servicio unificado de modelos
└── predictionService.js      # CRUD de predicciones (nuevo)
```

---

## 14. Estado de Completitud

### Sistema Actual: COMPLETO para Clasificacion en Tiempo Real

| Componente | Estado | Notas |
|------------|--------|-------|
| Modelo Phishing | ✅ | F1 99.09%, no requiere tuning |
| Modelo ATO | ✅ | F1 75.86% + SMOTE, aceptable |
| Modelo Brute Force | ✅ | F1 99.97%, excelente |
| APIs REST | ✅ | FastAPI funcionando |
| Auth Gateway | ✅ | JWT + roles (8h expiracion) |
| Sistema de Alertas | ✅ | Umbrales configurables |
| Sistema de Predicciones | ✅ | Auditoria de predicciones manuales |
| Frontend Dashboard | ✅ | React + Design Tokens + Formularios mejorados |
| Docker | ✅ | docker-compose con healthchecks |
| Nginx (Produccion) | ✅ | Security headers + cache |
| Explainability | ✅ | Explicaciones por prediccion |
| Documentacion | ✅ | CLAUDE.md + VARIABLES_MODELOS.md |
| Git LFS | ✅ | Modelos y datos grandes |

### Trabajo Futuro (Fase 2)
- Integracion con SIEM (Splunk, Elastic SIEM)
- Modelos de series temporales para forecasting
- Prediccion temporal ("en 48h habra ataque")
- Reentrenamiento automatico de modelos
- Kubernetes deployment

---

**Ultima Actualizacion**: 2026-02-04
