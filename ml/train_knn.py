from data_loader import load_cdc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib

df = load_cdc()

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

scaler = joblib.load("scaler.pkl")
X_scaled = scaler.transform(X)

model = KNeighborsClassifier(
    n_neighbors=7,
    weights="distance"
)

model.fit(X_scaled, y)

joblib.dump(model, "model_knn.pkl")
