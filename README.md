# Hello World AMP

> **Level 3** — Cloudera AI AMP Beginner Series: Advanced Environment Variables

A hands-on reference AMP for learning Cloudera AI (CML) fundamentals. This prototype builds on Level 2 (Session + Job + Application) and demonstrates how to use **required** and **optional environment variables** to control runtime behavior of a deployed application.

---

## Overview

| Task Type | Script | Purpose |
|---|---|---|
| `run_session` | `0_session-install-deps/install_deps.py` | Install & verify Python packages |
| `create_job` + `run_job` | `1_job-data-report/report.py` | Generate a data summary report |
| `start_application` | `2_app-streamlit/launch.py` | Launch the Streamlit dashboard |

---

## What's New in Level 3

Level 3 introduces three new environment variables that demonstrate different patterns for configuring AMP behavior at deploy time:

| Variable | Type | Default | Pattern |
|---|---|---|---|
| `DASHBOARD_TITLE` | **Required** | _(none)_ | App validates at startup; shows error if missing |
| `SCORE_ALERT_THRESHOLD` | Optional | `80` | Integer config; changes dashboard content |
| `ENABLE_RAW_DATA_DOWNLOAD` | Optional | `true` | Boolean flag; controls UI feature visibility |

### Required vs. Optional Environment Variables

```
Required  →  No default in .project-metadata.yaml
           →  App checks os.environ.get(...) == "" and calls st.stop()
           →  User MUST provide a value before the app works

Optional  →  Has a sensible default in .project-metadata.yaml
           →  App uses the default if not set
           →  User CAN override to customize behavior
```

---

## Project Structure

```
sample-amp/
├── .project-metadata.yaml              # AMP runbook — tasks, runtime, env vars
├── catalog.yaml                         # AMP Catalog registration metadata
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
├── assets/
│   └── cover.png                        # Catalog tile image
├── 0_session-install-deps/
│   └── install_deps.py                  # Session: pip install + package verification
├── 1_job-data-report/
│   └── report.py                        # Job: pandas data processing → CSV + JSON output
└── 2_app-streamlit/
    ├── launch.py                        # Application launcher (IPython magic entry point)
    └── app.py                           # Streamlit dashboard UI (Level 3 env vars)
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
│  - Validates DASHBOARD_TITLE is set (required)       │
│  - Reads outputs/ files produced by the Job          │
│  - Highlights products above SCORE_ALERT_THRESHOLD   │
│  - Shows/hides download based on ENABLE_RAW_DATA_DOWNLOAD │
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

### Level 2 — File I/O Configuration

| Variable | Default | Required | Description |
|---|---|---|---|
| `REPORT_OUTPUT_DIR` | `outputs` | No | Directory where the job saves report files |
| `REPORT_NAME` | `data_report` | No | Base filename for the generated report (no extension) |

### Level 3 — Dashboard Runtime Configuration

| Variable | Default | Required | Description |
|---|---|---|---|
| `DASHBOARD_TITLE` | _(none)_ | **Yes** | Custom title shown in the dashboard header. App will not start without this. |
| `SCORE_ALERT_THRESHOLD` | `80` | No | Integer. Products with usage score ≥ this value are shown as High Performers. |
| `ENABLE_RAW_DATA_DOWNLOAD` | `true` | No | Set to `false` to hide the CSV download button. |

---

## Output Files

| File | Format | Description |
|---|---|---|
| `outputs/data_report.csv` | CSV | Full sample dataset (5 rows × 4 columns) |
| `outputs/data_report.json` | JSON | Summary statistics (mean, max, top product, etc.) |

---

## Dashboard Features

| Section | Description |
|---|---|
| **KPI Metrics** | Total Users, Average Score, Top Product, Product Count |
| **High Performers** _(Level 3)_ | Products with score ≥ `SCORE_ALERT_THRESHOLD`, shown as metric cards with delta |
| **Bar Chart** | Usage Score per product |
| **Category Table** | Active User count grouped by category |
| **Raw Data** | Expandable full dataset with 🏆 badge for high performers and optional CSV download |

---

## Environment Variable Patterns in Code

### Pattern 1 — Required Variable with Validation

```python
DASHBOARD_TITLE = os.environ.get("DASHBOARD_TITLE", "")

if not DASHBOARD_TITLE:
    st.error("Required environment variable `DASHBOARD_TITLE` is not set. ...")
    st.stop()
```

### Pattern 2 — Optional Integer Variable

```python
SCORE_ALERT_THRESHOLD = int(os.environ.get("SCORE_ALERT_THRESHOLD", "80"))
```

### Pattern 3 — Optional Boolean Flag

```python
ENABLE_RAW_DATA_DOWNLOAD = os.environ.get("ENABLE_RAW_DATA_DOWNLOAD", "true").lower() == "true"
```

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
| `!` (single line) | — | CML's `python.dedent` parser crashes on `!` magic with backslash line continuations. |

---

## How to Deploy

### From the AMP Catalog
1. In Cloudera AI, go to **AMPs** in the left navigation panel.
2. Find **Hello World AMP** and click **Deploy**.
3. Set the **required** environment variable:
   - `DASHBOARD_TITLE` — e.g. `My Team's Data Report Dashboard`
4. Optionally override other variables.
5. Click **Launch Project** and wait for all 4 tasks to complete.
6. Go to **Applications** menu → open **Data Report Dashboard**.

### Redeployment Notes
- If you need to redeploy the Application task, always **Delete** the existing Application first (do not just Restart).
- This ensures a clean container with no orphaned processes from previous runs.

---

## Learning Path

| Level | Title | What's Introduced |
|---|---|---|
| 0 | Hello World Session | `run_session` |
| 1 | Session + Batch Job | `create_job`, `run_job` |
| 2 | Session + Job + App | `start_application`, Streamlit |
| **3** | **Advanced Env Vars** ← *this AMP* | Required env var validation, Boolean/Integer type conversion |
| 4 | Model Deployment | `create_model`, `build_model`, `deploy_model` |
| 5 | GPU / LLM Serving | GPU Edition, Custom Runtime |

---

## Repository

[https://github.com/jshin-jackson/sample-amp](https://github.com/jshin-jackson/sample-amp)
