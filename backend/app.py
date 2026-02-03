from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from exercise_service import get_exercises_by_target


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
    bmi_description: str
    exercises: list

def adapt_ui_input_to_brfss(raw: dict) -> dict:
    """
    Adapter layer:
    - Accepts dirty / partial frontend input
    - Outputs FULL BRFSS feature dict (ordered later)
    """

    # ---- BMI handling ----
    if "BMI" in raw:
        bmi = float(raw["BMI"])
    else:
        height_cm = raw.get("height_cm")
        weight_kg = raw.get("weight_kg")
        if height_cm and weight_kg:
            h_m = height_cm / 100
            bmi = weight_kg / (h_m ** 2)
        else:
            raise ValueError("BMI or height/weight required")

    return {
        "HighBP": raw.get("HighBP", 0),
        "HighChol": raw.get("HighChol", 0),
        "CholCheck": raw.get("CholCheck", 1),
        "BMI": round(bmi, 2),
        "Smoker": raw.get("Smoker", 0),
        "Stroke": raw.get("Stroke", 0),
        "HeartDiseaseorAttack": raw.get("HeartDiseaseorAttack", 0),
        "PhysActivity": raw.get("PhysActivity", 0),
        "Fruits": raw.get("Fruits", 1),
        "Veggies": raw.get("Veggies", 1),
        "HvyAlcoholConsump": raw.get("HvyAlcoholConsump", 0),
        "AnyHealthcare": raw.get("AnyHealthcare", 1),
        "NoDocbcCost": raw.get("NoDocbcCost", 0),
        "GenHlth": raw.get("GenHlth", 3),
        "MentHlth": raw.get("MentHlth", 0),
        "PhysHlth": raw.get("PhysHlth", 0),
        "DiffWalk": raw.get("DiffWalk", 0),
        "Sex": raw.get("Sex", 1),
        "Age": raw.get("Age"),
        "Education": raw.get("Education", 4),
        "Income": raw.get("Income"),
    }



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


def bmi_description(bmi: float) -> str:
    if bmi < 18.5:
        return "Your body weight is below normal. You may need to increase nutritional intake."
    elif bmi < 25:
        return "Your body weight is in the normal range. Maintain your current lifestyle."
    elif bmi < 30:
        return "Your body weight is above normal. Regular exercise is recommended."
    else:
        return "Your body weight is in the obese range. Lifestyle changes are strongly recommended."


# ===== ExerciseDB VALID TARGET MAPPING =====
BMI_DIABETES_TO_TARGET = {
    "UNDERWEIGHT": "cardiovascular system",
    "NORMAL": "cardiovascular system",
    "OVERWEIGHT": "upper legs",
    "OBESE": "lower legs",
    "DIABETES": "lower back"
}


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
async def predict(input_data: PatientInput):
    try:
        # ---- validation ----
        brfss_data = adapt_ui_input_to_brfss(input_data.data)

        missing = [f for f in FEATURES if f not in brfss_data]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing features after adaptation: {missing}"
            )

        # ---- ML inference ----
        X = np.array([[brfss_data[f] for f in FEATURES]])
        X_scaled = scaler.transform(X)

        prediction = int(model.predict(X_scaled)[0])
        proba = float(model.predict_proba(X_scaled)[0][1])

        # ---- BMI logic ----
        bmi_value = float(brfss_data["BMI"])
        bmi_cat = bmi_category(bmi_value)

        risk_label = "Diabetes Risk" if prediction == 1 else "No Diabetes"

        # ---- Exercise target decision (STRICT & VALID) ----
        if prediction == 1:
            target = BMI_DIABETES_TO_TARGET["DIABETES"]
        elif bmi_cat == "Underweight":
            target = BMI_DIABETES_TO_TARGET["UNDERWEIGHT"]
        elif bmi_cat == "Normal":
            target = BMI_DIABETES_TO_TARGET["NORMAL"]
        elif bmi_cat == "Overweight":
            target = BMI_DIABETES_TO_TARGET["OVERWEIGHT"]
        else:
            target = BMI_DIABETES_TO_TARGET["OBESE"]

        # ---- ExerciseDB call ----
        exercises = await get_exercises_by_target(target)

        return {
            "prediction": prediction,
            "risk": risk_label,
            "probability": round(proba, 4),
            "bmi": round(bmi_value, 2),
            "bmi_category": bmi_cat,
            "bmi_description": bmi_description(bmi_value),
            "exercises": exercises
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
