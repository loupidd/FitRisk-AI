from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from exercise_service import get_exercises_by_target
import logging
import random

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
try:
    model = joblib.load("model_knn.pkl")
    scaler = joblib.load("scaler.pkl")

    with open("features.json", "r") as f:
        FEATURES = json.load(f)
    
    logger.info(f"Model loaded: {type(model)}")
    logger.info(f"Number of features: {len(FEATURES)}")

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
    """
    score = 0
    
    # BMI contribution (0-6 points)
    if bmi < 18.5:
        score += 2
    elif bmi >= 25 and bmi < 28:
        score += 3
    elif bmi >= 28 and bmi < 30:
        score += 4
    elif bmi >= 30 and bmi < 35:
        score += 5
    elif bmi >= 35:
        score += 6
    
    # Other risk factors
    score += high_bp
    score += high_chol
    score += smoker
    score += (1 if phys_activity == 0 else 0)
    
    # Age factor
    if age >= 10:
        score += 2
    elif age >= 7:
        score += 1
    
    return score


def get_exercise_targets(bmi: float, prediction: int, risk_score: int) -> list:
    """
    Get exercise targets based on BMI, diabetes prediction, and risk score.
    Returns a list of targets to fetch exercises from.
    """
    targets = []
    
    # PRIORITY 1: Always include cardio for diabetes prevention
    targets.append("cardiovascular system")
    
    # PRIORITY 2: Based on BMI category
    if bmi < 18.5:
        # Underweight: Focus on strength building
        targets.extend(["upper back", "chest", "shoulders"])
    
    elif bmi >= 18.5 and bmi < 25:
        # Normal: Balanced full-body
        targets.extend(["abs", "glutes", "upper back"])
    
    elif bmi >= 25 and bmi < 30:
        # Overweight: Core + lower body
        targets.extend(["abs", "glutes", "hamstrings"])
    
    elif bmi >= 30 and bmi < 35:
        # Obese Class I: Focus on core stability and lower body
        targets.extend(["abs", "lower back", "glutes"])
    
    else:  # bmi >= 35
        # Obese Class II+: Low-impact, core focused
        targets.extend(["abs", "lower back", "glutes"])
    
    # PRIORITY 3: If high diabetes risk, add more cardio variety
    if prediction == 1 or risk_score >= 7:
        # Don't add duplicate cardiovascular system
        pass
    
    logger.info(f"Selected exercise targets for BMI {bmi}, risk {risk_score}: {targets}")
    
    return targets


async def fetch_varied_exercises(targets: list, total_count: int = 5) -> list:
    """
    Fetch exercises from multiple targets and mix them.
    """
    all_exercises = []
    exercises_per_target = max(2, total_count // len(targets))
    
    for target in targets:
        try:
            exercises = await get_exercises_by_target(target, limit=exercises_per_target)
            logger.info(f"Fetched {len(exercises)} exercises for target: {target}")
            all_exercises.extend(exercises)
        except Exception as e:
            logger.error(f"Failed to fetch exercises for {target}: {e}")
            continue
    
    # Shuffle to mix different targets
    random.shuffle(all_exercises)
    
    # Return exactly total_count exercises
    return all_exercises[:total_count]


def adapt_ui_input_to_brfss(raw: dict) -> dict:
    """
    Adapter layer with INTELLIGENT defaults based on risk profile.
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
    
    # Intelligent defaults based on risk score
    if risk_score >= 7:
        gen_hlth = 5
        fruits = 0
        veggies = 0
        stroke_risk = 1 if bmi >= 35 else 0
        heart_risk = 1 if (high_bp or high_chol or bmi >= 35) else 0
        diff_walk = 1 if bmi >= 32 else 0
    elif risk_score >= 5:
        gen_hlth = 4
        fruits = 0
        veggies = 1
        stroke_risk = 0
        heart_risk = 1 if (high_bp or high_chol) else 0
        diff_walk = 1 if bmi >= 30 else 0
    elif risk_score >= 3:
        gen_hlth = 3
        fruits = 1
        veggies = 1
        stroke_risk = 0
        heart_risk = 0
        diff_walk = 0
    else:
        gen_hlth = 2
        fruits = 1
        veggies = 1
        stroke_risk = 0
        heart_risk = 0
        diff_walk = 0
    
    logger.info(f"Applied defaults: GenHlth={gen_hlth}, DiffWalk={diff_walk}, HeartDisease={heart_risk}")

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


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "model": "KNN Diabetes Classifier",
        "features": len(FEATURES)
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PatientInput):
    try:
        # ---- validation ----
        brfss_data = adapt_ui_input_to_brfss(input_data.data)
        
        bmi_value = float(brfss_data["BMI"])
        risk_score = calculate_risk_score(
            bmi_value,
            brfss_data["HighBP"],
            brfss_data["HighChol"],
            brfss_data["Smoker"],
            brfss_data["PhysActivity"],
            brfss_data["Age"]
        )

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

        bmi_cat = bmi_category(bmi_value)
        risk_label = "Diabetes Risk" if prediction == 1 else "No Diabetes"

        # ---- Get varied exercise recommendations ----
        exercise_targets = get_exercise_targets(bmi_value, prediction, risk_score)
        exercises = []
        
        try:
            exercises = await fetch_varied_exercises(exercise_targets, total_count=5)
            logger.info(f"Retrieved {len(exercises)} total exercises from {len(exercise_targets)} targets")
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