"""
notifications_show_completion.py
--------------------------------
Defines show_completion_toast() to display a completion toast notification.
"""
from .notifications_toast_backend import show_toast

def show_completion_toast(archive_name: str, success: bool, target_dir: str):
    title = "Success" if success else "Error"
    body = f"Extracted to {target_dir}" if success else f"Failed to extract {archive_name}"
    show_toast(f"Auto-Unzip {title}", body)
