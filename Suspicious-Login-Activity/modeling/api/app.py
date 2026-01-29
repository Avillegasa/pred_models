"""
Account Takeover Detection API - FastAPI Application
Provides REST endpoints for real-time account takeover detection.
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models import (
    LoginInput,
    PredictionResponse,
    BatchLoginInput,
    BatchPredictionResponse,
    HealthResponse,
    ModelInfoResponse,
    ModelMetrics,
    ModelFeatures,
    TrainingData,
    ThresholdInfo
)
from predictor import get_predictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
API_VERSION = "1.0.0"
MODEL_PATH = os.getenv("MODEL_PATH", "../outputs/models/gradient_boosting.pkl")
ENCODERS_PATH = os.getenv("ENCODERS_PATH", "../outputs/features/label_encoders.pkl")
THRESHOLD_PATH = os.getenv("THRESHOLD_PATH", "../outputs/models/optimal_threshold.pkl")
MODEL_INFO_PATH = os.getenv("MODEL_INFO_PATH", "../outputs/models/model_info.json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Loads model, encoders, and threshold once at startup.
    """
    # Startup
    logger.info("🚀 Starting Account Takeover Detection API...")

    # Resolve paths (relative to api/ directory)
    api_dir = os.path.dirname(os.path.abspath(__file__))
    model_path_abs = os.path.join(api_dir, MODEL_PATH)
    encoders_path_abs = os.path.join(api_dir, ENCODERS_PATH)
    threshold_path_abs = os.path.join(api_dir, THRESHOLD_PATH)
    model_info_path_abs = os.path.join(api_dir, MODEL_INFO_PATH)

    # Check if required files exist
    if not os.path.exists(model_path_abs):
        logger.error(f"❌ Model not found at: {model_path_abs}")
        raise FileNotFoundError(f"Model file not found: {model_path_abs}")

    if not os.path.exists(encoders_path_abs):
        logger.error(f"❌ Encoders not found at: {encoders_path_abs}")
        raise FileNotFoundError(f"Encoders file not found: {encoders_path_abs}")

    # Initialize predictor (singleton)
    try:
        predictor = get_predictor(
            model_path=model_path_abs,
            encoders_path=encoders_path_abs,
            threshold_path=threshold_path_abs if os.path.exists(threshold_path_abs) else None,
            model_info_path=model_info_path_abs if os.path.exists(model_info_path_abs) else None
        )
        logger.info(f"✅ Model loaded: {predictor.get_model_name()}")
        logger.info(f"✅ Features: {predictor.get_features_count()}")
        logger.info(f"✅ Threshold: {predictor.optimal_threshold:.4f}")
        logger.info("✅ API ready to accept requests")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("🛑 Shutting down Account Takeover Detection API...")


# Initialize FastAPI app
app = FastAPI(
    title="Account Takeover Detection API",
    description="REST API for real-time account takeover detection using ML",
    version=API_VERSION,
    lifespan=lifespan
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Global exception handler for unexpected errors."""
    logger.error(f"❌ Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing your request",
            "details": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None
        }
    )


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    Verifies that the API is running and model is loaded.
    """
    predictor = get_predictor()

    return HealthResponse(
        status="ok",
        message="Account Takeover Detection API",
        model=predictor.get_model_name(),
        version=API_VERSION
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_login(login: LoginInput) -> PredictionResponse:
    """
    Predict if a single login attempt is normal or account takeover.

    Args:
        login: Login data (user_id, ip_address, country, etc.)

    Returns:
        Prediction result with confidence scores, risk score, and metadata

    Raises:
        HTTPException: If prediction fails
    """
    try:
        logger.info(f"🔐 Received prediction request for user: {login.user_id}")

        # Get predictor
        predictor = get_predictor()

        # Convert Pydantic model to dict
        login_data = {
            'user_id': login.user_id,
            'ip_address': login.ip_address,
            'country': login.country,
            'region': login.region,
            'city': login.city,
            'browser': login.browser,
            'os': login.os,
            'device': login.device,
            'login_successful': login.login_successful,
            'is_attack_ip': login.is_attack_ip,
            'asn': login.asn,
            'rtt': login.rtt,
            'login_timestamp': login.login_timestamp
        }

        # Predict
        result = predictor.predict_single(login_data)

        logger.info(
            f"✅ Prediction: {result['prediction_label']} "
            f"(risk: {result['risk_score']:.2f}%, confidence: {result['confidence']:.4f})"
        )

        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"❌ Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch(batch: BatchLoginInput) -> BatchPredictionResponse:
    """
    Predict multiple login attempts in a single request.
    More efficient than calling /predict multiple times.

    Args:
        batch: List of logins to predict

    Returns:
        List of predictions with metadata

    Raises:
        HTTPException: If batch prediction fails
    """
    try:
        logger.info(f"🔐 Received batch prediction request: {len(batch.logins)} logins")

        # Get predictor
        predictor = get_predictor()

        # Convert Pydantic models to dicts
        logins_data = [
            {
                'user_id': login.user_id,
                'ip_address': login.ip_address,
                'country': login.country,
                'region': login.region,
                'city': login.city,
                'browser': login.browser,
                'os': login.os,
                'device': login.device,
                'login_successful': login.login_successful,
                'is_attack_ip': login.is_attack_ip,
                'asn': login.asn,
                'rtt': login.rtt,
                'login_timestamp': login.login_timestamp
            }
            for login in batch.logins
        ]

        # Batch predict
        predictions, processing_time_ms = predictor.predict_batch(logins_data)

        logger.info(
            f"✅ Batch prediction completed: {len(predictions)} logins "
            f"in {processing_time_ms:.2f}ms"
        )

        # Format response
        from models import SingleBatchPrediction, BatchMetadata

        return BatchPredictionResponse(
            predictions=[SingleBatchPrediction(**pred) for pred in predictions],
            metadata=BatchMetadata(
                total_logins=len(predictions),
                processing_time_ms=round(processing_time_ms, 2),
                model=predictor.get_model_name()
            )
        )

    except Exception as e:
        logger.error(f"❌ Batch prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def get_model_info() -> ModelInfoResponse:
    """
    Get information about the loaded model.
    Includes metrics, features, training data, and threshold information.

    Returns:
        Model information and performance metrics
    """
    try:
        predictor = get_predictor()

        # Get model info
        metrics = predictor.get_metrics()
        feature_info = predictor.get_feature_info()
        training_info = predictor.get_training_info()
        threshold_info = predictor.get_threshold_info()

        return ModelInfoResponse(
            model_name=predictor.get_model_name(),
            model_version=API_VERSION,
            training_date=training_info.get("training_date", "2026-01-15"),
            metrics=ModelMetrics(
                f1_score=metrics.get("f1_score", 0.7416),
                accuracy=metrics.get("accuracy", 0.9986),
                precision=metrics.get("precision", 0.7021),
                recall=metrics.get("recall", 0.7857),
                roc_auc=metrics.get("roc_auc", 0.9772),
                auc_pr=metrics.get("average_precision", 0.7955)
            ),
            features=ModelFeatures(
                total=feature_info.get("total_features", 35),
                temporal=feature_info.get("temporal_features", 7),
                behavioral=feature_info.get("behavioral_features", 8),
                aggregated=feature_info.get("aggregated_features", 10),
                categorical=feature_info.get("categorical_features", 6),
                numeric=feature_info.get("numeric_features", 4)
            ),
            training_data=TrainingData(
                total_samples=training_info.get("total_samples", 85141),
                train_samples=training_info.get("train_samples", 68112),
                test_samples=training_info.get("test_samples", 17029),
                ato_samples=42,  # From our training
                normal_samples=16987  # From our training
            ),
            threshold=ThresholdInfo(
                optimal_threshold=threshold_info.get("optimal_threshold", 0.5),
                default_threshold=threshold_info.get("default_threshold", 0.5),
                f1_improvement_pct=threshold_info.get("f1_improvement_pct", 0.0)
            )
        )

    except Exception as e:
        logger.error(f"❌ Failed to get model info: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )


# ============================================================================
# MAIN (for development only)
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))  # Port 8001 (Phishing uses 8000)
    reload = os.getenv("RELOAD", "true").lower() == "true"

    logger.info(f"🚀 Starting server on {host}:{port}")
    logger.info(f"📚 API docs available at: http://{host}:{port}/docs")

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
