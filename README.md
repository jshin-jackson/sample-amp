# Hello World AMP

> Level 1 - Session + Job example for Cloudera AI AMP beginners.

## Overview

This AMP demonstrates two core Cloudera AI task types:

- **`run_session`** — Installs Python dependencies (one-time setup)
- **`create_job` + `run_job`** — Creates and executes a batch data report job

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
└── 1_job-data-report/
    └── report.py                        # Job: generate data summary report
```

## AMP Task Flow

```
[AMP Deploy]
      ↓
[run_session] 0_session-install-deps/install_deps.py
  1. pip install -r requirements.txt
  2. Verify imported packages (requests, pandas)
  3. Print runtime environment info
      ↓
[create_job] Data Report Job  ← registered in CML Jobs menu
      ↓
[run_job] 1_job-data-report/report.py
  1. Create sample dataset with pandas
  2. Compute summary statistics
  3. Save outputs/data_report.csv
  4. Save outputs/data_report.json
  5. Print report to Job log
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
| `REPORT_OUTPUT_DIR` | `outputs` | Directory to save report files |
| `REPORT_NAME` | `data_report` | Base filename for generated reports |

## Output Files

After the Job runs, the following files are saved in the project filesystem:

| File | Description |
|---|---|
| `outputs/data_report.csv` | Raw dataset in CSV format |
| `outputs/data_report.json` | Summary statistics in JSON format |

## How to Install

1. In Cloudera AI, go to **AMPs** in the left panel.
2. Find **Hello World AMP** and click **Deploy**.
3. Optionally set `REPORT_OUTPUT_DIR` or `REPORT_NAME` environment variables.
4. Click **Launch Project** and wait for the session and job to complete.
5. Check **Jobs** menu to view the run history and logs.

## Learning Path

| Level | Description | Task Types |
|-------|-------------|------------|
| 0 | Hello World | `run_session` |
| **1** | **Session + Job (this AMP)** | **`run_session` + `create_job` / `run_job`** |
| 2 | Add an Application | + `start_application` |
| 3 | User Config via Env Vars | + `environment_variables` |
| 4 | Deploy a Model | + `create_model` / `build_model` / `deploy_model` |
| 5 | GPU + LLM Serving | GPU Edition + Custom Runtime |
