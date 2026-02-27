# CML Application Launcher for Streamlit
#
# Key: use --server.address 127.0.0.1 (loopback), NOT 0.0.0.0
# CML's container proxy (PID 1) binds to the external container IP on
# CDSW_APP_PORT. Streamlit binds to 127.0.0.1 on the same port — no conflict.
# The '!' IPython magic keeps the kernel alive while Streamlit runs.

!streamlit run 2_app-streamlit/app.py \
    --server.port $CDSW_APP_PORT \
    --server.address 127.0.0.1 \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false \
    --server.headless true
