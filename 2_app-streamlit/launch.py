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

port = os.environ.get("CDSW_APP_PORT", "8100")

# Release the port if it is already occupied by a previous instance.
# This can happen when CML restarts the application before the old
# process has fully terminated.
subprocess.run(
    f"fuser -k {port}/tcp",
    shell=True,
    capture_output=True,
)

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
