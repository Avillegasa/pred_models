# 📊 Dataset Limpio y Splits para Modelado

Este directorio contiene los datasets procesados y listos para modelado, con **exactamente los mismos 39,154 registros** que fueron analizados en el EDA.

---

## 📁 Archivos Disponibles

### **1. CEAS_08_clean.csv** (65 MB)
- **Descripción**: Dataset completo limpio con todos los registros parseados correctamente
- **Registros**: 39,154 emails
- **Columnas**: 7 (sender, receiver, date, subject, body, label, urls)
- **Uso**: Para análisis completo o crear tus propios splits personalizados

### **2. train.csv** (52 MB)
- **Descripción**: Conjunto de entrenamiento (80% del dataset)
- **Registros**: 31,323 emails
- **Distribución**:
  - Clase 0 (Legítimo): 13,850 (44.22%)
  - Clase 1 (Spam/Phishing): 17,473 (55.78%)
- **Uso**: Para entrenar modelos de Machine Learning

### **3. test.csv** (13 MB)
- **Descripción**: Conjunto de prueba (20% del dataset)
- **Registros**: 7,831 emails
- **Distribución**:
  - Clase 0 (Legítimo): 3,462 (44.21%)
  - Clase 1 (Spam/Phishing): 4,369 (55.79%)
- **Uso**: Para evaluar el rendimiento final de modelos entrenados

### **4. dataset_metadata.json**
- **Descripción**: Metadata del proceso de split
- **Contenido**: Fecha, tamaños, distribución, parámetros usados
- **Uso**: Documentación y reproducibilidad

### **5. prepare_clean_dataset.py**
- **Descripción**: Script Python que generó todos los archivos
- **Uso**: Reproducir el proceso o crear nuevos splits con diferentes parámetros

---

## 🎯 Características del Split

| Parámetro | Valor |
|-----------|-------|
| **Total de registros** | 39,154 |
| **Train size** | 31,323 (80%) |
| **Test size** | 7,831 (20%) |
| **Estratificado** | ✅ Sí (mantiene proporción de clases) |
| **Random state** | 42 (reproducible) |
| **Balance de clases** | 44.22% Legítimo / 55.78% Spam |

---

## 🚀 Cómo Usar en tu Modelado

### **Opción 1: Usar splits pre-creados (Recomendado)**

```python
import pandas as pd

# Cargar datasets
train_df = pd.read_csv('processed_data/train.csv')
test_df = pd.read_csv('processed_data/test.csv')

# Separar features y target
X_train = train_df.drop('label', axis=1)
y_train = train_df['label']

X_test = test_df.drop('label', axis=1)
y_test = test_df['label']

print(f"Train: {len(X_train):,} registros")
print(f"Test: {len(X_test):,} registros")
```

### **Opción 2: Usar dataset completo y crear tu propio split**

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Cargar dataset completo
df = pd.read_csv('processed_data/CEAS_08_clean.csv')

# Crear tu propio split (ejemplo: 70/30)
X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    stratify=y,
    random_state=42
)
```

### **Opción 3: Crear train/val/test (70/15/15)**

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('processed_data/CEAS_08_clean.csv')
X = df.drop('label', axis=1)
y = df['label']

# Primero: separar test (15%)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.15, stratify=y, random_state=42
)

# Segundo: separar train/val del resto
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, stratify=y_temp, random_state=42
)

print(f"Train: {len(X_train):,} ({len(X_train)/len(df)*100:.1f}%)")
print(f"Val: {len(X_val):,} ({len(X_val)/len(df)*100:.1f}%)")
print(f"Test: {len(X_test):,} ({len(X_test)/len(df)*100:.1f}%)")
```

---

## ✅ Ventajas de este Dataset

1. **Consistencia con EDA**: Los mismos registros analizados en el análisis exploratorio
2. **Datos limpios**: Solo registros parseados correctamente, sin errores
3. **Split estratificado**: Mantiene la proporción de clases en train/test
4. **Reproducible**: Random state fijo (42) para resultados consistentes
5. **Listo para usar**: No necesitas preprocesar, solo cargar y modelar

---

## ⚠️ Notas Importantes

### **Valores Nulos**
El dataset contiene algunos valores nulos:
- `receiver`: 462 nulos (1.18%)
- `subject`: 28 nulos (0.07%)

**Recomendación**: Manejar estos nulos en tu preprocesamiento:
```python
# Opción 1: Rellenar con string vacío
df['subject'] = df['subject'].fillna('')
df['receiver'] = df['receiver'].fillna('')

# Opción 2: Eliminar filas con nulos en subject (solo 28)
df = df.dropna(subset=['subject'])
```

### **Columnas del Dataset**
```
1. sender     → Email del remitente (object)
2. receiver   → Email del destinatario (object)
3. date       → Fecha/hora del email (object)
4. subject    → Asunto del email (object)
5. body       → Cuerpo del email (object)
6. label      → Clase (0=Legítimo, 1=Spam) (int64)
7. urls       → Tiene URLs (0=No, 1=Sí) (int64)
```

### **Preprocesamiento Sugerido**
Antes de modelar, considera:
1. Limpiar nulos en `subject` y `receiver`
2. Crear features de longitud (subject_length, body_length, etc.)
3. Vectorizar texto con TF-IDF o Count Vectorizer
4. Extraer features del dominio del sender
5. No usar features temporales (fechas tienen errores, ver EDA)

---

## 📚 Siguiente Paso

Ahora estás listo para crear tu **notebook de Modelado** con datos consistentes del EDA.

**Ejemplo de estructura sugerida:**
```
1. Cargar train.csv y test.csv
2. Preprocesamiento (limpiar nulos, feature engineering)
3. Vectorización de texto (TF-IDF)
4. Entrenar modelo baseline (Naive Bayes, Logistic Regression)
5. Evaluar en test set
6. Analizar resultados
```

---

**Fecha de creación**: 2026-01-10 14:10:08
**Total de registros**: 39,154
**Split**: 80% Train (31,323) / 20% Test (7,831)
**Balance**: Ligeramente desbalanceado (55.78% Spam, 44.22% Legítimo)
