# Hello World AMP

> **Level 4** — Cloudera AI AMP Beginner Series: Model Deployment

A hands-on reference AMP for learning Cloudera AI (CML) fundamentals. This prototype builds on Level 3 and demonstrates how to **train, register, build, and deploy a machine learning model** as a live REST API endpoint using CML's `create_model`, `build_model`, and `deploy_model` tasks.

---

## Overview

| Step | Task Type | Script | Purpose |
|---|---|---|---|
| 1 | `run_session` | `0_session-install-deps/install_deps.py` | Install & verify Python packages |
| 2 | `create_job` | — | Register the data report job |
| 3 | `run_job` | `1_job-data-report/report.py` | Generate data summary report |
| 4 | `run_session` | `3_model-usage-predictor/train.py` | **Train & save model.pkl** |
| 5 | `create_model` | `3_model-usage-predictor/predict.py` | **Register model serving function** |
| 6 | `build_model` | — | **Build model serving Docker image** |
| 7 | `deploy_model` | — | **Deploy model as REST API** |
| 8 | `start_application` | `2_app-streamlit/launch.py` | Launch Streamlit dashboard |

---

## What's New in Level 4

### Model Deployment: 3-Step Process

```
create_model  →  build_model  →  deploy_model
    │                │                │
Register the     Package project   Start REST
predict()        files + model.pkl  API endpoint
function         into Docker image
```

### The Model: Usage Score Predictor

A simple **Linear Regression** model (scikit-learn) that predicts a product's usage score from its active user count.

```
Input:   {"active_users": 350}
Output:  {"active_users": 350, "predicted_score": 87.5, "model": "LinearRegression"}
```

### Why train.py must run before build_model

```
Step 4: run_session → train.py
  └─ saves model.pkl to 3_model-usage-predictor/model.pkl

Step 6: build_model
  └─ packages the ENTIRE project directory into Docker image
       └─ model.pkl is included in the image ✓

Step 7: deploy_model
  └─ serving container has model.pkl at startup
       └─ predict() loads it on first request ✓
```

---

## Project Structure

```
sample-amp/
├── .project-metadata.yaml              # AMP runbook (8 tasks)
├── catalog.yaml                         # AMP Catalog registration
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
├── assets/
│   └── cover.png                        # Catalog tile image
├── 0_session-install-deps/
│   └── install_deps.py                  # Session: pip install + verify
├── 1_job-data-report/
│   └── report.py                        # Job: data processing → CSV + JSON
├── 2_app-streamlit/
│   ├── launch.py                        # Application launcher
│   └── app.py                           # Streamlit dashboard UI
└── 3_model-usage-predictor/             # ← NEW in Level 4
    ├── train.py                         # Session: train & save model.pkl
    ├── predict.py                       # Model serving function (REST API)
    └── model.pkl                        # Generated artifact (after train.py runs)
```

---

## AMP Task Flow

```
[AMP Deploy]
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 1: run_session                                  │
│ Script: 0_session-install-deps/install_deps.py       │
│  - pip install requests, pandas, streamlit,          │
│    scikit-learn                                      │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 2+3: create_job + run_job                       │
│ Script: 1_job-data-report/report.py                  │
│  - Generate data report → outputs/data_report.csv   │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 4: run_session   ← NEW                          │
│ Script: 3_model-usage-predictor/train.py             │
│  - Train LinearRegression on sample dataset          │
│  - Evaluate: R², MAE, per-product predictions        │
│  - Save model artifact → model.pkl                   │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 5: create_model   ← NEW                         │
│ Script: 3_model-usage-predictor/predict.py           │
│ Function: predict                                    │
│  - Register predict() as the REST API endpoint       │
│  - Model appears in CML Models menu                  │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 6: build_model   ← NEW                          │
│  - Package project files + model.pkl into image      │
│  - Build status visible in Models → Builds tab       │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 7: deploy_model   ← NEW                         │
│  - Deploy built image as a live REST API             │
│  - Status: Stopped → Starting → Running              │
│  - Test: Models → Usage Score Predictor → Test tab   │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 8: start_application                            │
│ Script: 2_app-streamlit/launch.py                    │
│  - Streamlit dashboard (unchanged from Level 3)      │
└─────────────────────────────────────────────────────┘
```

---

## Runtime

| Property | Value |
|---|---|
| Editor | PBJ Workbench |
| Kernel | Python 3.11 |
| Edition | Standard |
| CPU (all tasks) | 1–2 vCPU |
| Memory (all tasks) | 2–4 GB |

---

## Python Dependencies

```
requests==2.32.3
pandas==2.2.3
streamlit==1.41.1
scikit-learn==1.5.2        ← NEW in Level 4
```

---

## Environment Variables

### Level 2 — File I/O

| Variable | Default | Required | Description |
|---|---|---|---|
| `REPORT_OUTPUT_DIR` | `outputs` | No | Job output directory |
| `REPORT_NAME` | `data_report` | No | Report base filename |

### Level 3 — Dashboard Config

| Variable | Default | Required | Description |
|---|---|---|---|
| `DASHBOARD_TITLE` | _(none)_ | **Yes** | Dashboard header title |
| `SCORE_ALERT_THRESHOLD` | `80` | No | High performer threshold |
| `ENABLE_RAW_DATA_DOWNLOAD` | `true` | No | Show/hide CSV download |

---

## Model API Reference

### Endpoint

After `deploy_model` completes, the model is available as a REST endpoint managed by CML.

### Request

```bash
curl -X POST \
  https://<workspace-domain>/api/v1/predict \
  -H "Authorization: Bearer <model-access-key>" \
  -H "Content-Type: application/json" \
  -d '{"active_users": 350}'
```

### Response

```json
{
  "active_users": 350,
  "predicted_score": 87.5,
  "model": "LinearRegression"
}
```

### Test from CML UI

1. Go to **Models** in the left menu
2. Click **Usage Score Predictor**
3. Click the **Test** tab
4. Enter input JSON: `{"active_users": 350}`
5. Click **Test**

### How predict.py works

```python
_model = None                          # module-level cache

def _load_model():
    global _model
    if _model is None:                 # load once, reuse for all requests
        with open("3_model-usage-predictor/model.pkl", "rb") as f:
            _model = pickle.load(f)
    return _model

def predict(args):                     # CML calls this function on every request
    model = _load_model()
    active_users = int(args.get("active_users", 200))
    score = float(model.predict([[active_users]])[0])
    return {
        "active_users": active_users,
        "predicted_score": round(max(0.0, min(100.0, score)), 1),
        "model": type(model).__name__,
    }
```

---

## Streamlit Application Architecture

CML runs application scripts inside an **IPython kernel**. The launcher uses a single-line IPython `!` magic command:

```python
!streamlit run 2_app-streamlit/app.py --server.port $CDSW_APP_PORT --server.address 127.0.0.1 ...
```

`--server.address 127.0.0.1` binds Streamlit to the loopback interface, avoiding port conflict with CML's container proxy (PID 1) which binds to the external container IP on the same port.

---

## How to Deploy

1. Go to **AMPs** → find **Hello World AMP** → click **Deploy**
2. Set the required environment variable:
   - `DASHBOARD_TITLE` — e.g. `My Data Report Dashboard`
3. Click **Launch Project** — all 8 tasks will run sequentially
4. After completion:
   - **Models** menu → test the Usage Score Predictor REST API
   - **Applications** menu → open the Streamlit dashboard

---

## Learning Path

| Level | Title | Task Types Added |
|---|---|---|
| 0 | Hello World Session | `run_session` |
| 1 | Session + Batch Job | `create_job`, `run_job` |
| 2 | Session + Job + App | `start_application`, Streamlit |
| 3 | Advanced Env Vars | Required vars, type conversion |
| **4** | **Model Deployment** ← *this AMP* | `create_model`, `build_model`, `deploy_model` |
| 5 | GPU / LLM Serving | GPU Edition, Custom Runtime |

---

## Repository

[https://github.com/jshin-jackson/sample-amp](https://github.com/jshin-jackson/sample-amp)
