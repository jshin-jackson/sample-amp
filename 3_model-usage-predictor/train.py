"""
Level 4 - Model Training Script
================================
This script runs as a CML Session task (run_session).
It must complete BEFORE the create_model / build_model / deploy_model tasks,
because build_model packages model.pkl into the serving image.

What it does:
  - Trains a simple Linear Regression model (active_users → usage_score)
  - Evaluates the model with R² and MAE metrics
  - Saves the trained artifact to 3_model-usage-predictor/model.pkl
"""

import os
import pickle
from datetime import datetime

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


OUTPUT_DIR = "3_model-usage-predictor"
MODEL_FILE = os.path.join(OUTPUT_DIR, "model.pkl")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def get_training_data():
    """
    Returns the same dataset used in the data report job.
    Each row: (active_users) → usage_score
    """
    products = ["Cloudera AI", "CML Sessions", "CML Jobs", "CML Models", "CML Apps"]
    X = np.array([[500], [320], [210], [180], [145]], dtype=float)
    y = np.array([98, 87, 76, 91, 83], dtype=float)
    return X, y, products


def train(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model


def evaluate(model, X, y, products):
    y_pred = model.predict(X)
    print()
    print("=" * 55)
    print("  MODEL EVALUATION  (LinearRegression)")
    print("=" * 55)
    print(f"  R² Score     : {r2_score(y, y_pred):.4f}")
    print(f"  MAE          : {mean_absolute_error(y, y_pred):.2f}")
    print(f"  Coefficient  : {model.coef_[0]:.6f}")
    print(f"  Intercept    : {model.intercept_:.4f}")
    print()
    print("  Predictions vs Actual:")
    print(f"  {'Product':<20} {'Actual':>6} {'Predicted':>10} {'Error':>8}")
    print("  " + "-" * 48)
    for p, actual, pred in zip(products, y, y_pred):
        err = pred - actual
        print(f"  {p:<20} {actual:>6.0f} {pred:>10.1f} {err:>+8.1f}")
    print("=" * 55)
    print()


def save_model(model):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    log(f"Model artifact saved → {MODEL_FILE}")


def main():
    log("Training session started")

    log("Loading training data...")
    X, y, products = get_training_data()
    log(f"Dataset: {len(X)} samples, feature: active_users, target: usage_score")

    log("Training LinearRegression model...")
    model = train(X, y)

    evaluate(model, X, y, products)

    log("Saving model artifact...")
    save_model(model)

    log("Training completed successfully.")
    log(f"Next step: create_model → build_model → deploy_model will package {MODEL_FILE}")


if __name__ == "__main__":
    main()
