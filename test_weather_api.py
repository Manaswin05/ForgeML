"""
Test Weather Prediction API
"""

import requests

API_BASE = "http://localhost:8000"

print("=" * 70)
print("🌤️  Weather Prediction API Test")
print("=" * 70)

# Test cases
test_cases = [
    {
        "name": "Warm & Dry",
        "params": {"temperature": 25, "humidity": 40}
    },
    {
        "name": "Hot & Humid",
        "params": {"temperature": 35, "humidity": 80}
    },
    {
        "name": "Cold & Dry",
        "params": {"temperature": 5, "humidity": 30}
    },
    {
        "name": "Cold & Humid",
        "params": {"temperature": 10, "humidity": 75}
    },
    {
        "name": "Moderate",
        "params": {"temperature": 20, "humidity": 60}
    }
]

print("\n📍 Testing: GET /api/weather?temperature=X&humidity=Y\n")

for i, test in enumerate(test_cases, 1):
    print(f"{i}️⃣  Test: {test['name']}")
    print(f"   Input: Temperature={test['params']['temperature']}°C, Humidity={test['params']['humidity']}%")
    
    try:
        response = requests.get(
            f"{API_BASE}/api/weather",
            params=test['params'],
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success!")
            print(f"   Output: Feels Like = {result['feels_like']}")
            print(f"   Full Response: {result}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Make sure server is running at {API_BASE}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()

print("=" * 70)
print("✅ Test Complete!")
print("=" * 70)

print("\n📝 Usage Examples:\n")
print("curl 'http://localhost:8000/api/weather?temperature=25&humidity=60'")
print("\nPython:")
print("  import requests")
print("  r = requests.get('http://localhost:8000/api/weather', params={'temperature': 25, 'humidity': 60})")
print("  print(r.json())")
