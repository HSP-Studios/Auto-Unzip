"""
notifications_show_startup.py
-----------------------------
Defines show_startup_toast() to display a toast notification (fallback to console).
"""
from .notifications_toast_backend import show_toast

def show_startup_toast():
    show_toast("Auto-Unzip", "Started monitoring.")
