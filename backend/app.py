from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from exercise_service import get_exercises_by_target
import logging
from pathlib import Path


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model_knn.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
FEATURES_PATH = BASE_DIR / "features.json"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    with open(FEATURES_PATH, "r") as f:
        FEATURES = json.load(f)
    
    logger.info(f"Model loaded: {type(model)}")
    logger.info(f"Number of features: {len(FEATURES)}")
    logger.info(f"Artifacts loaded from: {BASE_DIR}")

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


def calculate_risk_score(bmi: float, high_bp: int, high_chol: int, smoker: int, 
                         phys_activity: int, age: int) -> int:
    """
    Calculate a risk score to determine appropriate defaults.
    Higher score = higher risk
    MORE AGGRESSIVE scoring for BMI
    """
    score = 0
    
    # BMI contribution (0-6 points) - INCREASED WEIGHT
    if bmi < 18.5:
        score += 2  # Underweight is also a risk
    elif bmi >= 25 and bmi < 28:
        score += 3  # Overweight
    elif bmi >= 28 and bmi < 30:
        score += 4  # High overweight
    elif bmi >= 30 and bmi < 35:
        score += 5  # Obese class I
    elif bmi >= 35:
        score += 6  # Obese class II+
    
    # Other risk factors (1 point each)
    score += high_bp
    score += high_chol
    score += smoker
    score += (1 if phys_activity == 0 else 0)
    
    # Age factor (0-2 points)
    if age >= 10:  # 65+ years
        score += 2
    elif age >= 7:  # 50+ years
        score += 1
    
    logger.info(f"Risk score breakdown: BMI={bmi}, HighBP={high_bp}, HighChol={high_chol}, Smoker={smoker}, PhysActivity={phys_activity}, Age={age} -> Score={score}")
    
    return score


def adapt_ui_input_to_brfss(raw: dict) -> dict:
    """
    Adapter layer with INTELLIGENT defaults based on risk profile.
    MORE AGGRESSIVE thresholds
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

    # Get user-provided risk factors
    high_bp = raw.get("HighBP", 0)
    high_chol = raw.get("HighChol", 0)
    smoker = raw.get("Smoker", 0)
    phys_activity = raw.get("PhysActivity", 0)
    age = raw.get("Age", 5)
    
    # Calculate risk score
    risk_score = calculate_risk_score(bmi, high_bp, high_chol, smoker, phys_activity, age)
    
    logger.info(f"Calculated risk score: {risk_score}/11 (BMI: {bmi})")
    
    # MORE AGGRESSIVE thresholds
    # GenHlth: 1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor
    if risk_score >= 7:  # Very high risk
        gen_hlth = 5  # Poor health
        fruits = 0
        veggies = 0
        stroke_risk = 1 if bmi >= 35 else 0
        heart_risk = 1 if (high_bp or high_chol or bmi >= 35) else 0
        diff_walk = 1 if bmi >= 32 else 0
    elif risk_score >= 5:  # High risk (BMI 30+ falls here)
        gen_hlth = 4  # Fair health
        fruits = 0
        veggies = 1
        stroke_risk = 0
        heart_risk = 1 if (high_bp or high_chol) else 0
        diff_walk = 1 if bmi >= 30 else 0
    elif risk_score >= 3:  # Moderate risk
        gen_hlth = 3  # Good health
        fruits = 1
        veggies = 1
        stroke_risk = 0
        heart_risk = 0
        diff_walk = 0
    else:  # Low risk
        gen_hlth = 2  # Very good health
        fruits = 1
        veggies = 1
        stroke_risk = 0
        heart_risk = 0
        diff_walk = 0
    
    logger.info(f"Applied defaults: GenHlth={gen_hlth}, Fruits={fruits}, Veggies={veggies}, DiffWalk={diff_walk}, HeartDisease={heart_risk}")

    return {
        "HighBP": high_bp,
        "HighChol": high_chol,
        "CholCheck": 1,
        "BMI": round(bmi, 2),
        "Smoker": smoker,
        "Stroke": stroke_risk,
        "HeartDiseaseorAttack": heart_risk,
        "PhysActivity": phys_activity,
        "Fruits": fruits,
        "Veggies": veggies,
        "HvyAlcoholConsump": 0,
        "AnyHealthcare": 1,
        "NoDocbcCost": 0,
        "GenHlth": gen_hlth,
        "MentHlth": 0,
        "PhysHlth": 0,
        "DiffWalk": diff_walk,
        "Sex": 1,
        "Age": age,
        "Education": 4,
        "Income": raw.get("Income", 5),
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
        
        logger.info(f"Final features for model: GenHlth={brfss_data['GenHlth']}, BMI={brfss_data['BMI']}, DiffWalk={brfss_data['DiffWalk']}, HeartDisease={brfss_data['HeartDiseaseorAttack']}")

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
        proba_array = model.predict_proba(X_scaled)[0]
        proba = float(proba_array[1])
        
        logger.info(f"MODEL OUTPUT: prediction={prediction}, diabetes_prob={proba:.4f} ({proba*100:.2f}%)")

        # ---- BMI logic ----
        bmi_value = float(brfss_data["BMI"])
        bmi_cat = bmi_category(bmi_value)

        risk_label = "Diabetes Risk" if prediction == 1 else "No Diabetes"

        # ---- Exercise target decision ----
        target = "cardiovascular system"

        # ---- ExerciseDB call with error handling ----
        exercises = []
        try:
            exercises = await get_exercises_by_target(target)
            logger.info(f"Retrieved {len(exercises)} exercises")
        except Exception as e:
            logger.error(f"Failed to fetch exercises: {e}")
            exercises = []

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
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))