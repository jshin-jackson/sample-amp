"""
Level 4 - CML Model Serving Function
======================================
This file is registered with CML via the 'create_model' task.
The 'predict' function becomes the REST API endpoint.

Design note:
  The LinearRegression coefficients are pre-computed by train.py and hardcoded
  here. This eliminates ALL external dependencies (no sklearn, no pickle, no
  file I/O), ensuring the model serving Docker image always builds successfully.

  Coefficients were computed on the training dataset:
    X = active_users: [500, 320, 210, 180, 145]
    y = usage_score:  [ 98,  87,  76,  91,  83]

    coef      = 0.040258  (slope: score per active user)
    intercept = 76.09     (baseline score)

CML Model API:
  POST /api/v1/predict
  Authorization: Bearer <model-access-key>
  Content-Type: application/json

  Request body:  {"active_users": 350}
  Response body: {"active_users": 350, "predicted_score": 90.2, "model": "LinearRegression"}

Test from the CML UI:
  Models → Usage Score Predictor → Test tab → enter {"active_users": 350}
"""

# Pre-computed LinearRegression coefficients (no sklearn needed at serve time)
_COEF      = 0.040258   # slope
_INTERCEPT = 76.09      # intercept


def predict(args):
    """
    Predict usage score from active user count.

    Args:
        args (dict):
            active_users (int): Number of active users. Default: 200.

    Returns:
        dict:
            active_users (int):       Echo of input value.
            predicted_score (float):  Predicted score, clamped to [0, 100].
            model (str):              Model type name.

    Examples:
        {"active_users": 145}  →  {"predicted_score": 82.0, ...}
        {"active_users": 350}  →  {"predicted_score": 90.2, ...}
        {"active_users": 500}  →  {"predicted_score": 96.2, ...}
    """
    active_users = int(args.get("active_users", 200))
    raw_score = _COEF * active_users + _INTERCEPT
    predicted_score = round(max(0.0, min(100.0, raw_score)), 1)

    return {
        "active_users": active_users,
        "predicted_score": predicted_score,
        "model": "LinearRegression",
    }
