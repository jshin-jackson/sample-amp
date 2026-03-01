"""
Manual model build trigger using CML Python SDK.

Run this script in a CML Session if the AMP build_model task fails silently:
  - Lists models in the current project
  - Triggers a build via cmlapi
  - Polls build status until complete or failed

Usage:
  Run in a CML Session (the CDSW_PROJECT_ID env var is auto-injected).
"""

import os
import time
import cmlapi

PROJECT_ID = os.environ.get("CDSW_PROJECT_ID")
MODEL_NAME = "Usage Score Predictor"

client = cmlapi.default_client()

# ── Step 1: Find the model ─────────────────────────────────────────────────────
print(f"Project ID: {PROJECT_ID}")
print("Listing models...")

models = client.list_models(project_id=PROJECT_ID)
model = None
for m in models.models:
    print(f"  [{m.id}] {m.name}")
    if m.name == MODEL_NAME:
        model = m

if model is None:
    print(f"\nERROR: Model '{MODEL_NAME}' not found.")
    print("Please run the AMP Step 5 (create_model) first.")
    raise SystemExit(1)

print(f"\nFound model: {model.name} (id={model.id})")

# ── Step 2: Trigger build ──────────────────────────────────────────────────────
print("\nTriggering model build...")

build = client.create_model_build(
    project_id=PROJECT_ID,
    model_id=model.id,
    CreateModelBuildRequest={
        "comment": "Manual build via SDK",
        "file_path": "3_model-usage-predictor/predict.py",
        "function_name": "predict",
        "kernel": "python3",
    }
)

print(f"Build created: id={build.id}, status={build.status}")

# ── Step 3: Poll build status ──────────────────────────────────────────────────
print("\nPolling build status (this may take a few minutes)...")
print("-" * 50)

while True:
    b = client.get_model_build(
        project_id=PROJECT_ID,
        model_id=model.id,
        build_id=build.id,
    )
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] status: {b.status}")

    if b.status in ("built", "succeeded"):
        print("\nBuild SUCCEEDED!")
        print(f"Build ID: {b.id}")
        print("\nNext: go to Models → Usage Score Predictor → Deployments → Deploy")
        break
    elif b.status in ("failed", "error", "build failed"):
        print(f"\nBuild FAILED. Check Models → Builds → {b.id} for logs.")
        break

    time.sleep(15)
