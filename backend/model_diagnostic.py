import joblib
import json
import numpy as np

# Load the model artifacts
model = joblib.load("model_knn.pkl")
scaler = joblib.load("scaler.pkl")

with open("features.json", "r") as f:
    FEATURES = json.load(f)

print("=== MODEL DIAGNOSTIC ===")
print(f"Features expected: {FEATURES}")
print(f"Number of features: {len(FEATURES)}")
print(f"Model type: {type(model)}")
print(f"Scaler type: {type(scaler)}")

# Test cases to debug
test_cases = [
    {
        "name": "Healthy person",
        "data": {
            "HighBP": 0,
            "HighChol": 0,
            "CholCheck": 1,
            "BMI": 22.0,
            "Smoker": 0,
            "Stroke": 0,
            "HeartDiseaseorAttack": 0,
            "PhysActivity": 1,
            "Fruits": 1,
            "Veggies": 1,
            "HvyAlcoholConsump": 0,
            "AnyHealthcare": 1,
            "NoDocbcCost": 0,
            "GenHlth": 1,
            "MentHlth": 0,
            "PhysHlth": 0,
            "DiffWalk": 0,
            "Sex": 1,
            "Age": 3,
            "Education": 6,
            "Income": 8,
        }
    },
    {
        "name": "High risk person (BMI 45, high BP, high cholesterol)",
        "data": {
            "HighBP": 1,
            "HighChol": 1,
            "CholCheck": 1,
            "BMI": 45.0,
            "Smoker": 1,
            "Stroke": 0,
            "HeartDiseaseorAttack": 1,
            "PhysActivity": 0,
            "Fruits": 0,
            "Veggies": 0,
            "HvyAlcoholConsump": 1,
            "AnyHealthcare": 1,
            "NoDocbcCost": 1,
            "GenHlth": 5,
            "MentHlth": 30,
            "PhysHlth": 30,
            "DiffWalk": 1,
            "Sex": 1,
            "Age": 13,
            "Education": 1,
            "Income": 1,
        }
    },
    {
        "name": "Extreme high risk (BMI 60, all bad indicators)",
        "data": {
            "HighBP": 1,
            "HighChol": 1,
            "CholCheck": 1,
            "BMI": 60.0,
            "Smoker": 1,
            "Stroke": 1,
            "HeartDiseaseorAttack": 1,
            "PhysActivity": 0,
            "Fruits": 0,
            "Veggies": 0,
            "HvyAlcoholConsump": 1,
            "AnyHealthcare": 0,
            "NoDocbcCost": 1,
            "GenHlth": 5,
            "MentHlth": 30,
            "PhysHlth": 30,
            "DiffWalk": 1,
            "Sex": 1,
            "Age": 13,
            "Education": 1,
            "Income": 1,
        }
    }
]

print("\n=== TESTING PREDICTIONS ===\n")

for test in test_cases:
    print(f"Test: {test['name']}")
    print(f"BMI: {test['data']['BMI']}")
    print(f"High BP: {test['data']['HighBP']}, High Chol: {test['data']['HighChol']}")
    
    # Create feature array in correct order
    X = np.array([[test['data'][f] for f in FEATURES]])
    print(f"Input shape: {X.shape}")
    print(f"Input values: {X[0][:5]}... (first 5 features)")
    
    # Scale
    X_scaled = scaler.transform(X)
    print(f"Scaled values: {X_scaled[0][:5]}... (first 5 features)")
    
    # Predict
    prediction = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]
    
    print(f"Prediction: {prediction} (0=No Diabetes, 1=Diabetes)")
    print(f"Probability: {proba}")
    print(f"Diabetes probability: {proba[1]*100:.2f}%")
    print("-" * 60)
    print()

# Check model details
print("\n=== MODEL DETAILS ===")
if hasattr(model, 'n_neighbors'):
    print(f"K neighbors: {model.n_neighbors}")
if hasattr(model, 'classes_'):
    print(f"Classes: {model.classes_}")
if hasattr(model, 'get_params'):
    print(f"Model params: {model.get_params()}")

# Check scaler details
print("\n=== SCALER DETAILS ===")
if hasattr(scaler, 'mean_'):
    print(f"Scaler means (first 5): {scaler.mean_[:5]}")
if hasattr(scaler, 'scale_'):
    print(f"Scaler scales (first 5): {scaler.scale_[:5]}")