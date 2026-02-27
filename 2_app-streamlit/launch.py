"""
CML Application Launcher for Streamlit
=======================================
Runs Streamlit via its internal Python API (not subprocess) so that
CML's process termination also kills Streamlit — eliminating the
'Port already in use' error caused by orphaned subprocesses.
"""

import os
import sys

port = os.environ.get("CDSW_APP_PORT", "8100")

sys.argv = [
    "streamlit", "run",
    "2_app-streamlit/app.py",
    "--server.port", port,
    "--server.address", "0.0.0.0",
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false",
    "--browser.gatherUsageStats", "false",
    "--server.headless", "true",
]

from streamlit.web import cli as stcli
stcli.main()
