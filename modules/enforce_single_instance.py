"""
enforce_single_instance.py
-------------------------
Provides enforce_single_instance() to ensure only one active instance of the app.
"""
import os
from modules.read_pid_file import read_pid_file
from modules.kill_pid import kill_pid
from modules.write_pid_file import write_pid_file
import sys

def enforce_single_instance():
    existing = read_pid_file()
    current = os.getpid()
    remaining: list[int] = []
    for pid in existing:
        if pid == current:
            continue
        kill_pid(pid)
    remaining.append(current)
    write_pid_file(remaining)
