# Hello World AMP

> Level 2 - Session + Job + Streamlit Application example for Cloudera AI AMP beginners.

## Overview

This AMP demonstrates three core Cloudera AI task types in sequence:

- **`run_session`** — Installs Python dependencies (one-time setup)
- **`create_job` + `run_job`** — Creates and executes a batch data report job
- **`start_application`** — Launches an interactive Streamlit dashboard

## Project Structure

```
sample-amp/
├── .project-metadata.yaml              # AMP runbook (required)
├── catalog.yaml                         # AMP catalog registration
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
├── assets/
│   └── cover.png                        # Catalog tile image
├── 0_session-install-deps/
│   └── install_deps.py                  # Session: install & verify packages
├── 1_job-data-report/
│   └── report.py                        # Job: generate data summary report
└── 2_app-streamlit/
    └── app.py                           # Application: Streamlit dashboard
```

## AMP Task Flow

```
[AMP Deploy]
      ↓
[run_session] 0_session-install-deps/install_deps.py
  1. pip install -r requirements.txt (requests, pandas, streamlit)
  2. Verify imported packages
  3. Print runtime environment info
      ↓
[create_job] Data Report Job  ← registered in CML Jobs menu
      ↓
[run_job] 1_job-data-report/report.py
  1. Create sample dataset with pandas
  2. Compute summary statistics
  3. Save outputs/data_report.csv
  4. Save outputs/data_report.json
      ↓
[start_application] 2_app-streamlit/app.py
  → Reads outputs/ files from the Job
  → Displays KPI metrics, bar chart, category table
  → Accessible at https://hello-world-amp.{workspace-domain}
```

## Runtime

| Property | Value        |
|----------|--------------|
| Editor   | Workbench    |
| Kernel   | Python 3.11  |
| Edition  | Standard     |
| CPU      | 1 vCPU       |
| Memory   | 2 GB         |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `REPORT_OUTPUT_DIR` | `outputs` | Directory to save/read report files |
| `REPORT_NAME` | `data_report` | Base filename for generated reports |

## Output Files

| File | Description |
|---|---|
| `outputs/data_report.csv` | Raw dataset in CSV format |
| `outputs/data_report.json` | Summary statistics in JSON format |

## Dashboard Features

| Section | Description |
|---|---|
| KPI Metrics | Total Users, Avg Score, Top Product, Product Count |
| Bar Chart | Usage Score per product |
| Category Table | Active Users grouped by category |
| Raw Data | Expandable full dataset with CSV download button |

## How to Install

1. In Cloudera AI, go to **AMPs** in the left panel.
2. Find **Hello World AMP** and click **Deploy**.
3. Optionally set environment variables.
4. Click **Launch Project** and wait for all 4 tasks to complete.
5. Go to **Applications** menu to open the dashboard.

## Learning Path

| Level | Description | Task Types |
|-------|-------------|------------|
| 0 | Hello World | `run_session` |
| 1 | Session + Job | `run_session` + `create_job` / `run_job` |
| **2** | **Session + Job + App (this AMP)** | **+ `start_application`** |
| 3 | User Config via Env Vars | + `environment_variables` |
| 4 | Deploy a Model | + `create_model` / `build_model` / `deploy_model` |
| 5 | GPU + LLM Serving | GPU Edition + Custom Runtime |
