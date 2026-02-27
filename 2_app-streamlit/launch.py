"""
CML Application Launcher for Streamlit
=======================================
- Keep Python process alive (CML monitors it as the application process)
- Run Streamlit as a child process on port 8501 (CDSW_APP_PORT is owned by CML proxy)
- Stream Streamlit output directly to CML Application Logs (no capture)
"""

import os
import subprocess
import sys

port = os.environ.get("CDSW_APP_PORT", "8100")

print(f"[launcher] CDSW_APP_PORT={port}")
print(f"[launcher] Starting Streamlit on port {port}...")
sys.stdout.flush()

proc = subprocess.Popen(
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true",
    ]
    # stdout/stderr not captured → goes directly to CML Application Logs
)

print(f"[launcher] Streamlit PID={proc.pid}. Waiting...")
sys.stdout.flush()

proc.wait()

print(f"[launcher] Streamlit exited (rc={proc.returncode})")
