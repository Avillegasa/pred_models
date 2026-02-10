# GUÍA DE ACTUALIZACIÓN — CAPÍTULO 3: MARCO PRÁCTICO

## Alineada con Tabla 31: Plan de Desarrollo del Proyecto

**Fecha:** 2026-02-09

**Principio clave:** La estructura del capítulo 3 sigue EXACTAMENTE la Tabla 31:
- **TEMARIO** → Títulos principales (3.2, 3.3, 3.4, 3.5, 3.6, 3.7)
- **TAREA** → Subtítulos de cada sección
- **PRODUCTO ENTREGABLE** → Sub-subtítulos y contenido dentro de cada tarea

---

# TABLA 31 ACTUALIZADA — PRODUCTO ENTREGABLE

> Solo se actualiza la columna PRODUCTO ENTREGABLE. Las columnas TEMARIO, SCRUM, CRISP-DM y TAREA **NO cambian**.

---

### 3.2. ANÁLISIS DE LA SITUACIÓN ACTUAL — Preparación / Comprensión del Negocio

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.2.1. Recopilación de la Información | - Resumen informativo de los incidentes de ciberseguridad a enfocarse — - Tabla de incidentes priorizados (Tabla 32, mantener) — - Justificación de selección de datasets públicos de investigación |
| 3.2.2. Información del Proceso Actual | - Diagrama de flujo del proceso actual (Figura 17, mantener) — - Diagrama de flujo del proceso propuesto con el sistema predictivo |
| 3.2.3. Identificación de participantes | - Tabla de identificación del personal involucrado (Tabla 33, verificar) |
| 3.2.4. Identificación de Requerimientos | - Tabla de identificación de roles de usuario (2 roles: Admin, Analyst) — - Tabla de Historias de Usuario (actualizadas al sistema real) — - Tabla de Requerimientos funcionales (RF01-RF14) — - Tabla de Requerimientos no funcionales (RNF01-RNF08) |
| 3.2.5. Visión General de los Procesos | - Diagrama de Caso de uso de Alto Nivel (rehecho con sistema real) — - Tabla de procesos del sistema (9 procesos) |

### 3.3. IDENTIFICACIÓN DE REQUERIMIENTOS — Sprint Planning / Comprensión de los Datos

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.3.1. Priorización de Requerimientos | - Tabla del Product Backlog (actualizado con RF01-RF14, RNF01-RNF08) |
| 3.3.2. Formación del Equipo Scrum | - Tabla de identificación de roles del equipo Scrum (mantener) |

### 3.4. CONSTRUCCIÓN DEL DATASET — Sprint / Preparación de los Datos

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.4.1. Recopilación y exploración de datos | - Tabla resumen de los 3 datasets (CEAS_08, RBA, CSE-CIC-IDS2018) — - Definición de variables de entrada por dataset — - Análisis EDA por dataset: distribuciones, estadísticas, correlaciones, hallazgos |
| 3.4.2. Limpieza y Preparación de Datos | - Carga de datos (3 datasets reales) — - Tabla de problemas de calidad identificados — - Resultados de preparación y limpieza (tablas antes/después) |
| 3.4.3. Selección de variables relevantes | - Pipelines de ingeniería de características por modelo — - Selección de variables independientes y dependientes — - Tabla resumen de features finales por modelo |

### 3.5. DESARROLLO DEL MODELO DE PREDICCIÓN — Sprint / Modelado + Evaluación

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.5.1. Selección y evaluación de algoritmos | - Creación y ajuste del modelo Gradient Boosting — - Creación y ajuste del modelo Random Forest — - Creación y ajuste del modelo SVM — - Creación y ajuste del modelo Regresión Logística — - Tabla comparativa de algoritmos por dataset — - Tabla de hiperparámetros del modelo seleccionado |
| 3.5.2. Validación del modelo | - Matrices de confusión por modelo (heatmap) — - Curvas ROC por modelo — - Gráficos de importancia de features (top 15 por modelo) — - Cálculo de métricas (F1, Accuracy, Precision, Recall, ROC-AUC) — - Tabla comparativa general de los 3 modelos — - Selección de modelo(s) óptimo(s) con justificación |

### 3.6. DESARROLLO DEL SISTEMA — Sprint / Implementación

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.6.1. Diseño de la Base de Datos | - Diseño lógico (Diagrama E-R: 5 tablas) — - Diseño físico (SQLite) — - Diccionario de la base de datos |
| 3.6.2. Diseño de la Arquitectura | - Diagrama de arquitectura de microservicios (5 servicios + puertos) — - Tabla de servicios del sistema — - Diagrama de red Docker |
| **Sprint 1** – 3.6.3.1 Inicio | - Sprint Backlog |
| 3.6.3.2 Diseño de funcionalidad | - Casos de uso expandidos (Login, CRUD usuarios, Perfil) — - Diseño navegacional |
| 3.6.3.3 Diseño de Interfaz | - Mockups (Login, Gestión de usuarios, Perfil) |
| 3.6.3.4 Desarrollo de interfaces | - Capturas de pantalla: Login, Gestión de usuarios, Perfil |
| 3.6.3.5 Codificación | - Capturas de código: auth_service.py, users router |
| 3.6.3.6 Pruebas Unitarias | - Tabla de pruebas unitarias del módulo |
| **Sprint 2** – 3.6.4.1 Inicio | - Sprint Backlog |
| 3.6.4.2 Diseño de funcionalidad | - Casos de uso expandidos (Subir archivo, Generar reporte, Ver reportes) — - Diseño navegacional |
| 3.6.4.3 Diseño de interfaz | - Mockups (Subida de archivos, Reportes, Detalle de reporte) |
| 3.6.4.4 Desarrollo de interfaces | - Capturas: Subida archivos, Lista reportes, Detalle con gráficos |
| 3.6.4.5 Codificación | - Capturas de código: report_service.py, files router |
| 3.6.4.6 Pruebas Unitarias | - Tabla de pruebas unitarias del módulo |
| **Sprint 3** – 3.6.5.1 Inicio | - Sprint Backlog |
| 3.6.5.2 Diseño de funcionalidad | - Casos de uso expandidos (Predecir Phishing/ATO/BF, Ver explicación) — - Diagrama de secuencia de predicción — - Diseño navegacional |
| 3.6.5.3 Diseño de interfaz | - Mockups (Selector modelo, 3 formularios, Resultados + explicación) |
| 3.6.5.4 Desarrollo de interfaces | - Capturas: Selector, 3 formularios, Resultados ataque (×3), Resultados benigno (×3) |
| 3.6.5.5 Codificación | - Capturas de código: predictor.py (×3), predictions router, explainability |
| 3.6.5.6 Pruebas Unitarias | - Tabla de pruebas unitarias del módulo |
| **Sprint 4** – 3.6.6.1 Inicio | - Sprint Backlog |
| 3.6.6.2 Diseño de funcionalidad | - Casos de uso expandidos (Ver/Filtrar alertas, Estadísticas) — - Diagrama de flujo del sistema de alertas — - Diseño navegacional |
| 3.6.6.3 Diseño de interfaz | - Mockups (Alertas, Filtros, Badge en TopBar) |
| 3.6.6.4 Desarrollo de interfaces | - Capturas: Alertas con severidades, Filtros, Badge de conteo |
| 3.6.6.5 Codificación | - Capturas de código: alert_service.py, config.py (umbrales), alerts router |
| 3.6.6.6 Pruebas Unitarias | - Tabla de pruebas unitarias del módulo |
| **Sprint 5** – 3.6.7.1 Inicio | - Sprint Backlog |
| 3.6.7.2 Diseño de funcionalidad | - Casos de uso expandidos (Dashboard, Estadísticas, Reportes mensuales) — - Diseño navegacional |
| 3.6.7.3 Diseño de interfaz | - Mockups (Dashboard, Cards, Gráficos de distribución) |
| 3.6.7.4 Desarrollo de interfaces | - Capturas: Dashboard completo, Cards estadísticas, Gráficos |
| 3.6.7.5 Codificación | - Capturas de código: DashboardOverview.jsx, componentes de charts |
| 3.6.7.6 Pruebas Unitarias | - Tabla de pruebas unitarias del módulo |
| 3.6.8. Integración del modelo al sistema | - Despliegue de modelos como APIs FastAPI — - Containerización con Docker Compose — - Configuración de healthchecks y volúmenes — - Diagrama de arquitectura Docker |
| 3.6.9. Pruebas del modelo en el sistema | - Capturas del sistema integrado corriendo en Docker — - Pruebas de predicciones en tiempo real (end-to-end) — - Tabla de tiempos de respuesta por endpoint |

### 3.7. VALIDACIÓN DEL SISTEMA — Product Review + Retrospective / Evaluación

| TAREA | PRODUCTO ENTREGABLE (ACTUALIZADO) |
|-------|-----------------------------------|
| 3.7.1. Puntos fuertes y áreas de mejora | - Análisis de métricas de rendimiento — - Fortalezas del sistema — - Limitaciones identificadas — - Trabajo futuro propuesto |
| 3.7.2. Obtención de retroalimentación | - Tabla de pruebas de validación (15+ escenarios funcionales) — - Tabla de pruebas de integración — - Lista de acciones de mejora continua |

---
---

# GUÍA DETALLADA POR SECCIÓN

---

## 3.1 — PLANIFICACIÓN DEL DESARROLLO DEL SISTEMA

Esta sección contiene la Tabla 31 misma. **Qué hacer:**
- Actualizar la columna PRODUCTO ENTREGABLE según la tabla de arriba
- Si tienes Diagrama de Gantt: actualizarlo con los sprints reales y las fechas reales de ejecución
- Si no tienes Gantt: crear uno que muestre la distribución temporal de los sprints

---

## 3.2 — ANÁLISIS DE LA SITUACIÓN ACTUAL

### 3.2.1 Recopilación de la Información

**Mantener:** El contenido actual (entrevista con Ing. Gutiérrez, Tabla 32 de incidentes priorizados) está correcto.

**Agregar** un párrafo después de la Tabla 32 explicando:
- Que por confidencialidad de ASFI, los datos internos del BCP no pudieron usarse para entrenamiento
- Que se seleccionaron 3 datasets públicos de investigación que representan los mismos vectores de amenaza identificados en las entrevistas
- Nombrar los 3 datasets: **CEAS_08** (phishing), **RBA Dataset** (account takeover), **CSE-CIC-IDS2018** (brute force)
- Que esta práctica es estándar en investigación académica de ciberseguridad

**IMPORTANTE:** Esto reemplaza la narrativa de "datos sintetizados del BCP" que aparece en 3.4. Los datos NO son sintetizados, son datasets públicos.

---

### 3.2.2 Información del Proceso Actual

**Mantener:** Figura 17 (Diagrama de flujo del proceso actual) y todo el texto que la acompaña.

**Agregar DESPUÉS de la Figura 17:** Una nueva figura:

**FIGURA NUEVA — Proceso propuesto con el sistema predictivo:**
```
Evento de seguridad (email/login/flujo de red)
    ↓
API de ML recibe el evento
    ↓
Modelo clasifica: ¿Es amenaza?
    ↓
  ├── SÍ (confidence ≥ umbral) → Genera alerta temprana automática
  │       ↓
  │   Alerta aparece en Dashboard del SOC
  │       ↓
  │   Analista revisa alerta + explicación del modelo
  │       ↓
  │   Acción de mitigación
  │
  └── NO → Registro normal, sin alerta
```

**Párrafo debajo:** Explicar cómo este flujo transforma la gestión de reactiva a proactiva.

---

### 3.2.3 Identificación de participantes del proyecto

**Tabla 33 (Personal Involucrado):** Verificar que los nombres y roles estén correctos.

**Tabla 34 (Roles de Usuario):** El sistema real tiene **2 roles, NO 3**. Si la tabla lista un "Super Usuario", eliminarlo. Los roles son:

| Rol | Descripción | Permisos clave |
|-----|-------------|----------------|
| **Admin (Jefe SOC)** | Acceso completo | Subir archivos, generar reportes, gestionar usuarios, predicción |
| **Analyst (Analista SOC)** | Acceso de lectura + predicción | Predicción manual, ver reportes/alertas/historial, gestionar perfil |

---

### 3.2.4 Identificación de Requerimientos del Sistema

#### Requerimientos Funcionales (Tabla 37) — REHACER con 14 RF:

| ID | Nombre | Descripción |
|----|--------|-------------|
| RF01 | Autenticación JWT | Login/logout con tokens de 8 horas |
| RF02 | Gestión de usuarios | CRUD con roles admin/analyst |
| RF03 | Predicción manual Phishing | Formulario: remitente, destinatario, asunto, cuerpo, URLs → clasificación + explicación |
| RF04 | Predicción manual ATO | Formulario: usuario, país (97 países por riesgo), IP/device cambiados, hora, ASN, RTT |
| RF05 | Predicción manual Brute Force | Formulario con 60 campos en 12 tabs + 4 ejemplos precargados |
| RF06 | Carga de archivos | Subida CSV/Excel para análisis masivo. Max 50MB. Solo admin |
| RF07 | Generación de reportes | Análisis masivo enviando cada registro a la API ML |
| RF08 | Visualización de reportes | Lista con gráficos de distribución de amenazas y severidades |
| RF09 | Sistema de alertas tempranas | Alertas automáticas cuando predicciones superan umbrales (3 niveles) |
| RF10 | Dashboard de estadísticas | Cards: total predicciones, alertas por severidad, distribución por modelo |
| RF11 | Filtrado de alertas | Filtrar por modelo, severidad y rango de fechas |
| RF12 | Auditoría de predicciones | Registro automático: quién, cuándo, qué modelo, datos, resultado |
| RF13 | Explainabilidad | Indicadores de riesgo + evidencia + resumen en lenguaje natural |
| RF14 | Gestión de perfil | Cambio de contraseña desde perfil |

#### Requerimientos No Funcionales (Tabla 38) — REHACER con 8 RNF:

| ID | Nombre | Descripción |
|----|--------|-------------|
| RNF01 | Interfaz responsive | Paleta corporativa BCP (#004B8E, #F26E29), design tokens 3 niveles, Bootstrap 5.3 |
| RNF02 | Seguridad de autenticación | JWT HS256, tokens 8h, bcrypt para contraseñas, control por roles |
| RNF03 | Rendimiento | Predicciones individuales < 2 segundos |
| RNF04 | Compatibilidad | Chrome, Firefox, Edge versiones actuales |
| RNF05 | Validación de datos | Pydantic en todas las APIs |
| RNF06 | Arquitectura microservicios | 5 servicios independientes via HTTP/REST |
| RNF07 | Containerización | Docker Compose con healthchecks cada 30s |
| RNF08 | Código mantenible | Separación por capas (routers, services, schemas, models) |

---

### 3.2.5 Visión General de los Procesos del Sistema

**Figura 18 (Caso de Uso de Alto Nivel) — REHACER COMPLETAMENTE:**

Actores y casos de uso REALES del sistema:

```
Usuario No Autenticado:
  • Iniciar sesión

Analyst (todo lo siguiente):
  • Ver dashboard con estadísticas
  • Predicción manual de Phishing / ATO / Brute Force
  • Ver lista de reportes y detalle con gráficos
  • Ver alertas tempranas (con filtros)
  • Ver historial de predicciones
  • Gestionar perfil (cambiar contraseña)
  • Cerrar sesión

Admin (todo lo de Analyst +):
  • Subir archivos CSV/Excel
  • Generar reportes desde archivos
  • Gestionar usuarios (crear, editar, activar/desactivar)
```

**Relaciones <<include>>:**
- "Predicción manual" include → "Generar explicación" y "Registrar en auditoría"
- "Generar reporte" include → "Enviar a API ML" y "Evaluar umbrales → generar alertas"

**Tabla 39 (Procesos del Sistema) — REHACER con 9 procesos:**

| ID | Proceso | Descripción | Actores |
|----|---------|-------------|---------|
| P01 | Autenticación | Login/logout con JWT de 8 horas | Todos |
| P02 | Gestión de usuarios | CRUD con roles admin/analyst | Admin |
| P03 | Predicción manual | Clasificación por modelo + explicación | Admin, Analyst |
| P04 | Carga de archivos | Importación CSV/Excel para análisis masivo | Admin |
| P05 | Generación de reportes | Predicciones masivas sobre archivo subido | Admin |
| P06 | Visualización de reportes | Consulta con gráficos de distribución | Todos |
| P07 | Gestión de alertas | Visualización/filtrado por severidad y modelo | Todos |
| P08 | Auditoría de predicciones | Historial de predicciones manuales | Todos |
| P09 | Gestión de perfil | Cambio de contraseña | Todos |

---

## 3.3 — IDENTIFICACIÓN DE REQUERIMIENTOS

### 3.3.1 Priorización de requerimientos

**Tabla 40 (Product Backlog) — ACTUALIZAR** con los RF01-RF14 y RNF01-RNF08 listados arriba. Reorganizar prioridades según lo implementado.

---

### 3.3.2 Formación del Equipo Scrum

**Tabla 41:** Mantener si los datos son correctos.

---

## 3.4 — CONSTRUCCIÓN DEL DATASET

### Párrafo introductorio — REESCRIBIR

Explicar que se seleccionaron 3 datasets públicos internacionales alineados con los vectores de amenaza del BCP. NO usar la narrativa de "datos sintetizados". Justificar cada dataset:
- **CEAS_08**: Estándar de referencia para phishing con emails reales etiquetados
- **RBA Dataset**: Único dataset público de autenticación basada en riesgo con patrones de ATO
- **CSE-CIC-IDS2018**: Dataset de referencia del Canadian Institute for Cybersecurity

---

### 3.4.1 Recopilación y exploración de los datos disponibles

**Tabla resumen de datasets — REHACER (reemplaza tabla actual):**

| Dato | Phishing (CEAS_08) | Account Takeover (RBA) | Brute Force (CSE-CIC-IDS2018) |
|------|--------------------|-----------------------|-------------------------------|
| Fuente | Conference on Email and Anti-Spam 2008 | Zenodo (Freeman et al., 2016) | Canadian Institute for Cybersecurity |
| Tipo de datos | Texto de emails | Registros de login | Flujos de tráfico de red |
| Registros | 39,154 | 85,141 | 763,568 |
| Atributos originales | 5 (sender, receiver, subject, body, date) | ~20 (user_id, ip, country, browser, etc.) | 80+ (features de tráfico) |
| Variable objetivo | label (ham/spam) | is_attack (0/1) | Label (Benign/Attack) |
| Balance | 44% legítimo / 56% phishing | 99.83% normal / 0.17% ATO | 50% / 50% (post-balanceo) |

**Figuras 19-20 (Configuración de entorno, Estructura de directorios):** Actualizar screenshots con entorno real.

#### Para CADA dataset (3.4.1.1, 3.4.1.2, 3.4.1.3), incluir en este orden:

1. **Párrafo descriptivo** del dataset (origen, qué contiene, por qué se eligió)
2. **TABLA** — Distribución de clases (cantidad y porcentaje por clase)
3. **FIGURA** — Gráfico de barras de distribución de clases
4. **FIGURAS de exploración** específicas por dataset:
   - **Phishing**: Distribución de longitud de emails, Distribución de conteo de URLs
   - **ATO**: Distribución por país (top 10), Distribución por hora, **Porcentaje de cambio de país: ATO vs Normal** (98.6% de ATOs cambian país — el hallazgo más importante)
   - **Brute Force**: Comparativa de features clave ataque vs normal (ratios: Bwd Pkts/s 112.7x, Flow Pkts/s 24.7x, Flow Duration 0.01x)
5. **TABLA** — Estadísticas descriptivas comparando clases
6. **FIGURA** — Matriz de correlación de features relevantes
7. **Párrafo de hallazgos clave** del EDA

**Tablas de verificación de calidad (reemplaza Tabla 46):**

| Dataset | Problema | Severidad | Acción |
|---------|----------|-----------|--------|
| CEAS_08 | Emails vacíos o sin cuerpo | Baja | Eliminación |
| CEAS_08 | Caracteres especiales en texto | Media | Limpieza |
| RBA | Valores faltantes en region/city | Baja | Imputación |
| RBA | Desbalance extremo (0.17% ATO) | Alta | SMOTE en modelado |
| CSE-CIC-IDS2018 | Valores infinitos en features de velocidad | Media | Reemplazo por NaN |
| CSE-CIC-IDS2018 | Registros duplicados | Media | Eliminación |
| CSE-CIC-IDS2018 | Features con varianza cero | Baja | Eliminación de features |

**Tablas de variables de entrada/salida** — Una tabla por dataset con: Variable, Tipo, Rol (independiente/dependiente), Descripción.

---

### 3.4.2 Limpieza y Preparación de los Datos

#### 3.4.2.1 Carga de Datos
- **Screenshot de código:** Carga real de los 3 datasets
- **Tabla 50 (Info general)** — REHACER con datos reales (filas, columnas, memoria, tipo)

#### 3.4.2.2 Resultados de Preparación y Limpieza
- **Tabla 53 (Antes/después)** con números reales de limpieza por dataset
- **Tablas de distribución post-limpieza** para cada dataset, incluyendo split train/test:

  Para ATO, mostrar el efecto de SMOTE:
  | Conjunto | Normal | ATO | % ATO |
  |----------|--------|-----|-------|
  | Train (antes SMOTE) | 74,687 | 127 | 0.17% |
  | Train (después SMOTE) | 74,687 | 7,468 | 9.09% |
  | Test (sin SMOTE) | 16,999 | 30 | 0.17% |

---

### 3.4.3 Selección de variables relevantes

**Esta sección ahora incluye Feature Engineering + Selección. La TAREA no cambia, pero el ENTREGABLE se amplía.**

#### Pipeline de Ingeniería de Características — Para cada modelo:

**Phishing — DIAGRAMA de pipeline:**
```
Email crudo → Limpieza de texto → Tokenización → Eliminación stopwords
    ↓
┌──────────────────────┬────────────────────────────┐
│ TF-IDF (1,000 feat.) │ Features numéricas (16)     │
└──────────┬───────────┴──────────────┬─────────────┘
           └──── Concatenación ──────┘
                      ↓
             Vector: 1,016 features
```
- **TABLA** de las 16 features numéricas (body_length, url_count, has_urgent, sender_domain_encoded, etc.) con tipo, descripción e importancia
- **Párrafo** explicando TF-IDF (max_features=1000)
- **SCREENSHOT** de `feature_engineering.py` del modelo Phishing

**Account Takeover — DIAGRAMA de pipeline:**
```
Login crudo → Extracción temporal (7) + Comparación con login anterior (8)
            + Agregados por usuario (7) + Codificación categóricas (6)
            + Features de red (4) + Z-score RTT (1)
                      ↓
             Vector: 35 features
```
- **TABLA** de las 35 features organizadas por categoría (Temporales, Comportamiento, Geográficas, Red, Agregados, Categóricas)
- **Párrafo sobre SMOTE**: sampling_strategy=0.1, k_neighbors=5, aplicado SOLO a train
- **SCREENSHOT** del feature engineering + SMOTE del modelo ATO

**Brute Force — DIAGRAMA de pipeline:**
```
80+ features de red → Eliminar varianza cero → Eliminar redundantes
                    → Binarizar Label → Normalización Min-Max [0,1]
                      ↓
             Vector: 60 features normalizadas
```
- **TABLA** de las 60 features organizadas en 12 categorías (Puerto/Protocolo, Duración, Pkts Forward, Pkts Backward, Bytes/s, IAT, Flags PSH/URG, Pkts/s, Flags TCP, Ratios, Ventanas TCP, Actividad/Inactividad)
- **Párrafo** sobre normalización Min-Max
- **SCREENSHOT** del preprocesamiento

**Tabla resumen final de features:**

| Modelo | Features originales | Features finales | Técnica principal |
|--------|--------------------|-----------------:|-------------------|
| Phishing | 5 campos de texto | 1,016 | TF-IDF + extracción numérica |
| ATO | ~20 campos de login | 35 | Derivación temporal + comportamiento + SMOTE |
| Brute Force | 80+ métricas de red | 60 | Limpieza + normalización Min-Max |

**Selección de variables (importancia):** Para cada modelo, una **FIGURA** de barras horizontales con top 15 features más importantes (obtenidas del modelo entrenado con `model.feature_importances_`).

---

## 3.5 — DESARROLLO DEL MODELO DE PREDICCIÓN

### 3.5.1 Selección y evaluación de algoritmos

**Párrafo introductorio:** Siguiendo la fase de Modelado de CRISP-DM, se evaluaron 4 algoritmos de clasificación supervisada para cada dataset.

**TABLA — Algoritmos candidatos:**

| Algoritmo | Tipo | Justificación |
|-----------|------|---------------|
| Gradient Boosting | Ensemble secuencial | Alta precisión, robusto ante desbalance |
| Random Forest | Ensemble paralelo (bagging) | Rápido, interpretable, resistente a overfitting |
| SVM | Margen máximo | Buen rendimiento en alta dimensión |
| Regresión Logística | Lineal | Baseline interpretable |

**Para CADA dataset (3 subsecciones), incluir:**

1. **TABLA comparativa de 4 algoritmos:**

   | Algoritmo | F1-Score | Accuracy | Precision | Recall | ROC-AUC |
   |-----------|----------|----------|-----------|--------|---------|
   | **Gradient Boosting** | **99.09%** | **98.98%** | **98.91%** | **99.27%** | **99.90%** |
   | Random Forest | X% | X% | X% | X% | X% |
   | SVM | X% | X% | X% | X% | X% |
   | Regresión Logística | X% | X% | X% | X% | X% |

   (Completar con resultados reales. El modelo en negrita es el ganador)

2. **FIGURA** — Gráfico de barras comparativo de F1-Score de los 4 algoritmos
3. **Párrafo** justificando la selección del ganador
4. **TABLA** de hiperparámetros finales del modelo seleccionado
5. **SCREENSHOT** de la sección de entrenamiento del código

**Modelos ganadores por dataset:**
- Phishing → Gradient Boosting (F1=99.09%)
- ATO → Gradient Boosting + SMOTE (F1=75.86%)
- Brute Force → Random Forest (F1=99.97%)

---

### 3.5.2 Validación del modelo

**Para CADA modelo, incluir:**

1. **TABLA de métricas finales** (F1, Accuracy, Precision, Recall, ROC-AUC)
   - Para ATO: agregar columna "Nota" explicando que Accuracy 99.88% es engañoso por desbalance
2. **FIGURA — Matriz de confusión (heatmap 2x2)** con TP, TN, FP, FN numéricos
3. **FIGURA — Curva ROC** con AUC marcada + línea diagonal de referencia
   - Para ATO: agregar también **Curva Precision-Recall** (más informativa en datasets desbalanceados)
4. **FIGURA — Top 15 features más importantes** (barras horizontales)
5. **Párrafo de interpretación** de los resultados

**Después de los 3 modelos individuales:**

**Tabla comparativa general:**

| Modelo | Algoritmo | Features | F1-Score | Precision | Recall | ROC-AUC |
|--------|-----------|----------|----------|-----------|--------|---------|
| Phishing | Gradient Boosting | 1,016 | 99.09% | 98.91% | 99.27% | 99.90% |
| ATO | Gradient Boosting + SMOTE | 35 | 75.86% | 73.33% | 78.57% | 98.06% |
| Brute Force | Random Forest | 60 | 99.97% | 99.99% | 99.99% | ~100% |

**FIGURA** — Gráfico de barras agrupadas de los 3 modelos lado a lado.

**Párrafo de análisis comparativo:**
- Brute Force: mejor rendimiento (tráfico automatizado genera patrones muy distintivos)
- Phishing: excelente (TF-IDF captura vocabulario predecible)
- ATO: más desafiante por desbalance extremo (0.17%), pero ROC-AUC 98.06% confirma buena discriminación
- Los 3 modelos son aptos para producción

## 3.6 — DESARROLLO DEL SISTEMA

### 3.6.1 Diseño de la Base de Datos

**Diseño lógico — DIAGRAMA ENTIDAD-RELACIÓN (5 tablas):**

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│     User     │──1:N─│ UploadedFile │──1:N─│    Report    │──1:N─┐
├──────────────┤      ├──────────────┤      ├──────────────┤      │
│ id (PK)      │      │ id (PK)      │      │ id (PK)      │      │
│ username     │      │ filename     │      │ file_id (FK) │      │
│ email        │      │ file_path    │      │ created_by   │      │
│ password_hash│      │ uploaded_by  │      │ model_type   │      │
│ role         │      │ row_count    │      │ total_records│      │
│ is_active    │      │ detected_model│     │ threats_det. │      │
│ created_at   │      │ created_at   │      │ results_json │      │
└──────┬───────┘      └──────────────┘      │ created_at   │      │
       │                                     └──────────────┘      │
       │                                                           │
       │──1:N─┐                                    ┌───────────────┘
       │      │                                    │
       │  ┌───┴──────────┐                ┌────────┴───────┐
       │  │  Prediction  │                │     Alert      │
       │  ├──────────────┤                ├────────────────┤
       │  │ id (PK)      │                │ id (PK)        │
       │  │ created_by   │                │ report_id (FK) │
       │  │ model_type   │                │ model_type     │
       │  │ prediction   │                │ severity       │
       │  │ pred_label   │                │ confidence     │
       │  │ confidence   │                │ description    │
       │  │ input_data   │                │ input_data     │
       │  │ explanation  │                │ created_at     │
       │  │ created_at   │                └────────────────┘
       │  └──────────────┘
```

**Diseño físico:** Explicar que se usa **SQLite** (no PostgreSQL). Justificar: sistema de archivo único, sin necesidad de servidor de BD separado, suficiente para el volumen de datos del SOC.

**Diccionario de la base de datos** — TABLA con las 5 tablas:

| Tabla | Campo | Tipo SQLite | Restricciones | Descripción |
|-------|-------|-------------|---------------|-------------|
| users | id | INTEGER | PK, AUTOINCREMENT | Identificador único |
| users | username | VARCHAR | UNIQUE, NOT NULL | Nombre de usuario |
| users | role | VARCHAR | NOT NULL | "admin" o "analyst" |
| ... | ... | ... | ... | (completar todos los campos de las 5 tablas) |

---

### 3.6.2 Diseño de la Arquitectura de Software

**DIAGRAMA de arquitectura de microservicios:**

```
┌───────────────────────────────────────────────┐
│              Frontend React (:5173/80)         │
└────────────────────┬──────────────────────────┘
                     │ HTTP
                     ▼
┌───────────────────────────────────────────────┐
│          Auth Gateway (:8003)                  │
│    FastAPI + JWT + SQLite + bcrypt              │
└──────┬──────────────┬──────────────┬──────────┘
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Phishing │   │   ATO    │   │  Brute   │
│   :8000  │   │  :8001   │   │  Force   │
│ Gradient │   │ Gradient │   │  :8002   │
│ Boosting │   │Boosting+ │   │ Random   │
│ +TF-IDF  │   │  SMOTE   │   │ Forest   │
└──────────┘   └──────────┘   └──────────┘
```

**TABLA de servicios:**

| Servicio | Puerto | Tecnología | Función |
|----------|--------|-----------|---------|
| Phishing API | 8000 | FastAPI + scikit-learn | Clasificación de emails |
| ATO API | 8001 | FastAPI + scikit-learn + imbalanced-learn | Clasificación de logins |
| Brute Force API | 8002 | FastAPI + scikit-learn | Clasificación de tráfico |
| Auth Gateway | 8003 | FastAPI + SQLAlchemy + JWT | Autenticación y proxy |
| Frontend | 5173/80 | React + Vite + Bootstrap | Dashboard web |

**Párrafo:** Justificar por qué microservicios (independencia, escalabilidad individual, actualización de modelos sin afectar otros servicios).

---

### 3.6.3 Sprint 1: Módulo de Autenticación y Usuarios

#### 3.6.3.1 Inicio del Sprint 1

**Sprint Backlog** — Tabla con formato de la Tabla 29:

| Sprint | Título | Objetivo | HU consideradas | Responsable |
|--------|--------|----------|-----------------|-------------|
| 1 | Autenticación y Usuarios | Implementar login JWT, gestión de usuarios con roles y perfil | HU-01 (Login), HU-02 (Gestión usuarios), HU-14 (Perfil) | (tu nombre) |

#### 3.6.3.2 Diseño de funcionalidad

**Diagrama de caso de uso expandido** para este sprint. Casos de uso:
- Iniciar sesión (entrada: username/password → salida: JWT token)
- Cerrar sesión (elimina token del localStorage)
- Crear usuario (admin ingresa datos → se crea con bcrypt hash)
- Editar usuario (admin cambia rol o datos)
- Activar/Desactivar usuario (admin toggle is_active)
- Cambiar contraseña (usuario desde su perfil)

**Diseño navegacional** — Flujo de pantallas del módulo:
```
Login → (auth OK) → Dashboard
                      ├── /users (solo admin) → Crear/Editar/Activar-Desactivar
                      └── /profile → Cambiar contraseña
```

#### 3.6.3.3 Diseño de Interfaz

**Mockups** (wireframes) de:
- Página de Login (campos username/password, botón, logo BCP)
- Página de gestión de usuarios (tabla con acciones)
- Página de perfil (formulario de cambio de contraseña)

#### 3.6.3.4 Desarrollo de interfaces

**SCREENSHOTS del sistema corriendo:**
- Screenshot de la página de Login real
- Screenshot de la tabla de gestión de usuarios
- Screenshot de la página de perfil

#### 3.6.3.5 Codificación

**SCREENSHOTS de código relevante:**
- `auth_service.py`: función de generación de JWT y verificación de bcrypt
- `users.py` (router): endpoints CRUD
- `LoginForm.jsx`: componente del formulario de login

#### 3.6.3.6 Pruebas Unitarias

**TABLA de pruebas:**

| ID | Caso | Entrada | Resultado Esperado | Estado |
|----|------|---------|--------------------|--------|
| PU1.1 | Login válido | admin/admin123 | JWT token recibido | Pasó |
| PU1.2 | Login inválido | admin/wrongpass | Error 401 | Pasó |
| PU1.3 | Crear usuario | Datos válidos | Usuario creado | Pasó |
| PU1.4 | Acceso sin rol | Analyst → /users | Error 403 | Pasó |
| PU1.5 | Cambiar contraseña | Contraseña válida | Actualizada | Pasó |

---

### 3.6.4 Sprint 2: Módulo de Gestión de Incidentes

> En el sistema real, "Gestión de Incidentes" se implementa como **Carga de Archivos + Generación de Reportes**, que es el mecanismo para analizar incidentes masivamente.

#### 3.6.4.1 Inicio del Sprint 2

**Sprint Backlog:**

| Sprint | Título | Objetivo | HU consideradas | Responsable |
|--------|--------|----------|-----------------|-------------|
| 2 | Gestión de Incidentes | Implementar subida de archivos CSV/Excel y generación de reportes con análisis masivo | HU-06 (Archivos), HU-07 (Reportes), HU-08 (Ver reportes) | (tu nombre) |

#### 3.6.4.2 Diseño de funcionalidad

**Casos de uso expandidos:**
- Subir archivo CSV/Excel (admin selecciona archivo → se valida tipo/tamaño → se detecta modelo → se guarda)
- Generar reporte (admin selecciona archivo → se envía cada fila a API ML → se generan alertas → se guarda reporte)
- Ver lista de reportes (todos ven reportes con estadísticas)
- Ver detalle de reporte (gráficos de distribución + tabla de resultados)

**Diseño navegacional:**
```
Dashboard → /files (admin) → Subir archivo → Generar reporte
         → /reports → Lista de reportes → /reports/:id (Detalle con gráficos)
```

#### 3.6.4.3 Diseño de interfaz
**Mockups** de: Zona de subida (drag & drop), Lista de reportes, Detalle de reporte con gráficos

#### 3.6.4.4 Desarrollo de interfaces
**SCREENSHOTS:** Subida de archivos, Lista de reportes, Detalle con gráfico pie + tabla de resultados

#### 3.6.4.5 Codificación
**SCREENSHOTS de código:** `report_service.py` (lógica de batch prediction), `files.py` (router de subida)

#### 3.6.4.6 Pruebas Unitarias

| ID | Caso | Entrada | Resultado Esperado | Estado |
|----|------|---------|--------------------|--------|
| PU2.1 | Subir CSV válido | archivo.csv (100 filas) | Archivo guardado, modelo detectado | Pasó |
| PU2.2 | Subir archivo inválido | archivo.txt | Error de validación | Pasó |
| PU2.3 | Subir como analyst | Analyst intenta subir | Error 403 | Pasó |
| PU2.4 | Generar reporte | Archivo de phishing | Reporte creado con conteo | Pasó |
| PU2.5 | Ver detalle reporte | GET /reports/:id | Gráficos y tabla | Pasó |

---

### 3.6.5 Sprint 3: Módulo de Predicción de Amenazas

#### 3.6.5.1 Inicio del Sprint 3

**Sprint Backlog:**

| Sprint | Título | Objetivo | HU consideradas | Responsable |
|--------|--------|----------|-----------------|-------------|
| 3 | Predicción de Amenazas | Implementar predicción manual de los 3 modelos con formularios, resultados, explicación y auditoría | HU-03 (Phishing), HU-04 (ATO), HU-05 (BF), HU-12 (Auditoría), HU-13 (Explainabilidad) | (tu nombre) |

#### 3.6.5.2 Diseño de funcionalidad

**Casos de uso expandidos:**
- Seleccionar modelo (usuario elige entre Phishing, ATO, Brute Force)
- Predecir Phishing (llena formulario o carga ejemplo → envía → resultado + explicación)
- Predecir ATO (formulario con país por riesgo, IP/device cambiados, hora, etc.)
- Predecir Brute Force (modal con 60 campos en 12 tabs o carga ejemplo precargado)
- Ver explicación (indicadores de riesgo con severidad + resumen en lenguaje natural)
- Ver historial de predicciones (tabla con filtros por modelo/fecha)

**DIAGRAMA DE SECUENCIA — Flujo de predicción:**
```
Usuario → Llena formulario → Frontend POST Auth Gateway (+JWT)
→ Gateway verifica JWT → Gateway POST API ML (:800X)
→ API carga modelo .pkl → Feature engineering → Predicción + Explicación
→ Respuesta a Gateway → Gateway guarda en tabla Prediction (auditoría)
→ Respuesta a Frontend → Muestra tarjeta de resultado con explicación
```

**Diseño navegacional:**
```
Dashboard → /dashboard/predict → Selector de modelo
  → Phishing Form (campos: remitente, destinatario, asunto, cuerpo, URLs)
  → ATO Form (campos: usuario, país, IP/device cambiados, hora, ASN, RTT)
  → BF Form (modal 12 tabs con 60 campos)
  → Resultado: tarjeta con predicción + barra de confianza + indicadores de riesgo
```

#### 3.6.5.3 Diseño de interfaz
**Mockups** de: Selector de modelo, Formulario Phishing, Formulario ATO, Modal BF (con tabs), Tarjeta de resultado con explicación

#### 3.6.5.4 Desarrollo de interfaces
**SCREENSHOTS (los más numerosos del proyecto):**
- Selector de modelo
- Formulario de Phishing con ejemplo precargado
- Formulario de ATO con ejemplo precargado
- Modal de Brute Force con tabs
- Resultado: PHISHING DETECTADO (tarjeta roja, barra 97%+, indicadores)
- Resultado: EMAIL LEGÍTIMO (tarjeta verde, barra 95%+)
- Resultado: ACCOUNT TAKEOVER DETECTADO (tarjeta roja, indicadores geo)
- Resultado: LOGIN NORMAL (tarjeta verde)
- Resultado: ATAQUE DE FUERZA BRUTA (tarjeta roja, features destacadas)
- Resultado: TRÁFICO NORMAL (tarjeta verde)

#### 3.6.5.5 Codificación
**SCREENSHOTS de código:**
- `predictor.py` de Phishing (feature engineering + TF-IDF + predicción + generación de explicación)
- `predictor.py` de ATO (feature derivation + predicción + geo_info)
- `predictor.py` de Brute Force (normalización + predicción + top_features)
- `predictions.py` (router del Auth Gateway para guardar auditoría)

#### 3.6.5.6 Pruebas Unitarias

| ID | Caso | Entrada | Resultado Esperado | Estado |
|----|------|---------|--------------------|--------|
| PU3.1 | Phishing (ataque) | Email PayPal falso con URL | PHISHING 97%+ | Pasó |
| PU3.2 | Phishing (legítimo) | Email interno sin URLs | LEGÍTIMO 95%+ | Pasó |
| PU3.3 | ATO (ataque) | Login desde Rusia, IP/device cambiados, 3AM | ATO 85%+ | Pasó |
| PU3.4 | ATO (legítimo) | Login desde Bolivia, sin cambios, 9:30 AM | NORMAL 95%+ | Pasó |
| PU3.5 | BF (ataque SSH) | Tráfico puerto 22, alta velocidad | ATAQUE 99%+ | Pasó |
| PU3.6 | BF (normal) | Tráfico web normal puerto 80 | NORMAL 99%+ | Pasó |
| PU3.7 | Auditoría | Después de predicción | Registro en tabla Prediction | Pasó |
| PU3.8 | Explicación | Cualquier predicción | risk_indicators + summary presentes | Pasó |

---

### 3.6.6 Sprint 4: Módulo de Alertas Tempranas

#### 3.6.6.1 Inicio del Sprint 4

**Sprint Backlog:**

| Sprint | Título | Objetivo | HU consideradas | Responsable |
|--------|--------|----------|-----------------|-------------|
| 4 | Alertas Tempranas | Implementar generación automática de alertas basadas en umbrales de confianza, con visualización y filtros | HU-09 (Alertas), HU-11 (Filtrado) | (tu nombre) |

#### 3.6.6.2 Diseño de funcionalidad

**Casos de uso expandidos:**
- Ver alertas (lista con badges de severidad: Critical=rojo, High=naranja, Medium=amarillo)
- Filtrar alertas (por modelo, severidad, rango de fechas)
- Ver estadísticas de alertas (conteos por severidad y modelo)

**DIAGRAMA DE FLUJO del sistema de alertas:**
```
Reporte generado → Para cada predicción con prediction=1 (amenaza):
  → ¿Confianza ≥ umbral_critical? → CRITICAL (rojo)
  → ¿Confianza ≥ umbral_high? → HIGH (naranja)
  → ¿Confianza ≥ umbral_medium? → MEDIUM (amarillo)
  → Crear alerta en BD → Badge se actualiza en TopBar/Sidebar
```

**TABLA de umbrales:**

| Modelo | Critical (≥) | High (≥) | Medium (≥) | Justificación |
|--------|-------------|----------|------------|---------------|
| Phishing | 95% | 85% | 75% | F1=99.09%, alta precisión |
| ATO | 90% | 80% | 70% | F1=75.86%, más conservador |
| Brute Force | 98% | 90% | 80% | F1=99.97%, precisión casi perfecta |

**Diseño navegacional:**
```
Dashboard (badge de alertas en TopBar y Sidebar) → /alerts → Filtros laterales → Detalle de alerta
```

#### 3.6.6.3 Diseño de interfaz
**Mockups** de: Página de alertas con badges de severidad, Panel de filtros, Badge de conteo en TopBar

#### 3.6.6.4 Desarrollo de interfaces
**SCREENSHOTS:** Alertas con severidades (Critical/High/Medium), Filtros aplicados, Badge de conteo en TopBar

#### 3.6.6.5 Codificación
**SCREENSHOTS de código:**
- `alert_service.py` (lógica de evaluación de umbrales y creación de alertas)
- `config.py` (configuración de umbrales por modelo)
- `alerts.py` (router con filtros)

#### 3.6.6.6 Pruebas Unitarias

| ID | Caso | Entrada | Resultado Esperado | Estado |
|----|------|---------|--------------------|--------|
| PU4.1 | Alerta critical | Predicción phishing 97% | Alerta CRITICAL creada | Pasó |
| PU4.2 | Alerta high | Predicción ATO 82% | Alerta HIGH creada | Pasó |
| PU4.3 | Sin alerta | Predicción BF 75% (< umbral 80%) | No se crea alerta | Pasó |
| PU4.4 | Filtrar por modelo | Filtro: phishing | Solo alertas de phishing | Pasó |
| PU4.5 | Badge de conteo | Nuevas alertas generadas | Badge actualizado | Pasó |

---

### 3.6.7 Sprint 5: Módulo de Dashboard y Reportes

#### 3.6.7.1 Inicio del Sprint 5

**Sprint Backlog:**

| Sprint | Título | Objetivo | HU consideradas | Responsable |
|--------|--------|----------|-----------------|-------------|
| 5 | Dashboard y Reportes | Implementar dashboard con estadísticas, gráficos de distribución y reportes mensuales | HU-10 (Dashboard) | (tu nombre) |

#### 3.6.7.2 Diseño de funcionalidad

**Casos de uso expandidos:**
- Ver dashboard (cards con total predicciones, alertas activas por severidad, distribución por modelo)
- Ver gráficos de distribución (pie charts, bar charts)
- Reportes mensuales (resumen por mes)

**Diseño navegacional:**
```
/dashboard → Cards de estadísticas + Gráficos de distribución
           → Selector de reportes mensuales
```

#### 3.6.7.3 Diseño de interfaz
**Mockups** de: Dashboard con cards, Gráficos de distribución, Selector mensual

#### 3.6.7.4 Desarrollo de interfaces
**SCREENSHOTS:** Dashboard completo con cards de estadísticas, Gráficos de distribución por modelo

#### 3.6.7.5 Codificación
**SCREENSHOTS de código:** `DashboardOverview.jsx`, componentes de charts

#### 3.6.7.6 Pruebas Unitarias

| ID | Caso | Entrada | Resultado Esperado | Estado |
|----|------|---------|--------------------|--------|
| PU5.1 | Dashboard carga | GET /dashboard | Cards con datos correctos | Pasó |
| PU5.2 | Estadísticas | Después de predicciones | Conteos actualizados | Pasó |
| PU5.3 | Gráficos | Datos disponibles | Charts renderizados | Pasó |

---

### 3.6.8 Integración del modelo al sistema

**Contenido de esta sección:**

1. **Párrafo** explicando que siguiendo la fase de Implementación de CRISP-DM, los modelos entrenados (.pkl) se despliegan como servicios API independientes usando FastAPI.

2. **DIAGRAMA de arquitectura Docker:**
```
┌──────────────────────────────────────────────────┐
│            cybersecurity-network (bridge)          │
│                                                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐     │
│  │phishing-api│ │  ato-api   │ │brute-force │     │
│  │   :8000    │ │   :8001    │ │ -api :8002 │     │
│  │python:3.12 │ │python:3.12 │ │python:3.12 │     │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘     │
│        └──────────────┼──────────────┘             │
│                       ▼                            │
│             ┌──────────────────┐                   │
│             │   auth-gateway   │                   │
│             │      :8003       │                   │
│             └────────┬─────────┘                   │
│        ┌─────────────┴─────────────┐               │
│        ▼                           ▼               │
│  [auth-gateway-data]     [auth-gateway-uploads]    │
│  (SQLite DB)             (archivos)                │
│                                                    │
│             ┌──────────────────┐                   │
│             │     frontend     │                   │
│             │   :80 (nginx)    │                   │
│             └──────────────────┘                   │
└──────────────────────────────────────────────────┘
```

3. **TABLA de contenedores:**

| Contenedor | Imagen Base | Puerto | Healthcheck |
|------------|-------------|--------|-------------|
| phishing-api | python:3.12-slim | 8000 | GET /docs cada 30s |
| ato-api | python:3.12-slim | 8001 | GET /docs cada 30s |
| brute-force-api | python:3.12-slim | 8002 | GET /docs cada 30s |
| auth-gateway | python:3.12-slim | 8003 | GET /health cada 30s |
| frontend | nginx:alpine | 80 | GET /health cada 30s |

4. **TABLA de volúmenes:**

| Volumen | Ruta en Container | Propósito |
|---------|-------------------|-----------|
| auth-gateway-data | /app/data | Base de datos SQLite |
| auth-gateway-uploads | /app/uploads | Archivos subidos |

5. **Párrafo** sobre Docker Compose, red bridge, healthchecks (30s intervalo, 10s timeout, 3 retries), orden de arranque.

6. **SCREENSHOT** de `docker-compose ps` o Docker Desktop con los 5 contenedores corriendo.

---

### 3.6.9 Pruebas del modelo en el sistema

**Contenido:**

1. **SCREENSHOTS del sistema integrado corriendo** — Captura mostrando todos los servicios activos (Docker Desktop o terminal con docker-compose up).

2. **Pruebas de predicciones en tiempo real (end-to-end):**

**DIAGRAMA de flujo end-to-end:**
```
Login → JWT → Seleccionar Phishing → Llenar formulario →
Envía POST → Auth Gateway → Phishing API :8000 →
Modelo .pkl → Feature eng + TF-IDF → Predicción + Explicación →
Respuesta → Auth Gateway guarda auditoría → Frontend muestra resultado
```

3. **TABLA de tiempos de respuesta:**

| Endpoint | Método | Tiempo Promedio | Cumple RNF03 |
|----------|--------|-----------------|--------------|
| POST /auth/login | Auth | ~Xms | Sí |
| POST /predict (Phishing) | Predicción | ~Xms | Sí/No |
| POST /predict (ATO) | Predicción | ~Xms | Sí/No |
| POST /predict (Brute Force) | Predicción | ~Xms | Sí/No |
| POST /reports/generate (100 reg.) | Batch | ~Xs | N/A |

(Medir tiempos reales y completar)

---

## 3.7 — VALIDACIÓN DEL SISTEMA

### 3.7.1 Identificación de puntos fuertes y áreas de mejora

**Contenido:**

1. **Párrafo de fortalezas del sistema:**
   - 3 modelos de ML funcionando con métricas altas (F1: 99.09%, 75.86%, 99.97%)
   - Arquitectura de microservicios escalable
   - Alertas tempranas automáticas con umbrales configurables
   - Explainabilidad en cada predicción
   - Containerización completa con Docker
   - Auditoría de predicciones

2. **Párrafo de limitaciones:**
   - Modelo ATO tiene F1 de 75.86% por desbalance extremo del dataset
   - Sistema no integrado con SIEM del BCP (funciona independiente)
   - No incluye forecasting temporal (clasificación en tiempo real, no predicción futura)
   - Datasets públicos, no datos reales del BCP

3. **Párrafo de trabajo futuro:**
   - Integración con SIEM (Splunk, Elastic SIEM)
   - Modelos de series temporales para forecasting
   - Reentrenamiento automático de modelos
   - Kubernetes para escalamiento en producción

---

### 3.7.2 Obtención de retroalimentación

**TABLA de pruebas de validación funcional (15+ escenarios):**

| ID | Escenario | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|----|-----------|-----------------|-------------------|-------------------|--------|
| PV01 | Login válido | admin / admin123 | JWT recibido | (completar) | |
| PV02 | Login inválido | admin / wrongpass | Error 401 | (completar) | |
| PV03 | Phishing (ataque) | Email PayPal falso | PHISHING 97%+ | (completar) | |
| PV04 | Phishing (legítimo) | Email interno | LEGÍTIMO 95%+ | (completar) | |
| PV05 | ATO (ataque) | Login Rusia, cambios | ATO 85%+ | (completar) | |
| PV06 | ATO (legítimo) | Login Bolivia, sin cambios | NORMAL 95%+ | (completar) | |
| PV07 | BF (ataque SSH) | Puerto 22, alta velocidad | ATAQUE 99%+ | (completar) | |
| PV08 | BF (normal) | Tráfico web normal | NORMAL 99%+ | (completar) | |
| PV09 | Subir archivo (admin) | CSV 100 filas | Procesado | (completar) | |
| PV10 | Subir archivo (analyst) | Intentar subir | Error 403 | (completar) | |
| PV11 | Generar reporte | Desde archivo | Reporte con gráficos | (completar) | |
| PV12 | Alertas generadas | Reporte con amenazas | Alertas con severidad | (completar) | |
| PV13 | Crear usuario (admin) | Datos válidos | Usuario creado | (completar) | |
| PV14 | Acceso /users (analyst) | Analyst navega | Acceso denegado | (completar) | |
| PV15 | Explicación presente | Predicción cualquiera | risk_indicators + summary | (completar) | |

(Completar las columnas ejecutando las pruebas reales. Agregar SCREENSHOTS de las pruebas más importantes: PV03, PV05, PV07, PV10, PV12)

**Lista de acciones de mejora continua:**
- Mejora 1: Reentrenar modelo ATO con más datos de ataques
- Mejora 2: Integrar con SIEM para alimentación automática de datos
- Mejora 3: Agregar forecasting temporal como fase 2
- (Agregar las que correspondan según retroalimentación real)

---
---

# RESUMEN DE ENTREGABLES

## Diagramas a crear

| # | Tipo | Sección | Descripción |
|---|------|---------|-------------|
| 1 | Flujo | 3.2.2 | Proceso propuesto con el sistema predictivo |
| 2 | Caso de Uso | 3.2.5 | Alto nivel con actores y casos de uso reales |
| 3 | Pipeline | 3.4.3 | Feature Engineering Phishing (×1) |
| 4 | Pipeline | 3.4.3 | Feature Engineering ATO (×1) |
| 5 | Pipeline | 3.4.3 | Feature Engineering Brute Force (×1) |
| 6 | Barras | 3.5.1 | Comparativa 4 algoritmos por dataset (×3) |
| 7 | Heatmap | 3.5.2 | Matriz de confusión (×3) |
| 8 | Curva | 3.5.2 | Curva ROC (×3) + Precision-Recall para ATO |
| 9 | Barras | 3.5.2 | Importancia features top 15 (×3) |
| 10 | Barras | 3.5.2 | Comparativa general 3 modelos |
| 11 | E-R | 3.6.1 | Entidad-Relación (5 tablas) |
| 12 | Arquitectura | 3.6.2 | Microservicios (5 servicios + puertos) |
| 13 | Secuencia | 3.6.5.2 | Flujo de predicción end-to-end |
| 14 | Flujo | 3.6.6.2 | Sistema de alertas (umbrales → severidad) |
| 15 | Docker | 3.6.8 | Arquitectura Docker (contenedores + red + volúmenes) |
| + | Caso uso expandido | 3.6.X.2 | Uno por sprint (×5) |
| + | Navegacional | 3.6.X.2 | Uno por sprint (×5) |

## Screenshots a tomar

| # | Pantalla | Sección |
|---|----------|---------|
| 1 | Login | 3.6.3.4 |
| 2 | Gestión de usuarios | 3.6.3.4 |
| 3 | Perfil | 3.6.3.4 |
| 4 | Subida de archivos | 3.6.4.4 |
| 5 | Lista de reportes | 3.6.4.4 |
| 6 | Detalle de reporte con gráficos | 3.6.4.4 |
| 7 | Selector de modelo | 3.6.5.4 |
| 8 | Formulario Phishing | 3.6.5.4 |
| 9 | Formulario ATO | 3.6.5.4 |
| 10 | Modal Brute Force (tabs) | 3.6.5.4 |
| 11 | Resultado: Phishing detectado | 3.6.5.4 |
| 12 | Resultado: ATO detectado | 3.6.5.4 |
| 13 | Resultado: BF detectado | 3.6.5.4 |
| 14 | Alertas con severidades | 3.6.6.4 |
| 15 | Dashboard completo | 3.6.7.4 |
| 16 | Docker containers corriendo | 3.6.8 |
| + | Código relevante | 3.6.X.5 (×5 sprints) |

## Tablas a crear

| # | Tabla | Sección |
|---|-------|---------|
| 1 | Roles de usuario (2 roles) | 3.2.4 |
| 2 | Requerimientos funcionales (RF01-RF14) | 3.2.4 |
| 3 | Requerimientos no funcionales (RNF01-RNF08) | 3.2.4 |
| 4 | Procesos del sistema (9) | 3.2.5 |
| 5 | Product Backlog actualizado | 3.3.1 |
| 6 | Resumen de 3 datasets | 3.4.1 |
| 7 | Distribución de clases (×3) | 3.4.1 |
| 8 | Estadísticas descriptivas (×3) | 3.4.1 |
| 9 | Problemas de calidad | 3.4.1 |
| 10 | Variables entrada/salida (×3) | 3.4.1 |
| 11 | Info general post-carga | 3.4.2 |
| 12 | Antes/después limpieza | 3.4.2 |
| 13 | Features por modelo (16, 35, 60) | 3.4.3 |
| 14 | Resumen features finales | 3.4.3 |
| 15 | Algoritmos candidatos | 3.5.1 |
| 16 | Comparativa 4 algoritmos (×3) | 3.5.1 |
| 17 | Hiperparámetros (×3) | 3.5.1 |
| 18 | Métricas finales (×3) | 3.5.2 |
| 19 | Comparativa general 3 modelos | 3.5.2 |
| 20 | Diccionario BD (5 tablas) | 3.6.1 |
| 21 | Servicios del sistema | 3.6.2 |
| 22 | Sprint Backlog (×5) | 3.6.X.1 |
| 23 | Pruebas unitarias (×5) | 3.6.X.6 |
| 24 | Umbrales de alertas | 3.6.6.2 |
| 25 | Contenedores Docker | 3.6.8 |
| 26 | Tiempos de respuesta | 3.6.9 |
| 27 | Pruebas de validación (15+) | 3.7.2 |

---

# MAPEO: OBJETIVO ESPECÍFICO → SECCIÓN

| Objetivo Específico | Secciones que lo cubren |
|---------------------|-------------------------|
| **OE1:** Analizar datos históricos mediante procesamiento y normalización | 3.4.1 (EDA), 3.4.2 (Limpieza), 3.4.3 (Feature Engineering) |
| **OE2:** Construir dataset etiquetado mediante limpieza y estructuración | 3.4.2 (Limpieza), 3.4.3 (Feature Engineering + Selección) |
| **OE3:** Determinar y entrenar modelos de ML supervisado | 3.5.1 (Selección y evaluación), 3.5.2 (Validación y métricas) |
| **OE4:** Integrar modelos al sistema con alertas tempranas | 3.6 completo (Sistema: BD, arquitectura, 5 sprints, Docker), especialmente Sprint 4 (Alertas) |
| **OE5:** Validación y evaluación técnica | 3.5.2 (Métricas ML), 3.6.9 (Pruebas en sistema), 3.7 (Validación completa) |

---

# ORDEN DE TRABAJO SUGERIDO

1. **Primero:** Generar figuras de EDA de los 3 datasets reales → para 3.4.1
2. **Segundo:** Documentar feature engineering real → para 3.4.3
3. **Tercero:** Generar figuras de evaluación (matrices confusión, ROC, features) → para 3.5.2
4. **Cuarto:** Tomar screenshots del frontend (16+) → para los 5 sprints
5. **Quinto:** Crear diagramas UML (caso uso, secuencia, E-R, arquitectura) → para 3.2.5, 3.6
6. **Sexto:** Redactar contenido de cada sprint (Sprint Backlog → Pruebas) → para 3.6.3-3.6.7
7. **Séptimo:** Actualizar secciones existentes (3.1-3.4) con datos correctos
8. **Octavo:** Completar pruebas de validación → para 3.7
9. **Último:** Actualizar Tabla 31 e índices de figuras/tablas
