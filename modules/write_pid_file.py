"""
write_pid_file.py
----------------
Provides write_pid_file() to write the current process ID to the PID file.
"""
import os
import sys

PID_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'auto_unzip.pid')

def write_pid_file(pids: list[int] | None = None):
    try:
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        if pids is None:
            pids = [os.getpid()]
        with open(PID_FILE, 'w', encoding='utf-8') as f:
            f.write(','.join(str(p) for p in pids))
    except Exception:
        pass
