"""
perform_exec_restart.py
----------------------
Provides perform_exec_restart() to restart the application process.
"""
import os
import sys
import subprocess
from modules.write_pid_file import write_pid_file

def perform_exec_restart():
    """Spawn a fresh process running the same script then exit current one."""
    script_path = os.path.abspath(sys.argv[0])
    write_pid_file()  # refresh our pid timestamp
    args = [sys.executable, script_path] + sys.argv[1:]
    try:
        subprocess.Popen(args, cwd=os.path.dirname(script_path))
    finally:
        os._exit(0)
