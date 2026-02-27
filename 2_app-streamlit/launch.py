"""
CML Application Launcher for Streamlit
=======================================
IPython kernels (used by CML) run their own asyncio event loop.
Calling stcli.main() directly raises:
  RuntimeError: asyncio.run() cannot be called from a running event loop

Fix: run Streamlit inside a separate thread with its own event loop,
fully isolated from IPython's event loop.
"""

import asyncio
import os
import sys
import threading

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


def run_streamlit():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from streamlit.web import cli as stcli
    stcli.main()


thread = threading.Thread(target=run_streamlit)
thread.start()
thread.join()
