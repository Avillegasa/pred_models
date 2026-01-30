# DIAGRAMAS DEL SISTEMA PREDICTIVO DE INCIDENTES DE CIBERSEGURIDAD

**Proyecto:** Sistema de Deteccion de Incidentes de Ciberseguridad
**Institucion:** Escuela Militar de Ingenieria - Bolivia
**Caso de Estudio:** Banco de Credito de Bolivia
**Fecha:** 2026-01-30

---

# INDICE DE DIAGRAMAS

1. [Diagrama de Componentes](#1-diagrama-de-componentes)
2. [Diagrama de Clases](#2-diagrama-de-clases)
3. [Diagrama de Base de Datos (ER)](#3-diagrama-de-base-de-datos-er)
4. [Diagrama de Casos de Uso de Alto Nivel](#4-diagrama-de-casos-de-uso-de-alto-nivel)
5. [Diagramas de Casos de Uso Expandidos](#5-diagramas-de-casos-de-uso-expandidos)
6. [Diagramas de Secuencia](#6-diagramas-de-secuencia)
7. [Diagrama de Flujo del Proceso Actual](#7-diagrama-de-flujo-del-proceso-actual)
8. [Diagrama de Flujo del Proceso Propuesto](#8-diagrama-de-flujo-del-proceso-propuesto)
9. [Diagrama de Navegacion de Pantallas](#9-diagrama-de-navegacion-de-pantallas)
10. [Diagrama de Flujo CRISP-DM Aplicado](#10-diagrama-de-flujo-crisp-dm-aplicado)
11. [Diagrama de Pipeline de Machine Learning](#11-diagrama-de-pipeline-de-machine-learning)

---

# 1. DIAGRAMA DE COMPONENTES

## 1.1 Arquitectura General del Sistema

```
+===========================================================================+
|                        SISTEMA PREDICTIVO DE CIBERSEGURIDAD                |
+===========================================================================+
|                                                                            |
|  +--------------------------------------------------------------------+   |
|  |                    CAPA DE PRESENTACION (Frontend)                  |   |
|  |                         React 19.2.0 + Vite                         |   |
|  |                           Puerto: 5173                              |   |
|  |  +-------------+ +-------------+ +-------------+ +-------------+   |   |
|  |  |   Inicio    | |    Panel    | |  Reportes   | |   Alertas   |   |   |
|  |  |   Sesion    | |  Principal  | |             | |             |   |   |
|  |  +-------------+ +-------------+ +-------------+ +-------------+   |   |
|  |  +-------------+ +-------------+ +-------------+                   |   |
|  |  |  Archivos   | |  Usuarios   | | Formularios |                   |   |
|  |  |             | |             | | Prediccion  |                   |   |
|  |  +-------------+ +-------------+ +-------------+                   |   |
|  +--------------------------------------------------------------------+   |
|                                    |                                       |
|                                    | HTTP/REST + JSON                      |
|                                    v                                       |
|  +--------------------------------------------------------------------+   |
|  |                    CAPA DE APLICACION (Backend)                     |   |
|  |                                                                     |   |
|  |  +--------------------------------------------------------------+  |   |
|  |  |                    AUTH GATEWAY (FastAPI)                     |  |   |
|  |  |                        Puerto: 8003                           |  |   |
|  |  |  +------------+ +------------+ +------------+ +------------+ |  |   |
|  |  |  |   Enrut.   | |   Enrut.   | |   Enrut.   | |   Enrut.   | |  |   |
|  |  |  |    Auth    | |  Archivos  | |  Reportes  | |  Alertas   | |  |   |
|  |  |  +------------+ +------------+ +------------+ +------------+ |  |   |
|  |  |  +------------+ +------------+ +------------+                |  |   |
|  |  |  |   Enrut.   | |  Cliente   | |  Detector  |                |  |   |
|  |  |  |  Usuarios  | | Prediccion | |  Columnas  |                |  |   |
|  |  |  +------------+ +------------+ +------------+                |  |   |
|  |  +--------------------------------------------------------------+  |   |
|  |                         |          |          |                     |   |
|  |            +------------+          |          +------------+        |   |
|  |            v                       v                       v        |   |
|  |  +----------------+    +----------------+    +----------------+     |   |
|  |  |  PHISHING API  |    |    ATO API     |    | BRUTE FORCE API|     |   |
|  |  |  Puerto: 8000  |    |  Puerto: 8001  |    |  Puerto: 8002  |     |   |
|  |  |                |    |                |    |                |     |   |
|  |  | +-----------+  |    | +-----------+  |    | +-----------+  |     |   |
|  |  | | Predictor |  |    | | Predictor |  |    | | Predictor |  |     |   |
|  |  | +-----------+  |    | +-----------+  |    | +-----------+  |     |   |
|  |  | +-----------+  |    | +-----------+  |    | +-----------+  |     |   |
|  |  | |Ingenieria |  |    | |Ingenieria |  |    | |Ingenieria |  |     |   |
|  |  | |de Caract. |  |    | |de Caract. |  |    | |de Caract. |  |     |   |
|  |  | +-----------+  |    | +-----------+  |    | +-----------+  |     |   |
|  |  +----------------+    +----------------+    +----------------+     |   |
|  +--------------------------------------------------------------------+   |
|                                    |                                       |
|                                    v                                       |
|  +--------------------------------------------------------------------+   |
|  |                       CAPA DE DATOS                                 |   |
|  |                                                                     |   |
|  |  +------------------+    +------------------+    +----------------+ |   |
|  |  |     SQLite       |    |   Modelos ML     |    |   Datasets     | |   |
|  |  | auth_gateway.db  |    |    (*.pkl)       |    |   (*.csv)      | |   |
|  |  |                  |    |                  |    |                | |   |
|  |  | - users          |    | - best_model.pkl |    | - train.csv    | |   |
|  |  | - uploaded_files |    | - tfidf.pkl      |    | - test.csv     | |   |
|  |  | - reports        |    | - encoders.pkl   |    | - balanced.csv | |   |
|  |  | - alerts         |    |                  |    |                | |   |
|  |  +------------------+    +------------------+    +----------------+ |   |
|  +--------------------------------------------------------------------+   |
|                                                                            |
+============================================================================+
```

## 1.2 Interfaces entre Componentes

| Componente Origen | Componente Destino | Interfaz | Protocolo | Puerto |
|-------------------|-------------------|----------|-----------|--------|
| Frontend | Auth Gateway | REST API | HTTP/JSON | 8003 |
| Frontend | Phishing API | REST API | HTTP/JSON | 8000 |
| Frontend | ATO API | REST API | HTTP/JSON | 8001 |
| Frontend | Brute Force API | REST API | HTTP/JSON | 8002 |
| Auth Gateway | Phishing API | REST API | HTTP/JSON | 8000 |
| Auth Gateway | ATO API | REST API | HTTP/JSON | 8001 |
| Auth Gateway | Brute Force API | REST API | HTTP/JSON | 8002 |
| Auth Gateway | SQLite | ORM | SQLAlchemy | - |
| APIs ML | Modelos (.pkl) | File I/O | joblib/pickle | - |

---

# 2. DIAGRAMA DE CLASES

## 2.1 Modelo de Dominio Principal

```
+=====================================================================+
|                        DIAGRAMA DE CLASES                            |
+=====================================================================+

+---------------------------+          +---------------------------+
|         <<Entity>>        |          |         <<Entity>>        |
|           User            |          |       UploadedFile        |
+---------------------------+          +---------------------------+
| - id: Integer [PK]        |          | - id: Integer [PK]        |
| - username: String(50)    |  1    *  | - filename: String(255)   |
| - email: String(100)      |<>------->| - original_filename: Str  |
| - password_hash: Str(255) |          | - file_path: String(500)  |
| - role: Enum(admin,analyst)|         | - uploaded_by: Integer[FK]|
| - full_name: String(100)  |          | - uploaded_at: DateTime   |
| - is_active: Boolean      |          | - row_count: Integer      |
| - created_at: DateTime    |          | - columns_json: Text      |
+---------------------------+          | - detected_model: String  |
| + authenticate()          |          +---------------------------+
| + has_permission()        |          | + detect_model_type()     |
| + change_password()       |          | + get_columns()           |
+---------------------------+          +---------------------------+
            |                                      |
            | 1                                    | 1
            |                                      |
            v *                                    v *
+---------------------------+          +---------------------------+
|         <<Entity>>        |          |         <<Entity>>        |
|          Report           |<---------|           Alert           |
+---------------------------+   1   *  +---------------------------+
| - id: Integer [PK]        |          | - id: Integer [PK]        |
| - title: String(255)      |          | - title: String(255)      |
| - model_type: String(50)  |          | - description: Text       |
| - file_id: Integer [FK]   |          | - severity: Enum          |
| - created_by: Integer[FK] |          | - status: Enum            |
| - created_at: DateTime    |          | - model_type: String(50)  |
| - total_records: Integer  |          | - report_id: Integer [FK] |
| - threats_detected: Int   |          | - prediction_index: Int   |
| - benign_count: Integer   |          | - confidence: Float       |
| - avg_confidence: Float   |          | - prediction_label: Str   |
| - results_json: Text      |          | - risk_level: String      |
| - status: Enum            |          | - raw_data_json: Text     |
+---------------------------+          | - created_at: DateTime    |
| + generate()              |          | - read_at: DateTime       |
| + get_statistics()        |          | - acknowledged_at: DT     |
| + export_csv()            |          | - acknowledged_by: Int[FK]|
+---------------------------+          +---------------------------+
                                       | + mark_as_read()          |
                                       | + acknowledge()           |
                                       | + get_explanation()       |
                                       +---------------------------+

+=====================================================================+
|                    CLASES DE MODELOS DE ML                           |
+=====================================================================+

+---------------------------+     +---------------------------+
|       <<Abstract>>        |     |         <<Value>>         |
|      BasePredictor        |     |       Prediction          |
+---------------------------+     +---------------------------+
| # model: sklearn.Model    |     | - prediction: Integer     |
| # feature_names: List     |     | - prediction_label: Str   |
| # model_info: Dict        |     | - confidence: Float       |
+---------------------------+     | - probabilities: Dict     |
| + load_model()            |     | - explanation: Explanation|
| + predict()               |     | - metadata: Dict          |
| + predict_batch()         |     +---------------------------+
| + generate_explanation()  |
| + get_model_info()        |
+---------------------------+
            ^
            |
  +---------+---------+---------+
  |                   |         |
  v                   v         v
+----------------+ +----------------+ +----------------+
| PhishingPred.  | | ATOPredictor   | | BruteForcePred |
+----------------+ +----------------+ +----------------+
| - tfidf_vect   | | - label_enc    | | - scaler       |
| - threshold    | | - smote_config | | - features     |
+----------------+ +----------------+ +----------------+
| + extract_urls()| + check_country()| + calc_rates()  |
| + calc_tfidf() | + calc_risk()    | + norm_features()|
+----------------+ +----------------+ +----------------+

+---------------------------+
|         <<Value>>         |
|       Explanation         |
+---------------------------+
| - risk_indicators: List   |
| - summary: String         |
| - total_indicators: Int   |
| - additional_info: Dict   |
+---------------------------+

+---------------------------+
|         <<Value>>         |
|      RiskIndicator        |
+---------------------------+
| - indicator: String       |
| - evidence: List[String]  |
| - severity: Enum          |
+---------------------------+
```

## 2.2 Enumeraciones

```
+---------------------------+    +---------------------------+
|        <<Enum>>           |    |        <<Enum>>           |
|         Role              |    |        Severity           |
+---------------------------+    +---------------------------+
| ADMIN = "admin"           |    | CRITICAL = "critical"     |
| ANALYST = "analyst"       |    | HIGH = "high"             |
+---------------------------+    | MEDIUM = "medium"         |
                                 | LOW = "low"               |
+---------------------------+    +---------------------------+
|        <<Enum>>           |
|      AlertStatus          |    +---------------------------+
+---------------------------+    |        <<Enum>>           |
| UNREAD = "unread"         |    |       ModelType           |
| READ = "read"             |    +---------------------------+
| ACKNOWLEDGED = "ack..."   |    | PHISHING = "phishing"     |
+---------------------------+    | ATO = "ato"               |
                                 | BRUTE_FORCE = "brute_force"|
+---------------------------+    +---------------------------+
|        <<Enum>>           |
|     ReportStatus          |
+---------------------------+
| PENDING = "pending"       |
| PROCESSING = "processing" |
| COMPLETED = "completed"   |
| FAILED = "failed"         |
+---------------------------+
```

---

# 3. DIAGRAMA DE BASE DE DATOS (ER)

## 3.1 Modelo Entidad-Relacion

```
+===========================================================================+
|                    DIAGRAMA ENTIDAD-RELACION (ER)                         |
+===========================================================================+

                              +----------------+
                              |     users      |
                              +----------------+
                              | PK id          |
                              |    username    |
                              |    email       |
                              |    password_hash|
                              |    role        |
                              |    full_name   |
                              |    is_active   |
                              |    created_at  |
                              +-------+--------+
                                      |
           +--------------------------+---------------------------+
           |                          |                           |
           | 1                        | 1                         | 1
           |                          |                           |
           v *                        v *                         v *
+------------------+        +------------------+        +------------------+
| uploaded_files   |        |     reports      |        |     alerts       |
+------------------+        +------------------+        +------------------+
| PK id            |        | PK id            |        | PK id            |
|    filename      |        |    title         |        |    title         |
|    original_name |        |    model_type    |        |    description   |
|    file_path     |        | FK file_id  -----+------->|    severity      |
| FK uploaded_by --+------->| FK created_by ---+------->|    status        |
|    uploaded_at   |        |    created_at    |        |    model_type    |
|    row_count     |        |    total_records |        | FK report_id ----+--+
|    columns_json  |        |    threats_det.  |        |    pred_index    |  |
|    detected_model|        |    benign_count  |        |    confidence    |  |
+------------------+        |    avg_confidence|        |    pred_label    |  |
         ^                  |    results_json  |        |    risk_level    |  |
         |                  |    status        |        |    raw_data_json |  |
         | 1                +--------+---------+        |    created_at    |  |
         |                           |                  |    read_at       |  |
         +---------------------------+                  |    acknowledged_at|  |
                                     |                  | FK acknowledged_by|  |
                                     | 1                +------------------+  |
                                     |                           ^            |
                                     +---------------------------+------------+
                                                   *
```

## 3.2 Modelo Fisico de Base de Datos

```sql
-- =====================================================
-- MODELO FISICO - SQLite (auth_gateway.db)
-- =====================================================

-- Tabla: users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'analyst')),
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_users_username (username),
    INDEX idx_users_email (email)
);

-- Tabla: uploaded_files
CREATE TABLE uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_by INTEGER NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    row_count INTEGER,
    columns_json TEXT,
    detected_model VARCHAR(50) CHECK (detected_model IN ('phishing', 'ato', 'brute_force')),

    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_files_uploaded_by (uploaded_by),
    INDEX idx_files_uploaded_at (uploaded_at)
);

-- Tabla: reports
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('phishing', 'ato', 'brute_force')),
    file_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_records INTEGER DEFAULT 0,
    threats_detected INTEGER DEFAULT 0,
    benign_count INTEGER DEFAULT 0,
    avg_confidence FLOAT DEFAULT 0.0,
    results_json TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),

    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_reports_model_type (model_type),
    INDEX idx_reports_status (status),
    INDEX idx_reports_created_at (created_at)
);

-- Tabla: alerts
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    status VARCHAR(20) DEFAULT 'unread' CHECK (status IN ('unread', 'read', 'acknowledged')),
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('phishing', 'ato', 'brute_force')),
    report_id INTEGER,
    prediction_index INTEGER,
    confidence FLOAT,
    prediction_label VARCHAR(100),
    risk_level VARCHAR(50),
    raw_data_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME,
    acknowledged_at DATETIME,
    acknowledged_by INTEGER,

    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE SET NULL,
    FOREIGN KEY (acknowledged_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_alerts_severity (severity),
    INDEX idx_alerts_status (status),
    INDEX idx_alerts_model_type (model_type),
    INDEX idx_alerts_created_at (created_at)
);
```

## 3.3 Diccionario de Datos

| Tabla | Campo | Tipo | Nulo | Descripcion |
|-------|-------|------|------|-------------|
| **users** | id | INTEGER | NO | Identificador unico |
| | username | VARCHAR(50) | NO | Nombre de usuario unico |
| | email | VARCHAR(100) | NO | Email unico |
| | password_hash | VARCHAR(255) | NO | Hash bcrypt del password |
| | role | VARCHAR(20) | NO | Rol: admin o analyst |
| | full_name | VARCHAR(100) | SI | Nombre completo |
| | is_active | BOOLEAN | NO | Estado de la cuenta |
| | created_at | DATETIME | NO | Fecha de creacion |
| **uploaded_files** | id | INTEGER | NO | Identificador unico |
| | filename | VARCHAR(255) | NO | Nombre del archivo en servidor |
| | original_filename | VARCHAR(255) | NO | Nombre original del archivo |
| | file_path | VARCHAR(500) | NO | Ruta completa del archivo |
| | uploaded_by | INTEGER | NO | FK a users.id |
| | uploaded_at | DATETIME | NO | Fecha de subida |
| | row_count | INTEGER | SI | Cantidad de registros |
| | columns_json | TEXT | SI | JSON con columnas detectadas |
| | detected_model | VARCHAR(50) | SI | Modelo detectado automaticamente |
| **reports** | id | INTEGER | NO | Identificador unico |
| | title | VARCHAR(255) | NO | Titulo del reporte |
| | model_type | VARCHAR(50) | NO | Tipo de modelo usado |
| | file_id | INTEGER | NO | FK a uploaded_files.id |
| | created_by | INTEGER | NO | FK a users.id |
| | total_records | INTEGER | NO | Total de registros procesados |
| | threats_detected | INTEGER | NO | Amenazas detectadas |
| | benign_count | INTEGER | NO | Registros benignos |
| | avg_confidence | FLOAT | NO | Confianza promedio |
| | results_json | TEXT | SI | JSON con resultados completos |
| | status | VARCHAR(20) | NO | Estado del reporte |
| **alerts** | id | INTEGER | NO | Identificador unico |
| | title | VARCHAR(255) | NO | Titulo de la alerta |
| | description | TEXT | SI | Descripcion detallada |
| | severity | VARCHAR(20) | NO | Severidad: critical/high/medium |
| | status | VARCHAR(20) | NO | Estado: unread/read/acknowledged |
| | model_type | VARCHAR(50) | NO | Modelo que genero la alerta |
| | confidence | FLOAT | SI | Confianza de la prediccion |
| | raw_data_json | TEXT | SI | Datos originales en JSON |

---

# 4. DIAGRAMA DE CASOS DE USO DE ALTO NIVEL

```
+===========================================================================+
|              DIAGRAMA DE CASOS DE USO - ALTO NIVEL                        |
+===========================================================================+

                    +------------------------------------------+
                    |    Sistema Predictivo de Ciberseguridad   |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |
| Admin  |          |  |                                  |    |
| (Jefe  |----------+->|  UC01: Gestionar Usuarios        |    |
|  SOC)  |          |  |                                  |    |
+--------+          |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC02: Subir Archivos de Datos   |    |
    |               |  |                                  |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC03: Generar Reportes de       |    |
    |               |  |        Prediccion                |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |          +----------+
    +-------------->|  |  UC04: Visualizar Panel Principal      |<-------------| Analista |
    |               |  |                                  |    |          |   SOC    |
    |               |  +----------------------------------+    |          +----------+
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC05: Gestionar Alertas         |<-------------------+
    |               |  |        Tempranas                 |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC06: Realizar Prediccion       |<-------------------+
                    |  |        Manual                    |    |
                    |  +----------------------------------+    |
                    |                                          |
                    |  +----------------------------------+    |
                    |  |  UC07: Exportar Reportes         |<-------------------+
                    |  |                                  |    |
                    |  +----------------------------------+    |
                    |                                          |
                    +------------------------------------------+

+===========================================================================+
|                         ACTORES DEL SISTEMA                               |
+===========================================================================+

+----------------+----------------------------------------------------------+
| Actor          | Descripcion                                              |
+----------------+----------------------------------------------------------+
| Admin          | Jefe del SOC. Acceso completo: gestiona usuarios,        |
| (Jefe SOC)     | sube archivos, genera reportes, visualiza todo.          |
+----------------+----------------------------------------------------------+
| Analista SOC   | Analista de seguridad. Acceso limitado: visualiza        |
|                | dashboard, reportes, alertas y realiza predicciones.     |
+----------------+----------------------------------------------------------+
```

---

# 5. DIAGRAMAS DE CASOS DE USO EXPANDIDOS

## 5.1 Modulo de Autenticacion y Usuarios

```
+===========================================================================+
|           CASOS DE USO - MODULO AUTENTICACION Y USUARIOS                  |
+===========================================================================+

                    +------------------------------------------+
                    |     Modulo de Autenticacion y Usuarios    |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |
| Admin  |--------->|  |  UC1.1: Iniciar Sesion           |<-----------+
+--------+          |  +----------------------------------+    |       |
    |               |         |                                |       |
    |               |         | <<include>>                    |       |
    |               |         v                                |       |
    |               |  +----------------------------------+    |       |
    |               |  |  UC1.2: Validar Credenciales     |    |       |
    |               |  +----------------------------------+    |       |
    |               |                                          |       |
    |               |  +----------------------------------+    |       |
    +-------------->|  |  UC1.3: Crear Usuario            |    |   +--------+
    |               |  +----------------------------------+    |   | Analista|
    |               |                                          |   +--------+
    |               |  +----------------------------------+    |
    +-------------->|  |  UC1.4: Modificar Usuario        |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC1.5: Eliminar Usuario         |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC1.6: Listar Usuarios          |    |
                    |  +----------------------------------+    |
                    |                                          |
                    |  +----------------------------------+    |
                    |  |  UC1.7: Cerrar Sesion            |<-----------+
                    |  +----------------------------------+    |
                    +------------------------------------------+
```

### Especificacion UC1.1: Iniciar Sesion

| Campo | Descripcion |
|-------|-------------|
| **ID** | UC1.1 |
| **Nombre** | Iniciar Sesion |
| **Actor** | Admin, Analista |
| **Precondicion** | Usuario registrado en el sistema |
| **Postcondicion** | Usuario autenticado con token JWT activo |
| **Flujo Principal** | 1. Usuario ingresa usuario y contraseña<br>2. Sistema valida credenciales<br>3. Sistema genera token JWT<br>4. Sistema redirige a Panel Principal |
| **Flujo Alternativo** | 2a. Credenciales invalidas: mostrar error |

## 5.2 Modulo de Gestion de Archivos

```
+===========================================================================+
|              CASOS DE USO - MODULO GESTION DE ARCHIVOS                    |
+===========================================================================+

                    +------------------------------------------+
                    |       Modulo de Gestion de Archivos       |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |
| Admin  |--------->|  |  UC2.1: Subir Archivo CSV/Excel  |    |
+--------+          |  +----------------------------------+    |
    |               |         |                                |
    |               |         | <<include>>                    |
    |               |         v                                |
    |               |  +----------------------------------+    |
    |               |  |  UC2.2: Validar Formato Archivo  |    |
    |               |  +----------------------------------+    |
    |               |         |                                |
    |               |         | <<include>>                    |
    |               |         v                                |
    |               |  +----------------------------------+    |
    |               |  |  UC2.3: Detectar Tipo de Modelo  |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC2.4: Listar Archivos Subidos  |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC2.5: Ver Detalle de Archivo   |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC2.6: Eliminar Archivo         |    |
                    |  +----------------------------------+    |
                    |                                          |
                    +------------------------------------------+
```

## 5.3 Modulo de Prediccion de Amenazas

```
+===========================================================================+
|             CASOS DE USO - MODULO PREDICCION DE AMENAZAS                  |
+===========================================================================+

                    +------------------------------------------+
                    |      Modulo de Prediccion de Amenazas     |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |
| Admin  |--------->|  |  UC3.1: Seleccionar Modelo ML    |<-----------+
+--------+          |  +----------------------------------+    |       |
    |               |         |                                |       |
    |               |         v                                |       |
    |               |  +----------------------------------+    |       |
    +-------------->|  |  UC3.2: Predecir Phishing        |<-----------+
    |               |  |        (Email Individual)        |    |       |
    |               |  +----------------------------------+    |       |
    |               |                                          |       |
    |               |  +----------------------------------+    |       |
    +-------------->|  |  UC3.3: Predecir Toma de Cuenta  |<-----------+
    |               |  |        (Login Individual)        |    |       |
    |               |  +----------------------------------+    |       |
    |               |                                          |       |
    |               |  +----------------------------------+    |   +--------+
    +-------------->|  |  UC3.4: Predecir Fuerza Bruta    |<---| Analista|
    |               |  |        (Flujo de Red Individual) |    |   +--------+
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC3.5: Ver Explicacion de       |<-----------+
                    |  |        Prediccion                |    |
                    |  +----------------------------------+    |
                    |         |                                |
                    |         | <<extend>>                     |
                    |         v                                |
                    |  +----------------------------------+    |
                    |  |  UC3.6: Mostrar Indicadores de   |    |
                    |  |        Riesgo                    |    |
                    |  +----------------------------------+    |
                    +------------------------------------------+
```

## 5.4 Modulo de Alertas Tempranas

```
+===========================================================================+
|              CASOS DE USO - MODULO ALERTAS TEMPRANAS                      |
+===========================================================================+

                    +------------------------------------------+
                    |        Modulo de Alertas Tempranas        |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |          +--------+
| Admin  |--------->|  |  UC4.1: Listar Alertas           |<-------------| Analista|
+--------+          |  +----------------------------------+    |          +--------+
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC4.2: Filtrar Alertas por      |<-------------------+
    |               |  |   Severidad/Estado/Modelo        |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC4.3: Ver Detalle de Alerta    |<-------------------+
    |               |  +----------------------------------+    |               |
    |               |         |                                |               |
    |               |         | <<include>>                    |               |
    |               |         v                                |               |
    |               |  +----------------------------------+    |               |
    |               |  |  UC4.4: Marcar Alerta como Leida |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC4.5: Reconocer Alerta         |<-------------------+
    |               |  |        (Acknowledge)             |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC4.6: Reconocer Multiples      |<-------------------+
    |               |  |        Alertas (Bulk)            |    |
    |               |  +----------------------------------+    |
    |               |                                          |
    |               |  +----------------------------------+    |
    +-------------->|  |  UC4.7: Ver Estadisticas de      |<-------------------+
                    |  |        Alertas                   |    |
                    |  +----------------------------------+    |
                    +------------------------------------------+

+------------------------------------------+
|         <<Sistema Automatico>>           |
+------------------------------------------+
                    |
                    v
+----------------------------------+
|  UC4.8: Generar Alertas desde    |
|         Predicciones (Lote)     |
+----------------------------------+
         |
         | <<include>>
         v
+----------------------------------+
|  UC4.9: Evaluar Umbrales de      |
|         Severidad                |
+----------------------------------+
```

## 5.5 Modulo de Panel Principal y Reportes

```
+===========================================================================+
|            CASOS DE USO - MODULO DASHBOARD Y REPORTES                     |
+===========================================================================+

                    +------------------------------------------+
                    |    Modulo de Panel Principal y Reportes   |
                    +------------------------------------------+
                    |                                          |
+--------+          |  +----------------------------------+    |          +--------+
| Admin  |--------->|  |  UC5.1: Visualizar Panel Principal     |<-------------| Analista|
+--------+          |  |        Principal                 |    |          +--------+
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC5.2: Ver Estadisticas por     |<-------------------+
    |               |  |        Modelo                    |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC5.3: Generar Reporte de       |    |               |
    |               |  |        Predicciones (Lote)      |    |               |
    |               |  +----------------------------------+    |               |
    |               |         |                                |               |
    |               |         | <<include>>                    |               |
    |               |         v                                |               |
    |               |  +----------------------------------+    |               |
    |               |  |  UC5.4: Procesar Archivo con     |    |               |
    |               |  |        Modelo ML                 |    |               |
    |               |  +----------------------------------+    |               |
    |               |         |                                |               |
    |               |         | <<include>>                    |               |
    |               |         v                                |               |
    |               |  +----------------------------------+    |               |
    |               |  |  UC5.5: Generar Alertas          |    |               |
    |               |  |        Automaticas               |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC5.6: Listar Reportes          |<-------------------+
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC5.7: Ver Detalle de Reporte   |<-------------------+
    |               |  |        con Graficos              |    |               |
    |               |  +----------------------------------+    |               |
    |               |                                          |               |
    |               |  +----------------------------------+    |               |
    +-------------->|  |  UC5.8: Exportar Reporte a CSV   |<-------------------+
                    |  +----------------------------------+    |
                    +------------------------------------------+
```

---

# 6. DIAGRAMAS DE SECUENCIA

## 6.1 Secuencia de Carga y Procesamiento de Datos

```
+===========================================================================+
|        DIAGRAMA DE SECUENCIA: Carga y Procesamiento de Datos              |
+===========================================================================+

  Admin          Frontend         Auth Gateway    Serv. Archivos   Detector Columnas
    |                |                  |                  |                  |
    | 1. Selecciona  |                  |                  |                  |
    |    archivo CSV |                  |                  |                  |
    |--------------->|                  |                  |                  |
    |                |                  |                  |                  |
    |                | 2. POST /files/upload              |                  |
    |                |    (multipart/form-data)           |                  |
    |                |----------------->|                  |                  |
    |                |                  |                  |                  |
    |                |                  | 3. validate_file()|                 |
    |                |                  |----------------->|                  |
    |                |                  |                  |                  |
    |                |                  |                  | 4. Valida extension
    |                |                  |                  |    (.csv, .xlsx) |
    |                |                  |                  |                  |
    |                |                  | 5. file_valid    |                  |
    |                |                  |<-----------------|                  |
    |                |                  |                  |                  |
    |                |                  | 6. save_file()   |                  |
    |                |                  |----------------->|                  |
    |                |                  |                  |                  |
    |                |                  |                  | 7. Guarda en /uploads
    |                |                  |                  |    genera UUID   |
    |                |                  |                  |                  |
    |                |                  | 8. file_path     |                  |
    |                |                  |<-----------------|                  |
    |                |                  |                  |                  |
    |                |                  | 9. detect_model(columns)           |
    |                |                  |----------------------------------->|
    |                |                  |                  |                  |
    |                |                  |                  |     10. Analiza columnas
    |                |                  |                  |         segun patrones
    |                |                  |                  |                  |
    |                |                  | 11. model_type (phishing/ato/brute_force)
    |                |                  |<-----------------------------------|
    |                |                  |                  |                  |
    |                |                  | 12. INSERT uploaded_files          |
    |                |                  |     (filename, path, model_type)   |
    |                |                  |------------------+                  |
    |                |                  |                  |                  |
    |                | 13. Response {id, filename, detected_model}           |
    |                |<-----------------|                  |                  |
    |                |                  |                  |                  |
    | 14. Muestra    |                  |                  |                  |
    |    confirmacion|                  |                  |                  |
    |<---------------|                  |                  |                  |
    |                |                  |                  |                  |
```

## 6.2 Secuencia de Generacion de Predicciones (Lote)

```
+===========================================================================+
|        DIAGRAMA DE SECUENCIA: Generacion de Predicciones en Lote          |
+===========================================================================+

  Admin      Frontend    Auth Gateway   Serv. Reportes   ML API     Serv. Alertas
    |            |             |              |             |              |
    | 1. Clic    |             |              |             |              |
    |  "Generar" |             |              |             |              |
    |----------->|             |              |             |              |
    |            |             |              |             |              |
    |            | 2. POST /reports/generate  |             |              |
    |            |    {file_id, model_type}   |             |              |
    |            |------------>|              |             |              |
    |            |             |              |             |              |
    |            |             | 3. generate_report()       |              |
    |            |             |------------->|             |              |
    |            |             |              |             |              |
    |            |             |              | 4. Lee archivo CSV         |
    |            |             |              |    del disco               |
    |            |             |              |             |              |
    |            |             |              | 5. Formatea datos          |
    |            |             |              |    segun modelo            |
    |            |             |              |             |              |
    |            |             |              | 6. POST /predict/batch     |
    |            |             |              |------------>|              |
    |            |             |              |             |              |
    |            |             |              |             | 7. Para cada registro:
    |            |             |              |             |    - Feature engineering
    |            |             |              |             |    - Prediccion
    |            |             |              |             |    - Explicacion
    |            |             |              |             |              |
    |            |             |              | 8. [{prediction, confidence,|
    |            |             |              |     explanation}, ...]     |
    |            |             |              |<------------|              |
    |            |             |              |             |              |
    |            |             |              | 9. Calcula estadisticas    |
    |            |             |              |    (threats, benign, avg)  |
    |            |             |              |             |              |
    |            |             |              | 10. generate_alerts()      |
    |            |             |              |-------------------------->|
    |            |             |              |             |              |
    |            |             |              |             |    11. Para cada amenaza:
    |            |             |              |             |        IF confidence >= threshold
    |            |             |              |             |           CREATE alert
    |            |             |              |             |              |
    |            |             |              | 12. alerts_count           |
    |            |             |              |<--------------------------|
    |            |             |              |             |              |
    |            |             |              | 13. INSERT reports         |
    |            |             |              |     (stats, results_json)  |
    |            |             |              |             |              |
    |            |             | 14. {report_id, stats, alerts_generated}  |
    |            |             |<-------------|             |              |
    |            |             |              |             |              |
    |            | 15. Response con estadisticas            |              |
    |            |<------------|              |             |              |
    |            |             |              |             |              |
    | 16. Muestra|             |              |             |              |
    |   reporte  |             |              |             |              |
    |<-----------|             |              |             |              |
    |            |             |              |             |              |
```

## 6.3 Secuencia de Visualizacion de Panel Principal

```
+===========================================================================+
|       DIAGRAMA DE SECUENCIA: Visualizacion de Panel Principal             |
+===========================================================================+

  Analista     Frontend        Auth Gateway        Database
     |             |                 |                 |
     | 1. Accede   |                 |                 |
     |  /dashboard |                 |                 |
     |------------>|                 |                 |
     |             |                 |                 |
     |             | 2. Verifica token JWT            |
     |             |    (localStorage)                |
     |             |                 |                 |
     |             | 3. GET /auth/me (validar sesion) |
     |             |---------------->|                 |
     |             |                 |                 |
     |             |                 | 4. Valida JWT   |
     |             |                 |                 |
     |             | 5. {user, role} |                 |
     |             |<----------------|                 |
     |             |                 |                 |
     |             | 6. GET /reports (ultimos reportes)|
     |             |---------------->|                 |
     |             |                 |                 |
     |             |                 | 7. SELECT * FROM reports
     |             |                 |    ORDER BY created_at DESC
     |             |                 |---------------->|
     |             |                 |                 |
     |             |                 | 8. [reports]    |
     |             |                 |<----------------|
     |             |                 |                 |
     |             | 9. [reports]    |                 |
     |             |<----------------|                 |
     |             |                 |                 |
     |             | 10. GET /alerts/stats            |
     |             |---------------->|                 |
     |             |                 |                 |
     |             |                 | 11. SELECT COUNT(*)
     |             |                 |     GROUP BY severity, status
     |             |                 |---------------->|
     |             |                 |                 |
     |             |                 | 12. {stats}     |
     |             |                 |<----------------|
     |             |                 |                 |
     |             | 13. {total, critical, high, medium, unread}
     |             |<----------------|                 |
     |             |                 |                 |
     |             | 14. GET /alerts/unread/count     |
     |             |---------------->|                 |
     |             |                 |                 |
     |             |                 | 15. SELECT COUNT(*)
     |             |                 |     WHERE status='unread'
     |             |                 |---------------->|
     |             |                 |                 |
     |             | 16. {count}     |                 |
     |             |<----------------|                 |
     |             |                 |                 |
     | 17. Renderiza Panel con estadisticas           |
     |<------------|                 |                 |
     |             |                 |                 |
     |             | [Sondeo cada 30 segundos]       |
     |             | 18. GET /alerts/unread/count     |
     |             |---------------->|                 |
     |             |                 |                 |
```

## 6.4 Secuencia de Exportacion de Reportes

```
+===========================================================================+
|           DIAGRAMA DE SECUENCIA: Exportacion de Reportes                  |
+===========================================================================+

  Usuario      Frontend        Auth Gateway        Database
     |             |                 |                 |
     | 1. Clic     |                 |                 |
     |  "Exportar" |                 |                 |
     |------------>|                 |                 |
     |             |                 |                 |
     |             | 2. GET /reports/{id}             |
     |             |---------------->|                 |
     |             |                 |                 |
     |             |                 | 3. SELECT * FROM reports
     |             |                 |    WHERE id = {id}
     |             |                 |---------------->|
     |             |                 |                 |
     |             |                 | 4. {report with results_json}
     |             |                 |<----------------|
     |             |                 |                 |
     |             | 5. {report data}|                 |
     |             |<----------------|                 |
     |             |                 |                 |
     |             | 6. Procesa results_json          |
     |             |    - Procesa JSON                |
     |             |    - Formatea columnas           |
     |             |                 |                 |
     |             | 7. Genera CSV en memoria         |
     |             |    - Encabezados                 |
     |             |    - Filas de datos              |
     |             |    - Predicciones                |
     |             |                 |                 |
     |             | 8. Crea Blob con CSV             |
     |             |                 |                 |
     |             | 9. Inicia descarga               |
     |             |    (atributo download)           |
     |             |                 |                 |
     | 10. Descarga archivo CSV      |                 |
     |<------------|                 |                 |
     |             |                 |                 |

Nota: La exportacion se realiza en el Frontend para evitar
      carga adicional en el servidor.
```

## 6.5 Secuencia de Prediccion Individual

```
+===========================================================================+
|          DIAGRAMA DE SECUENCIA: Prediccion Individual                     |
+===========================================================================+

  Usuario      Frontend        ML API (Phishing/ATO/BruteForce)
     |             |                 |
     | 1. Completa |                 |
     |   formulario|                 |
     |------------>|                 |
     |             |                 |
     |             | 2. Valida campos en cliente      |
     |             |    (required, format)            |
     |             |                 |
     |             | 3. POST /predict                 |
     |             |    {email_data/login_data/flow_data}
     |             |---------------->|
     |             |                 |
     |             |                 | 4. Valida entrada (Pydantic)
     |             |                 |
     |             |                 | 5. Ingenieria de Caracteristicas:
     |             |                 |    - Phishing: TF-IDF + numericas
     |             |                 |    - ATO: temporales + cambios
     |             |                 |    - BF: normalizacion 0-1
     |             |                 |
     |             |                 | 6. model.predict_proba()
     |             |                 |
     |             |                 | 7. Genera explicacion:
     |             |                 |    - Detecta indicadores
     |             |                 |    - Asigna severidad
     |             |                 |    - Crea resumen
     |             |                 |
     |             | 8. {prediction, confidence, explanation}
     |             |<----------------|
     |             |                 |
     |             | 9. Renderiza resultado:          |
     |             |    - Tarjeta con prediccion      |
     |             |    - Barra de confianza          |
     |             |    - Boton explicacion           |
     |             |                 |
     | 10. Muestra resultado         |
     |<------------|                 |
     |             |                 |
     | 11. Clic    |                 |
     |  "Explicar" |                 |
     |------------>|                 |
     |             |                 |
     |             | 12. Abre ventana con:            |
     |             |     - indicadores_riesgo         |
     |             |     - evidencia                  |
     |             |     - resumen                    |
     |             |                 |
     | 13. Ventana explicacion       |
     |<------------|                 |
     |             |                 |
```

---

# 7. DIAGRAMA DE FLUJO DEL PROCESO ACTUAL

```
+===========================================================================+
|      DIAGRAMA DE FLUJO: Proceso Actual (Sin Sistema Predictivo)           |
+===========================================================================+

                              +-------------------+
                              |      INICIO       |
                              +-------------------+
                                       |
                                       v
                     +----------------------------------+
                     |   Logs de seguridad generados   |
                     |   (SIEM, Firewalls, IDS/IPS)    |
                     +----------------------------------+
                                       |
                                       v
                     +----------------------------------+
                     |  Analista SOC revisa logs       |
                     |  MANUALMENTE (8 horas/dia)      |
                     +----------------------------------+
                                       |
                                       v
                          +-----------------------+
                          |  Hay patron sospechoso |
                          |     en los logs?       |
                          +-----------------------+
                             /              \
                           SI                NO
                           /                  \
                          v                    v
       +------------------------+    +------------------------+
       | Analista investiga     |    |  Continua revision     |
       | MANUALMENTE el evento  |    |  manual de logs        |
       | (30-60 min promedio)   |    +------------------------+
       +------------------------+              |
                  |                            |
                  v                            |
         +------------------+                  |
         | Es amenaza real? |                  |
         +------------------+                  |
            /          \                       |
          SI            NO                     |
          /              \                     |
         v                v                    |
+------------------+ +------------------+      |
| Escala a equipo  | | Falso positivo   |      |
| de respuesta     | | Tiempo perdido   |------+
| (Nivel 2)         | +------------------+
+------------------+
         |
         v
+----------------------------------+
|  Equipo Nivel 2 analiza y        |
|  determina severidad            |
|  (2-4 horas adicionales)        |
+----------------------------------+
         |
         v
+----------------------------------+
|  Documentacion manual del       |
|  incidente en planilla Excel    |
+----------------------------------+
         |
         v
+----------------------------------+
|  Tiempo total promedio:         |
|  4-8 horas por incidente        |
+----------------------------------+
         |
         v
                              +-------------------+
                              |        FIN        |
                              +-------------------+

+===========================================================================+
|                        PROBLEMAS IDENTIFICADOS                            |
+===========================================================================+
| 1. Proceso manual intensivo (8+ horas de revision diaria)                 |
| 2. Alta tasa de falsos positivos (>60% en revision manual)                |
| 3. Tiempo de respuesta lento (4-8 horas por incidente)                    |
| 4. No hay priorizacion automatica por severidad                           |
| 5. Documentacion inconsistente en planillas                               |
| 6. Fatiga del analista por volumen de alertas                             |
+===========================================================================+
```

---

# 8. DIAGRAMA DE FLUJO DEL PROCESO PROPUESTO

```
+===========================================================================+
|      DIAGRAMA DE FLUJO: Proceso Propuesto (Con Sistema Predictivo)        |
+===========================================================================+

                              +-------------------+
                              |      INICIO       |
                              +-------------------+
                                       |
                                       v
                     +----------------------------------+
                     |   Datos de seguridad ingresados |
                     |   (CSV/Excel desde SIEM/logs)   |
                     +----------------------------------+
                                       |
                                       v
                     +----------------------------------+
                     |  Admin sube archivo al sistema  |
                     |  (Interfaz web - 1 minuto)      |
                     +----------------------------------+
                                       |
                                       v
                     +----------------------------------+
                     |  Sistema detecta automaticamente|
                     |  el tipo de modelo a usar       |
                     +----------------------------------+
                                       |
                                       v
                     +----------------------------------+
                     |  Admin genera reporte con       |
                     |  predicciones en lote           |
                     +----------------------------------+
                                       |
                                       v
           +--------------------------------------------------+
           |           MODELOS DE MACHINE LEARNING            |
           |                                                  |
           |  +-------------+ +-------------+ +-------------+ |
           |  | Phishing    | |    ATO      | | Brute Force | |
           |  | F1: 99.09%  | | F1: 75.86%  | | F1: 99.97%  | |
           |  +-------------+ +-------------+ +-------------+ |
           +--------------------------------------------------+
                                       |
                                       v
                     +----------------------------------+
                     |  Para cada registro:            |
                     |  - Prediccion (amenaza/benigno) |
                     |  - Confianza (0-100%)           |
                     |  - Explicacion detallada        |
                     +----------------------------------+
                                       |
                                       v
                          +-----------------------+
                          |  Confianza >= Umbral? |
                          +-----------------------+
                             /              \
                           SI                NO
                           /                  \
                          v                    v
       +------------------------+    +------------------------+
       |  GENERA ALERTA         |    |  Registro clasificado  |
       |  AUTOMATICA            |    |  como BENIGNO          |
       |                        |    |  (sin accion requerida)|
       |  Severidad basada en:  |    +------------------------+
       |  - Critical (>=95%)    |              |
       |  - High (>=85%)        |              |
       |  - Medium (>=75%)      |              |
       +------------------------+              |
                  |                            |
                  v                            |
       +------------------------+              |
       |  Panel actualiza       |              |
       |  contador de alertas   |              |
       |  (polling 30 seg)      |              |
       +------------------------+              |
                  |                            |
                  v                            |
       +------------------------+              |
       |  Analista revisa       |              |
       |  alertas PRIORIZADAS   |              |
       |  por severidad         |              |
       +------------------------+              |
                  |                            |
                  v                            |
       +------------------------+              |
       |  Clic en alerta para   |              |
       |  ver EXPLICACION       |              |
       |  detallada con:        |              |
       |  - Indicadores riesgo  |              |
       |  - Evidencia especifica|              |
       |  - Datos originales    |              |
       +------------------------+              |
                  |                            |
                  v                            |
         +------------------+                  |
         | Requiere accion? |                  |
         +------------------+                  |
            /          \                       |
          SI            NO                     |
          /              \                     |
         v                v                    |
+------------------+ +------------------+      |
| Escala a Nivel 2  | | Reconoce alerta  |      |
| con evidencia    | | (acknowledge)    |------+
| ya documentada   | +------------------+
+------------------+
         |
         v
+----------------------------------+
|  Tiempo total promedio:         |
|  15-30 minutos por incidente    |
+----------------------------------+
         |
         v
+----------------------------------+
|  Reportes y estadisticas        |
|  generados automaticamente      |
+----------------------------------+
         |
         v
                              +-------------------+
                              |        FIN        |
                              +-------------------+

+===========================================================================+
|                        MEJORAS IMPLEMENTADAS                              |
+===========================================================================+
| 1. Procesamiento automatico (segundos vs horas)                           |
| 2. Reduccion de falsos positivos (precision >98% en phishing/BF)          |
| 3. Tiempo de respuesta: 15-30 min vs 4-8 horas                           |
| 4. Priorizacion automatica por severidad (critical/high/medium)           |
| 5. Documentacion automatica con explicabilidad                            |
| 6. Menor fatiga del analista (solo alertas relevantes)                    |
+===========================================================================+
```

## 8.1 Comparativa de Procesos

| Aspecto | Proceso Actual | Proceso Propuesto | Mejora |
|---------|----------------|-------------------|--------|
| **Tiempo de analisis** | 4-8 horas | 15-30 minutos | 90% reduccion |
| **Revision manual** | 8 horas/dia | 2 horas/dia | 75% reduccion |
| **Falsos positivos** | >60% | <5% (phishing, BF) | 90% reduccion |
| **Priorizacion** | Manual | Automatica | 100% automatizado |
| **Documentacion** | Excel manual | Sistema automatico | 100% automatizado |
| **Explicabilidad** | No existe | Indicadores + evidencia | Nueva capacidad |

---

# 9. DIAGRAMA DE NAVEGACION DE PANTALLAS

```
+===========================================================================+
|              DIAGRAMA DE NAVEGACION / FLUJO DE PANTALLAS                  |
+===========================================================================+

                           +--------------------+
                           |   PAGINA LOGIN     |
                           |   /login           |
                           +--------------------+
                                     |
                                     | Autenticacion exitosa
                                     v
+===========================================================================+
|                           AREA AUTENTICADA                                |
+===========================================================================+
|                                                                           |
|  +--------------------+                                                   |
|  |     SIDEBAR        |                                                   |
|  +--------------------+                                                   |
|  | [Panel]       -----|--------+                                          |
|  | [Prediccion]  -----|--------|---+                                      |
|  | [Archivos]*   -----|--------|---|---+                                  |
|  | [Reportes]    -----|--------|---|---|---+                              |
|  | [Alertas]     -----|--------|---|---|---|---+                          |
|  | [Usuarios]*   -----|--------|---|---|---|---|---+                      |
|  +--------------------+        |   |   |   |   |   |                      |
|                                v   |   |   |   |   |                      |
|                     +--------------+   |   |   |   |                      |
|                     |  DASHBOARD   |   |   |   |   |                      |
|                     |  /dashboard  |   |   |   |   |                      |
|                     +--------------+   |   |   |   |                      |
|                     | - Resumen    |   |   |   |   |                      |
|                     | - Estadist.  |   |   |   |   |                      |
|                     | - Graficos   |   |   |   |   |                      |
|                     +--------------+   |   |   |   |                      |
|                                        |   |   |   |                      |
|                     +------------------+   |   |   |                      |
|                     |  PREDICCION      |   |   |   |                      |
|                     |/dashboard/predict|   |   |   |                      |
|                     +------------------+   |   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | | Phishing   |   |   |   |   |                      |
|                     | | Formulario |---|-->|   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | | ATO        |   |   |   |   |                      |
|                     | | Formulario |---|-->|   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | |Fuerza Bruta|   |   |   |   |                      |
|                     | | Formulario |---|-->|   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     |                  |   |   |   |                      |
|                     | +------------+   |   |   |   |                      |
|                     | | Resultado  |<--+   |   |   |                      |
|                     | | + Explicar |       |   |   |                      |
|                     | +------------+       |   |   |                      |
|                     +------------------+   |   |   |                      |
|                                            |   |   |                      |
|                     +----------------------+   |   |                      |
|                     |  ARCHIVOS (Admin)    |   |   |                      |
|                     |  /files              |   |   |                      |
|                     +----------------------+   |   |                      |
|                     | - Subir (arrastrar)  |   |   |                      |
|                     | - Lista de archivos  |   |   |                      |
|                     | - Eliminar           |   |   |                      |
|                     +----------------------+   |   |                      |
|                                                |   |                      |
|                     +--------------------------+   |                      |
|                     |  REPORTES                |   |                      |
|                     |  /reports                |   |                      |
|                     +--------------------------+   |                      |
|                     | - Lista de reportes      |   |                      |
|                     | - Generar nuevo (Admin)  |   |                      |
|                     |          |               |   |                      |
|                     |          v               |   |                      |
|                     | +--------------------+   |   |                      |
|                     | | Detalle Reporte    |   |   |                      |
|                     | | - Estadisticas     |   |   |                      |
|                     | | - Graficos         |   |   |                      |
|                     | | - Tabla resultados |   |   |                      |
|                     | | - Exportar CSV     |   |   |                      |
|                     | +--------------------+   |   |                      |
|                     +--------------------------+   |                      |
|                                                    |                      |
|                     +------------------------------+                      |
|                     |  ALERTAS                     |                      |
|                     |  /alerts                     |                      |
|                     +------------------------------+                      |
|                     | - Tarjetas Estadisticas      |                      |
|                     | - Filtros (severidad/estado) |                      |
|                     | - Lista de alertas           |                      |
|                     | - Seleccion multiple         |                      |
|                     |          |                   |                      |
|                     |          v                   |                      |
|                     | +------------------------+   |                      |
|                     | | Ventana Detalle Alerta |   |                      |
|                     | | - Explicacion visual   |   |                      |
|                     | | - Indicadores riesgo   |   |                      |
|                     | | - Datos originales     |   |                      |
|                     | | - Reconocer            |   |                      |
|                     | +------------------------+   |                      |
|                     +------------------------------+                      |
|                                                                           |
|                     +------------------------------+                      |
|                     |  USUARIOS (Admin)            |                      |
|                     |  /users                      |                      |
|                     +------------------------------+                      |
|                     | - Lista usuarios             |                      |
|                     | - Crear usuario              |                      |
|                     | - Editar usuario             |                      |
|                     | - Eliminar usuario           |                      |
|                     +------------------------------+                      |
|                                                                           |
+===========================================================================+

* = Solo visible para rol Admin
```

## 9.1 Mapa de Navegacion Simplificado

```
LOGIN (/login)
    |
    +---> DASHBOARD (/dashboard)
    |         |
    |         +---> PREDICCION (/dashboard/predict)
    |                   |
    |                   +---> Formulario Phishing
    |                   +---> Formulario ATO
    |                   +---> Formulario Fuerza Bruta
    |                   +---> Resultado + Explicacion (Ventana)
    |
    +---> ARCHIVOS (/files) [Admin]
    |         |
    |         +---> Subir
    |         +---> Lista
    |         +---> Eliminar
    |
    +---> REPORTES (/reports)
    |         |
    |         +---> Lista Reportes
    |         +---> Generar Reporte [Admin]
    |         +---> Detalle Reporte
    |               +---> Exportar CSV
    |
    +---> ALERTAS (/alerts)
    |         |
    |         +---> Tarjetas Estadisticas
    |         +---> Filtros
    |         +---> Lista Alertas
    |         +---> Detalle Alerta (Ventana)
    |               +---> Reconocer
    |
    +---> USUARIOS (/users) [Admin]
              |
              +---> Gestion Usuarios
```

---

# 10. DIAGRAMA DE FLUJO CRISP-DM APLICADO

```
+===========================================================================+
|          DIAGRAMA DE FLUJO CRISP-DM - APLICACION EN EL PROYECTO           |
+===========================================================================+

                    +-----------------------------------+
                    |     1. COMPRENSION DEL NEGOCIO    |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Reunion con stakeholders BCP    |
                    | - Identificacion de vectores de   |
                    |   ataque prioritarios:            |
                    |   * Phishing (emails)             |
                    |   * Toma de Cuenta (logins)       |
                    |   * Fuerza Bruta (red)            |
                    | - Definicion de metricas objetivo:|
                    |   * F1-Score > 75%                |
                    |   * Tiempo respuesta < 1 min      |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                    +-----------------------------------+
                    |    2. COMPRENSION DE LOS DATOS    |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Seleccion de datasets publicos: |
                    |   * CEAS_08 (39K emails)          |
                    |   * RBA Dataset (85K logins)      |
                    |   * CSE-CIC-IDS2018 (763K flows)  |
                    | - Analisis exploratorio (EDA)     |
                    | - Identificacion de patrones:     |
                    |   * 98.6% ATOs con cambio pais    |
                    |   * 75% phishing con URLs         |
                    |   * Trafico "plano" en BF         |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                    +-----------------------------------+
                    |   3. PREPARACION DE LOS DATOS     |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Limpieza de datos nulos/dupl.   |
                    | - Ingenieria de Caracteristicas:  |
                    |   * Phishing: TF-IDF + 16 num.    |
                    |   * ATO: 35 variables derivadas   |
                    |   * BF: 60 variables normalizadas |
                    | - Balanceo de clases:             |
                    |   * SMOTE para ATO (0.17% -> 9%)  |
                    |   * Submuestreo para BF (50/50)   |
                    | - Division entren./prueba (80/20) |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                    +-----------------------------------+
                    |           4. MODELADO             |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Evaluacion de 4 algoritmos:     |
                    |   * Logistic Regression           |
                    |   * SVM                           |
                    |   * Random Forest                 |
                    |   * Gradient Boosting             |
                    | - Optimizacion hiperparametros    |
                    | - Validacion cruzada (5-fold)     |
                    | - Seleccion final:                |
                    |   * Phishing: Gradient Boosting   |
                    |   * ATO: Gradient Boosting+SMOTE  |
                    |   * BF: Random Forest             |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                    +-----------------------------------+
                    |          5. EVALUACION            |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Evaluacion en test set:         |
                    |   * Phishing: F1=99.09%           |
                    |   * ATO: F1=75.86%                |
                    |   * BF: F1=99.97%                 |
                    | - Matrices de confusion           |
                    | - Curvas ROC-AUC                  |
                    | - Analisis de errores             |
                    | - Validacion con stakeholders     |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                    +-----------------------------------+
                    |        6. IMPLEMENTACION          |
                    +-----------------------------------+
                    |                                   |
                    | Actividades realizadas:           |
                    | - Serializacion modelos (.pkl)    |
                    | - Desarrollo APIs REST (FastAPI)  |
                    | - Sistema de alertas automatico   |
                    | - Panel React para SOC            |
                    | - Documentacion tecnica           |
                    | - Pruebas de integracion          |
                    | - Despliegue en ambiente local    |
                    |                                   |
                    +-----------------------------------+
                                    |
                                    v
                         +-----------------+
                         |      FIN        |
                         +-----------------+

+===========================================================================+
|                    ITERACIONES REALIZADAS                                 |
+===========================================================================+
| Iteracion 1: Modelo Phishing (2 semanas)                                  |
|   - Comprension -> Datos -> Preparacion -> Modelado -> Evaluacion         |
|                                                                           |
| Iteracion 2: Modelo ATO (3 semanas - requirio SMOTE por desbalance)       |
|   - Retorno a Preparacion para aplicar SMOTE                              |
|   - Re-evaluacion con nuevos umbrales                                     |
|                                                                           |
| Iteracion 3: Modelo Fuerza Bruta (2 semanas)                              |
|   - Flujo directo sin iteraciones adicionales                             |
|                                                                           |
| Iteracion 4: Integracion y Alertas (2 semanas)                            |
|   - Implementacion -> Ajuste de umbrales -> Re-evaluacion                 |
+===========================================================================+
```

---

# 11. DIAGRAMA DE PIPELINE DE MACHINE LEARNING

## 11.1 Pipeline General

```
+===========================================================================+
|                    PIPELINE DE MACHINE LEARNING                           |
+===========================================================================+

+----------+    +----------+    +----------+    +----------+    +----------+
|  DATOS   |    | LIMPIEZA |    |INGENIERIA|    | ENTRENA- |    | VALIDA-  |
|  CRUDOS  |--->|    Y     |--->|   DE     |--->|  MIENTO  |--->|   CION   |
|          |    | PREPRO-  |    | CARACT.  |    |          |    |          |
|          |    | CESADO   |    |          |    |          |    |          |
+----------+    +----------+    +----------+    +----------+    +----------+
     |               |               |               |               |
     v               v               v               v               v
+----------+    +----------+    +----------+    +----------+    +----------+
| - CSV    |    | - Nulos  |    | - TF-IDF |    | - Entren/|    | - Conj.  |
| - Emails |    | - Duplic.|    | - Nuevas |    |   Prueba |    |   Prueba |
| - Logins |    | - Tipos  |    |   vars   |    | - Valid. |    | - Metricas|
| - Flujos |    | - Atipicos|   | - Encod. |    |  Cruzada |    | - Matrices|
+----------+    +----------+    +----------+    +----------+    +----------+
                                                                      |
                                                                      v
+----------+    +----------+    +----------+    +----------+    +----------+
| INTEGRA- |    |  PREDIC- |    |  MODELO  |    | SELEC-   |    | EVALUA-  |
|   CION   |<---|   CION   |<---|  (.pkl)  |<---|   CION   |<---|   CION   |
|  SISTEMA |    |          |    |          |    |  MODELO  |    |  COMPAR. |
|          |    |          |    |          |    |          |    |          |
+----------+    +----------+    +----------+    +----------+    +----------+
     |               |               |               |               |
     v               v               v               v               v
+----------+    +----------+    +----------+    +----------+    +----------+
| - APIs   |    | - Tiempo |    | - Gradient|   | - Mejor  |    | - F1     |
| - Alertas|    |   Real   |    |   Boost  |    |   F1     |    | - Prec.  |
| - Panel  |    | - Lote   |    | - Random |    | - Compro-|    | - Recall |
| - Reportes|   | - Explic.|    |   Forest |    |   misos  |    | - AUC    |
+----------+    +----------+    +----------+    +----------+    +----------+
```

## 11.2 Pipeline Detallado por Modelo

### Pipeline Modelo Phishing

```
+===========================================================================+
|                    PIPELINE MODELO PHISHING                               |
+===========================================================================+

ENTRADA                PROCESAMIENTO                           SALIDA
+--------+    +--------------------------------------------------+    +--------+
| Email  |    |                                                  |    |0/1     |
|- remite|   |  +----------+    +----------+    +----------+   |    |Prediccion
|- asunto|-->|  | LIMPIEZA |    | TF-IDF   |    | GRADIENT |   |--->|        |
|- cuerpo|   |  |          |--->|VECTORIZER|--->| BOOSTING |   |    |Confianza
| - urls  |   |  |- Minusc. |    |          |    |          |   |    |        |
+--------+    |  |- Caract. |    | 1000     |    |100 arboles|  |    |Explicacion
              |  |  espec.  |    | caract.  |    | prof.=5  |   |    +--------+
              |  +----------+    +----------+    +----------+   |
              |       |               |               |          |
              |       v               v               v          |
              |  +---------+    +---------+    +---------+      |
              |  | Texto   |    | Vector  |    | 1016    |      |
              |  | limpio  |    | disperso|    | caract. |      |
              |  +---------+    +---------+    +---------+      |
              |                                                  |
              |  +------------------------------------------+   |
              |  | CARACTERISTICAS ADICIONALES (16):        |   |
              |  | - long_asunto, long_cuerpo               |   |
              |  | - cant_urls, tiene_urls                  |   |
              |  | - palabras_phishing, dominio_remitente   |   |
              |  | - ratio_mayusculas, cant_exclamaciones   |   |
              |  +------------------------------------------+   |
              +--------------------------------------------------+
```

### Pipeline Modelo Toma de Cuenta (ATO)

```
+===========================================================================+
|                  PIPELINE MODELO TOMA DE CUENTA (ATO)                     |
+===========================================================================+

ENTRADA                PROCESAMIENTO                           SALIDA
+--------+    +--------------------------------------------------+    +--------+
| Login  |    |                                                  |    |0/1     |
|- id_usu.|   |  +----------+    +----------+    +----------+   |    |Prediccion
| - ip    |-->|  |CODIFICAC.|    |INGENIERIA|    | GRADIENT |   |--->|        |
| - pais  |   |  |ETIQUETAS |--->|DE CARACT.|--->| BOOSTING |   |    |Confianza
|- navegad|   |  |          |    |          |    | + SMOTE  |   |    |        |
|- disposit|  |  | Categ -> |    | 35 vars  |    |          |   |    |Explicacion
| - so    |   |  | Numerico |    | derivadas|    |100 arboles|  |    +--------+
+--------+    |  +----------+    +----------+    +----------+   |
              |       |               |               |          |
              |       v               v               v          |
              |  +---------+    +---------+    +---------+      |
              |  |Navegador|    | Temporales|   | SMOTE    |     |
              |  | Pais    |    | Cambios  |    | muestreo |     |
              |  |Dispositivo|  | Agregados|    | 0.1      |     |
              |  +---------+    +---------+    +---------+      |
              |                                                  |
              |  +------------------------------------------+   |
              |  | CARACTERISTICAS DERIVADAS (35):          |   |
              |  | - Temporales: hora, dia, es_finsemana... |   |
              |  | - Cambios: cambio_ip, cambio_pais...     |   |
              |  | - Agregados: logins_por_usuario, etc.    |   |
              |  | - Riesgo: viaje_imposible, ip_ataque     |   |
              |  +------------------------------------------+   |
              +--------------------------------------------------+
```

### Pipeline Modelo Fuerza Bruta

```
+===========================================================================+
|                   PIPELINE MODELO FUERZA BRUTA                            |
+===========================================================================+

ENTRADA                PROCESAMIENTO                           SALIDA
+--------+    +--------------------------------------------------+    +--------+
| Flujo  |    |                                                  |    |0/1     |
| de Red |    |  +----------+    +----------+    +----------+   |    |Prediccion
|- pto_dst|-->|  | ESCALADO |    | SELECCION|    | RANDOM   |   |--->|        |
|- protocol|  |  | MIN-MAX  |--->| CARACT.  |--->| FOREST   |   |    |Confianza
|- duracion|  |  |          |    |          |    |          |   |    |        |
| - pqts  |   |  | [0, 1]   |    | 60 vars  |    |100 arboles|  |    |Explicacion
| - bytes |   |  | rango    |    | relevantes|   | prof.=20 |   |    +--------+
+--------+    |  +----------+    +----------+    +----------+   |
              |       |               |               |          |
              |       v               v               v          |
              |  +---------+    +---------+    +---------+      |
              |  | Valores |    | Sin vars|    | Paralelo|      |
              |  | normali-|    | constantes|   | n_jobs=-1|     |
              |  | zados   |    |          |    |          |     |
              |  +---------+    +---------+    +---------+      |
              |                                                  |
              |  +------------------------------------------+   |
              |  | CARACTERISTICAS PRINCIPALES (60):        |   |
              |  | - Paquetes: tot_fwd/bwd_pkts, len_*      |   |
              |  | - Flujo: duracion, bytes/s, pqts/s       |   |
              |  | - Banderas: SYN, FIN, RST, PSH, ACK      |   |
              |  | - IAT: flujo/fwd/bwd_iat_media/std/max   |   |
              |  +------------------------------------------+   |
              +--------------------------------------------------+
```

## 11.3 Pipeline de Explicabilidad

```
+===========================================================================+
|                    PIPELINE DE EXPLICABILIDAD                             |
+===========================================================================+

                     +---------------------------+
                     |      PREDICCION           |
                     | (prediccion, probabilidad)|
                     +---------------------------+
                                  |
                                  v
                     +---------------------------+
                     | ANALISIS DE CARACTERIST.  |
                     +---------------------------+
                     | - Extrae valores clave    |
                     | - Compara con umbrales    |
                     | - Identifica anomalias    |
                     +---------------------------+
                                  |
            +---------------------+---------------------+
            |                     |                     |
            v                     v                     v
    +---------------+     +---------------+     +---------------+
    |   PHISHING    |     |      ATO      |     | FUERZA BRUTA  |
    +---------------+     +---------------+     +---------------+
    | - URLs detectadas|   | - cambio_pais |    | - flujo_pqts_s|
    | - Palabras urg. |   | - cambio_ip   |    | - bwd_pqts_s  |
    | - Dominio remit.|   | - es_noche    |    | - duracion_flujo|
    | - Cant. palabras|   | - ip_ataque   |    | - bandera_psh |
    +---------------+     +---------------+     +---------------+
            |                     |                     |
            +---------------------+---------------------+
                                  |
                                  v
                     +---------------------------+
                     |   GENERA INDICADORES      |
                     +---------------------------+
                     | Para cada anomalia:       |
                     | - indicador: descripcion  |
                     | - evidencia: valor real   |
                     | - severidad: critico/alto/|
                     |              medio/bajo   |
                     +---------------------------+
                                  |
                                  v
                     +---------------------------+
                     |     GENERA RESUMEN        |
                     +---------------------------+
                     | "Este [email/login/flujo] |
                     |  muestra N indicadores    |
                     |  de [amenaza] con X%      |
                     |  de confianza."           |
                     +---------------------------+
                                  |
                                  v
                     +---------------------------+
                     |      EXPLICACION          |
                     +---------------------------+
                     | {                         |
                     |   indicadores_riesgo:[...],|
                     |   resumen: "...",         |
                     |   total_indicadores: N,   |
                     |   info_adicional: {...}   |
                     | }                         |
                     +---------------------------+
```

---

# RESUMEN DE DIAGRAMAS

| # | Diagrama | Tipo UML | Proposito |
|---|----------|----------|-----------|
| 1 | Componentes | Estructura | Arquitectura del sistema |
| 2 | Clases | Estructura | Modelo de dominio y entidades |
| 3 | Base de Datos (ER) | Estructura | Modelo relacional |
| 4 | Casos de Uso Alto Nivel | Comportamiento | Vision general de funcionalidades |
| 5 | Casos de Uso Expandidos | Comportamiento | Detalle por modulo |
| 6 | Secuencia | Comportamiento | Interacciones entre componentes |
| 7 | Flujo Proceso Actual | Flujo | Situacion sin sistema |
| 8 | Flujo Proceso Propuesto | Flujo | Situacion con sistema |
| 9 | Navegacion | Interfaz | Flujo de pantallas |
| 10 | CRISP-DM | Metodologia | Proceso de ML aplicado |
| 11 | Pipeline ML | Tecnico | Flujo de datos en modelos |

---

**FIN DEL DOCUMENTO DE DIAGRAMAS**

---

*Documento generado como parte del proyecto de investigacion academica del Sistema Predictivo de Incidentes de Ciberseguridad para el Banco de Credito de Bolivia.*

*Ultima actualizacion: 2026-01-30*
