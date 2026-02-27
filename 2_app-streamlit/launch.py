"""
CML Application Launcher for Streamlit — Port Discovery
"""

import os
import subprocess
import sys

# ── Print all environment variables to find correct internal port ─────────────
print("=" * 60)
print("  ALL ENVIRONMENT VARIABLES")
print("=" * 60)
for key, val in sorted(os.environ.items()):
    print(f"  {key}={val}")
print("=" * 60)
sys.stdout.flush()

# ── Try common CML internal ports: 8080 → 8888 → 8501 ────────────────────────
import socket

def find_free_port(candidates):
    for p in candidates:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", p))
            s.close()
            return p
        except OSError:
            print(f"[launcher] Port {p} is busy, trying next...")
    return None

candidates = [8080, 8888, 8501, 8502, 9000]
port = find_free_port(candidates)

if port is None:
    print("[launcher] ERROR: No free port found!")
    sys.exit(1)

print(f"[launcher] Using port {port}")
sys.stdout.flush()

proc = subprocess.Popen(
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true",
    ]
)

print(f"[launcher] Streamlit PID={proc.pid} on port {port}. Waiting...")
sys.stdout.flush()
proc.wait()
print(f"[launcher] Streamlit exited (rc={proc.returncode})")
