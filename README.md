# Hello World AMP

> **Level 5** — Cloudera AI AMP Beginner Series: Model API Integration

A hands-on reference AMP for learning Cloudera AI (CML) fundamentals. This prototype builds on Level 4 and demonstrates how to **call a deployed CML model REST API from a Streamlit dashboard** for real-time predictions.

---

## Overview

| Step | Task Type | Script | Purpose |
|---|---|---|---|
| 1 | `run_session` | `0_session-install-deps/install_deps.py` | Install & verify Python packages |
| 2 | `create_job` | — | Register the data report job |
| 3 | `run_job` | `1_job-data-report/report.py` | Generate data summary report |
| 4 | `run_session` | `3_model-usage-predictor/train.py` | Train LinearRegression & log metrics |
| 5 | `run_session` | `3_model-usage-predictor/deploy_model.py` | Create, build & deploy model via cmlapi |
| 6 | `start_application` | `2_app-streamlit/launch.py` | **Launch Streamlit dashboard with live predictions** |

---

## What's New in Level 5

### Real-time Model Prediction in Dashboard

The Streamlit dashboard now includes a **live prediction panel** that calls the deployed model REST API:

```
사용자 슬라이더 입력 (active_users: 0 ~ 1000)
        ↓
Streamlit → POST MODEL_ENDPOINT_URL
        ↓  (Bearer MODEL_API_KEY)
Usage Score Predictor REST API
        ↓
Predicted usage_score → 대시보드 실시간 표시
```

### New Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MODEL_ENDPOINT_URL` | Optional | REST endpoint URL of the deployed model |
| `MODEL_API_KEY` | Optional | Access key for model authentication |

Find these values in **Models → Usage Score Predictor → Overview tab**.

### How to Enable Live Predictions

1. Go to **Applications → Data Report Dashboard → Edit**
2. Add environment variables:
   - `MODEL_ENDPOINT_URL`: copied from model Overview tab (Endpoint URL)
   - `MODEL_API_KEY`: copied from model Overview tab → Access Key
3. Restart the application
4. The prediction panel appears at the bottom of the dashboard

---

## What's New in Level 4

### Model Deployment via cmlapi

CML 2.0.55의 AMP `create_model`/`build_model`/`deploy_model` 태스크 버그로 인해, `cmlapi` SDK를 직접 사용해 모델 라이프사이클을 관리합니다:

```
deploy_model.py (run_session)
  ├─ 1. list_models()       → 기존 모델 확인
  ├─ 2. create_model()      → 모델 셸 생성
  ├─ 3. create_model_build() → Docker 이미지 빌드
  └─ 4. create_model_deployment() → REST API 배포
```

### The Model: Usage Score Predictor

A simple **Linear Regression** model that predicts a product's usage score from its active user count.

```
Input:   {"active_users": 350}
Output:  {"active_users": 350, "predicted_score": 87.5, "model": "LinearRegression"}
```

---

## Project Structure

```
sample-amp/
├── .project-metadata.yaml              # AMP runbook (6 tasks)
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
│   └── app.py                           # Streamlit dashboard + live predictions ← Level 5
└── 3_model-usage-predictor/
    ├── train.py                         # Session: train & log metrics
    ├── predict.py                       # Model serving function (REST API)
    └── deploy_model.py                  # Session: cmlapi create/build/deploy
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
│ Step 4: run_session                                  │
│ Script: 3_model-usage-predictor/train.py             │
│  - Train LinearRegression on sample dataset          │
│  - Log R², MAE evaluation metrics                    │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 5: run_session                                  │
│ Script: 3_model-usage-predictor/deploy_model.py      │
│  - cmlapi: create model + build Docker image         │
│  - cmlapi: deploy as REST API endpoint               │
│  - Status: Deployed ✓                                │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 6: start_application                            │
│ Script: 2_app-streamlit/launch.py                    │
│  - Streamlit dashboard with live prediction panel    │
│  - Calls model REST API on button click  ← Level 5  │
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
scikit-learn==1.5.2
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

### Level 5 — Model API Integration

| Variable | Default | Required | Description |
|---|---|---|---|
| `MODEL_ENDPOINT_URL` | _(none)_ | No | REST endpoint URL of deployed model |
| `MODEL_API_KEY` | _(none)_ | No | Model access key for authentication |

---

## Model API Reference

### Endpoint

After deployment, the model is available as a REST endpoint managed by CML.

### Request

```bash
curl -X POST \
  https://<workspace-domain>/model/<model-id>/predict \
  -H "Authorization: Bearer <model-access-key>" \
  -H "Content-Type: application/json" \
  -d '{"request": {"active_users": 350}}'
```

### Response

```json
{
  "response": {
    "active_users": 350,
    "predicted_score": 87.5,
    "model": "LinearRegression"
  }
}
```

### Test from CML UI

1. Go to **Models** in the left menu
2. Click **Usage Score Predictor**
3. Click the **Test** tab
4. Enter input JSON: `{"active_users": 350}`
5. Click **Test**

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
3. Optionally set model API variables (can be added later):
   - `MODEL_ENDPOINT_URL` — from Models → Usage Score Predictor → Overview
   - `MODEL_API_KEY` — from Models → Usage Score Predictor → Overview → Access Key
4. Click **Launch Project** — all 6 tasks will run sequentially
5. After completion:
   - **Models** menu → verify Usage Score Predictor is Deployed
   - **Applications** menu → open the Streamlit dashboard
   - Scroll to the **Real-time Prediction** panel and test with the slider

---

## Learning Path

| Level | Title | Task Types Added |
|---|---|---|
| 0 | Hello World Session | `run_session` |
| 1 | Session + Batch Job | `create_job`, `run_job` |
| 2 | Session + Job + App | `start_application`, Streamlit |
| 3 | Advanced Env Vars | Required vars, type conversion |
| 4 | Model Deployment | `cmlapi` create/build/deploy |
| **5** | **Model API Integration** ← *this AMP* | REST API call from Streamlit |
| 6 | GPU / LLM Serving | GPU Edition, Custom Runtime |

---

## Repository

[https://github.com/jshin-jackson/sample-amp](https://github.com/jshin-jackson/sample-amp)
