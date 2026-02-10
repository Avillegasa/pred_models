"""
PhishingPredictor - ML prediction logic for phishing email detection.
Encapsulates model loading, feature engineering, and prediction.
"""
import sys
import os
import time
import joblib
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
import re

# Add parent directory to path to import feature engineering
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.features.feature_engineering import engineer_features


class PhishingPredictor:
    """Encapsulates phishing detection model and prediction logic."""

    def __init__(self, model_path: str, vectorizer_path: str, model_info_path: str = None):
        """
        Initialize predictor by loading model and vectorizer.

        Args:
            model_path: Path to trained model (.pkl)
            vectorizer_path: Path to TF-IDF vectorizer (.pkl)
            model_info_path: Path to model info JSON (optional)
        """
        print(f"🔧 Initializing PhishingPredictor...")

        # Load model
        print(f"📦 Loading model from: {model_path}")
        self.model = joblib.load(model_path)

        # Load TF-IDF vectorizer
        print(f"📦 Loading vectorizer from: {vectorizer_path}")
        self.vectorizer = joblib.load(vectorizer_path)

        # Load model info (optional)
        self.model_info = {}
        if model_info_path and os.path.exists(model_info_path):
            print(f"📦 Loading model info from: {model_info_path}")
            with open(model_info_path, 'r') as f:
                raw_info = json.load(f)
                # Normalize structure to expected format
                self.model_info = self._normalize_model_info(raw_info)
        else:
            # Default model info if file not found
            self.model_info = self._get_default_model_info()

        print("✅ PhishingPredictor initialized successfully!")
        print(f"   Model: {self.get_model_name()}")
        print(f"   Features: {self.get_features_count()}")

    def _normalize_model_info(self, raw_info: dict) -> dict:
        """
        Normalize model_info.json structure to expected format.
        Handles the actual structure from training output.
        """
        # Extract model name (can be string or dict)
        model_name = raw_info.get("best_model", "Gradient Boosting")
        if isinstance(model_name, dict):
            model_name = model_name.get("model_name", "Gradient Boosting")

        # Extract metrics
        metrics = raw_info.get("best_metrics", {})

        # Extract training date from timestamp
        timestamp = raw_info.get("timestamp", "2026-01-10T00:00:00")
        training_date = timestamp.split("T")[0] if "T" in timestamp else "2026-01-10"

        # Extract samples info
        n_train = raw_info.get("n_train_samples", 31323)
        n_test = raw_info.get("n_test_samples", 7831)
        n_total = n_train + n_test

        # Extract features count
        n_features = raw_info.get("n_features", 1016)

        # Return normalized structure
        return {
            "best_model": {
                "model_name": model_name,
                "metrics": {
                    "f1_score": metrics.get("f1_score", 0.9909),
                    "accuracy": metrics.get("accuracy", 0.9898),
                    "precision": metrics.get("precision", 0.9891),
                    "recall": metrics.get("recall", 0.9927),
                    "roc_auc": metrics.get("roc_auc", 0.9990)
                }
            },
            "training_info": {
                "training_date": training_date,
                "total_samples": n_total,
                "train_samples": n_train,
                "test_samples": n_test
            },
            "feature_info": {
                "total_features": n_features,
                "tfidf_features": 1000,
                "numeric_features": 16
            }
        }

    def _get_default_model_info(self) -> dict:
        """Get default model info structure when file is not available."""
        return {
            "best_model": {
                "model_name": "Gradient Boosting",
                "metrics": {
                    "f1_score": 0.9909,
                    "accuracy": 0.9898,
                    "precision": 0.9891,
                    "recall": 0.9927,
                    "roc_auc": 0.9990
                }
            },
            "training_info": {
                "training_date": "2026-01-10",
                "total_samples": 39154,
                "train_samples": 31323,
                "test_samples": 7831
            },
            "feature_info": {
                "total_features": 1016,
                "tfidf_features": 1000,
                "numeric_features": 16
            }
        }

    def get_model_name(self) -> str:
        """Get model name."""
        return self.model_info.get("best_model", {}).get("model_name", "Gradient Boosting")

    def get_features_count(self) -> int:
        """Get total features count."""
        return self.model_info.get("feature_info", {}).get("total_features", 1016)

    def get_model_info_dict(self) -> dict:
        """Get full model info as dictionary."""
        return self.model_info

    def _prepare_dataframe(self, email_data: dict) -> pd.DataFrame:
        """
        Convert email data dict to DataFrame format expected by feature engineering.

        Args:
            email_data: Dictionary with keys: sender, receiver, subject, body, urls

        Returns:
            DataFrame with 1 row ready for feature engineering
        """
        # Create DataFrame with expected columns
        df = pd.DataFrame([{
            'sender': email_data.get('sender', ''),
            'receiver': email_data.get('receiver', ''),
            'subject': email_data.get('subject', ''),
            'body': email_data.get('body', ''),
            'urls': email_data.get('urls', 0),
            'date': '',  # Not used in features but expected by some code
            'label': 0  # Dummy label, will be removed after feature engineering
        }])

        return df

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering using loaded vectorizer.
        CRITICAL: Uses fit_tfidf=False to only transform, not fit.

        Args:
            df: Raw email DataFrame

        Returns:
            DataFrame with engineered features (1016 features)
        """
        # Apply feature engineering with loaded vectorizer
        features_df, _ = engineer_features(
            df,
            tfidf_vectorizer=self.vectorizer,  # Use loaded vectorizer
            fit_tfidf=False,  # CRITICAL: Only transform, don't fit
            config=None  # Use defaults
        )

        # Remove label column if present
        if 'label' in features_df.columns:
            features_df = features_df.drop('label', axis=1)

        return features_df

    def _generate_explanation(
        self,
        email_data: dict,
        prediction: int,
        confidence: float
    ) -> dict:
        """
        Generate human-readable explanation for the prediction.
        Analyzes email content to identify risk indicators with specific evidence.

        Args:
            email_data: Original email data (sender, subject, body, urls)
            prediction: Model prediction (0=Legitimate, 1=Phishing)
            confidence: Model confidence score (0-1)

        Returns:
            Dictionary with risk_indicators (with evidence), suspicious_terms, and summary
        """
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        sender = email_data.get('sender', '')
        has_urls = email_data.get('urls', 0) == 1

        subject_lower = subject.lower()
        body_lower = body.lower()
        sender_lower = sender.lower()
        full_text_lower = f"{subject_lower} {body_lower}"
        full_text_original = f"{subject} {body}"

        risk_indicators = []  # List of dicts with 'indicator' and 'evidence'
        suspicious_terms = []

        # Helper to find and extract evidence with context
        def find_evidence(text_lower, text_original, patterns, context_chars=40):
            """Find patterns and return evidence with surrounding context"""
            evidence_list = []
            for pattern in patterns:
                idx = text_lower.find(pattern)
                if idx != -1:
                    start = max(0, idx - 15)
                    end = min(len(text_original), idx + len(pattern) + context_chars)
                    snippet = text_original[start:end].strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(text_original):
                        snippet = snippet + "..."
                    evidence_list.append(snippet)
            return evidence_list

        # Check for URL presence
        if has_urls:
            # Try to find actual URLs in text
            url_matches = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', full_text_original, re.IGNORECASE)
            if url_matches:
                risk_indicators.append({
                    "indicator": "Contiene URLs/enlaces",
                    "evidence": url_matches[:3]  # Max 3 URLs
                })
            else:
                risk_indicators.append({
                    "indicator": "Contiene URLs/enlaces",
                    "evidence": ["El campo 'urls' indica presencia de enlaces"]
                })

        # Check for URL patterns in text (if not already found)
        if not has_urls:
            url_matches = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', full_text_original, re.IGNORECASE)
            if url_matches:
                risk_indicators.append({
                    "indicator": "URLs detectadas en el texto",
                    "evidence": url_matches[:3]
                })

        # Check for UPPERCASE words (shouting)
        uppercase_words = re.findall(r'\b[A-Z]{3,}\b', full_text_original)
        uppercase_words = [w for w in uppercase_words if w not in ['URL', 'HTML', 'HTTP', 'HTTPS', 'WWW', 'CEO', 'USA', 'UK']]
        if uppercase_words:
            risk_indicators.append({
                "indicator": "Contiene texto en MAYUSCULAS (indicador de urgencia)",
                "evidence": list(set(uppercase_words))[:5]
            })

        # Check for urgency language
        urgency_words = ['urgent', 'urgente', 'immediately', 'inmediatamente', 'asap', 'right now',
                        'ahora mismo', 'expire', 'expira', 'limited time', 'tiempo limitado',
                        'act now', 'actua ahora', 'hurry', 'rapido', '24 hours', '24 horas']
        urgency_evidence = find_evidence(full_text_lower, full_text_original, urgency_words)
        if urgency_evidence:
            risk_indicators.append({
                "indicator": "Contiene lenguaje de urgencia",
                "evidence": urgency_evidence[:3]
            })

        # Check for call-to-action patterns
        cta_patterns = ['click here', 'haz clic', 'click below', 'click the link', 'click to',
                       'log in now', 'sign in now', 'inicia sesion', 'verify now', 'verifica ahora']
        cta_evidence = find_evidence(full_text_lower, full_text_original, cta_patterns)
        if cta_evidence:
            risk_indicators.append({
                "indicator": "Contiene llamada a la accion (click here)",
                "evidence": cta_evidence[:3]
            })

        # Check for credential requests
        credential_words = ['password', 'contrasena', 'login', 'credential', 'credenciales',
                           'username', 'usuario', 'pin', 'ssn', 'social security', 'cvv', 'credit card']
        credential_evidence = find_evidence(full_text_lower, full_text_original, credential_words)
        if credential_evidence:
            risk_indicators.append({
                "indicator": "Solicita credenciales sensibles",
                "evidence": credential_evidence[:3]
            })

        # Check for financial language
        financial_words = ['bank', 'banco', 'account', 'cuenta', 'payment', 'pago', 'invoice',
                          'factura', 'transaction', 'transaccion', 'transfer', 'wire', 'credit card',
                          'tarjeta de credito', 'dinero', 'money']
        financial_evidence = find_evidence(full_text_lower, full_text_original, financial_words)
        if financial_evidence:
            risk_indicators.append({
                "indicator": "Contiene lenguaje financiero/bancario",
                "evidence": financial_evidence[:3]
            })

        # Check for impersonation (brand names)
        brand_names = ['paypal', 'amazon', 'apple', 'microsoft', 'netflix', 'facebook',
                      'google', 'linkedin', 'ebay', 'wells fargo', 'chase', 'bank of america']
        found_brands = []
        for brand in brand_names:
            if brand in full_text_lower or brand in sender_lower:
                found_brands.append(brand.title())
        if found_brands:
            evidence = [f"Marca mencionada: {brand}" for brand in found_brands[:3]]
            if any(brand.lower() in sender_lower for brand in found_brands):
                evidence.append(f"Remitente sospechoso: {sender}")
            risk_indicators.append({
                "indicator": "Suplantacion de marca conocida",
                "evidence": evidence
            })

        # Check for threat language
        threat_words = ['suspend', 'suspender', 'terminate', 'terminar', 'close', 'cerrar',
                       'locked', 'bloqueado', 'blocked', 'unauthorized', 'no autorizado',
                       'unusual activity', 'actividad inusual', 'will be deleted', 'sera eliminado']
        threat_evidence = find_evidence(full_text_lower, full_text_original, threat_words)
        if threat_evidence:
            risk_indicators.append({
                "indicator": "Contiene amenazas o advertencias",
                "evidence": threat_evidence[:3]
            })

        # Check for suspicious sender patterns
        suspicious_sender_patterns = ['noreply', 'no-reply', 'support@', 'security@', 'alert@',
                                     'verify@', 'update@', 'admin@']
        sender_suspicious = any(p in sender_lower for p in suspicious_sender_patterns)
        # Check for domain mismatch (e.g., paypal in text but sender is not paypal.com)
        if found_brands:
            sender_domain = sender_lower.split('@')[-1] if '@' in sender_lower else ''
            for brand in found_brands:
                if brand.lower() in full_text_lower and brand.lower() not in sender_domain:
                    risk_indicators.append({
                        "indicator": "Dominio del remitente no coincide con la marca",
                        "evidence": [f"Menciona '{brand}' pero el remitente es '{sender}'"]
                    })
                    break

        # Collect suspicious terms found (for legacy compatibility)
        phishing_keywords = ['urgent', 'verify', 'account', 'suspended', 'click here',
                            'confirm', 'password', 'expire', 'immediately', 'limited time',
                            'winner', 'free', 'prize', 'congratulations', 'selected']
        for keyword in phishing_keywords:
            if keyword in full_text_lower:
                suspicious_terms.append(keyword)
        suspicious_terms = list(set(suspicious_terms))[:10]

        # Generate summary
        prediction_label = "phishing" if prediction == 1 else "legitimo"
        confidence_pct = confidence * 100
        indicator_count = len(risk_indicators)

        if prediction == 1:
            if indicator_count == 0:
                summary = f"Este email fue clasificado como {prediction_label} con {confidence_pct:.1f}% de confianza basado en patrones de texto."
            else:
                summary = f"Este email muestra {indicator_count} indicador{'es' if indicator_count > 1 else ''} de phishing con {confidence_pct:.1f}% de confianza."
        else:
            if indicator_count > 0:
                summary = f"Este email fue clasificado como {prediction_label} con {confidence_pct:.1f}% de confianza, aunque se detectaron {indicator_count} patron{'es' if indicator_count > 1 else ''} sospechoso{'s' if indicator_count > 1 else ''}."
            else:
                summary = f"Este email fue clasificado como {prediction_label} con {confidence_pct:.1f}% de confianza. No se detectaron indicadores de phishing."

        return {
            "risk_indicators": risk_indicators if risk_indicators else [],
            "suspicious_terms": suspicious_terms if suspicious_terms else [],
            "summary": summary,
            "total_indicators": indicator_count
        }

    def _generate_metrics_analysis(self, email_data: dict) -> List[Dict]:
        """
        Generate metrics analysis comparing current values against normal ranges.
        Returns a list of metric comparisons for the frontend to display.

        Args:
            email_data: Original email data (sender, subject, body, urls)

        Returns:
            List of metric analysis dictionaries
        """
        metrics_analysis = []

        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        sender = email_data.get('sender', '')
        has_urls = email_data.get('urls', 0) == 1

        full_text = f"{subject} {body}"
        full_text_lower = full_text.lower()

        # Count URLs in text
        url_matches = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', full_text, re.IGNORECASE)
        url_count = len(url_matches) + (1 if has_urls and not url_matches else 0)
        url_anomalous = url_count > 5
        metrics_analysis.append({
            "metric_name": "Conteo de URLs",
            "metric_key": "url_count",
            "normal_range": {"min": 0, "max": 2},
            "current_value": url_count,
            "is_anomalous": url_anomalous,
            "anomaly_direction": "high" if url_anomalous else None,
            "interpretation": "Exceso de URLs puede indicar intento de redireccion maliciosa" if url_anomalous else "Cantidad de URLs dentro del rango normal para comunicacion legitima"
        })

        # Count urgent words
        urgency_words = ['urgent', 'urgente', 'immediately', 'inmediatamente', 'asap', 'right now',
                        'ahora mismo', 'expire', 'expira', 'limited time', 'tiempo limitado',
                        'act now', 'actua ahora', 'hurry', 'rapido', '24 hours', '24 horas']
        urgent_count = sum(1 for word in urgency_words if word in full_text_lower)
        urgent_anomalous = urgent_count > 0
        metrics_analysis.append({
            "metric_name": "Palabras de Urgencia",
            "metric_key": "urgent_words",
            "normal_range": {"min": 0, "max": 0},
            "current_value": urgent_count,
            "is_anomalous": urgent_anomalous,
            "anomaly_direction": "high" if urgent_anomalous else None,
            "interpretation": "Presion psicologica detectada, tactica principal de phishing" if urgent_anomalous else "Sin lenguaje de urgencia, comunicacion normal"
        })

        # Count suspicious terms
        suspicious_keywords = ['verify', 'account', 'suspended', 'click here', 'confirm',
                              'password', 'winner', 'free', 'prize', 'congratulations',
                              'selected', 'claim', 'reward', 'limited offer']
        suspicious_count = sum(1 for word in suspicious_keywords if word in full_text_lower)
        suspicious_anomalous = suspicious_count > 3
        metrics_analysis.append({
            "metric_name": "Terminos Sospechosos",
            "metric_key": "suspicious_terms",
            "normal_range": {"min": 0, "max": 1},
            "current_value": suspicious_count,
            "is_anomalous": suspicious_anomalous,
            "anomaly_direction": "high" if suspicious_anomalous else None,
            "interpretation": "Alto uso de vocabulario tipico de phishing" if suspicious_anomalous else "Terminologia dentro del rango normal"
        })

        # Count uppercase words (shouting)
        uppercase_words = re.findall(r'\b[A-Z]{3,}\b', full_text)
        uppercase_words = [w for w in uppercase_words if w not in ['URL', 'HTML', 'HTTP', 'HTTPS', 'WWW', 'CEO', 'USA', 'UK', 'PDF', 'FAQ']]
        uppercase_count = len(uppercase_words)
        uppercase_anomalous = uppercase_count > 3
        metrics_analysis.append({
            "metric_name": "Palabras en MAYUSCULAS",
            "metric_key": "uppercase_count",
            "normal_range": {"min": 0, "max": 2},
            "current_value": uppercase_count,
            "is_anomalous": uppercase_anomalous,
            "anomaly_direction": "high" if uppercase_anomalous else None,
            "interpretation": "Uso excesivo de mayusculas para crear urgencia" if uppercase_anomalous else "Uso normal de mayusculas"
        })

        # Check sender domain suspiciousness
        sender_domain = sender.lower().split('@')[-1] if '@' in sender.lower() else ''
        suspicious_sender_patterns = ['noreply', 'no-reply', 'support', 'security', 'alert', 'verify', 'update', 'admin']
        sender_suspicious = any(p in sender.lower() for p in suspicious_sender_patterns)
        # Check for known brands in text but not in sender domain
        brand_names = ['paypal', 'amazon', 'apple', 'microsoft', 'netflix', 'facebook', 'google', 'linkedin', 'ebay']
        brand_mismatch = any(brand in full_text_lower and brand not in sender_domain for brand in brand_names)
        domain_suspicious = sender_suspicious or brand_mismatch
        metrics_analysis.append({
            "metric_name": "Dominio del Remitente",
            "metric_key": "sender_domain",
            "normal_range": {"min": 0, "max": 0},
            "current_value": 1 if domain_suspicious else 0,
            "is_anomalous": domain_suspicious,
            "anomaly_direction": "high" if domain_suspicious else None,
            "interpretation": f"Dominio sospechoso o no coincide con marca mencionada: {sender}" if domain_suspicious else "Dominio del remitente parece legitimo"
        })

        return metrics_analysis

    def predict_single(self, email_data: dict) -> dict:
        """
        Predict if a single email is phishing or legitimate.

        Args:
            email_data: Dictionary with keys:
                - sender (str): Email sender
                - receiver (str, optional): Email receiver
                - subject (str): Email subject
                - body (str): Email body
                - urls (int, optional): 0 or 1

        Returns:
            Dictionary with prediction results:
                - prediction (int): 0=Legitimate, 1=Phishing
                - prediction_label (str): Human-readable label
                - confidence (float): Confidence score
                - probability_legitimate (float): P(legitimate)
                - probability_phishing (float): P(phishing)
                - explanation (dict): Risk indicators and reasoning
                - metadata (dict): Model info and timing
        """
        start_time = time.time()

        # Step 1: Convert to DataFrame
        df = self._prepare_dataframe(email_data)

        # Step 2: Feature engineering
        X = self._engineer_features(df)

        # Step 3: Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        confidence = float(max(probabilities))

        # Step 4: Generate explanation
        explanation = self._generate_explanation(email_data, int(prediction), confidence)

        # Step 5: Generate metrics analysis
        metrics_analysis = self._generate_metrics_analysis(email_data)

        # Step 6: Format response
        processing_time_ms = (time.time() - start_time) * 1000

        result = {
            'prediction': int(prediction),
            'prediction_label': 'Phishing' if prediction == 1 else 'Legitimate',
            'confidence': confidence,
            'probability_legitimate': float(probabilities[0]),
            'probability_phishing': float(probabilities[1]),
            'explanation': explanation,
            'metrics_analysis': metrics_analysis,
            'metadata': {
                'model': self.get_model_name(),
                'features_count': self.get_features_count(),
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'processing_time_ms': round(processing_time_ms, 2)
            }
        }

        return result

    def predict_batch(self, emails: List[dict]) -> Tuple[List[dict], float]:
        """
        Predict multiple emails in batch.
        More efficient than calling predict_single multiple times.

        Args:
            emails: List of email dictionaries

        Returns:
            Tuple of (List of prediction dictionaries, processing_time_ms)
            Each prediction dictionary contains:
                - email_index (int): Index in input list
                - prediction (int): 0 or 1
                - prediction_label (str): Human-readable label
                - confidence (float): Confidence score
                - explanation (dict): Risk indicators and reasoning
        """
        start_time = time.time()

        # Step 1: Convert all emails to DataFrame
        df_list = [self._prepare_dataframe(email) for email in emails]
        df = pd.concat(df_list, ignore_index=True)

        # Step 2: Feature engineering (once for all emails)
        X = self._engineer_features(df)

        # Step 3: Batch prediction
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        # Step 4: Format responses with explanations and metrics analysis
        results = []
        for idx, (pred, probs, email) in enumerate(zip(predictions, probabilities, emails)):
            confidence = float(max(probs))
            explanation = self._generate_explanation(email, int(pred), confidence)
            metrics_analysis = self._generate_metrics_analysis(email)
            results.append({
                'email_index': idx,
                'prediction': int(pred),
                'prediction_label': 'Phishing' if pred == 1 else 'Legitimate',
                'confidence': confidence,
                'explanation': explanation,
                'metrics_analysis': metrics_analysis
            })

        processing_time_ms = (time.time() - start_time) * 1000

        return results, processing_time_ms

    def get_metrics(self) -> dict:
        """Get model performance metrics."""
        return self.model_info.get("best_model", {}).get("metrics", {})

    def get_training_info(self) -> dict:
        """Get training data information."""
        return self.model_info.get("training_info", {})

    def get_feature_info(self) -> dict:
        """Get feature information."""
        return self.model_info.get("feature_info", {})


# Singleton instance (will be initialized on app startup)
predictor_instance = None


def get_predictor(
    model_path: str = None,
    vectorizer_path: str = None,
    model_info_path: str = None
) -> PhishingPredictor:
    """
    Get or create predictor instance (singleton pattern).

    Args:
        model_path: Path to model (only needed for first call)
        vectorizer_path: Path to vectorizer (only needed for first call)
        model_info_path: Path to model info (optional)

    Returns:
        PhishingPredictor instance
    """
    global predictor_instance

    if predictor_instance is None:
        if model_path is None or vectorizer_path is None:
            raise ValueError("First call to get_predictor() requires model_path and vectorizer_path")

        predictor_instance = PhishingPredictor(
            model_path=model_path,
            vectorizer_path=vectorizer_path,
            model_info_path=model_info_path
        )

    return predictor_instance
