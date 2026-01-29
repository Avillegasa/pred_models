"""
Brute Force Detection - Predictor Module
Handles model loading and predictions.
"""
import time
import json
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

# Singleton predictor instance
_predictor_instance = None


class BruteForcePredictor:
    """
    Predictor for Brute Force Detection.
    Loads trained Random Forest model and makes predictions on network flows.
    """

    # Expected feature names (must match training data)
    FEATURE_NAMES = [
        'Dst Port', 'Protocol', 'Timestamp', 'Flow Duration', 'Tot Fwd Pkts',
        'Tot Bwd Pkts', 'TotLen Fwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min',
        'Fwd Pkt Len Mean', 'Fwd Pkt Len Std', 'Bwd Pkt Len Max', 'Bwd Pkt Len Min',
        'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s', 'Flow Pkts/s',
        'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Fwd IAT Std',
        'Bwd IAT Tot', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
        'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags',
        'Fwd Pkts/s', 'Bwd Pkts/s', 'Pkt Len Min', 'Pkt Len Max', 'Pkt Len Mean',
        'Pkt Len Std', 'Pkt Len Var', 'FIN Flag Cnt', 'RST Flag Cnt',
        'PSH Flag Cnt', 'ACK Flag Cnt', 'URG Flag Cnt', 'CWE Flag Count',
        'Down/Up Ratio', 'Fwd Byts/b Avg', 'Fwd Pkts/b Avg', 'Fwd Blk Rate Avg',
        'Bwd Byts/b Avg', 'Bwd Pkts/b Avg', 'Bwd Blk Rate Avg', 'Init Fwd Win Byts',
        'Init Bwd Win Byts', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean',
        'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std'
    ]

    # Mapping from API field names to feature names
    API_TO_FEATURE_MAP = {
        'dst_port': 'Dst Port',
        'protocol': 'Protocol',
        'timestamp': 'Timestamp',
        'flow_duration': 'Flow Duration',
        'tot_fwd_pkts': 'Tot Fwd Pkts',
        'tot_bwd_pkts': 'Tot Bwd Pkts',
        'totlen_fwd_pkts': 'TotLen Fwd Pkts',
        'fwd_pkt_len_max': 'Fwd Pkt Len Max',
        'fwd_pkt_len_min': 'Fwd Pkt Len Min',
        'fwd_pkt_len_mean': 'Fwd Pkt Len Mean',
        'fwd_pkt_len_std': 'Fwd Pkt Len Std',
        'bwd_pkt_len_max': 'Bwd Pkt Len Max',
        'bwd_pkt_len_min': 'Bwd Pkt Len Min',
        'bwd_pkt_len_mean': 'Bwd Pkt Len Mean',
        'bwd_pkt_len_std': 'Bwd Pkt Len Std',
        'flow_byts_s': 'Flow Byts/s',
        'flow_pkts_s': 'Flow Pkts/s',
        'flow_iat_mean': 'Flow IAT Mean',
        'flow_iat_std': 'Flow IAT Std',
        'flow_iat_max': 'Flow IAT Max',
        'fwd_iat_std': 'Fwd IAT Std',
        'bwd_iat_tot': 'Bwd IAT Tot',
        'bwd_iat_mean': 'Bwd IAT Mean',
        'bwd_iat_std': 'Bwd IAT Std',
        'bwd_iat_max': 'Bwd IAT Max',
        'bwd_iat_min': 'Bwd IAT Min',
        'fwd_psh_flags': 'Fwd PSH Flags',
        'bwd_psh_flags': 'Bwd PSH Flags',
        'fwd_urg_flags': 'Fwd URG Flags',
        'bwd_urg_flags': 'Bwd URG Flags',
        'fwd_pkts_s': 'Fwd Pkts/s',
        'bwd_pkts_s': 'Bwd Pkts/s',
        'pkt_len_min': 'Pkt Len Min',
        'pkt_len_max': 'Pkt Len Max',
        'pkt_len_mean': 'Pkt Len Mean',
        'pkt_len_std': 'Pkt Len Std',
        'pkt_len_var': 'Pkt Len Var',
        'fin_flag_cnt': 'FIN Flag Cnt',
        'rst_flag_cnt': 'RST Flag Cnt',
        'psh_flag_cnt': 'PSH Flag Cnt',
        'ack_flag_cnt': 'ACK Flag Cnt',
        'urg_flag_cnt': 'URG Flag Cnt',
        'cwe_flag_count': 'CWE Flag Count',
        'down_up_ratio': 'Down/Up Ratio',
        'fwd_byts_b_avg': 'Fwd Byts/b Avg',
        'fwd_pkts_b_avg': 'Fwd Pkts/b Avg',
        'fwd_blk_rate_avg': 'Fwd Blk Rate Avg',
        'bwd_byts_b_avg': 'Bwd Byts/b Avg',
        'bwd_pkts_b_avg': 'Bwd Pkts/b Avg',
        'bwd_blk_rate_avg': 'Bwd Blk Rate Avg',
        'init_fwd_win_byts': 'Init Fwd Win Byts',
        'init_bwd_win_byts': 'Init Bwd Win Byts',
        'fwd_act_data_pkts': 'Fwd Act Data Pkts',
        'fwd_seg_size_min': 'Fwd Seg Size Min',
        'active_mean': 'Active Mean',
        'active_std': 'Active Std',
        'active_max': 'Active Max',
        'active_min': 'Active Min',
        'idle_mean': 'Idle Mean',
        'idle_std': 'Idle Std'
    }

    def __init__(self, model_path: str, model_info_path: Optional[str] = None):
        """
        Initialize predictor with trained model.

        Args:
            model_path: Path to trained model (.pkl)
            model_info_path: Path to model metadata (.json)
        """
        logger.info(f"Loading model from: {model_path}")

        # Load model
        self.model = joblib.load(model_path)
        self.model_name = type(self.model).__name__

        # Load model info if available
        self.model_info = {}
        if model_info_path:
            try:
                with open(model_info_path, 'r') as f:
                    self.model_info = json.load(f)
                logger.info("✅ Model metadata loaded")
            except Exception as e:
                logger.warning(f"⚠️ Could not load model info: {e}")

        logger.info(f"✅ Model loaded: {self.model_name}")
        logger.info(f"✅ Features: {len(self.FEATURE_NAMES)}")

    def _prepare_features(self, flow_data: Dict) -> pd.DataFrame:
        """
        Convert API input to model features.

        Args:
            flow_data: Dictionary with network flow data

        Returns:
            DataFrame with features in correct order
        """
        # Map API field names to feature names
        features_dict = {}
        for api_name, feature_name in self.API_TO_FEATURE_MAP.items():
            features_dict[feature_name] = flow_data.get(api_name, 0.0)

        # Create DataFrame with features in correct order
        df = pd.DataFrame([features_dict], columns=self.FEATURE_NAMES)

        return df

    def _generate_explanation(
        self,
        flow_data: Dict,
        prediction: int,
        confidence: float
    ) -> Dict:
        """
        Generate human-readable explanation for the brute force prediction.
        Analyzes network flow features to identify attack patterns with evidence.

        Args:
            flow_data: Dictionary with network flow data (normalized 0-1)
            prediction: Model prediction (0=Benign, 1=Brute Force)
            confidence: Model confidence score (0-1)

        Returns:
            Dictionary with risk_indicators (with evidence), top_features, and summary
        """
        risk_indicators = []  # List of dicts with 'indicator' and 'evidence'
        top_features = {}

        # Thresholds for identifying anomalous values
        HIGH_BWD_PKTS_S = 0.5
        HIGH_FLOW_PKTS_S = 0.3
        LOW_FLOW_DURATION = 0.01
        HIGH_PSH_FLAG = 0.5
        HIGH_FWD_PKTS_S = 0.3

        # Normal traffic baselines (for comparison)
        NORMAL_BWD_PKTS_S = 0.008
        NORMAL_FLOW_PKTS_S = 0.024
        NORMAL_FLOW_DURATION = 0.5

        # Check backward packet rate (key discriminator - 112.7x ratio)
        bwd_pkts_s = flow_data.get('bwd_pkts_s', 0)
        if bwd_pkts_s >= HIGH_BWD_PKTS_S:
            ratio = bwd_pkts_s / NORMAL_BWD_PKTS_S if NORMAL_BWD_PKTS_S > 0 else 0
            risk_indicators.append({
                "indicator": "Tasa de paquetes backward extremadamente alta",
                "evidence": [
                    f"Valor actual: {bwd_pkts_s:.4f} (normalizado)",
                    f"Valor normal: ~{NORMAL_BWD_PKTS_S:.4f}",
                    f"Ratio: {ratio:.1f}x por encima de lo normal"
                ],
                "severity": "critical"
            })
        top_features['bwd_pkts_s'] = bwd_pkts_s

        # Check flow packets rate (24.7x ratio)
        flow_pkts_s = flow_data.get('flow_pkts_s', 0)
        if flow_pkts_s >= HIGH_FLOW_PKTS_S:
            ratio = flow_pkts_s / NORMAL_FLOW_PKTS_S if NORMAL_FLOW_PKTS_S > 0 else 0
            risk_indicators.append({
                "indicator": "Tasa de paquetes de flujo muy alta",
                "evidence": [
                    f"Valor actual: {flow_pkts_s:.4f}",
                    f"Valor normal: ~{NORMAL_FLOW_PKTS_S:.4f}",
                    "Patron tipico de trafico automatizado"
                ],
                "severity": "high"
            })
        top_features['flow_pkts_s'] = flow_pkts_s

        # Check flow duration (0.01x ratio - very short)
        flow_duration = flow_data.get('flow_duration', 1)
        if flow_duration < LOW_FLOW_DURATION:
            risk_indicators.append({
                "indicator": "Duracion de flujo extremadamente corta",
                "evidence": [
                    f"Duracion actual: {flow_duration:.6f} (normalizado)",
                    f"Duracion normal: ~{NORMAL_FLOW_DURATION:.2f}",
                    "Conexiones muy rapidas tipicas de brute force"
                ],
                "severity": "high"
            })
        top_features['flow_duration'] = flow_duration

        # Check PSH flag count (1.96x ratio)
        psh_flag_cnt = flow_data.get('psh_flag_cnt', 0)
        if psh_flag_cnt >= HIGH_PSH_FLAG:
            risk_indicators.append({
                "indicator": "Alto conteo de flags PSH",
                "evidence": [
                    f"Valor: {psh_flag_cnt:.4f}",
                    "Flag PSH indica envio inmediato de datos",
                    "Firma de herramientas automatizadas"
                ],
                "severity": "medium"
            })
        top_features['psh_flag_cnt'] = psh_flag_cnt

        # Check forward packet rate
        fwd_pkts_s = flow_data.get('fwd_pkts_s', 0)
        if fwd_pkts_s >= HIGH_FWD_PKTS_S:
            risk_indicators.append({
                "indicator": "Tasa alta de paquetes forward",
                "evidence": [
                    f"Valor: {fwd_pkts_s:.4f}",
                    "Alto volumen de solicitudes salientes"
                ],
                "severity": "medium"
            })
        top_features['fwd_pkts_s'] = fwd_pkts_s

        # Check destination port (common attack ports)
        dst_port = flow_data.get('dst_port', 0)
        if dst_port < 0.01 and dst_port > 0:
            # Denormalize to approximate port number
            approx_port = int(dst_port * 65535)
            common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS", 3389: "RDP"}
            port_name = ""
            for p, name in common_ports.items():
                if abs(approx_port - p) < 10:
                    port_name = f" ({name})"
                    break
            risk_indicators.append({
                "indicator": "Puerto de destino comun para ataques",
                "evidence": [
                    f"Puerto aproximado: {approx_port}{port_name}",
                    "Puertos bajos son objetivos frecuentes"
                ],
                "severity": "low"
            })
        top_features['dst_port'] = dst_port

        # Check total backward packets
        tot_bwd_pkts = flow_data.get('tot_bwd_pkts', 0)
        if tot_bwd_pkts >= 0.5:
            risk_indicators.append({
                "indicator": "Alto volumen de paquetes de respuesta",
                "evidence": [
                    f"Valor: {tot_bwd_pkts:.4f}",
                    "Indica multiples respuestas del servidor"
                ],
                "severity": "medium"
            })
        top_features['tot_bwd_pkts'] = tot_bwd_pkts

        # Check for RST flags (connection resets - common in attacks)
        rst_flag_cnt = flow_data.get('rst_flag_cnt', 0)
        if rst_flag_cnt >= 0.3:
            risk_indicators.append({
                "indicator": "Alto conteo de flags RST",
                "evidence": [
                    f"Valor: {rst_flag_cnt:.4f}",
                    "Indica conexiones rechazadas/reseteadas",
                    "Comun en intentos fallidos de autenticacion"
                ],
                "severity": "medium"
            })

        # Sort top_features by value descending and keep top 5
        top_features = dict(sorted(top_features.items(), key=lambda x: x[1], reverse=True)[:5])

        # Generate summary
        confidence_pct = confidence * 100
        num_indicators = len(risk_indicators)

        if prediction == 1:
            if num_indicators == 0:
                summary = f"Ataque brute force detectado con {confidence_pct:.1f}% de confianza basado en patrones de red."
            else:
                critical = sum(1 for i in risk_indicators if i.get('severity') == 'critical')
                high = sum(1 for i in risk_indicators if i.get('severity') == 'high')
                summary = f"Ataque brute force detectado: {num_indicators} anomalia{'s' if num_indicators > 1 else ''} de red ({critical} critica{'s' if critical != 1 else ''}, {high} alta{'s' if high != 1 else ''})."
        else:
            if num_indicators > 0:
                summary = f"Trafico clasificado como benigno con {confidence_pct:.1f}% de confianza, aunque se detectaron {num_indicators} patron{'es' if num_indicators > 1 else ''} inusual{'es' if num_indicators > 1 else ''}."
            else:
                summary = f"Trafico benigno con {confidence_pct:.1f}% de confianza. Patrones de red normales."

        return {
            "risk_indicators": risk_indicators,
            "top_features": top_features,
            "summary": summary,
            "total_indicators": num_indicators
        }

    def predict_single(self, flow_data: Dict) -> Dict:
        """
        Predict a single network flow.

        Args:
            flow_data: Network flow data

        Returns:
            Dictionary with prediction, explanation and metadata
        """
        start_time = time.time()

        # Prepare features
        X = self._prepare_features(flow_data)

        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        # Format response
        prediction_label = "Brute Force" if prediction == 1 else "Benign"
        confidence = float(probabilities[prediction])

        # Generate explanation
        explanation = self._generate_explanation(flow_data, int(prediction), confidence)

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        return {
            "prediction": int(prediction),
            "prediction_label": prediction_label,
            "confidence": confidence,
            "probabilities": {
                "Benign": float(probabilities[0]),
                "Brute Force": float(probabilities[1])
            },
            "explanation": explanation,
            "processing_time_ms": round(processing_time_ms, 2),
            "model_name": self.model_name
        }

    def predict_batch(self, flows_data: List[Dict]) -> Tuple[List[Dict], float]:
        """
        Predict multiple network flows.

        Args:
            flows_data: List of network flow data

        Returns:
            Tuple of (predictions list with explanations, total processing time in ms)
        """
        start_time = time.time()

        # Prepare all features
        X_list = [self._prepare_features(flow) for flow in flows_data]
        X = pd.concat(X_list, ignore_index=True)

        # Batch predict
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # Format results with explanations
        results = []
        for idx, (pred, probs, flow) in enumerate(zip(predictions, probabilities, flows_data)):
            prediction_label = "Brute Force" if pred == 1 else "Benign"
            confidence = float(probs[pred])
            explanation = self._generate_explanation(flow, int(pred), confidence)

            results.append({
                "index": idx,
                "prediction": int(pred),
                "prediction_label": prediction_label,
                "confidence": confidence,
                "probabilities": {
                    "Benign": float(probs[0]),
                    "Brute Force": float(probs[1])
                },
                "explanation": explanation
            })

        return results, processing_time_ms

    def get_model_name(self) -> str:
        """Get model name."""
        return self.model_name

    def get_features_count(self) -> int:
        """Get number of features."""
        return len(self.FEATURE_NAMES)

    def get_metrics(self) -> Dict:
        """Get model metrics from metadata."""
        return self.model_info.get("best_model", {}).get("metrics", {})

    def get_feature_info(self) -> Dict:
        """Get feature information."""
        return {
            "total_features": len(self.FEATURE_NAMES),
            "feature_names": self.FEATURE_NAMES
        }

    def get_training_info(self) -> Dict:
        """Get training data information."""
        dataset_info = self.model_info.get("dataset", {})
        split_info = self.model_info.get("split", {})

        return {
            "training_date": self.model_info.get("timestamp", "2026-01-17"),
            "total_samples": dataset_info.get("total_records", 763568),
            "train_samples": split_info.get("train_size", 610854),
            "test_samples": split_info.get("test_size", 152714),
            "balance": dataset_info.get("balance", {
                "Benign": 381784,
                "Brute Force": 381784
            })
        }


def get_predictor(
    model_path: Optional[str] = None,
    model_info_path: Optional[str] = None
) -> BruteForcePredictor:
    """
    Get or create predictor instance (singleton pattern).

    Args:
        model_path: Path to model (only for first initialization)
        model_info_path: Path to model info (only for first initialization)

    Returns:
        BruteForcePredictor instance
    """
    global _predictor_instance

    if _predictor_instance is None:
        if model_path is None:
            raise ValueError("model_path required for first initialization")

        _predictor_instance = BruteForcePredictor(
            model_path=model_path,
            model_info_path=model_info_path
        )

    return _predictor_instance
