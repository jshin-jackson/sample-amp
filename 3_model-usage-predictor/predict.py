"""
Level 4 - CML Model Serving Function
======================================
This file is registered with CML via the 'create_model' task.
The 'predict' function becomes the REST API endpoint.

Design note:
  The model is trained at module import time (when the serving container starts).
  This avoids any dependency on model.pkl, which is a runtime-generated artifact
  that is NOT included in the git-committed project snapshot that build_model
  packages into the Docker image.

  For large models (e.g. LLMs), you would load a pre-trained artifact from
  object storage (S3/ADLS). For this learning example, inline training is used.

CML Model API:
  POST /api/v1/predict
  Authorization: Bearer <model-access-key>
  Content-Type: application/json

  Request body:  {"active_users": 350}
  Response body: {"active_users": 350, "predicted_score": 87.5, "model": "LinearRegression"}

Test from the CML UI:
  Models → Usage Score Predictor → Test tab → enter {"active_users": 350}
"""

from sklearn.linear_model import LinearRegression

# ── Train at module load time (runs once when the serving container starts) ────
# Same dataset as 1_job-data-report/report.py
_X = [[500], [320], [210], [180], [145]]   # active_users
_y = [98,    87,    76,    91,    83]       # usage_score

_model = LinearRegression().fit(_X, _y)


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
            predicted_score (float):  Predicted score, clamped to [0, 100].
            model (str):              Model class name for traceability.

    Example:
        Input:  {"active_users": 350}
        Output: {"active_users": 350, "predicted_score": 90.2, "model": "LinearRegression"}
    """
    active_users = int(args.get("active_users", 200))
    raw_score = float(_model.predict([[active_users]])[0])
    predicted_score = round(max(0.0, min(100.0, raw_score)), 1)

    return {
        "active_users": active_users,
        "predicted_score": predicted_score,
        "model": type(_model).__name__,
    }
