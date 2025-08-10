"""
kill_pid.py
-----------
Provides kill_pid() to attempt to terminate a process by PID.
"""
import os
import sys
import time
import signal
import subprocess

def kill_pid(pid: int):
    if pid == os.getpid():
        return
    try:
        os.kill(pid, 0)
    except Exception:
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass
    time.sleep(0.2)
    try:
        os.kill(pid, 0)
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
