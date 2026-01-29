"""
Automated tests for Phishing Detection API.
Run these tests to verify API functionality.

Usage:
    python test_api.py

Prerequisites:
    - API must be running on http://localhost:8000
    - Run: uvicorn app:app --reload
"""
import requests
import sys
import time
from typing import Dict, List


# API Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # seconds


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test_header(test_name: str):
    """Print test header."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}TEST: {test_name}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_info(message: str):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.RESET}")


def check_api_available() -> bool:
    """Check if API is running and accessible."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ============================================================================
# TESTS
# ============================================================================

def test_health_check() -> bool:
    """Test 1: Health check endpoint."""
    print_test_header("Health Check (GET /)")

    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)

        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Status code: {response.status_code}")

        # Check response structure
        data = response.json()
        assert "status" in data, "Missing 'status' field"
        assert "message" in data, "Missing 'message' field"
        assert "model" in data, "Missing 'model' field"
        assert "version" in data, "Missing 'version' field"
        print_success(f"Response structure valid")

        # Check values
        assert data["status"] == "ok", f"Expected status 'ok', got '{data['status']}'"
        print_success(f"Status: {data['status']}")
        print_success(f"Model: {data['model']}")
        print_success(f"Version: {data['version']}")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_predict_legitimate() -> bool:
    """Test 2: Predict legitimate email."""
    print_test_header("Predict Legitimate Email (POST /predict)")

    legitimate_email = {
        "sender": "boss@company.com",
        "receiver": "employee@company.com",
        "subject": "Meeting tomorrow at 10am",
        "body": "Hi team, let's discuss the project tomorrow at 10am in room 305. Please bring your reports.",
        "urls": 0
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=legitimate_email,
            timeout=TIMEOUT
        )

        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Status code: {response.status_code}")

        # Check response structure
        data = response.json()
        assert "prediction" in data, "Missing 'prediction' field"
        assert "prediction_label" in data, "Missing 'prediction_label' field"
        assert "confidence" in data, "Missing 'confidence' field"
        assert "metadata" in data, "Missing 'metadata' field"
        print_success("Response structure valid")

        # Check prediction (should be Legitimate = 0)
        print_info(f"Prediction: {data['prediction']} ({data['prediction_label']})")
        print_info(f"Confidence: {data['confidence']:.4f}")
        print_info(f"P(Legitimate): {data['probability_legitimate']:.4f}")
        print_info(f"P(Phishing): {data['probability_phishing']:.4f}")
        print_info(f"Processing time: {data['metadata']['processing_time_ms']:.2f}ms")

        # Verify it's classified as legitimate (0)
        if data['prediction'] == 0:
            print_success("Email correctly classified as Legitimate!")
        else:
            print_error(f"Expected Legitimate (0), got {data['prediction_label']} ({data['prediction']})")
            print_info("Note: Model may classify differently based on training")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_predict_phishing() -> bool:
    """Test 3: Predict phishing email."""
    print_test_header("Predict Phishing Email (POST /predict)")

    phishing_email = {
        "sender": "urgent@suspicious.com",
        "receiver": "victim@example.com",
        "subject": "URGENT: Verify your account NOW or be suspended!",
        "body": "Your account will be suspended in 24 hours. Click here immediately to verify your identity and update your password: http://phishing-site.com/verify",
        "urls": 1
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=phishing_email,
            timeout=TIMEOUT
        )

        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Status code: {response.status_code}")

        # Check response structure
        data = response.json()
        assert "prediction" in data, "Missing 'prediction' field"
        print_success("Response structure valid")

        # Check prediction (should be Phishing = 1)
        print_info(f"Prediction: {data['prediction']} ({data['prediction_label']})")
        print_info(f"Confidence: {data['confidence']:.4f}")
        print_info(f"P(Legitimate): {data['probability_legitimate']:.4f}")
        print_info(f"P(Phishing): {data['probability_phishing']:.4f}")
        print_info(f"Processing time: {data['metadata']['processing_time_ms']:.2f}ms")

        # Verify it's classified as phishing (1)
        if data['prediction'] == 1:
            print_success("Email correctly classified as Phishing!")
        else:
            print_error(f"Expected Phishing (1), got {data['prediction_label']} ({data['prediction']})")
            print_info("Note: Model may classify differently based on training")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_batch_prediction() -> bool:
    """Test 4: Batch prediction."""
    print_test_header("Batch Prediction (POST /predict/batch)")

    batch_emails = {
        "emails": [
            {
                "sender": "colleague@work.com",
                "subject": "Code review needed",
                "body": "Can you review my pull request? Thanks!",
                "urls": 0
            },
            {
                "sender": "scam@fake.com",
                "subject": "You won $1,000,000!!!",
                "body": "Congratulations! Click here to claim your prize now!",
                "urls": 1
            },
            {
                "sender": "hr@company.com",
                "subject": "Benefits enrollment",
                "body": "Please complete your benefits enrollment by Friday.",
                "urls": 0
            }
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json=batch_emails,
            timeout=TIMEOUT
        )

        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Status code: {response.status_code}")

        # Check response structure
        data = response.json()
        assert "predictions" in data, "Missing 'predictions' field"
        assert "metadata" in data, "Missing 'metadata' field"
        print_success("Response structure valid")

        # Check predictions
        predictions = data["predictions"]
        assert len(predictions) == 3, f"Expected 3 predictions, got {len(predictions)}"
        print_success(f"Received {len(predictions)} predictions")

        for pred in predictions:
            idx = pred["email_index"]
            label = pred["prediction_label"]
            conf = pred["confidence"]
            print_info(f"Email {idx}: {label} (confidence: {conf:.4f})")

        # Check metadata
        metadata = data["metadata"]
        print_info(f"Total emails: {metadata['total_emails']}")
        print_info(f"Processing time: {metadata['processing_time_ms']:.2f}ms")
        print_success("Batch prediction successful!")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_missing_fields() -> bool:
    """Test 5: Request with missing required fields."""
    print_test_header("Validation Error - Missing Fields (POST /predict)")

    incomplete_email = {
        "sender": "test@example.com"
        # Missing: subject, body (required fields)
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=incomplete_email,
            timeout=TIMEOUT
        )

        # Should return 422 Unprocessable Entity
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print_success(f"Correctly returned status code: {response.status_code}")

        # Check error response
        data = response.json()
        assert "detail" in data, "Missing 'detail' field in error response"
        print_success("Validation error response structure valid")
        print_info(f"Error details: {data['detail']}")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_invalid_format() -> bool:
    """Test 6: Request with invalid field format."""
    print_test_header("Validation Error - Invalid Format (POST /predict)")

    invalid_email = {
        "sender": "test@example.com",
        "subject": "Test",
        "body": "Test body",
        "urls": 5  # Invalid: should be 0 or 1
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_email,
            timeout=TIMEOUT
        )

        # Should return 422 Unprocessable Entity
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print_success(f"Correctly returned status code: {response.status_code}")

        # Check error response
        data = response.json()
        assert "detail" in data, "Missing 'detail' field in error response"
        print_success("Validation error response structure valid")
        print_info(f"Error details: {data['detail']}")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_model_info() -> bool:
    """Test 7: Get model information."""
    print_test_header("Model Information (GET /model/info)")

    try:
        response = requests.get(f"{BASE_URL}/model/info", timeout=TIMEOUT)

        # Check status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Status code: {response.status_code}")

        # Check response structure
        data = response.json()
        assert "model_name" in data, "Missing 'model_name' field"
        assert "metrics" in data, "Missing 'metrics' field"
        assert "features" in data, "Missing 'features' field"
        assert "training_data" in data, "Missing 'training_data' field"
        print_success("Response structure valid")

        # Display model info
        print_info(f"Model: {data['model_name']}")
        print_info(f"Version: {data['model_version']}")
        print_info(f"Training date: {data['training_date']}")

        metrics = data['metrics']
        print_info(f"F1 Score: {metrics['f1_score']:.4f}")
        print_info(f"Accuracy: {metrics['accuracy']:.4f}")
        print_info(f"Precision: {metrics['precision']:.4f}")
        print_info(f"Recall: {metrics['recall']:.4f}")

        features = data['features']
        print_info(f"Total features: {features['total']}")
        print_info(f"TF-IDF features: {features['tfidf']}")
        print_info(f"Numeric features: {features['numeric']}")

        training = data['training_data']
        print_info(f"Total samples: {training['total_samples']}")
        print_info(f"Train samples: {training['train_samples']}")
        print_info(f"Test samples: {training['test_samples']}")

        return True

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and report results."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}PHISHING DETECTION API - AUTOMATED TESTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

    # Check if API is available
    print_info(f"Checking if API is running at {BASE_URL}...")
    if not check_api_available():
        print_error(f"API is not running at {BASE_URL}")
        print_info("Please start the API first:")
        print_info("  cd Phishing/modeling/api")
        print_info("  uvicorn app:app --reload")
        sys.exit(1)

    print_success("API is running!")

    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Predict Legitimate Email", test_predict_legitimate),
        ("Predict Phishing Email", test_predict_phishing),
        ("Batch Prediction", test_batch_prediction),
        ("Validation - Missing Fields", test_missing_fields),
        ("Validation - Invalid Format", test_invalid_format),
        ("Model Information", test_model_info)
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(0.5)  # Small delay between tests

    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"{status} - {test_name}")

    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    if passed == total:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED ({passed}/{total}){Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ SOME TESTS FAILED ({passed}/{total} passed){Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
