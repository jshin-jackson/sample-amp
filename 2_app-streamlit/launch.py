"""
CML Application Launcher for Streamlit — Diagnostic Mode
"""

import os
import subprocess
import sys

port = "8501"

print("=" * 60)
print("  CML Streamlit Launcher — Diagnostics")
print("=" * 60)
print(f"  cwd            : {os.getcwd()}")
print(f"  sys.executable : {sys.executable}")
print(f"  port           : {port}")
print(f"  app.py exists  : {os.path.exists('2_app-streamlit/app.py')}")

# ── Test 1: Is streamlit installed? ───────────────────────────────────────────
r1 = subprocess.run(
    [sys.executable, "-m", "streamlit", "--version"],
    capture_output=True, text=True, timeout=15,
)
print(f"\n[test1] streamlit --version (rc={r1.returncode})")
print(f"  stdout : {r1.stdout.strip()}")
print(f"  stderr : {r1.stderr.strip()[:300]}")

# ── Test 2: Does app.py have syntax errors? ───────────────────────────────────
r2 = subprocess.run(
    [sys.executable, "-m", "py_compile", "2_app-streamlit/app.py"],
    capture_output=True, text=True, timeout=15,
)
print(f"\n[test2] py_compile app.py (rc={r2.returncode})")
print(f"  stderr : {r2.stderr.strip()[:300] or 'OK'}")

# ── Test 3: Dry-run streamlit (capture first 5s of output) ────────────────────
print(f"\n[test3] Starting Streamlit (capturing output)...")
proc = subprocess.Popen(
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
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

import time
start = time.time()
output_lines = []

while time.time() - start < 10:
    line = proc.stdout.readline()
    if line:
        print(f"  [st] {line}", end="")
        output_lines.append(line)
        if "You can now view your Streamlit app" in line:
            print("\n[launcher] Streamlit started successfully — keeping alive")
            proc.wait()
            break
    elif proc.poll() is not None:
        print(f"\n[launcher] Streamlit exited (rc={proc.returncode}) after {time.time()-start:.1f}s")
        remaining = proc.stdout.read()
        if remaining:
            print(remaining[:500])
        break
