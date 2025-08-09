"""
notifications_show_progress.py
------------------------------
Defines show_progress_toast() to display limited toast notifications for progress.
"""
from .notifications_toast_backend import show_toast

_last_shown = {}

def show_progress_toast(archive_name: str, percent: float):
    """Show toast at 0, 50, 100 percent to reduce notification noise."""
    rounded = int(percent)
    key = archive_name
    should = rounded in (0, 50, 100)
    if should:
        last = _last_shown.get(key)
        if last == rounded:
            return
        _last_shown[key] = rounded
        show_toast("Auto-Unzip", f"Extracting {archive_name} - {rounded}%")
