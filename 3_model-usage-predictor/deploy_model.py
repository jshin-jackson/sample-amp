"""
Level 4 - Model Build & Deploy via cmlapi
==========================================
This script runs as a CML Session task (run_session).

Background:
  In CML 2.0.55, the AMP 'create_model' task creates an empty model shell
  without file/function/runtime information. As a result, 'build_model' has
  nothing to build and fails silently. This script replaces all three AMP
  model tasks (create_model, build_model, deploy_model) using the CML Python
  SDK (cmlapi) directly.

What this script does:
  1. Deletes any existing model with the same name (clean slate)
  2. Creates the model with file, function, and runtime_identifier
  3. Triggers a build and waits for it to complete
  4. Deploys the built model and waits until it is Running

Runtime Image used (matches the manual deployment that succeeded):
  docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-pbj-workbench-python3.11-standard:2026.01.1-b6
"""

import os
import time

import cmlapi

# ── Configuration ──────────────────────────────────────────────────────────────
MODEL_NAME         = "Usage Score Predictor"
MODEL_FILE         = "3_model-usage-predictor/predict.py"
MODEL_FUNCTION     = "predict"
MODEL_RUNTIME      = "docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-pbj-workbench-python3.11-standard:2026.01.1-b6"
BUILD_COMMENT      = "AMP automated build via cmlapi"
DEPLOY_CPU         = 2
DEPLOY_MEMORY      = 4
DEPLOY_REPLICAS    = 1

BUILD_TIMEOUT_SEC  = 900   # 15 min
DEPLOY_TIMEOUT_SEC = 300   # 5 min
POLL_INTERVAL_SEC  = 15

PROJECT_ID = os.environ["CDSW_PROJECT_ID"]

# ── Helpers ────────────────────────────────────────────────────────────────────

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def wait_for_build(client, project_id, model_id, build_id, timeout):
    log(f"Waiting for build {build_id} to complete (timeout: {timeout}s)...")
    elapsed = 0
    while elapsed < timeout:
        b = client.get_model_build(project_id=project_id, model_id=model_id, build_id=build_id)
        log(f"  build status: {b.status}")
        if b.status in ("built", "succeeded"):
            return b
        if b.status in ("failed", "error", "build failed", "timedout"):
            raise RuntimeError(f"Build failed with status: {b.status}")
        time.sleep(POLL_INTERVAL_SEC)
        elapsed += POLL_INTERVAL_SEC
    raise TimeoutError(f"Build did not complete within {timeout}s")


def wait_for_deploy(client, project_id, model_id, deployment_id, timeout):
    log(f"Waiting for deployment {deployment_id} to become running (timeout: {timeout}s)...")
    elapsed = 0
    while elapsed < timeout:
        d = client.get_model_deployment(
            project_id=project_id,
            model_id=model_id,
            deployment_id=deployment_id,
        )
        log(f"  deployment status: {d.status}")
        if d.status == "running":
            return d
        if d.status in ("failed", "error", "stopped"):
            raise RuntimeError(f"Deployment failed with status: {d.status}")
        time.sleep(POLL_INTERVAL_SEC)
        elapsed += POLL_INTERVAL_SEC
    raise TimeoutError(f"Deployment did not become running within {timeout}s")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    client = cmlapi.default_client()

    log(f"Project ID: {PROJECT_ID}")

    # Step 1: Delete existing model if present
    log(f"Checking for existing model '{MODEL_NAME}'...")
    models = client.list_models(project_id=PROJECT_ID)
    for m in models.models:
        if m.name == MODEL_NAME:
            log(f"  Deleting existing model: {m.id}")
            client.delete_model(project_id=PROJECT_ID, model_id=m.id)
            time.sleep(5)
            log("  Deleted.")
            break

    # Step 2: Create model with full configuration
    log(f"Creating model '{MODEL_NAME}'...")
    model = client.create_model(
        project_id=PROJECT_ID,
        CreateModelRequest={
            "name": MODEL_NAME,
            "description": "Predicts usage score from active user count (LinearRegression)",
            "file_path": MODEL_FILE,
            "function_name": MODEL_FUNCTION,
            "runtime_identifier": MODEL_RUNTIME,
        },
    )
    log(f"  Model created: id={model.id}")

    # Step 3: Trigger build
    log("Triggering model build...")
    build = client.create_model_build(
        project_id=PROJECT_ID,
        model_id=model.id,
        CreateModelBuildRequest={
            "comment": BUILD_COMMENT,
            "file_path": MODEL_FILE,
            "function_name": MODEL_FUNCTION,
            "runtime_identifier": MODEL_RUNTIME,
        },
    )
    log(f"  Build created: id={build.id}")

    # Step 4: Wait for build
    wait_for_build(client, PROJECT_ID, model.id, build.id, BUILD_TIMEOUT_SEC)
    log("Build completed successfully.")

    # Step 5: Deploy
    log("Deploying model...")
    deployment = client.create_model_deployment(
        project_id=PROJECT_ID,
        model_id=model.id,
        build_id=build.id,
        CreateModelDeploymentRequest={
            "cpu": DEPLOY_CPU,
            "memory": DEPLOY_MEMORY,
            "replicas": DEPLOY_REPLICAS,
        },
    )
    log(f"  Deployment created: id={deployment.id}")

    # Step 6: Wait for deployment
    wait_for_deploy(client, PROJECT_ID, model.id, deployment.id, DEPLOY_TIMEOUT_SEC)

    log("=" * 55)
    log("Model deployment SUCCEEDED!")
    log(f"  Model ID     : {model.id}")
    log(f"  Build ID     : {build.id}")
    log(f"  Deployment ID: {deployment.id}")
    log("Test: Models → Usage Score Predictor → Test tab")
    log('Input: {"active_users": 350}')
    log("=" * 55)


if __name__ == "__main__":
    main()
