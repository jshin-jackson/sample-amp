# CML Application Launcher for Streamlit
# Use IPython '!' magic on a single line — CML's python.dedent parser crashes on backslash continuations.
# --server.address 127.0.0.1 avoids port conflict with CML's proxy (PID 1) which binds to the external container IP.

!streamlit run 2_app-streamlit/app.py --server.port $CDSW_APP_PORT --server.address 127.0.0.1 --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false --server.headless true
