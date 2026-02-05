import requests
import json

# Test the EXACT scenario from your screenshot
payload = {
    "data": {
        "height_cm": 158,
        "weight_kg": 75,
        "BMI": 30.04,
        "HighBP": 0,
        "HighChol": 0,
        "Smoker": 0,
        "PhysActivity": 1,
        "Age": 1,
        "Income": 2,
    }
}

print("=== TESTING YOUR EXACT INPUT ===")
print(f"Height: 158cm, Weight: 75kg")
print(f"BMI: 30.04 (Obese)")
print(f"Age: 18-24 years")
print(f"No high BP, No high cholesterol")
print(f"No smoking, Active lifestyle")
print()

try:
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n=== SERVER RESPONSE ===")
        print(json.dumps(result, indent=2))
        
        print(f"\n=== KEY RESULTS ===")
        print(f"Prediction: {result['prediction']} (0=Low, 1=High)")
        print(f"Probability: {result['probability']} = {result['probability']*100:.2f}%")
        print(f"Risk: {result['risk']}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Connection Error: {e}")
    print("\nMake sure your backend is running:")
    print("  cd backend")
    print("  uvicorn app:app --reload")