"""
notifications_show_progress.py
------------------------------
Defines show_progress_toast() which displays an intermittent toast at major
progress milestones (0%, 50%, 100%) to avoid spamming notifications. For
intermediate updates it logs to console only.
"""
from __future__ import annotations
from .notifications_toast_backend import show_toast

_milestones = {0, 50, 100}

def show_progress_toast(archive_name: str, percent: float):
    rounded = int(percent)
    msg = f"Extracting {archive_name} - {rounded}%"
    if rounded in _milestones:
        show_toast("Auto-Unzip", msg)
    else:
        print(f"[Auto-Unzip] {msg}")
