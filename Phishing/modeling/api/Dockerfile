# Dockerfile for Phishing Detection API
# Build context: Phishing/modeling/ (not api/)
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

# Copy source code (feature engineering module)
COPY src/ /app/src/

# Copy the API code
COPY api/ /app/

# Copy the model, vectorizer, and model info
COPY outputs/models/best_model.pkl /app/outputs/models/best_model.pkl
COPY outputs/models/model_info.json /app/outputs/models/model_info.json
COPY outputs/features/tfidf_vectorizer.pkl /app/outputs/features/tfidf_vectorizer.pkl

# Set environment variables for model paths
ENV MODEL_PATH=/app/outputs/models/best_model.pkl \
    VECTORIZER_PATH=/app/outputs/features/tfidf_vectorizer.pkl \
    MODEL_INFO_PATH=/app/outputs/models/model_info.json

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
