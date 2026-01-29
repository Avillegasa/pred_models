"""
Brute Force Detection API - Pydantic Models
Data models for request/response validation.
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


# ============================================================================
# REQUEST MODELS
# ============================================================================

class NetworkFlowInput(BaseModel):
    """
    Network flow data for brute force detection.
    All features normalized between 0 and 1.
    """
    dst_port: float = Field(..., ge=0, le=1, description="Destination Port (normalized)")
    protocol: float = Field(..., ge=0, le=1, description="Protocol (normalized)")
    timestamp: float = Field(..., ge=0, le=1, description="Timestamp (normalized)")
    flow_duration: float = Field(..., ge=0, le=1, description="Flow Duration (normalized)")
    tot_fwd_pkts: float = Field(..., ge=0, le=1, description="Total Forward Packets (normalized)")
    tot_bwd_pkts: float = Field(..., ge=0, le=1, description="Total Backward Packets (normalized)")
    totlen_fwd_pkts: float = Field(..., ge=0, le=1, description="Total Length Forward Packets (normalized)")
    fwd_pkt_len_max: float = Field(..., ge=0, le=1, description="Forward Packet Length Max (normalized)")
    fwd_pkt_len_min: float = Field(..., ge=0, le=1, description="Forward Packet Length Min (normalized)")
    fwd_pkt_len_mean: float = Field(..., ge=0, le=1, description="Forward Packet Length Mean (normalized)")
    fwd_pkt_len_std: float = Field(..., ge=0, le=1, description="Forward Packet Length Std (normalized)")
    bwd_pkt_len_max: float = Field(..., ge=0, le=1, description="Backward Packet Length Max (normalized)")
    bwd_pkt_len_min: float = Field(..., ge=0, le=1, description="Backward Packet Length Min (normalized)")
    bwd_pkt_len_mean: float = Field(..., ge=0, le=1, description="Backward Packet Length Mean (normalized)")
    bwd_pkt_len_std: float = Field(..., ge=0, le=1, description="Backward Packet Length Std (normalized)")
    flow_byts_s: float = Field(..., ge=0, le=1, description="Flow Bytes/s (normalized)")
    flow_pkts_s: float = Field(..., ge=0, le=1, description="Flow Packets/s (normalized)")
    flow_iat_mean: float = Field(..., ge=0, le=1, description="Flow IAT Mean (normalized)")
    flow_iat_std: float = Field(..., ge=0, le=1, description="Flow IAT Std (normalized)")
    flow_iat_max: float = Field(..., ge=0, le=1, description="Flow IAT Max (normalized)")
    fwd_iat_std: float = Field(..., ge=0, le=1, description="Forward IAT Std (normalized)")
    bwd_iat_tot: float = Field(..., ge=0, le=1, description="Backward IAT Total (normalized)")
    bwd_iat_mean: float = Field(..., ge=0, le=1, description="Backward IAT Mean (normalized)")
    bwd_iat_std: float = Field(..., ge=0, le=1, description="Backward IAT Std (normalized)")
    bwd_iat_max: float = Field(..., ge=0, le=1, description="Backward IAT Max (normalized)")
    bwd_iat_min: float = Field(..., ge=0, le=1, description="Backward IAT Min (normalized)")
    fwd_psh_flags: float = Field(..., ge=0, le=1, description="Forward PSH Flags (normalized)")
    bwd_psh_flags: float = Field(..., ge=0, le=1, description="Backward PSH Flags (normalized)")
    fwd_urg_flags: float = Field(..., ge=0, le=1, description="Forward URG Flags (normalized)")
    bwd_urg_flags: float = Field(..., ge=0, le=1, description="Backward URG Flags (normalized)")
    fwd_pkts_s: float = Field(..., ge=0, le=1, description="Forward Packets/s (normalized)")
    bwd_pkts_s: float = Field(..., ge=0, le=1, description="Backward Packets/s (normalized)")
    pkt_len_min: float = Field(..., ge=0, le=1, description="Packet Length Min (normalized)")
    pkt_len_max: float = Field(..., ge=0, le=1, description="Packet Length Max (normalized)")
    pkt_len_mean: float = Field(..., ge=0, le=1, description="Packet Length Mean (normalized)")
    pkt_len_std: float = Field(..., ge=0, le=1, description="Packet Length Std (normalized)")
    pkt_len_var: float = Field(..., ge=0, le=1, description="Packet Length Variance (normalized)")
    fin_flag_cnt: float = Field(..., ge=0, le=1, description="FIN Flag Count (normalized)")
    rst_flag_cnt: float = Field(..., ge=0, le=1, description="RST Flag Count (normalized)")
    psh_flag_cnt: float = Field(..., ge=0, le=1, description="PSH Flag Count (normalized)")
    ack_flag_cnt: float = Field(..., ge=0, le=1, description="ACK Flag Count (normalized)")
    urg_flag_cnt: float = Field(..., ge=0, le=1, description="URG Flag Count (normalized)")
    cwe_flag_count: float = Field(..., ge=0, le=1, description="CWE Flag Count (normalized)")
    down_up_ratio: float = Field(..., ge=0, le=1, description="Down/Up Ratio (normalized)")
    fwd_byts_b_avg: float = Field(..., ge=0, le=1, description="Forward Bytes/Bulk Avg (normalized)")
    fwd_pkts_b_avg: float = Field(..., ge=0, le=1, description="Forward Packets/Bulk Avg (normalized)")
    fwd_blk_rate_avg: float = Field(..., ge=0, le=1, description="Forward Bulk Rate Avg (normalized)")
    bwd_byts_b_avg: float = Field(..., ge=0, le=1, description="Backward Bytes/Bulk Avg (normalized)")
    bwd_pkts_b_avg: float = Field(..., ge=0, le=1, description="Backward Packets/Bulk Avg (normalized)")
    bwd_blk_rate_avg: float = Field(..., ge=0, le=1, description="Backward Bulk Rate Avg (normalized)")
    init_fwd_win_byts: float = Field(..., ge=0, le=1, description="Initial Forward Window Bytes (normalized)")
    init_bwd_win_byts: float = Field(..., ge=0, le=1, description="Initial Backward Window Bytes (normalized)")
    fwd_act_data_pkts: float = Field(..., ge=0, le=1, description="Forward Active Data Packets (normalized)")
    fwd_seg_size_min: float = Field(..., ge=0, le=1, description="Forward Segment Size Min (normalized)")
    active_mean: float = Field(..., ge=0, le=1, description="Active Mean (normalized)")
    active_std: float = Field(..., ge=0, le=1, description="Active Std (normalized)")
    active_max: float = Field(..., ge=0, le=1, description="Active Max (normalized)")
    active_min: float = Field(..., ge=0, le=1, description="Active Min (normalized)")
    idle_mean: float = Field(..., ge=0, le=1, description="Idle Mean (normalized)")
    idle_std: float = Field(..., ge=0, le=1, description="Idle Std (normalized)")

    class Config:
        schema_extra = {
            "example": {
                "dst_port": 0.0003,
                "protocol": 0.3529,
                "timestamp": 0.0432,
                "flow_duration": 0.0000,
                "tot_fwd_pkts": 0.0000,
                "tot_bwd_pkts": 0.0000,
                "totlen_fwd_pkts": 0.0000,
                "fwd_pkt_len_max": 0.0000,
                "fwd_pkt_len_min": 0.0000,
                "fwd_pkt_len_mean": 0.0000,
                "fwd_pkt_len_std": 0.0000,
                "bwd_pkt_len_max": 0.0000,
                "bwd_pkt_len_min": 0.0000,
                "bwd_pkt_len_mean": 0.0000,
                "bwd_pkt_len_std": 0.0000,
                "flow_byts_s": 0.0000,
                "flow_pkts_s": 0.5000,
                "flow_iat_mean": 0.0000,
                "flow_iat_std": 0.0000,
                "flow_iat_max": 0.0000,
                "fwd_iat_std": 0.0000,
                "bwd_iat_tot": 0.0000,
                "bwd_iat_mean": 0.0000,
                "bwd_iat_std": 0.0000,
                "bwd_iat_max": 0.0000,
                "bwd_iat_min": 0.0000,
                "fwd_psh_flags": 0.0000,
                "bwd_psh_flags": 0.0000,
                "fwd_urg_flags": 0.0000,
                "bwd_urg_flags": 0.0000,
                "fwd_pkts_s": 0.2500,
                "bwd_pkts_s": 0.5000,
                "pkt_len_min": 0.0000,
                "pkt_len_max": 0.0000,
                "pkt_len_mean": 0.0000,
                "pkt_len_std": 0.0000,
                "pkt_len_var": 0.0000,
                "fin_flag_cnt": 0.0000,
                "rst_flag_cnt": 0.0000,
                "psh_flag_cnt": 1.0000,
                "ack_flag_cnt": 0.0000,
                "urg_flag_cnt": 0.0000,
                "cwe_flag_count": 0.0000,
                "down_up_ratio": 0.0119,
                "fwd_byts_b_avg": 0.0000,
                "fwd_pkts_b_avg": 0.0000,
                "fwd_blk_rate_avg": 0.0000,
                "bwd_byts_b_avg": 0.0000,
                "bwd_pkts_b_avg": 0.0000,
                "bwd_blk_rate_avg": 0.0000,
                "init_fwd_win_byts": 0.4102,
                "init_bwd_win_byts": 0.0000,
                "fwd_act_data_pkts": 0.0000,
                "fwd_seg_size_min": 0.8333,
                "active_mean": 0.0000,
                "active_std": 0.0000,
                "active_max": 0.0000,
                "active_min": 0.0000,
                "idle_mean": 0.0000,
                "idle_std": 0.0000
            }
        }


class BatchFlowInput(BaseModel):
    """Batch of network flows for prediction."""
    flows: List[NetworkFlowInput] = Field(..., min_items=1, max_items=100)


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class RiskIndicator(BaseModel):
    """Single risk indicator with evidence."""
    indicator: str = Field(..., description="Description of the risk indicator")
    evidence: List[str] = Field(default=[], description="Evidence supporting this indicator")
    severity: Optional[str] = Field(default="medium", description="Severity level: critical, high, medium, low")


class BruteForceExplanation(BaseModel):
    """Explanation for brute force prediction - why the model flagged this network flow."""
    risk_indicators: List[RiskIndicator] = Field(default=[], description="List of risk indicators detected with evidence")
    top_features: Dict[str, float] = Field(default={}, description="Top features contributing to prediction (feature: value)")
    summary: str = Field(..., description="Human-readable summary of the prediction reasoning")
    total_indicators: Optional[int] = Field(default=0, description="Total number of indicators detected")

    class Config:
        schema_extra = {
            "example": {
                "risk_indicators": [
                    {
                        "indicator": "Tasa de paquetes backward extremadamente alta",
                        "evidence": ["Valor actual: 0.9500", "Valor normal: ~0.0080", "Ratio: 118.8x por encima de lo normal"],
                        "severity": "critical"
                    },
                    {
                        "indicator": "Duracion de flujo extremadamente corta",
                        "evidence": ["Duracion actual: 0.000100", "Duracion normal: ~0.50"],
                        "severity": "high"
                    }
                ],
                "top_features": {
                    "bwd_pkts_s": 0.95,
                    "flow_duration": 0.001,
                    "psh_flag_cnt": 0.85
                },
                "summary": "Ataque brute force detectado: 2 anomalias de red (1 criticas, 1 altas).",
                "total_indicators": 2
            }
        }


class PredictionResponse(BaseModel):
    """Response for single flow prediction."""
    prediction: int = Field(..., description="0 = Benign, 1 = Brute Force")
    prediction_label: str = Field(..., description="Human-readable prediction")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    probabilities: Dict[str, float] = Field(..., description="Class probabilities")
    explanation: BruteForceExplanation = Field(..., description="Explanation of why this prediction was made")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    model_name: str = Field(..., description="Model used for prediction")


class SingleBatchPrediction(BaseModel):
    """Single prediction in a batch response."""
    index: int = Field(..., description="Index in batch")
    prediction: int = Field(..., description="0 = Benign, 1 = Brute Force")
    prediction_label: str = Field(..., description="Human-readable prediction")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    probabilities: Dict[str, float] = Field(..., description="Class probabilities")
    explanation: BruteForceExplanation = Field(..., description="Explanation of why this prediction was made")


class BatchMetadata(BaseModel):
    """Metadata for batch prediction."""
    total_flows: int = Field(..., description="Total flows processed")
    processing_time_ms: float = Field(..., description="Total processing time")
    brute_force_count: int = Field(..., description="Number of brute force flows detected")
    benign_count: int = Field(..., description="Number of benign flows")


class BatchPredictionResponse(BaseModel):
    """Response for batch flow prediction."""
    predictions: List[SingleBatchPrediction]
    metadata: BatchMetadata


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Status message")
    model: str = Field(..., description="Loaded model name")
    version: str = Field(..., description="API version")


class ModelMetrics(BaseModel):
    """Model performance metrics."""
    f1_score: float = Field(..., ge=0, le=1)
    accuracy: float = Field(..., ge=0, le=1)
    precision: float = Field(..., ge=0, le=1)
    recall: float = Field(..., ge=0, le=1)
    roc_auc: float = Field(..., ge=0, le=1)


class ModelFeatures(BaseModel):
    """Model features information."""
    total: int = Field(..., description="Total number of features")
    feature_names: List[str] = Field(..., description="List of feature names")


class TrainingData(BaseModel):
    """Training data information."""
    total_samples: int
    train_samples: int
    test_samples: int
    balance: Dict[str, int] = Field(..., description="Class distribution")


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_name: str
    model_version: str
    training_date: str
    metrics: ModelMetrics
    features: ModelFeatures
    training_data: TrainingData
