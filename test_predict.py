"""
Test the Prediction API
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8001"

print("=" * 60)
print("ForgeML Prediction API Test")
print("=" * 60)

# Step 1: Check health
print("\n1️⃣ Checking API health...")
response = requests.get(f"{API_URL}/health")
print(f"   Status: {response.json()}")

# Step 2: List available models
print("\n2️⃣ Listing available models...")
response = requests.get(f"{API_URL}/models")
models = response.json()
print(f"   Available models: {models['models']}")
print(f"   Count: {models['count']}")

if models['count'] == 0:
    print("\n   ⚠️  No models found. Train a model first using the main ForgeML app!")
    print("      Go to http://localhost:8000 and train a model.")
    exit(1)

# Step 3: Load first model
model_to_load = models['models'][0]
print(f"\n3️⃣ Loading model: {model_to_load}...")
response = requests.post(f"{API_URL}/load/{model_to_load}")
print(f"   Response: {response.json()}")

# Step 4: Make predictions with sample data
print(f"\n4️⃣ Making predictions...")

test_cases = [
    {
        "name": "Test Case 1: Young, Low Salary",
        "data": {
            "Age": 25,
            "Salary": 35000,
            "Years_Experience": 1,
            "Performance_Score": 72
        }
    },
    {
        "name": "Test Case 2: Mid-level, Medium Salary",
        "data": {
            "Age": 35,
            "Salary": 50000,
            "Years_Experience": 8,
            "Performance_Score": 85
        }
    },
    {
        "name": "Test Case 3: Senior, High Salary",
        "data": {
            "Age": 45,
            "Salary": 70000,
            "Years_Experience": 15,
            "Performance_Score": 92
        }
    }
]

for test in test_cases:
    print(f"\n   {test['name']}")
    print(f"   Input: {test['data']}")
    
    response = requests.post(
        f"{API_URL}/predict",
        json={"data": test['data']},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result['prediction']}")
        if result.get('confidence'):
            print(f"   Confidence: {result['confidence']:.2%}")
    else:
        print(f"   Error: {response.json()}")

print("\n" + "=" * 60)
print("✅ Test complete!")
print("=" * 60)
