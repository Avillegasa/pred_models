"""
AccountTakeoverPredictor - ML prediction logic for account takeover detection.
Encapsulates model loading, feature engineering, and prediction with optimal threshold.
"""
import sys
import os
import time
import joblib
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directory to path to import feature engineering
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class AccountTakeoverPredictor:
    """Encapsulates account takeover detection model and prediction logic."""

    def __init__(
        self,
        model_path: str,
        encoders_path: str,
        threshold_path: str = None,
        model_info_path: str = None
    ):
        """
        Initialize predictor by loading model, encoders, and threshold.

        Args:
            model_path: Path to trained model (.pkl)
            encoders_path: Path to label encoders (.pkl)
            threshold_path: Path to optimal threshold info (.pkl, optional)
            model_info_path: Path to model info JSON (optional)
        """
        print(f"🔧 Initializing AccountTakeoverPredictor...")

        # Load model
        print(f"📦 Loading model from: {model_path}")
        self.model = joblib.load(model_path)

        # Load label encoders
        print(f"📦 Loading encoders from: {encoders_path}")
        self.encoders = joblib.load(encoders_path)

        # Load optimal threshold (if available)
        self.threshold_info = None
        self.optimal_threshold = 0.5  # Default
        if threshold_path and os.path.exists(threshold_path):
            print(f"📦 Loading threshold info from: {threshold_path}")
            self.threshold_info = joblib.load(threshold_path)
            self.optimal_threshold = self.threshold_info.get('optimal_threshold', 0.5)
            print(f"   ✅ Using optimal threshold: {self.optimal_threshold:.4f}")
        else:
            print(f"   ⚠️  Threshold file not found, using default: 0.5")

        # Load model info (optional)
        self.model_info = {}
        if model_info_path and os.path.exists(model_info_path):
            print(f"📦 Loading model info from: {model_info_path}")
            with open(model_info_path, 'r') as f:
                raw_info = json.load(f)
                self.model_info = self._normalize_model_info(raw_info)
        else:
            # Default model info if file not found
            self.model_info = self._get_default_model_info()

        # Cache for user history (for behavioral features)
        # In production, this should be a database or cache service
        self.user_history = {}

        print("✅ AccountTakeoverPredictor initialized successfully!")
        print(f"   Model: {self.get_model_name()}")
        print(f"   Features: {self.get_features_count()}")
        print(f"   Threshold: {self.optimal_threshold:.4f}")

    def _normalize_model_info(self, raw_info: dict) -> dict:
        """Normalize model_info.json structure to expected format."""
        model_name = raw_info.get("best_model", "Gradient Boosting")
        if isinstance(model_name, dict):
            model_name = model_name.get("model_name", "Gradient Boosting")

        metrics = raw_info.get("best_metrics", {})
        timestamp = raw_info.get("timestamp", "2026-01-15T00:00:00")
        training_date = timestamp.split("T")[0] if "T" in timestamp else "2026-01-15"
        n_train = raw_info.get("n_train_samples", 68112)
        n_test = raw_info.get("n_test_samples", 17029)
        n_total = n_train + n_test
        n_features = raw_info.get("n_features", 35)

        return {
            "best_model": {
                "model_name": model_name,
                "metrics": {
                    "f1_score": metrics.get("f1_score", 0.7416),
                    "accuracy": metrics.get("accuracy", 0.9986),
                    "precision": metrics.get("precision", 0.7021),
                    "recall": metrics.get("recall", 0.7857),
                    "roc_auc": metrics.get("roc_auc", 0.9772),
                    "average_precision": metrics.get("average_precision", 0.7955)
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
                "temporal_features": 7,
                "behavioral_features": 8,
                "aggregated_features": 10,
                "categorical_features": 6,
                "numeric_features": 4
            }
        }

    def _get_default_model_info(self) -> dict:
        """Get default model info structure when file is not available."""
        return {
            "best_model": {
                "model_name": "Gradient Boosting",
                "metrics": {
                    "f1_score": 0.7416,
                    "accuracy": 0.9986,
                    "precision": 0.7021,
                    "recall": 0.7857,
                    "roc_auc": 0.9772,
                    "average_precision": 0.7955
                }
            },
            "training_info": {
                "training_date": "2026-01-15",
                "total_samples": 85141,
                "train_samples": 68112,
                "test_samples": 17029
            },
            "feature_info": {
                "total_features": 35,
                "temporal_features": 7,
                "behavioral_features": 8,
                "aggregated_features": 10,
                "categorical_features": 6,
                "numeric_features": 4
            }
        }

    def get_model_name(self) -> str:
        """Get model name."""
        return self.model_info.get("best_model", {}).get("model_name", "Gradient Boosting")

    def get_features_count(self) -> int:
        """Get total features count."""
        return self.model_info.get("feature_info", {}).get("total_features", 35)

    def get_model_info_dict(self) -> dict:
        """Get full model info as dictionary."""
        return self.model_info

    def _prepare_dataframe(self, login_data: dict) -> pd.DataFrame:
        """
        Convert login data dict to DataFrame format expected by feature engineering.

        Args:
            login_data: Dictionary with keys matching LoginInput schema

        Returns:
            DataFrame with 1 row ready for feature engineering
        """
        # Use provided timestamp or current time
        timestamp = login_data.get('login_timestamp', datetime.utcnow().isoformat() + 'Z')

        # Create DataFrame with expected columns
        df = pd.DataFrame([{
            'User ID': login_data.get('user_id', ''),
            'IP Address': login_data.get('ip_address', ''),
            'Country': login_data.get('country', ''),
            'Region': login_data.get('region', ''),
            'City': login_data.get('city', ''),
            'Browser Name and Version': login_data.get('browser', ''),
            'OS Name and Version': login_data.get('os', ''),
            'Device Type': login_data.get('device', ''),
            'Login Successful': login_data.get('login_successful', 1),
            'Is Attack IP': login_data.get('is_attack_ip', 0),
            'ASN': login_data.get('asn', 0),
            'Round-Trip Time (RTT) (ms)': login_data.get('rtt', 0.0),
            'Login Timestamp': timestamp,
            'Is Account Takeover': 0  # Dummy label, will be removed
        }])

        return df

    def _generate_explanation(
        self,
        features_df: pd.DataFrame,
        login_data: dict,
        prediction: int,
        confidence: float
    ) -> dict:
        """
        Generate human-readable explanation for the ATO prediction.
        Analyzes behavioral changes and risk factors with specific evidence.

        Args:
            features_df: DataFrame with engineered features
            login_data: Original login data
            prediction: Model prediction (0=Normal, 1=ATO)
            confidence: Model confidence score (0-1)

        Returns:
            Dictionary with behavioral_changes (with evidence), risk_factors, key_features, and summary
        """
        risk_indicators = []  # List of dicts with 'indicator' and 'evidence'
        risk_factors = {}
        key_features = {}

        # Extract feature values from the engineered features DataFrame
        row = features_df.iloc[0] if len(features_df) > 0 else {}

        # Get user history for comparison if available
        user_id = login_data.get('user_id', '')
        prev_login = self.user_history.get(user_id, {})

        # Check behavioral change features with evidence
        if row.get('country_changed', 0) == 1:
            prev_country = prev_login.get('country', 'desconocido')
            curr_country = login_data.get('country', 'desconocido')
            risk_indicators.append({
                "indicator": "Cambio de pais detectado",
                "evidence": [
                    f"Pais anterior: {prev_country}",
                    f"Pais actual: {curr_country}"
                ],
                "severity": "high"
            })
            risk_factors['country_changed'] = 0.35
        key_features['country_changed'] = bool(row.get('country_changed', 0))

        if row.get('ip_changed', 0) == 1:
            prev_ip = prev_login.get('ip', 'desconocida')
            curr_ip = login_data.get('ip_address', 'desconocida')
            risk_indicators.append({
                "indicator": "Cambio de direccion IP",
                "evidence": [
                    f"IP anterior: {prev_ip}",
                    f"IP actual: {curr_ip}"
                ],
                "severity": "medium"
            })
            risk_factors['ip_changed'] = 0.15
        key_features['ip_changed'] = bool(row.get('ip_changed', 0))

        if row.get('browser_changed', 0) == 1:
            prev_browser = prev_login.get('browser', 'desconocido')
            curr_browser = login_data.get('browser', 'desconocido')
            risk_indicators.append({
                "indicator": "Cambio de navegador",
                "evidence": [
                    f"Navegador anterior: {prev_browser}",
                    f"Navegador actual: {curr_browser}"
                ],
                "severity": "medium"
            })
            risk_factors['browser_changed'] = 0.10
        key_features['browser_changed'] = bool(row.get('browser_changed', 0))

        if row.get('device_changed', 0) == 1:
            prev_device = prev_login.get('device', 'desconocido')
            curr_device = login_data.get('device', 'desconocido')
            risk_indicators.append({
                "indicator": "Cambio de dispositivo",
                "evidence": [
                    f"Dispositivo anterior: {prev_device}",
                    f"Dispositivo actual: {curr_device}"
                ],
                "severity": "medium"
            })
            risk_factors['device_changed'] = 0.10
        key_features['device_changed'] = bool(row.get('device_changed', 0))

        if row.get('os_changed', 0) == 1:
            prev_os = prev_login.get('os', 'desconocido')
            curr_os = login_data.get('os', 'desconocido')
            risk_indicators.append({
                "indicator": "Cambio de sistema operativo",
                "evidence": [
                    f"SO anterior: {prev_os}",
                    f"SO actual: {curr_os}"
                ],
                "severity": "low"
            })
            risk_factors['os_changed'] = 0.08
        key_features['os_changed'] = bool(row.get('os_changed', 0))

        # Check temporal features
        hour = row.get('hour', 0)
        if row.get('is_night', 0) == 1:
            risk_indicators.append({
                "indicator": "Login en horario nocturno inusual",
                "evidence": [
                    f"Hora del login: {int(hour):02d}:00",
                    "Horario considerado de riesgo: 22:00 - 06:00"
                ],
                "severity": "low"
            })
            risk_factors['is_night'] = 0.05
        key_features['is_night'] = bool(row.get('is_night', 0))
        key_features['is_weekend'] = bool(row.get('is_weekend', 0))

        # Check attack IP
        if login_data.get('is_attack_ip', 0) == 1:
            risk_indicators.append({
                "indicator": "IP en lista negra de ataques",
                "evidence": [
                    f"IP reportada: {login_data.get('ip_address', 'desconocida')}",
                    "Esta IP ha sido identificada en ataques previos"
                ],
                "severity": "critical"
            })
            risk_factors['is_attack_ip'] = 0.25
        key_features['is_attack_ip'] = bool(login_data.get('is_attack_ip', 0))

        # Check rapid login
        time_since = row.get('time_since_last_login_hours', 0)
        if row.get('is_rapid_login', 0) == 1:
            risk_indicators.append({
                "indicator": "Login muy rapido desde ultimo acceso",
                "evidence": [
                    f"Tiempo desde ultimo login: {time_since:.1f} horas",
                    "Umbral de alerta: < 0.5 horas (30 minutos)"
                ],
                "severity": "medium"
            })
            risk_factors['is_rapid_login'] = 0.05
        key_features['is_rapid_login'] = bool(row.get('is_rapid_login', 0))

        # Check long gap
        if row.get('is_long_gap', 0) == 1:
            risk_indicators.append({
                "indicator": "Login tras largo periodo de inactividad",
                "evidence": [
                    f"Tiempo desde ultimo login: {time_since:.1f} horas",
                    "Umbral de alerta: > 24 horas"
                ],
                "severity": "low"
            })
            risk_factors['is_long_gap'] = 0.03
        key_features['is_long_gap'] = bool(row.get('is_long_gap', 0))

        # Check abnormal RTT
        rtt = login_data.get('rtt', 0)
        if row.get('is_abnormal_rtt', 0) == 1:
            risk_indicators.append({
                "indicator": "Tiempo de respuesta de red anormal",
                "evidence": [
                    f"RTT actual: {rtt:.1f} ms",
                    "RTT promedio esperado: ~650 ms"
                ],
                "severity": "low"
            })
            risk_factors['is_abnormal_rtt'] = 0.05
        key_features['is_abnormal_rtt'] = bool(row.get('is_abnormal_rtt', 0))

        # Add geographic info
        geo_info = {
            "country": login_data.get('country', 'N/A'),
            "region": login_data.get('region', 'N/A'),
            "city": login_data.get('city', 'N/A'),
            "asn": login_data.get('asn', 'N/A')
        }

        # Generate summary
        confidence_pct = confidence * 100
        num_indicators = len(risk_indicators)

        if prediction == 1:
            if num_indicators == 0:
                summary = f"Login clasificado como Account Takeover con {confidence_pct:.1f}% de confianza basado en patrones de comportamiento."
            else:
                high_risk = sum(1 for i in risk_indicators if i.get('severity') in ['high', 'critical'])
                summary = f"Login de alto riesgo: {num_indicators} indicador{'es' if num_indicators > 1 else ''} detectado{'s' if num_indicators > 1 else ''} ({high_risk} critico{'s' if high_risk != 1 else ''})."
        else:
            if num_indicators > 0:
                summary = f"Login clasificado como normal con {confidence_pct:.1f}% de confianza, aunque se detectaron {num_indicators} patron{'es' if num_indicators > 1 else ''} inusual{'es' if num_indicators > 1 else ''}."
            else:
                summary = f"Login normal con {confidence_pct:.1f}% de confianza. No se detectaron anomalias."

        return {
            "risk_indicators": risk_indicators,
            "risk_factors": risk_factors,
            "key_features": key_features,
            "geo_info": geo_info,
            "summary": summary,
            "total_indicators": num_indicators
        }

    def _engineer_features_simple(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Simplified feature engineering for API prediction.
        Replicates training feature engineering but without requiring full dataset history.

        Args:
            df: Raw login DataFrame (1 row)

        Returns:
            DataFrame with engineered features (35 features)
        """
        result_df = df.copy()

        # Parse timestamp
        result_df['timestamp'] = pd.to_datetime(result_df['Login Timestamp'], errors='coerce')

        # === TEMPORAL FEATURES (11) ===
        result_df['hour'] = result_df['timestamp'].dt.hour
        result_df['day_of_week'] = result_df['timestamp'].dt.dayofweek
        result_df['day_of_month'] = result_df['timestamp'].dt.day
        result_df['month'] = result_df['timestamp'].dt.month
        result_df['is_weekend'] = (result_df['day_of_week'] >= 5).astype(int)
        result_df['is_night'] = ((result_df['hour'] >= 22) | (result_df['hour'] <= 6)).astype(int)
        result_df['is_business_hours'] = ((result_df['hour'] >= 9) & (result_df['hour'] <= 17)).astype(int)

        # === BEHAVIORAL FEATURES (9) - simplified for single prediction ===
        user_id = result_df['User ID'].iloc[0]

        # Check user history cache
        if user_id in self.user_history:
            prev_login = self.user_history[user_id]
            result_df['ip_changed'] = int(result_df['IP Address'].iloc[0] != prev_login['ip'])
            result_df['country_changed'] = int(result_df['Country'].iloc[0] != prev_login['country'])
            result_df['browser_changed'] = int(result_df['Browser Name and Version'].iloc[0] != prev_login['browser'])
            result_df['device_changed'] = int(result_df['Device Type'].iloc[0] != prev_login['device'])
            result_df['os_changed'] = int(result_df['OS Name and Version'].iloc[0] != prev_login['os'])

            # Time since last login (in hours)
            time_diff = (result_df['timestamp'].iloc[0] - prev_login['timestamp']).total_seconds() / 3600
            result_df['time_since_last_login_hours'] = time_diff

            # Rapid login and long gap detection
            result_df['is_rapid_login'] = int(time_diff < 0.5)  # Less than 30 minutes
            result_df['is_long_gap'] = int(time_diff > 24)  # More than 24 hours
        else:
            # First login for this user (no history)
            result_df['ip_changed'] = 0
            result_df['country_changed'] = 0
            result_df['browser_changed'] = 0
            result_df['device_changed'] = 0
            result_df['os_changed'] = 0
            result_df['time_since_last_login_hours'] = 0.0
            result_df['is_rapid_login'] = 0
            result_df['is_long_gap'] = 0

        # === AGGREGATED FEATURES (10) - simplified defaults ===
        # In production, these should come from database queries
        result_df['ip_count_per_user'] = 1  # Default
        result_df['country_count_per_user'] = 1  # Default
        result_df['browser_count_per_user'] = 1  # Default
        result_df['device_count_per_user'] = 1  # Default
        result_df['total_logins_per_user'] = 1  # Default
        result_df['success_rate_per_user'] = 1.0  # Default
        result_df['user_count_per_ip'] = 1  # Default
        result_df['is_suspicious_ip'] = result_df['Is Attack IP']

        # RTT z-score (simplified, assume mean=650, std=150 from training)
        rtt_mean, rtt_std = 650, 150
        result_df['rtt_zscore'] = (result_df['Round-Trip Time (RTT) (ms)'] - rtt_mean) / rtt_std
        result_df['is_abnormal_rtt'] = (np.abs(result_df['rtt_zscore']) > 2).astype(int)

        # === NUMERIC FEATURES (4) - RENAME to match model ===
        result_df['Round-Trip Time [ms]'] = result_df['Round-Trip Time (RTT) (ms)'].astype(float)
        result_df['ASN'] = result_df['ASN'].astype(int)
        result_df['Login Successful'] = result_df['Login Successful'].astype(int)
        result_df['Is Attack IP'] = result_df['Is Attack IP'].astype(int)

        # === CATEGORICAL ENCODING (6) - ADD _encoded SUFFIX ===
        categorical_cols = [
            'Browser Name and Version',
            'OS Name and Version',
            'Device Type',
            'Country',
            'Region',
            'City'
        ]

        for col in categorical_cols:
            encoded_col_name = f"{col}_encoded"
            if col in self.encoders:
                encoder = self.encoders[col]
                # Handle unseen categories (assign to -1)
                try:
                    result_df[encoded_col_name] = encoder.transform(result_df[col])
                except ValueError:
                    # Unseen category, use -1
                    result_df[encoded_col_name] = -1
            else:
                # Encoder not found, use -1
                result_df[encoded_col_name] = -1

        # === SELECT FINAL FEATURES (35 features, EXACT order from training) ===
        feature_cols = [
            # Numeric (4)
            'Round-Trip Time [ms]',
            'ASN',
            'Login Successful',
            'Is Attack IP',
            # Temporal (11)
            'hour',
            'day_of_week',
            'day_of_month',
            'month',
            'is_weekend',
            'is_night',
            'is_business_hours',
            # Behavioral (9)
            'ip_changed',
            'country_changed',
            'browser_changed',
            'device_changed',
            'os_changed',
            'time_since_last_login_hours',
            'is_rapid_login',
            'is_long_gap',
            # Aggregated (10)
            'ip_count_per_user',
            'country_count_per_user',
            'browser_count_per_user',
            'device_count_per_user',
            'total_logins_per_user',
            'success_rate_per_user',
            'user_count_per_ip',
            'is_suspicious_ip',
            'rtt_zscore',
            'is_abnormal_rtt',
            # Categorical encoded (6)
            'Browser Name and Version_encoded',
            'OS Name and Version_encoded',
            'Device Type_encoded',
            'Country_encoded',
            'Region_encoded',
            'City_encoded'
        ]

        # Update user history cache
        self.user_history[user_id] = {
            'ip': result_df['IP Address'].iloc[0],
            'country': df['Country'].iloc[0],  # Use original non-encoded value
            'browser': df['Browser Name and Version'].iloc[0],
            'device': df['Device Type'].iloc[0],
            'os': df['OS Name and Version'].iloc[0],
            'timestamp': result_df['timestamp'].iloc[0]
        }

        # Select features in correct order
        final_df = result_df[feature_cols]

        # CRITICAL: Replace any NaN values with defaults
        final_df = final_df.fillna({
            'time_since_last_login_hours': 0.0,
            'is_rapid_login': 0,
            'is_long_gap': 0,
            'ip_count_per_user': 1,
            'country_count_per_user': 1,
            'browser_count_per_user': 1,
            'device_count_per_user': 1,
            'total_logins_per_user': 1,
            'success_rate_per_user': 1.0,
            'user_count_per_ip': 1,
            'is_suspicious_ip': 0,
            'rtt_zscore': 0.0,
            'is_abnormal_rtt': 0,
            'Browser Name and Version_encoded': -1,
            'OS Name and Version_encoded': -1,
            'Device Type_encoded': -1,
            'Country_encoded': -1,
            'Region_encoded': -1,
            'City_encoded': -1
        })

        # Fill any remaining NaN with 0
        final_df = final_df.fillna(0)

        return final_df

    def predict_single(self, login_data: dict) -> dict:
        """
        Predict if a single login is normal or account takeover.

        Args:
            login_data: Dictionary with login information

        Returns:
            Dictionary with prediction results including explanation
        """
        start_time = time.time()

        # Step 1: Convert to DataFrame
        df = self._prepare_dataframe(login_data)

        # Step 2: Feature engineering
        X = self._engineer_features_simple(df)

        # Step 3: Predict with model
        probabilities = self.model.predict_proba(X)[0]
        prob_normal = float(probabilities[0])
        prob_ato = float(probabilities[1])

        # Step 4: Apply optimal threshold
        prediction = int(prob_ato >= self.optimal_threshold)
        confidence = float(max(probabilities))

        # Step 5: Calculate risk score (0-100)
        risk_score = round(prob_ato * 100, 2)

        # Step 6: Generate explanation
        explanation = self._generate_explanation(X, login_data, prediction, confidence)

        # Step 7: Format response
        processing_time_ms = (time.time() - start_time) * 1000

        result = {
            'prediction': prediction,
            'prediction_label': 'Account Takeover' if prediction == 1 else 'Normal',
            'confidence': confidence,
            'probability_normal': prob_normal,
            'probability_ato': prob_ato,
            'risk_score': risk_score,
            'explanation': explanation,
            'metadata': {
                'model': self.get_model_name(),
                'features_count': self.get_features_count(),
                'threshold': self.optimal_threshold,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'processing_time_ms': round(processing_time_ms, 2)
            }
        }

        return result

    def predict_batch(self, logins: List[dict]) -> Tuple[List[dict], float]:
        """
        Predict multiple logins in batch.

        Args:
            logins: List of login dictionaries

        Returns:
            Tuple of (predictions list with explanations, processing_time_ms)
        """
        start_time = time.time()

        results = []
        for idx, login in enumerate(logins):
            # Note: For true batch efficiency, we'd process all together
            # For simplicity, we'll call predict_single which handles user history
            single_result = self.predict_single(login)

            results.append({
                'login_index': idx,
                'user_id': login.get('user_id', ''),
                'prediction': single_result['prediction'],
                'prediction_label': single_result['prediction_label'],
                'confidence': single_result['confidence'],
                'risk_score': single_result['risk_score'],
                'explanation': single_result['explanation']
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

    def get_threshold_info(self) -> dict:
        """Get threshold information."""
        if self.threshold_info:
            return {
                'optimal_threshold': self.threshold_info.get('optimal_threshold', 0.5),
                'default_threshold': self.threshold_info.get('default_threshold', 0.5),
                'f1_improvement_pct': self.threshold_info.get('improvement_pct', 0.0)
            }
        return {
            'optimal_threshold': 0.5,
            'default_threshold': 0.5,
            'f1_improvement_pct': 0.0
        }


# Singleton instance (will be initialized on app startup)
predictor_instance = None


def get_predictor(
    model_path: str = None,
    encoders_path: str = None,
    threshold_path: str = None,
    model_info_path: str = None
) -> AccountTakeoverPredictor:
    """
    Get or create predictor instance (singleton pattern).

    Args:
        model_path: Path to model (only needed for first call)
        encoders_path: Path to encoders (only needed for first call)
        threshold_path: Path to threshold (optional)
        model_info_path: Path to model info (optional)

    Returns:
        AccountTakeoverPredictor instance
    """
    global predictor_instance

    if predictor_instance is None:
        if model_path is None or encoders_path is None:
            raise ValueError(
                "First call to get_predictor() requires model_path and encoders_path"
            )

        predictor_instance = AccountTakeoverPredictor(
            model_path=model_path,
            encoders_path=encoders_path,
            threshold_path=threshold_path,
            model_info_path=model_info_path
        )

    return predictor_instance
