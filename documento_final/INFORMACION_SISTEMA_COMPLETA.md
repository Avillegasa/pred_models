# DOCUMENTACION COMPLETA DEL SISTEMA DE PREDICCION DE INCIDENTES DE CIBERSEGURIDAD

## INFORMACION PARA ACTUALIZAR TRABAJO DE GRADO

**Fecha de generacion:** 2026-01-26
**Autor del sistema:** Andres Alvaro Villegas Salazar
**Institucion:** Escuela Militar de Ingenieria - Bolivia
**Caso de estudio:** Banco de Credito de Bolivia

---

# PARTE 1: RESUMEN EJECUTIVO DEL SISTEMA IMPLEMENTADO

## 1.1 Descripcion General

Sistema de prediccion de incidentes de ciberseguridad basado en aprendizaje automatico, compuesto por:

- **3 modelos de Machine Learning** independientes (microservicios)
- **1 Gateway de autenticacion** centralizado
- **1 Dashboard web** (React)
- **Base de datos SQLite** para gestion de usuarios, archivos y reportes

## 1.2 Tabla Resumen de Modelos

| Modelo | Dataset | Registros | Algoritmo | F1-Score | Puerto |
|--------|---------|-----------|-----------|----------|--------|
| **Phishing Detection** | CEAS_08 | 39,154 emails | Gradient Boosting | 99.01% | 8000 |
| **Account Takeover** | RBA Dataset | 85,141 logins | Gradient Boosting | 75.86% | 8001 |
| **Brute Force** | CSE-CIC-IDS2018 | 763,568 flows | Random Forest | 99.97% | 8002 |
| **Auth Gateway** | - | - | JWT + SQLite | - | 8003 |
| **Frontend** | - | - | React + Vite | - | 5173 |

## 1.3 Stack Tecnologico Completo

### Backend (APIs de ML)
- **Lenguaje:** Python 3.12
- **Framework:** FastAPI 0.115.0
- **Servidor:** Uvicorn 0.30.6
- **ML:** scikit-learn 1.8.0
- **Datos:** Pandas 2.2.3, NumPy 1.26.3
- **Validacion:** Pydantic 2.9.2

### Auth Gateway
- **Framework:** FastAPI 0.115.0
- **ORM:** SQLAlchemy 2.0.35
- **Base de datos:** SQLite
- **Autenticacion:** JWT (PyJWT 3.3.0)
- **Hashing:** bcrypt 4.0.1
- **HTTP Client:** httpx 0.27.2

### Frontend
- **Framework:** React 19.2.0
- **Build Tool:** Vite 7.2.4
- **UI:** Bootstrap 5.3.8 + React-Bootstrap 2.10.10
- **Routing:** React Router 7.12.0
- **HTTP Client:** Axios 1.13.2
- **Estilos:** Sass 1.97.2

---

# PARTE 2: ARQUITECTURA DEL SISTEMA

## 2.1 Diagrama de Arquitectura

```
+------------------------------------------------------------------+
|                      FRONTEND (React)                             |
|                      Puerto: 5173                                 |
|  +------------------+  +------------------+  +------------------+ |
|  | Login/Auth      |  | Dashboard        |  | Reports/Files    | |
|  | Components      |  | Prediction Forms |  | Management       | |
|  +------------------+  +------------------+  +------------------+ |
+------------------------------------------------------------------+
                              |
                              | HTTP/REST (JSON)
                              v
+------------------------------------------------------------------+
|                    AUTH GATEWAY (FastAPI)                         |
|                    Puerto: 8003                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | JWT Auth        |  | User Management  |  | File/Report      | |
|  | Middleware      |  | (SQLite)         |  | Services         | |
|  +------------------+  +------------------+  +------------------+ |
|                              |                                    |
|                    +------------------+                           |
|                    | Prediction       |                           |
|                    | Client (Router)  |                           |
|                    +------------------+                           |
+------------------------------------------------------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| PHISHING API     |  | ATO API          |  | BRUTE FORCE API  |
| Puerto: 8000     |  | Puerto: 8001     |  | Puerto: 8002     |
|                  |  |                  |  |                  |
| Gradient Boost   |  | Gradient Boost   |  | Random Forest    |
| 1,016 features   |  | 35 features      |  | 60 features      |
| TF-IDF + Numeric |  | Temporal+Behav   |  | Network Metrics  |
|                  |  |                  |  |                  |
| F1: 99.01%       |  | F1: 75.86%       |  | F1: 99.97%       |
+------------------+  +------------------+  +------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| best_model.pkl   |  | best_model.pkl   |  | random_forest.pkl|
| tfidf_vector.pkl |  | label_encoders   |  | model_info.json  |
| model_info.json  |  | model_info.json  |  |                  |
+------------------+  +------------------+  +------------------+
```

## 2.2 Estructura de Directorios del Proyecto

```
pred_model/
|
+-- Phishing/                           # MODELO 1: Deteccion de Phishing
|   +-- modeling/
|   |   +-- api/
|   |   |   +-- app.py                  # FastAPI application
|   |   |   +-- models.py               # Pydantic schemas
|   |   |   +-- predictor.py            # PhishingPredictor class
|   |   +-- outputs/
|   |   |   +-- models/
|   |   |   |   +-- best_model.pkl      # Gradient Boosting (476 KB)
|   |   |   |   +-- tfidf_vectorizer.pkl
|   |   |   +-- features/
|   |   |   +-- reports/
|   |   +-- src/
|   |       +-- features/
|   |           +-- feature_engineering.py
|   +-- processed_data/
|   |   +-- train.csv                   # 31,323 registros
|   |   +-- test.csv                    # 7,831 registros
|   +-- analysis/
|
+-- Suspicious-Login-Activity/          # MODELO 2: Account Takeover
|   +-- modeling/
|   |   +-- api/
|   |   |   +-- app.py
|   |   |   +-- models.py
|   |   |   +-- predictor.py            # AccountTakeoverPredictor
|   |   +-- outputs/
|   |   |   +-- models/
|   |   |   |   +-- best_model.pkl      # Gradient Boosting (1.5 MB)
|   |   |   |   +-- label_encoders.pkl
|   |   |   |   +-- model_info.json
|   |   +-- src/
|   |       +-- features/
|   |           +-- feature_engineering.py
|   +-- processed_data/
|   |   +-- rba_reduced.csv             # Dataset principal
|   +-- analysis/
|
+-- fuerza-bruta/                       # MODELO 3: Brute Force
|   +-- api/
|   |   +-- app.py
|   |   +-- models.py
|   |   +-- predictor.py                # BruteForcePredictor
|   +-- modeling/
|   |   +-- outputs/
|   |   |   +-- models/
|   |   |   |   +-- random_forest_*.pkl # Random Forest (1.5 MB)
|   |   |   +-- results/
|   |   +-- notebooks/
|   |   +-- src/
|   +-- processed_data/
|   |   +-- brute_force_balanced.csv    # 763,568 registros
|   +-- analysis/
|
+-- auth-gateway/                       # GATEWAY DE AUTENTICACION
|   +-- app/
|   |   +-- main.py                     # FastAPI app principal
|   |   +-- config.py                   # Configuracion
|   |   +-- database.py                 # SQLAlchemy setup
|   |   +-- models/
|   |   |   +-- user.py                 # User model
|   |   |   +-- file.py                 # UploadedFile model
|   |   |   +-- report.py               # Report model
|   |   +-- schemas/
|   |   |   +-- user.py                 # User schemas
|   |   |   +-- file.py                 # File schemas
|   |   |   +-- report.py               # Report schemas
|   |   +-- routers/
|   |   |   +-- auth.py                 # /auth/* endpoints
|   |   |   +-- users.py                # /users/* endpoints
|   |   |   +-- files.py                # /files/* endpoints
|   |   |   +-- reports.py              # /reports/* endpoints
|   |   +-- services/
|   |       +-- auth_service.py         # JWT, bcrypt
|   |       +-- file_service.py         # File management
|   |       +-- report_service.py       # Report generation
|   |       +-- prediction_client.py    # ML API client
|   +-- uploads/                        # Archivos subidos
|   +-- auth_gateway.db                 # SQLite database
|   +-- requirements.txt
|
+-- frontend/                           # DASHBOARD REACT
|   +-- src/
|   |   +-- components/
|   |   |   +-- auth/                   # Login, ProtectedRoute, RoleGuard
|   |   |   +-- dashboard/              # Dashboard, ModelSelector
|   |   |   +-- forms/                  # PhishingForm, ATOForm, BruteForceForm
|   |   |   +-- results/                # ResultsDisplay, PredictionCard
|   |   |   +-- files/                  # FileUpload, FileList
|   |   |   +-- reports/                # ReportsList, ReportDetail
|   |   |   +-- users/                  # UserManagement
|   |   |   +-- layout/                 # Sidebar, TopBar, MainLayout
|   |   +-- pages/
|   |   +-- context/
|   |   |   +-- AuthContext.jsx         # Estado de autenticacion
|   |   |   +-- DashboardContext.jsx    # Estado del dashboard
|   |   +-- services/
|   |   |   +-- authService.js          # -> localhost:8003
|   |   |   +-- phishingService.js      # -> localhost:8000
|   |   |   +-- ataquesSospechososService.js  # -> localhost:8001
|   |   |   +-- fuerzaBrutaService.js   # -> localhost:8002
|   |   +-- styles/
|   |   |   +-- theme.js                # Design tokens
|   |   |   +-- index.css
|   |   +-- App.jsx
|   |   +-- main.jsx
|   +-- package.json
|   +-- vite.config.js
|
+-- CLAUDE.md                           # Documentacion del proyecto
+-- documento_final/                    # Trabajo de grado
```

---

# PARTE 3: MODELO 1 - PHISHING EMAIL DETECTION

## 3.1 Informacion del Dataset

| Caracteristica | Valor |
|----------------|-------|
| **Nombre** | CEAS_08 |
| **Tipo** | Emails etiquetados |
| **Total registros** | 39,154 |
| **Train set** | 31,323 (80%) |
| **Test set** | 7,831 (20%) |
| **Clase Legitimo** | 44% |
| **Clase Phishing** | 56% |

## 3.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Gradient Boosting Classifier |
| **Libreria** | scikit-learn 1.8.0 |
| **Total features** | 1,016 |
| **Features TF-IDF** | 1,000 (texto) |
| **Features numericas** | 16 (metadata) |

## 3.3 Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| **F1-Score** | 99.01% |
| **Accuracy** | 98.89% |
| **Precision** | 98.73% |
| **Recall** | 99.29% |
| **ROC-AUC** | 99.90% |

## 3.4 Feature Engineering

### Features de Texto (TF-IDF)
- **Vectorizador:** TfidfVectorizer
- **max_features:** 1,000
- **ngram_range:** (1, 2) - unigramas y bigramas
- **min_df:** 5 (minimo 5 documentos)

### Features Numericas (16 total)
1. **subject_length** - Longitud del asunto
2. **body_length** - Longitud del cuerpo
3. **subject_word_count** - Palabras en asunto
4. **body_word_count** - Palabras en cuerpo
5. **subject_special_chars** - Caracteres especiales en asunto
6. **body_special_chars** - Caracteres especiales en cuerpo
7. **url_count** - Cantidad de URLs
8. **has_urls** - Indicador binario de URLs
9. **sender_domain_length** - Longitud del dominio del remitente
10. **is_common_domain** - Si es dominio comun (gmail, yahoo, etc.)
11. **phishing_keyword_count** - Conteo de palabras sospechosas
12. **legitimate_keyword_count** - Conteo de palabras legitimas
13. **sentiment_score** - Score basado en keywords
14. **uppercase_ratio** - Proporcion de mayusculas
15. **exclamation_count** - Cantidad de signos de exclamacion
16. **question_count** - Cantidad de signos de interrogacion

### Keywords de Phishing Detectadas
```python
PHISHING_KEYWORDS = [
    'urgent', 'free', 'click', 'verify', 'password',
    'claim', 'prize', 'winner', 'bank', 'account',
    'suspended', 'limited', 'confirm', 'update', 'secure'
]
```

## 3.5 Entrada de API (Schema)

```python
class EmailInput(BaseModel):
    sender: str           # Email del remitente
    receiver: str = ""    # Email del destinatario (opcional)
    subject: str          # Asunto del email
    body: str             # Cuerpo del email
    urls: int = 0         # Indicador de URLs (0 o 1)
```

## 3.6 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Phishing",
    "confidence": 0.9927,
    "probability_legitimate": 0.0073,
    "probability_phishing": 0.9927,
    "metadata": {
        "model": "Gradient Boosting",
        "version": "1.0.0",
        "features_count": 1016,
        "timestamp": "2026-01-10T15:30:45.123Z",
        "processing_time_ms": 45.2
    }
}
```

## 3.7 Endpoints de la API

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /predict | Prediccion individual |
| POST | /predict/batch | Prediccion por lotes |
| GET | /model/info | Informacion del modelo |

---

# PARTE 4: MODELO 2 - ACCOUNT TAKEOVER DETECTION

## 4.1 Informacion del Dataset

| Caracteristica | Valor |
|----------------|-------|
| **Nombre** | RBA Dataset (Risk-Based Authentication) |
| **Tipo** | Registros de login |
| **Total registros** | 85,141 |
| **Train set** | 68,112 (80%) |
| **Test set** | 17,029 (20%) |
| **Clase Normal** | 99.83% |
| **Clase ATO** | 0.17% |

**NOTA IMPORTANTE:** Dataset fuertemente desbalanceado. Solo 0.17% son Account Takeover.

## 4.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Gradient Boosting Classifier |
| **Libreria** | scikit-learn 1.8.0 |
| **Total features** | 35 |
| **Threshold optimo** | 0.5 |

## 4.3 Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| **F1-Score** | 75.86% |
| **Accuracy** | 99.88% |
| **Precision** | 73.33% |
| **Recall** | 78.57% |
| **ROC-AUC** | 98.06% |
| **Average Precision** | 79.01% |

### Matriz de Confusion (Test Set)
```
                  Predicho
              Normal    ATO
Real Normal   16,975     12    (FP Rate: 0.07%)
Real ATO           9     33    (FN Rate: 21.43%)
```

## 4.4 Feature Engineering

### Features Temporales (7)
1. **hour** - Hora del login (0-23)
2. **day_of_week** - Dia de la semana (0-6)
3. **day_of_month** - Dia del mes (1-31)
4. **month** - Mes (1-12)
5. **is_weekend** - Es fin de semana (0/1)
6. **is_night** - Es horario nocturno (0/1)
7. **is_business_hours** - Es horario laboral (0/1)

### Features de Comportamiento (8)
1. **ip_changed** - Cambio de IP desde ultimo login
2. **country_changed** - Cambio de pais (FEATURE MAS IMPORTANTE)
3. **browser_changed** - Cambio de navegador
4. **device_changed** - Cambio de dispositivo
5. **os_changed** - Cambio de sistema operativo
6. **time_since_last_login_hours** - Horas desde ultimo login
7. **region_changed** - Cambio de region
8. **city_changed** - Cambio de ciudad

### Features Geograficas (3)
1. **country_risk_score** - Score de riesgo del pais
2. **city_risk_score** - Score de riesgo de la ciudad
3. **impossible_travel** - Viaje imposible detectado

### Features de Red (4)
1. **rtt** - Round Trip Time
2. **asn** - Autonomous System Number
3. **is_attack_ip** - IP conocida como maliciosa
4. **port** - Puerto utilizado

### Features Agregados (7)
1. **logins_per_user_day** - Logins del usuario por dia
2. **logins_per_ip_hour** - Logins por IP por hora
3. **unique_countries_per_user_day** - Paises unicos por usuario/dia
4. **users_per_ip** - Usuarios por IP
5. **failed_logins_last_hour** - Logins fallidos ultima hora
6. **unique_devices_per_user** - Dispositivos unicos por usuario
7. **unique_browsers_per_user** - Navegadores unicos por usuario

### Features Categoricos (6) - Label Encoded
1. **Browser Name**
2. **Browser Version**
3. **OS Name**
4. **OS Version**
5. **Device Type**
6. **Country/Region/City**

## 4.5 Insight Critico

> **98.6% de los Account Takeovers tienen cambio de pais**

Este es el feature mas discriminante. El modelo aprende que un cambio de pais es un fuerte indicador de ATO.

> **99.3% de los ATOs son logins exitosos**

Los Account Takeover NO son intentos de fuerza bruta. Son accesos exitosos desde ubicaciones anomalas.

## 4.6 Entrada de API (Schema)

```python
class LoginInput(BaseModel):
    user_id: str              # ID del usuario
    ip_address: str           # Direccion IP
    country: str              # Codigo pais (2 chars)
    region: str               # Region/Estado
    city: str                 # Ciudad
    browser: str              # Nombre del navegador
    os: str                   # Sistema operativo
    device: str               # Tipo de dispositivo
    login_successful: int     # Login exitoso (0/1)
    is_attack_ip: int         # IP conocida maliciosa (0/1)
    asn: int                  # Autonomous System Number
    rtt: float                # Round Trip Time (ms)
```

## 4.7 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Account Takeover",
    "confidence": 0.8532,
    "probability_normal": 0.1468,
    "probability_ato": 0.8532,
    "threshold_used": 0.5,
    "metadata": {
        "model": "Gradient Boosting",
        "version": "1.0.0",
        "features_count": 35,
        "timestamp": "2026-01-15T12:00:00Z",
        "processing_time_ms": 32.1
    }
}
```

---

# PARTE 5: MODELO 3 - BRUTE FORCE DETECTION

## 5.1 Informacion del Dataset

| Caracteristica | Valor |
|----------------|-------|
| **Nombre** | CSE-CIC-IDS2018 |
| **Tipo** | Network flows |
| **Total registros** | 763,568 |
| **Train set** | 610,854 (80%) |
| **Test set** | 152,714 (20%) |
| **Clase Benign** | 50% (381,784) |
| **Clase Brute Force** | 50% (381,784) |

### Tipos de Ataques Incluidos
- FTP Brute Force
- SSH Brute Force
- Web Brute Force
- XSS Brute Force

## 5.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Random Forest Classifier |
| **Libreria** | scikit-learn 1.8.0 |
| **Total features** | 60 |
| **Normalizacion** | Min-Max (0-1) |

## 5.3 Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| **F1-Score** | 99.97% |
| **Accuracy** | 99.97% |
| **Precision** | 100.00% |
| **Recall** | 99.94% |
| **ROC-AUC** | 99.9996% |

### Matriz de Confusion (Test Set: 152,714)
```
                    Predicho
                Benign    Attack
Real Benign     76,353       4    (FP: 4)
Real Attack          5  76,352    (FN: 5)

Total Correctos: 152,705 / 152,714 (99.9941%)
```

## 5.4 Features Principales (60 total)

### Features de Paquetes
- **tot_fwd_pkts** - Total paquetes forward
- **tot_bwd_pkts** - Total paquetes backward
- **totlen_fwd_pkts** - Longitud total forward
- **totlen_bwd_pkts** - Longitud total backward
- **fwd_pkt_len_max/min/mean/std** - Estadisticas de longitud forward
- **bwd_pkt_len_max/min/mean/std** - Estadisticas de longitud backward

### Features de Flujo
- **flow_duration** - Duracion del flujo
- **flow_byts_s** - Bytes por segundo
- **flow_pkts_s** - Paquetes por segundo
- **flow_iat_mean/std/max/min** - Inter-Arrival Time

### Features TCP Flags
- **syn_flag_cnt** - Conteo flags SYN
- **fin_flag_cnt** - Conteo flags FIN
- **rst_flag_cnt** - Conteo flags RST
- **psh_flag_cnt** - Conteo flags PSH
- **ack_flag_cnt** - Conteo flags ACK
- **urg_flag_cnt** - Conteo flags URG

### Features Direccionales
- **fwd_pkts_s** - Paquetes forward por segundo
- **bwd_pkts_s** - Paquetes backward por segundo
- **fwd_iat_tot/mean/std/max/min** - IAT forward
- **bwd_iat_tot/mean/std/max/min** - IAT backward

## 5.5 Features Mas Discriminantes

| Feature | Ratio Ataque/Normal | Interpretacion |
|---------|---------------------|----------------|
| **Bwd Pkts/s** | 112.7x | Velocidad extrema de bots |
| **Flow Pkts/s** | 24.7x | Ataques automatizados |
| **PSH Flag Cnt** | 1.96x | Firma de herramientas |
| **Flow Duration** | 0.01x | Intentos muy rapidos |

## 5.6 Entrada de API (Schema)

```python
class NetworkFlowInput(BaseModel):
    dst_port: float           # Puerto destino (normalizado 0-1)
    protocol: float           # Protocolo (normalizado 0-1)
    timestamp: float          # Timestamp (normalizado 0-1)
    flow_duration: float      # Duracion del flujo
    tot_fwd_pkts: float       # Total paquetes forward
    tot_bwd_pkts: float       # Total paquetes backward
    totlen_fwd_pkts: float    # Longitud total forward
    totlen_bwd_pkts: float    # Longitud total backward
    # ... 52 features mas ...
    idle_std: float           # Desviacion estandar idle
    # Todos normalizados entre 0 y 1
```

## 5.7 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Brute Force Attack",
    "confidence": 0.9998,
    "probability_benign": 0.0002,
    "probability_attack": 0.9998,
    "metadata": {
        "model": "Random Forest",
        "version": "1.0.0",
        "features_count": 60,
        "timestamp": "2026-01-17T08:15:30Z",
        "processing_time_ms": 28.5
    }
}
```

---

# PARTE 6: AUTH GATEWAY (Sistema de Autenticacion)

## 6.1 Proposito

El Auth Gateway actua como punto central de:
- Autenticacion de usuarios (JWT)
- Gestion de roles (admin/analyst)
- Gestion de archivos subidos
- Generacion de reportes
- Enrutamiento a APIs de ML

## 6.2 Modelos de Base de Datos

### Tabla: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'admin' o 'analyst'
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: uploaded_files
```sql
CREATE TABLE uploaded_files (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_by INTEGER REFERENCES users(id),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    row_count INTEGER,
    columns_json TEXT,          -- JSON con nombres de columnas
    detected_model VARCHAR(50)  -- 'phishing', 'ato', 'brute_force'
);
```

### Tabla: reports
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    file_id INTEGER REFERENCES uploaded_files(id),
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_records INTEGER,
    threats_detected INTEGER,
    benign_count INTEGER,
    avg_confidence FLOAT,
    results_json TEXT,          -- JSON con resultados completos
    status VARCHAR(20)          -- 'pending', 'processing', 'completed', 'failed'
);
```

## 6.3 Sistema de Autenticacion

### Configuracion JWT
```python
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas
```

### Flujo de Autenticacion
1. Usuario envia username/password a POST /auth/login
2. AuthService valida credenciales con bcrypt
3. Si valido, genera JWT con claims: {sub: username, role: role, exp: expiration}
4. Frontend almacena token en localStorage
5. Requests subsiguientes incluyen header: Authorization: Bearer <token>
6. Middleware valida token en cada request protegido

## 6.4 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **admin** | Subir archivos, generar reportes, gestionar usuarios, ver todo |
| **analyst** | Ver reportes, prediccion manual, ver dashboard |

## 6.5 Usuarios por Defecto

```
Usuario Admin:
  - username: admin
  - password: admin123
  - email: admin@company.com
  - role: admin

Usuario Analyst:
  - username: analyst
  - password: analyst123
  - email: analyst@company.com
  - role: analyst
```

## 6.6 Endpoints de la API

### Autenticacion (/auth)
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| POST | /auth/login | Login, retorna JWT | Publico |
| POST | /auth/login/json | Login con JSON body | Publico |
| GET | /auth/me | Info usuario actual | Autenticado |

### Usuarios (/users)
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| GET | /users | Listar usuarios | Admin |
| POST | /users | Crear usuario | Admin |
| PUT | /users/{id} | Actualizar usuario | Admin |
| DELETE | /users/{id} | Eliminar usuario | Admin |

### Archivos (/files)
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| POST | /files/upload | Subir CSV/Excel | Admin |
| GET | /files | Listar archivos | Admin |
| GET | /files/{id} | Detalle archivo | Admin |
| DELETE | /files/{id} | Eliminar archivo | Admin |

### Reportes (/reports)
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| GET | /reports | Listar reportes | Todos |
| GET | /reports/{id} | Detalle reporte | Todos |
| POST | /reports/generate | Generar reporte | Admin |

## 6.7 Configuracion de APIs de ML

```python
# config.py
PHISHING_API_URL = "http://localhost:8000"
ATO_API_URL = "http://localhost:8001"
BRUTE_FORCE_API_URL = "http://localhost:8002"
```

---

# PARTE 7: FRONTEND (Dashboard React)

## 7.1 Rutas de la Aplicacion

| Ruta | Pagina | Autenticacion | Rol |
|------|--------|---------------|-----|
| /login | LoginPage | NO | - |
| /dashboard | DashboardPage (Overview) | SI | Todos |
| /dashboard/predict | DashboardPage (Prediccion) | SI | Todos |
| /files | FilesPage | SI | Admin |
| /reports | ReportsPage | SI | Todos |
| /users | UsersPage | SI | Admin |

## 7.2 Componentes Principales

### Layout
- **MainLayout** - Estructura principal con Sidebar y TopBar
- **Sidebar** - Menu de navegacion lateral
- **TopBar** - Barra superior con info de usuario

### Autenticacion
- **LoginForm** - Formulario de login
- **ProtectedRoute** - HOC para rutas protegidas
- **RoleGuard** - HOC para verificar roles

### Dashboard
- **Dashboard** - Contenedor principal
- **DashboardOverview** - Estadisticas y resumen
- **ModelSelector** - Selector de modelo (3 botones)

### Formularios de Prediccion
- **PhishingForm** - Formulario para emails
- **AtaquesSospechososForm** - Formulario para logins
- **FuerzaBrutaForm** - Formulario para network flows

### Resultados
- **ResultsDisplay** - Contenedor de resultados
- **PredictionCard** - Tarjeta con prediccion
- **ConfidenceMetrics** - Barra de confianza

### Gestion
- **FileUpload** - Subida de archivos (drag & drop)
- **FileList** - Lista de archivos
- **ReportsList** - Lista de reportes
- **ReportDetail** - Detalle con graficos
- **UserManagement** - CRUD de usuarios

## 7.3 Servicios (API Clients)

```javascript
// authService.js -> localhost:8003
login(username, password)
logout()
getCurrentUser()

// phishingService.js -> localhost:8000
predict(emailData)
predictBatch(emails)
getModelInfo()

// ataquesSospechososService.js -> localhost:8001
predict(loginData)
predictBatch(logins)
getModelInfo()

// fuerzaBrutaService.js -> localhost:8002
predict(flowData)
predictBatch(flows)
getModelInfo()

// fileService.js -> localhost:8003
uploadFile(file)
getFiles()
deleteFile(id)

// reportService.js -> localhost:8003
getReports()
getReport(id)
generateReport(fileId, modelType)
```

## 7.4 Contexto de Autenticacion

```javascript
// AuthContext.jsx
{
    user: {
        username: string,
        role: string,
        exp: number
    },
    token: string,
    login: async (username, password) => {success, error},
    logout: () => void,
    isAuthenticated: boolean,
    hasRole: (role) => boolean,
    isAdmin: () => boolean,
    loading: boolean
}
```

## 7.5 Design System (Paleta de Colores)

### Colores Primarios
```css
--primary-blue: #00498C;    /* Azul BCP */
--primary-orange: #FF7800;  /* Naranja BCP (acento) */
```

### Colores de Fondo
```css
--bg-primary: #191E29;      /* Fondo principal oscuro */
--bg-secondary: #132D46;    /* Fondo secundario */
--bg-elevated: #1E3A5F;     /* Fondo elevado */
```

### Colores Semanticos
```css
--color-success: #10B981;   /* Verde exito */
--color-danger: #EF4444;    /* Rojo peligro */
--color-warning: #F59E0B;   /* Amarillo advertencia */
--color-info: #3B82F6;      /* Azul informacion */
```

---

# PARTE 8: FLUJOS DEL SISTEMA

## 8.1 Flujo de Prediccion Manual

```
1. Usuario inicia sesion en Frontend
2. Selecciona modelo (Phishing/ATO/Brute Force)
3. Completa formulario con datos
4. Frontend envia POST a API del modelo correspondiente
5. API procesa:
   a. Valida entrada con Pydantic
   b. Aplica feature engineering
   c. Carga modelo entrenado (.pkl)
   d. Ejecuta prediccion
   e. Calcula probabilidades y confianza
6. API retorna resultado JSON
7. Frontend muestra:
   - Prediccion (Normal/Amenaza)
   - Porcentaje de confianza
   - Probabilidades por clase
   - Metadata (tiempo, version)
```

## 8.2 Flujo de Prediccion Batch (Admin)

```
1. Admin sube archivo CSV/Excel
2. Auth Gateway:
   a. Guarda archivo en /uploads
   b. Detecta modelo automaticamente por columnas
   c. Registra en tabla uploaded_files
3. Admin genera reporte:
   a. Selecciona archivo y modelo
   b. POST /reports/generate
4. Auth Gateway:
   a. Lee archivo
   b. Formatea datos para API
   c. Llama endpoint /predict/batch del modelo
5. API de ML:
   a. Procesa todos los registros
   b. Retorna predicciones + tiempo total
6. Auth Gateway:
   a. Calcula estadisticas (amenazas, benignos, confianza promedio)
   b. Guarda en tabla reports
7. Frontend muestra:
   - Total procesados
   - Amenazas detectadas
   - Porcentaje de amenazas
   - Graficos de distribucion
```

## 8.3 Flujo de Autenticacion

```
1. Usuario accede a /login
2. Ingresa username y password
3. Frontend envia POST /auth/login
4. Auth Gateway:
   a. Busca usuario en BD
   b. Verifica password con bcrypt
   c. Si valido, genera JWT
   d. Retorna {access_token, token_type}
5. Frontend:
   a. Guarda token en localStorage
   b. Decodifica JWT para obtener user info
   c. Redirige a /dashboard
6. Requests subsiguientes:
   a. Interceptor agrega header Authorization
   b. Backend valida JWT en cada request
```

---

# PARTE 9: COMPARATIVA DE MODELOS

## 9.1 Tabla Comparativa Completa

| Aspecto | Phishing | Account Takeover | Brute Force |
|---------|----------|------------------|-------------|
| **Dataset** | CEAS_08 | RBA Dataset | CSE-CIC-IDS2018 |
| **Registros** | 39,154 | 85,141 | 763,568 |
| **Balance** | 44/56% | 0.17/99.83% | 50/50% |
| **Algoritmo** | Gradient Boosting | Gradient Boosting | Random Forest |
| **Features** | 1,016 | 35 | 60 |
| **F1-Score** | 99.01% | 75.86% | 99.97% |
| **Accuracy** | 98.89% | 99.88% | 99.97% |
| **Precision** | 98.73% | 73.33% | 100% |
| **Recall** | 99.29% | 78.57% | 99.94% |
| **ROC-AUC** | 99.90% | 98.06% | 99.9996% |

## 9.2 Analisis por Modelo

### Phishing Detection
- **Fortaleza:** Muy alto rendimiento en todas las metricas
- **Tecnica clave:** TF-IDF para vectorizacion de texto
- **Mejor para:** Emails con texto abundante

### Account Takeover
- **Desafio:** Dataset extremadamente desbalanceado
- **Feature clave:** Cambio de pais (98.6% de ATOs)
- **Consideracion:** F1 menor por el desbalance, pero ROC-AUC alto

### Brute Force
- **Fortaleza:** Casi perfecto (99.97%)
- **Tecnica clave:** Features de trafico de red normalizados
- **Mejor para:** Deteccion en tiempo real de patrones de red

---

# PARTE 10: METODOLOGIAS UTILIZADAS

## 10.1 Metodologia de Desarrollo: SCRUM

### Roles del Equipo
- **Product Owner:** Define requerimientos y prioridades
- **Scrum Master:** Facilita proceso y remueve impedimentos
- **Development Team:** Desarrolla el producto

### Artefactos
- **Product Backlog:** Lista priorizada de requerimientos
- **Sprint Backlog:** Tareas del sprint actual
- **Incremento:** Producto funcional al final de cada sprint

### Eventos
- **Sprint Planning:** Planificacion del sprint
- **Daily Scrum:** Reunion diaria de 15 minutos
- **Sprint Review:** Demostracion del incremento
- **Sprint Retrospective:** Mejora continua

## 10.2 Metodologia de Machine Learning: CRISP-DM

### Fase 1: Comprension del Negocio
- Identificacion de vectores de amenaza prioritarios
- Definicion de objetivos de prediccion
- Criterios de exito (metricas objetivo)

### Fase 2: Comprension de los Datos
- Analisis exploratorio de datasets
- Identificacion de variables relevantes
- Evaluacion de calidad de datos

### Fase 3: Preparacion de los Datos
- Limpieza de valores faltantes
- Tratamiento de outliers
- Balanceo de clases (cuando necesario)
- Feature engineering

### Fase 4: Modelado
- Seleccion de algoritmos candidatos
- Entrenamiento de modelos
- Optimizacion de hiperparametros
- Validacion cruzada

### Fase 5: Evaluacion
- Evaluacion con conjunto de prueba
- Calculo de metricas (F1, Precision, Recall, ROC-AUC)
- Seleccion del mejor modelo

### Fase 6: Implementacion
- Serializacion de modelos (.pkl)
- Desarrollo de APIs
- Integracion con sistema
- Monitoreo en produccion

---

# PARTE 11: REQUERIMIENTOS DEL SISTEMA

## 11.1 Requerimientos Funcionales

| ID | Requerimiento |
|----|---------------|
| RF-01 | El sistema debe permitir la autenticacion de usuarios mediante JWT |
| RF-02 | El sistema debe soportar dos roles: admin y analyst |
| RF-03 | El sistema debe predecir emails de phishing con >95% F1-Score |
| RF-04 | El sistema debe detectar Account Takeover basado en patrones de comportamiento |
| RF-05 | El sistema debe identificar ataques de fuerza bruta en trafico de red |
| RF-06 | El sistema debe permitir predicciones individuales y por lotes |
| RF-07 | El sistema debe generar reportes con estadisticas de prediccion |
| RF-08 | El sistema debe permitir la subida de archivos CSV/Excel |
| RF-09 | El sistema debe mostrar un dashboard con estadisticas |
| RF-10 | El sistema debe gestionar usuarios (CRUD) para administradores |

## 11.2 Requerimientos No Funcionales

| ID | Requerimiento |
|----|---------------|
| RNF-01 | Tiempo de respuesta de prediccion individual < 500ms |
| RNF-02 | Soporte para archivos de hasta 50MB |
| RNF-03 | Disponibilidad del sistema 99.5% |
| RNF-04 | Interfaz responsive para dispositivos moviles |
| RNF-05 | Tokens JWT con expiracion de 8 horas |
| RNF-06 | Almacenamiento seguro de contrasenas (bcrypt) |
| RNF-07 | APIs documentadas con Swagger/OpenAPI |
| RNF-08 | Logging de todas las operaciones criticas |

---

# PARTE 12: INSTRUCCIONES DE EJECUCION

## 12.1 Requisitos Previos
- Python 3.12
- Node.js 18+
- Virtual environment de Python

## 12.2 Iniciar el Sistema Completo

```bash
# Terminal 1: Activar venv e iniciar API Phishing
source /home/megalodon/dev/cbproy/venv/bin/activate
cd /home/megalodon/dev/cbproy/pred_model/Phishing/modeling/api
uvicorn app:app --reload --port 8000

# Terminal 2: API Account Takeover
source /home/megalodon/dev/cbproy/venv/bin/activate
cd /home/megalodon/dev/cbproy/pred_model/Suspicious-Login-Activity/modeling/api
uvicorn app:app --reload --port 8001

# Terminal 3: API Brute Force
source /home/megalodon/dev/cbproy/venv/bin/activate
cd /home/megalodon/dev/cbproy/pred_model/fuerza-bruta/api
uvicorn app:app --reload --port 8002

# Terminal 4: Auth Gateway
source /home/megalodon/dev/cbproy/venv/bin/activate
cd /home/megalodon/dev/cbproy/pred_model/auth-gateway
uvicorn app.main:app --reload --port 8003

# Terminal 5: Frontend React
cd /home/megalodon/dev/cbproy/pred_model/frontend
npm install  # Solo la primera vez
npm run dev
```

## 12.3 Acceso al Sistema

| Componente | URL |
|------------|-----|
| Frontend | http://localhost:5173 |
| Phishing API Docs | http://localhost:8000/docs |
| ATO API Docs | http://localhost:8001/docs |
| Brute Force API Docs | http://localhost:8002/docs |
| Auth Gateway Docs | http://localhost:8003/docs |

## 12.4 Credenciales de Prueba

```
Administrador:
  Usuario: admin
  Contrasena: admin123

Analista:
  Usuario: analyst
  Contrasena: analyst123
```

---

# PARTE 13: CONCLUSIONES TECNICAS

## 13.1 Logros del Sistema

1. **Tres modelos de ML funcionales** con metricas de produccion
2. **Arquitectura de microservicios** escalable y mantenible
3. **Sistema de autenticacion robusto** con JWT y roles
4. **Dashboard intuitivo** para predicciones manuales y por lotes
5. **APIs documentadas** con Swagger/OpenAPI
6. **Integracion completa** entre todos los componentes

## 13.2 Metricas Alcanzadas vs Objetivos

| Modelo | Objetivo F1 | F1 Alcanzado | Estado |
|--------|-------------|--------------|--------|
| Phishing | >95% | 99.01% | SUPERADO |
| Account Takeover | >70% | 75.86% | SUPERADO |
| Brute Force | >95% | 99.97% | SUPERADO |

## 13.3 Tecnologias Clave Implementadas

- **Machine Learning:** scikit-learn (Gradient Boosting, Random Forest)
- **NLP:** TF-IDF Vectorization para analisis de texto
- **Backend:** FastAPI con arquitectura de microservicios
- **Autenticacion:** JWT con bcrypt para hashing
- **Base de Datos:** SQLite con SQLAlchemy ORM
- **Frontend:** React con Bootstrap y Design Tokens

---

**FIN DEL DOCUMENTO**

*Este documento contiene toda la informacion tecnica del Sistema de Prediccion de Incidentes de Ciberseguridad para ser utilizado en la actualizacion del trabajo de grado.*
