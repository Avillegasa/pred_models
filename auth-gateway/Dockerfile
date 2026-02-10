# Dockerfile for Auth Gateway
# Build context: auth-gateway/
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
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ /app/app/

# Create uploads and data directories
RUN mkdir -p /app/uploads /app/data

# Set environment variables for ML API URLs (Docker network)
# These can be overridden in docker-compose.yml
ENV PHISHING_API_URL=http://phishing-api:8000 \
    ATO_API_URL=http://ato-api:8001 \
    BRUTE_FORCE_API_URL=http://brute-force-api:8002 \
    DATABASE_URL=sqlite:///./data/auth_gateway.db \
    UPLOAD_DIR=/app/uploads

# Expose port
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
