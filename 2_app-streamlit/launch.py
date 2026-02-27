"""
CML Application Launcher for Streamlit
=======================================
Uses os.execv() to REPLACE the current IPython kernel process with
Streamlit — no subprocess, no asyncio conflict, no orphaned processes.

When CML stops/restarts the Application, it kills this process directly
(which IS Streamlit), freeing the port immediately for the next start.
"""

import os
import sys

port = os.environ.get("CDSW_APP_PORT", "8100")

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
