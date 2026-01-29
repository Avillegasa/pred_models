"""
Quick API test script
"""
import requests
import json

API_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_predict_normal():
    """Test normal login prediction"""
    print("\n🔍 Testing normal login prediction...")
    data = {
        "user_id": "user123",
        "ip_address": "192.168.1.100",
        "country": "US",
        "region": "California",
        "city": "San Francisco",
        "browser": "Chrome 120.0",
        "os": "Windows 10",
        "device": "Desktop",
        "login_successful": 1,
        "is_attack_ip": 0,
        "asn": 15169,
        "rtt": 45.5
    }

    response = requests.post(f"{API_URL}/predict", json=data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Prediction: {result['prediction_label']}")
    print(f"   Risk Score: {result['risk_score']:.2f}%")
    print(f"   Confidence: {result['confidence']:.4f}")
    return response.status_code == 200

def test_predict_ato():
    """Test ATO prediction"""
    print("\n🔍 Testing Account Takeover prediction...")
    data = {
        "user_id": "user456",
        "ip_address": "89.46.23.10",
        "country": "RO",
        "region": "Bucharest",
        "city": "Bucharest",
        "browser": "Firefox 115.0",
        "os": "Linux",
        "device": "Desktop",
        "login_successful": 1,
        "is_attack_ip": 1,
        "asn": 9050,
        "rtt": 673.2
    }

    response = requests.post(f"{API_URL}/predict", json=data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Prediction: {result['prediction_label']}")
    print(f"   Risk Score: {result['risk_score']:.2f}%")
    print(f"   Confidence: {result['confidence']:.4f}")
    return response.status_code == 200

def test_model_info():
    """Test model info endpoint"""
    print("\n🔍 Testing model info endpoint...")
    response = requests.get(f"{API_URL}/model/info")
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Model: {result['model_name']}")
    print(f"   F1-Score: {result['metrics']['f1_score']:.4f}")
    print(f"   Recall: {result['metrics']['recall']:.4f}")
    print(f"   Features: {result['features']['total']}")
    return response.status_code == 200

if __name__ == "__main__":
    print("="*70)
    print("🚀 ACCOUNT TAKEOVER API - QUICK TEST")
    print("="*70)

    try:
        results = []
        results.append(("Health Check", test_health()))
        results.append(("Normal Login", test_predict_normal()))
        results.append(("ATO Login", test_predict_ato()))
        results.append(("Model Info", test_model_info()))

        print("\n" + "="*70)
        print("📊 TEST RESULTS")
        print("="*70)
        for name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"   {name}: {status}")

        all_passed = all(r[1] for r in results)
        if all_passed:
            print("\n✅ ALL TESTS PASSED!")
        else:
            print("\n❌ SOME TESTS FAILED")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("   Make sure the API is running on http://localhost:8001")
        print("   Run: uvicorn app:app --port 8001 --reload")
