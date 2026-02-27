"""
CML Application Launcher for Streamlit
=======================================
Uses os.execv() to replace the IPython kernel process with Streamlit.
Streamlit runs directly on CDSW_APP_PORT so CML's health check passes.

NOTE: If the Application shows 'Starting' after many failed restart
attempts, delete the Application from CML UI and redeploy the AMP.
Accumulated orphan processes from previous runs may hold the port.
A fresh container (new deployment) will always work correctly.
"""

import os
import sys

port = os.environ.get("CDSW_APP_PORT", "8100")

print(f"[launcher] Replacing kernel with Streamlit on port {port}")

os.execv(
    sys.executable,
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true",
    ],
)
