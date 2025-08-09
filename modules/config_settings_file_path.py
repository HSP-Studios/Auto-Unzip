"""
config_settings_file_path.py
----------------------------
Provides get_settings_file_path() which returns the file path where the
application stores its persistent JSON configuration.
"""
import os

def get_settings_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'settings.json')
