from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import json
import os


app = FastAPI()

# load model & scaler
model = joblib.load("../ml/model_knn.pkl")
scaler = joblib.load("../ml/scaler.pkl")

# load feature order
with open("../ml/features.json") as f:
    FEATURES = json.load(f)

# ---------- INPUT SCHEMA ----------
class PatientInput(BaseModel):
    data: dict  # flexible, we validate manually


# ---------- PREDICT ----------
@app.post("/predict")
def predict(input: PatientInput):

    X = []
    for feature in FEATURES:
        if feature not in input.data:
            return {
                "error": f"Missing feature: {feature}"
            }
        X.append(input.data[feature])

    X = np.array(X).reshape(1, -1)

    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]

    return {
        "prediction": int(prediction),
        "risk": "Diabetes" if prediction == 1 else "No Diabetes"
    }
