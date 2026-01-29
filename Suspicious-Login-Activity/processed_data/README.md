# Processed Data - Accesos Sospechosos (RBA Dataset)

## 📁 Contenido del Directorio

Este directorio contiene datos preprocesados para el análisis y modelado de **Accesos Sospechosos (Account Takeover)**.

### Archivos

#### `sample_1M.csv`
**Descripción**: Muestra estratificada de 1 millón de registros del dataset RBA completo (31.2M registros).

**Características**:
- **Registros**: 1,000,000
- **Tamaño**: ~277 MB
- **Origen**: Dataset RBA (DAS Group - KIT)
- **Periodo**: Febrero 2020 - Febrero 2021
- **Estratificación**: Mantiene proporción original de Account Takeover (~0.0005%)

**Distribución**:
- **Normal (False)**: 999,995 registros (99.9995%)
- **Account Takeover (True)**: 5 registros (0.0005%)

**Usuarios únicos**: ~460,000
**IPs únicas**: ~431,000
**Países**: 208

**Columnas (16)**:
1. `index` - Índice original del dataset
2. `Login Timestamp` - Timestamp del intento de login
3. `User ID` - ID pseudónimo del usuario
4. `Round-Trip Time [ms]` - Latencia cliente-servidor
5. `IP Address` - Dirección IP del cliente
6. `Country` - País derivado de la IP
7. `Region` - Región derivada de la IP
8. `City` - Ciudad derivada de la IP
9. `ASN` - Número de sistema autónomo
10. `User Agent String` - User agent completo
11. `Browser Name and Version` - Browser y versión
12. `OS Name and Version` - Sistema operativo y versión
13. `Device Type` - Tipo de dispositivo (mobile/desktop/tablet/bot/unknown)
14. `Login Successful` - Login exitoso (True/False)
15. `Is Attack IP` - IP marcada como atacante (True/False)
16. `Is Account Takeover` - Target variable (True/False)

#### `create_sample.py`
**Descripción**: Script Python para generar `sample_1M.csv` desde el dataset completo.

**Uso**:
```bash
cd processed_data
python3 create_sample.py
```

**Parámetros**:
- `SAMPLE_SIZE = 1_000_000` - Tamaño de la muestra
- `RANDOM_STATE = 42` - Semilla aleatoria para reproducibilidad
- `CHUNK_SIZE = 500_000` - Tamaño de chunks para carga eficiente

**Proceso**:
1. Carga el dataset completo por chunks (500K registros)
2. Muestrea aleatoriamente ~3.5% de cada chunk
3. Estratifica manteniendo proporción de Account Takeover
4. Guarda CSV de 1M registros

**Tiempo estimado**: 5-10 minutos (depende del hardware)

---

## 🎯 Uso

### Para EDA (Análisis Exploratorio)
```python
import pandas as pd

# Cargar muestra fija
df = pd.read_csv('../processed_data/sample_1M.csv')

# Verificar dimensiones
print(f"Registros: {len(df):,}")
print(f"Columnas: {df.shape[1]}")

# Distribución de target
print(df['Is Account Takeover'].value_counts())
```

### Para Modelado
Usar el mismo `sample_1M.csv` garantiza que el EDA y el modelado trabajen con los mismos datos.

**Ventajas**:
- ✅ **Reproducibilidad**: Resultados consistentes entre ejecuciones
- ✅ **Eficiencia**: No cargar 8.5GB cada vez (~277MB vs 8.5GB)
- ✅ **Validación**: Hallazgos del EDA coinciden exactamente con el modelado
- ✅ **Velocidad**: Carga instantánea vs 5-10 minutos de muestreo aleatorio

---

## ⚠️ Notas Importantes

### Desbalance Extremo
El dataset presenta **desbalance extremo** (Account Takeover < 0.001%), lo cual es **realista** para producción:
- En sistemas reales, los ataques exitosos son raros
- Requiere técnicas especiales de manejo de desbalance (SMOTE, class weights, threshold tuning)
- Métricas clave: **Precision**, **Recall**, **F1-Score**, **AUC-PR** (NO Accuracy)

### Dataset Completo
Para **producción** o **modelado final**, se recomienda usar el dataset completo (31.2M registros):
```python
# Cargar dataset completo (requiere ~16GB RAM)
df_full = pd.read_csv('../dataset/rba-dataset.csv')
```

O cargar por chunks:
```python
chunks = pd.read_csv('../dataset/rba-dataset.csv', chunksize=500_000)
for chunk in chunks:
    # Procesar cada chunk
    pass
```

### Regenerar Muestra
Si necesitas regenerar la muestra (por ejemplo, con diferente tamaño o semilla):
```bash
cd processed_data

# Editar create_sample.py (modificar SAMPLE_SIZE o RANDOM_STATE)
nano create_sample.py

# Ejecutar
python3 create_sample.py
```

---

## 📊 Estadísticas de la Muestra

| Métrica | Valor |
|---|---|
| **Registros totales** | 1,000,000 |
| **Usuarios únicos** | 460,021 |
| **IPs únicas** | 431,242 |
| **Países únicos** | 208 |
| **ASNs únicos** | ~15,000 |
| **Browsers únicos** | ~100 |
| **Account Takeover** | 5 (0.0005%) |
| **Login exitosos** | ~85% |
| **Login fallidos** | ~15% |
| **Valores nulos** | 960,980 (principalmente en RTT, Region, City) |

---

## 🔗 Referencias

- **Dataset original**: [RBA Dataset - DAS Group (Kaggle)](https://www.kaggle.com/datasets/dasgroup/rba-dataset)
- **Paper**: "Pump Up Password Security!" (Risk-Based Authentication)
- **GitHub**: [das-group/rba-dataset](https://github.com/das-group/rba-dataset)
- **DOI**: 10.5281/zenodo.6782156

---

**Última actualización**: 2026-01-12
**Autor**: Sistema de Predicción de Incidentes de Ciberseguridad
