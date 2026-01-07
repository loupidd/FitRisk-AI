from data_loader import load_cdc
from sklearn.preprocessing import StandardScaler
import joblib
import json

df = load_cdc()

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "scaler.pkl")
print("Scaler saved.")

FEATURES = X.columns.tolist()

with open("features.json", "w") as f:
    json.dump(FEATURES, f)

print("Features saved:", FEATURES)
