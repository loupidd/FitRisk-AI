from sklearn.metrics import classification_report, confusion_matrix
from data_loader import load_cdc
import joblib

df = load_cdc()

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

scaler = joblib.load("scaler.pkl")
model = joblib.load("model_knn.pkl")

X_scaled = scaler.transform(X)
y_pred = model.predict(X_scaled)

print(confusion_matrix(y, y_pred))
print(classification_report(y, y_pred))
