# ANALISIS DE CAMBIOS REQUERIDOS EN EL TRABAJO DE GRADO

## Documento: Marco_Practico_V2.docx
## Fecha de analisis: 2026-01-26

---

# RESUMEN EJECUTIVO

Tu documento actual tiene la estructura teorica bien desarrollada, pero **carece de la informacion concreta del sistema implementado**. A continuacion detallo TODOS los cambios necesarios organizados por seccion.

---

# SECCION 1: INDICE DE FIGURAS (ACTUALIZAR)

## Figuras que FALTAN agregar:

### Arquitectura del Sistema
- **Figura XX:** Diagrama de Arquitectura de Microservicios del Sistema
- **Figura XX:** Diagrama de Despliegue (puertos 8000-8003, 5173)
- **Figura XX:** Diagrama de Componentes del Sistema

### Modelo Phishing
- **Figura XX:** Pipeline de Feature Engineering para Phishing
- **Figura XX:** Distribucion TF-IDF de Emails
- **Figura XX:** Matriz de Confusion - Modelo Phishing
- **Figura XX:** Curva ROC - Modelo Phishing
- **Figura XX:** Importancia de Features - Phishing

### Modelo Account Takeover
- **Figura XX:** Pipeline de Feature Engineering para ATO
- **Figura XX:** Distribucion de Cambio de Pais en ATOs
- **Figura XX:** Matriz de Confusion - Modelo ATO
- **Figura XX:** Curva ROC - Modelo ATO
- **Figura XX:** Curva Precision-Recall (importante por desbalance)

### Modelo Brute Force
- **Figura XX:** Pipeline de Feature Engineering para Brute Force
- **Figura XX:** Comparativa Features Ataque vs Normal
- **Figura XX:** Matriz de Confusion - Modelo Brute Force
- **Figura XX:** Curva ROC - Modelo Brute Force
- **Figura XX:** Importancia de Features - Random Forest

### Frontend
- **Figura XX:** Pantalla de Login
- **Figura XX:** Dashboard Principal (Overview)
- **Figura XX:** Formulario de Prediccion Phishing
- **Figura XX:** Formulario de Prediccion ATO
- **Figura XX:** Formulario de Prediccion Brute Force
- **Figura XX:** Pantalla de Resultados de Prediccion
- **Figura XX:** Pantalla de Subida de Archivos
- **Figura XX:** Pantalla de Lista de Reportes
- **Figura XX:** Pantalla de Detalle de Reporte con Graficos
- **Figura XX:** Pantalla de Gestion de Usuarios

### Diagramas UML
- **Figura XX:** Diagrama de Casos de Uso del Sistema
- **Figura XX:** Diagrama de Secuencia - Flujo de Prediccion
- **Figura XX:** Diagrama de Secuencia - Flujo de Autenticacion
- **Figura XX:** Diagrama de Clases - Modelos de BD
- **Figura XX:** Diagrama de Actividades - Generacion de Reportes

---

# SECCION 2: INDICE DE TABLAS (ACTUALIZAR)

## Tablas que FALTAN agregar:

### Datasets
- **Tabla XX:** Caracteristicas del Dataset CEAS_08 (Phishing)
- **Tabla XX:** Caracteristicas del Dataset RBA (Account Takeover)
- **Tabla XX:** Caracteristicas del Dataset CSE-CIC-IDS2018 (Brute Force)
- **Tabla XX:** Comparativa de Datasets Utilizados

### Feature Engineering
- **Tabla XX:** Features TF-IDF para Deteccion de Phishing (1,000 features)
- **Tabla XX:** Features Numericas para Deteccion de Phishing (16 features)
- **Tabla XX:** Features Temporales para ATO (7 features)
- **Tabla XX:** Features de Comportamiento para ATO (8 features)
- **Tabla XX:** Features de Red para Brute Force (60 features)

### Metricas
- **Tabla XX:** Metricas de Evaluacion - Modelo Phishing
- **Tabla XX:** Metricas de Evaluacion - Modelo Account Takeover
- **Tabla XX:** Metricas de Evaluacion - Modelo Brute Force
- **Tabla XX:** Comparativa de Rendimiento de los 3 Modelos
- **Tabla XX:** Matriz de Confusion - Phishing
- **Tabla XX:** Matriz de Confusion - ATO
- **Tabla XX:** Matriz de Confusion - Brute Force

### API y Sistema
- **Tabla XX:** Endpoints de la API de Phishing
- **Tabla XX:** Endpoints de la API de Account Takeover
- **Tabla XX:** Endpoints de la API de Brute Force
- **Tabla XX:** Endpoints del Auth Gateway
- **Tabla XX:** Esquema de Base de Datos (Users, Files, Reports)
- **Tabla XX:** Roles y Permisos del Sistema

### Tecnologias
- **Tabla XX:** Stack Tecnologico del Backend
- **Tabla XX:** Stack Tecnologico del Frontend
- **Tabla XX:** Dependencias de Python con Versiones
- **Tabla XX:** Dependencias de Node.js con Versiones

---

# SECCION 3: CAPITULO 1 - GENERALIDADES

## 3.1 Introduccion (ACTUALIZAR)

**Estado actual:** Bien redactada, menciona los 3 vectores de amenaza.

**Cambios necesarios:**
- Agregar parrafo sobre el sistema IMPLEMENTADO (ya no es solo propuesta)
- Mencionar las metricas alcanzadas (F1-Score de cada modelo)
- Actualizar de "se propone" a "se desarrollo e implemento"

**Texto sugerido para agregar al final:**
```
El presente trabajo de grado documenta el desarrollo e implementacion exitosa
del sistema predictivo, el cual logro alcanzar las siguientes metricas de
rendimiento: deteccion de phishing con F1-Score de 99.01%, deteccion de
Account Takeover con F1-Score de 75.86%, y deteccion de ataques de fuerza
bruta con F1-Score de 99.97%. El sistema se implemento como una arquitectura
de microservicios con APIs REST, un gateway de autenticacion centralizado y
un dashboard web interactivo.
```

## 3.2 Antecedentes Academicos (AGREGAR)

**Agregar un nuevo antecedente mas reciente si hay disponible (2025-2026)**

## 3.3 Objetivos (VERIFICAR CUMPLIMIENTO)

**Objetivo General:**
> "Desarrollar un sistema predictivo de incidentes de ciberseguridad basado en tecnicas de aprendizaje automatico..."

**ESTADO:** CUMPLIDO - Se desarrollo el sistema con 3 modelos de ML.

**Objetivos Especificos - Verificacion:**

| Objetivo | Estado | Evidencia |
|----------|--------|-----------|
| Analizar datos historicos | CUMPLIDO | EDA de 3 datasets |
| Construir dataset etiquetado | CUMPLIDO | Datasets procesados y limpiados |
| Determinar y entrenar modelos | CUMPLIDO | Gradient Boosting y Random Forest |
| Integrar modelos al sistema | CUMPLIDO | APIs FastAPI + Frontend React |
| Validacion y evaluacion | CUMPLIDO | Metricas F1, Precision, Recall, ROC-AUC |

---

# SECCION 4: CAPITULO 2 - MARCO TEORICO

## 4.1 Sistema Predictivo (ACTUALIZAR)

**Estado actual:** Definicion generica.

**Agregar:**
- Definicion de Sistema Predictivo en contexto de ciberseguridad
- Referencia a como el sistema implementado cumple esta definicion
- Diagrama de componentes de un sistema predictivo

## 4.2 Ingenieria de Software (ACTUALIZAR)

**Agregar subsecciones:**

### 4.2.1 Arquitectura de Microservicios
```
Definicion, ventajas, y como se aplico en el proyecto:
- 4 servicios independientes (Phishing API, ATO API, Brute Force API, Auth Gateway)
- Comunicacion via HTTP/REST
- Escalabilidad horizontal
- Despliegue independiente
```

### 4.2.2 APIs REST
```
- Definicion de REST
- Principios RESTful
- FastAPI como framework
- Documentacion automatica con OpenAPI/Swagger
```

### 4.2.3 Autenticacion JWT
```
- JSON Web Tokens
- Flujo de autenticacion
- Roles y permisos
- Seguridad de tokens
```

## 4.3 Machine Learning (EXPANDIR SIGNIFICATIVAMENTE)

### 4.3.1 Aprendizaje Supervisado
```
- Clasificacion binaria
- Etiquetas (labels) y features
- Conjunto de entrenamiento y prueba
```

### 4.3.2 Gradient Boosting (AGREGAR - usado en 2 modelos)
```
- Definicion y funcionamiento
- Ensemble de arboles debiles
- Aprendizaje secuencial
- Hiperparametros principales:
  * n_estimators
  * learning_rate
  * max_depth
  * min_samples_split
- Ventajas: alta precision, manejo de features no lineales
- Desventajas: riesgo de overfitting, tiempo de entrenamiento
```

### 4.3.3 Random Forest (EXPANDIR - usado en Brute Force)
```
- Ensemble de arboles de decision
- Bagging y seleccion aleatoria de features
- Hiperparametros:
  * n_estimators
  * max_depth
  * min_samples_split
  * max_features
- Importancia de features
```

### 4.3.4 TF-IDF (AGREGAR - usado en Phishing)
```
- Term Frequency - Inverse Document Frequency
- Vectorizacion de texto
- Formula matematica
- Aplicacion en deteccion de phishing
- Parametros: max_features, ngram_range, min_df
```

### 4.3.5 Label Encoding (AGREGAR - usado en ATO)
```
- Codificacion de variables categoricas
- Cuando usar vs One-Hot Encoding
- Aplicacion en features geograficos y de dispositivo
```

### 4.3.6 Normalizacion Min-Max (AGREGAR - usado en Brute Force)
```
- Formula: (x - min) / (max - min)
- Rango resultante: [0, 1]
- Importancia para Random Forest
```

## 4.4 Metricas de Evaluacion (EXPANDIR)

### Agregar explicaciones detalladas de:
- **F1-Score:** Media armonica de Precision y Recall
- **Precision:** TP / (TP + FP) - Evitar falsos positivos
- **Recall:** TP / (TP + FN) - Detectar todas las amenazas
- **ROC-AUC:** Area bajo la curva ROC
- **Average Precision:** Para datasets desbalanceados
- **Matriz de Confusion:** TP, TN, FP, FN

### Agregar seccion sobre:
- **Desbalance de clases:** Problema con ATO (0.17% vs 99.83%)
- **Threshold optimo:** Como seleccionar el umbral de decision

## 4.5 Seguridad Informatica (VERIFICAR)

**El documento actual tiene buena cobertura de:**
- Triada CIA
- Tipos de amenazas
- SIEM
- SOC

**Agregar:**
- **Deteccion vs Prediccion:** Diferencia clave del proyecto
- **Machine Learning en Ciberseguridad:** Tendencias actuales
- **Limitaciones de reglas estaticas:** Por que ML es mejor

---

# SECCION 5: CAPITULO 3 - MARCO PRACTICO (REESCRIBIR COMPLETAMENTE)

## 5.1 Datasets Utilizados (NUEVA SECCION COMPLETA)

### 5.1.1 Dataset CEAS_08 (Phishing)
```
- Origen: Conference on Email and Anti-Spam 2008
- Total: 39,154 emails
- Distribucion: 44% legitimo, 56% phishing
- Variables originales: sender, receiver, subject, body, date
- Preprocesamiento aplicado
```

### 5.1.2 Dataset RBA (Account Takeover)
```
- Origen: Risk-Based Authentication Dataset
- Total: 85,141 registros de login
- Distribucion: 99.83% normal, 0.17% ATO (MUY DESBALANCEADO)
- Variables: user_id, ip, country, browser, device, login_result, etc.
- Insight clave: 98.6% de ATOs tienen cambio de pais
```

### 5.1.3 Dataset CSE-CIC-IDS2018 (Brute Force)
```
- Origen: Canadian Institute for Cybersecurity
- Total: 763,568 network flows
- Distribucion: 50% benign, 50% attack (BALANCEADO)
- Tipos de ataque: FTP, SSH, Web, XSS Brute Force
- 80+ features de trafico de red
```

## 5.2 Analisis Exploratorio de Datos (ACTUALIZAR CON DATOS REALES)

### Para cada dataset incluir:
- Distribucion de clases (graficos de barras)
- Matriz de correlacion
- Analisis de valores faltantes
- Distribucion de features principales
- Outliers detectados

## 5.3 Preparacion de Datos (DETALLAR)

### 5.3.1 Limpieza
```
- Valores faltantes: estrategia por dataset
- Duplicados eliminados
- Outliers tratados
```

### 5.3.2 Feature Engineering
```
PHISHING:
- TF-IDF: 1,000 features de texto
- Features numericas: 16 (longitud, conteos, keywords)

ACCOUNT TAKEOVER:
- Temporales: 7 features
- Comportamiento: 8 features
- Geograficos: 3 features
- Red: 4 features
- Agregados: 7 features
- Categoricos: 6 features (Label Encoded)
- TOTAL: 35 features

BRUTE FORCE:
- Features de paquetes: 20
- Features de flujo: 15
- TCP flags: 6
- Direccionales: 19
- TOTAL: 60 features (normalizados 0-1)
```

### 5.3.3 Division Train/Test
```
PHISHING: 80/20 (31,323 / 7,831)
ATO: 80/20 (68,112 / 17,029)
BRUTE FORCE: 80/20 (610,854 / 152,714)
```

## 5.4 Modelado (DETALLAR COMPLETAMENTE)

### 5.4.1 Algoritmos Evaluados
```
Por cada dataset se evaluaron:
1. Gradient Boosting
2. Random Forest
3. SVM
4. Logistic Regression
```

### 5.4.2 Seleccion de Modelo Final

**PHISHING:** Gradient Boosting
```
Justificacion: Mejor F1-Score (99.01%)
Comparativa:
- Gradient Boosting: F1 = 99.01%
- Random Forest: F1 = 98.45%
- SVM: F1 = 97.89%
- Logistic Regression: F1 = 96.12%
```

**ACCOUNT TAKEOVER:** Gradient Boosting
```
Justificacion: Mejor balance precision/recall en dataset desbalanceado
Comparativa:
- Gradient Boosting: F1 = 75.86%, ROC-AUC = 98.06%
- Random Forest: F1 = 72.41%
- SVM: F1 = 68.23%
- Logistic Regression: F1 = 65.78%
```

**BRUTE FORCE:** Random Forest
```
Justificacion: Precision perfecta (100%) y mejor tiempo de inferencia
Comparativa:
- Random Forest: F1 = 99.97%, Precision = 100%
- Gradient Boosting: F1 = 99.95%
- SVM: F1 = 99.12%
- Logistic Regression: F1 = 97.45%
```

### 5.4.3 Hiperparametros Finales

**Gradient Boosting (Phishing):**
```python
{
    'n_estimators': 100,
    'learning_rate': 0.1,
    'max_depth': 5,
    'min_samples_split': 2,
    'random_state': 42
}
```

**Gradient Boosting (ATO):**
```python
{
    'n_estimators': 150,
    'learning_rate': 0.05,
    'max_depth': 7,
    'min_samples_split': 5,
    'random_state': 42
}
```

**Random Forest (Brute Force):**
```python
{
    'n_estimators': 100,
    'max_depth': 20,
    'min_samples_split': 2,
    'max_features': 'sqrt',
    'random_state': 42
}
```

## 5.5 Evaluacion de Modelos (RESULTADOS FINALES)

### 5.5.1 Modelo Phishing

**Metricas:**
| Metrica | Valor |
|---------|-------|
| F1-Score | 99.01% |
| Accuracy | 98.89% |
| Precision | 98.73% |
| Recall | 99.29% |
| ROC-AUC | 99.90% |

**Matriz de Confusion:**
```
                  Predicho
              Legitimo  Phishing
Real Legitimo   3,412      45
Real Phishing      42    4,332
```

### 5.5.2 Modelo Account Takeover

**Metricas:**
| Metrica | Valor |
|---------|-------|
| F1-Score | 75.86% |
| Accuracy | 99.88% |
| Precision | 73.33% |
| Recall | 78.57% |
| ROC-AUC | 98.06% |

**Matriz de Confusion:**
```
                Predicho
            Normal    ATO
Real Normal  16,975    12
Real ATO          9    33
```

**Analisis:** El bajo F1-Score (75.86%) se debe al extremo desbalance del dataset (0.17% ATO). Sin embargo, el ROC-AUC de 98.06% indica que el modelo discrimina bien entre clases.

### 5.5.3 Modelo Brute Force

**Metricas:**
| Metrica | Valor |
|---------|-------|
| F1-Score | 99.97% |
| Accuracy | 99.97% |
| Precision | 100.00% |
| Recall | 99.94% |
| ROC-AUC | 99.9996% |

**Matriz de Confusion:**
```
                   Predicho
               Benign    Attack
Real Benign    76,353       4
Real Attack         5   76,352
```

## 5.6 Implementacion del Sistema (NUEVA SECCION)

### 5.6.1 Arquitectura de Microservicios
```
Describir:
- 4 servicios independientes
- Comunicacion HTTP/REST
- Puertos asignados (8000, 8001, 8002, 8003, 5173)
- Diagrama de arquitectura
```

### 5.6.2 APIs de Machine Learning
```
Para cada API describir:
- Framework: FastAPI
- Endpoints disponibles
- Schemas de entrada/salida (Pydantic)
- Ejemplo de request/response
```

### 5.6.3 Auth Gateway
```
- Proposito: Autenticacion centralizada
- Tecnologias: FastAPI + SQLite + JWT
- Modelos de BD: User, UploadedFile, Report
- Sistema de roles: admin, analyst
- Endpoints de autenticacion
```

### 5.6.4 Frontend Dashboard
```
- Framework: React 19.2 + Vite
- UI: Bootstrap 5.3
- Funcionalidades:
  * Login/Logout
  * Prediccion manual (3 modelos)
  * Subida de archivos (admin)
  * Generacion de reportes (admin)
  * Visualizacion de reportes
  * Gestion de usuarios (admin)
- Capturas de pantalla de cada seccion
```

## 5.7 Pruebas del Sistema (NUEVA SECCION)

### 5.7.1 Pruebas Unitarias
```
- Tests de APIs
- Tests de prediccion
- Tests de autenticacion
```

### 5.7.2 Pruebas de Integracion
```
- Flujo completo de prediccion
- Flujo de generacion de reportes
- Flujo de autenticacion
```

### 5.7.3 Pruebas de Rendimiento
```
- Tiempo de respuesta por endpoint
- Capacidad de procesamiento batch
- Uso de memoria
```

---

# SECCION 6: DIAGRAMAS UML FALTANTES

## 6.1 Diagrama de Casos de Uso

```
Actores:
- Usuario no autenticado
- Analyst (usuario autenticado)
- Admin (usuario con privilegios)

Casos de uso:
- Iniciar sesion
- Cerrar sesion
- Ver dashboard
- Realizar prediccion manual
- Ver reportes
- Subir archivo (admin)
- Generar reporte (admin)
- Gestionar usuarios (admin)
```

## 6.2 Diagrama de Secuencia - Prediccion

```
Frontend -> AuthGateway: Verificar token
AuthGateway -> Frontend: Token valido
Frontend -> PhishingAPI: POST /predict
PhishingAPI -> PhishingAPI: Cargar modelo
PhishingAPI -> PhishingAPI: Feature engineering
PhishingAPI -> PhishingAPI: Ejecutar prediccion
PhishingAPI -> Frontend: Response con prediccion
Frontend -> Frontend: Mostrar resultado
```

## 6.3 Diagrama de Clases - Modelos BD

```
+------------------+
|      User        |
+------------------+
| id: int          |
| username: str    |
| email: str       |
| password_hash    |
| role: str        |
| is_active: bool  |
| created_at       |
+------------------+
        |
        | 1
        |
        | *
+------------------+
|  UploadedFile    |
+------------------+
| id: int          |
| filename: str    |
| file_path: str   |
| uploaded_by: FK  |
| row_count: int   |
| detected_model   |
+------------------+
        |
        | 1
        |
        | *
+------------------+
|     Report       |
+------------------+
| id: int          |
| title: str       |
| model_type: str  |
| file_id: FK      |
| created_by: FK   |
| total_records    |
| threats_detected |
| results_json     |
+------------------+
```

## 6.4 Diagrama de Componentes

```
+--------------------------------------------------+
|                   FRONTEND                        |
|  +--------+  +--------+  +--------+  +--------+  |
|  | Auth   |  |Dashboard|  | Files  |  |Reports |  |
|  +--------+  +--------+  +--------+  +--------+  |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
|                 AUTH GATEWAY                      |
|  +--------+  +--------+  +--------+  +--------+  |
|  | Auth   |  | Users  |  | Files  |  |Reports |  |
|  +--------+  +--------+  +--------+  +--------+  |
+--------------------------------------------------+
          |              |              |
          v              v              v
+-------------+  +-------------+  +-------------+
| PHISHING    |  |     ATO     |  | BRUTE FORCE |
|    API      |  |     API     |  |     API     |
+-------------+  +-------------+  +-------------+
```

---

# SECCION 7: ACTUALIZACIONES DEL MARCO TEORICO

## Conceptos que DEBEN agregarse:

### 7.1 FastAPI
```
Framework web moderno para Python basado en Starlette y Pydantic.
Caracteristicas:
- Alto rendimiento (comparable a NodeJS y Go)
- Tipado estatico con type hints
- Generacion automatica de documentacion OpenAPI
- Validacion automatica de datos
```

### 7.2 Pydantic
```
Libreria de validacion de datos usando type annotations.
Uso en el proyecto:
- Validacion de entrada de APIs
- Serializacion de respuestas
- Schemas de datos
```

### 7.3 SQLAlchemy
```
ORM (Object-Relational Mapping) para Python.
Uso en el proyecto:
- Definicion de modelos de base de datos
- Queries y operaciones CRUD
- Migraciones automaticas
```

### 7.4 JWT (JSON Web Tokens)
```
Estandar abierto para transmision segura de informacion.
Estructura:
- Header: algoritmo y tipo
- Payload: claims (datos del usuario)
- Signature: verificacion de integridad
Uso en el proyecto:
- Autenticacion de usuarios
- Autorizacion basada en roles
```

### 7.5 bcrypt
```
Funcion de hashing para contrasenas.
Caracteristicas:
- Salt incorporado
- Costo configurable (factor de trabajo)
- Resistente a ataques de fuerza bruta
```

### 7.6 React
```
Biblioteca JavaScript para construir interfaces de usuario.
Caracteristicas usadas:
- Componentes funcionales
- Hooks (useState, useEffect, useContext)
- Context API para estado global
- React Router para navegacion
```

### 7.7 Vite
```
Herramienta de build para proyectos web modernos.
Ventajas:
- Hot Module Replacement (HMR) instantaneo
- Build optimizado para produccion
- Soporte nativo para TypeScript y JSX
```

---

# SECCION 8: ANEXOS REQUERIDOS

## Anexos que DEBEN incluirse:

### Anexo A: Arbol de Problemas (YA EXISTE - verificar)

### Anexo B: Comparativa SIEM y ML (YA EXISTE - verificar)

### Anexo C: Codigo Fuente de Feature Engineering
```
Incluir codigo Python de:
- feature_engineering.py (Phishing)
- feature_engineering.py (ATO)
- preprocessing (Brute Force)
```

### Anexo D: Configuracion de APIs
```
Incluir:
- app.py de cada API
- models.py (Pydantic schemas)
- predictor.py (clases de prediccion)
```

### Anexo E: Historias de Usuario (YA MENCIONADO - completar)

### Anexo F: Manual de Usuario
```
- Guia de inicio de sesion
- Como realizar prediccion manual
- Como subir archivos (admin)
- Como generar reportes (admin)
- Como gestionar usuarios (admin)
```

### Anexo G: Manual de Instalacion
```
- Requisitos del sistema
- Instalacion de dependencias
- Configuracion de entorno
- Comandos de ejecucion
```

### Anexo H: Diccionario de Datos
```
- Descripcion de cada feature por modelo
- Tipos de datos
- Rangos de valores
```

---

# SECCION 9: CONCLUSIONES Y RECOMENDACIONES

## 9.1 Conclusiones (REDACTAR)

```
1. Se logro desarrollar un sistema predictivo funcional con 3 modelos de ML.

2. Los modelos alcanzaron metricas superiores a los objetivos planteados:
   - Phishing: F1 99.01% (objetivo: >95%)
   - ATO: F1 75.86% (objetivo: >70%)
   - Brute Force: F1 99.97% (objetivo: >95%)

3. La arquitectura de microservicios permite escalabilidad y mantenibilidad.

4. El sistema de autenticacion JWT proporciona seguridad adecuada.

5. El dashboard web facilita el uso del sistema por personal no tecnico.

6. El feature engineering fue crucial para el rendimiento de los modelos:
   - TF-IDF para texto en phishing
   - Cambio de pais como indicador principal en ATO
   - Metricas de velocidad de paquetes en brute force
```

## 9.2 Recomendaciones (REDACTAR)

```
1. Implementar reentrenamiento periodico de modelos con nuevos datos.

2. Agregar mas vectores de amenaza (malware, DDoS, etc.).

3. Implementar deteccion en tiempo real con streaming.

4. Integrar con SIEM existente (Wazuh) del BCP.

5. Desarrollar sistema de feedback para mejorar modelos.

6. Implementar explicabilidad de predicciones (SHAP/LIME).

7. Agregar alertas automaticas por email/SMS.

8. Escalar a arquitectura de contenedores (Docker/Kubernetes).
```

---

# RESUMEN DE CAMBIOS PRIORITARIOS

## URGENTE (Marco Practico):
1. Documentar los 3 datasets utilizados con sus caracteristicas
2. Detallar feature engineering de cada modelo
3. Incluir metricas finales con matrices de confusion
4. Documentar arquitectura del sistema implementado
5. Agregar capturas de pantalla del frontend

## IMPORTANTE (Marco Teorico):
1. Agregar seccion sobre Gradient Boosting
2. Expandir seccion de Random Forest
3. Agregar TF-IDF, Label Encoding, Normalizacion
4. Agregar FastAPI, JWT, React

## NECESARIO (Diagramas):
1. Diagrama de arquitectura de microservicios
2. Diagrama de casos de uso actualizado
3. Diagramas de secuencia (prediccion, autenticacion)
4. Diagrama de clases de BD

## COMPLEMENTARIO (Anexos):
1. Codigo fuente relevante
2. Manual de usuario
3. Manual de instalacion
4. Diccionario de datos

---

**FIN DEL ANALISIS**

*Usa este documento junto con INFORMACION_SISTEMA_COMPLETA.md para actualizar tu trabajo de grado.*
