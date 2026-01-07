from data_loader import load_cdc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

df = load_cdc()

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

scaler = joblib.load("scaler.pkl")
X_scaled = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(
    n_neighbors=7,
    weights="distance"
)

model.fit(X_train, y_train)

joblib.dump(model, "model_knn.pkl")

print("KNN model trained and saved.")
