"""
FEATURE ENGINEERING para Phishing Email Detection
Adaptado para ejecución local (sin Azure ML)

Este módulo extrae features de emails para clasificación de phishing:
- Features de texto (longitudes, conteo de palabras, caracteres especiales)
- Features de metadata (dominio del sender, presencia de URLs)
- Sentiment analysis (simulado con keywords)
- TF-IDF vectorization del contenido combinado
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
import joblib


def extract_domain(email):
    """Extraer dominio del email del remitente"""
    try:
        if pd.isna(email):
            return 'unknown'
        if '@' in str(email):
            return str(email).split('@')[1].lower()
        return 'unknown'
    except:
        return 'unknown'


def count_urls(text):
    """Contar URLs en el texto del cuerpo del email"""
    if pd.isna(text):
        return 0
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return len(re.findall(url_pattern, str(text)))


def extract_text_features(text):
    """
    Extraer features básicas de un texto:
    - Longitud total (caracteres)
    - Conteo de palabras
    - Conteo de caracteres especiales
    """
    if pd.isna(text):
        return 0, 0, 0

    text = str(text)
    length = len(text)
    word_count = len(text.split())
    special_chars = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', text))

    return length, word_count, special_chars


def get_sentiment_score(text):
    """
    Análisis de sentimiento simplificado basado en keywords.
    Retorna un score entre 0.0 (sospechoso) y 1.0 (legítimo)
    """
    if pd.isna(text) or len(str(text).strip()) == 0:
        return 0.5  # Neutral para textos vacíos

    # Keywords indicativas de phishing/spam
    phishing_keywords = [
        'urgent', 'free', 'click', 'limited', 'offer', 'prize', 'winner',
        'congratulations', 'verify', 'suspend', 'account', 'expired',
        'password', 'reset', 'confirm', 'update', 'act now', 'claim',
        'viagra', 'pills', 'rolex', 'replica', 'enlargement'
    ]

    # Keywords indicativas de emails legítimos
    legitimate_keywords = [
        'meeting', 'schedule', 'project', 'team', 'report', 'update',
        'information', 'attached', 'regards', 'sincerely', 'python',
        'development', 'code', 'bug', 'patch', 'commit'
    ]

    text_lower = str(text).lower()

    phishing_count = sum(1 for word in phishing_keywords if word in text_lower)
    legitimate_count = sum(1 for word in legitimate_keywords if word in text_lower)

    # Calcular score
    if phishing_count > legitimate_count:
        return 0.3  # Sospechoso
    elif legitimate_count > phishing_count:
        return 0.8  # Legítimo
    else:
        return 0.5  # Neutral


def engineer_features(df, tfidf_vectorizer=None, fit_tfidf=True, config=None):
    """
    Pipeline completo de feature engineering

    Args:
        df: DataFrame con columnas raw (sender, receiver, subject, body, label, urls)
        tfidf_vectorizer: Vectorizador TF-IDF pre-entrenado (opcional)
        fit_tfidf: Si True, fit el vectorizador; si False, solo transform
        config: Diccionario con configuración (max_features, ngram_range, etc.)

    Returns:
        features_df: DataFrame con todas las features engineered
        tfidf_vectorizer: Vectorizador TF-IDF (para guardar y reusar en test)
    """
    print("🔧 Iniciando Feature Engineering...")
    print(f"📊 Datos de entrada: {len(df)} registros")

    # Configuración por defecto
    if config is None:
        config = {
            'max_features': 1000,
            'ngram_range': (1, 2),
            'min_df': 5
        }

    # ======== 1. LIMPIEZA BÁSICA ========
    print("🧹 Limpiando datos...")
    df = df.copy()
    df['subject'] = df['subject'].fillna('')
    df['body'] = df['body'].fillna('')
    df['sender'] = df['sender'].fillna('unknown@unknown.com')
    df['receiver'] = df['receiver'].fillna('unknown@unknown.com')

    # ======== 2. FEATURES DE TEXTO ========
    print("📝 Extrayendo features de texto...")

    # Subject features
    subject_features = df['subject'].apply(extract_text_features)
    df['subject_length'] = [x[0] for x in subject_features]
    df['subject_words'] = [x[1] for x in subject_features]
    df['subject_special'] = [x[2] for x in subject_features]

    # Body features
    body_features = df['body'].apply(extract_text_features)
    df['body_length'] = [x[0] for x in body_features]
    df['body_words'] = [x[1] for x in body_features]
    df['body_special'] = [x[2] for x in body_features]

    # ======== 3. FEATURES DE METADATA ========
    print("🔍 Extrayendo features de metadata...")

    # Sender domain
    df['sender_domain'] = df['sender'].apply(extract_domain)

    # URL count (además de la columna 'urls' que ya existe)
    df['url_count'] = df['body'].apply(count_urls)

    # ======== 4. SENTIMENT ANALYSIS ========
    print("🧠 Analizando sentiment (basado en keywords)...")
    df['subject_sentiment'] = df['subject'].apply(get_sentiment_score)
    df['body_sentiment'] = df['body'].apply(get_sentiment_score)

    # ======== 5. FEATURES DERIVADAS ========
    print("🔢 Creando features derivadas...")

    # Ratios
    df['subject_body_ratio'] = df['subject_length'] / (df['body_length'] + 1)
    df['special_chars_ratio'] = (df['subject_special'] + df['body_special']) / (df['subject_length'] + df['body_length'] + 1)

    # Presencia de keywords sospechosas
    df['has_urgent'] = df['subject'].str.contains('urgent|urgente', case=False, na=False).astype(int)
    df['has_free'] = df['subject'].str.contains('free|gratis', case=False, na=False).astype(int)
    df['has_click'] = df['body'].str.contains('click here|haz clic', case=False, na=False).astype(int)

    # ======== 6. ENCODING CATEGÓRICO ========
    print("🏷️ Encoding sender domain...")

    # Label encoding para sender domain (top 50 dominios más frecuentes)
    domain_counts = df['sender_domain'].value_counts()
    top_domains = domain_counts.head(50).index.tolist()
    df['sender_domain_encoded'] = df['sender_domain'].apply(
        lambda x: top_domains.index(x) if x in top_domains else -1
    )

    # ======== 7. TF-IDF VECTORIZATION ========
    print("🔤 Creando TF-IDF features...")

    # Combinar subject y body para TF-IDF
    df['combined_text'] = df['subject'] + ' ' + df['body']

    # Inicializar o usar vectorizador existente
    if tfidf_vectorizer is None:
        tfidf_vectorizer = TfidfVectorizer(
            max_features=config['max_features'],
            stop_words='english',
            ngram_range=config['ngram_range'],
            min_df=config['min_df'],
            lowercase=True,
            strip_accents='unicode'
        )

    # Fit o transform
    if fit_tfidf:
        tfidf_features = tfidf_vectorizer.fit_transform(df['combined_text'])
        print(f"✅ TF-IDF vocabulary size: {len(tfidf_vectorizer.vocabulary_)}")
    else:
        tfidf_features = tfidf_vectorizer.transform(df['combined_text'])

    # Convertir a DataFrame
    tfidf_df = pd.DataFrame(
        tfidf_features.toarray(),
        columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
    )

    # ======== 8. COMBINAR TODAS LAS FEATURES ========
    print("🔗 Combinando features...")

    # Features numéricas finales
    numeric_features = [
        'subject_length', 'subject_words', 'subject_special',
        'body_length', 'body_words', 'body_special',
        'url_count', 'urls',  # urls es la columna original (0/1)
        'sender_domain_encoded',
        'subject_sentiment', 'body_sentiment',
        'subject_body_ratio', 'special_chars_ratio',
        'has_urgent', 'has_free', 'has_click'
    ]

    # Combinar features numéricas con TF-IDF
    final_features = pd.concat([
        df[numeric_features].reset_index(drop=True),
        tfidf_df.reset_index(drop=True)
    ], axis=1)

    # Agregar label si existe
    if 'label' in df.columns:
        final_features['label'] = df['label'].values

    print(f"✅ Features totales creadas: {final_features.shape[1] - (1 if 'label' in final_features.columns else 0)}")
    print(f"   - Features numéricas: {len(numeric_features)}")
    print(f"   - Features TF-IDF: {tfidf_features.shape[1]}")

    if 'label' in final_features.columns:
        print(f"📊 Distribución de labels: {final_features['label'].value_counts().to_dict()}")

    return final_features, tfidf_vectorizer


def save_features_and_vectorizer(features_df, tfidf_vectorizer, output_dir):
    """Guardar features y vectorizador TF-IDF"""
    os.makedirs(output_dir, exist_ok=True)

    # Guardar features
    features_path = os.path.join(output_dir, 'features.csv')
    features_df.to_csv(features_path, index=False)
    print(f"💾 Features guardadas en: {features_path}")

    # Guardar vectorizador
    vectorizer_path = os.path.join(output_dir, 'tfidf_vectorizer.pkl')
    joblib.dump(tfidf_vectorizer, vectorizer_path)
    print(f"💾 TF-IDF vectorizer guardado en: {vectorizer_path}")

    return features_path, vectorizer_path


def load_vectorizer(vectorizer_path):
    """Cargar vectorizador TF-IDF guardado"""
    return joblib.load(vectorizer_path)


if __name__ == "__main__":
    # Ejemplo de uso standalone
    import argparse

    parser = argparse.ArgumentParser(description='Feature Engineering para Phishing Detection')
    parser.add_argument('--input_data', type=str, required=True, help='Path al CSV de entrada')
    parser.add_argument('--output_dir', type=str, required=True, help='Directorio de salida')
    parser.add_argument('--max_features', type=int, default=1000, help='Max features TF-IDF')
    parser.add_argument('--ngram_min', type=int, default=1, help='Ngram min')
    parser.add_argument('--ngram_max', type=int, default=2, help='Ngram max')
    parser.add_argument('--min_df', type=int, default=5, help='Min document frequency')

    args = parser.parse_args()

    # Configuración
    config = {
        'max_features': args.max_features,
        'ngram_range': (args.ngram_min, args.ngram_max),
        'min_df': args.min_df
    }

    # Cargar datos
    print(f"📂 Cargando datos desde: {args.input_data}")
    df = pd.read_csv(args.input_data)

    # Feature engineering
    features_df, tfidf_vectorizer = engineer_features(df, config=config, fit_tfidf=True)

    # Guardar
    save_features_and_vectorizer(features_df, tfidf_vectorizer, args.output_dir)

    print("🎯 Feature Engineering completado exitosamente!")
