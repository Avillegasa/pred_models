# Análisis Exploratorio de Datos - CEAS_08 Phishing Dataset

Este directorio contiene el análisis exploratorio completo del dataset CEAS_08 para detección de phishing y spam en emails.

## 📁 Contenido

- **EDA_Phishing_CEAS08.ipynb**: Notebook Jupyter con el análisis exploratorio completo

## 🚀 Cómo Usar

### Requisitos

Instalar las librerías necesarias:

```bash
pip install pandas numpy matplotlib seaborn wordcloud jupyter
```

### Ejecutar el Notebook

```bash
# Navegar al directorio
cd Phishing/analysis

# Iniciar Jupyter Notebook
jupyter notebook EDA_Phishing_CEAS08.ipynb
```

## 📊 Contenido del EDA

El notebook incluye 6 fases de análisis:

### **Fase 1: Exploración Inicial**
- Carga del dataset (1.3M+ emails)
- Estructura y dimensiones
- Análisis de valores nulos
- Distribución de clases (legítimo vs spam/phishing)

### **Fase 2: Análisis de Características Textuales**
- Longitudes de asuntos y cuerpos
- Conteo de palabras
- Análisis de dominios de remitentes
- Comparación entre clases

### **Fase 3: Análisis Temporal**
- Distribución por hora del día
- Distribución por día de la semana
- Patrones temporales de ataques
- Heatmaps de actividad

### **Fase 4: Análisis de URLs**
- Presencia de URLs en emails
- Comparación entre clases
- Tablas de contingencia

### **Fase 5: Análisis de Palabras y Contenido**
- Palabras más frecuentes por clase
- Word clouds visuales
- Palabras distintivas y exclusivas
- Ratios de asociación con spam

### **Fase 6: Resumen y Conclusiones**
- Estadísticas finales
- Conclusiones clave
- Recomendaciones para modelado
- Próximos pasos

## 📈 Características del Dataset

- **Total de registros**: 1,305,707 emails
- **Columnas**: sender, receiver, date, subject, body, label, urls
- **Clases**:
  - 0 = Email legítimo
  - 1 = Spam/Phishing
- **Periodo**: Agosto 2008

## 🎯 Hallazgos Principales

El EDA revela:

1. **Balance de clases**: Distribución entre emails legítimos y spam
2. **Patrones textuales**: Diferencias en longitud y vocabulario
3. **Presencia de URLs**: Mayor frecuencia en emails maliciosos
4. **Patrones temporales**: Concentración de ataques en horarios específicos
5. **Dominios sospechosos**: Identificación de dominios frecuentes en spam

## 🔧 Recomendaciones para Modelado

Basado en el EDA, se sugiere:

### Preprocesamiento
- Tokenización y limpieza de texto
- Vectorización (TF-IDF, embeddings)
- Manejo de valores nulos

### Feature Engineering
- Longitudes de texto
- Presencia de URLs
- Características del remitente
- Features temporales
- Ratio de caracteres especiales

### Modelos Sugeridos
- **Baseline**: Naive Bayes
- **Tradicionales**: Logistic Regression, Random Forest, SVM
- **Deep Learning**: LSTM, BERT, RoBERTa
- **Ensemble**: XGBoost, LightGBM

### Métricas de Evaluación
- Precision, Recall, F1-Score
- AUC-ROC
- Matriz de confusión
- No confiar solo en Accuracy (especialmente si hay desbalance)

## 📝 Notas

- El dataset es grande, algunas visualizaciones usan muestras para mejorar performance
- Los word clouds se generan con las primeras 10,000 muestras de cada clase
- Considerar usar chunks para procesamiento si hay problemas de memoria

## 👤 Autor

Análisis realizado para trabajo académico de predicción de incidentes de ciberseguridad.

## 📅 Fecha

Enero 2026
