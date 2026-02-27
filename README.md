# Hello World AMP

> Level 0 - The simplest possible Cloudera AI AMP example.

## Overview

This AMP is designed as a starting point for learning how to build and deploy
Applied ML Prototypes (AMPs) on Cloudera AI. It runs a single session that
installs dependencies and prints a Hello World message.

## Project Structure

```
sample-amp/
├── .project-metadata.yaml          # AMP runbook (required)
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
└── 0_session-hello-world/
    └── hello_world.py               # Session script
```

## AMP Task Flow

```
[AMP Catalog Install]
        ↓
[run_session: hello_world.py]
        ↓
  1. Install dependencies (requirements.txt)
  2. Print environment info (Python version, platform)
  3. Print Hello World message
```

## Runtime

| Property | Value        |
|----------|--------------|
| Editor   | Workbench    |
| Kernel   | Python 3.11  |
| Edition  | Standard     |
| CPU      | 1 vCPU       |
| Memory   | 2 GB         |

## How to Install

1. In Cloudera AI, go to **AMPs** in the left panel.
2. Add this repository as a custom AMP catalog source (Site Administration > AMPs).
3. Click the **Hello World AMP** tile and then **Configure Project**.
4. Click **Launch Project** and wait for the session to complete.

## Learning Path

This is **Level 0** of a progressive AMP learning series:

| Level | Description                              |
|-------|------------------------------------------|
| 0     | Hello World (this AMP) — `run_session`   |
| 1     | Add a Job — `create_job` / `run_job`     |
| 2     | Deploy a Model — `create_model`          |
| 3     | Launch an Application — `start_application` |
