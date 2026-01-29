# CLAUDE.md

**Sistema de Predicción de Incidentes de Ciberseguridad** - Proyecto de investigación académica con 3 modelos de ML en producción.

---

## Estado del Proyecto (2026-01-29)

| Modelo | Dataset | Algoritmo | F1-Score | API | Puerto |
|--------|---------|-----------|----------|-----|--------|
| **Phishing Detection** | CEAS_08 (39K emails) | Gradient Boosting | 99.01% | ✅ | 8000 |
| **Account Takeover** | RBA (85K logins) | Gradient Boosting | 75.86% | ✅ | 8001 |
| **Brute Force** | CSE-CIC-IDS2018 (763K flows) | Random Forest | 99.97% | ✅ | 8002 |
| **Auth Gateway** | - | JWT + SQLite | - | ✅ | 8003 |

**Frontend**: React Dashboard con autenticacion en puerto 5173

---

## 1. Phishing Email Detection

### Dataset
- **Fuente**: CEAS_08
- **Registros**: 39,154 emails (31,323 train / 7,831 test)
- **Balance**: 44% Legítimo / 56% Phishing

### Modelo
- **Algoritmo**: Gradient Boosting
- **Features**: 1,016 (1,000 TF-IDF + 16 numéricas)
- **Métricas**:
  - F1-Score: 99.01%
  - Accuracy: 98.89%
  - Precision: 98.73%
  - Recall: 99.29%

### Archivos Clave
```
Phishing/
├── modeling/
│   ├── api/                          # API FastAPI
│   │   ├── app.py
│   │   ├── predictor.py
│   │   └── models.py
│   ├── outputs/
│   │   ├── models/best_model.pkl     # Gradient Boosting
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
- **Balance**: 0.17% ATO / 99.83% Normal (muy desbalanceado)

### Modelo
- **Algoritmo**: Gradient Boosting
- **Features**: 35 (temporal, comportamiento, agregados)
- **Métricas**:
  - F1-Score: 75.86%
  - Accuracy: 99.88%
  - Precision: 73.33%
  - Recall: 78.57%
  - ROC-AUC: 98.06%

### Insight Clave
- **98.6% de ATOs tienen cambio de país** ← Feature más importante
- 99.3% de ATOs son logins exitosos (no es Brute Force)

### Archivos Clave
```
Suspicious-Login-Activity/
├── modeling/
│   ├── api/                          # API FastAPI
│   │   ├── app.py
│   │   ├── predictor.py
│   │   └── models.py
│   └── outputs/models/best_model.pkl # Gradient Boosting
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
- **Features**: 60 (tráfico de red normalizado 0-1)
- **Métricas**:
  - F1-Score: 99.97%
  - Accuracy: 99.97%
  - Precision: 100%
  - Recall: 99.94%

### Features Discriminantes
| Feature | Ratio Ataque/Normal | Interpretación |
|---------|---------------------|----------------|
| Bwd Pkts/s | 112.7x | Velocidad extrema de bots |
| Flow Pkts/s | 24.7x | Ataques automatizados |
| PSH Flag Cnt | 1.96x | Firma de herramientas |
| Flow Duration | 0.01x | Intentos rápidos |

### Archivos Clave
```
fuerza-bruta/
├── api/                              # API FastAPI
│   ├── app.py
│   ├── predictor.py
│   ├── models.py
│   └── .env
├── modeling/outputs/models/
│   └── random_forest_20260117_021309.pkl
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
                     (Users, Files, Reports, Alerts)
```

### Roles
| Rol | Permisos |
|-----|----------|
| **Admin (Jefe SOC)** | Subir archivos, generar reportes, gestionar usuarios |
| **Analyst** | Ver reportes, prediccion manual |

### Usuarios por Defecto
- `admin` / `admin123` (rol: admin)
- `analyst` / `analyst123` (rol: analyst)

### Endpoints
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| POST | /auth/login | Login, devuelve JWT | Publico |
| GET | /auth/me | Info del usuario actual | Autenticado |
| POST | /files/upload | Subir CSV/Excel | Admin |
| GET | /files | Listar archivos | Admin |
| POST | /reports/generate | Generar reporte | Admin |
| GET | /reports | Listar reportes | Todos |
| GET | /alerts | Listar alertas con filtros | Todos |
| GET | /alerts/unread/count | Contador alertas no leidas | Todos |
| GET | /alerts/stats | Estadisticas de alertas | Todos |
| GET | /alerts/{id} | Detalle de alerta (marca como leida) | Todos |
| POST | /alerts/{id}/acknowledge | Reconocer alerta | Todos |
| POST | /alerts/acknowledge/bulk | Reconocer multiples alertas | Todos |
| POST | /alerts/mark-all-read | Marcar todas como leidas | Todos |
| GET | /alerts/thresholds | Ver umbrales configurados | Todos |

### Procesamiento de Predicciones
El `report_service.py` procesa las respuestas de las APIs:
- Las APIs devuelven `prediction: 0|1` (entero), no strings
- `prediction=1` significa amenaza, `prediction=0` significa benigno
- El campo `prediction_label` contiene el texto descriptivo
- La confianza se convierte a porcentaje (*100)
- **Tras procesar, se generan alertas automaticas** para amenazas que superen umbrales

### Archivos Clave
```
auth-gateway/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuracion + umbrales de alertas
│   ├── database.py          # SQLAlchemy setup
│   ├── models/              # ORM models (User, File, Report, Alert)
│   │   ├── user.py
│   │   ├── file.py
│   │   ├── report.py
│   │   └── alert.py         # Modelo de alertas
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── report.py
│   │   └── alert.py         # Schemas de alertas
│   ├── routers/             # Endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── files.py
│   │   ├── reports.py
│   │   └── alerts.py        # Router de alertas
│   └── services/
│       ├── auth_service.py
│       ├── file_service.py
│       ├── report_service.py      # Procesa predicciones + genera alertas
│       ├── prediction_client.py   # Cliente HTTP a APIs ML
│       ├── column_detector.py     # Detecta modelo por columnas
│       └── alert_service.py       # Generacion y gestion de alertas
├── uploads/                 # Archivos subidos
└── requirements.txt
```

### Ejecutar
```bash
cd auth-gateway && uvicorn app.main:app --port 8003 --reload
# http://localhost:8003/docs
```

---

## 5. Sistema de Alertas Tempranas

### Descripcion
Generacion automatica de alertas basadas en umbrales de confianza cuando se procesan predicciones. Las alertas se generan en `report_service.py` tras procesar cada reporte.

### Umbrales por Modelo
| Modelo | Critical (>=) | High (>=) | Medium (>=) | Justificacion |
|--------|---------------|-----------|-------------|---------------|
| Phishing | 95% | 85% | 75% | F1 99.01% - alta precision |
| ATO | 90% | 80% | 70% | F1 75.86% - mas conservador |
| Brute Force | 98% | 90% | 80% | F1 99.97% - precision muy alta |

Los umbrales se configuran en `auth-gateway/app/config.py` (`ALERT_THRESHOLDS`).

### Modelo de Datos Alert
```python
Alert:
  id, title, description
  severity: 'critical' | 'high' | 'medium'
  status: 'unread' | 'read' | 'acknowledged'
  model_type: 'phishing' | 'ato' | 'brute_force'
  report_id (FK -> reports.id)
  prediction_index, confidence, prediction_label, risk_level
  created_at, read_at, acknowledged_at, acknowledged_by
  raw_data_json  # JSON de la prediccion original
```

### Flujo de Alertas
1. Admin sube archivo CSV y genera reporte
2. `report_service.py` envia datos a API ML correspondiente
3. Al procesar resultados, `AlertService.generate_alerts_from_predictions()` evalua cada amenaza
4. Si `confidence >= umbral_medium`, se crea una alerta con severidad correspondiente
5. Frontend muestra badge con conteo en TopBar y Sidebar
6. Usuarios pueden ver, filtrar y reconocer alertas en `/alerts`

### Frontend - Integracion de Alertas
- **TopBar**: Icono campana con badge dinamico (contador no leidas), click navega a `/alerts`
- **Sidebar**: Pestaña "Alertas" con badge pill rojo, visible para todos los roles
- **AlertContext**: Contexto global con polling cada 30 segundos para actualizar contadores
- **AlertsPage**: Pagina completa con tarjetas de estadisticas, filtros y lista de alertas

### Archivos Frontend de Alertas
```
frontend/src/
├── services/
│   └── alertService.js              # Cliente API alertas -> :8003
├── context/
│   └── AlertContext.jsx             # Estado global + polling 30s
├── components/alerts/
│   ├── AlertsList.jsx               # Tabla con seleccion multiple
│   ├── AlertDetail.jsx              # Modal de detalle
│   ├── AlertFilters.jsx             # Filtros status/severity/model
│   └── AlertStatsCards.jsx          # Tarjetas de estadisticas
└── pages/
    └── AlertsPage.jsx               # Pagina principal de alertas
```

---

## 6. Explainabilidad de Predicciones

### Descripcion
Cada prediccion incluye un campo `explanation` que explica **por que** el modelo clasifico algo como amenaza o benigno. La explicacion muestra indicadores de riesgo especificos con evidencia detallada.

### Estructura de Explicacion (Comun a todos los modelos)

```python
RiskIndicator:
  indicator: str      # Descripcion del indicador
  evidence: List[str] # Evidencia especifica encontrada
  severity: str       # 'critical' | 'high' | 'medium' | 'low'

Explanation:
  risk_indicators: List[RiskIndicator]  # Indicadores con evidencia
  summary: str                          # Resumen en lenguaje natural
  total_indicators: int                 # Cantidad de indicadores
  # + campos adicionales por modelo
```

### Indicadores por Modelo

| Modelo | Indicadores Detectados | Campos Adicionales |
|--------|------------------------|-------------------|
| **Phishing** | URLs/enlaces, MAYUSCULAS, urgencia, "click here", credenciales, suplantacion de marca | `suspicious_terms: List[str]` |
| **ATO** | Cambio de pais/IP/navegador/dispositivo/SO, horario nocturno, IP en lista negra, login rapido | `risk_factors: dict`, `key_features: dict`, `geo_info: dict` |
| **Brute Force** | Tasa de paquetes alta, duracion de flujo corta, flags PSH/RST, puerto de ataque | `top_features: dict` |

### Ejemplo de Respuesta API (Phishing)

```json
{
  "prediction": 1,
  "prediction_label": "Phishing",
  "confidence": 0.95,
  "explanation": {
    "risk_indicators": [
      {
        "indicator": "Contiene URLs/enlaces",
        "evidence": ["https://suspicious-link.com/login"],
        "severity": "high"
      },
      {
        "indicator": "Contiene lenguaje de urgencia",
        "evidence": ["...Your account will be SUSPENDED immediately..."],
        "severity": "medium"
      }
    ],
    "suspicious_terms": ["urgent", "click", "verify"],
    "summary": "Este email muestra 2 indicadores de phishing con 95.0% de confianza.",
    "total_indicators": 2
  }
}
```

### Frontend - Componente ExplainabilitySection

**Archivo:** `frontend/src/components/results/ExplainabilitySection.jsx`

Componente que muestra un boton "¿Por que esta prediccion?" que abre un modal con:
- Resumen de la prediccion
- Indicadores de riesgo en formato Accordion (expandibles)
- Evidencia especifica para cada indicador
- Badge de severidad (critical/high/medium/low)
- Informacion adicional segun el modelo (geo_info, top_features, etc.)

### Integracion en Frontend

| Componente | Uso |
|------------|-----|
| `ResultsDisplay.jsx` | Prediccion manual - boton debajo de metricas |
| `ReportDetail.jsx` | Reportes - columna "Explicacion" con modal por registro |
| `AlertDetail.jsx` | Alertas - seccion visual arriba del JSON raw |

### Archivos Modificados (Backend)

```
# Schemas Pydantic (models.py)
Phishing/modeling/api/models.py           # PhishingExplanation + RiskIndicator
Suspicious-Login-Activity/modeling/api/models.py  # ATOExplanation + RiskIndicator
fuerza-bruta/api/models.py                # BruteForceExplanation + RiskIndicator

# Generacion de explicaciones (predictor.py)
Phishing/modeling/api/predictor.py        # _generate_explanation()
Suspicious-Login-Activity/modeling/api/predictor.py  # _generate_explanation()
fuerza-bruta/api/predictor.py             # _generate_explanation()

# Auth Gateway
auth-gateway/app/services/report_service.py   # Preserva campo explanation
auth-gateway/app/services/alert_service.py    # Incluye explicacion en descripcion
```

---

## Frontend (React Dashboard)

### Ejecutar
```bash
cd frontend && npm run dev
# http://localhost:5173
```

### Rutas
| Ruta | Descripcion | Rol |
|------|-------------|-----|
| /login | Pagina de login | Publico |
| /dashboard | **Dashboard con estadisticas** (Overview) | Todos |
| /dashboard/predict | Prediccion manual (3 modelos) | Todos |
| /files | Gestion de archivos | Admin |
| /reports | Lista de reportes con graficos | Todos |
| /alerts | **Alertas tempranas** (lista, filtros, stats) | Todos |
| /users | Gestion de usuarios | Admin |

### Layout
- **Sidebar**: `position: fixed`, 260px, colapsa en <992px
- **TopBar**: `position: sticky`, gradiente naranja, se mantiene fijo al scrollear
- **MainLayout**: `.main-content` es el contenedor scrolleable (`height: 100vh; overflow-y: auto`)

### Componentes Principales
```
frontend/src/components/
├── layout/
│   ├── MainLayout.jsx       # Contenedor principal (sidebar + content scrolleable)
│   ├── Sidebar.jsx          # Navegacion lateral fija (260px, colapsa en <992px)
│   └── TopBar.jsx           # Barra superior naranja sticky
├── dashboard/
│   ├── Dashboard.jsx        # Formularios de prediccion manual
│   ├── DashboardOverview.jsx # Estadisticas y resumen
│   └── ModelSelector.jsx    # Selector de modelos (grid responsive)
├── results/
│   ├── ResultsDisplay.jsx   # Muestra resultados de prediccion
│   ├── ConfidenceMetrics.jsx # Metricas de confianza
│   └── ExplainabilitySection.jsx  # Boton + modal de explicacion
├── reports/
│   ├── ReportsList.jsx      # Lista de reportes
│   └── ReportDetail.jsx     # Detalle con graficos + explicacion
├── alerts/
│   ├── AlertsList.jsx       # Lista con seleccion multiple
│   ├── AlertDetail.jsx      # Modal de detalle + explicacion
│   ├── AlertFilters.jsx     # Filtros por status/severity/model
│   └── AlertStatsCards.jsx  # Tarjetas de estadisticas
└── ...
```

### Sistema de Design Tokens
```
frontend/src/styles/
├── theme.js                 # Tokens JS (primitivos + semanticos)
├── index.css                # Variables CSS globales
├── dashboard.css            # Estilos del dashboard (responsive)
├── components.css           # Componentes reutilizables
└── custom-bootstrap.scss    # Bootstrap overrides + responsive
```

### Paleta de Colores (BCP Corporate)
- **Primario**: `#00498C` (Azul BCP)
- **Acento**: `#FF7800` (Naranja BCP) - usado en TopBar
- **Fondos**: `#FFFFFF`, `#F8F9FA`, `#F0F0F0`
- **Texto**: `#333333` (primario), `#666666` (secundario)
- **Status**: Success `#38A169`, Danger `#E53E3E`, Warning `#ECC94B`

### TopBar
- Fondo: Gradiente naranja (`#FF7800` → `#E56A00`)
- Titulo: Texto blanco
- Botones (alertas, usuario): Fondo blanco, iconos azules
- Avatar: Fondo azul con letra blanca
- Position: sticky top:0, z-index: 900

### Breakpoints Responsive
- **Desktop**: >= 992px (sidebar visible, grid 2 columnas)
- **Tablet**: 768px - 992px (sidebar oculto, grid 1 columna)
- **Mobile**: < 768px (estilos compactos)
- **Small Mobile**: < 480px (model buttons en 1 columna)

### Servicios
```
frontend/src/services/
├── authService.js           # → localhost:8003 (Auth Gateway)
├── fileService.js           # → localhost:8003 (Auth Gateway)
├── reportService.js         # → localhost:8003 (Auth Gateway)
├── alertService.js          # → localhost:8003 (Auth Gateway) - Alertas
├── userService.js           # → localhost:8003 (Auth Gateway)
├── phishingService.js       # → localhost:8000
├── ataquesSospechososService.js # → localhost:8001
└── fuerzaBrutaService.js    # → localhost:8002
```

### Contextos
```
frontend/src/context/
├── AuthContext.jsx           # Autenticacion (user, token, login, logout)
├── AlertContext.jsx          # Alertas (unreadCount, polling 30s, CRUD)
└── DashboardContext.jsx      # Estado del dashboard de prediccion
```

---

## Scripts de Utilidad

### Seed Data (Poblar BD con datos de prueba)
```bash
source /home/megalodon/dev/cbproy/venv/bin/activate
python seed_data.py
```

Genera:
- 9 archivos CSV (3 por modelo) con datos reales de los datasets
- 9 reportes con predicciones ejecutadas

### Sincronizar Alertas (Generar alertas desde reportes existentes)
```bash
source /home/megalodon/dev/cbproy/venv/bin/activate
cd auth-gateway && python ../sync_alerts.py
```

Recorre todos los reportes completados y genera alertas retroactivas para predicciones que superen los umbrales. Limpia alertas existentes antes de regenerar.

### Regenerar Reportes
```bash
python regenerate_reports.py
```

---

## Ejecutar Sistema Completo

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

## Estructura del Proyecto

```
pred_model/
├── Phishing/                    # Deteccion de emails phishing
│   ├── modeling/api/            # Puerto 8000
│   ├── processed_data/
│   └── analysis/
│
├── Suspicious-Login-Activity/   # Deteccion de Account Takeover
│   ├── modeling/api/            # Puerto 8001
│   ├── processed_data/
│   └── analysis/
│
├── fuerza-bruta/                # Deteccion de Brute Force
│   ├── api/                     # Puerto 8002
│   ├── modeling/outputs/
│   ├── processed_data/
│   └── analysis/
│
├── auth-gateway/                # Auth Gateway (Puerto 8003)
│   ├── app/
│   │   ├── models/              # User, File, Report, Alert
│   │   ├── schemas/             # Pydantic schemas (user, report, alert)
│   │   ├── routers/             # auth, users, files, reports, alerts
│   │   └── services/            # auth, file, report, prediction_client, alert
│   └── uploads/                 # Archivos CSV/Excel subidos
│
├── frontend/                    # React Dashboard (Puerto 5173)
│   └── src/
│       ├── components/
│       │   ├── auth/            # Login, ProtectedRoute, RoleGuard
│       │   ├── dashboard/       # Dashboard, DashboardOverview, ModelSelector
│       │   ├── layout/          # Sidebar (fixed), TopBar (sticky), MainLayout
│       │   ├── files/           # FileUpload, FileList, FilePreview
│       │   ├── results/         # ResultsDisplay, ConfidenceMetrics, ExplainabilitySection
│       │   ├── reports/         # ReportsList, ReportDetail (con explicacion)
│       │   ├── alerts/          # AlertsList, AlertDetail (con explicacion), AlertFilters
│       │   └── users/           # UserManagement
│       ├── styles/              # Design Tokens (theme.js, CSS)
│       ├── context/
│       │   ├── AuthContext.jsx  # Autenticacion
│       │   ├── AlertContext.jsx # Alertas (polling, unread count)
│       │   └── DashboardContext.jsx
│       ├── pages/               # LoginPage, DashboardPage, AlertsPage, etc.
│       └── services/            # authService, alertService, reportService, etc.
│
├── seed_data.py                 # Script para poblar BD
├── sync_alerts.py               # Script para sincronizar alertas con reportes existentes
├── regenerate_reports.py        # Script para regenerar reportes
└── CLAUDE.md                    # Este archivo
```

---

## Notas Técnicas

### Dependencias
- Python 3.12 con venv en `/home/megalodon/dev/cbproy/venv`
- NumPy 1.26.3, Scikit-learn 1.8.0
- FastAPI + Uvicorn para APIs
- React + Vite para Frontend

### Re-entrenar Modelos
Si hay incompatibilidad de versiones NumPy:
```bash
cd Phishing/modeling && python retrain_model.py
```

### Formato de Respuesta de APIs ML
Las APIs devuelven predicciones en formato:
```json
{
  "prediction": 0,              // 0=benigno, 1=amenaza
  "prediction_label": "...",    // texto descriptivo
  "confidence": 0.95,           // 0-1, se multiplica por 100 en report_service
  "explanation": {              // Explicacion de la prediccion
    "risk_indicators": [
      {
        "indicator": "...",     // Descripcion del indicador
        "evidence": ["..."],    // Evidencia especifica
        "severity": "high"      // critical | high | medium | low
      }
    ],
    "summary": "...",           // Resumen en lenguaje natural
    "total_indicators": 2       // Cantidad de indicadores
  }
}
```

### Mapeo de Tipos de Modelo (Frontend ↔ Backend)
El frontend usa nombres diferentes para algunos modelos:

| Frontend (modelType) | Backend (model_type) | API Puerto |
|---------------------|---------------------|------------|
| `phishing` | `phishing` | 8000 |
| `ataques_sospechosos` | `ato` | 8001 |
| `fuerza_bruta` | `brute_force` | 8002 |

El componente `ExplainabilitySection` maneja ambos nombres con aliases en el switch.

---

**Ultima Actualizacion**: 2026-01-29
