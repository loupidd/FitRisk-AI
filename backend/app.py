from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FitRisk-AI",
    description="Diabetes Risk Prediction API using KNN (CDC BRFSS 2015)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Load artifacts =====
try:
    model = joblib.load("model_knn.pkl")
    scaler = joblib.load("scaler.pkl")

    with open("features.json", "r") as f:
        FEATURES = json.load(f)

except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")

# ===== Schemas =====
class PatientInput(BaseModel):
    data: dict


class PredictionResponse(BaseModel):
    prediction: int
    risk: str
    probability: float
    bmi: float
    bmi_category: str


# ===== BMI CATEGORY (WHO) =====
def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# ===== Health Check =====
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "model": "KNN Diabetes Classifier",
        "features": len(FEATURES)
    }


# ===== Prediction Endpoint =====
@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: PatientInput):
    try:
        missing = [f for f in FEATURES if f not in input_data.data]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing features: {missing}"
            )

        # Arrange input in correct order
        X = np.array([[input_data.data[f] for f in FEATURES]])

        # Scale
        X_scaled = scaler.transform(X)

        # Predict
        prediction = int(model.predict(X_scaled)[0])
        proba = float(model.predict_proba(X_scaled)[0][1])

        bmi_value = float(input_data.data["BMI"])
        bmi_cat = bmi_category(bmi_value)

        risk_label = "Diabetes Risk" if prediction == 1 else "No Diabetes"

        return {
            "prediction": prediction,
            "risk": risk_label,
            "probability": round(proba, 4),
            "bmi": round(bmi_value, 2),
            "bmi_category": bmi_cat
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
