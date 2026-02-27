"""
CML Application Launcher for Streamlit
=======================================
CML runs Application scripts via Python interpreter (python script.py).
Streamlit must be started with `streamlit run` and must listen on
CDSW_APP_PORT assigned by CML. This launcher handles both requirements.
"""

import os
import signal
import subprocess
import sys
import time


def kill_process_on_port(port_num: int):
    """
    Kill the process listening on port_num using the /proc filesystem.
    This is a pure-Python approach that works in any Linux container
    regardless of which system tools (fuser, lsof, ss) are installed.
    """
    hex_port = format(port_num, "04X")
    target_inode = None

    # Step 1: Find the socket inode for the port in /proc/net/tcp
    try:
        with open("/proc/net/tcp") as f:
            for line in f.readlines()[1:]:
                fields = line.strip().split()
                if len(fields) < 10:
                    continue
                local_port_hex = fields[1].split(":")[1]
                if local_port_hex == hex_port:
                    target_inode = fields[9]
                    break
    except Exception as e:
        print(f"[launcher] Could not read /proc/net/tcp: {e}")
        return

    if not target_inode:
        print(f"[launcher] Port {port_num} is free.")
        return

    # Step 2: Scan all /proc/{pid}/fd/ to find the process owning that inode
    for pid_str in os.listdir("/proc"):
        if not pid_str.isdigit():
            continue
        fd_dir = f"/proc/{pid_str}/fd"
        try:
            for fd in os.listdir(fd_dir):
                try:
                    link = os.readlink(f"{fd_dir}/{fd}")
                    if f"socket:[{target_inode}]" in link:
                        pid = int(pid_str)
                        print(f"[launcher] Killing PID {pid} holding port {port_num}")
                        os.kill(pid, signal.SIGKILL)
                        time.sleep(2)
                        return
                except OSError:
                    continue
        except (PermissionError, FileNotFoundError):
            continue

    print(f"[launcher] Could not resolve PID for port {port_num}.")


port = int(os.environ.get("CDSW_APP_PORT", "8100"))

kill_process_on_port(port)

subprocess.run(
    [
        sys.executable, "-m", "streamlit", "run",
        "2_app-streamlit/app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
    ]
)
