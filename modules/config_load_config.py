"""
config_load_config.py
---------------------
Provides load_config() to load settings from disk and return a Config instance
(or defaults if the file is missing or invalid).
"""
import json
import os
from .config_dataclass import Config
from .config_settings_file_path import get_settings_file_path

def load_config() -> Config:
    path = get_settings_file_path()
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Config(**data)
        except Exception:
            return Config()
    return Config()
