"""
CML Application Launcher for Streamlit
"""

import os
import signal
import socket
import sys
import time

# ── Diagnostics ───────────────────────────────────────────────────────────────

port_str = os.environ.get("CDSW_APP_PORT", "8100")
port = int(port_str)

print(f"[launcher] CDSW_APP_PORT = {port}")
print(f"[launcher] sys.executable = {sys.executable}")
print(f"[launcher] cwd = {os.getcwd()}")
print(f"[launcher] app script exists = {os.path.exists('2_app-streamlit/app.py')}")

# ── Wait until the port is free (max 30 s) ────────────────────────────────────

def is_port_free(p: int) -> bool:
    """Return True if we can bind the port (i.e. nothing else is using it)."""
    for family in (socket.AF_INET6, socket.AF_INET):
        try:
            s = socket.socket(family, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", p))
            s.close()
            return True
        except OSError:
            pass
    return False


def kill_owner(p: int):
    """Try to kill whatever process owns port p via /proc/net/tcp{,6}."""
    hex_port = format(p, "04X")
    for proc_file in ("/proc/net/tcp6", "/proc/net/tcp"):
        inode = None
        try:
            with open(proc_file) as f:
                for line in f.readlines()[1:]:
                    fields = line.strip().split()
                    if len(fields) >= 10 and fields[1].split(":")[-1] == hex_port:
                        inode = fields[9]
                        break
        except Exception:
            continue
        if not inode:
            continue
        for pid_str in os.listdir("/proc"):
            if not pid_str.isdigit():
                continue
            try:
                for fd in os.listdir(f"/proc/{pid_str}/fd"):
                    try:
                        if f"socket:[{inode}]" in os.readlink(f"/proc/{pid_str}/fd/{fd}"):
                            pid = int(pid_str)
                            print(f"[launcher] Sending SIGKILL to PID {pid} (owns port {p})")
                            os.kill(pid, signal.SIGKILL)
                            return
                    except OSError:
                        pass
            except (PermissionError, FileNotFoundError):
                pass


waited = 0
max_wait = 30

while not is_port_free(port) and waited < max_wait:
    print(f"[launcher] Port {port} is busy — attempting kill... ({waited}s/{max_wait}s)")
    kill_owner(port)
    time.sleep(2)
    waited += 2

if is_port_free(port):
    print(f"[launcher] Port {port} is free. Launching Streamlit...")
else:
    print(f"[launcher] WARNING: port {port} still busy after {max_wait}s. Launching anyway.")

# ── Replace this process with Streamlit ───────────────────────────────────────

os.execv(
    sys.executable,
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", port_str,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true",
    ],
)
