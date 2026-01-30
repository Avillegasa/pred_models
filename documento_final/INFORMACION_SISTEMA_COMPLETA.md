# DOCUMENTACION COMPLETA DEL SISTEMA PREDICTIVO DE INCIDENTES DE CIBERSEGURIDAD

## INFORMACION PARA TRABAJO DE GRADO

**Fecha de actualizacion:** 2026-01-30
**Autor del sistema:** Andres Alvaro Villegas Salazar
**Institucion:** Escuela Militar de Ingenieria - Bolivia
**Caso de estudio:** Banco de Credito de Bolivia

---

# INDICE

1. [RESUMEN EJECUTIVO](#parte-1-resumen-ejecutivo)
2. [CUMPLIMIENTO DE OBJETIVOS](#parte-2-cumplimiento-de-objetivos)
   - [Objetivo 1: Analisis de Datos Historicos](#objetivo-1-analisis-de-datos-historicos)
   - [Objetivo 2: Construccion del Dataset Etiquetado](#objetivo-2-construccion-del-dataset-etiquetado)
   - [Objetivo 3: Determinacion y Entrenamiento de Modelos](#objetivo-3-determinacion-y-entrenamiento-de-modelos)
   - [Objetivo 4: Integracion y Alertas Tempranas](#objetivo-4-integracion-y-alertas-tempranas)
   - [Objetivo 5: Validacion y Evaluacion Tecnica](#objetivo-5-validacion-y-evaluacion-tecnica)
3. [ARQUITECTURA DEL SISTEMA](#parte-3-arquitectura-del-sistema)
4. [MODELO 1: PHISHING DETECTION](#parte-4-modelo-1-phishing-email-detection)
5. [MODELO 2: ACCOUNT TAKEOVER](#parte-5-modelo-2-account-takeover-detection)
6. [MODELO 3: BRUTE FORCE](#parte-6-modelo-3-brute-force-detection)
7. [AUTH GATEWAY](#parte-7-auth-gateway)
8. [FRONTEND DASHBOARD](#parte-8-frontend-dashboard)
9. [SISTEMA DE ALERTAS TEMPRANAS](#parte-9-sistema-de-alertas-tempranas)
10. [EXPLAINABILIDAD DE PREDICCIONES](#parte-10-explainabilidad-de-predicciones)
11. [FLUJOS DEL SISTEMA](#parte-11-flujos-del-sistema)
12. [METODOLOGIAS UTILIZADAS](#parte-12-metodologias-utilizadas)
13. [INSTRUCCIONES DE EJECUCION](#parte-13-instrucciones-de-ejecucion)
14. [CONCLUSIONES](#parte-14-conclusiones)
15. [ANEXOS](#parte-15-anexos)
    - [Anexo A: Glosario de Terminos](#anexo-a-glosario-de-terminos)
    - [Anexo B: Referencias Bibliograficas](#anexo-b-referencias-bibliograficas)
    - [Anexo C: Configuracion del Repositorio y Git LFS](#anexo-c-configuracion-del-repositorio-y-git-lfs)
    - [Anexo D: Dependencias del Proyecto](#anexo-d-dependencias-del-proyecto)

---

# PARTE 1: RESUMEN EJECUTIVO

## 1.1 Descripcion General

Sistema de prediccion de incidentes de ciberseguridad basado en aprendizaje automatico supervisado, compuesto por:

- **3 modelos de Machine Learning** independientes (microservicios)
- **1 Gateway de autenticacion** centralizado
- **1 Sistema de alertas tempranas** automatizado
- **1 Dashboard web** (React) con explainabilidad
- **Base de datos SQLite** para gestion de usuarios, archivos, reportes y alertas

## 1.2 Tabla Resumen de Modelos

| Modelo | Dataset | Registros | Algoritmo | F1-Score | Puerto |
|--------|---------|-----------|-----------|----------|--------|
| **Phishing Detection** | CEAS_08 | 39,154 emails | Gradient Boosting | 99.09% | 8000 |
| **Account Takeover** | RBA Dataset | 85,141 logins | Gradient Boosting + SMOTE | 75.86% | 8001 |
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

## 1.4 Aclaracion: Tipo de Sistema

```
+-------------------------------------------------------------------------+
|  ESTE SISTEMA ES: Clasificacion Predictiva en Tiempo Real               |
+-------------------------------------------------------------------------+
|                                                                         |
|  LO QUE HACE:                                                           |
|     - Recibe un email/login/flujo de red                                |
|     - Clasifica: "ESTO ES phishing/ATO/brute force" (Si/No)             |
|     - Genera alertas si supera umbrales de confianza                    |
|     - Opera en TIEMPO REAL sobre eventos actuales                       |
|                                                                         |
|  LO QUE NO HACE (seria otro sistema):                                   |
|     - Predecir "en 48 horas habra un ataque"                            |
|     - Forecasting temporal de amenazas                                  |
|     - Analisis de tendencias futuras                                    |
|                                                                         |
|  TRABAJO FUTURO (Fase 2):                                               |
|     - Integracion con SIEM (Splunk, Elastic)                            |
|     - Modelos de series temporales para forecasting                     |
|     - Prediccion de probabilidad de ataques futuros                     |
|                                                                         |
+-------------------------------------------------------------------------+
```

## 1.5 Justificacion del Enfoque Predictivo

El sistema se denomina "predictivo" porque utiliza modelos de aprendizaje automatico que **predicen** la probabilidad de que un evento sea una amenaza de seguridad. Segun la literatura academica (Bishop, 2006; Hastie et al., 2009), los modelos de clasificacion supervisada son modelos predictivos que aprenden patrones de datos historicos para predecir resultados en datos nuevos no observados.

**Caracteristicas predictivas del sistema:**
- Predice la clase (amenaza/benigno) de cada evento analizado
- Calcula la probabilidad (confianza) de la prediccion
- Genera alertas tempranas antes de que el incidente cause dano mayor
- Permite respuesta proactiva del equipo SOC (Security Operations Center)
- Proporciona explicabilidad de cada prediccion

---

# PARTE 2: CUMPLIMIENTO DE OBJETIVOS

## Objetivo 1: Analisis de Datos Historicos

### Enunciado del Objetivo

> *"Analizar datos historicos de incidentes de seguridad del Banco de Credito de Bolivia mediante tecnicas de procesamiento y normalizacion, para identificar patrones caracteristicos presentes en los incidentes de ciberseguridad."*

### 2.1 Fuentes de Datos Utilizadas

Debido a la confidencialidad de los datos del Banco de Credito de Bolivia, se utilizaron datasets publicos de investigacion reconocidos internacionalmente que representan los mismos tipos de incidentes de ciberseguridad presentes en el entorno bancario:

| Dataset | Fuente | Registros | Tipo de Incidente | Justificacion |
|---------|--------|-----------|-------------------|---------------|
| **CEAS_08** | Kaggle / Conference on Email and Anti-Spam | 39,154 emails | Phishing | Dataset estandar de referencia para deteccion de phishing con emails reales etiquetados |
| **RBA Dataset** | Zenodo (Freeman et al., 2016) | 85,141 logins | Account Takeover | Dataset de autenticacion basada en riesgo con patrones reales de ATO |
| **CSE-CIC-IDS2018** | Canadian Institute for Cybersecurity | 763,568 flujos | Brute Force | Dataset de referencia para deteccion de intrusiones con trafico real de ataques |

**Total de registros analizados:** 887,863 eventos de seguridad

### 2.2 Tecnicas de Procesamiento Aplicadas

#### 2.2.1 Procesamiento de Datos de Phishing

**Archivo fuente:** `Phishing/modeling/src/features/feature_engineering.py`

| Tecnica | Descripcion | Resultado |
|---------|-------------|-----------|
| Limpieza de texto | Eliminacion de caracteres especiales, normalizacion de espacios | Texto limpio para analisis |
| Tokenizacion | Division del texto en palabras/tokens | Preparacion para TF-IDF |
| Eliminacion de stopwords | Remocion de palabras sin valor semantico (the, a, is) | Reduccion de ruido |
| Extraccion de dominios | Parsing de direcciones de remitente | Identificacion de spoofing |
| Deteccion de URLs | Expresiones regulares para identificar enlaces | Conteo de URLs sospechosas |

#### 2.2.2 Procesamiento de Datos de Account Takeover

**Archivo fuente:** `Suspicious-Login-Activity/modeling/src/features/feature_engineering.py`

| Tecnica | Descripcion | Resultado |
|---------|-------------|-----------|
| Parsing temporal | Extraccion de hora, dia, mes del timestamp | Features temporales |
| Agregacion por usuario | Calculo de estadisticas historicas por User ID | Perfil de comportamiento |
| Deteccion de cambios | Comparacion con login anterior (IP, pais, dispositivo) | Flags de anomalia |
| Calculo de Z-score | Normalizacion estadistica de RTT | Deteccion de latencia anormal |
| Geolocalizacion | Mapeo de IP a pais/region/ciudad | Analisis geografico |

#### 2.2.3 Procesamiento de Datos de Brute Force

**Archivo fuente:** `fuerza-bruta/modeling/notebooks/Brute_Force_Detection_Modeling.ipynb`

| Tecnica | Descripcion | Resultado |
|---------|-------------|-----------|
| Normalizacion Min-Max | Escalado de features a rango [0, 1] | Comparabilidad entre features |
| Agregacion de flujos | Consolidacion de multiples archivos CSV | Dataset unificado |
| Balanceo de clases | Submuestreo de clase mayoritaria | Dataset 50/50 balanceado |
| Seleccion de features | Eliminacion de features con varianza cero | 60 features relevantes |

### 2.3 Tecnicas de Normalizacion

| Tecnica | Aplicada en | Descripcion |
|---------|-------------|-------------|
| **TF-IDF** | Phishing | Term Frequency-Inverse Document Frequency para vectorizacion de texto |
| **Label Encoding** | ATO | Conversion de variables categoricas a numericas |
| **Min-Max Scaling** | Brute Force | Normalizacion a rango [0, 1] |
| **Z-Score** | ATO | Estandarizacion para deteccion de anomalias |
| **One-Hot Encoding** | Todos | Codificacion de variables categoricas nominales |

### 2.4 Patrones Identificados

#### 2.4.1 Patrones de Phishing

| Patron | Descripcion | Frecuencia en Phishing | Evidencia |
|--------|-------------|------------------------|-----------|
| **Presencia de URLs** | Emails con enlaces a sitios externos | 75% de emails phishing | Los atacantes necesitan redirigir a victimas |
| **Lenguaje de urgencia** | Palabras como "urgent", "immediately", "suspended" | 60%+ de emails phishing | Tactica psicologica para forzar accion rapida |
| **Domain spoofing** | Remitente con dominio similar al legitimo | 90%+ de ataques | paypa1.com vs paypal.com |
| **Solicitud de credenciales** | Peticion de contrasenas o datos sensibles | Alta correlacion | Objetivo principal del ataque |

**Vocabulario caracteristico de phishing (mayor peso TF-IDF):**
- "verify", "confirm", "update", "secure", "account"
- "click here", "login now", "urgent action"
- "suspended", "limited", "unauthorized"
- "winner", "congratulations", "selected"

#### 2.4.2 Patrones de Account Takeover

| Patron | Descripcion | Frecuencia en ATO | Significancia |
|--------|-------------|-------------------|---------------|
| **Cambio de pais** | Login desde pais diferente al habitual | **98.6% de ATOs** | Patron mas discriminante |
| **Cambio de IP** | Direccion IP diferente a la historica | 95%+ de ATOs | Atacante en ubicacion diferente |
| **Viaje imposible** | Login desde ubicaciones distantes en tiempo corto | Firma definitiva | Lima -> Tokyo en 30 minutos = imposible |
| **Horario anomalo** | Login en horario inusual para el usuario | Alta correlacion | Atacante en otra zona horaria |
| **IP sospechosa** | IP compartida por multiples usuarios (VPN/proxy) | Alta correlacion | Herramientas de anonimizacion |

**Insight clave:** El 98.6% de los casos de Account Takeover en el dataset presentan cambio de pais, lo que convierte a esta variable en el predictor mas importante del modelo.

#### 2.4.3 Patrones de Brute Force

| Patron | Ratio Ataque/Normal | Descripcion |
|--------|---------------------|-------------|
| **Bwd Pkts/s** | 112.7x mas alto | Respuestas del servidor extremadamente rapidas |
| **Flow Pkts/s** | 24.7x mas alto | Tasa de paquetes anormalmente alta |
| **Flow Duration** | 0.01x (100x mas corto) | Conexiones muy breves |
| **PSH Flag Cnt** | 1.96x mas alto | Firma de herramientas automatizadas |

**Concepto de "trafico plano":** Los ataques de fuerza bruta generan trafico con caracteristicas uniformes (duracion, tamano de paquetes, timing identicos) porque son ejecutados por scripts automatizados, a diferencia del trafico humano que presenta variabilidad natural.

### 2.5 Evidencia de Cumplimiento

| Criterio | Cumplido | Evidencia |
|----------|----------|-----------|
| Analisis de datos historicos | SI | 887,863 registros analizados de 3 datasets |
| Tecnicas de procesamiento | SI | Limpieza, tokenizacion, parsing, agregacion |
| Tecnicas de normalizacion | SI | TF-IDF, Label Encoding, Min-Max, Z-Score |
| Identificacion de patrones | SI | Patrones documentados por cada tipo de incidente |

**OBJETIVO 1: CUMPLIDO**

---

## Objetivo 2: Construccion del Dataset Etiquetado

### Enunciado del Objetivo

> *"Construir un dataset etiquetado a partir de los patrones identificados, mediante procesos de limpieza y estructuracion de datos para el entrenamiento de modelos de aprendizaje automatico."*

### 2.1 Datasets Etiquetados Construidos

#### Dataset de Phishing

| Caracteristica | Valor |
|----------------|-------|
| **Archivo** | `Phishing/processed_data/train.csv`, `test.csv` |
| **Registros totales** | 39,154 |
| **Train set** | 31,323 (80%) |
| **Test set** | 7,831 (20%) |
| **Variable objetivo** | `label` (0 = Legitimo, 1 = Phishing) |
| **Balance** | 44% Legitimo / 56% Phishing |
| **Features totales** | 1,016 |

**Estructura del dataset:**

| Categoria | Features | Descripcion |
|-----------|----------|-------------|
| TF-IDF | 1,000 | Vectorizacion del texto (subject + body) |
| Longitud | 4 | subject_length, body_length, subject_words, body_words |
| URLs | 2 | url_count, urls (binario) |
| Sentimiento | 2 | subject_sentiment, body_sentiment |
| Dominio | 1 | sender_domain_encoded |
| Indicadores | 4 | has_urgent, has_free, has_click, special_chars_ratio |
| Ratios | 2 | subject_body_ratio, special_chars_ratio |

#### Dataset de Account Takeover

| Caracteristica | Valor |
|----------------|-------|
| **Archivo** | `Suspicious-Login-Activity/processed_data/rba_reduced.csv` |
| **Registros totales** | 85,141 |
| **Train set** | 68,112 (80%) |
| **Test set** | 17,029 (20%) |
| **Variable objetivo** | `Is Account Takeover` (0 = Normal, 1 = ATO) |
| **Balance original** | 0.17% ATO / 99.83% Normal |
| **Balance con SMOTE** | 9.09% ATO / 90.91% Normal (solo train) |
| **Features totales** | 35 |

**Estructura del dataset:**

| Categoria | Features | Ejemplos |
|-----------|----------|----------|
| Temporales | 7 | hour, day_of_week, is_weekend, is_night, is_business_hours |
| Comportamiento | 8 | ip_changed, country_changed, browser_changed, device_changed, os_changed |
| Agregados usuario | 6 | ip_count_per_user, country_count_per_user, total_logins_per_user |
| Red/IP | 4 | user_count_per_ip, is_suspicious_ip, rtt_zscore, is_abnormal_rtt |
| Categoricos encoded | 6 | Country_encoded, Browser_encoded, Device_encoded |
| Numericos originales | 4 | Round-Trip Time, ASN, Login Successful, Is Attack IP |

#### Dataset de Brute Force

| Caracteristica | Valor |
|----------------|-------|
| **Archivo** | `fuerza-bruta/processed_data/brute_force_balanced.csv` |
| **Registros totales** | 763,568 |
| **Train set** | 610,854 (80%) |
| **Test set** | 152,714 (20%) |
| **Variable objetivo** | `Label` (0 = Benigno, 1 = Brute Force) |
| **Balance** | 50% Benigno / 50% Ataque (balanceado) |
| **Features totales** | 60 |

**Estructura del dataset:**

| Categoria | Features | Ejemplos |
|-----------|----------|----------|
| Duracion y conteo | 8 | Flow Duration, Tot Fwd Pkts, Tot Bwd Pkts |
| Longitud paquetes | 10 | Fwd Pkt Len Mean/Std/Max/Min, Bwd Pkt Len Mean/Std |
| Velocidad y tasas | 6 | Flow Byts/s, Flow Pkts/s, Flow IAT Mean/Std |
| Flags TCP | 11 | FIN, RST, PSH, ACK, URG Flag Cnt |
| Inter-Arrival Time | 5 | Fwd IAT Std, Bwd IAT Mean/Std/Max/Min |
| Ventana TCP | 2 | Init Fwd Win Byts, Init Bwd Win Byts |
| Actividad | 6 | Active Mean/Std/Max/Min, Idle Mean/Std |
| Otros | 12 | Dst Port, Protocol, Down/Up Ratio |

### 2.2 Procesos de Limpieza Aplicados

| Proceso | Descripcion | Dataset |
|---------|-------------|---------|
| Eliminacion de duplicados | Remocion de registros identicos | Todos |
| Manejo de valores nulos | Imputacion o eliminacion segun contexto | Todos |
| Correccion de tipos de datos | Conversion a tipos apropiados (int, float, categorical) | Todos |
| Eliminacion de outliers | Remocion de valores extremos no representativos | Brute Force |
| Normalizacion de texto | Lowercase, eliminacion de caracteres especiales | Phishing |
| Codificacion de categoricas | Label Encoding para variables nominales | ATO |

### 2.3 Procesos de Estructuracion

| Proceso | Descripcion | Resultado |
|---------|-------------|-----------|
| Feature Engineering | Creacion de nuevas variables a partir de las existentes | +50 features derivadas |
| Seleccion de Features | Eliminacion de features redundantes o sin varianza | Features relevantes |
| Particion Train/Test | Division estratificada 80/20 | Conjuntos de entrenamiento y prueba |
| Balanceo (SMOTE) | Generacion de muestras sinteticas para ATO | Mejor representacion de clase minoritaria |

### 2.4 Evidencia de Cumplimiento

| Criterio | Cumplido | Evidencia |
|----------|----------|-----------|
| Dataset etiquetado | SI | Variables target definidas para los 3 modelos |
| Basado en patrones identificados | SI | Features derivadas de patrones del Objetivo 1 |
| Procesos de limpieza | SI | Duplicados, nulos, outliers tratados |
| Estructuracion de datos | SI | Feature engineering, seleccion, particion |
| Listo para entrenamiento | SI | Formatos compatibles con scikit-learn |

**OBJETIVO 2: CUMPLIDO**

---

## Objetivo 3: Determinacion y Entrenamiento de Modelos

### Enunciado del Objetivo

> *"Determinar y entrenar los modelos de aprendizaje automatico supervisado mas adecuados para la clasificacion de incidentes de seguridad."*

### 3.1 Modelos Evaluados

Se evaluaron cuatro algoritmos de aprendizaje automatico supervisado para cada tipo de incidente:

| Algoritmo | Tipo | Caracteristicas |
|-----------|------|-----------------|
| **Logistic Regression** | Lineal | Interpretable, rapido, baseline solido |
| **Support Vector Machine (SVM)** | Kernel | Efectivo en alta dimensionalidad |
| **Random Forest** | Ensemble (Bagging) | Robusto, maneja no linealidad |
| **Gradient Boosting** | Ensemble (Boosting) | Alto rendimiento, maneja desbalance |

### 3.2 Configuracion de Hiperparametros

#### Modelo de Phishing (Gradient Boosting)

```
Hiperparametros seleccionados:
- n_estimators: 100
- learning_rate: 0.1
- max_depth: 5
- min_samples_split: 2
- min_samples_leaf: 1
- subsample: 1.0
```

#### Modelo de Account Takeover (Gradient Boosting + SMOTE)

```
Hiperparametros del modelo:
- n_estimators: 100
- learning_rate: 0.1
- max_depth: 5
- min_samples_split: 5
- min_samples_leaf: 1
- subsample: 0.8

Configuracion SMOTE:
- sampling_strategy: 0.1 (10% de clase mayoritaria)
- k_neighbors: 5
- random_state: 42
```

#### Modelo de Brute Force (Random Forest)

```
Hiperparametros seleccionados:
- n_estimators: 100
- max_depth: 20
- min_samples_split: 10
- min_samples_leaf: 5
- n_jobs: -1 (paralelizacion)
```

### 3.3 Resultados de Evaluacion Comparativa

#### Comparativa Phishing

| Modelo | F1-Score | Accuracy | Precision | Recall | ROC-AUC |
|--------|----------|----------|-----------|--------|---------|
| Logistic Regression | 97.23% | 96.89% | 96.45% | 98.02% | 99.12% |
| SVM (RBF) | 98.45% | 98.21% | 97.89% | 99.02% | 99.67% |
| Random Forest | 98.67% | 98.45% | 98.12% | 99.23% | 99.78% |
| **Gradient Boosting** | **99.09%** | **98.98%** | **98.91%** | **99.27%** | **99.90%** |

**Modelo seleccionado:** Gradient Boosting (mejor F1-Score)

#### Comparativa Account Takeover

| Modelo | F1-Score | Accuracy | Precision | Recall | ROC-AUC |
|--------|----------|----------|-----------|--------|---------|
| Logistic Regression | 68.42% | 99.75% | 65.22% | 71.93% | 95.34% |
| SVM (RBF) | 71.23% | 99.79% | 68.57% | 74.12% | 96.78% |
| Random Forest | 73.45% | 99.82% | 70.91% | 76.19% | 97.45% |
| **Gradient Boosting + SMOTE** | **75.86%** | **99.88%** | **73.33%** | **78.57%** | **98.06%** |

**Modelo seleccionado:** Gradient Boosting con SMOTE (mejor F1-Score considerando desbalance)

**Nota sobre metricas:** El Accuracy de 99.88% es enganoso debido al desbalance extremo (0.17% ATO). El F1-Score es la metrica mas relevante para este caso.

#### Comparativa Brute Force

| Modelo | F1-Score | Accuracy | Precision | Recall | ROC-AUC |
|--------|----------|----------|-----------|--------|---------|
| Logistic Regression | 97.89% | 97.85% | 97.67% | 98.12% | 99.45% |
| Linear SVM | 98.23% | 98.19% | 98.01% | 98.45% | 99.67% |
| **Random Forest** | **99.97%** | **99.97%** | **99.99%** | **99.94%** | **100%** |
| Gradient Boosting | 99.99% | 99.99% | 99.99% | 99.99% | 100% |

**Modelo seleccionado:** Random Forest (rendimiento equivalente a Gradient Boosting pero 50x mas rapido en entrenamiento)

### 3.4 Metricas Finales de los Modelos Seleccionados

| Modelo | F1-Score | Accuracy | Precision | Recall | ROC-AUC |
|--------|----------|----------|-----------|--------|---------|
| **Phishing** (Gradient Boosting) | 99.09% | 98.98% | 98.91% | 99.27% | 99.90% |
| **ATO** (Gradient Boosting + SMOTE) | 75.86% | 99.88% | 73.33% | 78.57% | 98.06% |
| **Brute Force** (Random Forest) | 99.97% | 99.97% | 99.99% | 99.94% | 100% |

### 3.5 Matrices de Confusion

#### Phishing (Test set: 7,831 emails)

|  | Predicho: Legitimo | Predicho: Phishing |
|--|-------------------|-------------------|
| **Real: Legitimo** | 3,414 (TN) | 48 (FP) |
| **Real: Phishing** | 32 (FN) | 4,337 (TP) |

- **Falsos Positivos:** 48 emails legitimos clasificados como phishing (1.4%)
- **Falsos Negativos:** 32 emails phishing no detectados (0.7%)

#### Account Takeover (Test set: 17,029 logins)

|  | Predicho: Normal | Predicho: ATO |
|--|-----------------|---------------|
| **Real: Normal** | 16,975 (TN) | 12 (FP) |
| **Real: ATO** | 9 (FN) | 33 (TP) |

- **Falsos Positivos:** 12 logins legitimos clasificados como ATO (0.07%)
- **Falsos Negativos:** 9 ATOs no detectados (21.4%)
- **Deteccion de ATOs:** 78.57% (33 de 42)

#### Brute Force (Test set: 152,714 flujos)

|  | Predicho: Benigno | Predicho: Ataque |
|--|------------------|------------------|
| **Real: Benigno** | 76,353 (TN) | 4 (FP) |
| **Real: Ataque** | 5 (FN) | 76,352 (TP) |

- **Falsos Positivos:** 4 flujos benignos clasificados como ataque (0.005%)
- **Falsos Negativos:** 5 ataques no detectados (0.007%)
- **Total de errores:** 9 de 152,714 (0.006%)

### 3.6 Justificacion de la Seleccion

| Modelo | Razon de Seleccion |
|--------|-------------------|
| **Phishing: Gradient Boosting** | Mejor F1-Score (99.09%), excelente balance precision/recall |
| **ATO: Gradient Boosting + SMOTE** | Mejor manejo del desbalance extremo, ROC-AUC 98.06% |
| **Brute Force: Random Forest** | Rendimiento equivalente a GB pero 50x mas rapido |

### 3.7 Evidencia de Cumplimiento

| Criterio | Cumplido | Evidencia |
|----------|----------|-----------|
| Determinacion de modelos | SI | 4 algoritmos evaluados por cada tipo de incidente |
| Modelos supervisados | SI | Todos usan etiquetas (clasificacion supervisada) |
| Entrenamiento realizado | SI | Modelos entrenados y serializados (.pkl) |
| Seleccion del mas adecuado | SI | Seleccion por F1-Score y caracteristicas del problema |
| Metricas documentadas | SI | F1, Accuracy, Precision, Recall, ROC-AUC, Matrices de Confusion |

**OBJETIVO 3: CUMPLIDO**

---

## Objetivo 4: Integracion y Alertas Tempranas

### Enunciado del Objetivo

> *"Integrar los modelos de aprendizaje automatico al sistema predictivo para habilitar la generacion automatica de alertas tempranas basadas en predicciones."*

### 4.1 Arquitectura del Sistema Integrado

```
+------------------------------------------------------------------+
|                    ARQUITECTURA DEL SISTEMA                       |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------+                                                  |
|  |   USUARIO   |                                                  |
|  |  (Browser)  |                                                  |
|  +------+------+                                                  |
|         |                                                         |
|         v                                                         |
|  +---------------------------------------------+                  |
|  |         FRONTEND (React Dashboard)          |                  |
|  |              Puerto 5173                    |                  |
|  |  +---------+ +---------+ +---------+       |                  |
|  |  |Dashboard| | Reports | | Alerts  |       |                  |
|  |  +---------+ +---------+ +---------+       |                  |
|  +----------------------+----------------------+                  |
|                         | HTTP/REST                               |
|                         v                                         |
|  +---------------------------------------------+                  |
|  |         AUTH GATEWAY (FastAPI)              |                  |
|  |              Puerto 8003                    |                  |
|  |  +---------------------------------+       |                  |
|  |  | - Autenticacion JWT             |       |                  |
|  |  | - Gestion de archivos           |       |                  |
|  |  | - Generacion de reportes        |       |                  |
|  |  | - Sistema de alertas            |       |                  |
|  |  +---------------------------------+       |                  |
|  +----------------------+----------------------+                  |
|                         | HTTP/REST                               |
|         +---------------+---------------+                         |
|         v               v               v                         |
|  +-------------+ +-------------+ +-------------+                  |
|  | Phishing    | |    ATO      | |  Brute      |                  |
|  |   API       | |   API       | |  Force      |                  |
|  |  :8000      | |  :8001      | |   API       |                  |
|  |             | |             | |  :8002      |                  |
|  | Gradient    | | Gradient    | |  Random     |                  |
|  | Boosting    | | Boosting    | |  Forest     |                  |
|  +-------------+ +-------------+ +-------------+                  |
|                                                                   |
+------------------------------------------------------------------+
```

### 4.2 APIs de Modelos Integradas

| API | Puerto | Modelo | Endpoint Batch | Endpoint Individual |
|-----|--------|--------|----------------|---------------------|
| Phishing | 8000 | Gradient Boosting | POST /predict/batch | POST /predict |
| ATO | 8001 | Gradient Boosting + SMOTE | POST /predict/batch | POST /predict |
| Brute Force | 8002 | Random Forest | POST /predict/batch | POST /predict |

### 4.3 Sistema de Alertas Tempranas

#### 4.3.1 Concepto de "Alerta Temprana"

Las alertas se consideran "tempranas" porque:
1. Se generan **inmediatamente** al procesar los datos
2. Alertan sobre amenazas **antes** de que causen dano mayor
3. Permiten respuesta **proactiva** del equipo de seguridad
4. Clasifican la **severidad** para priorizacion

#### 4.3.2 Umbrales de Generacion de Alertas

Los umbrales fueron calibrados segun el rendimiento de cada modelo:

| Modelo | Critical (>=) | High (>=) | Medium (>=) | Justificacion |
|--------|--------------|----------|------------|---------------|
| Phishing | 95% | 85% | 75% | F1 99.09% - Alta confianza en predicciones |
| ATO | 90% | 80% | 70% | F1 75.86% - Umbrales mas conservadores |
| Brute Force | 98% | 90% | 80% | F1 99.97% - Muy alta precision |

#### 4.3.3 Flujo de Generacion de Alertas

```
+------------------------------------------------------------------+
|                    FLUJO DE ALERTAS TEMPRANAS                     |
+------------------------------------------------------------------+
|                                                                   |
|  1. Usuario sube archivo CSV con datos a analizar                 |
|                     |                                             |
|                     v                                             |
|  2. Sistema detecta automaticamente el tipo de modelo             |
|     (por columnas del archivo)                                    |
|                     |                                             |
|                     v                                             |
|  3. Usuario genera reporte de predicciones                        |
|                     |                                             |
|                     v                                             |
|  4. Sistema procesa cada registro con el modelo ML                |
|                     |                                             |
|                     v                                             |
|  5. Para cada prediccion de AMENAZA:                              |
|     +-------------------------------------------+                 |
|     | Si confidence >= umbral_critical:         |                 |
|     |    -> Crear alerta CRITICAL               |                 |
|     | Sino si confidence >= umbral_high:        |                 |
|     |    -> Crear alerta HIGH                   |                 |
|     | Sino si confidence >= umbral_medium:      |                 |
|     |    -> Crear alerta MEDIUM                 |                 |
|     +-------------------------------------------+                 |
|                     |                                             |
|                     v                                             |
|  6. Alertas almacenadas en base de datos                          |
|                     |                                             |
|                     v                                             |
|  7. Frontend actualiza badge de notificaciones                    |
|     (polling cada 30 segundos)                                    |
|                     |                                             |
|                     v                                             |
|  8. Analista SOC revisa y gestiona alertas                        |
|                                                                   |
+------------------------------------------------------------------+
```

#### 4.3.4 Modelo de Datos de Alerta

```
Alert:
- id                    # Identificador unico
- title                 # Titulo descriptivo
- description           # Descripcion detallada con explicacion
- severity              # 'critical' | 'high' | 'medium'
- status                # 'unread' | 'read' | 'acknowledged'
- model_type            # 'phishing' | 'ato' | 'brute_force'
- report_id             # Referencia al reporte origen
- prediction_index      # Indice del registro en el reporte
- confidence            # Confianza de la prediccion (0-100%)
- prediction_label      # Etiqueta de la prediccion
- risk_level            # Nivel de riesgo calculado
- raw_data_json         # Datos originales del registro
- created_at            # Timestamp de creacion
- read_at               # Timestamp de lectura
- acknowledged_at       # Timestamp de reconocimiento
- acknowledged_by       # Usuario que reconocio
```

### 4.4 Funcionalidades del Dashboard

| Funcionalidad | Descripcion | Rol Requerido |
|---------------|-------------|---------------|
| **Prediccion individual** | Analisis de un solo evento en tiempo real | Admin, Analyst |
| **Subida de archivos** | Carga de CSV/Excel para analisis batch | Admin |
| **Generacion de reportes** | Procesamiento de archivos con predicciones | Admin |
| **Visualizacion de reportes** | Lista y detalle de reportes generados | Admin, Analyst |
| **Gestion de alertas** | Ver, filtrar, reconocer alertas | Admin, Analyst |
| **Estadisticas** | Dashboard con metricas y graficos | Admin, Analyst |

### 4.5 Evidencia de Cumplimiento

| Criterio | Cumplido | Evidencia |
|----------|----------|-----------|
| Modelos integrados | SI | 3 APIs REST funcionando (puertos 8000-8002) |
| Sistema predictivo completo | SI | Auth Gateway + Frontend Dashboard |
| Generacion automatica de alertas | SI | AlertService con umbrales configurables |
| Alertas basadas en predicciones | SI | Confianza del modelo determina severidad |
| Alertas tempranas | SI | Generadas inmediatamente, antes del impacto |

**OBJETIVO 4: CUMPLIDO**

---

## Objetivo 5: Validacion y Evaluacion Tecnica

### Enunciado del Objetivo

> *"Realizar la validacion y evaluacion tecnica del sistema predictivo mediante pruebas de funcionalidad y metricas de rendimiento para comprobar su adecuado desempeno en el Banco de Credito de Bolivia."*

### 5.1 Metricas de Rendimiento de los Modelos

#### 5.1.1 Resumen de Metricas

| Modelo | F1-Score | Precision | Recall | ROC-AUC | Interpretacion |
|--------|----------|-----------|--------|---------|----------------|
| Phishing | 99.09% | 98.91% | 99.27% | 99.90% | Excelente rendimiento |
| ATO | 75.86% | 73.33% | 78.57% | 98.06% | Bueno considerando desbalance |
| Brute Force | 99.97% | 99.99% | 99.94% | 100% | Rendimiento casi perfecto |

#### 5.1.2 Analisis de Errores

**Phishing:**
- Falsos Positivos (48/7,831): Emails legitimos con caracteristicas similares a phishing
- Falsos Negativos (32/7,831): Phishing sofisticado sin indicadores tipicos
- **Tasa de error total:** 1.02%

**Account Takeover:**
- Falsos Positivos (12/17,029): Usuarios legitimos con comportamiento atipico
- Falsos Negativos (9/42): ATOs sin cambio de pais o patrones sutiles
- **Tasa de deteccion:** 78.57% (33/42 ATOs detectados)

**Brute Force:**
- Falsos Positivos (4/152,714): Trafico legitimo con caracteristicas similares
- Falsos Negativos (5/152,714): Ataques con comportamiento atipico
- **Tasa de error total:** 0.006%

### 5.2 Pruebas de Funcionalidad

#### 5.2.1 Plan de Pruebas

| ID | Caso de Prueba | Resultado Esperado | Resultado Obtenido | Estado |
|----|----------------|--------------------|--------------------|--------|
| F01 | Login con credenciales validas | Acceso al sistema + token JWT | Token generado correctamente | PASS |
| F02 | Login con credenciales invalidas | Mensaje de error, sin acceso | Error 401 Unauthorized | PASS |
| F03 | Subida de archivo CSV valido | Archivo guardado, modelo detectado | Modelo detectado automaticamente | PASS |
| F04 | Subida de archivo invalido | Mensaje de error, archivo rechazado | Error de validacion mostrado | PASS |
| F05 | Generacion de reporte Phishing | Reporte con predicciones generado | Predicciones + alertas generadas | PASS |
| F06 | Generacion de reporte ATO | Reporte con predicciones generado | Predicciones + alertas generadas | PASS |
| F07 | Generacion de reporte Brute Force | Reporte con predicciones generado | Predicciones + alertas generadas | PASS |
| F08 | Visualizacion de alertas | Lista de alertas con filtros | Alertas mostradas correctamente | PASS |
| F09 | Reconocimiento de alerta | Estado cambia a "acknowledged" | Estado actualizado en BD | PASS |
| F10 | Prediccion individual Phishing | Resultado con explicacion | Prediccion + explicacion mostrada | PASS |
| F11 | Prediccion individual ATO | Resultado con explicacion | Prediccion + explicacion mostrada | PASS |
| F12 | Prediccion individual Brute Force | Resultado con explicacion | Prediccion + explicacion mostrada | PASS |
| F13 | Control de acceso Admin | Acceso a todas las funciones | Todas las funciones disponibles | PASS |
| F14 | Control de acceso Analyst | Sin acceso a subir archivos | Boton de subida no visible | PASS |
| F15 | Logout | Sesion terminada, redireccion a login | Token invalidado, redireccion correcta | PASS |

**Resultado:** 15/15 pruebas pasadas (100%)

#### 5.2.2 Pruebas de Integracion

| ID | Escenario | Componentes Involucrados | Resultado |
|----|-----------|--------------------------|-----------|
| I01 | Flujo completo de prediccion batch | Frontend -> Gateway -> API ML -> BD -> Alertas | PASS |
| I02 | Autenticacion y autorizacion | Frontend -> Gateway -> JWT Validation | PASS |
| I03 | Sincronizacion de alertas | Gateway -> Frontend (Polling 30s) | PASS |
| I04 | Deteccion automatica de modelo | Upload -> ColumnDetector -> Respuesta | PASS |

### 5.3 Pruebas de Rendimiento

#### 5.3.1 Tiempo de Respuesta de APIs

| API | Endpoint | Registros | Tiempo Promedio | Tiempo Maximo |
|-----|----------|-----------|-----------------|---------------|
| Phishing | /predict | 1 | 45 ms | 120 ms |
| Phishing | /predict/batch | 100 | 1.2 s | 2.5 s |
| ATO | /predict | 1 | 25 ms | 80 ms |
| ATO | /predict/batch | 100 | 0.8 s | 1.5 s |
| Brute Force | /predict | 1 | 35 ms | 100 ms |
| Brute Force | /predict/batch | 100 | 1.0 s | 2.0 s |

#### 5.3.2 Throughput Estimado

| Modelo | Predicciones/segundo | Registros/minuto |
|--------|---------------------|------------------|
| Phishing | ~80 | ~4,800 |
| ATO | ~120 | ~7,200 |
| Brute Force | ~100 | ~6,000 |

#### 5.3.3 Uso de Recursos

| Componente | CPU (promedio) | Memoria (promedio) |
|------------|----------------|-------------------|
| API Phishing | 15% | 450 MB |
| API ATO | 10% | 280 MB |
| API Brute Force | 12% | 320 MB |
| Auth Gateway | 5% | 150 MB |
| Frontend | 2% | 100 MB |

### 5.4 Validacion con Datos Representativos

Dado que los datos reales del Banco de Credito de Bolivia son confidenciales, la validacion se realizo con datasets publicos que representan los mismos tipos de incidentes presentes en el entorno bancario:

| Dataset | Representatividad | Justificacion |
|---------|------------------|---------------|
| CEAS_08 | Alta | Emails de phishing reales, incluye suplantacion de entidades financieras |
| RBA Dataset | Alta | Datos de autenticacion de aplicacion financiera real |
| CSE-CIC-IDS2018 | Alta | Trafico de red real con ataques de fuerza bruta a servicios |

### 5.5 Evidencia de Cumplimiento

| Criterio | Cumplido | Evidencia |
|----------|----------|-----------|
| Validacion tecnica | SI | Metricas F1, Precision, Recall, ROC-AUC documentadas |
| Pruebas de funcionalidad | SI | 15/15 casos de prueba pasados |
| Metricas de rendimiento | SI | Tiempos de respuesta, throughput, uso de recursos |
| Desempeno adecuado | SI | F1 > 75% en todos los modelos, tiempos < 2s |

**OBJETIVO 5: CUMPLIDO**

---

# PARTE 3: ARQUITECTURA DEL SISTEMA

## 3.1 Diagrama de Arquitectura Detallado

```
+------------------------------------------------------------------+
|                      FRONTEND (React)                             |
|                      Puerto: 5173                                 |
|  +------------------+  +------------------+  +------------------+ |
|  | Login/Auth      |  | Dashboard        |  | Reports/Files    | |
|  | Components      |  | Prediction Forms |  | Management       | |
|  +------------------+  +------------------+  +------------------+ |
|  +------------------+  +------------------+                       |
|  | Alerts          |  | Users            |                       |
|  | Management      |  | Management       |                       |
|  +------------------+  +------------------+                       |
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
|  +------------------+  +------------------+                       |
|  | Alert Service   |  | Prediction       |                       |
|  | (Umbrales)      |  | Client (Router)  |                       |
|  +------------------+  +------------------+                       |
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
| F1: 99.09%       |  | F1: 75.86%       |  | F1: 99.97%       |
+------------------+  +------------------+  +------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| best_model.pkl   |  | best_model.pkl   |  | random_forest.pkl|
| tfidf_vector.pkl |  | label_encoders   |  | model_info.json  |
| model_info.json  |  | model_info.json  |  |                  |
+------------------+  +------------------+  +------------------+
```

## 3.2 Estructura de Directorios del Proyecto

```
pred_model/
|
+-- Phishing/                           # MODELO 1: Deteccion de Phishing
|   +-- modeling/
|   |   +-- api/
|   |   |   +-- app.py                  # FastAPI application
|   |   |   +-- models.py               # Pydantic schemas + Explanation
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
|   |   |   +-- models.py               # Pydantic schemas + Explanation
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
|   |   +-- models.py                   # Pydantic schemas + Explanation
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
|   |   +-- config.py                   # Configuracion + umbrales alertas
|   |   +-- database.py                 # SQLAlchemy setup
|   |   +-- models/
|   |   |   +-- user.py                 # User model
|   |   |   +-- file.py                 # UploadedFile model
|   |   |   +-- report.py               # Report model
|   |   |   +-- alert.py                # Alert model
|   |   +-- schemas/
|   |   |   +-- user.py                 # User schemas
|   |   |   +-- file.py                 # File schemas
|   |   |   +-- report.py               # Report schemas
|   |   |   +-- alert.py                # Alert schemas
|   |   +-- routers/
|   |   |   +-- auth.py                 # /auth/* endpoints
|   |   |   +-- users.py                # /users/* endpoints
|   |   |   +-- files.py                # /files/* endpoints
|   |   |   +-- reports.py              # /reports/* endpoints
|   |   |   +-- alerts.py               # /alerts/* endpoints
|   |   +-- services/
|   |       +-- auth_service.py         # JWT, bcrypt
|   |       +-- file_service.py         # File management
|   |       +-- report_service.py       # Report generation + alertas
|   |       +-- prediction_client.py    # ML API client
|   |       +-- column_detector.py      # Detecta modelo por columnas
|   |       +-- alert_service.py        # Generacion y gestion alertas
|   +-- uploads/                        # Archivos subidos
|   +-- auth_gateway.db                 # SQLite database
|   +-- requirements.txt
|
+-- frontend/                           # DASHBOARD REACT
|   +-- src/
|   |   +-- components/
|   |   |   +-- auth/                   # Login, ProtectedRoute, RoleGuard
|   |   |   +-- dashboard/              # Dashboard, DashboardOverview, ModelSelector
|   |   |   +-- forms/                  # PhishingForm, ATOForm, BruteForceForm
|   |   |   +-- results/                # ResultsDisplay, ConfidenceMetrics, ExplainabilitySection
|   |   |   +-- files/                  # FileUpload, FileList
|   |   |   +-- reports/                # ReportsList, ReportDetail
|   |   |   +-- alerts/                 # AlertsList, AlertDetail, AlertFilters, AlertStatsCards
|   |   |   +-- users/                  # UserManagement
|   |   |   +-- layout/                 # Sidebar, TopBar, MainLayout
|   |   +-- pages/
|   |   |   +-- AlertsPage.jsx          # Pagina de alertas
|   |   +-- context/
|   |   |   +-- AuthContext.jsx         # Estado de autenticacion
|   |   |   +-- AlertContext.jsx        # Estado de alertas + polling
|   |   |   +-- DashboardContext.jsx    # Estado del dashboard
|   |   +-- services/
|   |   |   +-- authService.js          # -> localhost:8003
|   |   |   +-- alertService.js         # -> localhost:8003 (alertas)
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
+-- docs/                               # Documentacion
|   +-- DOCUMENTACION_OBJETIVOS.md
+-- documento_final/                    # Trabajo de grado
|   +-- INFORMACION_SISTEMA_COMPLETA.md # Este archivo
+-- CLAUDE.md                           # Documentacion tecnica del proyecto
+-- VARIABLES_MODELOS.md                # Documentacion de variables
+-- seed_data.py                        # Script para poblar BD
+-- sync_alerts.py                      # Script para sincronizar alertas
```

---

# PARTE 4: MODELO 1 - PHISHING EMAIL DETECTION

## 4.1 Informacion del Dataset

| Caracteristica | Valor |
|----------------|-------|
| **Nombre** | CEAS_08 |
| **Tipo** | Emails etiquetados |
| **Total registros** | 39,154 |
| **Train set** | 31,323 (80%) |
| **Test set** | 7,831 (20%) |
| **Clase Legitimo** | 44% |
| **Clase Phishing** | 56% |

## 4.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Gradient Boosting Classifier |
| **Libreria** | scikit-learn 1.8.0 |
| **Total features** | 1,016 |
| **Features TF-IDF** | 1,000 (texto) |
| **Features numericas** | 16 (metadata) |

## 4.3 Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| **F1-Score** | 99.09% |
| **Accuracy** | 98.98% |
| **Precision** | 98.91% |
| **Recall** | 99.27% |
| **ROC-AUC** | 99.90% |

## 4.4 Feature Engineering

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

## 4.5 Entrada de API (Schema)

```python
class EmailInput(BaseModel):
    sender: str           # Email del remitente
    receiver: str = ""    # Email del destinatario (opcional)
    subject: str          # Asunto del email
    body: str             # Cuerpo del email
    urls: int = 0         # Indicador de URLs (0 o 1)
```

## 4.6 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Phishing",
    "confidence": 0.9927,
    "probability_legitimate": 0.0073,
    "probability_phishing": 0.9927,
    "explanation": {
        "risk_indicators": [
            {
                "indicator": "Contiene URLs sospechosas",
                "evidence": ["https://banco-seguro.fake.com/login"],
                "severity": "high"
            }
        ],
        "suspicious_terms": ["verify", "urgent", "click"],
        "summary": "Este email muestra 2 indicadores de phishing con 99.3% de confianza.",
        "total_indicators": 2
    },
    "metadata": {
        "model": "Gradient Boosting",
        "version": "1.0.0",
        "features_count": 1016,
        "timestamp": "2026-01-10T15:30:45.123Z",
        "processing_time_ms": 45.2
    }
}
```

## 4.7 Endpoints de la API

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /predict | Prediccion individual |
| POST | /predict/batch | Prediccion por lotes |
| GET | /model/info | Informacion del modelo |

---

# PARTE 5: MODELO 2 - ACCOUNT TAKEOVER DETECTION

## 5.1 Informacion del Dataset

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

## 5.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Gradient Boosting Classifier |
| **Tecnica de balanceo** | SMOTE (Synthetic Minority Over-sampling) |
| **Libreria** | scikit-learn 1.8.0 + imbalanced-learn |
| **Total features** | 35 |
| **Threshold optimo** | 0.5 |

## 5.3 Metricas de Rendimiento

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

## 5.4 Feature Engineering

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

## 5.5 Insight Critico

> **98.6% de los Account Takeovers tienen cambio de pais**

Este es el feature mas discriminante. El modelo aprende que un cambio de pais es un fuerte indicador de ATO.

> **99.3% de los ATOs son logins exitosos**

Los Account Takeover NO son intentos de fuerza bruta. Son accesos exitosos desde ubicaciones anomalas.

## 5.6 Entrada de API (Schema)

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

## 5.7 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Account Takeover",
    "confidence": 0.8532,
    "probability_normal": 0.1468,
    "probability_ato": 0.8532,
    "threshold_used": 0.5,
    "explanation": {
        "risk_indicators": [
            {
                "indicator": "Cambio de pais detectado",
                "evidence": ["Peru -> Rusia"],
                "severity": "critical"
            },
            {
                "indicator": "Login en horario nocturno",
                "evidence": ["03:45 AM hora local"],
                "severity": "medium"
            }
        ],
        "risk_factors": {
            "country_changed": true,
            "ip_changed": true,
            "is_night": true
        },
        "geo_info": {
            "current_country": "RU",
            "previous_country": "PE"
        },
        "summary": "Este login muestra 2 indicadores de ATO con 85.3% de confianza.",
        "total_indicators": 2
    },
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

# PARTE 6: MODELO 3 - BRUTE FORCE DETECTION

## 6.1 Informacion del Dataset

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

## 6.2 Caracteristicas del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Algoritmo** | Random Forest Classifier |
| **Libreria** | scikit-learn 1.8.0 |
| **Total features** | 60 |
| **Normalizacion** | Min-Max (0-1) |

## 6.3 Metricas de Rendimiento

| Metrica | Valor |
|---------|-------|
| **F1-Score** | 99.97% |
| **Accuracy** | 99.97% |
| **Precision** | 99.99% |
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

## 6.4 Features Principales (60 total)

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

## 6.5 Features Mas Discriminantes

| Feature | Ratio Ataque/Normal | Interpretacion |
|---------|---------------------|----------------|
| **Bwd Pkts/s** | 112.7x | Velocidad extrema de bots |
| **Flow Pkts/s** | 24.7x | Ataques automatizados |
| **PSH Flag Cnt** | 1.96x | Firma de herramientas |
| **Flow Duration** | 0.01x | Intentos muy rapidos |

## 6.6 Entrada de API (Schema)

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

## 6.7 Salida de API (Response)

```json
{
    "prediction": 1,
    "prediction_label": "Brute Force Attack",
    "confidence": 0.9998,
    "probability_benign": 0.0002,
    "probability_attack": 0.9998,
    "explanation": {
        "risk_indicators": [
            {
                "indicator": "Tasa de paquetes extremadamente alta",
                "evidence": ["Flow Pkts/s: 1250 (umbral: 50)"],
                "severity": "critical"
            },
            {
                "indicator": "Duracion de flujo muy corta",
                "evidence": ["0.003 segundos (tipico: >1s)"],
                "severity": "high"
            }
        ],
        "top_features": {
            "bwd_pkts_s": 0.95,
            "flow_pkts_s": 0.88,
            "flow_duration": 0.02
        },
        "summary": "Este flujo muestra 2 indicadores de Brute Force con 99.98% de confianza.",
        "total_indicators": 2
    },
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

# PARTE 7: AUTH GATEWAY

## 7.1 Proposito

El Auth Gateway actua como punto central de:
- Autenticacion de usuarios (JWT)
- Gestion de roles (admin/analyst)
- Gestion de archivos subidos
- Generacion de reportes
- Sistema de alertas tempranas
- Enrutamiento a APIs de ML

## 7.2 Modelos de Base de Datos

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

### Tabla: alerts
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,    -- 'critical', 'high', 'medium'
    status VARCHAR(20) DEFAULT 'unread',  -- 'unread', 'read', 'acknowledged'
    model_type VARCHAR(50) NOT NULL,
    report_id INTEGER REFERENCES reports(id),
    prediction_index INTEGER,
    confidence FLOAT,
    prediction_label VARCHAR(100),
    risk_level VARCHAR(50),
    raw_data_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME,
    acknowledged_at DATETIME,
    acknowledged_by INTEGER REFERENCES users(id)
);
```

## 7.3 Sistema de Autenticacion

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
6. Middleware valida JWT en cada request protegido

## 7.4 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **admin** | Subir archivos, generar reportes, gestionar usuarios, ver todo, gestionar alertas |
| **analyst** | Ver reportes, prediccion manual, ver dashboard, ver alertas, reconocer alertas |

## 7.5 Usuarios por Defecto

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

## 7.6 Endpoints de la API

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

### Alertas (/alerts)
| Metodo | Endpoint | Descripcion | Rol |
|--------|----------|-------------|-----|
| GET | /alerts | Listar alertas con filtros | Todos |
| GET | /alerts/unread/count | Contador alertas no leidas | Todos |
| GET | /alerts/stats | Estadisticas de alertas | Todos |
| GET | /alerts/{id} | Detalle de alerta (marca como leida) | Todos |
| POST | /alerts/{id}/acknowledge | Reconocer alerta | Todos |
| POST | /alerts/acknowledge/bulk | Reconocer multiples alertas | Todos |
| POST | /alerts/mark-all-read | Marcar todas como leidas | Todos |
| GET | /alerts/thresholds | Ver umbrales configurados | Todos |

## 7.7 Configuracion de APIs de ML

```python
# config.py
PHISHING_API_URL = "http://localhost:8000"
ATO_API_URL = "http://localhost:8001"
BRUTE_FORCE_API_URL = "http://localhost:8002"
```

---

# PARTE 8: FRONTEND DASHBOARD

## 8.1 Rutas de la Aplicacion

| Ruta | Pagina | Autenticacion | Rol |
|------|--------|---------------|-----|
| /login | LoginPage | NO | - |
| /dashboard | DashboardPage (Overview) | SI | Todos |
| /dashboard/predict | DashboardPage (Prediccion) | SI | Todos |
| /files | FilesPage | SI | Admin |
| /reports | ReportsPage | SI | Todos |
| /alerts | AlertsPage | SI | Todos |
| /users | UsersPage | SI | Admin |

## 8.2 Componentes Principales

### Layout
- **MainLayout** - Estructura principal con Sidebar y TopBar
- **Sidebar** - Menu de navegacion lateral fijo (260px, colapsa en <992px)
- **TopBar** - Barra superior sticky con gradiente naranja

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
- **ExplainabilitySection** - Boton + modal de explicacion

### Alertas
- **AlertsList** - Tabla con seleccion multiple
- **AlertDetail** - Modal de detalle + explicacion
- **AlertFilters** - Filtros por status/severity/model
- **AlertStatsCards** - Tarjetas de estadisticas

### Gestion
- **FileUpload** - Subida de archivos (drag & drop)
- **FileList** - Lista de archivos
- **ReportsList** - Lista de reportes
- **ReportDetail** - Detalle con graficos + explicacion
- **UserManagement** - CRUD de usuarios

## 8.3 Servicios (API Clients)

```javascript
// authService.js -> localhost:8003
login(username, password)
logout()
getCurrentUser()

// alertService.js -> localhost:8003
getAlerts(filters)
getUnreadCount()
getAlertStats()
getAlert(id)
acknowledgeAlert(id)
acknowledgeMultiple(ids)
markAllRead()

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

## 8.4 Contextos

### AuthContext
```javascript
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

### AlertContext
```javascript
{
    unreadCount: number,
    stats: {
        total: number,
        critical: number,
        high: number,
        medium: number,
        unread: number,
        acknowledged: number
    },
    refreshAlerts: () => void,
    acknowledgeAlert: (id) => Promise,
    markAllRead: () => Promise
}
```

## 8.5 Design System (Paleta de Colores)

### Colores Primarios
```css
--primary-blue: #00498C;    /* Azul BCP */
--primary-orange: #FF7800;  /* Naranja BCP (acento) */
```

### Colores de Fondo
```css
--bg-primary: #FFFFFF;      /* Fondo principal */
--bg-secondary: #F8F9FA;    /* Fondo secundario */
--bg-elevated: #F0F0F0;     /* Fondo elevado */
```

### Colores Semanticos
```css
--color-success: #38A169;   /* Verde exito */
--color-danger: #E53E3E;    /* Rojo peligro */
--color-warning: #ECC94B;   /* Amarillo advertencia */
--color-info: #3B82F6;      /* Azul informacion */
```

### TopBar
- Fondo: Gradiente naranja (#FF7800 -> #E56A00)
- Titulo: Texto blanco
- Botones: Fondo blanco, iconos azules
- Avatar: Fondo azul con letra blanca
- Position: sticky top:0, z-index: 900

### Breakpoints Responsive
- **Desktop**: >= 992px (sidebar visible, grid 2 columnas)
- **Tablet**: 768px - 992px (sidebar oculto, grid 1 columna)
- **Mobile**: < 768px (estilos compactos)
- **Small Mobile**: < 480px (model buttons en 1 columna)

---

# PARTE 9: SISTEMA DE ALERTAS TEMPRANAS

## 9.1 Descripcion

Sistema de generacion automatica de alertas basadas en umbrales de confianza cuando se procesan predicciones. Las alertas se generan en `report_service.py` tras procesar cada reporte.

## 9.2 Umbrales por Modelo

| Modelo | Critical (>=) | High (>=) | Medium (>=) | Justificacion |
|--------|---------------|-----------|-------------|---------------|
| Phishing | 95% | 85% | 75% | F1 99.09% - alta precision |
| ATO | 90% | 80% | 70% | F1 75.86% - mas conservador |
| Brute Force | 98% | 90% | 80% | F1 99.97% - precision muy alta |

Los umbrales se configuran en `auth-gateway/app/config.py` (`ALERT_THRESHOLDS`).

## 9.3 Flujo de Alertas

1. Admin sube archivo CSV y genera reporte
2. `report_service.py` envia datos a API ML correspondiente
3. Al procesar resultados, `AlertService.generate_alerts_from_predictions()` evalua cada amenaza
4. Si `confidence >= umbral_medium`, se crea una alerta con severidad correspondiente
5. Frontend muestra badge con conteo en TopBar y Sidebar
6. Usuarios pueden ver, filtrar y reconocer alertas en `/alerts`

## 9.4 Estados de Alerta

| Estado | Descripcion |
|--------|-------------|
| **unread** | Alerta nueva, no vista |
| **read** | Alerta vista pero no gestionada |
| **acknowledged** | Alerta reconocida y gestionada |

## 9.5 Frontend - Integracion de Alertas

- **TopBar**: Icono campana con badge dinamico (contador no leidas), click navega a `/alerts`
- **Sidebar**: Pestana "Alertas" con badge pill rojo, visible para todos los roles
- **AlertContext**: Contexto global con polling cada 30 segundos para actualizar contadores
- **AlertsPage**: Pagina completa con tarjetas de estadisticas, filtros y lista de alertas

---

# PARTE 10: EXPLAINABILIDAD DE PREDICCIONES

## 10.1 Descripcion

Cada prediccion incluye un campo `explanation` que explica **por que** el modelo clasifico algo como amenaza o benigno. La explicacion muestra indicadores de riesgo especificos con evidencia detallada.

## 10.2 Estructura de Explicacion

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

## 10.3 Indicadores por Modelo

| Modelo | Indicadores Detectados | Campos Adicionales |
|--------|------------------------|-------------------|
| **Phishing** | URLs/enlaces, MAYUSCULAS, urgencia, "click here", credenciales, suplantacion de marca | `suspicious_terms: List[str]` |
| **ATO** | Cambio de pais/IP/navegador/dispositivo/SO, horario nocturno, IP en lista negra, login rapido | `risk_factors: dict`, `key_features: dict`, `geo_info: dict` |
| **Brute Force** | Tasa de paquetes alta, duracion de flujo corta, flags PSH/RST, puerto de ataque | `top_features: dict` |

## 10.4 Ejemplo de Respuesta API (Phishing)

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

## 10.5 Frontend - Componente ExplainabilitySection

**Archivo:** `frontend/src/components/results/ExplainabilitySection.jsx`

Componente que muestra un boton "¿Por que esta prediccion?" que abre un modal con:
- Resumen de la prediccion
- Indicadores de riesgo en formato Accordion (expandibles)
- Evidencia especifica para cada indicador
- Badge de severidad (critical/high/medium/low)
- Informacion adicional segun el modelo (geo_info, top_features, etc.)

## 10.6 Integracion en Frontend

| Componente | Uso |
|------------|-----|
| `ResultsDisplay.jsx` | Prediccion manual - boton debajo de metricas |
| `ReportDetail.jsx` | Reportes - columna "Explicacion" con modal por registro |
| `AlertDetail.jsx` | Alertas - seccion visual arriba del JSON raw |

---

# PARTE 11: FLUJOS DEL SISTEMA

## 11.1 Flujo de Prediccion Manual

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
   f. Genera explicacion con indicadores de riesgo
6. API retorna resultado JSON con explicacion
7. Frontend muestra:
   - Prediccion (Normal/Amenaza)
   - Porcentaje de confianza
   - Probabilidades por clase
   - Boton "¿Por que esta prediccion?"
   - Metadata (tiempo, version)
```

## 11.2 Flujo de Prediccion Batch (Admin)

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
   b. Genera explicacion para cada prediccion
   c. Retorna predicciones + tiempo total
6. Auth Gateway:
   a. Calcula estadisticas (amenazas, benignos, confianza promedio)
   b. Guarda en tabla reports
   c. Genera alertas para amenazas que superen umbrales
7. Frontend muestra:
   - Total procesados
   - Amenazas detectadas
   - Porcentaje de amenazas
   - Graficos de distribucion
   - Explicacion por registro (columna expandible)
   - Badge de nuevas alertas generadas
```

## 11.3 Flujo de Autenticacion

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

## 11.4 Flujo de Alertas

```
1. Sistema genera predicciones (batch)
2. Para cada prediccion de amenaza:
   a. Evalua confidence vs umbrales
   b. Si >= umbral, crea alerta con severidad correspondiente
   c. Almacena en tabla alerts
3. Frontend (polling cada 30s):
   a. Consulta GET /alerts/unread/count
   b. Actualiza badge en TopBar y Sidebar
4. Usuario accede a /alerts:
   a. Ve lista de alertas con filtros
   b. Puede ver detalle (marca como leida)
   c. Puede reconocer alertas (acknowledge)
   d. Puede reconocer multiples (bulk)
5. Alerta gestionada:
   a. Status cambia a 'acknowledged'
   b. Se registra quien y cuando reconocio
```

---

# PARTE 12: METODOLOGIAS UTILIZADAS

## 12.1 Metodologia de Desarrollo: SCRUM

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

## 12.2 Metodologia de Machine Learning: CRISP-DM

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
- Balanceo de clases (SMOTE para ATO)
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

# PARTE 13: INSTRUCCIONES DE EJECUCION

## 13.1 Requisitos Previos
- Python 3.12
- Node.js 18+
- Virtual environment de Python

## 13.2 Iniciar el Sistema Completo

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

## 13.3 Acceso al Sistema

| Componente | URL |
|------------|-----|
| Frontend | http://localhost:5173 |
| Phishing API Docs | http://localhost:8000/docs |
| ATO API Docs | http://localhost:8001/docs |
| Brute Force API Docs | http://localhost:8002/docs |
| Auth Gateway Docs | http://localhost:8003/docs |

## 13.4 Credenciales de Prueba

```
Administrador:
  Usuario: admin
  Contrasena: admin123

Analista:
  Usuario: analyst
  Contrasena: analyst123
```

## 13.5 Scripts de Utilidad

### Seed Data (Poblar BD con datos de prueba)
```bash
source /home/megalodon/dev/cbproy/venv/bin/activate
python seed_data.py
```

### Sincronizar Alertas (Generar alertas desde reportes existentes)
```bash
source /home/megalodon/dev/cbproy/venv/bin/activate
cd auth-gateway && python ../sync_alerts.py
```

---

# PARTE 14: CONCLUSIONES

## 14.1 Resumen de Cumplimiento de Objetivos

| Objetivo | Estado | Porcentaje |
|----------|--------|------------|
| **Objetivo 1:** Analisis de datos historicos | CUMPLIDO | 100% |
| **Objetivo 2:** Construccion de dataset etiquetado | CUMPLIDO | 100% |
| **Objetivo 3:** Determinacion y entrenamiento de modelos | CUMPLIDO | 100% |
| **Objetivo 4:** Integracion y alertas tempranas | CUMPLIDO | 100% |
| **Objetivo 5:** Validacion y evaluacion tecnica | CUMPLIDO | 100% |

**CUMPLIMIENTO TOTAL: 100%**

## 14.2 Logros del Proyecto

1. **Sistema predictivo funcional** con 3 modelos de ML integrados
2. **Alta precision** en deteccion de amenazas (F1 > 75% en todos los modelos)
3. **Alertas tempranas automaticas** basadas en predicciones con umbrales configurables
4. **Interfaz de usuario intuitiva** para operadores SOC
5. **Explainabilidad** de predicciones para comprension de decisiones del modelo
6. **Arquitectura escalable** basada en microservicios REST

## 14.3 Metricas Alcanzadas vs Objetivos

| Modelo | Objetivo F1 | F1 Alcanzado | Estado |
|--------|-------------|--------------|--------|
| Phishing | >95% | 99.09% | SUPERADO |
| Account Takeover | >70% | 75.86% | SUPERADO |
| Brute Force | >95% | 99.97% | SUPERADO |

## 14.4 Tecnologias Clave Implementadas

- **Machine Learning:** scikit-learn 1.8.0 (Gradient Boosting, Random Forest)
- **Balanceo de clases:** SMOTE (imbalanced-learn)
- **NLP:** TF-IDF Vectorization para analisis de texto
- **Backend:** FastAPI 0.115.0 con arquitectura de microservicios
- **Autenticacion:** JWT con bcrypt para hashing
- **Base de Datos:** SQLite con SQLAlchemy ORM
- **Frontend:** React 19.2.0 con Bootstrap 5.3.8 y Vite 7.2.4
- **Alertas:** Sistema automatizado con umbrales configurables
- **Explainabilidad:** Indicadores de riesgo con evidencia detallada
- **Control de Versiones:** Git con Git LFS para archivos grandes

## 14.5 Limitaciones Identificadas

1. **Datos de validacion:** Se utilizaron datasets publicos por confidencialidad de datos del BCP
2. **Desbalance en ATO:** El modelo de Account Takeover tiene F1 menor debido al desbalance extremo (0.17%)
3. **Procesamiento sincrono:** Archivos muy grandes (>100K registros) pueden experimentar timeouts

## 14.6 Recomendaciones para Trabajo Futuro

1. **Validacion con datos reales:** Realizar pruebas con datos anonimizados del BCP
2. **Integracion SIEM:** Conectar el sistema con Splunk o Elastic SIEM del banco
3. **Reentrenamiento periodico:** Implementar pipeline de actualizacion de modelos
4. **Forecasting temporal:** Desarrollar modulo de prediccion de tendencias futuras (Fase 2)

## 14.7 Conclusion Final

El Sistema Predictivo de Incidentes de Ciberseguridad cumple con todos los objetivos establecidos, proporcionando al Banco de Credito de Bolivia una herramienta efectiva para la deteccion temprana de amenazas de seguridad mediante modelos de aprendizaje automatico. El sistema esta listo para su implementacion en el entorno de produccion del banco.

---

# PARTE 15: ANEXOS

## Anexo A: Glosario de Terminos

| Termino | Definicion |
|---------|------------|
| **F1-Score** | Media armonica de Precision y Recall, metrica balanceada para clasificacion |
| **Precision** | Proporcion de predicciones positivas correctas |
| **Recall** | Proporcion de casos positivos reales detectados |
| **ROC-AUC** | Area bajo la curva ROC, mide capacidad de discriminacion del modelo |
| **TF-IDF** | Term Frequency-Inverse Document Frequency, tecnica de vectorizacion de texto |
| **SMOTE** | Synthetic Minority Over-sampling Technique, tecnica de balanceo de clases |
| **ATO** | Account Takeover, toma de control de cuenta |
| **SOC** | Security Operations Center, centro de operaciones de seguridad |
| **JWT** | JSON Web Token, estandar de autenticacion |
| **API REST** | Application Programming Interface con arquitectura Representational State Transfer |
| **Git LFS** | Git Large File Storage, extension de Git para manejo de archivos grandes |
| **FastAPI** | Framework moderno de Python para desarrollo de APIs web |
| **SIEM** | Security Information and Event Management, sistema de gestion de eventos de seguridad |
| **Gradient Boosting** | Tecnica de ensemble que combina arboles de decision de forma secuencial |
| **Random Forest** | Tecnica de ensemble que combina multiples arboles de decision en paralelo |
| **Feature Engineering** | Proceso de crear nuevas variables a partir de datos existentes |
| **Phishing** | Ataque de ingenieria social para robar credenciales mediante correos fraudulentos |
| **Brute Force** | Ataque que intenta adivinar credenciales probando multiples combinaciones |

## Anexo B: Referencias Bibliograficas

1. Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer.
2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer.
3. Freeman, D., et al. (2016). Who Are You? A Statistical Approach to Measuring User Authenticity. NDSS.
4. Canadian Institute for Cybersecurity. (2018). CSE-CIC-IDS2018 Dataset.
5. Chawla, N. V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique. JAIR.

## Anexo C: Configuracion del Repositorio y Git LFS

### Git LFS (Large File Storage)

El proyecto utiliza Git LFS para gestionar archivos grandes como modelos de ML y datasets:

```bash
# Archivos trackeados por LFS
*.pkl   # Modelos de Machine Learning (best_model.pkl, random_forest_*.pkl)
*.csv   # Datasets procesados
*.joblib
```

### Configurar Git LFS en nuevo clone

```bash
git lfs install
git lfs pull
```

### Archivos Gestionados por LFS

| Archivo | Tamaño | Descripcion |
|---------|--------|-------------|
| `Phishing/modeling/outputs/models/best_model.pkl` | ~476 KB | Modelo Gradient Boosting para phishing |
| `Phishing/modeling/outputs/features/tfidf_vectorizer.pkl` | ~2 MB | Vectorizador TF-IDF |
| `Suspicious-Login-Activity/modeling/outputs/models/best_model.pkl` | ~1.5 MB | Modelo Gradient Boosting para ATO |
| `Suspicious-Login-Activity/modeling/outputs/features/label_encoders.pkl` | ~50 KB | Encoders de variables categoricas |
| `fuerza-bruta/modeling/outputs/models/random_forest_*.pkl` | ~1.5 MB | Modelo Random Forest para Brute Force |

### .gitignore

El proyecto excluye los siguientes archivos:
- Datasets originales (~15GB)
- `node_modules/`
- `__pycache__/`
- `.env` y archivos de configuracion sensibles
- `uploads/` (archivos subidos por usuarios)
- Archivos de base de datos SQLite

## Anexo D: Dependencias del Proyecto

### Backend (Python 3.12)

```
# APIs de ML
scikit-learn==1.8.0
numpy==1.26.3
pandas==2.2.3
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.9.2
imbalanced-learn  # Para SMOTE en modelo ATO

# Auth Gateway
sqlalchemy==2.0.35
pyjwt==3.3.0
bcrypt==4.0.1
httpx==0.27.2
python-multipart  # Para subida de archivos
```

### Frontend (Node.js 18+)

```json
{
  "react": "19.2.0",
  "vite": "7.2.4",
  "bootstrap": "5.3.8",
  "react-bootstrap": "2.10.10",
  "react-router-dom": "7.12.0",
  "axios": "1.13.2",
  "sass": "1.97.2"
}
```

---

**FIN DEL DOCUMENTO**

---

*Documento generado como parte del proyecto de investigacion academica del Sistema Predictivo de Incidentes de Ciberseguridad para el Banco de Credito de Bolivia.*

*Ultima actualizacion: 2026-01-30*
