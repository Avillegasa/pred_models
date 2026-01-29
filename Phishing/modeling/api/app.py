"""
Phishing Detection API - FastAPI Application
Provides REST endpoints for real-time phishing email detection.
"""
import os
import time
import logging
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models import (
    EmailInput,
    PredictionResponse,
    BatchEmailInput,
    BatchPredictionResponse,
    SingleBatchPrediction,
    BatchMetadata,
    HealthResponse,
    ModelInfoResponse,
    ModelMetrics,
    ModelFeatures,
    TrainingData
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
MODEL_PATH = os.getenv("MODEL_PATH", "../outputs/models/best_model.pkl")
VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "../outputs/features/tfidf_vectorizer.pkl")
MODEL_INFO_PATH = os.getenv("MODEL_INFO_PATH", "../outputs/models/model_info.json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Loads model and vectorizer once at startup.
    """
    # Startup
    logger.info("🚀 Starting Phishing Detection API...")

    # Resolve paths (relative to api/ directory)
    api_dir = os.path.dirname(os.path.abspath(__file__))
    model_path_abs = os.path.join(api_dir, MODEL_PATH)
    vectorizer_path_abs = os.path.join(api_dir, VECTORIZER_PATH)
    model_info_path_abs = os.path.join(api_dir, MODEL_INFO_PATH)

    # Check if files exist
    if not os.path.exists(model_path_abs):
        logger.error(f"❌ Model not found at: {model_path_abs}")
        raise FileNotFoundError(f"Model file not found: {model_path_abs}")

    if not os.path.exists(vectorizer_path_abs):
        logger.error(f"❌ Vectorizer not found at: {vectorizer_path_abs}")
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path_abs}")

    # Initialize predictor (singleton)
    try:
        predictor = get_predictor(
            model_path=model_path_abs,
            vectorizer_path=vectorizer_path_abs,
            model_info_path=model_info_path_abs if os.path.exists(model_info_path_abs) else None
        )
        logger.info(f"✅ Model loaded: {predictor.get_model_name()}")
        logger.info(f"✅ Features: {predictor.get_features_count()}")
        logger.info("✅ API ready to accept requests")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("🛑 Shutting down Phishing Detection API...")


# Initialize FastAPI app
app = FastAPI(
    title="Phishing Detection API",
    description="REST API for real-time phishing email detection using ML",
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
        message="Phishing Detection API",
        model=predictor.get_model_name(),
        version=API_VERSION
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_email(email: EmailInput) -> PredictionResponse:
    """
    Predict if a single email is phishing or legitimate.

    Args:
        email: Email data (sender, subject, body, etc.)

    Returns:
        Prediction result with confidence scores and metadata

    Raises:
        HTTPException: If prediction fails
    """
    try:
        logger.info(f"📧 Received prediction request from: {email.sender}")

        # Get predictor
        predictor = get_predictor()

        # Convert Pydantic model to dict
        email_data = {
            'sender': email.sender,
            'receiver': email.receiver if email.receiver else '',
            'subject': email.subject,
            'body': email.body,
            'urls': email.urls
        }

        # Predict
        result = predictor.predict_single(email_data)

        logger.info(
            f"✅ Prediction: {result['prediction_label']} "
            f"(confidence: {result['confidence']:.4f})"
        )

        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"❌ Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch(batch: BatchEmailInput) -> BatchPredictionResponse:
    """
    Predict multiple emails in a single request.
    More efficient than calling /predict multiple times.

    Args:
        batch: List of emails to predict

    Returns:
        List of predictions with metadata

    Raises:
        HTTPException: If batch prediction fails
    """
    try:
        logger.info(f"📧 Received batch prediction request: {len(batch.emails)} emails")

        # Get predictor
        predictor = get_predictor()

        # Convert Pydantic models to dicts
        emails_data = [
            {
                'sender': email.sender,
                'receiver': email.receiver if email.receiver else '',
                'subject': email.subject,
                'body': email.body,
                'urls': email.urls
            }
            for email in batch.emails
        ]

        # Batch predict
        predictions, processing_time_ms = predictor.predict_batch(emails_data)

        logger.info(
            f"✅ Batch prediction completed: {len(predictions)} emails "
            f"in {processing_time_ms:.2f}ms"
        )

        # Format response
        return BatchPredictionResponse(
            predictions=[SingleBatchPrediction(**pred) for pred in predictions],
            metadata=BatchMetadata(
                total_emails=len(predictions),
                processing_time_ms=round(processing_time_ms, 2)
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
    Includes metrics, features, and training data information.

    Returns:
        Model information and performance metrics
    """
    try:
        predictor = get_predictor()

        # Get model info
        metrics = predictor.get_metrics()
        feature_info = predictor.get_feature_info()
        training_info = predictor.get_training_info()

        return ModelInfoResponse(
            model_name=predictor.get_model_name(),
            model_version=API_VERSION,
            training_date=training_info.get("training_date", "2026-01-10"),
            metrics=ModelMetrics(
                f1_score=metrics.get("f1_score", 0.9909),
                accuracy=metrics.get("accuracy", 0.9898),
                precision=metrics.get("precision", 0.9891),
                recall=metrics.get("recall", 0.9927),
                roc_auc=metrics.get("roc_auc", 0.9990)
            ),
            features=ModelFeatures(
                total=feature_info.get("total_features", 1016),
                tfidf=feature_info.get("tfidf_features", 1000),
                numeric=feature_info.get("numeric_features", 16)
            ),
            training_data=TrainingData(
                total_samples=training_info.get("total_samples", 39154),
                train_samples=training_info.get("train_samples", 31323),
                test_samples=training_info.get("test_samples", 7831)
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
    port = int(os.getenv("PORT", 8000))
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
