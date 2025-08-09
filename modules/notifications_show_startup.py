"""
notifications_show_startup.py
-----------------------------
Defines show_startup_toast() which displays a startup toast when monitoring
begins.
"""
from __future__ import annotations
from .notifications_toast_backend import show_toast

def show_startup_toast():
    show_toast("Auto-Unzip", "Started monitoring.")
