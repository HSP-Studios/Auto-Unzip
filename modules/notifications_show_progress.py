"""
notifications_show_progress.py
------------------------------
Defines show_progress_toast() to print progress to console only.
"""
def show_progress_toast(archive_name: str, percent: float):
    msg = f"Extracting {archive_name} - {percent:.0f}%"
    print(f"[Auto-Unzip] {msg}")
