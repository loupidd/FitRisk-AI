FitRisk-AI

Diabetes Risk Prediction using Machine Learning (KNN) and FastAPI

Overview

FitRisk-AI is an end-to-end machine learning application designed to predict the risk of diabetes based on health-related indicators.
The project uses real-world public health data from the Centers for Disease Control and Prevention (CDC) and demonstrates a complete machine learning pipeline, from data preprocessing and model training to backend API deployment.

This project is intended for academic purposes, machine learning practice, and portfolio demonstration.

Dataset

Source: CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015

Provider: Kaggle

Dataset name: cdc-diabetes-health-indicators

The dataset contains health and lifestyle indicators collected through surveys, including:

Blood pressure and cholesterol indicators

Body Mass Index (BMI)

Smoking and alcohol consumption

Physical activity and diet

General, mental, and physical health

Demographic information such as age, education, and income

Target variable:

Diabetes_binary

0: No diabetes

1: Diabetes

The dataset is non-synthetic and reflects real population health data.

Machine Learning Approach

Algorithm: K-Nearest Neighbors (KNN)

Preprocessing: StandardScaler

Features: 21 health indicators

Target: Binary diabetes classification

Model Evaluation

The trained model achieved the following performance on the test set:

Accuracy: 97%

Precision (diabetes class): 0.93

Recall (diabetes class): 0.81

F1-score (diabetes class): 0.87

These results indicate a strong balance between overall accuracy and sensitivity to diabetes cases.

Project Structure
FitRisk-AI/
├── ml/
│ ├── data_loader.py
│ ├── preprocess.py
│ ├── model_knn.py
│ ├── evaluate.py
│ ├── model_knn.pkl
│ ├── scaler.pkl
│ └── features.json
│
├── backend/
│ └── app.py
│
├── frontend/
│ ├── index.html
│ └── script.js
│
├── requirements.txt
└── README.md

Installation

Install all required dependencies using:

pip install -r requirements.txt

Model Training and Evaluation

To preprocess the data, train the model, and evaluate performance:

cd ml
python3 preprocess.py
python3 model_knn.py
python3 evaluate.py

Trained artifacts such as the scaler, model, and feature list are saved locally for reuse during inference.

Backend API

The backend is built using FastAPI and provides an endpoint for real-time diabetes risk prediction.

Run the API server
cd backend
uvicorn app:app --reload

API documentation will be available at:

http://127.0.0.1:8000/docs

API Usage
Endpoint
POST /predict

Request Body Example
{
"data": {
"HighBP": 1,
"HighChol": 1,
"CholCheck": 1,
"BMI": 28,
"Smoker": 0,
"Stroke": 0,
"HeartDiseaseorAttack": 0,
"PhysActivity": 1,
"Fruits": 1,
"Veggies": 1,
"HvyAlcoholConsump": 0,
"AnyHealthcare": 1,
"NoDocbcCost": 0,
"GenHlth": 3,
"MentHlth": 0,
"PhysHlth": 0,
"DiffWalk": 0,
"Sex": 1,
"Age": 9,
"Education": 4,
"Income": 6
}
}

Response Example
{
"prediction": 0,
"risk": "No Diabetes"
}

Use Cases

Academic machine learning coursework

AI and data science portfolio project

Backend machine learning deployment practice

Health data analysis experimentation

Disclaimer

This project is for educational and research purposes only.
It is not intended to be used as a medical diagnostic tool.

Author

Rangga Ahmad Fauzan
Machine Learning and Software Engineering Enthusiast
