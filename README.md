# Hello World AMP

> **Level 2** — Cloudera AI AMP Beginner Series: Session + Job + Streamlit Application

A hands-on reference AMP for learning Cloudera AI (CML) fundamentals. This prototype walks through three core CML task types in sequence — dependency installation, batch job execution, and a live interactive web dashboard — using only Python, pandas, and Streamlit.

---

## Overview

| Task Type | Script | Purpose |
|---|---|---|
| `run_session` | `0_session-install-deps/install_deps.py` | Install & verify Python packages |
| `create_job` + `run_job` | `1_job-data-report/report.py` | Generate a data summary report |
| `start_application` | `2_app-streamlit/launch.py` | Launch the Streamlit dashboard |

---

## Project Structure

```
sample-amp/
├── .project-metadata.yaml              # AMP runbook — defines all tasks, runtime, and env vars
├── catalog.yaml                         # AMP Catalog registration metadata
├── README.md                            # This file
├── requirements.txt                     # Python dependencies (requests, pandas, streamlit)
├── assets/
│   └── cover.png                        # Catalog tile image
├── 0_session-install-deps/
│   └── install_deps.py                  # Session: pip install + package verification
├── 1_job-data-report/
│   └── report.py                        # Job: pandas data processing → CSV + JSON output
└── 2_app-streamlit/
    ├── launch.py                        # Application launcher (IPython magic entry point)
    └── app.py                           # Streamlit dashboard UI
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
│  - pip install -r requirements.txt                   │
│  - Verify: requests, pandas, streamlit               │
│  - Print runtime environment info                    │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 2: create_job                                   │
│  - Registers "Data Report Job" in CML Jobs menu      │
│  - Script: 1_job-data-report/report.py               │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 3: run_job                                      │
│  - Executes the registered job                       │
│  - Creates sample dataset with pandas                │
│  - Computes summary statistics                       │
│  - Saves outputs/data_report.csv                     │
│  - Saves outputs/data_report.json                    │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│ Step 4: start_application                            │
│ Script: 2_app-streamlit/launch.py                    │
│  - Reads outputs/ files produced by the Job          │
│  - Displays KPI metrics, bar chart, category table   │
│  - Accessible at https://hello-world-amp.{domain}    │
└─────────────────────────────────────────────────────┘
```

---

## Runtime

| Property | Value |
|---|---|
| Editor | PBJ Workbench |
| Kernel | Python 3.11 |
| Edition | Standard |
| CPU (all tasks) | 2 vCPU |
| Memory (all tasks) | 4 GB |

---

## Python Dependencies

```
requests==2.32.3
pandas==2.2.3
streamlit==1.41.1
```

---

## Environment Variables

| Variable | Default | Required | Description |
|---|---|---|---|
| `REPORT_OUTPUT_DIR` | `outputs` | No | Directory where the job saves report files |
| `REPORT_NAME` | `data_report` | No | Base filename for the generated report (no extension) |

---

## Output Files

| File | Format | Description |
|---|---|---|
| `outputs/data_report.csv` | CSV | Full sample dataset (20 rows × 5 columns) |
| `outputs/data_report.json` | JSON | Summary statistics (mean, max, top product, etc.) |

---

## Dashboard Features

| Section | Description |
|---|---|
| **KPI Metrics** | Total Users, Average Score, Top Product, Product Count |
| **Bar Chart** | Usage Score per product (Altair chart) |
| **Category Table** | Active User count grouped by category |
| **Raw Data** | Expandable full dataset with CSV download button |

If the job output files are not found, the dashboard displays a friendly warning with instructions to run the Data Report Job first.

---

## Streamlit Application Architecture

CML runs application scripts inside an **IPython kernel**. The launcher (`launch.py`) uses a single-line IPython `!` magic command to start Streamlit as a shell subprocess:

```python
!streamlit run 2_app-streamlit/app.py --server.port $CDSW_APP_PORT --server.address 127.0.0.1 ...
```

**Key design decisions:**

| Option | Value | Reason |
|---|---|---|
| `--server.address` | `127.0.0.1` | CML's container proxy (PID 1) binds to the external container IP on `CDSW_APP_PORT`. Binding Streamlit to the loopback interface avoids port conflict. |
| `--server.port` | `$CDSW_APP_PORT` | CML's internal proxy forwards traffic to this port (`8100` by default). |
| `--server.enableCORS` | `false` | CML's proxy handles CORS; Streamlit-level CORS would block dashboard access. |
| `--server.enableXsrfProtection` | `false` | Requests proxied through CML do not carry Streamlit's XSRF tokens. |
| `--server.headless` | `true` | Suppresses browser launch and email prompts in the container environment. |
| `!` (single line) | — | CML's `python.dedent` parser crashes on `!` magic with backslash line continuations. The entire command must be on one line. |

---

## How to Deploy

### From the AMP Catalog
1. In Cloudera AI, go to **AMPs** in the left navigation panel.
2. Find **Hello World AMP** and click **Deploy**.
3. Optionally override `REPORT_OUTPUT_DIR` or `REPORT_NAME`.
4. Click **Launch Project** and wait for all 4 tasks to complete.
5. Go to **Applications** menu → open **Data Report Dashboard**.

### Redeployment Notes
- If you need to redeploy the Application task, always **Delete** the existing Application first (do not just Restart).
- This ensures a clean container with no orphaned processes from previous runs.

---

## Learning Path

This AMP is part of a progressive series:

| Level | Title | Task Types Added |
|---|---|---|
| 0 | Hello World Session | `run_session` |
| 1 | Session + Batch Job | `create_job`, `run_job` |
| **2** | **Session + Job + App** ← *this AMP* | `start_application` |
| 3 | User Configuration | `environment_variables` (advanced) |
| 4 | Model Deployment | `create_model`, `build_model`, `deploy_model` |
| 5 | GPU / LLM Serving | GPU Edition, Custom Runtime |

---

## Repository

[https://github.com/jshin-jackson/sample-amp](https://github.com/jshin-jackson/sample-amp)
