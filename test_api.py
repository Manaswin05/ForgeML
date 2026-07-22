"""Quick test script to verify ForgeML API is working"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_homepage():
    """Test if homepage loads"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Homepage failed: {response.status_code}"
    assert "ForgeML" in response.text
    print("✓ Homepage loads successfully")

def test_api_docs():
    """Test if API docs are available"""
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200, f"Docs failed: {response.status_code}"
    print("✓ API docs available at /docs")

def test_upload():
    """Test dataset upload"""
    with open("sample_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    assert response.status_code == 200, f"Upload failed: {response.status_code}"
    data = response.json()
    assert data["status"] == "success"
    print(f"✓ Dataset uploaded: {data['info']['rows']} rows, {data['info']['columns']} columns")
    return data

def test_profile():
    """Test profile endpoint"""
    response = requests.get(f"{BASE_URL}/api/profile")
    assert response.status_code == 200, f"Profile failed: {response.status_code}"
    data = response.json()
    print(f"✓ Profile loaded: {data['duplicates']} duplicates found")
    return data

def test_training():
    """Test model training"""
    training_config = {
        "target_column": "Promoted",
        "feature_columns": ["Age", "Salary", "Years_Experience", "Performance_Score"],
        "model_type": "random_forest",
        "cleaning_operations": {
            "drop_missing_values": True,
            "fill_numeric_mean": False,
            "fill_numeric_median": False,
            "one_hot_encode": False,
            "standard_scale": True
        },
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 10
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/train", json=training_config)
    assert response.status_code == 200, f"Training failed: {response.status_code} - {response.text}"
    data = response.json()
    print(f"✓ Model trained successfully!")
    print(f"  - Task Type: {data['task_type']}")
    print(f"  - Model Type: {data['model_type']}")
    print(f"  - Metrics: {list(data['metrics'].keys())}")
    return data

def test_export():
    """Test model export"""
    response = requests.post(f"{BASE_URL}/api/export")
    assert response.status_code == 200, f"Export failed: {response.status_code}"
    data = response.json()
    print(f"✓ Model exported: {data['filename']}")
    return data

def test_analysis():
    """Test dataset analysis"""
    analysis_request = {
        "target_column": "Promoted",
        "feature_columns": ["Age", "Salary"]
    }
    response = requests.post(f"{BASE_URL}/api/analysis", json=analysis_request)
    assert response.status_code == 200, f"Analysis failed: {response.status_code} - {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert "pairplot" in data
    assert "model_comparisons" in data
    print("✓ Analysis generated successfully")
    return data

if __name__ == "__main__":
    print("Testing ForgeML API...\n")
    
    try:
        test_homepage()
        test_api_docs()
        test_upload()
        test_profile()
        test_analysis()
        test_training()
        test_export()
        
        print("\n✓ All tests passed! ForgeML is ready to use.")
        print("\nAccess the application at: http://localhost:8000")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure the server is running: python backend/app.py")
