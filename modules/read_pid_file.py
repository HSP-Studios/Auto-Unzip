"""
read_pid_file.py
----------------
Provides read_pid_file() to read process IDs from the PID file.
"""
import os

PID_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'auto_unzip.pid')

def read_pid_file() -> list[int]:
    try:
        with open(PID_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if not content:
            return []
        return [int(p) for p in content.split(',') if p.strip().isdigit()]
    except Exception:
        return []
