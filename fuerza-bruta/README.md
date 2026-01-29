# Brute Force Detection - CSE-CIC-IDS2018

## 📊 Dataset

**Fuente**: CSE-CIC-IDS2018 Dataset
**Tipo de ataque**: Brute Force (múltiples tipos consolidados)

### Archivos Originales Consolidados

Este modelo consolida **4 tipos diferentes de ataques de Brute Force** presentes en el dataset CSE-CIC-IDS2018:

| Archivo | Tipo de Ataque | Registros Ataque | Registros Benign |
|---------|----------------|------------------|------------------|
| 02-14-2018.csv | FTP-BruteForce | ~193,000 | ~663,000 |
| 02-14-2018.csv | SSH-Bruteforce | ~187,000 | ~663,000 |
| 02-22-2018.csv | Brute Force-Web | ~249 | ~1,042,000 |
| 02-22-2018.csv | Brute Force-XSS | ~79 | ~1,042,000 |
| 02-23-2018.csv | Brute Force-Web | ~362 | ~1,042,000 |
| 02-23-2018.csv | Brute Force-XSS | ~151 | ~1,042,000 |

**Total consolidado**: ~380,000 ataques Brute Force + ~2,700,000 Benign

### Dataset Preprocesado

**Archivo**: `processed_data/brute_force_balanced.csv`

- **Balance**: 50% Brute Force / 50% Benign
- **Registros totales**: ~760,000 (después de preprocessing)
- **Features**: ~64 (después de eliminar correlacionadas)
- **Tamaño**: ~100-150 MB
- **Listo para**: EDA y modelado

## 🔧 Pipeline de Preprocessing

El script `processed_data/preprocess_bruteforce_consolidated.py` implementa un pipeline de 9 pasos basado en el notebook de referencia `external_ref/preprocessing-cse-cic-ids2018.ipynb`:

### Paso 1: Cargar y Consolidar Datasets
- Carga los 3 archivos CSV (02-14, 02-22, 02-23)
- Consolida todos en un único DataFrame
- Mapea todas las variantes de Brute Force a clase única: **"Brute Force"**

### Paso 2: Eliminar Columnas String
- Elimina: `Flow ID`, `Src IP`, `Dst IP`
- Razón: No aportan información para ML, solo identificación

### Paso 3: Limpiar INF/-INF y NaN
- Reemplaza valores infinitos con NaN
- Elimina todas las filas con NaN

### Paso 4: Convertir Timestamp a Epoch
- Formato original: `dd/mm/yyyy HH:MM:SS`
- Conversión: Unix epoch (segundos desde 1970-01-01)
- Permite usar Timestamp como feature numérica

### Paso 5: Convertir Tipos de Datos
- Todas las columnas (excepto Label) → `float64`
- Strings inválidos → NaN → eliminados

### Paso 6: Filtrar Outliers (Z-score)
- Threshold: Z-score = 7 (~99.9999999% de datos)
- Filtrado independiente por clase (Brute Force y Benign)
- Preserva clases minoritarias

### Paso 7: Normalizar (MinMaxScaler)
- Rango: [0, 1]
- Todas las features numéricas
- Facilita convergencia de modelos

### Paso 8: Eliminar Features Correlacionadas
- Threshold: Correlación > 0.99
- Reduce multicolinealidad
- Mejora eficiencia del modelo
- Features eliminadas: ~16 (varía por dataset)

### Paso 9: Balancear Dataset
- Estrategia: Undersample de Benign
- Ratio final: 50% Brute Force / 50% Benign
- Random state: 42 (reproducible)
- Shuffle final para mezclar clases

## 📁 Estructura del Proyecto

```
fuerza-bruta/
├── dataset/                     # Datasets originales CSE-CIC-IDS2018
│   ├── 02-14-2018.csv          # FTP, SSH Brute Force
│   ├── 02-22-2018.csv          # Web, XSS Brute Force
│   └── 02-23-2018.csv          # Web, XSS Brute Force
│
├── processed_data/              # Datasets procesados
│   ├── preprocess_bruteforce_consolidated.py  # Script de preprocessing
│   └── brute_force_balanced.csv              # Dataset listo para EDA ✓
│
├── analysis/                    # Análisis exploratorios
│   └── eda_bruteforce.ipynb    # (Por crear)
│
├── modeling/                    # Modelado de ML
│   ├── notebooks/
│   │   └── Brute_Force_Detection_Modeling.ipynb  # (Por crear)
│   ├── src/
│   │   ├── features/
│   │   │   └── feature_engineering.py
│   │   ├── models/
│   │   │   └── train.py
│   │   └── data/
│   ├── config/
│   │   └── config.yaml
│   └── outputs/
│       └── models/              # Modelos entrenados
│
├── api/                         # API REST (por crear)
│   └── app.py
│
└── README.md                    # Este archivo
```

## 🔬 Features del Dataset

### Features Temporales
- **Timestamp**: Tiempo del flujo (epoch)
- **Flow Duration**: Duración del flujo en microsegundos

### Flow Metrics
- **Total Fwd/Bwd Packets**: Total de paquetes forward/backward
- **Total Length Fwd/Bwd Packets**: Longitud total de paquetes
- **Fwd/Bwd Packet Length** (Max, Min, Mean, Std): Estadísticas de longitud

### Inter-Arrival Time (IAT)
- **Flow IAT** (Mean, Std, Max, Min): Tiempo entre llegadas del flujo
- **Fwd IAT** (Total, Mean, Std, Max, Min): IAT de paquetes forward
- **Bwd IAT** (Total, Mean, Std, Max, Min): IAT de paquetes backward

### TCP Flags
- **PSH, URG, SYN, ACK, FIN, RST, ECE Flag Cnt**: Contadores de flags TCP

### Velocidad
- **Flow Bytes/s**: Bytes por segundo del flujo
- **Flow Packets/s**: Paquetes por segundo del flujo
- **Fwd/Bwd Packets/s**: Paquetes por segundo forward/backward

### Active/Idle Times
- **Active** (Mean, Std, Max, Min): Tiempo activo del flujo
- **Idle** (Mean, Std, Max, Min): Tiempo inactivo del flujo

### Otros
- **Down/Up Ratio**: Ratio de paquetes down/up
- **Average Packet Size**: Tamaño promedio de paquetes
- **Subflow Metrics**: Métricas de subflujos
- **Init Window Bytes**: Bytes de ventana inicial

## 🚀 Cómo Usar

### 1. Preprocesar Dataset (si aún no está hecho)

```bash
cd fuerza-bruta/processed_data
python3 preprocess_bruteforce_consolidated.py
```

**Tiempo estimado**: 5-10 minutos
**Memoria requerida**: ~8-16 GB RAM

### 2. Realizar EDA

```bash
cd fuerza-bruta/analysis
jupyter notebook eda_bruteforce.ipynb
```

### 3. Entrenar Modelos

```bash
cd fuerza-bruta/modeling/notebooks
jupyter notebook Brute_Force_Detection_Modeling.ipynb
```

### 4. Desplegar API (después de entrenar)

```bash
cd fuerza-bruta/api
uvicorn app:app --port 8002 --reload
```

## 📊 Métricas Esperadas

### Sin Feature Engineering
- **F1-Score**: 0.95-0.98
- **Recall**: 0.94-0.97
- **Precision**: 0.95-0.98

### Con Feature Engineering
- **F1-Score**: 0.97-0.99
- **Recall**: 0.96-0.99
- **Precision**: 0.97-0.99

**Nota**: El dataset CSE-CIC-IDS2018 es muy limpio y balanceado, lo que facilita métricas altas.

## 🎯 Características de los Ataques Brute Force

### FTP-BruteForce
- Múltiples intentos de login en puerto FTP (21)
- Alta frecuencia de paquetes
- Patrones repetitivos de autenticación
- Mayormente fallidos hasta éxito

### SSH-Bruteforce
- Múltiples intentos de login en puerto SSH (22)
- Conexiones secuenciales rápidas
- Diferentes credenciales probadas
- Tráfico encriptado característico

### Brute Force-Web
- Intentos repetidos en formularios web
- HTTP POST requests frecuentes
- Mismo endpoint, diferentes payloads
- User-Agent consistente

### Brute Force-XSS
- Inyección de scripts vía fuerza bruta
- Payloads XSS en parámetros web
- Prueba sistemática de vectores de ataque
- Patrones en query strings

## 🔜 Próximos Pasos

1. ✅ **Preprocessing completado** → Dataset balanceado generado
2. 🔄 **EDA** → Análisis exploratorio del dataset preprocesado
3. 🔜 **Feature Engineering** → Crear features adicionales
4. 🔜 **Modelado** → Entrenar XGBoost, Random Forest, Gradient Boosting
5. 🔜 **API REST** → Desplegar modelo como servicio
6. 🔜 **Integración Frontend** → Conectar con dashboard

## 📚 Referencias

- **Dataset**: [CSE-CIC-IDS2018](https://www.unb.ca/cic/datasets/ids-2018.html)
- **Paper**: "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization" (2018)
- **Notebook de referencia**: `external_ref/preprocessing-cse-cic-ids2018.ipynb`

---

**Última actualización**: 2026-01-16
