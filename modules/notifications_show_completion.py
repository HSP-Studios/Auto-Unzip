"""
notifications_show_completion.py
--------------------------------
Defines show_completion_toast() which displays a toast for success or failure
of archive extraction.
"""
from __future__ import annotations
from .notifications_toast_backend import show_toast

def show_completion_toast(archive_name: str, success: bool, target_dir: str):
    title = "Auto-Unzip" if success else "Auto-Unzip Error"
    body = f"Extracted {archive_name} to {target_dir}" if success else f"Failed to extract {archive_name}"
    show_toast(title, body)
