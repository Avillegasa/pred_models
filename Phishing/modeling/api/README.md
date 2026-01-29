# Phishing Detection API

REST API for real-time phishing email detection using Machine Learning.

## Description

This API provides endpoints to classify emails as **legitimate** or **phishing** using a trained Gradient Boosting model with 99.09% F1-Score.

**Key Features:**
- Single email prediction via `POST /predict`
- Batch prediction via `POST /predict/batch`
- Model performance metrics via `GET /model/info`
- Automatic request validation with Pydantic
- Interactive API documentation at `/docs`
- Production-ready FastAPI implementation

**Model Performance:**
- F1-Score: **99.09%**
- Accuracy: **98.98%**
- Precision: **98.91%**
- Recall: **99.27%**
- ROC-AUC: **99.90%**

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Trained model files (automatically available in `../outputs/`)

### Setup

1. Navigate to the API directory:
```bash
cd Phishing/modeling/api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create environment file:
```bash
cp .env.example .env
# Edit .env if needed (default paths should work)
```

---

## Running the API

### Development Mode (with auto-reload)

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Alternative:** Run directly with Python:
```bash
python app.py
```

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access Points

Once running, access:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

---

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Verify API is running and model is loaded.

**Response:**
```json
{
  "status": "ok",
  "message": "Phishing Detection API",
  "model": "Gradient Boosting",
  "version": "1.0.0"
}
```

**Example (curl):**
```bash
curl http://localhost:8000/
```

---

### 2. Predict Single Email

**Endpoint:** `POST /predict`

**Description:** Classify a single email as legitimate or phishing.

**Request Body:**
```json
{
  "sender": "user@example.com",
  "receiver": "admin@company.com",
  "subject": "Urgent: Verify your account",
  "body": "Click here to verify your account immediately...",
  "urls": 1
}
```

**Fields:**
- `sender` (required): Email sender address
- `receiver` (optional): Email receiver address
- `subject` (required): Email subject line
- `body` (required): Email body content
- `urls` (optional): 0 or 1, indicates URL presence (default: 0)

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Phishing",
  "confidence": 0.9927,
  "probability_legitimate": 0.0073,
  "probability_phishing": 0.9927,
  "metadata": {
    "model": "Gradient Boosting",
    "features_count": 1016,
    "timestamp": "2026-01-10T15:30:45.123Z",
    "processing_time_ms": 45.2
  }
}
```

**Interpretation:**
- `prediction`: 0 = Legitimate, 1 = Phishing
- `confidence`: Probability of the predicted class (0.0 - 1.0)
- `probability_phishing`: Specific probability of being phishing

**Example (curl):**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "boss@company.com",
    "subject": "Meeting tomorrow",
    "body": "Let us discuss the project at 10am",
    "urls": 0
  }'
```

**Example (Python):**
```python
import requests

email = {
    "sender": "urgent@suspicious.com",
    "subject": "URGENT: Verify your account NOW",
    "body": "Click here to verify: http://phishing.com",
    "urls": 1
}

response = requests.post(
    "http://localhost:8000/predict",
    json=email
)

result = response.json()
print(f"Prediction: {result['prediction_label']}")
print(f"Confidence: {result['confidence']:.4f}")
```

---

### 3. Batch Prediction

**Endpoint:** `POST /predict/batch`

**Description:** Classify multiple emails in a single request.

**Request Body:**
```json
{
  "emails": [
    {
      "sender": "colleague@work.com",
      "subject": "Code review",
      "body": "Can you review my PR? Thanks!"
    },
    {
      "sender": "scam@fake.com",
      "subject": "You won $1M!",
      "body": "Click here to claim your prize!"
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "email_index": 0,
      "prediction": 0,
      "prediction_label": "Legitimate",
      "confidence": 0.9856
    },
    {
      "email_index": 1,
      "prediction": 1,
      "prediction_label": "Phishing",
      "confidence": 0.9943
    }
  ],
  "metadata": {
    "total_emails": 2,
    "processing_time_ms": 78.5
  }
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {
        "sender": "hr@company.com",
        "subject": "Benefits enrollment",
        "body": "Please complete enrollment by Friday"
      }
    ]
  }'
```

---

### 4. Model Information

**Endpoint:** `GET /model/info`

**Description:** Get model performance metrics and details.

**Response:**
```json
{
  "model_name": "Gradient Boosting",
  "model_version": "1.0.0",
  "training_date": "2026-01-10",
  "metrics": {
    "f1_score": 0.9909,
    "accuracy": 0.9898,
    "precision": 0.9891,
    "recall": 0.9927,
    "roc_auc": 0.9990
  },
  "features": {
    "total": 1016,
    "tfidf": 1000,
    "numeric": 16
  },
  "training_data": {
    "total_samples": 39154,
    "train_samples": 31323,
    "test_samples": 7831
  }
}
```

**Example (curl):**
```bash
curl http://localhost:8000/model/info
```

---

## Testing

### Automated Tests

Run the automated test suite:

```bash
# Start the API first (in another terminal)
uvicorn app:app --reload

# Run tests
python test_api.py
```

The test suite validates:
1. Health check endpoint
2. Legitimate email prediction
3. Phishing email prediction
4. Batch prediction
5. Validation errors (missing fields)
6. Validation errors (invalid format)
7. Model info endpoint

**Expected output:**
```
✅ ALL TESTS PASSED (7/7)
```

### Manual Testing with Postman

1. **Import Collection:**
   - Open Postman
   - Create new collection: "Phishing Detection API"
   - Set base URL variable: `http://localhost:8000`

2. **Test Endpoints:**
   - GET `/` - Health check
   - POST `/predict` - Single prediction
   - POST `/predict/batch` - Batch prediction
   - GET `/model/info` - Model information

3. **Example Payloads:**

**Legitimate Email:**
```json
{
  "sender": "manager@company.com",
  "subject": "Weekly team meeting",
  "body": "Please join our weekly sync at 2pm",
  "urls": 0
}
```

**Phishing Email:**
```json
{
  "sender": "noreply@suspicious-bank.com",
  "subject": "URGENT: Account verification required",
  "body": "Your account will be suspended. Click here now: http://fake-bank.com",
  "urls": 1
}
```

---

## Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **422 Unprocessable Entity**: Validation error (missing/invalid fields)
- **500 Internal Server Error**: Server or model error

### Error Response Format

```json
{
  "error": "Validation Error",
  "message": "Field 'subject' is required",
  "details": { ... }
}
```

---

## Architecture

### Directory Structure

```
api/
├── app.py              # FastAPI application (main entry point)
├── models.py           # Pydantic schemas for validation
├── predictor.py        # ML prediction logic
├── requirements.txt    # Dependencies
├── test_api.py         # Automated tests
├── .env.example        # Environment variables example
└── README.md           # This file
```

### Data Flow

```
1. Request → FastAPI → Pydantic Validation
2. Validated Data → PhishingPredictor
3. Feature Engineering (1,016 features)
   - Text features (subject/body length, word count)
   - TF-IDF vectorization (1,000 features)
   - Metadata (sender domain, URL presence)
   - Sentiment scores
4. Model Prediction → Probabilities
5. Format Response → JSON
6. Response → Client
```

**Processing Time:** ~50-100ms per email

---

## Configuration

### Environment Variables

Create `.env` file (or use defaults):

```env
# Model paths (relative to api/ directory)
MODEL_PATH=../outputs/models/best_model.pkl
VECTORIZER_PATH=../outputs/features/tfidf_vectorizer.pkl
MODEL_INFO_PATH=../outputs/models/model_info.json

# Server configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Logging
LOG_LEVEL=INFO
DEBUG=false
```

---

## Troubleshooting

### API won't start

**Error:** `Model file not found`
**Solution:** Ensure model files exist:
```bash
ls -lh ../outputs/models/best_model.pkl
ls -lh ../outputs/features/tfidf_vectorizer.pkl
```

**Error:** `Port 8000 already in use`
**Solution:** Use different port:
```bash
uvicorn app:app --port 8001
```

### Predictions seem incorrect

**Issue:** Model classifies emails unexpectedly
**Explanation:** Model is trained on CEAS_08 dataset. Different email patterns may behave differently.
**Solution:** Retrain model with your specific dataset if needed.

### Slow predictions

**Issue:** Response time > 500ms
**Solution:**
- Use batch endpoint for multiple emails
- Increase workers in production: `--workers 4`
- Check system resources (RAM, CPU)

### Import errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
**Solution:**
```bash
pip install -r requirements.txt
```

### Feature engineering errors

**Error:** `TF-IDF vocabulary mismatch`
**Cause:** Vectorizer file corrupted or wrong version
**Solution:** Retrain model or restore vectorizer from backup

---

## Production Deployment

### Recommendations

1. **Use production server:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Enable HTTPS:**
   - Use reverse proxy (Nginx, Traefik)
   - Add SSL certificates

3. **Add authentication:**
   - API keys
   - OAuth2
   - JWT tokens

4. **Rate limiting:**
   - Protect against abuse
   - Use middleware or API gateway

5. **Monitoring:**
   - Log predictions
   - Track latency
   - Monitor error rates

6. **CORS configuration:**
   - Update `allow_origins` in `app.py` to specific domains
   - Remove wildcard `*` in production

---

## Performance

### Benchmark Results

**Single Prediction:**
- Average time: ~50ms
- Features: 1,016 per email
- Memory: ~500MB (model loaded)

**Batch Prediction (10 emails):**
- Average time: ~200ms
- Throughput: ~50 emails/second

**Model Accuracy:**
- F1-Score: 99.09%
- False Positive Rate: 1.39%
- False Negative Rate: 0.73%

---

## API Documentation

### Interactive Documentation

Access automatically generated docs:
- **Swagger UI**: http://localhost:8000/docs
  - Try endpoints interactively
  - See request/response schemas
  - Download OpenAPI spec

- **ReDoc**: http://localhost:8000/redoc
  - Cleaner documentation view
  - Better for reading

---

## Support

For issues or questions:
1. Check this README
2. Review API docs at `/docs`
3. Check logs for error details
4. Verify model files exist
5. Review `CLAUDE.md` in project root

---

## Version History

**v1.0.0** (2026-01-10)
- Initial release
- Gradient Boosting model (99.09% F1)
- Four endpoints: health, predict, batch, model info
- Automated testing
- Complete documentation

---

## License

This API is part of the Phishing Email Detection research project.
For academic and research purposes.

---

**Model Ready for Production Deployment** 🚀
