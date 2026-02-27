"""
CML Application Launcher for Streamlit
=======================================
CML runs Application scripts via Python interpreter (python script.py).
Streamlit must be started with `streamlit run` and must listen on
CDSW_APP_PORT assigned by CML. This launcher handles both requirements.
"""

import os
import subprocess
import sys
import time

port = os.environ.get("CDSW_APP_PORT", "8100")

# Kill any existing Streamlit processes before starting a new one.
# 'fuser' is not available in CML runtime containers; use 'pkill' instead.
subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
time.sleep(2)

subprocess.run(
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
    ]
)
