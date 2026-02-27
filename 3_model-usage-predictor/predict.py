"""
Level 4 - CML Model Serving Function
======================================
This file is registered with CML via the 'create_model' task.
The 'predict' function becomes the REST API endpoint.

CML Model API:
  POST /api/v1/predict
  Authorization: Bearer <model-access-key>
  Content-Type: application/json

  Request body:  {"active_users": 350}
  Response body: {"active_users": 350, "predicted_score": 87.5, "model": "LinearRegression"}

Test from the CML UI:
  Models → Usage Score Predictor → Test → enter {"active_users": 350}

Constraints:
  - Function name must match 'function' field in create_model task
  - Input/output must be JSON-serializable dicts
  - model.pkl must exist before build_model runs (created by train.py)
"""

import pickle

# ── Model loading (lazy, cached after first call) ──────────────────────────────

_MODEL_PATH = "3_model-usage-predictor/model.pkl"
_model = None


def _load_model():
    """Load the model from disk on first call, then cache in module-level variable."""
    global _model
    if _model is None:
        with open(_MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


# ── Serving function ───────────────────────────────────────────────────────────

def predict(args):
    """
    Predict usage score from active user count.

    Args:
        args (dict):
            active_users (int): Number of active users. Default: 200.

    Returns:
        dict:
            active_users (int):       Echo of input value.
            predicted_score (float):  Predicted usage score, clamped to [0, 100].
            model (str):              Model class name for traceability.

    Example:
        Input:  {"active_users": 350}
        Output: {"active_users": 350, "predicted_score": 87.5, "model": "LinearRegression"}
    """
    model = _load_model()

    active_users = int(args.get("active_users", 200))
    raw_score = float(model.predict([[active_users]])[0])
    predicted_score = round(max(0.0, min(100.0, raw_score)), 1)

    return {
        "active_users": active_users,
        "predicted_score": predicted_score,
        "model": type(model).__name__,
    }
