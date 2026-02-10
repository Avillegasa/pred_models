# Dockerfile for Account Takeover (ATO) Detection API
# Build context: Suspicious-Login-Activity/modeling/ (not api/)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better layer caching)
COPY api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (preprocessing and training modules)
COPY src/ /app/src/

# Copy the API code
COPY api/ /app/

# Copy the model, encoders, and metadata
COPY outputs/models/best_model.pkl /app/outputs/models/best_model.pkl
COPY outputs/models/model_info.json /app/outputs/models/model_info.json
COPY outputs/features/label_encoders.pkl /app/outputs/features/label_encoders.pkl

# Set environment variables for model paths
# The app.py resolves paths relative to api_dir, but env vars can be absolute
ENV MODEL_PATH=/app/outputs/models/best_model.pkl \
    ENCODERS_PATH=/app/outputs/features/label_encoders.pkl \
    THRESHOLD_PATH=/app/outputs/models/optimal_threshold.pkl \
    MODEL_INFO_PATH=/app/outputs/models/model_info.json

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/ || exit 1

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
