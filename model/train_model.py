import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "crop_model.pkl"
)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()

    return joblib.load(MODEL_PATH)
    
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "dataset" / "Crop_recommendationV2.csv"
MODEL_PATH = Path(__file__).parent / "crop_model.pkl"

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "soil_moisture",
    "soil_type",
    "sunlight_exposure",
    "wind_speed",
    "organic_matter"
]

NUMERIC_FEATURES = [
    "N", "P", "K", "temperature",
    "humidity", "ph", "rainfall",
    "soil_moisture", "sunlight_exposure",
    "wind_speed", "organic_matter"
]

CATEGORICAL_FEATURES = ["soil_type"]


def train_model():

    data = pd.read_csv(DATA_PATH)

    X = data[FEATURES].copy()
    y = data["label"].astype(str)

    X["soil_type"] = X["soil_type"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    preprocessing = ColumnTransformer(
        transformers=[
            ("soil", OneHotEncoder(handle_unknown="ignore"),
             CATEGORICAL_FEATURES)
        ],
        remainder="passthrough"
    )

    pipeline = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Model Training Completed!")
    print("Test Accuracy:", round(accuracy * 100, 2), "%")

    print(classification_report(y_test, predictions))

    # Train final model on the complete dataset
    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)

    print("Model saved successfully!")

    return accuracy


def load_model():

    if not MODEL_PATH.exists():
        train_model()

    return joblib.load(MODEL_PATH)


if __name__ == "__main__":
    train_model()

