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
from pathlib import Path

port = os.environ.get("CDSW_APP_PORT", "8100")
app_script = Path(__file__).parent / "app.py"

subprocess.run(
    [
        sys.executable, "-m", "streamlit", "run",
        str(app_script),
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
    ],
    check=True,
)
