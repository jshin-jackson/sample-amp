"""
CML Application Launcher for Streamlit
=======================================
CML's container runs a proxy as PID 1 that already owns CDSW_APP_PORT.
PID 1 cannot be killed (OS-protected). The proxy forwards external
traffic from CDSW_APP_PORT to the application's internal port.

Streamlit must listen on its own internal port (8501 default),
NOT on CDSW_APP_PORT which belongs to the CML proxy.
"""

import os
import sys

# Do NOT use CDSW_APP_PORT — it is owned by CML's proxy (PID 1).
# Use Streamlit's default internal port instead.
port = "8501"

print(f"[launcher] Starting Streamlit on internal port {port}")
print(f"[launcher] CML proxy (PID 1) handles external traffic on CDSW_APP_PORT")

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
