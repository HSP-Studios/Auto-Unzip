"""
config_default_downloads_folder.py
----------------------------------
Provides default_downloads_folder() which returns the path to the current
user's Downloads directory (best-effort). This is used as the initial folder
that the application watches for new archive files.
"""
import os

def default_downloads_folder() -> str:
    """Return the path to the user's Downloads folder."""
    return os.path.join(os.path.expanduser('~'), 'Downloads')
